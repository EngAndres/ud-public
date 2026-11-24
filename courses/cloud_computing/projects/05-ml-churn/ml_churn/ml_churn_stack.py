from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_sagemaker as sagemaker,
)
from constructs import Construct


class MlChurnStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Context values, passed with -c on the command line.
        model_version = self.node.try_get_context("modelVersion") or "v1"
        model_data_url = self.node.try_get_context("modelDataUrl")   # s3://.../model.tar.gz
        # Built-in XGBoost image. Image URIs are region specific: look up yours in the
        # SageMaker "Common parameters for built-in algorithms" page.
        inference_image = (
            self.node.try_get_context("inferenceImage")
            or "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1"
        )

        # Data, model artifacts, and captured requests.
        data_bucket = s3.Bucket(
            self, "MlDataBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,   # lab only
            auto_delete_objects=True,               # lab only
        )
        # data/train/train.csv -> s3://bucket/train/train.csv, data/validation/validation.csv -> .../validation/
        s3deploy.BucketDeployment(
            self, "DeployTrainingData",
            sources=[s3deploy.Source.asset("./data")],
            destination_bucket=data_bucket,
        )

        # SageMaker execution role: read data, write artifacts and captures, write logs.
        sagemaker_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
        )
        data_bucket.grant_read_write(sagemaker_role)
        sagemaker_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents",
                "cloudwatch:PutMetricData", "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage",
            ],
            resources=["*"],
        ))

        # Model: points to the trained artifact in S3 and to the inference container.
        # Created only after you pass the artifact location with -c modelDataUrl=...
        if model_data_url:
            model = sagemaker.CfnModel(
                self, "ChurnModel",
                model_name=f"churn-model-{model_version}",
                execution_role_arn=sagemaker_role.role_arn,
                primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                    image=inference_image,
                    model_data_url=model_data_url,
                ),
            )

            endpoint_config = sagemaker.CfnEndpointConfig(
                self, "ChurnEndpointConfig",
                endpoint_config_name=f"churn-config-{model_version}",
                production_variants=[sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    model_name=model.model_name,
                    variant_name="AllTraffic",
                    initial_instance_count=1,
                    instance_type="ml.t2.medium",
                    initial_variant_weight=1,
                )],
                # Save every request and response to S3 for drift analysis.
                data_capture_config=sagemaker.CfnEndpointConfig.DataCaptureConfigProperty(
                    enable_capture=True,
                    initial_sampling_percentage=100,
                    destination_s3_uri=f"s3://{data_bucket.bucket_name}/captured",
                    capture_options=[
                        sagemaker.CfnEndpointConfig.CaptureOptionProperty(capture_mode="Input"),
                        sagemaker.CfnEndpointConfig.CaptureOptionProperty(capture_mode="Output"),
                    ],
                ),
            )
            endpoint_config.add_dependency(model)

            endpoint = sagemaker.CfnEndpoint(
                self, "ChurnEndpoint",
                endpoint_name="churn-endpoint",
                endpoint_config_name=endpoint_config.endpoint_config_name,
            )
            endpoint.add_dependency(endpoint_config)

            CfnOutput(self, "EndpointName", value=endpoint.endpoint_name)

        # Retraining: a Lambda starts a new training job every week.
        retrain_fn = _lambda.Function(
            self, "RetrainFn",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="retrain.handler",              # file lambda/retrain.py, function handler
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            log_group=logs.LogGroup(
                self, "RetrainLogs",
                retention=logs.RetentionDays.ONE_WEEK,
                removal_policy=RemovalPolicy.DESTROY,   # lab only
            ),
            environment={
                "TRAINING_IMAGE": inference_image,
                "ROLE_ARN": sagemaker_role.role_arn,
                "TRAIN_URI": f"s3://{data_bucket.bucket_name}/train/",
                "VALIDATION_URI": f"s3://{data_bucket.bucket_name}/validation/",
                "OUTPUT_URI": f"s3://{data_bucket.bucket_name}/models/",
            },
        )
        retrain_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["sagemaker:CreateTrainingJob"],
            resources=["*"],
        ))
        retrain_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["iam:PassRole"],
            resources=[sagemaker_role.role_arn],
        ))

        events.Rule(
            self, "WeeklyRetrainRule",
            schedule=events.Schedule.rate(Duration.days(7)),
            targets=[targets.LambdaFunction(retrain_fn)],
        )

        CfnOutput(self, "DataBucketName", value=data_bucket.bucket_name)
        CfnOutput(self, "SageMakerRoleArn", value=sagemaker_role.role_arn)
