from io import BytesIO
import requests
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    if 'create' in event.keys():
        url = f'http://blog-service-dev.techwithlyle.xyz/image?filename={event["create"]}'
    
        r = requests.get(url)
        if r.ok:
            
            im = BytesIO(r.content)
            
            try:
                s3.upload_fileobj(
                    im,
                    'flask-image-service',
                    event["create"],
                    ExtraArgs={"ACL": "public-read"},
                )
                url = f'http://blog-service-dev.techwithlyle.xyz/delete?filename={event["create"]}'
                r = requests.get(url)
                if not r.ok:
                    return {
                        'statusCode': r.status_code,
                        'message': r.json()
                    }
            except ClientError as e:        
                return {
                    'statusCode': 400,
                    'res': str(e)
                }
            return {
                    'statusCode': 200,
                    'res': 'uploaded'
                }
        return {
                    'statusCode': r.status_code,
                    'res': 'Not uploaded'
                }
    else:
        s3.delete_object(Bucket='flask-image-service', Key=event["delete"])
        return {
            'statusCode': 200,
            'res': 'deleted'
        }