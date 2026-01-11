# step 1:
import os,time


from dotenv import load_dotenv
load_dotenv()




# -----------------------------
# Load environment
# -----------------------------



# Azure OpenAI
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Azure AI Search
SEARCH_ENDPOINT = os.getenv("AI-SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AI-SEARCH_KEY")

# Blob Storage (for data source)
BLOB_ACCOUNT_URL = os.getenv("BLOB_SHTORAGE_URL")   
BLOB_KEY = os.getenv("BLOB_SHTORAGE_KEY")
CONTAINER_NAME = os.getenv("learning")

# Document Intelligence (if using layout-aware skill)
DI_ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
DI_KEY = os.getenv("DOCUMENT_INTELLIGENCE_KEY")


# Model name and version
OPENAI_EMBED_DEPLOYMENT  = os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT","text-embedding-ada-002")
OPENAI_EMBED_MODEL_NAME  = os.getenv("AZURE_OPENAI_EMBED_MODEL","2")

OPENAI_LLM_MODEL_NAME =os.getenv("AZURE_OPENAI_LLM_MODEL","gpt-4o-mini")
OPENAI_LLM_DEPLOYMENT =os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT","2024-07-18")

# Names (you can hardcode or add to .env)
INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")
DATASOURCE_NAME = os.getenv("DATASOURCE_NAME", "blob-ds")
SKILLSET_NAME = os.getenv("SKILLSET_NAME", "rag-skillset")
INDEXER_NAME = os.getenv("INDEXER_NAME", "blob-indexer")






#------------------------------------------------------------------






# Step 2
# create_index.py

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField,
    VectorSearch, HnswVectorSearchAlgorithmConfiguration, VectorSearchProfile
)

client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

fields = [
    SimpleField(name="id", type="Edm.String", key=True),
    SearchableField(name="content", type="Edm.String"),
    SimpleField(name="filename", type="Edm.String", filterable=True, sortable=True),
    SimpleField(name="pageNumber", type="Edm.Int32", filterable=True, sortable=True),
    SimpleField(name="chunkId", type="Edm.String", filterable=True),
    SimpleField(name="title", type="Edm.String", filterable=True, sortable=True),
    SimpleField(name="metadata", type="Edm.String"),
    # Vector field for embeddings (1536 dims typical for text-embedding-3 family)
    SimpleField(name="contentVector", type="Collection(Edm.Single)", searchable=True),
]



vector_search = VectorSearch(
    algorithms=[HnswVectorSearchAlgorithmConfiguration(name="hnsw-default", m=32, efConstruction=400)],
    profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="hnsw-default")]
)

index = SearchIndex(name=INDEX_NAME, fields=fields, vector_search=vector_search)
client.create_or_update_index(index)
print("Index created/updated:", INDEX_NAME)


#----------------------------------------------------------------------------------------------------------------


# Step 3
# create_datasource.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection, SearchIndexerDataContainer
from config import SEARCH_ENDPOINT, SEARCH_KEY, DATASOURCE_NAME, BLOB_ACCOUNT_URL, BLOB_KEY, CONTAINER_NAME

client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

# Connection string-like syntax for blob DS using key
# Format: "DefaultEndpointsProtocol=https;AccountName=<name>;AccountKey=<key>;EndpointSuffix=core.windows.net"
# If you only have URL + key, build from them or use the 'connection string' from portal.
account_name = BLOB_ACCOUNT_URL.split("//")[1].split(".")[0]
conn_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={BLOB_KEY};EndpointSuffix=core.windows.net"

data_source = SearchIndexerDataSourceConnection(
    name=DATASOURCE_NAME,
    type="azureblob",
    connection_string=conn_str,
    container=SearchIndexerDataContainer(name=CONTAINER_NAME)
)

client.create_or_update_data_source_connection(data_source)
print("Data source created:", DATASOURCE_NAME)


#-------------------------------------------------------------------------------------------------------------------------



# step 4


# create_skillset.py

# Creates (or updates) an Azure AI Search skillset with:
# 1) Document Intelligence Layout skill (structure-aware extraction → Markdown)
# 2) Text Split skill (chunking with overlap)
# 3) Azure OpenAI Embedding skill (vectorization during indexing)
#




from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    SearchIndexerSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
)

# 1) Document Intelligence Layout skill (Markdown output)
layout_skill = SearchIndexerSkill(
    name="layout-skill",
    description="Extract markdown with headings/structure using Azure Document Intelligence layout model",
    skill_type="DocumentIntelligenceLayoutSkill",  # OData type: #Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill
    context="/document",
    inputs=[
        InputFieldMappingEntry(name="document", source="/document")
    ],
    outputs=[
        OutputFieldMappingEntry(name="markdown", target_name="markdown")
    ]
)

# 2) Text Split (chunking) – split markdown into ~5k-char pages with 200 char overlap
chunk_skill = SearchIndexerSkill(
    name="chunk-skill",
    description="Chunk markdown into pages with overlap",
    skill_type="SplitSkill",  # OData type: #Microsoft.Skills.Text.SplitSkill
    context="/document",
    inputs=[
        InputFieldMappingEntry(name="text", source="/document/markdown")
    ],
    outputs=[
        OutputFieldMappingEntry(name="textItems", target_name="chunks")
    ]
)
# Extended parameters for SplitSkill
chunk_skill.additional_properties = {
    "textSplitMode": "pages",       # or "sentences" / preview token mode via REST
    "maximumPageLength": 5000,      # ~5k characters
    "pageOverlapLength": 200,       # overlap to preserve context
    "defaultLanguageCode": "en"
}

# 3) Azure OpenAI Embedding skill – vectorize each chunk
embedding_skill = SearchIndexerSkill(
    name="embedding-skill",
    description="Generate embeddings for each chunk using Azure OpenAI",
    skill_type="AzureOpenAIEmbeddingSkill",  # OData type: #Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill
    context="/document/chunks/*",
    inputs=[
        InputFieldMappingEntry(name="text", source="/document/chunks/*")
    ],
    outputs=[
        OutputFieldMappingEntry(name="embedding", target_name="contentVector")
    ]
)
# Embedding skill parameters
embedding_skill.additional_properties = {
    "resourceUri": OPENAI_ENDPOINT,           # must be *.openai.azure.com / services.ai.azure.com / cognitiveservices.azure.com
    "apiKey": OPENAI_KEY,
    "deploymentId": OPENAI_EMBED_DEPLOYMENT,  # your embeddings deployment name
    "modelName": OPENAI_EMBED_MODEL_NAME      # e.g., text-embedding-3-small / text-embedding-3-large
    # If you need custom dimensions:
    # "dimensions": 1536
    # Make sure your index vector field uses the same dimensions.
}

skills = [layout_skill, chunk_skill, embedding_skill]

# Optional: bind Foundry/DI billing via cognitiveServices (often not required)
# cognitive_services = {
#     "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
#     "description": "Foundry/DI key",
#     "key": DI_KEY
# }

skillset = SearchIndexerSkillset(
    name=SKILLSET_NAME,
    description="RAG skillset: Document Intelligence Layout → Split → Embeddings",
    skills=skills,
    cognitive_services=None,  # set to cognitive_services if your environment requires DI key binding
    knowledge_store=None
)

# -----------------------------
# Create or update skillset
# -----------------------------
result = client.create_or_update_skillset(skillset)
print(f"Skillset '{result.name}' created/updated successfully.")







# -------------------------------------------------------------------------------------------

# Step 5

# create_indexer.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndexer
from config import SEARCH_ENDPOINT, SEARCH_KEY, INDEXER_NAME, INDEX_NAME, DATASOURCE_NAME, SKILLSET_NAME

client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

indexer = SearchIndexer(
    name=INDEXER_NAME,
    data_source_name=DATASOURCE_NAME,
    target_index_name=INDEX_NAME,
    skillset_name=SKILLSET_NAME
    # TODO: If you want Integrated Vectorization now, I’ll add REST config snippet next.
)

client.create_or_update_indexer(indexer)
print("Indexer created:", INDEXER_NAME)







#-------------------------------------------------------------------------------------------------------------


# Step 6


# run_indexer.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from config import SEARCH_ENDPOINT, SEARCH_KEY, INDEXER_NAME

client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))
client.run_indexer(INDEXER_NAME)
print("Indexer run triggered:", INDEXER_NAME)




#-------------------------------------------------------------

# Step 7

# Configure Integrated Vectorization via REST


#-----------------------------------------------------------------------

#Step 8


# query.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from config import SEARCH_ENDPOINT, SEARCH_KEY, INDEX_NAME

search = SearchClient(SEARCH_ENDPOINT, INDEX_NAME, AzureKeyCredential(SEARCH_KEY))

def keyword_search(q):
    results = search.search(search_text=q, query_type=QueryType.SIMPLE,
                            select=["content", "filename", "pageNumber", "chunkId", "title"])
    return list(results)

# For vector/hybrid, we’ll add OpenAI embeddings next if you want.




