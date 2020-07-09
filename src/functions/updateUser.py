import ast
import boto3
import os
import json
from botocore.exceptions import ClientError


def updateUser(event, context, dynamodb=None):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        password = body['password']
        update_key = body['update']
        user_type = body['user_type']
        item = body['item']
        print(user_id, item,update_key,item[update_key],user_type,item[update_key])
        
        response = etoken_table.get_item(
            Key={
                'pk': user_id,
                'sk': password
            })
        
        db_user_type = response['Item']['user']        
        if user_type == db_user_type:
            key = "shop_details"
        elif user_type == db_user_type:
            key = "user_details"
        print(key,update_key)
        response = etoken_table.update_item(
            Key={
                'pk': user_id,
                'sk': password
            },
            UpdateExpression="set #t.#s = :a",
            ExpressionAttributeNames={
                '#t': "shop_details",
                '#s': update_key
            },
            ExpressionAttributeValues={
                ':a': item[update_key]
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
