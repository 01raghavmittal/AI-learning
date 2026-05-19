import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# 1. .env file se credentials load karein
load_dotenv()

def get_nova_response(prompt):
    try:
        # 2. Bedrock Runtime Client banayein
        # Yeh automatic .env se keys utha lega
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN") # Temporary credentials ke liye zaroori hai
        )

        model_id = "amazon.nova-lite-v1:0"

        # 3. Model ko message bhejein (Converse API)
        response = client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.7
            },
            
        )

        # 4. Response extract karein
        return response["output"]["message"]["content"][0]["text"]

    except ClientError as e:
        return f"AWS Error: {e}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    p = "Write a short poem about coding in Hindi."
    print("Nova Lite is thinking...")
    result = get_nova_response(p)
    print("\nResponse from Nova Lite:")
    print(result)