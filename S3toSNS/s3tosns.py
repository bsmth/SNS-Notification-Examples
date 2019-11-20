import csv
import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Get name of the S3 bucket & retrieve the latest-written object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_file = obj['Body'].read().decode("utf-8").split('\n')
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Example to compose an SNS message based on three fields we're interested in.
            sns_message ='{ "description": "%s","endpoint_name": "%s", "endpoint_id": "%s"}'  % (row['event_type_description'], row['endpoint_name'], row['endpoint_id'])
            sns_subject = "%s Notification" %(row["event_type_description"])
            
            # It might be nice to use event severity description to route important messages
            if "suspension" in row['event_type_description']:
                sns_topic='arn:aws:sns:....slack-notifications-topic'
                

            if "activation" in row['event_type_description']:
                sns_topic='arn:aws:sns:....email-notifications-topic'
            
            sns_response = sns.publish(
                TopicArn=sns_topic,
                Message=sns_message,
                Subject=sns_subject
            )
            

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

