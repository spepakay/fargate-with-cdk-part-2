#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from fargate_with_cdk_part_2.platform_stack import PlatformStack
from fargate_with_cdk_part_2.db_stack import DbStack

app = core.App()

platform = PlatformStack(app, "PlatformStack")
db = DbStack(app, "DbStack", platform.cluster, platform.sg_db)

app.synth()
