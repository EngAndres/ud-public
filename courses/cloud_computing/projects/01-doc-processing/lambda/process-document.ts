import { S3Event } from 'aws-lambda';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { TextractClient, AnalyzeDocumentCommand, Block } from '@aws-sdk/client-textract';
import { ComprehendClient, DetectEntitiesCommand } from '@aws-sdk/client-comprehend';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';

const s3 = new S3Client({});
const textract = new TextractClient({});
const comprehend = new ComprehendClient({});
const ddb = DynamoDBDocumentClient.from(new DynamoDBClient({}), {
  marshallOptions: { removeUndefinedValues: true },
});
const sns = new SNSClient({});

const minConfidence = Number(process.env.MIN_CONFIDENCE ?? '90');

// Text of a block: its WORD children joined (a KEY or VALUE block has no text of its own).
const textOf = (block: Block, byId: Map<string, Block>): string =>
  (block.Relationships ?? [])
    .filter(r => r.Type === 'CHILD')
    .flatMap(r => r.Ids ?? [])
    .map(id => byId.get(id))
    .filter((b): b is Block => b?.BlockType === 'WORD')
    .map(b => b.Text ?? '')
    .join(' ');

// Form fields as { "Name": "Maria Perez", "Date": "2025-03-01" }.
const extractFields = (blocks: Block[]): Record<string, string> => {
  const byId = new Map(blocks.filter(b => b.Id).map(b => [b.Id!, b]));
  const fields: Record<string, string> = {};
  for (const key of blocks.filter(b => b.BlockType === 'KEY_VALUE_SET' && b.EntityTypes?.includes('KEY'))) {
    const valueId = (key.Relationships ?? []).find(r => r.Type === 'VALUE')?.Ids?.[0];
    const value = valueId ? byId.get(valueId) : undefined;
    const name = textOf(key, byId).trim();
    if (name) fields[name] = value ? textOf(value, byId).trim() : '';
  }
  return fields;
};

export const handler = async (event: S3Event): Promise<void> => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));
    const requestId = key.split('/').pop() ?? key;

    // 1. Extract text, forms and tables with Textract (synchronous, one page).
    const analysis = await textract.send(new AnalyzeDocumentCommand({
      Document: { S3Object: { Bucket: bucket, Name: key } },
      FeatureTypes: ['FORMS', 'TABLES'],
    }));
    const blocks: Block[] = analysis.Blocks ?? [];
    const lines = blocks.filter(b => b.BlockType === 'LINE').map(b => b.Text ?? '');
    // Only blocks that carry a confidence: a PAGE block has none and must not count as 0.
    const confidences = blocks
      .filter(b => (b.BlockType === 'LINE' || b.BlockType === 'KEY_VALUE_SET') && b.Confidence !== undefined)
      .map(b => b.Confidence as number);
    const fields = extractFields(blocks);
    const avgConfidence = confidences.length
      ? confidences.reduce((a, b) => a + b, 0) / confidences.length
      : 0;

    // 2. Detect entities in the extracted text with Comprehend (max 5000 bytes).
    const text = lines.join('\n').slice(0, 4900);
    const entities = text
      ? (await comprehend.send(new DetectEntitiesCommand({ Text: text, LanguageCode: 'en' })))
          .Entities ?? []
      : [];

    // 3. Decision rule.
    const hasFields = Object.keys(fields).length > 0;
    const status = hasFields && avgConfidence >= minConfidence ? 'AUTO_APPROVED' : 'NEEDS_REVIEW';

    // 4. Store the result as JSON next to the source document.
    const entityCounts: Record<string, number> = {};
    for (const e of entities) entityCounts[e.Type ?? 'OTHER'] = (entityCounts[e.Type ?? 'OTHER'] ?? 0) + 1;
    const result = { requestId, status, avgConfidence, fields, entities, lines };
    await s3.send(new PutObjectCommand({
      Bucket: bucket,
      Key: `results/${requestId}.json`,
      Body: JSON.stringify(result),
      ContentType: 'application/json',
    }));

    // 5. Persist the decision.
    await ddb.send(new PutCommand({
      TableName: process.env.TABLE_NAME,
      Item: { requestId, status, avgConfidence, fields, entityCounts, sourceKey: key, processedAt: new Date().toISOString() },
    }));

    // 6. Send doubtful requests to a person.
    if (status === 'NEEDS_REVIEW') {
      await sns.send(new PublishCommand({
        TopicArn: process.env.TOPIC_ARN,
        Subject: `Review needed: ${requestId}`,
        Message: `Request ${requestId} (${key}) has average confidence ${avgConfidence.toFixed(1)}.`,
      }));
    }
  }
};
