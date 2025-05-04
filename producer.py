import boto3
import json
import time
import random

# Kinesis client setup
kinesis = boto3.client('kinesis', region_name='us-east-1')  # Change if your region is different

# Stream name
stream_name = 'user-activity-stream'

# Sample events
events = ['login', 'logout']

# Function to generate dummy user event
def generate_user_event():
    return {
        'user_id': f"user_{random.randint(1, 5)}",
        'event': random.choice(events),
        'timestamp': int(time.time())
    }

# Infinite loop to send events
while True:
    event = generate_user_event()
    print("Sending:", event)
    kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(event),
        PartitionKey=event['user_id']
    )
    time.sleep(2)
