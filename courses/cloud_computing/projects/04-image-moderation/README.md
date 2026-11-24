# 04 - Image Moderation Pipeline (Python)

Source: [../../guides/04-image-moderation-pipeline.md](../../guides/04-image-moderation-pipeline.md)

An upload under `uploads/` triggers a Python Lambda that calls Rekognition and applies two thresholds: `published/`, `rejected/`, or an SQS review queue. Every decision is written to DynamoDB.

## Deploy

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap                # once per account and region
cdk deploy
```

## Test

```bash
BUCKET=$(aws cloudformation describe-stacks --stack-name ImageModerationStack \
  --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
aws s3 cp ./safe.jpg s3://$BUCKET/uploads/safe.jpg
```

Then check `published/` and the `DecisionsTable` item. Section 6 of the guide has the full test list.

## Clean up

```bash
cdk destroy ImageModerationStack
```
