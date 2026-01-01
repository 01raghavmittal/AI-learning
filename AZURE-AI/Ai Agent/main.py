import os
import time
import requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

# Load values from .env
endpoint = os.getenv("PROJECT_ENDPOINT")
api_key = os.getenv("PROJECT_APIKEY")
client_id = os.getenv("AZURE_CLIENT_ID")
tenant_id = os.getenv("AZURE_TENANT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")

# -------------------------------
# 1. Test Service Principal Token
# -------------------------------
def test_token():
    print("🔑 Testing Service Principal token...")
    cred = DefaultAzureCredential()
    token = cred.get_token("https://management.azure.com/.default")
    print("✅ Token acquired:", token.token[:30], "...")

# -------------------------------
# 2. Test Agent Creation
# -------------------------------




from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FilePurpose

def test_agent():
    project = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    agent = project.agents.create_agent(
        model="gpt-4o",
        name="my-agent",
        instructions="You are a helpful writing assistant")

    thread = project.agents.threads.create()
    message = project.agents.messages.create(
        thread_id=thread.id, 
        role="user", 
        content="Write me a poem about flowers")

    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project.agents.messages.list(thread_id=thread.id)

    # Get the last message from the sender
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.run_id == run.id and message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")

    # Delete the agent once done
    project.agents.delete_agent(agent.id)
    print("Deleted agent")

# -------------------------------
# 3. Test API Key Authentication
# -------------------------------

import os
import requests
from dotenv import load_dotenv

load_dotenv()
def test_apikey():
        
    endpoint = os.getenv("OPENAI_ENDPOINT")
    print(endpoint)
    api_key = os.getenv("OPENAI_API_KEY")
    print(api_key)
    deployment_id = "gpt-4o-mini"

    url = f"{endpoint}openai/deployments/{deployment_id}/chat/completions?api-version=2024-10-01-preview"

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me something interesting about India."}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        reply = resp.json()["choices"][0]["message"]["content"]
        print("✅ Assistant response:\n", reply)
    else:
        print("❌ API call failed:", resp.status_code, resp.text)




# -------------------------------
# Run all tests
# -------------------------------
if __name__ == "__main__":
    test_token()
    test_agent()
    # test_apikey()

