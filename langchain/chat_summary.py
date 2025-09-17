import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# Your actual content to summarize
information = '''
The cheetah is the fastest land animal, capable of reaching speeds up to 70 mph.
It uses its speed to hunt prey in short bursts and has a lightweight body built for acceleration.
'''

# Define the prompt template
summary_template = """
Given the information below, I want to create:
1. A short summary
2. Two interesting facts about it

Information:
{information}
"""

# Fix: input_variables should be a list, and 'template' is spelled correctly
summary_prompt_template = PromptTemplate(
    input_variables=["information"],
    template=summary_template
)

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = init_chat_model("openai/gpt-oss-20b", model_provider="groq")





formatted_prompt = summary_prompt_template.format(information=information)
response = model.invoke(formatted_prompt)



chain=summary_prompt_template | model
response_1=chain.invoke({"information":information})

# Print the result
print(response)
print(response_1)
