import aws_cdk as core
import aws_cdk.assertions as assertions

from quicksight_continuous_deploy.quicksight_continuous_deploy_stack import QuicksightContinuousDeployStack

# example tests. To run these tests, uncomment this file along with the example
# resource in quicksight_continuous_deploy/quicksight_continuous_deploy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = QuicksightContinuousDeployStack(app, "quicksight-continuous-deploy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
