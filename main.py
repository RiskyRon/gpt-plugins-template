#main.py
import os
import quart
import mimetypes
from quart import request
import quart_cors
import boto3
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                  region_name=os.getenv("AWS_REGION"))

@app.route("/bucket/<bucketName>", methods=['GET'])
async def read_bucket(bucketName):
    try:
        response = s3.list_objects(Bucket=bucketName)
        return quart.jsonify(response), 200
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400

@app.route("/bucket/<bucketName>/<folderName>", methods=['GET'])
async def read_bucket_folder(bucketName, folderName):
    try:
        response = s3.list_objects(Bucket=bucketName, Prefix=folderName)
        return quart.jsonify(response), 200
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400



@app.route("/bucket/<bucketName>/<folderName>/<fileName>", methods=['GET'])
async def read_bucket_file(bucketName, folderName, fileName):
    try:
        file_key = os.path.join(folderName, fileName)
        response = s3.get_object(Bucket=bucketName, Key=file_key)
        file_content = response['Body'].read()

        # Guess the MIME type based on the file extension
        content_type, _ = mimetypes.guess_type(fileName)
        if content_type is None:
            content_type = 'application/octet-stream'

        return quart.Response(file_content, mimetype=content_type)
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400


@app.route("/bucket/<bucketName>/<folderName>/<fileName>", methods=['POST'])
async def write_bucket_file(bucketName, folderName, fileName):
    try:
        file_key = os.path.join(folderName, fileName)
        data = await request.get_json()
        s3.put_object(Body=str(data), Bucket=bucketName, Key=file_key)
        return quart.jsonify({"message": "File written successfully."}), 200
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400

@app.route("/bucket/<bucketName>/<folderName>/<fileName>", methods=['PUT'])
async def modify_bucket_file(bucketName, folderName, fileName):
    try:
        file_key = os.path.join(folderName, fileName)
        data = await request.get_json()
        s3.put_object(Body=str(data), Bucket=bucketName, Key=file_key)
        return quart.jsonify({"message": "File modified successfully."}), 200
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400

@app.route("/bucket/<bucketName>/<folderName>/<fileName>", methods=['DELETE'])
async def delete_bucket_file(bucketName, folderName, fileName):
    try:
        file_key = os.path.join(folderName, fileName)
        s3.delete_object(Bucket=bucketName, Key=file_key)
        return quart.jsonify({"message": "File deleted successfully."}), 200
    except Exception as e:
        return quart.jsonify({"error": str(e)}), 400


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
