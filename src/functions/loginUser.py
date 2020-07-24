import json
import boto3
import ast
import os
import logging
from botocore.exceptions import ClientError

# dynamodb instance creation
dynamodb = boto3.resource('dynamodb')
# fetching dynamodb table
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def userLogin(body):
    try:
        user_id = body ['user_id']
        user_type = body ['user_type']
        logger.info(user_id)
        logger.info(user_type)
        response = etoken_table.get_item(
                Key={
                'pk': user_id,
                'sk': user_type
                }
            )
    except (ClientError, KeyError) as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
    
# Lambda handler function
def loginUser(event,context,dynamodb=None):
        try:
            body = ast.literal_eval(event['body'])
            response = userLogin(body)
            logger.info(response)
            if ('Item' in resp):
                return {
                    'statusCode': 200,
                    'headers': {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Credentials": True,
                        "Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login Successful')
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Credentials": True,
                        "Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Incorrect login credentials.Try again')
            }
        except ClientError as e:
            print('Closing lambda function')
            print(e.response['Error']['Message'])
            return {
                    'statusCode': 400,
                    'headers': {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Credentials": True,
                        "Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login failed.Try again')
            }