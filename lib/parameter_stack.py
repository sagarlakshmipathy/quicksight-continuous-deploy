from aws_cdk import (
    Stack,
    aws_ssm as ssm,
)
from constructs import Construct

class ParameterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create parameters in SSM Parameter Store
        # source region parameter
        ssm.StringParameter(
            self,
            "QuickSightSourceRegion",
            parameter_name="/quicksight-continuous-deploy/source-region",
            string_value=self.region
        )

        # source account parameter
        ssm.StringParameter(
            self,
            "QuickSightSourceAccount",
            parameter_name="/quicksight-continuous-deploy/source-account-id",
            string_value=self.account
        )

        # target region parameter
        ssm.StringParameter(
            self,
            "QuickSightTargetRegion",
            parameter_name="/quicksight-continuous-deploy/target-region",
            string_value=self.region
        )

        # target account parameter
        ssm.StringParameter(
            self,
            "QuickSightTargetAccount",
            parameter_name="/quicksight-continuous-deploy/target-account-id",
            string_value=self.account
        )

        # dashboard id parameter
        ssm.StringParameter(
            self,
            "QuickSightDashboardId",
            parameter_name="/quicksight-continuous-deploy/dashboard-id",
            string_value="quicksight-continuous-deploy-dashboard"
        )

        # dashboard name parameter
        ssm.StringParameter(
            self,
            "QuickSightDashboardName",
            parameter_name="/quicksight-continuous-deploy/dashboard-name",
            string_value="Quicksight Continuous Deploy Dashboard"
        )
