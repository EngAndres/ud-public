from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sqs as sqs,
)
from constructs import Construct


class ImageModerationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "ImagesBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,   # lab only
            auto_delete_objects=True,               # lab only
        )

        table = dynamodb.Table(
            self, "DecisionsTable",
            partition_key=dynamodb.Attribute(name="imageKey", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,   # lab only
        )

        # Dead-letter queue catches messages that fail repeatedly.
        dlq = sqs.Queue(
            self, "ReviewDlq",
            encryption=sqs.QueueEncryption.SQS_MANAGED,
            enforce_ssl=True,
        )
        review_queue = sqs.Queue(
            self, "ReviewQueue",
            encryption=sqs.QueueEncryption.SQS_MANAGED,
            enforce_ssl=True,
            visibility_timeout=Duration.seconds(60),
            dead_letter_queue=sqs.DeadLetterQueue(queue=dlq, max_receive_count=5),
        )

        fn = _lambda.Function(
            self, "ModerateFn",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="moderate.handler",             # file lambda/moderate.py, function handler
            code=_lambda.Code.from_asset("lambda"),
            memory_size=512,
            timeout=Duration.seconds(30),
            log_group=logs.LogGroup(
                self, "ModerateLogs",
                retention=logs.RetentionDays.ONE_WEEK,
                removal_policy=RemovalPolicy.DESTROY,   # lab only
            ),
            dead_letter_queue=dlq,          # failed asynchronous invocations are kept, not lost
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": table.table_name,
                "QUEUE_URL": review_queue.queue_url,
                "BLOCK_THRESHOLD": "90",
                "REVIEW_THRESHOLD": "60",
            },
        )

        bucket.grant_read_write(fn)         # read the upload, copy, and delete
        table.grant_write_data(fn)
        review_queue.grant_send_messages(fn)
        fn.add_to_role_policy(iam.PolicyStatement(
            actions=["rekognition:DetectModerationLabels"],
            resources=["*"],                # no resource-level permissions for this API
        ))

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(fn),
            s3.NotificationKeyFilter(prefix="uploads/"),
        )

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "TableName", value=table.table_name)
        CfnOutput(self, "ReviewQueueUrl", value=review_queue.queue_url)
