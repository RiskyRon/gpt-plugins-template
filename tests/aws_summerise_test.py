import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

def summarize_folder(bucket_name, folder_name):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
        
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        
        if 'Contents' not in response:
            print(f'No objects found in {bucket_name}/{folder_name}')
            return

        total_size = sum(obj['Size'] for obj in response['Contents']) / 1024 / 1024  # Size in MB
        total_files = len(response['Contents'])
        
        print(f'Summary of {bucket_name}/{folder_name}:')
        print(f'Total Files: {total_files}')
        print(f'Total Size: {total_size:.2f} MB')

    except NoCredentialsError:
        print('No AWS Credentials were found.')
    except Exception as e:
        print(f'An error occurred: {e}')

# replace 'my_bucket' and 'my_folder' with your bucket and folder
summarize_folder('rondb', 'newfoldername')
