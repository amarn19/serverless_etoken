import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from src.repositories.repository import removeUser 

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to construct userDeletion request and delete user item in dynambodb
def userDeletion(body):
    try:
        user_id = body['user_id']
        user_type = body['user_type']
        logger.info(user_id)
        response = removeUser(user_id,user_type)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def deleteUser(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = userDeletion(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers':
                    {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully deleted user')}
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers':
                {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error in deleting user')
        }
