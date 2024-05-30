from aws_cdk import (
    Stack,
)
from aws_cdk.aws_lambda import Runtime, LayerVersion
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from cdklabs.generative_ai_cdk_constructs.bedrock import Agent, AgentActionGroup, ApiSchema, BedrockFoundationModel
from constructs import Construct

class CdkLambdaBedrockStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # THis is where the magic happens
        agent = Agent(
            self,
            "Agent",
            foundation_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_INSTANT_V1_2,
            instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
        )

        lambda_layer = LayerVersion.from_layer_version_arn(
            self, "AWSLambdaPowertoolsPythonV2",
            # "arn:aws:lambda:us-west-2:017000801446:layer:AWSLambdaPowertoolsPythonV2:71" # for us-west-2
            "arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:71"
        )

        action_group_function = PythonFunction(
            self,
            "LambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            entry="./lambda",  
            index="app.py",
            handler="lambda_handler",
            layers=[lambda_layer]
        )


        action_group = AgentActionGroup(
            self,
            "ActionGroup",
            action_group_name="TimeFunctions",
            description="Functions for getting the current time and other time related functions",
            action_group_executor=action_group_function,
            action_group_state="ENABLED",
            api_schema=ApiSchema.from_asset("./lambda/openapi.json"),  
        )

        # 2nd function
        mytodo_group_function = PythonFunction(
            self,
            "2LambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            entry="./lambda_two",  
            index="app.py",
            handler="lambda_handler",
            layers=[lambda_layer]
        )
        # 2nd action group
        mytodo_group = AgentActionGroup(
            self,
            "MytodoGroup",
            action_group_name="TodoListManagementFunctions",
            description="Use this action group to manage a TODO list",
            action_group_executor=mytodo_group_function,
            action_group_state="ENABLED",
            api_schema=ApiSchema.from_asset("./lambda_two/openapi.json"),  
        )


        # Associate actiong roup to the bla
        agent.add_action_group(action_group)
        agent.add_action_group(mytodo_group)
