from aws_cdk import CfnOutput, Stack, aws_wafv2 as wafv2
from constructs import Construct


def visibility(metric_name: str) -> wafv2.CfnWebACL.VisibilityConfigProperty:
    return wafv2.CfnWebACL.VisibilityConfigProperty(
        cloud_watch_metrics_enabled=True,
        metric_name=metric_name,
        sampled_requests_enabled=True,
    )


class WafStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        acl = wafv2.CfnWebACL(
            self, "EdgeWebAcl",
            scope="CLOUDFRONT",               # CloudFront WAF ACLs must live in us-east-1
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            visibility_config=visibility("resilientWebAcl"),
            rules=[
                # Flood protection: block an IP that sends more than 500 requests in 5 minutes.
                wafv2.CfnWebACL.RuleProperty(
                    name="RateLimitPerIp",
                    priority=0,
                    action=wafv2.CfnWebACL.RuleActionProperty(block={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                            limit=500, aggregate_key_type="IP",
                        ),
                    ),
                    visibility_config=visibility("rateLimitPerIp"),
                ),
                # Broad web exploits: cross-site scripting, bad inputs, oversized bodies.
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSCommonRules",
                    priority=1,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),  # keep the group's own actions
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS", name="AWSManagedRulesCommonRuleSet",
                        ),
                    ),
                    visibility_config=visibility("awsCommonRules"),
                ),
                # SQL injection patterns. They are NOT in the Common rule set.
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSSqliRules",
                    priority=2,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS", name="AWSManagedRulesSQLiRuleSet",
                        ),
                    ),
                    visibility_config=visibility("awsSqliRules"),
                ),
            ],
        )

        self.web_acl_arn = acl.attr_arn
        CfnOutput(self, "WebAclArn", value=acl.attr_arn)
