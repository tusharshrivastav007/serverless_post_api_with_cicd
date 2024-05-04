import json
import logging
import time
import boto3
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Customer')

def lambda_handler(event, context):
    print("Event:", event)
    
    # Extract customerId from the event body (multipart form-data)
    if 'body' in event:
        body = event['body']
        match = re.search(r'name="customerId"\r\n\r\n(\d+)', body)
        if match:
            customer_id = match.group(1)
        else:
            logging.error("CustomerId not found in form-data")
            return {
                'statusCode': 400,
                'body': json.dumps("Error: CustomerId not found in form-data")
            }
    else:
        logging.error("Request body is missing")
        return {
            'statusCode': 400,
            'body': json.dumps("Error: Request body is missing")
        }

    try:
        # Convert customerId to string
        customer_id = str(customer_id)

        # Put the item into the DynamoDB table
        table.put_item(Item={'customerId': customer_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda data added successfully!')
        }
    except Exception as e:
        logging.error(f"Error inserting data into DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error inserting data into DynamoDB: {str(e)}")
        }
