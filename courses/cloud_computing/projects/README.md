# Projects: ready-to-deploy versions of the guides

One CDK project per guide. Each one has the full code extracted from its guide, so you can deploy it without copying snippets.

| Folder | Guide | Language | Stack |
|--------|-------|----------|-------|
| [01-doc-processing](01-doc-processing/) | Intelligent document processing | TypeScript | `DocProcessingStack` |
| [02-call-analytics](02-call-analytics/) | Call center analytics | TypeScript | `CallAnalyticsStack` |
| [03-rag-chatbot](03-rag-chatbot/) | Enterprise chatbot with RAG | TypeScript | `RagChatbotStack` |
| [04-image-moderation](04-image-moderation/) | Image moderation pipeline | Python | `ImageModerationStack` |
| [05-ml-churn](05-ml-churn/) | Custom ML with SageMaker | Python | `MlChurnStack` |
| [06-resilient-web](06-resilient-web/) | Resilient web application | Python | `WafStack`, `ResilientWebStack` |

## Requirements

- AWS CLI v2, configured for a sandbox account (`aws sts get-caller-identity`).
- Node.js 20 or 22 (TypeScript projects 01 to 03).
- Python 3.10 or later (projects 04 to 06).
- AWS CDK CLI 2.x (`npm install -g aws-cdk`) if you do not use the `npx cdk` form.
- Bedrock model access enabled for projects 02 and 03.

Each project folder has a `README.md` with the deploy and test commands. Everything here creates resources that cost money. Run `cdk destroy` when you finish each lab.

These projects were generated from the guides and have not been deployed in an AWS account by the author. Run `cdk synth` before `cdk deploy`.
