
# Continuously deploy your dashboards across environments in Amazon QuickSight!

## About the project
Continuous Deploy is one of the standard practices followed by companies to promote code/software from lower environment to higher environment. This project will help you deploy your dashboards from your Development account to Production account without any manual intervention as soon as one commits the dashboard to the source repository.

This repo follows the below architecture to port dashboards:

<img width="803" alt="image" src="https://user-images.githubusercontent.com/30472234/235430476-e0cd1220-9b73-4a50-8577-f945dfd8dafc.png">


Please deploy the below stack in your environment and follow the steps mentioned in `Trigger the pipeline` section.

## Deployment steps

First clone this repo in your local and switch to the directory:

```
git clone https://github.com/sagarlakshmipathy/quicksight-continuous-deploy.git && cd quicksight-continuous-deploy
```

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Trigger the pipeline

Once the deployment is done. All you need to do is trigger the pipeline to see the dashboard migrating to the target account. To achieve it, I've provided a python file which takes dashboard id as one of the arguments and commits the definition json to the source control repository.

1. Run the below commands to update the target account and target region of your production QuickSight environment
`aws ssm  put-parameter --name /quicksight-continuous-deploy/target-account-id --value PROD_ACCOUNT_ID --type String --overwrite`
`aws ssm  put-parameter --name /quicksight-continuous-deploy/target-region --value PROD_REGION --type String --overwrite`
2. Login to your production account and create a policy as below:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "quicksight:CreateDashboard",
                "quicksight:UpdateDashboard",
                "quicksight:UpdateDashboardPermissions",
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```
3. Create a role in your production account by adding your development account to AssumeRole this role.
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::{DEV_ACCOUNT_ID}:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
4. Make sure you are in the root directory of quicksight-continuous-deploy folder
5. Run `python3 app/commit_dashboard.py --dashboard_id DASHBOARD_ID --account_id ACCOUNT_ID --region REGION --author_name AUTHOR_NAME --email EMAIL --user_name USER_NAME --namespace NAMESPACE`
Note 1: `--user_name` and `--namespace` fields are optional
Note 2: If you set the `--user_name` and `--namespace` fields, your dashboard will be provisioned with set user as owner of the dashboard

Voila! This should trigger the Continuous Deploy pipeline and deploy your dashboard to your Prod account.
