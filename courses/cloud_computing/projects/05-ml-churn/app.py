#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ml_churn.ml_churn_stack import MlChurnStack

app = cdk.App()
MlChurnStack(
    app, "MlChurnStack",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION"),
    ),
)
app.synth()
