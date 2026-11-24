# 02 - Call Center Analytics (TypeScript)

Source: [../../guides/02-call-center-analytics.md](../../guides/02-call-center-analytics.md)

Audio uploaded under `audio/` is transcribed by Amazon Transcribe. When the job completes, a second Lambda runs sentiment and PII detection (Comprehend), masks the PII, writes a summary with a Bedrock model, and stores one item per call in DynamoDB.

## Before you deploy

Enable the Bedrock model in the console (Model access). The default model id is set in the stack; pass another one with `-c summaryModelId` (see below).

## Deploy

```bash
npm install
npx cdk bootstrap            # once per account and region
npx cdk deploy
# If the Lambda fails with AccessDeniedException on Bedrock:
npx cdk deploy -c summaryModelId=<model-id-you-enabled>
```

## Test

```bash
BUCKET=$(aws cloudformation describe-stacks --stack-name CallAnalyticsStack \
  --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
aws s3 cp ./call.mp3 s3://$BUCKET/audio/call-001.mp3
```

Transcripts appear under `transcripts/`, and the results appear in the DynamoDB table `CallsTable`.

## Clean up

```bash
npx cdk destroy CallAnalyticsStack
```
