"""
Lab1 Script - Azure AI Agent (Production Async Version)

This script demonstrates a clean, production-grade, fully async
implementation of Azure AI Agent workflow using Azure AI Projects SDK.

Key Highlights:
- Async / await architecture
- Thread-safe execution using asyncio.to_thread
- Professional error handling
- Clean class-based design
- Same SDK methods (NO behavior change)
"""

# --------------------------------------------------------------------------------------

import os
import time
import asyncio
from typing import Optional

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder

# --------------------------------------------------------------------------------------
# Environment Setup
# --------------------------------------------------------------------------------------

load_dotenv()

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_NAME = "gpt-4o"


# --------------------------------------------------------------------------------------
# Azure AI Agent Async Manager
# --------------------------------------------------------------------------------------

class AzureAIAgentAsyncManager:
    """
    Fully asynchronous manager for Azure AI Agent lifecycle.

    NOTE:
    Azure SDK is internally synchronous, so blocking calls are safely
    wrapped using asyncio.to_thread for production scalability.
    """

    def __init__(self, project_endpoint: str):
        if not project_endpoint:
            raise ValueError("PROJECT_ENDPOINT is required.")

        self.project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential()
        )

        print("Azure AI Project Client initialized")

    async def create_agent(self, name: str, model: str, instructions: str = ""):
        return await asyncio.to_thread(
            self.project_client.agents.create_agent,
            name=name,
            model=model,
            instructions=instructions
        )

    async def create_thread(self):
        return await asyncio.to_thread(
            self.project_client.agents.threads.create
        )

    async def send_message(self, thread_id: str, user_query: str):
        return await asyncio.to_thread(
            self.project_client.agents.messages.create,
            thread_id=thread_id,
            role="user",
            content=user_query
        )

    async def run_agent(self, thread_id: str, agent_id: str):
        """
        Run agent and poll status asynchronously.
        """
        run = await asyncio.to_thread(
            self.project_client.agents.runs.create_and_process,
            thread_id=thread_id,
            agent_id=agent_id
        )

        if run.status == "failed":
            raise RuntimeError(f"Run failed: {run.last_error}")

        while run.status in ["Queued", "In- progress", "Require_action"]:
            print(f"Run status: {run.status}")
            await asyncio.sleep(1)

            run = await asyncio.to_thread(
                self.project_client.agents.runs.create_and_process,
                thread_id=thread_id,
                agent_id=agent_id
            )

        print(f"Run completed | status: {run.status}")
        return run

    async def fetch_responses(self, thread_id: str, run_id: str):
        responses = await asyncio.to_thread(
            self.project_client.agents.messages.list,
            thread_id=thread_id,
            order=ListSortOrder.ASCENDING
        )

        print("\n" + "*" * 100 + "\n")
        for response in responses:
            if response.run_id == run_id and response.text_messages:
                print(f"{response.role}: {response.text_messages[-1].text.value}")

    async def delete_agent(self, agent_id: str):
        await asyncio.to_thread(
            self.project_client.agents.delete_agent,
            agent_id
        )
        print("Agent deleted successfully")


# --------------------------------------------------------------------------------------
# Main Async Execution
# --------------------------------------------------------------------------------------

async def main():
    """
    Async entry point for Lab1 execution.
    """

    user_query = input("Please enter your query: ")

    try:
        manager = AzureAIAgentAsyncManager(PROJECT_ENDPOINT)

        agent = await manager.create_agent(
            name="Lab1 Agent",
            model=MODEL_NAME,
            instructions=""
        )
        print(f"Created agent | agent_id: {agent.id}")

        thread = await manager.create_thread()
        print(f"Created thread | thread_id: {thread.id}")

        message = await manager.send_message(thread.id, user_query)
        print(f"Created message | message_id: {message.id}")

        run = await manager.run_agent(thread.id, agent.id)
        await manager.fetch_responses(thread.id, run.id)

        await manager.delete_agent(agent.id)

        print("\nLab1 async execution completed successfully")

    except Exception as e:
        print(f"Execution error: {str(e)}")


# --------------------------------------------------------------------------------------
# Entry Point
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
