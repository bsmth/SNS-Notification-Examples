import csv
import json
import urllib.parse
import boto3

from botocore.exceptions import ClientError

SENDER = "EMnify Event Notifications <b.smith@emnify.com>"
RECIPIENT = "brian.smith@emnify.com"
AWS_REGION = "eu-west-1"

email_client = boto3.client('ses',region_name=AWS_REGION)

def compose_template(description, endpoint_name, endpoint_id):
    # Provide a HTML templte in this directory
    with open('template.html', mode='r') as html_template:
        template=html_template.read()
        # Add some strings in the form '{{replace-me}}' in the template
        # This syntax is also compatible with handlebars (used by SES templates)
        composed_template = template.replace('{{event_description}}', description).replace('{{endpoint_name}}', endpoint_name).replace('{{endpoint_id}}', endpoint_id)
        return composed_template

def send_mail_notification(description, endpoint_name, endpoint_id):
    SUBJECT = description
    BODY_TEXT = description
    html_body = compose_template(description, endpoint_name, endpoint_id)           

    CHARSET = "UTF-8"

    try:
        # When providing an SES template, see SES.Client.send_templated_email()
        response = email_client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': html_body,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
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