import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from src.repositories.repository import fetchUsers

# dynamodb instance creation
dynamodb = boto3.resource('dynamodb')
# fetching dynamodb table
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

# function to fetch all users 
def fetchAllUsers():
    try:
         response = fetchUsers()
         while 'LastEvaluatedKey' in response:
            response = etoken_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
    
# Lambda handler function
def getUsers(event, context, dynamodb=None):
    try:
        response = fetchAllUsers()
        data = response['Items']
        
        logger.info(response)
        return {'statusCode': 200,
                'headers':
                    {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps(data, default=default)
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
