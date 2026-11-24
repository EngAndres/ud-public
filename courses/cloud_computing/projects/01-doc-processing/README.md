# 01 - Intelligent Document Processing (TypeScript)

Source: [../../guides/01-intelligent-document-processing.md](../../guides/01-intelligent-document-processing.md)

S3 upload under `requests/` triggers a Lambda that runs Textract and Comprehend, writes the result to S3 and DynamoDB, and emails a reviewer when confidence is low.

## Deploy

```bash
npm install
npx cdk bootstrap            # once per account and region
npx cdk synth -c reviewerEmail=you@example.com
npx cdk deploy -c reviewerEmail=you@example.com
```

Confirm the SNS subscription in the email you receive, or no review messages arrive.

## Test

```bash
BUCKET=$(aws cloudformation describe-stacks --stack-name DocProcessingStack \
  --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
aws s3 cp ./sample-form.png s3://$BUCKET/requests/req-001.png
aws s3 cp s3://$BUCKET/results/req-001.png.json -
```

## Clean up

```bash
npx cdk destroy DocProcessingStack
```
