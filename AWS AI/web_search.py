import boto3
import os
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()

def chat_with_nova_grounding(prompt):
    # Extended timeout configuration for web grounding requests
    config = Config(read_timeout=3600)
    
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",  # Nova 2 grounding support
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),  # Only if using temporary credentials
        config=config
    )

    # Use Nova 2 Lite with cross-region inference profile for grounding
    model_id = "us.amazon.nova-2-lite-v1:0"  # Updated to Nova 2 Lite

    # Correct Grounding Tool Configuration
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

        # Extract response
        output = response["output"]["message"]["content"]
        
        print("Nova 2 Lite Response with Grounding:")
        print("-" * 50)
        print(output)

        for content in output:
            if "text" in content:
                print(content["text"])
            elif "citation" in content:
                # Handle citations
                citation = content["citation"]
                if "location" in citation and "web" in citation["location"]:
                    url = citation["location"]["web"]["url"]
                    domain = citation["location"]["web"].get("domain", "")
                    print(f"\n📎 Source: {url}")
                    if domain:
                        print(f"   Domain: {domain}")

        # Check for additional citation metadata
        if "citations" in response.get("output", {}).get("message", {}):
            print("\n" + "="*50)
            print("📚 All Sources Used:")
            print("="*50)
            for i, citation in enumerate(response["output"]["message"]["citations"], 1):
                if "location" in citation and "web" in citation["location"]:
                    url = citation["location"]["web"]["url"]
                    domain = citation["location"]["web"].get("domain", "")
                    print(f"{i}. {url}")
                    if domain:
                        print(f"   Domain: {domain}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have access to Nova 2 Lite model")
        print("2. Verify your IAM permissions include bedrock:InvokeTool")
        print("3. Check if you're in a supported region (US regions only)")

def chat_with_nova_grounding_streaming(prompt):
    """Streaming version with real-time citations"""
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
        # Use converse_stream for streaming
        response = client.converse_stream(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            toolConfig=tool_config,
            inferenceConfig={"temperature": 0, "maxTokens": 4000}
        )

        print("Nova 2 Lite Streaming Response with Grounding:")
        print("-" * 50)
        
        # Process streaming response
        for event in response["stream"]:
            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"]["delta"]
                
                if "text" in delta:
                    print(delta["text"], end="", flush=True)
                if "citation" in delta:
                    # Real-time citation display
                    url = delta["citation"]["location"]["web"]["url"]
                    print(f" [📎 {url}]", end="", flush=True)
            
            elif "messageStop" in event:
                print("\n\n" + "="*50)
                print("✅ Response Complete")
                print("="*50)

    except Exception as e:
        print(f"Error: {e}")

def test_basic_nova_2_lite():
    """Test basic Nova 2 Lite without grounding first"""
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

    model_id = "us.amazon.nova-2-lite-v1:0"

    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "Hello! Can you tell me what you are?"}]}],
            inferenceConfig={"temperature": 0.7, "maxTokens": 200}
        )

        output = response["output"]["message"]["content"][0]["text"]
        print("✅ Basic Nova 2 Lite Test Successful!")
        print(f"Response: {output}")
        return True

    except Exception as e:
        print(f"❌ Basic Nova 2 Lite Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Nova 2 Lite Basic Functionality...")
    print("="*60)
    
    # First test basic functionality
    if test_basic_nova_2_lite():
        print("\n" + "="*60)
        print("🌐 Testing Nova 2 Lite with Web Grounding...")
        print("="*60)
        
        # Test queries for grounding
        queries = [
            "What are the latest developments in AI technology in 2024?",
            "What is the current weather in New York City?",
            "Latest news about renewable energy developments",
            "Current stock market trends today"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\n{'='*60}")
            print(f"Query {i}: {query}")
            print('='*60)
            
            # Try non-streaming first
            chat_with_nova_grounding(query)
            
            # Uncomment below to test streaming version
            # print(f"\n{'-'*30} STREAMING VERSION {'-'*30}")
            # chat_with_nova_grounding_streaming(query)
            
            if i < len(queries):
                print("\n" + "⏳ Waiting before next query...")
                import time
                time.sleep(2)  # Brief pause between requests
    else:
        print("\n❌ Basic test failed. Please check your credentials and model access.")
        print("\nTo request access to Nova 2 Lite:")
        print("1. Go to Amazon Bedrock Console")
        print("2. Navigate to 'Model access'")
        print("3. Request access to 'Amazon Nova 2 Lite'")

 