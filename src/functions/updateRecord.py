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

# function to construct userProfile request and update userProfile in dynambodb
def updateRecord(body):
    try:
        pk = body['pk']
        sk = body['sk']
        item = body['item']
        logger.info(pk)
        logger.info(sk)
        logger.info(item)
        response = etoken_table.update_item(
            Key={
                'pk': pk,
                'sk': sk
            },
            UpdateExpression="set #t = :a",
            ExpressionAttributeNames={
                '#t': item['key']
            },
            ExpressionAttributeValues={
                ':a': item
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logger.info(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

# Lambda handler function
def userProfile(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        response = userProfileCreation(body)
        logger.info(response)
        return {'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Succesfully created user profile')}
    except Exception as e:
        logger.info('Closing lambda function')
        logger.info(e)
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating user profile')
        }
