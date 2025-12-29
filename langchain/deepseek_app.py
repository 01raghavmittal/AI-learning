import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv() 

# You can optionally verify the keys were loaded
print(os.getenv("DEEPSEEK_API_KEY")) 
print(os.getenv("DEEPSEEK_API_BASE"))

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# --- 1. Get the variables from the environment ---
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_API_BASE")

if not DEEPSEEK_KEY or not DEEPSEEK_BASE:
    raise ValueError("DeepSeek API key or base URL not found in environment variables.")

# --- 2. Initialize the ChatOpenAI model ---
# Use the DeepSeek key and the custom base URL
llm  = init_chat_model("openai/gpt-oss-20b", model_provider="groq")


# --- 3. Run a test inference ---
print("Sending request to DeepSeek-V3.1...")

response = llm.invoke(
    [HumanMessage(content="Describe a deep learning model to optimize supply chain logistics in two sentences.")]
)

print("\n--- DeepSeek Response ---")
print(response.content)