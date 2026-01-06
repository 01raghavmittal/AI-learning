import asyncio
import os
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential




async def main() -> None:
    project_client = AIProjectClient(
       endpoint=os.environ["PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
    
    )
    functions = FunctionTool()
    



    async with await project_client:
        agents_client = project_client.agents.create_agent()

        print(f"agent is created successfully: {agents_client.id}")

        





    


if __name__ == "__main__":
    asyncio.run(main())