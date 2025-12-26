import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()

# Set the Groq API key directly from the environment
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the LLaMA3-70B model from Groq
model = init_chat_model("f", model_provider="groq")

# Send a message to the model
response = model.invoke("Hello, world!")
print(response)


