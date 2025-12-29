from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")

azure_openai_client = AzureOpenAI(
    api_key=azure_openai_key,
    api_version="2024-02-15-preview",
    azure_endpoint=azure_openai_endpoint
)

ontology_list = []


'''
### Creating a function to identify nodes and their relationships
the code will send a call to GPT engine and the GPT engine will output nodes and relationships based upon the ontology defined in the prompt we feed
it with

'''
def identitfy_relationships_and_nodes(file_text):
    
    system_prompt = f"""Assistant is a Named Entity Recognition (NER) expert. The assistant can identify named entities 
    such as a person, place, or thing. The assistant can also identify entity relationships, which describe
    how entities relate to each other (eg: married to, located in, held by). Identify the named entities
    and the entity relationships present in the text by returning comma separated list of tuples
    representing the relationship between two entities in the format (entity, relationship, entity). Only
    generate tuples from the list of entities and the possible entity relationships listed below. Return
    only generated tuples in a comma separated tuple separated by a new line for each tuple.

    Entities:
    - Hotel
    - Location
    - Facilities
    - CustomerTyoe
    - Reviewer

    Relationships:
    - [Hotel],is_located_in,[Location]
    - [Hotel],has_facilities,[Facilities]
    - [Hotel],has_customers,[CustomerType]
    - [Hotel],has_reviewer,[Reviewer]

    Example Output:
    Creek Hotel,is_located_in,Dubai
    Creek Hotel,has_facilities,swimming pool
    Creek Hotel,has_customers,Businessmen
    Creek Hotel,has_customers,senior citizens
    Creek Hotel,has_reviewer,John Doe

    """

    user_prompt = f"""Identify the named entities and entity relationships in the hotel review text above. Return the
    entities and entity relationships in a tuple separated by commas. Return only generated tuples in a
    comma separated tuple separated by a new line for each tuple.

    Text: {file_text}"""


    
    chat_completions_response = azure_openai_client.chat.completions.create(
        model = os.getenv("GPT_ENGINE"),
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    
    ontology_list.append(chat_completions_response.choices[0].message.content)

    print(chat_completions_response.choices[0].message.content)



# with open(r"reviews\201801.pdf", "r") as file:
#     file_text = file.read()
#     identitfy_relationships_and_nodes(file_text)
    
# with open(r"reviews\201802.pdf", "r") as file:
#     file_text = file.read()
#     identitfy_relationships_and_nodes(file_text)

# with open(r"reviews\201803.pdf", "r") as file:
#     file_text = file.read()
#     identitfy_relationships_and_nodes(file_text)

# with open(r"reviews\201804.pdf", "r") as file:
#     file_text = file.read()
#     identitfy_relationships_and_nodes(file_text)

# with open(r"reviews\201805.pdf", "r") as file:
#     file_text = file.read()
#     identitfy_relationships_and_nodes(file_text)

import PyPDF2
import os

def get_pdf_text(file_path):
    text = ""
    # "rb" mode use karna zaroori hai (Read Binary)
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    return text

# Files ki list
files = ["201801.pdf", "201802.pdf", "201803.pdf", "201804.pdf", "201805.pdf"]

for filename in files:
    # Kyunki aap terminal mein pehle se 'Graph RAG' folder mein hain
    path = os.path.join("reviews", filename)
    
    if os.path.exists(path):
        print(f"Processing: {filename}...")
        file_text = get_pdf_text(path)
        
        # Ab aapka function kaam karega
        identitfy_relationships_and_nodes(file_text)
    else:
        print(f"File not found: {path}")



node_creation_cypher_list = []


'''
### Creating A Function for Cypher Query Generation
Based upon the relationships and nodes derived from the text, we instruct GPT engine to generate cypher query
for building a grpah in Neo4j Aura Database


'''


def generate_cypher_for_node_creation(ontology_text):
    cypher_system_prompt = f""" Assistant is an expert in Neo4j Cypher development. Create a cypher query to generate a graph using the data points provided. 
    make sure to only include the cypher query in your response so that I can directly send this cypher query to the Neo4j database API endpoint
    via a POST request. The data is in the format of a comma separated tuple separated by a new line for each tuple.

    """
    
    cypher_user_prompt = f"""Generate a cypher query to create new nodes and their relationships given the data provided. Return only the cypher query. 
    Data is composed of relationships between entities that have been extracted using NER.
    The data is in the format of a comma separated tuple separated by a new line for each tuple.
    
    Example Input: 
    Creek Hotel,is_located_in,Dubai
    Creek Hotel,has_customers,businessmen
    Creek Hotel,has_customers,tourists
    Creek Hotel,has_reviewer,Ryouta Sato
    Creeh Hotel,has_facilities,swimming pool

    Example Output:
    CREATE (ch:Hotel {{name: 'Creek Hotel'}})-[:is_located_in]->(d:Location {{name: 'Dubai'}}),
        (ch)-[:has_customers]->(b:CustomerType {{name: 'businessmen'}}),
        (ch)-[:has_customers]->(t:CustomerType {{name: 'tourists'}}),
        (ch)-[:has_reviewer]->(rs:Reviewer {{name: 'Ryouta Sato'}})
        (ch)-[:has_facilities]->(sp:Facilities {{name: 'swimming pool'}})
        
    strictly stick to the above output format
    
    use distinct variable names for each node and relationship to avoid conflicts

    the data is: {ontology_text}

    """
    
    cypher_query = azure_openai_client.chat.completions.create(
        model = os.getenv("GPT_ENGINE"),
        messages = [
            {"role": "system", "content": cypher_system_prompt},
            {"role": "user", "content": cypher_user_prompt}
        ],
        temperature=0
    )
    
    node_creation_cypher_list.append(cypher_query.choices[0].message.content)

    print(cypher_query.choices[0].message.content)



for x in ontology_list:
    generate_cypher_for_node_creation(x)


for x in node_creation_cypher_list:
    print(x)

print(node_creation_cypher_list[0])



from neo4j import GraphDatabase
import os

uri = os.getenv("NEO4J_URI")

url = "neo4j+s://{}.databases.neo4j.io".format(uri)

neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(url, auth=(neo4j_username, neo4j_password))
import re

def clean_cypher_query(query):
    # This removes ```cypher, ```Cypher, or just ``` from the start and end
    clean_query = re.sub(r'^```[a-zA-Z]*\n', '', query)
    clean_query = re.sub(r'\n```$', '', clean_query)
    # Also strip any leading/trailing whitespace
    return clean_query.strip()

with driver.session() as session:
        for cypher_query in node_creation_cypher_list:
            clean_query = clean_cypher_query(cypher_query)
            session.run(cypher_query)
            print(f"Executed: {cypher_query}")



'''
### Defining function for generation of cypher query to retrieve nodes and context based upon user query
'''

def query_neo4j_graph(user_query):
    query_with_cypher_system_prompt = f"""Assistant is an expert in Neo4j Cypher development. Only return a cypher query based on the user query
    the cypher graph has the following schema:

    Nodes:
    - Hotel
    - Location
    - Facilities
    - CustomerType
    - Reviewer

    Relationships:
    - [Hotel],is_located_in,[Location]
    - [Hotel],has_facilities,[Facilities]
    - [Hotel],has_customers,[CustomerType]
    - [Hotel],has_reviewer,[Reviewer]

    example of a node created through cypher query:
    {node_creation_cypher_list[0]}
    
    Example Input:
    what hotels are reviewed by Ryouta Sato?
    
    Example Output:
    MATCH (h:Hotel)-[:has_reviewer]-(r:Reviewer {{name: 'Ryouta Sato'}})
    RETURN h

    stick strictly to the above output format
    """

    query_with_cypher_user_prompt = f"""Generate a cypher query to answer the user query.
    user_query = {user_query}"""
    
    query_response = azure_openai_client.chat.completions.create(
        model = os.getenv("GPT_ENGINE"),
        messages = [
            {"role": "system", "content": query_with_cypher_system_prompt},
            {"role": "user", "content": query_with_cypher_user_prompt}
        ],
        temperature=0
    )
    
    
    
    cypher_query_for_retrieval = query_response.choices[0].message.content
    
    print(cypher_query_for_retrieval)
    
    return cypher_query_for_retrieval

user_query = "which hotels are visited by businessmen?"
cypher_query_for_retrieval = query_neo4j_graph(user_query)
with driver.session() as session:
        # Run the Cypher query
        result = session.run(cypher_query_for_retrieval)
        
        # Extract and print results
        records = [record.data() for record in result]
        print(records)

'''
### Sending a final call to GPT engine for summarisation

'''

final_system_prompt = f"""" you are an assistant made to help people. You will be provided with the results of 
a cypher query that returns data from a neo4j database. The results are in the form of list with each object inside
the list containing the final result. Answer the user query in a friendly and an easy to understand manner. 

Note that you will be provided with both the user query that triggered the result and the result itself."""

final_user_prompt = f"""Answer the user query using the results of the cypher query provided below.
user_query = {user_query}
result = {records}"""

final_answer = azure_openai_client.chat.completions.create(
    model = os.getenv("GPT_ENGINE"),
    messages = [
        {"role": "system", "content": final_system_prompt},
        {"role": "user", "content": final_user_prompt}
    ],
    temperature=0.7
)

print(final_answer.choices[0].message.content)