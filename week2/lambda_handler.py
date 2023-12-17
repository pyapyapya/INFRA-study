import os
import json
import urllib.request
from datetime import datetime, timedelta

slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    user = event["Records"][0]["userIdentity"]["principalId"]
    utc_now = datetime.utcnow()
    kst_now = utc_now + timedelta(hours=9)
    kst_now_str = kst_now.strftime('%Y-%m-%d %H:%M:%S')
    slack_data = {
        "channel": "hasan-test",
        "username": "WorksXpert",
        "text": f"*The {key.split('/')[-1]}* file is uploaded!",
        "attachments": [{"color": "#36a64f",
            "text": f"EventTime: {kst_now_str},\n BucketName: {bucket},\nObjectName: {key},\nuser: {user.split(':')[-1]}"}]
    }

    try:
        body = json.dumps(slack_data).encode("utf-8")
        print(body)
        request = urllib.request.Request(slack_webhook_url, data=json.dumps(slack_data).encode("utf-8"))
        with urllib.request.urlopen(request) as response:
            print(response)

    except Exception as e:
        print("error", e)
        raise e