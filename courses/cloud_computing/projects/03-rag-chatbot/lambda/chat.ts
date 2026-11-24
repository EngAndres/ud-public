import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { BedrockAgentRuntimeClient, RetrieveCommand } from '@aws-sdk/client-bedrock-agent-runtime';
import { BedrockRuntimeClient, ConverseCommand } from '@aws-sdk/client-bedrock-runtime';

const agent = new BedrockAgentRuntimeClient({});
const runtime = new BedrockRuntimeClient({});

const minScore = Number(process.env.MIN_SCORE ?? '0.35');

const json = (statusCode: number, body: unknown): APIGatewayProxyResult => ({
  statusCode,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

export const handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  const question = JSON.parse(event.body ?? '{}').question as string | undefined;
  if (!question) {
    return json(400, { error: 'Send a JSON body with a "question" field.' });
  }

  // 1. Retrieve the most relevant chunks from the knowledge base.
  const retrieval = await agent.send(new RetrieveCommand({
    knowledgeBaseId: process.env.KNOWLEDGE_BASE_ID,
    retrievalQuery: { text: question },
    retrievalConfiguration: { vectorSearchConfiguration: { numberOfResults: 4 } },
  }));
  // Keep only relevant chunks: Retrieve returns the best matches even when none is relevant.
  const relevant = (retrieval.retrievalResults ?? []).filter(r => (r.score ?? 0) >= minScore && r.content?.text);
  const sources = relevant.map(r => ({ uri: r.location?.s3Location?.uri, score: r.score }));
  const context = relevant.map(r => r.content!.text).join('\n---\n');

  if (!context) {
    return json(200, {
      answer: 'I could not find this information in the company documents.',
      sources: [],
      guardrailAction: 'NOT_CALLED',
    });
  }

  // 2. Answer from the context only, with the guardrail applied to input and output.
  const answer = await runtime.send(new ConverseCommand({
    modelId: process.env.MODEL_ID,
    system: [{
      text: 'You answer employee questions using only the provided context. ' +
            'If the context does not contain the answer, say you do not know.',
    }],
    messages: [{
      role: 'user',
      content: [
        { text: `Context:\n${context}` },
        // guardContent: the guardrail filters evaluate the user's question (including prompt attacks).
        { guardContent: { text: { text: question } } },
      ],
    }],
    inferenceConfig: { maxTokens: 400, temperature: 0 },
    guardrailConfig: {
      guardrailIdentifier: process.env.GUARDRAIL_ID,
      guardrailVersion: process.env.GUARDRAIL_VERSION,
      trace: 'enabled',
    },
  }));

  const blocked = answer.stopReason === 'guardrail_intervened';
  if (blocked) console.log('Guardrail trace', JSON.stringify(answer.trace?.guardrail));   // goes to CloudWatch Logs
  const text = answer.output?.message?.content?.[0]?.text ?? '';
  return json(200, { answer: text, sources: blocked ? [] : sources, guardrailAction: blocked ? 'BLOCKED' : 'ALLOWED' });
};
