import { EventBridgeEvent } from 'aws-lambda';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import { ComprehendClient, DetectSentimentCommand, DetectPiiEntitiesCommand } from '@aws-sdk/client-comprehend';
import { BedrockRuntimeClient, ConverseCommand } from '@aws-sdk/client-bedrock-runtime';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';

const s3 = new S3Client({});
const comprehend = new ComprehendClient({});
const bedrock = new BedrockRuntimeClient({});
const ddb = DynamoDBDocumentClient.from(new DynamoDBClient({}));

type TranscribeDetail = { TranscriptionJobName: string };

// Replace every PII span by its type, e.g. "my card is [CREDIT_DEBIT_NUMBER]". Offsets refer to `text`.
const maskPii = (text: string, entities: { Type?: string; BeginOffset?: number; EndOffset?: number }[]): string =>
  [...entities]
    .sort((a, b) => (b.BeginOffset ?? 0) - (a.BeginOffset ?? 0))   // from the end, so offsets stay valid
    .reduce((t, e) => t.slice(0, e.BeginOffset) + `[${e.Type}]` + t.slice(e.EndOffset), text);

export const handler = async (
  event: EventBridgeEvent<'Transcribe Job State Change', TranscribeDetail>,
): Promise<void> => {
  const jobName = event.detail.TranscriptionJobName;
  const callId = jobName.replace(/^call-/, '').replace(/-\d+$/, '');

  // 1. Read the transcript written by Transcribe.
  const obj = await s3.send(new GetObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `transcripts/${jobName}.json`,
  }));
  const body = JSON.parse(await obj.Body!.transformToString());
  const text: string = body.results.transcripts[0].transcript;
  const excerpt = text.slice(0, 4900); // Comprehend limit: 5000 bytes per call

  // 2. Sentiment and personal data.
  const sentiment = await comprehend.send(new DetectSentimentCommand({
    Text: excerpt, LanguageCode: 'en',
  }));
  const pii = await comprehend.send(new DetectPiiEntitiesCommand({
    Text: excerpt, LanguageCode: 'en',
  }));

  // 3. Summary with a foundation model on Bedrock. Personal data is masked first.
  const masked = maskPii(excerpt, pii.Entities ?? []);
  const response = await bedrock.send(new ConverseCommand({
    modelId: process.env.SUMMARY_MODEL_ID,
    system: [{ text: 'Summarize customer calls in three sentences. Never repeat personal data.' }],
    messages: [{ role: 'user', content: [{ text: masked }] }],
    inferenceConfig: { maxTokens: 300, temperature: 0 },
  }));
  const summary = response.output?.message?.content?.[0]?.text ?? '';

  // 4. Store one item per call. Negative calls get HIGH priority.
  const label = sentiment.Sentiment ?? 'NEUTRAL';
  await ddb.send(new PutCommand({
    TableName: process.env.TABLE_NAME,
    Item: {
      callId,
      sentiment: label,
      sentimentScore: sentiment.SentimentScore,
      piiCount: pii.Entities?.length ?? 0,
      piiTypes: [...new Set((pii.Entities ?? []).map(e => e.Type))],
      summary,
      priority: label === 'NEGATIVE' ? 'HIGH' : 'NORMAL',
      createdAt: new Date().toISOString(),
    },
  }));
};
