
# Welcome to the Powertools + CDK + Bedrock Agents Template

This project contains a template for using AWS Powertools and CDK to deploy lambda-powered Bedrock Agents.
Each of these things, CDK, Powertools, Lambda, and Bedrock, are awesome and powerful.
This template shows you how to use them all together.

Comments, suggestions, pull requests, are very welcome.

Author: [Stephen J. Barr (@stevejb on X)](https://x.com/stevejb).

## Layout

The core of the stack is seen in the `cdk_lambda_bedrock/cdk_lambda_bedrock_stack.py` folder.
This stack contains:

+ A single Agent
+ A reference to an existing Lambda Layer for AWS Power Tools
+ Two **Action Groups** 
+ For each **Action Group**, a `PythonFunction`
+ The `PythonFunction`'s share a common Lambda Layer. 
This is [provided here](https://docs.powertools.aws.dev/lambda/python/latest/#lambda-layer).

``` mermaid
graph TD;
    A[Stack] --> B[Agent]
    B --> C[AgentActionGroup - TimeFunctions]
    B --> D[AgentActionGroup - TodoListManagementFunctions]
    C --> E[LambdaFunction - TimeFunctions<br/><code>lambda/app.py</code>]
    D --> F[LambdaFunction - TodoListManagementFunctions<br/><code>lambda_two/app.py</code>]
    E --> G[AWSLambdaPowertoolsPythonV2 Layer]
    F --> G

    subgraph Lambda Functions
        E
        F
    end

    subgraph Agent Action Groups
        C
        D
    end

    subgraph Bedrock Foundation Model
        B
    end

    subgraph Layers
        G
    end
```

## Prerequisites

- Python 3
- AWS users with permission to create required resources. See [Sample IAM Policy](./sample_iam_policy.json)
- Install [aws-cdk]( https://github.com/aws/aws-cdk)
- Install [Docker](https://www.docker.com/)

## Steps to get started

### 1 - Clone the repository

``` shell
git clone git@github.com:stephenVertex/cdk-lambda-bedrock-template.git
cd cdk-lambda-bedrock-template/
```
**NOTE:** Make sure that you change the stack name in `app.py`.

``` python
CdkLambdaBedrockStack(app, "CdkLambdaBedrockStack", ## <-- Change this to your desired stack name
```

### 2 - Make a virtual environment. 

``` shell
python3 -m venv .venv
source .venv/bin/activate
```
and install the dependencies

``` shell
pip3 install -r requirements.txt
```

### 3 -  Make sure Docker is running. 

The `docker ps` command should work.

``` shell
❯ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### 4 - Add a policy for cdk bootstrap

``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::{ACCT_NUMBER}:role/cdk-hnb659fds-deploy-role-*",
                "arn:aws:iam::{ACCT_NUMBER}:role/cdk-hnb659fds-file-publishing-*",
                "arn:aws:iam::{ACCT_NUMBER}:role/cdk-hnb659fds-lookup-role-*",
                "arn:aws:iam::{ACCT_NUMBER}:role/cdk-readOnlyRole"
            ]
        }
    ]
}
```
Note that `hnb659fds` is the default value of the all resources in the CDK "bootstrap stack."
If you need to change this, you will know what to do.

### 5 Deploy

Run `./deploy.sh`.

The deployment script makes sure that the API specifications are nice.

``` shell
cd lambda
python3 app.py > openapi.json
cd ..

cd lambda_two
python3 app.py > openapi.json
cd ..

cdk deploy

```

# CDK General Advice
## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

# Resources

The [Agents for Bedrock page on AWS Powertools](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/bedrock_agents/)
contains much of this same information. I have just made it into one deployable template.

# Acknowledgements

Huge thank you to [Darko Mesaroš](https://x.com/darkosubotica) for helping me wrap my brain around CDK.
