#!/usr/bin/env python3
import os

import aws_cdk as cdk

from image_moderation.image_moderation_stack import ImageModerationStack

app = cdk.App()
ImageModerationStack(
    app, "ImageModerationStack",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION"),
    ),
)
app.synth()
