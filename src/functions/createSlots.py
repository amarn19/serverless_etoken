import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from src.repositories.repository import newSlots
from datetime import datetime
import time

# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#function to construct userCreation request and post item to dynambodb
def slotsCreation(body):
    try:
        zipcode = body['zipcode']
        store_name = body['store_name']
        slot_date = body['slot_date']
        start_time = body['start_time']
        end_time = body['end_time']
        shopping_time = body ['shopping_time']
        capacity = body ['capacity']
        tokens = generateTokens(start_time,end_time,shopping_time,capacity)
        logger.info(tokens)
        slot_info={
                'capacity':capacity,
                'start_time':start_time,
                'end_time':end_time,
                'shopping_time':shopping_time,
                'tokens':tokens
        }
        if slot_date[0]==slot_date[1]:
            response = newSlots(zipcode,store_name,slot_date[0],slot_info)
        else:
            for d in slot_date:
                response = newSlots(zipcode,store_name,d,slot_info)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
    
def generateTokens(start_time,end_time,shopping_time,capacity):
    shopping_time=datetime.strptime(shopping_time, '%H:%M').hour*3600+datetime.strptime(shopping_time, '%H:%M').minute*60
    diff = (datetime.strptime(end_time, '%H:%M')-datetime.strptime(start_time, '%H:%M')).seconds
    tokens=int(diff/shopping_time)*int(capacity)
    return tokens

def createSlots(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = slotsCreation(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers':
                    {"Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully created slot')}
    except Exception as e:
        logger.info('Closing lambda function')
        return {
            'statusCode': 400,
            'headers':
                {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating slot')
        }
