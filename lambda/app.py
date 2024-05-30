from time import time

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import BedrockAgentResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = BedrockAgentResolver()


@app.get("/current_time", description="Gets the current time in seconds")  
@tracer.capture_method
def current_time() -> int:
    return int(time())

@app.get("/tomorrow_time", description="Gets the time tomorrow")  
@tracer.capture_method
def tomorrow_time() -> int:
    return int(time()) + 86400


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)

if __name__ == "__main__":  
    print(app.get_openapi_json_schema())
