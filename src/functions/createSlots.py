import ast
import boto3
import os
import json
from botocore.exceptions import ClientError

if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])

def createSlots(event, context, dynamodb=None):
    try:
        body = ast.literal_eval(event['body'])
        zipcode = body['zipcode']
        store_name = body['store_name']
        slots=body['slots']
        print(zipcode, store_name,slots)
        response = etoken_table.update_item(
            Key={
                'pk': zipcode,
                'sk': store_name
            },
            UpdateExpression="set #t = :a",
            ExpressionAttributeNames={
                '#t': 'slots'
            },
            ExpressionAttributeValues={
                ':a': slots
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)
        return {'statusCode': 200, 'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"}, 'body': json.dumps('Succesfully created slot')}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating slot')
        }
