import json
import boto3
    
def loginUser(event,context,dynamodb=None):
        try:
            if not dynamodb:
                dynamodb = boto3.resource('dynamodb')
            etoken_table = dynamodb.Table('etoken_table')
            user_id = event ['user_id']
            password = event ['password']
            print(user_id)
            resp = etoken_table.get_item(
                Key={
                'pk': user_id,
                'sk': password
            }
            )
    
            print('lambda function')
            if ("Item" in resp):
                return {
                    'statusCode': 200,
                    'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                    'body': json.dumps('Incorrect login credentials.Try again')
            }
            else:
                return {
                    'statusCode': 200,
                    'headers': {"Allow-Contol-Allow-Origin": "*","Allow-Contol-Allow-Credentials": True,"Allow-Contol-Allow-Headers": "Authorization"},
                    'body': json.dumps('Incorrect login credentials.Try again')
            }
        except:
            print('Closing lambda function')
            return {
                    'statusCode': 400,
                    'body': json.dumps('Login failed.Try again')
            }