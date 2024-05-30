#!/bin/bash

cd lambda
python3 app.py > openapi.json
cd ..

cd lambda_two
python3 app.py > openapi.json
cd ..

cdk deploy

## TODO Prompt me for a note. Log it somewhere.

## TODO Generate the AWS Management Console URL for the Bedrock Agent, 
## https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/agents/{AGENT_ID}
