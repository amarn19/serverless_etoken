import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError

# dynamodb instance creation
dynamodb = boto3.resource('dynamodb')
# fetching dynamodb table
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to construct storeCreation request and post item to dynambodb
def storeCreation(body):
    try:
        zipcode = body['zipcode']
        store_name = body['store_name']
        store_details = body['store_details']
        slots = body['slots']
        item = {
            'pk': zipcode,
            'sk': store_name,
            'store_details': store_details,
            'slots': slots
        }
        logger.info(item)
        response = etoken_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(pk) AND attribute_not_exists(sk)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def createStore(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = storeCreation(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully created Store')}
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e)
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Credentials": True, 
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating Store')
        }
