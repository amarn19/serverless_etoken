import ast
import boto3
import os
import json
from botocore.exceptions import ClientError


def userProfile(event, context, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        user_type = body['user_type']
        item = body['item']
        print(user_id, item, item['key'])
        response = etoken_table.update_item(
            Key={
                'pk': user_id,
                'sk': user_type
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
        print(response)
        return {'statusCode': 200, 'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"}, 'body': json.dumps('Succesfully created user profile')}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Access-Control-Allow-Headers": "Authorization"},
            'body': json.dumps('Error creating user profile')
        }
