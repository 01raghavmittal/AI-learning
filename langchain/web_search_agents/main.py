# import os
# from dotenv import load_dotenv
# load_dotenv()

# from langchain.agents import AgentExecutor
# from langchain.agents.react.agent import create_react_agent
# from langchain_tavily import TavilySearch
# from langchain import hub
# from langchain.chat_models import init_chat_model
# from langchain_groq import ChatGroq


# model = ChatGroq(model="deepseek-r1-distill-llama-70b",temperature=0)

# tools =[TavilySearch()]
# prompt=hub.pull("hwchase17/react")

# agent = create_react_agent(model, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True, handle_parsing_errors=True)

# result= agent_executor.invoke(input={
#         "input":"what is current weather in banglore"
# }   
# )
 
# print(result)

#--------------------------------------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from langchain.agents import create_react_agent
from langchain_tavily import TavilySearch
from langchain import hub
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent
from langchain.agents.agent_executor import AgentExecutor

tools = [TavilySearchResults(max_results=5)]
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


model = ChatGroq(model="openai/gpt-oss-120b",temperature=0)

# tools =[TavilySearch()]
prompt=hub.pull("hwchase17/react")

# agent = create_react_agent(model, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True, handle_parsing_errors=True)

result= agent_executor.invoke(input={
        "input":"what is current weather in banglore"
}   
)

print(result)




