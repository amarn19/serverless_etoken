import json
import boto3
import ast
import os
from botocore.exceptions import ClientError

def loginUser(event,context,dynamodb=None):
        try:
            if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
            etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
            body = ast.literal_eval(event['body'])
            user_id = body ['user_id']
            user_type = body ['user_type']
            print(user_id)
            resp = etoken_table.get_item(
                Key={
                'pk': user_id,
                'sk': password
            }
            )
    
            print(resp)
            if ('Item' in resp):
                return {
                    'statusCode': 200,
                    'headers': {"Access-Control-Allow-Origin": "*","Access-Control-Allow-Credentials": True,"Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login Successful')
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': {"Access-Control-Allow-Origin": "*","Access-Control-Allow-Credentials": True,"Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Incorrect login credentials.Try again')
            }
        except ClientError as e:
            print('Closing lambda function')
            print(e.response['Error']['Message'])
            return {
                    'statusCode': 400,
                    'headers': {"Access-Control-Allow-Origin": "*","Access-Control-Allow-Credentials": True,"Access-Control-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login failed.Try again')
            }