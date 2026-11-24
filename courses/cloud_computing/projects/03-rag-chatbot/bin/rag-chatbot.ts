#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { RagChatbotStack } from '../lib/rag-chatbot-stack';

const app = new cdk.App();
new RagChatbotStack(app, 'RagChatbotStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
});
