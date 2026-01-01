
import os
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool
from dotenv import load_dotenv
load_dotenv() 


# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential(),  
    # Use Azure Default Credential for authentication
)

with project_client:

    code_interpreter = CodeInterpreterTool()

    agent = project_client.agents.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="""You politely help with math questions. 
        Use the Code Interpreter tool when asked to visualize numbers.""",  
        # Instructions for the agent
        tools=code_interpreter.definitions,  # Attach the tool
        tool_resources=code_interpreter.resources,  # Attach tool resources
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    question = """Draw a graph for a line with a slope of 4 
    and y-intercept of 9 and provide the file to me?"""

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",  # Role of the message sender
        content=question,  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process an agent run
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
        additional_instructions="""Please address the user as Jane Doe.
        The user has a premium account.""",
    )

    print(f"Run finished with status: {run.status}")

    # Check if the run failed
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages
    messages = project_client.agents.messages.list(thread_id=thread.id)
    print(f"Messages: {messages}")

    for message in messages:
        print(f"Role: {message.role}, Content: {message.content}")
        for this_content in message.content:
            print(f"Content Type: {this_content.type}, Content Data: {this_content}")
            if this_content.text.annotations:
                for annotation in this_content.text.annotations:
                    print(f"Annotation Type: {annotation.type}, Text: {annotation.text}")
                    print(f"Start Index: {annotation.start_index}")
                    print(f"End Index: {annotation.end_index}")
                    print(f"File ID: {annotation.file_path.file_id}")
                    # Save every image file in the message
                    file_id = annotation.file_path.file_id
                    file_name = f"{file_id}_image_file.png"
                    project_client.agents.files.save(file_id=file_id, file_name=file_name)
                    print(f"Saved image file to: {Path.cwd() / file_name}")
    #Uncomment these lines to delete the agent when done
    #project_client.agents.delete_agent(agent.id)
    #print("Deleted agent")