#!/usr/bin/env python3
import aws_cdk as cdk
from lib.parameter_stack import ParameterStack
from lib.pipeline_stack import PipelineStack
from lib.repository_stack import RepositoryStack

app = cdk.App()
ParameterStack(app, "ParameterStack")
RepositoryStack(app, "RepositoryStack")
PipelineStack(app, "PipelineStack")

app.synth()
