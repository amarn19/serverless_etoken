import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from src.repositories.repository import newSlots

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#function to construct userCreation request and post item to dynambodb
def slotsCreation(body):
    try:
        zipcode = body['zipcode']
        store_name = body['store_name']
        slots = body['slots']
        response = newSlots(zipcode,store_name,slots)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

def createSlots(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = userCreation(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers':
                    {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully created user')}
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers':
                {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating user')
        }
    
    
    
    try:
        body = ast.literal_eval(event['body'])
        
        return {'statusCode': 200, 'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"}, 'body': json.dumps('Succesfully created slot')}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating slot')
        }
