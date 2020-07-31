import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from src.repositories.repository import fetchUser

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)

# function to fetch single user details
def userDetails(body):
    try:
        user_id = body['user_id']
        user_type = body['user_type']
        logger.info(user_id)
        logger.info(user_type)
        response = fetchUser(user_id,user_type)
    except (ClientError, KeyError) as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def getUser(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = userDetails(body)
        logger.info(response)
        if 'Item' not in response:
            raise KeyError('User does not exist')
        return {'statusCode': 200,
                'headers':
                    {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps(response['Item'], default=default)
                }
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e)
        return {
            'statusCode': 400,
            'headers':
                {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': 'Error:{}'.format(e)
        }
