from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticache as elasticache,
    aws_elasticloadbalancingv2 as elbv2,
    aws_rds as rds,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from constructs import Construct


class ResilientWebStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        web_acl_arn: str,                 # from the WAF stack output (WebAclArn)
        cloudfront_prefix_list_id: str,   # managed prefix list of the CloudFront origin-facing servers
        alert_email: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Network: two AZs. Public subnets for the load balancer,
        #    private subnets with egress for tasks, isolated subnets for data.
        vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2,
            nat_gateways=2,         # one per AZ, so an AZ failure does not cut outbound traffic
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="app", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
                ec2.SubnetConfiguration(name="data", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24),
            ],
        )

        # 2. Database: PostgreSQL with a synchronous standby in another AZ.
        db = rds.DatabaseInstance(
            self, "Db",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            multi_az=True,
            allocated_storage=20,
            credentials=rds.Credentials.from_generated_secret("appadmin"),   # password in Secrets Manager
            storage_encrypted=True,
            backup_retention=Duration.days(1),
            deletion_protection=False,              # lab only
            removal_policy=RemovalPolicy.DESTROY,   # lab only
            delete_automated_backups=True,          # lab only
        )

        # 3. Cache: Redis with a replica in another AZ and automatic failover.
        cache_subnets = elasticache.CfnSubnetGroup(
            self, "CacheSubnets",
            description="Isolated subnets for the cache",
            subnet_ids=[subnet.subnet_id for subnet in vpc.isolated_subnets],
        )
        cache_sg = ec2.SecurityGroup(self, "CacheSg", vpc=vpc)
        cache = elasticache.CfnReplicationGroup(
            self, "Cache",
            replication_group_description="Resilient web app cache",
            engine="redis",
            engine_version="7.1",
            cache_node_type="cache.t4g.micro",
            num_cache_clusters=2,                 # primary + replica
            automatic_failover_enabled=True,
            multi_az_enabled=True,
            at_rest_encryption_enabled=True,
            transit_encryption_enabled=True,
            cache_subnet_group_name=cache_subnets.ref,
            security_group_ids=[cache_sg.security_group_id],
        )
        cache.add_dependency(cache_subnets)

        # 4. Compute: ECS on Fargate behind an internet-facing ALB, 2 tasks spread over AZs.
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        web = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Web",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            public_load_balancer=True,
            open_listener=False,            # do not open the ALB to 0.0.0.0/0 (see step 5)
            min_healthy_percent=100,        # a rollout never drops below the desired count
            max_healthy_percent=200,
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),   # a release that cannot start is rolled back
            task_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("public.ecr.aws/nginx/nginx:stable"),
                container_port=80,
                environment={
                    "DB_HOST": db.instance_endpoint.hostname,
                    "CACHE_HOST": cache.attr_primary_end_point_address,
                },
                # The password is injected by ECS from Secrets Manager; it never appears in the template.
                secrets={"DB_SECRET": ecs.Secret.from_secrets_manager(db.secret)},
            ),
        )
        # The ALB health check drives replacement. We do not add a container health check:
        # it needs a tool (curl) that the nginx image may not contain, and a failing one would kill every task.
        web.target_group.configure_health_check(
            path="/",
            healthy_http_codes="200",
            interval=Duration.seconds(15),
            healthy_threshold_count=2,
            unhealthy_threshold_count=2,
        )
        web.target_group.set_attribute("deregistration_delay.timeout_seconds", "30")

        # Scale between 2 and 6 tasks by CPU.
        scaling = web.service.auto_scale_task_count(min_capacity=2, max_capacity=6)
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=60,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        # 5. Network rules: only the expected traffic flows between tiers.
        db.connections.allow_default_port_from(web.service, "App to database")
        cache_sg.connections.allow_from(web.service, ec2.Port.tcp(6379), "App to cache")
        # The ALB accepts traffic only from CloudFront, so the WAF cannot be bypassed by calling the ALB directly.
        web.load_balancer.connections.allow_from(
            ec2.Peer.prefix_list(cloudfront_prefix_list_id),
            ec2.Port.tcp(80),
            "CloudFront origin-facing only",
        )

        # 6. Edge: CloudFront in front of the ALB, with the WAF ACL attached.
        alb_origin = origins.LoadBalancerV2Origin(
            web.load_balancer,
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,  # TLS ends at CloudFront (see Known limitations)
        )
        distribution = cloudfront.Distribution(
            self, "Edge",
            default_behavior=cloudfront.BehaviorOptions(      # dynamic content: never cached
                origin=alb_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
            ),
            additional_behaviors={
                "/static/*": cloudfront.BehaviorOptions(      # static assets: cached at the edge to absorb peaks
                    origin=alb_origin,
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                ),
            },
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,   # cheaper edge locations (lab)
            web_acl_id=web_acl_arn,
        )

        # 7. Alarms. Three signals, all to the same SNS topic:
        #    - target 5XX: the application answered with an error;
        #    - ELB 5XX: the load balancer itself failed (it returns 503 when NO target is healthy);
        #    - unhealthy hosts: a task fails its health check.
        alerts = sns.Topic(self, "AlertsTopic")
        alerts.add_subscription(subs.EmailSubscription(alert_email))
        one_minute = {"period": Duration.minutes(1), "statistic": "Sum"}

        target_5xx = cloudwatch.Alarm(
            self, "Target5xxAlarm",
            metric=web.load_balancer.metrics.http_code_target(
                elbv2.HttpCodeTarget.TARGET_5XX_COUNT, **one_minute),
            threshold=5,
            evaluation_periods=3,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        elb_5xx = cloudwatch.Alarm(
            self, "Elb5xxAlarm",
            metric=web.load_balancer.metrics.http_code_elb(
                elbv2.HttpCodeElb.ELB_5XX_COUNT, **one_minute),
            threshold=5,
            evaluation_periods=3,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        unhealthy = cloudwatch.Alarm(
            self, "UnhealthyHostsAlarm",
            metric=web.target_group.metrics.unhealthy_host_count(period=Duration.minutes(1)),
            threshold=1,
            evaluation_periods=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        for alarm in (target_5xx, elb_5xx, unhealthy):
            alarm.add_alarm_action(cw_actions.SnsAction(alerts))

        CfnOutput(self, "EdgeDomain", value=distribution.distribution_domain_name)
        CfnOutput(self, "DbEndpoint", value=db.instance_endpoint.hostname)
        CfnOutput(self, "CacheEndpoint", value=cache.attr_primary_end_point_address)
