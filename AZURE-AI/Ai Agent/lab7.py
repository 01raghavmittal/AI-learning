
"""
Simple Code Interpreter Agent: Upload CSV, Run, Save Generated Images (SDK without download_to_path)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool, MessageAttachment, FilePurpose

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

with project_client:

    # 1) Upload CSV for Code Interpreter (via Agents subclient)
    file = project_client.agents.files.upload_and_poll(
        file_path="electronics_products.csv",
        purpose=FilePurpose.AGENTS
    )
    print("Uploaded file:", file.id)

    # 2) Create Code Interpreter tool
    ci_tool = CodeInterpreterTool(file_ids=[file.id])

    # 3) Create Agent
    agent = project_client.agents.create_agent(
        name="simple-ci-agent",
        model="gpt-4o",
        instructions="You are a helpful data analysis agent.",
        tools=ci_tool.definitions,
        tool_resources=ci_tool.resources,
    )
    print("Agent:", agent.id)

    # 4) Create Thread
    thread = project_client.agents.threads.create()
    print("Thread:", thread.id)

    # 5) User query
    # user_query = input("Enter query: ")

    # 6) Send message with file attachment
    attachment = MessageAttachment(file_id=file.id, tools=ci_tool.definitions)
    project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Could you please create a column chart with products on the x-axis and their respective prices on the y-axis?",
        attachments=[attachment],
    )

    # 7) Run the agent
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    print("Run completed:", run.status)

    # 8) Save generated images (uses agents.download_file)
# 8) Save generated images
    out_dir = Path("output_images")
    out_dir.mkdir(exist_ok=True)

    messages = project_client.agents.messages.list(thread_id=thread.id)
    
    # ItemPaged objects are directly iterable
    for msg in messages:
        # Check if content exists and handle both object and dict access
        content_blocks = getattr(msg, 'content', [])
        
        for block in content_blocks:
            # Handle the block based on whether it's an object or a dict
            block_type = getattr(block, 'type', block.get('type') if isinstance(block, dict) else None)
            
            if block_type == "image_file":
                # Extract file_id
                if isinstance(block, dict):
                    file_id = block["image_file"]["file_id"]
                else:
                    file_id = block.image_file.file_id
                
                local_path = out_dir / f"{file_id}.png"
                print(f"Downloading image {file_id}...")
                
                # Retrieve and save content
                file_content = project_client.agents.files._get_file_content(file_id=file_id)
                
                with open(local_path, "wb") as f:
                    for chunk in file_content:
                        f.write(chunk)

                print(f"Saved image: {local_path.resolve()}")

    # 9) Cleanup
    project_client.agents.delete_agent(agent.id)
    print("Agent deleted.")

