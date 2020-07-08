import ast
import boto3
import os
import json
from botocore.exceptions import ClientError
from decimal import Decimal

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def getUser(event, context, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        password = body['password']
        print(user_id)

        response = etoken_table.get_item(
            Key={
                'pk': user_id,
                'sk': password
            })

        print(response)
        return {'statusCode': 200, 'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"}, 'body': json.dumps(response['Item'],default=default)}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"},
            'body': json.dumps('Error fetching user')
        }
