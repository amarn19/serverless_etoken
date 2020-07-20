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
        user_type = body['user_type']
        print(user_id)

        response = etoken_table.get_item(
            Key={
                'pk': user_id,
                'sk': user_type
            })
        if 'Item' not in response:
            raise KeyError('User does not exist')
        print(response)
        return {'statusCode': 200, 'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"}, 'body': json.dumps(response,default=default)}
    except (ClientError,KeyError) as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"},
            'body': 'Error:{}'.format(e)
        }
