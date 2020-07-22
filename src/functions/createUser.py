import ast
import boto3
import os
import json
from botocore.exceptions import ClientError


def createUser(event,context,dynamodb=None):
    try:
        if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
        
        etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
        body = ast.literal_eval(event['body'])
        user_id = body['user_id']
        item_type= body['item_type']
        user_type= body['user_type']
        dashboard=body['dashboard']
        item={
                'pk': user_id,
                'sk': user_type,
                'dashboard':dashboard,
                'type': item_type
        }
        if user_type == "shopper":
            user_details=body['user_details']
            history=body['history']
            item.update({'user_details':user_details,'history':history})
        elif user_type == "store_owner":
            store_details=body['store_details']
            messages=body['messages']
            item.update({'store_details':store_details,'messages':messages})
        print(user_id,user_type)
        response = etoken_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(pk) AND attribute_not_exists(sk)'
        )
        print(response)
        return {'statusCode': 200,
                'headers': {"Access-Control-Allow-Origin": "*","Access-Control-Allow-Credentials": True,"Access-Control-Allow-Headers": "Authorization"},'body': json.dumps('Succesfully created user')}
    except ClientError as e:
        print('Closing lambda function')
        print(e.response['Error']['Message'])
        return {
                'statusCode': 400,
                'headers': {"Access-Control-Allow-Origin": "*","Access-Control-Allow-Credentials": True,"Access-Control-Allow-Headers": "Authorization"},
                'body': json.dumps('Error creating user')
        }    


