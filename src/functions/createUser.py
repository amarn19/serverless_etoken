import json
import boto3


def createUser(event,context,dynamodb=None):
    try:
        if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
        etoken_table = dynamodb.Table('etoken_table')
        user_id = event ['user_id']
        password = event ['password']
        type = event ['type']
        print(user_id+type)
        response = etoken_table.put_item(
            Item={
                'pk': user_id,
                'sk': password,
                'type': type
            },
            ConditionExpression='attribute_not_exists(pk) AND attribute_not_exists(sk)'
        )
        print(response)
        return {'statusCode': 200,'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},'body': json.dumps('Succesfully created user')}
    except:
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'body': json.dumps('Error creating user')
        }    


