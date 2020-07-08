import ast
import boto3
import os
import json
from botocore.exceptions import ClientError


def deleteUser(event,context,dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        password = body['password']
        print(user_id)
        
        response = etoken_table.delete_item(
            Key={
                'pk': user_id,
                'sk': password
            }
        )
        print(response)
        return {'statusCode': 200, 'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"}, 'body': json.dumps('Succesfully deleted user')}
    
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"},
            'body': json.dumps('Error deleting user')
        }
