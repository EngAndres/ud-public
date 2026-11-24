# 06 - Resilient Web Application (Python)

Source: [../../guides/06-resilient-web-application.md](../../guides/06-resilient-web-application.md)

**Cost warning:** this stack bills about USD 0.20 to 0.25 per hour (NAT gateways, load balancer, Multi-AZ database, cache, WAF). Destroy it the same day.

Two stacks: the WAF stack must be in **us-east-1** (CloudFront requirement), and the application stack is in your region.

## Deploy

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://<ACCOUNT>/us-east-1    # the WAF stack needs us-east-1 too
cdk bootstrap aws://<ACCOUNT>/<YOUR-REGION>

# Step 1: WAF in us-east-1
cdk deploy WafStack

WAF_ARN=$(aws cloudformation describe-stacks --region us-east-1 --stack-name WafStack \
  --query "Stacks[0].Outputs[?OutputKey=='WebAclArn'].OutputValue" --output text)
CF_PL=$(aws ec2 describe-managed-prefix-lists \
  --filters Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing \
  --query "PrefixLists[0].PrefixListId" --output text)

# Step 2: application stack (takes 25 to 40 minutes)
cdk deploy ResilientWebStack -c alertEmail=you@example.com -c webAclArn=$WAF_ARN -c cfPrefixListId=$CF_PL
```

Confirm the SNS subscription in your email before you test.

## Clean up

Delete the application stack first, then the WAF stack:

```bash
cdk destroy ResilientWebStack -c alertEmail=you@example.com -c webAclArn=$WAF_ARN -c cfPrefixListId=$CF_PL
cdk destroy WafStack
```
