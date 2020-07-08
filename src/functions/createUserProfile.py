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
        password = body['password']
        item = body['item']
        print(user_id, item, item['key'])
        print(type(item))

        response = etoken_table.update_item(
            Key={
                'pk': user_id,
                'sk': password
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
        return {'statusCode': 200, 'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"}, 'body': json.dumps('Succesfully updated user')}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
            'statusCode': 400,
            'headers': {"Allow-Contol-Allow-Origin": "*", "Allow-Contol-Allow-Credentials": True, "Allow-Contol-Allow-Headers": "Authorization"},
            'body': json.dumps('Error updating user')
        }
