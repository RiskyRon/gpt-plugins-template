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

def rmdir(bucket, folder):
    # Ensure the folder name ends with '/'
    if not folder.endswith('/'):
        folder += '/'

    # List all objects within the folder
    response = s3.list_objects_v2(Bucket=bucket, Prefix=folder)

    # If there are any objects in the folder, delete them
    if 'Contents' in response:
        delete_dict = {'Objects': []}
        for obj in response['Contents']:
            delete_dict['Objects'].append({'Key': obj['Key']})

        s3.delete_objects(Bucket=bucket, Delete=delete_dict)

try:
    # Replace 'rondb' and 'newfoldername' with your actual bucket name and folder name
    rmdir('rondb', 'awstest')
    print("Folder deleted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
