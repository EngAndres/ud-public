#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CallAnalyticsStack } from '../lib/call-analytics-stack';

const app = new cdk.App();
new CallAnalyticsStack(app, 'CallAnalyticsStack', {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
});
