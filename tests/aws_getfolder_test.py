import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

def read_all_files(bucket_name, folder_name):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
        
        # List all files in the folder
        files_in_bucket = s3.list_objects(Bucket=bucket_name, Prefix=folder_name)
        
        if 'Contents' not in files_in_bucket:
            print(f'No files found in {folder_name}.')
            return
        
        for file in files_in_bucket['Contents']:
            file_name = file['Key']

            # Get the file's contents
            response = s3.get_object(Bucket=bucket_name, Key=file_name)

            file_content = response['Body'].read().decode()

            print(f'Contents of {bucket_name}/{file_name}:')
            print(file_content)

    except NoCredentialsError:
        print('No AWS Credentials were found.')
    except Exception as e:
        print(f'An error occurred: {e}')

# replace 'my_bucket' and 'my_folder' with your bucket and folder names
read_all_files('rondb', 'newfoldername')
