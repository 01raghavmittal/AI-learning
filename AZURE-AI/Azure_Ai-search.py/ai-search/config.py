import os
from dotenv import load_dotenv
load_dotenv()

# -----------------------------------------
# ENVIRONMENT VARIABLES
# -----------------------------------------
ai_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
ai_search_key = os.getenv("AZURE_SEARCH_API_KEY")

blob_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "learning")

document_intelligence_endpoint = os.getenv("AZURE_DI_ENDPOINT")
document_intelligence_key = os.getenv("AZURE_DI_KEY")

openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_key = os.getenv("AZURE_OPENAI_API_KEY")

llm_model = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o")
emd_model = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT","text-embedding-3-small")

index_name = os.getenv("INDEX_NAME", "rag-index")
datasource_name = os.getenv("DATASOURCE_NAME", "blob-datasource")
skillset_name = os.getenv("SKILLSET_NAME", "rag-skillset")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME","learning")





