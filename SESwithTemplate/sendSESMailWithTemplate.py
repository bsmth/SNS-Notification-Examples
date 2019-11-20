import csv
import json
import urllib.parse
import boto3

from botocore.exceptions import ClientError

SENDER = "EMnify Event Notifications <b.smith@emnify.com>"
RECIPIENT = "brian.smith@emnify.com"
AWS_REGION = "eu-west-1"

email_client = boto3.client('ses',region_name=AWS_REGION)

def send_mail_notification(description, endpoint_name, endpoint_id):
    try:
        response = email_client.send_templated_email(
            Template="NotificationTemplate",
            TemplateData="{ \"event_description\":\"%s\", \"endpoint_name\": \"%s\", \"endpoint_id\": \"%s\"}" %(description, endpoint_name, endpoint_id),
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Source=SENDER
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    print("From SNS %s" %(sns_message));

    send_mail_notification(sns_message['description'], sns_message['endpoint_name'], sns_message['endpoint_id'])