import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

def create_file(bucket_name, file_name, folder_name=None):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
        
        if folder_name:
            file_name = folder_name + '/' + file_name
            
        # Here we are creating an empty file. If you want to put some data in the file,
        # replace '' with your data.
        s3.put_object(Body='', Bucket=bucket_name, Key=file_name)
        
        print(f'File {file_name} created successfully in bucket {bucket_name}.')

    except NoCredentialsError:
        print('No AWS Credentials were found.')
    except Exception as e:
        print(f'An error occurred: {e}')

# usage examples:
create_file('my_bucket', 'my_file.txt') # to create a file in the root of the bucket
create_file('my_bucket', 'my_file.txt', 'my_folder') # to create a file in a specific folder
