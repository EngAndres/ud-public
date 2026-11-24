# 03 - Enterprise Chatbot with RAG (TypeScript)

Source: [../../guides/03-enterprise-chatbot-rag.md](../../guides/03-enterprise-chatbot-rag.md)

Sample policy documents in `docs/` are uploaded to S3 and indexed by a Bedrock Knowledge Base (Titan embeddings, OpenSearch Serverless). The `/ask` API answers from the retrieved context, with a Bedrock Guardrail applied, and requires IAM-signed requests.

**Check before you deploy:** the stack uses the community library `@cdklabs/generative-ai-cdk-constructs` (pinned to `^0.1.320`). Its class and property names change between releases. If `npx cdk synth` fails on `bedrock.*`, check that package's README and adjust the stack file.

## Deploy

```bash
npm install
npx cdk bootstrap            # once per account and region
npx cdk deploy
```

Ingest the documents after the first deploy (and after each document change):

```bash
KB_ID=$(aws cloudformation describe-stacks --stack-name RagChatbotStack \
  --query "Stacks[0].Outputs[?OutputKey=='KnowledgeBaseId'].OutputValue" --output text)
DS_ID=$(aws cloudformation describe-stacks --stack-name RagChatbotStack \
  --query "Stacks[0].Outputs[?OutputKey=='DataSourceId'].OutputValue" --output text)
aws bedrock-agent start-ingestion-job --knowledge-base-id $KB_ID --data-source-id $DS_ID
```

## Clean up

```bash
npx cdk destroy RagChatbotStack
```
