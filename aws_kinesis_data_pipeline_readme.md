
# AWS Kinesis Data Pipeline: Real-Time User Activity Tracking

## Project Overview
This project demonstrates a real-time data streaming pipeline using AWS services. It captures user activity data, processes it, and stores it for further analysis.

## Architecture

```
Producer (Python) → Amazon Kinesis Data Stream → AWS Lambda (Consumer) → Amazon S3
```

- **Producer**: A Python script that simulates user activity and sends data to the Kinesis Data Stream.
- **Kinesis Data Stream**: Captures and buffers streaming data in real-time.
- **AWS Lambda (Consumer)**: Processes incoming records from the Kinesis stream and writes them to Amazon S3.
- **Amazon S3**: Stores the processed data for further analysis.

## Prerequisites
- AWS Account with necessary permissions for Kinesis, Lambda, and S3.
- Python 3.x installed on your local machine.
- AWS CLI configured with your credentials.

## Project Structure
```
aws-kinesis-data-pipeline/
├── producer.py
├── lambda_function.py
├── requirements.txt
├── README.md
├── .gitignore
└── architecture_diagram.png
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/aws-kinesis-data-pipeline.git
cd aws-kinesis-data-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS CLI
Ensure your AWS CLI is configured:
```bash
aws configure
```

### 4. Create AWS Resources
1. **Amazon Kinesis Data Stream**: Create a stream named `user-activity-stream`.
2. **Amazon S3 Bucket**: Create a bucket named `user-activity-logs-sabari`.
3. **AWS Lambda Function**:
   - Create a Lambda function named `ProcessUserActivity`.
   - Set the runtime to Python 3.x.
   - Attach the necessary IAM role with permissions for Kinesis and S3.
   - Upload the `lambda_function.py` code.
   - Set the Kinesis stream as the trigger.

## Usage

### Run the Producer Script
```bash
python producer.py
```
This script simulates user activity and sends records to the Kinesis Data Stream.

### Monitor the Pipeline
- **AWS Lambda Console**: Check the invocation metrics and logs.
- **Amazon S3 Console**: Verify that the processed data is being stored in the `user-activity-logs-sabari` bucket.

## Code Explanation

### `producer.py`
```python
import boto3
import json
import time
import random

kinesis = boto3.client('kinesis', region_name='us-east-1')

def get_user_activity():
    user_ids = ['user_1', 'user_2', 'user_3', 'user_4']
    events = ['login', 'logout', 'purchase', 'click']
    return {
        'user_id': random.choice(user_ids),
        'event': random.choice(events),
        'timestamp': int(time.time())
    }

while True:
    data = get_user_activity()
    print(f"Sending: {data}")
    kinesis.put_record(
        StreamName='user-activity-stream',
        Data=json.dumps(data),
        PartitionKey=data['user_id']
    )
    time.sleep(1)
```
This script generates random user activity events and sends them to the Kinesis Data Stream every second.

### `lambda_function.py`
```python
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        user_id = data['user_id']
        timestamp = data['timestamp']
        filename = f"{user_id}_{timestamp}.json"
        s3.put_object(
            Bucket='user-activity-logs-sabari',
            Key=filename,
            Body=json.dumps(data)
        )
```
This Lambda function processes each record from the Kinesis stream, decodes the data, and stores it as a JSON file in the specified S3 bucket.

## Screenshots
Include relevant screenshots here, such as:
- AWS Kinesis Data Stream overview.
- AWS Lambda function configuration.
- Amazon S3 bucket with stored JSON files.

## Troubleshooting

- **AccessDeniedException**: Ensure that your IAM roles have the necessary permissions for Kinesis, Lambda, and S3 operations.
- **Data Not Appearing in S3**: Check the CloudWatch logs for your Lambda function to identify any errors during execution.
