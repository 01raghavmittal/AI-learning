# pip install -qU "langchain[anthropic]" to call the model
import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_tavily import TavilySearch


load_dotenv()
print(os.getenv("TAVILY_API_KEY"))
print(os.getenv("GROQ_API_KEY"))



web_search = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # include_favicon=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None,
    # country=None
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="openai/gpt-oss-120b",temperature=0)

agent = create_agent(
    model=model,
    tools=[get_weather,web_search],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result)


print('*'*100)

from langchain_core.messages import HumanMessage, AIMessage


# If result is a dict containing 'messages'
messages = result['messages']

# Grab the last AIMessage with content
final_output = None
for msg in reversed(messages):
    # Depending on LangChain version, AIMessage can be checked via 'type' or 'role'
    if msg.get('type') == 'AIMessage' or msg.get('role') == 'assistant':
        if msg.get('content'):
            final_output = msg['content']
            break

print(final_output)





