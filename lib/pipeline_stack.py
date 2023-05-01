import aws_cdk as cdk
from aws_cdk import (
    Stack,
    StackProps,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_iam as iam,
    aws_codepipeline_actions as codepipeline_actions,
)
from constructs import Construct

class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # import repository name from repository stack
        repository_name = codecommit.Repository.from_repository_name(
            self,
            'QuicksightContinuousDeployRepository',
            repository_name=f"quicksight-continuous-deploy-{self.region}-{self.account}",
        )

        # create codebuild role
        codebuild_role = iam.Role(
            self,
            'QuicksightContinuousDeployCodeBuildRole',
            assumed_by=iam.ServicePrincipal('codebuild.amazonaws.com'),
        )

        # attach policy to codebuild role
        iam.ManagedPolicy(
            self, 
            'QuicksightContinuousDeployCodeBuildPolicy',
            managed_policy_name='QuicksightContinuousDeployCodeBuildPolicy',
            statements=[
                iam.PolicyStatement(
                    actions=['sts:AssumeRole'],
                    resources=['*']
                    )
                ],
            roles=[codebuild_role]
        )

        # create codebuild project
        codebuild_project = codebuild.PipelineProject(
            self,
            'QuicksightContinuousDeployCodeBuildProject',
            project_name='quicksight-continuous-deploy-codebuild-project',
            role=codebuild_role,
            build_spec=codebuild.BuildSpec.from_asset(
                './obj/buildspecs/prod_deploy.yaml'
            ),
        )

        # create the source output artifact
        source_output=codepipeline.Artifact()

        # create codecommit stage
        commit_stage = codepipeline.StageOptions(
            stage_name='Commit',
            actions=[
                codepipeline_actions.CodeCommitSourceAction(
                    action_name='CodeCommit_Source',
                    repository=repository_name,
                    branch='main',
                    output=source_output,
                )
            ],
        )

        # create codebuild stage
        # in this case, we will let the codebuild environment deploy the dashboard for us
        codebuild_stage = codepipeline.StageOptions(
            stage_name='Deploy',
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name='Deploy',
                    project=codebuild_project,
                    input=source_output,
                )
            ]
        )

        # create codepipeline
        pipeline = codepipeline.Pipeline(
            self,
            'QuicksightContinuousDeployPipeline',
            pipeline_name='quicksight-continuous-deploy-pipeline',
            stages=[
                commit_stage,
                codebuild_stage
            ]
        )

        # output the build project name in CfnOutput
        cdk.CfnOutput(
            self, 'CodeBuildProjectName',
            value=codebuild_project.project_name,
            export_name="CodeBuildProjectName"
        )

        # output the pipeline in CfnOutput
        cdk.CfnOutput(
            self, 'PipelineName',
            value=pipeline.pipeline_name,
            export_name="PipelineName"
        )
