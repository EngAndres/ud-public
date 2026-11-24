#!/usr/bin/env python3
import os

import aws_cdk as cdk

from resilient_web.waf_stack import WafStack
from resilient_web.resilient_web_stack import ResilientWebStack

app = cdk.App()
account = os.environ.get("CDK_DEFAULT_ACCOUNT")
region = os.environ.get("CDK_DEFAULT_REGION")
alert_email = app.node.try_get_context("alertEmail") or "you@example.com"

WafStack(app, "WafStack", env=cdk.Environment(account=account, region="us-east-1"))

ResilientWebStack(
    app, "ResilientWebStack",
    env=cdk.Environment(account=account, region=region),
    web_acl_arn=(app.node.try_get_context("webAclArn")
                 or "arn:aws:wafv2:us-east-1:000000000000:global/webacl/placeholder/00000000"),
    cloudfront_prefix_list_id=app.node.try_get_context("cfPrefixListId") or "pl-00000000",
    alert_email=alert_email,
)
app.synth()
