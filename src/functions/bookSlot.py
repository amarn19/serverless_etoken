import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from src.repositories.repository import registerSlot

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to book slot
def book(body):
    try:
        zipcode = body['zipcode']
        store_name = body['store_name']
        slot_date = body['slot_date']
        logger.info(zipcode)
        logger.info(store_name)
        logger.info(slot_date)
        response = registerSlot(zipcode,store_name,slot_date)
    except ClientError as e:
            raise
    else:
        return response

# Lambda handler function
def bookSlot(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = book(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully booked slot')}
    except (Exception,ClientError) as e:
        logger.info('Closing lambda function')
        logger.info(e)
        return {
            'statusCode': 400,
            'headers':
                {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error booking slot')
        }

