import os
from datetime import datetime, timezone

import boto3

sagemaker = boto3.client("sagemaker")


def handler(event, context):
    # Job names must be unique and at most 63 characters.
    job_name = "churn-retrain-" + datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

    sagemaker.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            "TrainingImage": os.environ["TRAINING_IMAGE"],
            "TrainingInputMode": "File",
        },
        RoleArn=os.environ["ROLE_ARN"],
        HyperParameters={
            "objective": "binary:logistic",
            "eval_metric": "auc",            # reported as validation:auc
            "num_round": "50",
        },
        InputDataConfig=[
            {
                "ChannelName": channel,
                "ContentType": "text/csv",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": os.environ[env_var],
                        "S3DataDistributionType": "FullyReplicated",
                    },
                },
            }
            for channel, env_var in [("train", "TRAIN_URI"), ("validation", "VALIDATION_URI")]
        ],
        OutputDataConfig={"S3OutputPath": os.environ["OUTPUT_URI"]},
        ResourceConfig={"InstanceType": "ml.m5.large", "InstanceCount": 1, "VolumeSizeInGB": 10},
        StoppingCondition={"MaxRuntimeInSeconds": 900},
    )
    return {"trainingJobName": job_name}
