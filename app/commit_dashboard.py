import boto3
import json
import argparse

# initializing variables
parser = argparse.ArgumentParser(description='Commit a dashboard to a repository')
parser.add_argument('--dashboard_id', help='The dashboard id to commit', type=str, required=True)
parser.add_argument('--account_id', help='The account id to commit to', type=str, required=True)
parser.add_argument('--region', help='The region where QuickSight and CodeCommit repo exists', type=str, required=True)
parser.add_argument('--author_name', help='The name of the author', type=str, required=True)
parser.add_argument('--email', help='The email of the author', type=str, required=True)
parser.add_argument('--user_name', help='Permissions to be provided as owner in target environment', type=str, required=False)
parser.add_argument('--namespace', help='The namespace of the user in target environment', type=str, required=False)

args = parser.parse_args()

# hardcoded variables
repository_name = f"quicksight-continuous-deploy-{args.region}-{args.account_id}"
branch_name = 'main'

# create clients
session = boto3.Session(region_name=args.region)
qs_client = session.client('quicksight')
cc_client = session.client('codecommit')
ssm_client = session.client('ssm')

# extract definition for the dashboard
dashboard_definition = qs_client.describe_dashboard_definition(
    AwsAccountId=args.account_id,
    DashboardId=args.dashboard_id
)

def get_parent_commit_id(repository_name, branch_name):
    """
    Get the parent commit id for the branch
    """
    response = cc_client.get_branch(
        repositoryName=repository_name,
        branchName=branch_name
    )
    return response['branch']['commitId']

# commit the dashboard definition to the repository
commit_reponse = cc_client.create_commit(
    repositoryName=repository_name,
    branchName=branch_name,
    parentCommitId=get_parent_commit_id(repository_name, branch_name),
    authorName=args.author_name,
    email=args.email,
    commitMessage=f"Committing dashboard {args.dashboard_id}",
    putFiles=[
        {
            'filePath': f"{args.dashboard_id}.json",
            'fileContent': json.dumps(dashboard_definition, indent=4, default=str)
        }
    ]
)

# once commit is successful write parameters to parameter store
if commit_reponse['ResponseMetadata']['HTTPStatusCode'] == 200:
    print('Commit successful')

    # write user name to parameter store
    if args.user_name:
        ssm_client.put_parameter(
            Name=f"/quicksight-continuous-deploy/user-name",
            Value=args.user_name,
            Type='String',
            Overwrite=True
        )
        ssm_client.put_parameter(
            Name=f"/quicksight-continuous-deploy/namespace",
            Value=args.namespace,
            Type='String',
            Overwrite=True
        )
    else:
        ssm_client.put_parameter(
            Name=f"/quicksight-continuous-deploy/user-name",
            Value='',
            Type='String',
            Overwrite=True
        )
        ssm_client.put_parameter(
            Name=f"/quicksight-continuous-deploy/namespace",
            Value='',
            Type='String',
            Overwrite=True
        )
    
    # write dashboard id to parameter store
    ssm_client.put_parameter(
        Name=f"/quicksight-continuous-deploy/dashboard-id",
        Value=args.dashboard_id,
        Type='String',
        Overwrite=True
    )

    # write dashboard name to parameter store
    ssm_client.put_parameter(
        Name=f"/quicksight-continuous-deploy/dashboard-name",
        Value=dashboard_definition['Name'],
        Type='String',
        Overwrite=True
    )

else:
    print(commit_reponse)
