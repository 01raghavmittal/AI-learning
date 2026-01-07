'''
Docstring for Ai Agent.lab6

OpenAPI tools

'''
oepnai_spec= {
    "openapi": "3.1.0",
    "info": {
      "title": "get weather data",
      "description": "Retrieves current weather data for a location based on wttr.in.",
      "version": "v1.0.0"
    },
    "servers": [
      {
        "url": "https://wttr.in"
      }
    ],
    "auth": [],
    "paths": {
      "/{location}": {
        "get": {
          "description": "Get weather information for a specific location",
          "operationId": "GetCurrentWeather",
          "parameters": [
            {
              "name": "location",
              "in": "path",
              "description": "City or location to retrieve the weather for",
              "required": true,
              "schema": {
                "type": "string"
              }
            },
            {
             "name": "format",
             "in": "query",
             "description": "Always use j1 value for this parameter",
             "required": true,
             "schema": {
               "type": "string",
               "default": "j1"
            }
           }
          ],
          "responses": {
            "200": {
              "description": "Successful response",
              "content": {
                "text/plain": {
                  "schema": {
                    "type": "string"
                  }
                }
              }
            },
            "404": {
              "description": "Location not found"
            }
          },
          "deprecated": false
        }
      }
    },
    "components": {
      "schemes": {}
    }
  }


import os,time
import json
import requests

from dotenv import load_dotenv

load_dotenv()
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import OpenApiTool, OpenApiAnonymousAuthDetails

#----------------- OPENAIAPI----------------

auth = OpenApiAnonymousAuthDetails

openapi=OpenApiTool(name='get_weather',spec=oepnai_spec, description="retrieve weather information")



# ------------------- CLIENT INIT -------------------

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

#---------------------------------------------------

with project_client:
    agent = project_client.agents.create_agent(
        name='Lab6 agent',
        model="gpt-40",
        instructions="you are helpful assistant",
        tools=openapi.definitions )
    
    
    print(f"created agent, ID:{agent.id}")

    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    user_query = input("Enter query: ")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )
    print(f"Created message, ID: {message.id}")
    
    run = project_client.agents.runs.create(
        thread_id=thread.id,
        agent_id=agent.id
    )

    