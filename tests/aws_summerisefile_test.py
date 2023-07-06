import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

def summarize_file(bucket_name, file_name):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
        
        response = s3.head_object(Bucket=bucket_name, Key=file_name)

        file_size = response['ContentLength'] / 1024 / 1024  # Size in MB
        print(f'Summary of {bucket_name}/{file_name}:')
        print(f'File Size: {file_size:.2f} MB')

    except NoCredentialsError:
        print('No AWS Credentials were found.')
    except Exception as e:
        print(f'An error occurred: {e}')

# replace 'my_bucket' and 'main.py' with your bucket and file
summarize_file('rondb', 'main.py')
