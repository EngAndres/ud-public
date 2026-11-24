#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { DocProcessingStack } from '../lib/doc-processing-stack';

const app = new cdk.App();
new DocProcessingStack(app, 'DocProcessingStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
  reviewerEmail: app.node.tryGetContext('reviewerEmail') ?? 'you@example.com',
});
