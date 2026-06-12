import boto3
import os
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()

def test_web_search(prompt):
    config = Config(read_timeout=3600)

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1", 
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        config=config
    )
    model_id = "us.amazon.nova-2-lite-v1:0"

    tool_config = {
        "tools": [
            {
                "systemTool": {
                    "name": "nova_grounding"
                }
            }
        ]
    }

    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            toolConfig=tool_config,
            inferenceConfig={"temperature": 0, "maxTokens": 4000}
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    prompt = "I am a Sales rep and need to know about the lead https://www.reinkonline.com/ (Re-Ink). Can you give me a summary of the vertical and payment acceptable modes, 6 key features and pain points for this merchant. Verticals Falls Under the follows 1. Healthcare 2. Restaurants 3. Retail 4. Personal Services 5. Professional Services 6. Non profit 7. Automotive 8. B2B 9. Others. Payment Location can be online, in person or Omni. Method of collecting payment Can be Digital , e commnerce website, Mobile and POS System."
    result = test_web_search(prompt)
    
    if result:
        # 1. Extract Full Text Response and Citations
        full_text_response = ""
        citations_list = set() # Set use kiya hai taaki duplicate URLs na aayein
        
        content_blocks = result.get('output', {}).get('message', {}).get('content', [])
        
        for block in content_blocks:
            # Text extract karne ke liye
            if 'text' in block and block['text']:
                full_text_response += block['text']
            
            # Citations/Sources extract karne ke liye
            if 'citationsContent' in block:
                citations = block['citationsContent'].get('citations', [])
                for citation in citations:
                    web_url = citation.get('location', {}).get('web', {}).get('url')
                    if web_url:
                        citations_list.add(web_url)

        # 2. Printing as per your exact format
        print(f"Query : {prompt}")
        print("*"*60)
        print(f"Response : {result}")
        print("="*60)
        print()
        print()
        print("--"*60)
        print("formatted response :")
        print(full_text_response.strip())
        print()
        print()
        print("--"*60)
        print("Citations :")
        if citations_list:
            for source in citations_list:
                print(f"- {source}")
        else:
            print("No citations found.")
    else:
        print("Failed to get response from API.")