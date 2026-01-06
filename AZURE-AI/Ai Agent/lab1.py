"""
Lab1 Script - Azure AI Agent Hands-on

This script demonstrates the basic workflow of creating and interacting with 
an Azure AI Agent using the Azure AI Projects SDK.

Steps performed:
1. Load environment variables (PROJECT_ENDPOINT).
2. Create an AI Project client with Azure credentials.
3. Create a new agent (using gpt-4o model).
4. Start a conversation thread and send a user query.
5. Run the agent to process the query and wait for the response.
6. Print out the agent’s reply messages.
7. Delete the agent after completion.

Purpose:
- Serves as a hands-on practice script for learning Azure AI Agents.
- Acts as a simple starting point (Lab1) for experimenting with agent creation, 
  messaging, and cleanup.
"""





#---------------------------------------------------------------------------------------

import os, time

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FilePurpose


from dotenv import load_dotenv
load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = "gpt-4o"
user_query=input("Please enter your Query")


# Step 1 : creating project client
project_client=AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential())


# 
with project_client:
    
    #
    agent_client=project_client.agents.create_agent(
        name="Lab1 Agent",
        model=model_name,
        instructions=""   #system prompt
    )

    print(f"Created agent, agent_id {agent_client.id}")




    thread = project_client.agents.threads.create()
    print(f"Created thread, thread_id{thread.id}")

    # message that has been to agent 
    message = project_client.agents.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=user_query)
    
    print(f"Created message, Message id{message.id}")

    # run to agent : basically a run to the agent is just about sending message to user query  to the agent
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_client.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        while run.status in ["Queued", "In- progress","Require_action"]:
            time.sleep(1)
            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_client.id)
            print(f"Run Status:{run.status}")
    
    print(f"Final Run Status: {run.status}")
    
    responses =  project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    # debug
    print(responses)

    print('*'*100)
    print()
    print()
    print()
    for response in responses:
        if response.run_id == run.id and response.text_messages:
            print(f"{response.role}: {response.text_messages[-1].text.value}")



    # Delete the agent once done
    project_client.agents.delete_agent(agent_client.id)
    print("Deleted agent")