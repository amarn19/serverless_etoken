import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from src.repositories.repository import checkSlot

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)

# function to fetch single user details
def check(body):
    try:
        zipcode = body['zipcode']
        store_name = body['store_name']
        logger.info(zipcode)
        logger.info(store_name)
        response = checkSlot(zipcode,store_name)
    except (ClientError, KeyError) as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def checkAvailability(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = check(body)
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
