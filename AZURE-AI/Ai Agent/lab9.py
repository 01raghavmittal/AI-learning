'''
Docstring for Ai Agent.lab9


agentic rag
'''

import os
import time
import json
import requests
from typing import Any,Callable,Set,Dict,List,Optional

from dotenv import load_dotenv
load_dotenv()


from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


# ------------------- CLIENT INIT -------------------

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

#------------------MAIN AGENT LOGIC------------------------------
with project_client:

    agent=project_client.agents.create_agent(
        name="lab9 agent",
        

    )




