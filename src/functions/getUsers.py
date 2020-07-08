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

def getUsers(event, context, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])

        response = etoken_table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = etoken_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        print(response)
        return {'statusCode': 200, 'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"}, 'body': json.dumps(data,default=default)}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating user')
        }
