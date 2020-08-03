import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from src.repositories.repository import updateItem

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to construct userProfile request and update userProfile in dynambodb
def update(body):
    try:
        pk = body['pk']
        sk = body['sk']
        item = body['item']
        response = updateItem(pk,sk,item)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def updateRecord(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = update(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully updated record')}
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e)
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error updating record')
        }
