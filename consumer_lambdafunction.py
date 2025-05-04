import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
bucket_name = 'my-kinesis-data-bucket'

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        file_name = f"{uuid.uuid4()}.json"
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=payload)
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and stored in S3.')
    }
