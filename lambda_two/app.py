from time import time

from typing import Dict, List, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import BedrockAgentResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
import requests
tracer = Tracer()
logger = Logger()
app = BedrockAgentResolver()


@app.get("/list_todos", description="Gets a list of TODO items")  
@tracer.capture_method
def list_todos() -> Dict[str, List[Dict[str, Any]]]:
    tlist = requests.get("https://jsonplaceholder.typicode.com/todos")
    rv = tlist.json()[0:5]
    print("TODO LIST RETURNS:")
    print(rv)
    return {"todo_list" : rv}


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)

if __name__ == "__main__":  
    print(app.get_openapi_json_schema())
