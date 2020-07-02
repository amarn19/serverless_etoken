import json
import boto3
import ast
import os

def loginUser(event,context,dynamodb=None):
        try:
            if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
            etoken_table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
            body = ast.literal_eval(event['body'])
            user_id = body ['user_id']
            password = body ['password']
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
                    'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login Successful')
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                    'body': json.dumps('Incorrect login credentials.Try again')
            }
        except:
            print('Closing lambda function')
            return {
                    'statusCode': 400,
                    'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                    'body': json.dumps('Login failed.Try again')
            }