
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
OPENAI_EMBED_DEPLOYMENT  = os.getenv("openai_embedding_deployment") or os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT")
OPENAI_EMBED_MODEL_NAME  = os.getenv("openai_embedding_model_name") or os.getenv("AZURE_OPENAI_EMBED_MODEL")

OPENAI_LLM_MODEL_NAME ="gpt-4o mini"
OPENAI_LLM_DEPLOYMENT =""

# Names (you can hardcode or add to .env)
INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")
DATASOURCE_NAME = os.getenv("DATASOURCE_NAME", "blob-ds")
SKILLSET_NAME = os.getenv("SKILLSET_NAME", "rag-skillset")
INDEXER_NAME = os.getenv("INDEXER_NAME", "blob-indexer")


'''
# Basic validation
if not SEARCH_ENDPOINT or not SEARCH_KEY:
    raise SystemExit("Missing ai-search_enpoint/ai-search_key (or AZURE_SEARCH_ENDPOINT/AZURE_SEARCH_KEY) in .env")

if not OPENAI_ENDPOINT or not OPENAI_KEY or not OPENAI_EMBED_DEPLOYMENT or not OPENAI_EMBED_MODEL_NAME:
    raise SystemExit("Missing OpenAI settings: openai_endpoint, openai_key, openai_embedding_deployment, openai_embedding_model_name")

'''



#------------------------------------------------------------------



from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient


# -----------------------------
# Initialize client
# -----------------------------

#search index client

index_client= SearchIndexClient(endpoint=SEARCH_ENDPOINT,credential=AzureKeyCredential(SEARCH_KEY))



#search indexer client
indexer_client = SearchIndexerClient(endpoint=SEARCH_ENDPOINT,credential=AzureKeyCredential(SEARCH_KEY))




#----------------------------------------------------------------------------------



# -----------------------------
# Initialize datasource
# -----------------------------
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection,SearchIndexerDataContainer


data_source = SearchIndexerDataSourceConnection(
    name=DATASOURCE_NAME,
    type="azureblob",
    connection_string=BLOB_ACCOUNT_URL,
    container=SearchIndexerDataContainer(name=CONTAINER_NAME)
    #  indexer_permission_options=[IndexerPermissionOption.GROUP_IDS] # '''' REPO 
)


'''


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



'''

#---------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------
# Skillset = Document Intelligence layout → Text split (chunking) → Azure OpenAI embeddings
#------------------------------------------------------------------------------------------------------------



# Skill 1: Document Intelligence Layout (structure-aware Markdown)

layout_skill = SearchIndexerSkill(
    name="doc-intel-layout",
    description="Extract Markdown with headings & layout using Azure Document Intelligence (Layout model)",
    skill_type="DocumentIntelligenceLayoutSkill",   # OData type behind the scenes
    context="/document",
    inputs=[InputFieldMappingEntry(name="document", source="/document")],
    outputs=[OutputFieldMappingEntry(name="markdown", target_name="markdown")]
)
# Optional layout tuning via additional properties (header depth, cardinality)
layout_skill.additional_properties = {
    "outputMode": "oneToOne",
    "markdownHeaderDepth": "h6"
}


# Skill 2: Chunking (Text Split skill)

split_skill = SplitSkill(
    name="chunking-skill",
    description="Chunk Markdown into pages with overlap for embeddings",
    context="/document",
    inputs=[InputFieldMappingEntry(name="text", source="/document/markdown")],
    outputs=[OutputFieldMappingEntry(name="textItems", target_name="pages")]
)
# Set split parameters via additional_properties
split_skill.additional_properties = {
    "textSplitMode": "pages",
    "maximumPageLength": 2000,   # you asked for ~2000; good for large docs
    "pageOverlapLength": 200,
    "defaultLanguageCode": "en"
}



# Skill 3: Vectorization (Azure OpenAI Embedding skill)

embedding_skill = SearchIndexerSkill(
    name="vector-skill",
    description="Generate embeddings for each chunk using Azure OpenAI",
    skill_type="AzureOpenAIEmbeddingSkill",   # OData type
    context="/document/pages/*",
    inputs=[InputFieldMappingEntry(name="text", source="/document/pages/*")],
    outputs=[OutputFieldMappingEntry(name="embedding", target_name="vector")]
)
embedding_skill.additional_properties = {
    "resourceUri": OPENAI_ENDPOINT,             # must be a supported Azure OpenAI domain (e.g., *.openai.azure.com)
    "apiKey": OPENAI_KEY,
    "deploymentId": OPENAI_EMBED_DEPLOYMENT,    # e.g., text-embedding-3-small (your deployment name)
    "modelName": OPENAI_EMBED_MODEL_NAME        # e.g., text-embedding-3-small / text-embedding-3-large
    # If you configure custom embedding dimensions on the model, set:
    # "dimensions": 1536
    # Make sure your index vector field uses the same dimensions.
}





# Skill 3: Vectorization (Azure OpenAI Embedding skill)
# OData type: #Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-azure-openai-embedding
# -----------------------------





from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    SearchIndexerSkill,          # generic wrapper for skills identified by OData type
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SplitSkill                   # dedicated class for Text Split
)







# -----------------------------
# Skill 1: Document Intelligence Layout (structure-aware Markdown)
# OData type: #Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-intelligence-layout
# -----------------------------
layout_skill = SearchIndexerSkill(
    name="doc-intel-layout",
    description="Extract Markdown with headings & layout using Azure Document Intelligence (Layout model)",
    skill_type="DocumentIntelligenceLayoutSkill",   # OData type behind the scenes
    context="/document",
    inputs=[InputFieldMappingEntry(name="document", source="/document")],
    outputs=[OutputFieldMappingEntry(name="markdown", target_name="markdown")]
)
# Optional layout tuning via additional properties (header depth, cardinality)
layout_skill.additional_properties = {
    "outputMode": "oneToOne",
    "markdownHeaderDepth": "h6"
}

# -----------------------------
# Skill 2: Chunking (Text Split skill)
# OData type: #Microsoft.Skills.Text.SplitSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit
# -----------------------------
split_skill = SplitSkill(
    name="chunking-skill",
    description="Chunk Markdown into pages with overlap for embeddings",
    context="/document",
    inputs=[InputFieldMappingEntry(name="text", source="/document/markdown")],
    outputs=[OutputFieldMappingEntry(name="textItems", target_name="pages")]
)
# Set split parameters via additional_properties
split_skill.additional_properties = {
    "textSplitMode": "pages",
    "maximumPageLength": 2000,   # you asked for ~2000; good for large docs
    "pageOverlapLength": 200,
    "defaultLanguageCode": "en"
}

# -----------------------------
# Skill 3: Vectorization (Azure OpenAI Embedding skill)
# OData type: #Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-azure-openai-embedding
# -----------------------------
embedding_skill = SearchIndexerSkill(
    name="vector-skill",
    description="Generate embeddings for each chunk using Azure OpenAI",
    skill_type="AzureOpenAIEmbeddingSkill",   # OData type
    context="/document/pages/*",
    inputs=[InputFieldMappingEntry(name="text", source="/document/pages/*")],
    outputs=[OutputFieldMappingEntry(name="embedding", target_name="vector")]
)
embedding_skill.additional_properties = {
    "resourceUri": OPENAI_ENDPOINT,             # must be a supported Azure OpenAI domain (e.g., *.openai.azure.com)
    "apiKey": OPENAI_KEY,
    "deploymentId": OPENAI_EMBED_DEPLOYMENT,    # e.g., text-embedding-3-small (your deployment name)
    "modelName": OPENAI_EMBED_MODEL_NAME        # e.g., text-embedding-3-small / text-embedding-3-large
    # If you configure custom embedding dimensions on the model, set:
    # "dimensions": 1536
    # Make sure your index vector field uses the same dimensions.
}

# -----------------------------
# Assemble skillset
# -----------------------------
skills = [layout_skill, split_skill, embedding_skill]

# If your DI setup requires a Foundry/AI Services key for enrichment billing, you can bind it here.
# Many setups can leave cognitive_services=None.
# Example binding (uncomment if you must pass a key):
# cognitive_services = {
#     "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
#     "description": "Foundry/DI key",
#     "key": DI_KEY
# }

skillset = SearchIndexerSkillset(
    name=SKILLSET_NAME,
    description="RAG skillset: Document Intelligence Layout → Split → Azure OpenAI embeddings",
    skills=skills,
    cognitive_services=None,
    knowledge_store=None
)

# Create or update skillset
result = index_client.create_or_update_skillset(skillset)
print(f"✅ Skillset '{result.name}' created/updated successfully.")













#--------------------------------------------------------------------------------






# INTIALISE SKILLSET
# 







#---------------------------------------------------------------
#FIELDS


index = SearchIndex(
    name=index_name,
    fields=[
        SearchField(name="id", type="Edm.String", key=True, filterable=True, sortable=True),
        SearchField(name="content", type="Edm.String", searchable=True, filterable=False, sortable=False),
        SearchField(name="oids", type="Collection(Edm.String)", filterable=True, permission_filter=PermissionFilter.USER_IDS),
        SearchField(name="groups", type="Collection(Edm.String)", filterable=True, permission_filter=PermissionFilter.GROUP_IDS),
        SearchField(name="metadata_storage_path", type="Edm.String", searchable=True),
        SearchField(name="metadata_storage_name", type="Edm.String", searchable=True)
    ],
    permission_filter_option=SearchIndexPermissionFilterOption.ENABLED
)

index_client.create_or_update_index(index=index)
print(f"Index '{index_name}' created with permission filter option enabled.")




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





#-----------------------------------------------------------------------------


# create_skillset.py
# Skillset = Document Intelligence layout → Text split (chunking) → Azure OpenAI embeddings
# Reads configuration from your .env file (fields you said you already set).

import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    SearchIndexerSkill,          # generic wrapper for skills identified by OData type
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SplitSkill                   # dedicated class for Text Split
)

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

SEARCH_ENDPOINT = os.getenv("ai-search_enpoint") or os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY      = os.getenv("ai-search_key")     or os.getenv("AZURE_SEARCH_KEY")
SKILLSET_NAME   = os.getenv("SKILLSET_NAME", "rag-skillset")

# Azure OpenAI (embeddings)
OPENAI_ENDPOINT          = os.getenv("openai_endpoint") or os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_KEY               = os.getenv("openai_key")      or os.getenv("AZURE_OPENAI_KEY")
OPENAI_EMBED_DEPLOYMENT  = os.getenv("openai_embedding_deployment") or os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT")
OPENAI_EMBED_MODEL_NAME  = os.getenv("openai_embedding_model_name") or os.getenv("AZURE_OPENAI_EMBED_MODEL")

# (Optional) Document Intelligence billing keys (only required in some setups)
DI_ENDPOINT = os.getenv("document_intellgence_endpoint") or os.getenv("AZURE_DI_ENDPOINT")
DI_KEY      = os.getenv("document_intellgence_key")      or os.getenv("AZURE_DI_KEY")

# Basic validation
if not SEARCH_ENDPOINT or not SEARCH_KEY:
    raise SystemExit("Missing ai-search_enpoint/ai-search_key (or AZURE_SEARCH_ENDPOINT/AZURE_SEARCH_KEY) in .env")

if not OPENAI_ENDPOINT or not OPENAI_KEY or not OPENAI_EMBED_DEPLOYMENT or not OPENAI_EMBED_MODEL_NAME:
    raise SystemExit("Missing OpenAI settings: openai_endpoint, openai_key, openai_embedding_deployment, openai_embedding_model_name")

# -----------------------------
# Initialize client
# -----------------------------
client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

# -----------------------------
# Skill 1: Document Intelligence Layout (structure-aware Markdown)
# OData type: #Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-intelligence-layout
# -----------------------------
layout_skill = SearchIndexerSkill(
    name="doc-intel-layout",
    description="Extract Markdown with headings & layout using Azure Document Intelligence (Layout model)",
    skill_type="DocumentIntelligenceLayoutSkill",   # OData type behind the scenes
    context="/document",
    inputs=[InputFieldMappingEntry(name="document", source="/document")],
    outputs=[OutputFieldMappingEntry(name="markdown", target_name="markdown")]
)
# Optional layout tuning via additional properties (header depth, cardinality)
layout_skill.additional_properties = {
    "outputMode": "oneToOne",
    "markdownHeaderDepth": "h6"
}

# -----------------------------
# Skill 2: Chunking (Text Split skill)
# OData type: #Microsoft.Skills.Text.SplitSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit
# -----------------------------
split_skill = SplitSkill(
    name="chunking-skill",
    description="Chunk Markdown into pages with overlap for embeddings",
    context="/document",
    inputs=[InputFieldMappingEntry(name="text", source="/document/markdown")],
    outputs=[OutputFieldMappingEntry(name="textItems", target_name="pages")]
)
# Set split parameters via additional_properties
split_skill.additional_properties = {
    "textSplitMode": "pages",
    "maximumPageLength": 2000,   # you asked for ~2000; good for large docs
    "pageOverlapLength": 200,
    "defaultLanguageCode": "en"
}

# -----------------------------
# Skill 3: Vectorization (Azure OpenAI Embedding skill)
# OData type: #Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill
# Docs: https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-azure-openai-embedding
# -----------------------------
embedding_skill = SearchIndexerSkill(
    name="vector-skill",
    description="Generate embeddings for each chunk using Azure OpenAI",
    skill_type="AzureOpenAIEmbeddingSkill",   # OData type
    context="/document/pages/*",
    inputs=[InputFieldMappingEntry(name="text", source="/document/pages/*")],
    outputs=[OutputFieldMappingEntry(name="embedding", target_name="vector")]
)
embedding_skill.additional_properties = {
    "resourceUri": OPENAI_ENDPOINT,             # must be a supported Azure OpenAI domain (e.g., *.openai.azure.com)
    "apiKey": OPENAI_KEY,
    "deploymentId": OPENAI_EMBED_DEPLOYMENT,    # e.g., text-embedding-3-small (your deployment name)
    "modelName": OPENAI_EMBED_MODEL_NAME        # e.g., text-embedding-3-small / text-embedding-3-large
    # If you configure custom embedding dimensions on the model, set:
    # "dimensions": 1536
    # Make sure your index vector field uses the same dimensions.
}

# -----------------------------
# Assemble skillset
# -----------------------------
skills = [layout_skill, split_skill, embedding_skill]

# If your DI setup requires a Foundry/AI Services key for enrichment billing, you can bind it here.
# Many setups can leave cognitive_services=None.
# Example binding (uncomment if you must pass a key):
# cognitive_services = {
#     "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
#     "description": "Foundry/DI key",
#     "key": DI_KEY
# }

skillset = SearchIndexerSkillset(
    name=SKILLSET_NAME,
    description="RAG skillset: Document Intelligence Layout → Split → Azure OpenAI embeddings",
    skills=skills,
    cognitive_services=None,
    knowledge_store=None
)

# Create or update skillset
result = client.create_or_update_skillset(skillset)
print(f"✅ Skillset '{result.name}' created/updated successfully.")
