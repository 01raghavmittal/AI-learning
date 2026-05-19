import boto3
import time
import json
from datetime import datetime
from botocore.exceptions import ClientError

def test_all_nova_models():
    """Test all Nova models with the same query to compare accuracy and response time"""
    
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    # Test query
    test_query = "Explain quantum computing in simple terms with 3 key benefits."
    
    # All text-capable Nova models to test
    models_to_test = {
        # Nova 2 Models (Latest)
        "Nova 2 Lite (Regional)": "amazon.nova-2-lite-v1:0",
        "Nova 2 Lite (US CRIS)": "us.amazon.nova-2-lite-v1:0",
        "Nova 2 Lite (Global)": "global.amazon.nova-2-lite-v1:0",
        
        # Nova 1 Models
        "Nova Micro (Regional)": "amazon.nova-micro-v1:0",
        "Nova Micro (US CRIS)": "us.amazon.nova-micro-v1:0",
        "Nova Lite (Regional)": "amazon.nova-lite-v1:0",
        "Nova Lite (US CRIS)": "us.amazon.nova-lite-v1:0",
        "Nova Pro (Regional)": "amazon.nova-pro-v1:0",
        "Nova Pro (US CRIS)": "us.amazon.nova-pro-v1:0",
        "Nova Premier (Regional)": "amazon.nova-premier-v1:0",
        "Nova Premier (US CRIS)": "us.amazon.nova-premier-v1:0",
    }
    
    results = []
    
    print(f"🧪 Testing {len(models_to_test)} Nova models...")
    print(f"📝 Query: {test_query}")
    print("=" * 80)
    
    for model_name, model_id in models_to_test.items():
        print(f"\n🔄 Testing: {model_name}")
        print(f"   Model ID: {model_id}")
        
        try:
            # Record start time
            start_time = time.time()
            
            # Make the API call
            response = client.converse(
                modelId=model_id,
                messages=[{
                    "role": "user",
                    "content": [{"text": test_query}]
                }],
                inferenceConfig={
                    "maxTokens": 500,
                    "temperature": 0.7
                }
            )
            
            # Record end time
            end_time = time.time()
            response_time = end_time - start_time
            
            # Extract response
            response_text = response["output"]["message"]["content"][0]["text"]
            
            # Count tokens (approximate)
            input_tokens = len(test_query.split()) * 1.3  # Rough estimate
            output_tokens = len(response_text.split()) * 1.3  # Rough estimate
            
            # Store results
            result = {
                "model_name": model_name,
                "model_id": model_id,
                "response_time": round(response_time, 2),
                "input_tokens": int(input_tokens),
                "output_tokens": int(output_tokens),
                "response_text": response_text,
                "status": "✅ Success"
            }
            
            results.append(result)
            
            print(f"   ✅ Success - Response time: {response_time:.2f}s")
            print(f"   📊 Tokens: ~{int(input_tokens)} in, ~{int(output_tokens)} out")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            result = {
                "model_name": model_name,
                "model_id": model_id,
                "response_time": None,
                "input_tokens": None,
                "output_tokens": None,
                "response_text": None,
                "status": f"❌ Error: {error_code}",
                "error_message": error_message
            }
            
            results.append(result)
            print(f"   ❌ Error: {error_code} - {error_message}")
            
        except Exception as e:
            result = {
                "model_name": model_name,
                "model_id": model_id,
                "response_time": None,
                "input_tokens": None,
                "output_tokens": None,
                "response_text": None,
                "status": f"❌ Error: {str(e)}"
            }
            
            results.append(result)
            print(f"   ❌ Unexpected error: {str(e)}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY RESULTS")
    print("=" * 80)
    
    successful_results = [r for r in results if r["status"] == "✅ Success"]
    
    if successful_results:
        # Sort by response time
        successful_results.sort(key=lambda x: x["response_time"])
        
        print(f"\n🏆 FASTEST MODELS (by response time):")
        for i, result in enumerate(successful_results[:5], 1):
            print(f"{i}. {result['model_name']}: {result['response_time']}s")
        
        print(f"\n📝 DETAILED RESPONSES:")
        for result in successful_results:
            print(f"\n--- {result['model_name']} ---")
            print(f"Response time: {result['response_time']}s")
            print(f"Tokens: ~{result['input_tokens']} in, ~{result['output_tokens']} out")
            print(f"Response: {result['response_text'][:200]}...")
    
    # Print failed models
    failed_results = [r for r in results if r["status"] != "✅ Success"]
    if failed_results:
        print(f"\n❌ FAILED MODELS:")
        for result in failed_results:
            print(f"- {result['model_name']}: {result['status']}")
    
    return results

def test_with_web_grounding():
    """Test models that support web grounding"""
    
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    # Models that support web grounding
    grounding_models = {
        "Nova 2 Lite (US CRIS)": "us.amazon.nova-2-lite-v1:0",
        "Nova Premier (US CRIS)": "us.amazon.nova-premier-v1:0",  # May be legacy
    }
    
    # Query that benefits from web grounding
    grounding_query = "I am a Sales rep and need to know about the lead https://norcalorthosurgery.com/ (NORCAL ORTHOPEDICS SURGERY CENTER). Can you give me a summary of the vertical and payment acceptable modes, 6 key features and pain points for this merchant. Verticals Falls Under the follows 1. Healthcare 2. Restaurants 3. Retail 4. Personal Services 5. Professional Services 6. Non profit 7. Automotive 8. B2B 9. Others. Payment Location can be online, in person or Omni. Method of collecting payment Can be Digital , e commnerce website, Mobile and POS System."
    
    tool_config = {
        "tools": [
            {
                "systemTool": {
                    "name": "nova_grounding"
                }
            }
        ]
    }
    
    print(f"\n🌐 Testing Web Grounding Capabilities")
    print(f"📝 Query: {grounding_query}")
    print("=" * 80)
    
    for model_name, model_id in grounding_models.items():
        print(f"\n🔄 Testing: {model_name} with Web Grounding")
        
        try:
            start_time = time.time()
            
            response = client.converse(
                modelId=model_id,
                messages=[{
                    "role": "user",
                    "content": [{"text": grounding_query}]
                }],
                toolConfig=tool_config,
                inferenceConfig={
                    "maxTokens": 1000,
                    "temperature": 0
                }
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"   ✅ Success - Response time: {response_time:.2f}s")
            
            # Extract response and citations
            output = response["output"]["message"]["content"]
            for content in output:
                if "text" in content:
                    print(f"   📝 Response: {content['text'][:200]}...")
                elif "citation" in content:
                    url = content["citation"]["location"]["web"]["url"]
                    print(f"   📎 Source: {url}")
                    
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    # Test all models
    results = test_all_nova_models()
    
    # Test web grounding
    test_with_web_grounding()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nova_model_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
 