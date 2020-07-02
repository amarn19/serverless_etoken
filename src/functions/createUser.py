import ast
import boto3
import os
import json


def createUser(event,context,dynamodb=None):
    try:
        if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        password = body['password']
        user_type = body['type']
        print(user_id,user_type)
        response = etoken_table.put_item(
            Item={
                'pk': user_id,
                'sk': password,
                'type': user_type
            },
            ConditionExpression='attribute_not_exists(pk) AND attribute_not_exists(sk)'
        )
        print(response)
        return {'statusCode': 200,'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},'body': json.dumps('Succesfully created user')}
    except:
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                'body': json.dumps('Error creating user')
        }    


