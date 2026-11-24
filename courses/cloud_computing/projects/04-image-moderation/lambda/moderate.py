import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from urllib.parse import unquote_plus

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")
sqs = boto3.client("sqs")
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

BLOCK_THRESHOLD = float(os.environ.get("BLOCK_THRESHOLD", "90"))
REVIEW_THRESHOLD = float(os.environ.get("REVIEW_THRESHOLD", "60"))

# Errors that mean "Rekognition cannot read this file". Any other error is retried by Lambda.
UNREADABLE_ERRORS = {"InvalidImageFormatException", "ImageTooLargeException"}


def move(bucket, source_key, target_key):
    """Move the object: copy to the new prefix, then delete the original."""
    s3.copy_object(
        Bucket=bucket,
        Key=target_key,
        CopySource={"Bucket": bucket, "Key": source_key},
    )
    s3.delete_object(Bucket=bucket, Key=source_key)


def dec(value):
    """DynamoDB does not accept Python floats: use Decimal."""
    return Decimal(str(value))


def handler(event, context):
    bucket = os.environ["BUCKET_NAME"]

    for record in event["Records"]:
        key = unquote_plus(record["s3"]["object"]["key"])   # S3 events encode spaces as "+"
        filename = key.removeprefix("uploads/")

        # 1. Ask Rekognition for moderation labels.
        labels = []
        unreadable = False
        try:
            result = rekognition.detect_moderation_labels(
                Image={"S3Object": {"Bucket": bucket, "Name": key}},
                MinConfidence=50,
            )
            labels = result.get("ModerationLabels", [])
        except ClientError as err:
            # Not an image Rekognition can read: do not publish it unchecked.
            if err.response["Error"]["Code"] not in UNREADABLE_ERRORS:
                raise
            unreadable = True

        top = max((label["Confidence"] for label in labels), default=0.0)
        if unreadable:
            top_label = "unreadable-image"
        elif labels:
            top_label = max(labels, key=lambda label: label["Confidence"])["Name"]
        else:
            top_label = "none"

        # 2. Apply the policy.
        if unreadable:
            decision = "NEEDS_REVIEW"
        elif top >= BLOCK_THRESHOLD:
            decision = "BLOCKED"
        elif top >= REVIEW_THRESHOLD:
            decision = "NEEDS_REVIEW"
        else:
            decision = "PUBLISHED"

        # 3. Act on the decision.
        if decision == "PUBLISHED":
            move(bucket, key, f"published/{filename}")
        elif decision == "BLOCKED":
            move(bucket, key, f"rejected/{filename}")
        else:
            # Uncertain: leave the image in uploads/ and ask a person to decide.
            sqs.send_message(
                QueueUrl=os.environ["QUEUE_URL"],
                MessageBody=json.dumps({"key": key, "topLabel": top_label, "confidence": top}),
            )

        # 4. Audit record.
        table.put_item(Item={
            "imageKey": key,
            "decision": decision,
            "topLabel": top_label,
            "confidence": dec(top),
            "labels": [
                {
                    "name": label["Name"],
                    "parent": label.get("ParentName", ""),
                    "confidence": dec(label["Confidence"]),
                }
                for label in labels
            ],
            "decidedAt": datetime.now(timezone.utc).isoformat(),
        })
