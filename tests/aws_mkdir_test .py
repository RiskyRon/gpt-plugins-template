import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

try:
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)
    print('AWS S3 Client initiated successfully.')
except NoCredentialsError:
    print('No AWS Credentials were found.')

# Define the function to create a new 'folder' in an S3 bucket
def mkdir(bucket, folder):
    s3.put_object(Bucket=bucket, Key=(folder+'/'))

# Then use the function to create a folder
try:
    # Replace 'rondb' and 'newfoldername' with your actual bucket name and folder name
    mkdir('rondb', 'newfoldername')
    print("Folder created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
