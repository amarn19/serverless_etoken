import logging
import boto3
import os
import logging
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# dynamodb instance creation
dynamodb = boto3.resource('dynamodb')
# fetching dynamodb table
etoken_table = dynamodb.Table(os.environ['ETOKEN_TABLE'])
# Logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# createUser/createStore
def newItem(item):
    try:
        response = etoken_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(pk) AND attribute_not_exists(sk)'
        )
    except (ClientError, KeyError) as e:
            raise
    return response

# getUser
def fetchUser(user_id, user_type):
    try:
        response = etoken_table.get_item(
                Key={
                    'pk': user_id,
                    'sk': user_type
                })
    except (ClientError, KeyError) as e:
            raise
    return response

# getUsers
def fetchUsers():
    try:
        response = etoken_table.scan(
             FilterExpression=Attr("type").eq("user")
         )
    except (ClientError, KeyError) as e:
            raise
    return response

#removeUser
def removeUser(user_id,user_type):
    try:
        response = etoken_table.delete_item(
            Key={
                'pk': user_id,
                'sk': user_type
            }
        )
    except (ClientError, KeyError) as e:
            raise
    return response

# getStores
def fetchStores(zipcode):
    try:
        response = etoken_table.query(
            KeyConditionExpression=Key('pk').eq(zipcode)
        )
    except (ClientError, KeyError) as e:
            raise
    return response

#updaterecord
def updateItem(pk,sk,item):
    try:
        response = etoken_table.update_item(
            Key={
                'pk': pk,
                'sk': sk
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
    except (ClientError,Exception) as e:
            raise
    return response

def newSlots(zipcode,store_name,slot_date,slot_info):
    print(zipcode,store_name,slot_date,slot_info)
    try:
        response = etoken_table.update_item(
            Key={
                'pk': zipcode,
                'sk': store_name
            },
            UpdateExpression="set slots.#t = :a",
            ExpressionAttributeNames={
                '#t': slot_date
            },
            ExpressionAttributeValues={
                ':a': slot_info
            },
            ReturnValues="UPDATED_NEW"
        )
    except (Exception,ClientError) as e:
        raise
    return response

def registerSlot(zipcode,store_name,slot_date):
    logger.info(slot_date)
    try:
        response = etoken_table.update_item(
            Key={
                'pk': zipcode,
                'sk': store_name
            },
            UpdateExpression="set #s.#d.#t = #s.#d.#t - :a",
            ExpressionAttributeNames={
                '#s': "slots",
                '#d' : slot_date,
                '#t' : "tokens"
            },
            ExpressionAttributeValues={
                ':a': 1
            },
            ReturnValues="UPDATED_NEW"
        )
    except (Exception,ClientError) as e:
            raise
    return response

def checkSlot(zipcode,store_name):
    logger.info(zipcode)
    try:
        response = etoken_table.get_item(
            Key={
                'pk': zipcode,
                'sk': store_name
            },
            AttributesToGet = ["slots"])
    except (ClientError, KeyError) as e:
            raise
    return response