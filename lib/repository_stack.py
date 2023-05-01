import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
)
from constructs import Construct

class RepositoryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a repository in CodeCommit
        repository = codecommit.Repository(
            self,
            "QuicksightContinuousDeployRepository",
            repository_name=f"quicksight-continuous-deploy-{self.region}-{self.account}",
            description="Repository for Quicksight Continuous Deploy",
            code=codecommit.Code.from_directory('./obj/commit_files'),
        )
