from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
prompt_template.invoke({"topic": "cats"})
print(prompt_template.invoke({"topic": "cats"}))

#-----------------------------------------------------------------------------------------------------------


from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

prompt_template.invoke({"topic": "cats"})

print(prompt_template.invoke({"topic": "cats"}))


#------------------------------------------------------------------------------------------------
print()
print('MessagesPlaceholder')
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

# Simple example with one message
prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})

# More complex example with conversation history
messages_to_pass = [
    HumanMessage(content="What's the capital of France?"),
    AIMessage(content="The capital of France is Paris."),
    HumanMessage(content="And what about Germany?")
]

formatted_prompt = prompt_template.invoke({"msgs": messages_to_pass})
print(formatted_prompt)


#-------------------------------------------------------------------------------------------------------------------




