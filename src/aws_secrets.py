# src/aws_secrets.py 
import boto3
from botocore.exceptions import ClientError
import json

class AWSSecretsManager:
    def __init__(self, region_name="us-east-1"):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    
    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            print(f"Error: {e}")
            return None
