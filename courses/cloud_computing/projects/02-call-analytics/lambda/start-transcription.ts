import { S3Event } from 'aws-lambda';
import { TranscribeClient, StartTranscriptionJobCommand } from '@aws-sdk/client-transcribe';

const transcribe = new TranscribeClient({});

export const handler = async (event: S3Event): Promise<void> => {
  for (const record of event.Records) {
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));
    const callId = key.split('/').pop()!.replace(/\.[^.]+$/, '');
    // Job names allow only letters, digits, '.', '_' and '-'.
    const jobName = `call-${callId.replace(/[^0-9a-zA-Z._-]/g, '-')}-${Date.now()}`;

    await transcribe.send(new StartTranscriptionJobCommand({
      TranscriptionJobName: jobName,
      LanguageCode: 'en-US',
      Media: { MediaFileUri: `s3://${process.env.BUCKET_NAME}/${key}` },
      OutputBucketName: process.env.BUCKET_NAME,
      OutputKey: 'transcripts/',
      Settings: { ShowSpeakerLabels: true, MaxSpeakerLabels: 2 },
    }));
  }
};
