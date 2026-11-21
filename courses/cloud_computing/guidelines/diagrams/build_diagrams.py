#!/usr/bin/env python3
"""Generate the architecture diagrams of the six guides.

Outputs, next to this file:  NN-name.drawio (editable), NN-name.svg and NN-name.png (embedded in the guides).
Usage:  python3 build_diagrams.py      (needs Inkscape on the PATH for the PNG export)
"""
import os
import subprocess

from diagramlib import Diagram

HERE = os.path.dirname(os.path.abspath(__file__))
LEGEND = 'Solid arrow: call or data write   |   Dashed arrow: trigger, async event or optional path   |   Numbered circles match the Flow list'


def finish(d, key, steps_y, extra_h=0):
    d.text(24, 30, d.name, size=17, bold=True)
    d.text(24, steps_y - 22, LEGEND, size=11, color='#607D8B')
    d.add_steps_panel(steps_y)
    d.h = steps_y + 22 + 19 * len(d.legend_steps) + 24 + extra_h
    for ext, data in (('drawio', d.drawio()), ('svg', d.svg())):
        with open(os.path.join(HERE, f'{key}.{ext}'), 'w', encoding='utf-8') as f:
            f.write(data)
    svg = os.path.join(HERE, f'{key}.svg')
    png = os.path.join(HERE, f'{key}.png')
    subprocess.run(['inkscape', svg, '--export-type=png', f'--export-filename={png}', '--export-width=%d' % (d.w * 2)],
                   check=True, capture_output=True)
    print('built', key, d.w, d.h)


# --------------------------------------------------------------------------
def d1():
    d = Diagram('Guide 1: Intelligent Document Processing', 1340, 0)
    d.group('aws', 'AWS Cloud (one region)', 235, 44, 880, 480, right=True)
    d.node('req', 'Requesters', ['Scanned forms', 'PNG or JPEG'], 30, 203, cat='ext')
    d.node('s3', 'Amazon S3', ['requests/ (input)', 'results/ (JSON output)', 'encrypted, versioned'], 260, 195, h=100, cat='storage')
    d.node('fn', 'Lambda: ProcessDocument', ['Node.js 22, 512 MB, 60 s', 'orchestrates and decides', 'least-privilege role'], 540, 195, h=100, cat='compute')
    d.node('tx', 'Amazon Textract', ['AnalyzeDocument', 'FORMS + TABLES'], 900, 62, cat='ml')
    d.node('cmp', 'Amazon Comprehend', ['DetectEntities (en)', 'text up to 5,000 bytes'], 900, 203, cat='ml')
    d.node('ddb', 'DynamoDB table', ['status, avgConfidence,', 'fields, entity counts'], 900, 322, cat='db')
    d.node('sns', 'SNS topic', ['email subscription', 'NEEDS_REVIEW only'], 900, 424, cat='integ')
    d.node('rev', 'Human reviewer', ['confirms the email', 'decides manually'], 1150, 424, w=160, cat='ext')
    d.node('dlq', 'SQS dead-letter queue', ['failed async invokes', 'after 2 retries'], 540, 400, cat='integ')
    d.node('iam', 'IAM execution role', ['bucket.grantReadWrite', 'table.grantWriteData', 'textract/comprehend: *'], 260, 400, cat='sec')
    d.edge('req', 'r', 's3', 'l', 'upload')
    d.edge('s3', 'r', 'fn', 'l', 'event', dashed=True)
    d.edge('fn', 't', 's3', 't', 'results/<id>.json', via=[(625, 150), (345, 150)], lseg=1)
    d.edge('fn', 'r', 'tx', 'l', 'AnalyzeDocument', so=0.2, via=[(745, 215), (745, 100)], lseg=-1)
    d.edge('fn', 'r', 'cmp', 'l', 'DetectEntities', so=0.5, lseg=0)
    d.edge('fn', 'r', 'ddb', 'l', 'PutItem', so=0.7, via=[(775, 265), (775, 360)], lseg=-1)
    d.edge('fn', 'r', 'sns', 'l', 'Publish', so=0.85, via=[(745, 280), (745, 462)], lseg=-1)
    d.edge('sns', 'r', 'rev', 'l', 'email')
    d.edge('fn', 'b', 'dlq', 't', 'failed invoke', dashed=True)
    d.edge('iam', 'r', 'fn', 'l', 'assumes', dashed=True, so=0.5, do=0.85, via=[(490, 442), (490, 280)], lseg=1)
    for nid, n in (('req', 1), ('fn', 2), ('tx', 3), ('cmp', 4), ('ddb', 6), ('sns', 7)):
        d.badge(nid, n)
    d.badge('fn', 5, dx=150, dy=-8)
    d.text(260, 512, 'Rule: form fields found AND average confidence >= 90  ->  AUTO_APPROVED, otherwise NEEDS_REVIEW', size=12, bold=True)
    for n, s in [
        (1, 'A requester uploads a PNG or JPEG to requests/ (a different prefix from results/, so the output never re-triggers the function).'),
        (2, 'S3 ObjectCreated invokes ProcessDocumentFn. S3 delivers events at least once, so the item is keyed by requestId and is idempotent.'),
        (3, 'Textract AnalyzeDocument (synchronous, one page) returns lines, key/value pairs and tables.'),
        (4, 'Comprehend DetectEntities runs on the extracted text (names, dates, amounts, organizations).'),
        (5, 'The function applies the decision rule: average confidence of LINE and KEY_VALUE_SET blocks, and at least one form field.'),
        (6, 'It writes results/<id>.json to S3 and one DynamoDB item with the status, the confidence and the extracted fields.'),
        (7, 'NEEDS_REVIEW publishes to SNS; the reviewer gets an email. Invocations that keep failing land in the dead-letter queue.'),
    ]:
        d.step(n, s)
    finish(d, '01-intelligent-document-processing', 560)


# --------------------------------------------------------------------------
def d2():
    d = Diagram('Guide 2: Call-Center Analytics', 1580, 0)
    d.group('aws', 'AWS Cloud (one region)', 275, 20, 1285, 470, right=True)
    d.node('call', 'Customer calls', ['.mp3 / .wav', 'under 2 minutes'], 30, 70, w=160, cat='ext')
    d.node('s3', 'Amazon S3', ['audio/  transcripts/', 'encrypted, private'], 300, 70, w=160, cat='storage')
    d.node('st', 'Lambda: StartTranscription', ['starts the job', 'name: call-<id>-<time>'], 570, 70, w=160, cat='compute')
    d.node('tr', 'Amazon Transcribe', ['batch job, en-US', 'speaker labels (2)'], 840, 70, w=160, cat='ml')
    d.node('eb', 'EventBridge rule', ['Job State Change', 'COMPLETED, prefix call-'], 1110, 70, w=160, cat='integ')
    d.node('an', 'Lambda: AnalyzeTranscript', ['reads the transcript', 'masks PII', 'writes the item'], 1110, 215, w=160, h=160, cat='compute')
    d.node('cmp', 'Amazon Comprehend', ['DetectSentiment', 'DetectPiiEntities'], 840, 200, w=160, cat='ml')
    d.node('br', 'Amazon Bedrock', ['Converse API', '3-sentence summary'], 840, 300, w=160, cat='ml')
    d.node('ddb', 'DynamoDB table', ['PK callId', 'GSI bySentiment'], 1380, 215, w=160, cat='db')
    d.node('sup', 'Supervisor', ['negative calls first', 'QuickSight: extension'], 1380, 330, w=160, cat='ext')
    d.edge('call', 'r', 's3', 'l', 'upload')
    d.edge('s3', 'r', 'st', 'l', 'event', dashed=True)
    d.edge('st', 'r', 'tr', 'l', 'StartJob')
    d.edge('tr', 'r', 'eb', 'l', 'state change', dashed=True)
    d.edge('tr', 't', 's3', 't', 'transcripts/<job>.json', via=[(920, 52), (380, 52)], lseg=1)
    d.edge('eb', 'b', 'an', 't', 'invoke', dashed=True)
    d.edge('an', 'l', 'cmp', 'r', 'sentiment, PII', so=0.2, do=0.5)
    d.edge('an', 'l', 'br', 'r', 'summary', so=0.75, do=0.5)
    d.edge('an', 'r', 'ddb', 'l', 'PutItem')
    d.edge('ddb', 'b', 'sup', 't', 'Query GSI')
    d.edge('s3', 'b', 'an', 'b', 'GetObject transcripts/', via=[(380, 440), (1190, 440)], lseg=1)
    for nid, n in (('call', 1), ('st', 2), ('tr', 3), ('eb', 4), ('cmp', 5), ('br', 6), ('ddb', 7), ('sup', 8)):
        d.badge(nid, n)
    for n, s in [
        (1, 'A recording (.mp3 or .wav) is uploaded to audio/.'),
        (2, 'S3 invokes StartTranscriptionFn, which starts a Transcribe batch job with speaker labels. The job name carries the call id.'),
        (3, 'Transcribe writes transcripts/<job>.json to the same bucket (a different prefix, so there is no loop).'),
        (4, 'Transcribe emits "Job State Change = COMPLETED". The EventBridge rule filters on the call- prefix and invokes AnalyzeTranscriptFn: no polling.'),
        (5, 'The function reads the transcript and calls Comprehend for the sentiment and the personal data (PII) entities.'),
        (6, 'PII spans are masked, then Bedrock Converse writes a three-sentence summary (model id is a context value).'),
        (7, 'One DynamoDB item per call: sentiment, scores, PII types, summary, priority (HIGH when NEGATIVE).'),
        (8, 'Supervisors query the bySentiment index, newest first. A QuickSight dashboard on the index is the extension.'),
    ]:
        d.step(n, s)
    finish(d, '02-call-center-analytics', 540)


# --------------------------------------------------------------------------
def d3():
    d = Diagram('Guide 3: Enterprise Chatbot with RAG', 1580, 0)
    d.group('aws', 'AWS Cloud (one region)', 275, 20, 1285, 520, right=True)
    d.text(1300, 100, 'Ingestion (per document change)', size=12, bold=True, color='#01796B')
    d.text(1300, 300, 'Question answering (per request)', size=12, bold=True, color='#01796B')
    d.node('adm', 'Admin', ['uploads policy files', 'start-ingestion-job'], 30, 70, w=160, cat='ext')
    d.node('s3', 'Amazon S3', ['docs bucket', 'deployed from ./docs'], 300, 70, w=160, cat='storage')
    d.node('kb', 'Bedrock Knowledge Base', ['chunks documents', '(default strategy)', 'Retrieve API'], 570, 70, w=160, cat='ml')
    d.node('emb', 'Titan Text Embeddings', ['V2 (via the KB)', 'text -> vector'], 840, 70, w=160, cat='ml')
    d.node('oss', 'OpenSearch Serverless', ['vector collection', 'created by the construct'], 1110, 70, w=160, cat='db')
    d.node('emp', 'Employee', ['SigV4-signed', 'POST /ask'], 30, 270, w=160, cat='ext')
    d.node('api', 'API Gateway (REST)', ['IAM authorization', 'throttle 5 rps / burst 10'], 300, 270, w=160, cat='net')
    d.node('fn', 'Lambda: ChatFn', ['Retrieve + Converse', 'drops chunks < MIN_SCORE', 'timeout 29 s'], 570, 270, w=160, cat='compute')
    d.node('llm', 'Bedrock foundation model', ['Converse API', 'answers from context only'], 840, 270, w=160, cat='ml')
    d.node('gr', 'Bedrock Guardrails', ['content filters, denied', 'topic, PII anonymize'], 840, 390, w=160, cat='sec')
    d.node('iam', 'IAM role', ['bedrock:Retrieve (KB ARN)', 'InvokeModel (model ARN)', 'ApplyGuardrail (ARN)'], 300, 410, w=170, cat='sec')
    d.node('cw', 'CloudWatch Logs', ['7-day retention', 'guardrail trace logged'], 570, 410, w=160, cat='mgmt')
    d.edge('adm', 'r', 's3', 'l', 'upload')
    d.edge('s3', 'r', 'kb', 'l', 'data source')
    d.edge('kb', 'r', 'emb', 'l', 'embed chunks')
    d.edge('emb', 'r', 'oss', 'l', 'store vectors')
    d.edge('adm', 't', 'kb', 't', 'start-ingestion-job', dashed=True, via=[(110, 50), (650, 50)], lseg=1)
    d.edge('emp', 'r', 'api', 'l', 'HTTPS')
    d.edge('api', 'r', 'fn', 'l', 'proxy')
    d.edge('fn', 't', 'kb', 'b', 'Retrieve (top 4)')
    d.edge('fn', 'r', 'llm', 'l', 'Converse')
    d.edge('llm', 'b', 'gr', 't', 'input / output check', dashed=True)
    d.edge('fn', 'b', 'cw', 't', 'logs', dashed=True)
    for nid, n in (('adm', 1), ('kb', 2), ('oss', 3), ('api', 4), ('fn', 5), ('llm', 6), ('gr', 7), ('emp', 8)):
        d.badge(nid, n)
    for n, s in [
        (1, 'An admin uploads the policy files to S3 and runs start-ingestion-job (CDK does not start it).'),
        (2, 'The knowledge base splits each document into chunks and asks Titan Text Embeddings V2 for a vector per chunk.'),
        (3, 'The vectors are stored in an OpenSearch Serverless index. The same path serves the semantic search at query time.'),
        (4, 'An employee sends a SigV4-signed POST /ask. API Gateway checks IAM and throttles to protect the model budget.'),
        (5, 'ChatFn calls Retrieve (top 4) and drops chunks below MIN_SCORE; if nothing is left it answers "not found" without calling the model.'),
        (6, 'ChatFn calls Converse with the chunks as context. The question is sent as guardContent so the filters evaluate it.'),
        (7, 'The guardrail checks input and output (content filters, denied topic, PII). A block returns stopReason guardrail_intervened.'),
        (8, 'The API returns the answer, the sources (S3 URI and score) and guardrailAction ALLOWED or BLOCKED.'),
    ]:
        d.step(n, s)
    finish(d, '03-enterprise-chatbot-rag', 600)


# --------------------------------------------------------------------------
def d4():
    d = Diagram('Guide 4: Image Moderation Pipeline', 1340, 0)
    d.group('aws', 'AWS Cloud (one region)', 245, 20, 1075, 560, right=True)
    d.node('usr', 'Users', ['upload images', 'JPEG or PNG'], 30, 198, cat='ext')
    d.node('s3', 'Amazon S3', ['uploads/ (input, review)', 'published/  rejected/', 'encrypted, private'], 270, 170, h=140, cat='storage')
    d.node('fn', 'Lambda: ModerateFn', ['Node.js 22, 512 MB', 'applies the policy', 'moves the object'], 540, 170, h=140, cat='compute')
    d.node('rk', 'Amazon Rekognition', ['DetectModerationLabels', 'MinConfidence 50'], 850, 62, cat='ml')
    d.node('ddb', 'DynamoDB table', ['decision, top label,', 'all labels + confidence'], 850, 198, cat='db')
    d.node('sq', 'SQS: ReviewQueue', ['uncertain images', 'visibility 60 s'], 850, 320, cat='integ')
    d.node('dlq', 'SQS: ReviewDlq', ['after 5 receives'], 850, 440, cat='integ')
    d.node('rev', 'Human reviewer', ['polls the queue', 'resolves each case'], 1120, 320, w=160, cat='ext')
    d.edge('usr', 'r', 's3', 'l', 'upload')
    d.edge('s3', 'r', 'fn', 'l', 'event', dashed=True)
    d.edge('fn', 't', 's3', 't', 'copy + delete -> prefix', via=[(625, 130), (355, 130)], lseg=1)
    d.edge('fn', 'r', 'rk', 'l', 'detect labels', so=0.15, via=[(745, 191), (745, 104)], lseg=-1)
    d.edge('fn', 'r', 'ddb', 'l', 'audit record', so=0.5, lseg=0)
    d.edge('fn', 'r', 'sq', 'l', 'only if 60-89', so=0.85, via=[(745, 289), (745, 362)], lseg=-1)
    d.edge('sq', 'b', 'dlq', 't', 'poison msgs', dashed=True)
    d.edge('sq', 'r', 'rev', 'l', 'poll')
    d.edge('rev', 'b', 's3', 'b', 'reviewer moves the object and updates the audit item', dashed=True,
           via=[(1200, 540), (355, 540)], lseg=1)
    for nid, n in (('usr', 1), ('fn', 2), ('rk', 3), ('ddb', 7), ('sq', 6), ('rev', 8)):
        d.badge(nid, n)
    d.badge('fn', 4, dx=150, dy=-8)
    d.badge('s3', 5, dx=150, dy=-8)
    d.text(24, 500, 'Policy on the highest confidence', size=12, bold=True)
    d.text(24, 520, '>= 90   BLOCKED  -> rejected/', size=12, color='#B71C1C')
    d.text(24, 538, '60-89   NEEDS_REVIEW  -> SQS', size=12, color='#E65100')
    d.text(24, 556, '< 60   PUBLISHED  -> published/', size=12, color='#2E7D32')
    for n, s in [
        (1, 'A user uploads an image to uploads/.'),
        (2, 'S3 ObjectCreated invokes ModerateFn (the other prefixes have no trigger, so moving a file never re-invokes it).'),
        (3, 'Rekognition returns moderation labels with a confidence. A non-image or oversized file cannot be checked and goes to review (fail closed).'),
        (4, 'The policy compares the highest confidence with two thresholds that are environment variables.'),
        (5, 'Clear cases are moved (copy, then delete) to published/ or rejected/. Uncertain images stay in uploads/.'),
        (6, 'Uncertain images are sent to the review queue; messages that keep failing move to the dead-letter queue.'),
        (7, 'Every decision is stored in DynamoDB with all labels, so each automated decision can be audited.'),
        (8, 'A reviewer polls the queue and finishes the case by hand (s3 mv + update the audit item).'),
    ]:
        d.step(n, s)
    finish(d, '04-image-moderation-pipeline', 620)


# --------------------------------------------------------------------------
def d5():
    d = Diagram('Guide 5: Custom ML Model with SageMaker', 1580, 0)
    d.group('aws', 'AWS Cloud (one region)', 275, 20, 1285, 480, right=True)
    d.node('dev', 'Developer', ['awk: train.csv (400)', 'validation.csv (100)'], 30, 70, w=160, cat='ext')
    d.node('s3', 'Amazon S3: data bucket', ['train/  validation/', 'models/  captured/', 'encrypted, private'], 300, 70, w=160, h=100, cat='storage')
    d.node('trn', 'SageMaker training job', ['built-in XGBoost 1.7-1', 'ml.m5.large, max 900 s', 'binary:logistic, AUC'], 570, 70, w=160, h=100, cat='ml')
    d.node('ev', 'Evaluate (gate)', ['validation:auc from', 'describe-training-job', 'deploy only if >= 0.90'], 840, 70, w=160, h=100, cat='mgmt')
    d.node('ep', 'SageMaker endpoint', ['CfnModel + EndpointConfig', 'ml.t2.medium x1', 'created by cdk deploy'], 1110, 70, w=160, h=100, cat='ml')
    d.node('app', 'Application', ['InvokeEndpoint', 'text/csv, no label'], 1380, 70, w=160, h=100, cat='ext')
    d.node('cap', 'Data capture', ['100% of requests', 'and responses'], 1110, 270, w=160, cat='ml')
    d.node('eb', 'EventBridge rule', ['rate(7 days)'], 840, 270, w=160, cat='integ')
    d.node('rt', 'Lambda: RetrainFn', ['CreateTrainingJob', 'same channels as step 2'], 570, 270, w=160, cat='compute')
    d.node('iam', 'SageMaker execution role', ['S3 read/write, ECR pull,', 'CloudWatch logs'], 30, 270, w=160, cat='sec')
    d.edge('dev', 'r', 's3', 'l', 'BucketDeployment')
    d.edge('s3', 'r', 'trn', 'l', 'channels')
    d.edge('trn', 't', 's3', 't', 'model.tar.gz -> models/', via=[(650, 52), (380, 52)], lseg=1)
    d.edge('trn', 'r', 'ev', 'l', 'Completed')
    d.edge('ev', 'r', 'ep', 'l', 'cdk deploy', dashed=True)
    d.edge('ep', 'r', 'app', 'l', 'probability')
    d.edge('ep', 'b', 'cap', 't', 'capture', dashed=True)
    d.edge('cap', 'b', 's3', 'b', 'captured/ JSON (batched)', via=[(1190, 420), (380, 420)], lseg=1)
    d.edge('eb', 'l', 'rt', 'r', 'every 7 days', dashed=True)
    d.edge('rt', 't', 'trn', 'b', 'new job')
    for nid, n in (('dev', 1), ('trn', 2), ('ev', 3), ('ep', 4), ('app', 5), ('cap', 6), ('eb', 7)):
        d.badge(nid, n)
    d.badge('rt', 8)
    d.text(290, 470, 'Cost: the endpoint bills every hour it exists. Destroy the stack after the lab.', size=12, bold=True, color='#B71C1C')
    for n, s in [
        (1, 'The developer generates the CSV files (label in the first column, no header) and CDK uploads them to train/ and validation/.'),
        (2, 'A training job (built-in XGBoost, no custom container) reads both channels and writes model.tar.gz to models/.'),
        (3, 'Evaluate: read validation:auc from the finished job. Deploy only if it passes the threshold (a manual gate in this lab).'),
        (4, 'cdk deploy -c modelDataUrl=... creates the Model, an EndpointConfig with data capture and the Endpoint.'),
        (5, 'The application sends one CSV row and receives a probability between 0 and 1.'),
        (6, 'Data capture saves each request and response under captured/, the raw material for drift analysis.'),
        (7, 'EventBridge starts RetrainFn every 7 days; it launches a new training job on the current data.'),
        (8, 'A new model repeats steps 3 and 4 with a new modelVersion. SageMaker Model Monitor is the production extension.'),
    ]:
        d.step(n, s)
    finish(d, '05-custom-ml-sagemaker', 540)


# --------------------------------------------------------------------------
def d6():
    d = Diagram('Guide 6: Resilient Web Application', 1660, 0)
    d.group('edge', 'Edge (global)', 215, 70, 225, 460, stroke='#8C4FFF')
    d.group('reg', 'Region (application stack)', 465, 70, 1165, 710, stroke='#7D8998')
    d.group('vpc', 'VPC 10.0.0.0/16: two Availability Zones, no single point of failure', 490, 100, 895, 665, stroke='#147EBA')
    d.group('bp', 'Public subnets', 510, 160, 860, 190, stroke='#7AA116', fill='#F1F8E9', dashed=False, tcolor='#33691E')
    d.group('ba', 'Private subnets "app" (egress through NAT)', 510, 370, 860, 140, stroke='#147EBA', fill='#E8F4FB', dashed=False, tcolor='#0D47A1')
    d.group('bd', 'Isolated subnets "data" (no route to the internet)', 510, 530, 860, 190, stroke='#7B6BA8', fill='#F1EEF8', dashed=False, tcolor='#4527A0')
    d.group('aza', 'Availability Zone a', 530, 126, 400, 28, stroke='#546E7A', fill='#ECEFF1', dashed=False)
    d.group('azb', 'Availability Zone b', 960, 126, 400, 28, stroke='#546E7A', fill='#ECEFF1', dashed=False)
    d.text(500, 752, 'Security groups: ALB <- CloudFront prefix list | tasks <- ALB | PostgreSQL 5432 <- tasks | Redis 6379 <- tasks', size=11, color='#455A64')

    d.node('usr', 'Users', ['browser or API client'], 30, 260, w=160, cat='ext')
    d.node('r53', 'Route 53 (optional)', ['alias A record', 'needs a custom domain'], 235, 100, cat='net')
    d.node('cf', 'CloudFront', ['HTTPS redirect, TLS 1.2+', '/static/* cached, rest not', 'origin: ALB over HTTP'], 235, 260, h=90, cat='net')
    d.node('waf', 'AWS WAF web ACL', ['rate limit per IP', 'Common + SQLi managed rules'], 235, 410, cat='sec')
    d.node('alb', 'Application Load Balancer (internet-facing, spans both AZs)',
           ['health check GET / -> 200, removes unhealthy targets',
            'ingress only from the CloudFront origin-facing prefix list'], 545, 190, w=800, h=70, cat='net')
    d.node('nata', 'NAT gateway a', ['egress'], 555, 280, w=120, h=56, cat='net')
    d.node('natb', 'NAT gateway b', ['egress'], 985, 280, w=120, h=56, cat='net')
    d.node('ta', 'ECS Fargate task (AZ a)', ['nginx, 0.25 vCPU / 512 MiB', 'service: desired 2, scale 2-6 @ 60% CPU'], 545, 400, w=370, h=84, cat='compute')
    d.node('tb', 'ECS Fargate task (AZ b)', ['replaced automatically if it fails', 'circuit breaker rolls back bad deploys'], 975, 400, w=370, h=84, cat='compute')
    d.node('rda', 'RDS PostgreSQL primary', ['Multi-AZ, encrypted', 'secret in Secrets Manager'], 545, 562, w=175, h=84, cat='db')
    d.node('rdb', 'RDS standby', ['synchronous copy', 'automatic failover'], 1170, 562, w=175, h=84, cat='db')
    d.node('rea', 'Redis primary', ['ElastiCache t4g.micro', 'TLS + at-rest encryption'], 740, 562, w=175, h=84, cat='db')
    d.node('reb', 'Redis replica', ['promoted on failure', 'Multi-AZ failover'], 975, 562, w=175, h=84, cat='db')
    d.node('cw', 'CloudWatch alarms', ['ELB 5XX', 'target 5XX', 'unhealthy hosts'], 1440, 190, w=180, h=84, cat='mgmt')
    d.node('sns', 'SNS topic', ['email subscription', 'confirm it before testing'], 1440, 330, w=180, cat='integ')
    d.node('mail', 'Operator', ['receives the alert email'], 1440, 460, w=180, cat='ext')
    d.node('sec', 'Security baseline', ['IAM task roles, least privilege', 'AWS-managed KMS keys', 'DB secret via Secrets Manager'], 235, 590, w=200, h=84, cat='sec')

    d.edge('usr', 'r', 'cf', 'l', 'HTTPS', so=0.5, do=0.5)
    d.edge('usr', 't', 'r53', 'l', 'optional', dashed=True, via=[(110, 135)], lseg=1)
    d.edge('r53', 'b', 'cf', 't', 'alias', dashed=True)
    d.edge('waf', 't', 'cf', 'b', 'web ACL', dashed=True)
    d.edge('cf', 'r', 'alb', 'l', 'HTTP :80', do=0.8, via=[(475, 305), (475, 246)], lseg=2)
    d.edge('alb', 'b', 'ta', 't', 'target group', so=(730 - 545) / 800, do=0.5)
    d.edge('alb', 'b', 'tb', 't', 'target group', so=(1160 - 545) / 800, do=0.5)
    d.edge('ta', 'b', 'rda', 't', '5432', so=0.235, do=0.5)
    d.edge('ta', 'b', 'rea', 't', '6379', so=0.765, do=0.5)
    d.edge('tb', 'b', 'reb', 't', '6379', so=0.235, do=0.5)
    d.edge('tb', 'b', 'rdb', 't', '5432', so=0.762, do=0.5)
    d.edge('rea', 'r', 'reb', 'l', 'async')
    d.edge('rda', 'b', 'rdb', 'b', 'synchronous replication', via=[(632, 680), (1257, 680)], lseg=1)
    d.edge('ta', 't', 'nata', 'b', 'egress', so=0.189, do=0.5)
    d.edge('tb', 't', 'natb', 'b', 'egress', so=0.189, do=0.5)
    d.edge('alb', 'r', 'cw', 'l', 'metrics', dashed=True)
    d.edge('cw', 'b', 'sns', 't', 'ALARM')
    d.edge('sns', 'b', 'mail', 't', 'email')
    for nid, n in (('usr', 1), ('waf', 2), ('cf', 3), ('alb', 4), ('ta', 5), ('rda', 6), ('nata', 7), ('cw', 8)):
        d.badge(nid, n)
    for n, s in [
        (1, 'A user requests https://<edge-domain>; HTTP is redirected to HTTPS and TLS ends at CloudFront.'),
        (2, 'WAF inspects every request at the edge: a rate limit per IP and the Common and SQL-injection managed rule groups (403 when blocked).'),
        (3, 'CloudFront forwards dynamic requests to the ALB (caching disabled) and caches /static/* at the edge to absorb traffic peaks.'),
        (4, 'The ALB accepts traffic only from CloudFront and sends it to healthy targets in both AZs; it removes failing targets.'),
        (5, 'Fargate tasks in private subnets serve the request. ECS replaces a failed task and auto scaling keeps 2 to 6 tasks.'),
        (6, 'Tasks use PostgreSQL (synchronous standby, automatic failover) and Redis (replica promoted on failure) in isolated subnets.'),
        (7, 'Tasks reach the internet (image pull) through one NAT gateway per AZ, so one AZ failure does not cut outbound traffic.'),
        (8, 'CloudWatch alarms on ELB 5XX, target 5XX and unhealthy hosts notify the operator through SNS email. Nobody has to act to recover.'),
    ]:
        d.step(n, s)
    finish(d, '06-resilient-web-application', 840)


if __name__ == '__main__':
    for fn in (d1, d2, d3, d4, d5, d6):
        fn()
