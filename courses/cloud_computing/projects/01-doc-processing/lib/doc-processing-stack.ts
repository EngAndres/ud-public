import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subs from 'aws-cdk-lib/aws-sns-subscriptions';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as sqs from 'aws-cdk-lib/aws-sqs';

export interface DocProcessingStackProps extends cdk.StackProps {
  reviewerEmail: string;
}

// New class
export class DocProcessingStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: DocProcessingStackProps) {
    super(scope, id, props);

    // Requests and results. Encrypted, private, and versioned.
    const bucket = new s3.Bucket(this, 'RequestsBucket', {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,   // lab only
      autoDeleteObjects: true,                    // lab only
    });

    // One item per request.
    const table = new dynamodb.Table(this, 'RequestsTable', {
      partitionKey: { name: 'requestId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,   // lab only
    });

    // Human review channel.
    const reviewTopic = new sns.Topic(this, 'ReviewTopic', {
      displayName: 'Document review requests',
    });
    reviewTopic.addSubscription(new subs.EmailSubscription(props.reviewerEmail));

    // Failed asynchronous invocations (after the 2 automatic retries) are kept here.
    const dlq = new sqs.Queue(this, 'ProcessDocumentDlq', {
      encryption: sqs.QueueEncryption.SQS_MANAGED,
      enforceSSL: true,
    });

    const fn = new NodejsFunction(this, 'ProcessDocumentFn', {
      entry: 'lambda/process-document.ts',
      handler: 'handler',
      runtime: lambda.Runtime.NODEJS_22_X,
      memorySize: 512,
      timeout: cdk.Duration.seconds(60),
      logGroup: new logs.LogGroup(this, 'ProcessDocumentLogs', {
        retention: logs.RetentionDays.ONE_WEEK,
        removalPolicy: cdk.RemovalPolicy.DESTROY,   // lab only
      }),
      deadLetterQueue: dlq,
      environment: {
        TABLE_NAME: table.tableName,
        TOPIC_ARN: reviewTopic.topicArn,
        MIN_CONFIDENCE: '90',
      },
      bundling: { minify: true, sourceMap: true },
    });

    // Least privilege: only the actions the function uses.
    bucket.grantReadWrite(fn);
    table.grantWriteData(fn);
    reviewTopic.grantPublish(fn);
    fn.addToRolePolicy(new iam.PolicyStatement({
      actions: ['textract:AnalyzeDocument', 'comprehend:DetectEntities'],
      resources: ['*'], // these APIs do not support resource-level permissions
    }));

    // Trigger the function for every new object under requests/.
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED,
      new s3n.LambdaDestination(fn),
      { prefix: 'requests/' },
    );

    new cdk.CfnOutput(this, 'BucketName', { value: bucket.bucketName });
    new cdk.CfnOutput(this, 'TableName', { value: table.tableName });
  }
}

