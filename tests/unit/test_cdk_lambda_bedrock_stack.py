import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_lambda_bedrock.cdk_lambda_bedrock_stack import CdkLambdaBedrockStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_lambda_bedrock/cdk_lambda_bedrock_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkLambdaBedrockStack(app, "cdk-lambda-bedrock")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
