import ast
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError

#dynamodb instance creation
dynamodb = boto3.resource('dynamodb')
#fetching dynamodb table
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
#Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#function to construct userCreation request and post item to dynambodb
def userCreation(body):
    try:
        user_id = body['user_id']
        item_type = body['item_type']
        user_type = body['user_type']
        dashboard = body['dashboard']
        user_details = body['user_details']
        item = {
            'pk': user_id,
            'sk': user_type,
            'dashboard': dashboard,
            'type': item_type,
            'user_details': user_details
        }
        if user_type == "shopper":
            history = body['history']
            item.update({'history': history})
        elif user_type == "store_owner":
            store_details = body['store_details']
            messages = body['messages']
            item.update({'store_details': store_details, 'messages': messages})
            logger.info(user_id)
            logger.info(user_type)
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

#Lambda handler function 
def createUser(event, context, dynamodb=None):

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
