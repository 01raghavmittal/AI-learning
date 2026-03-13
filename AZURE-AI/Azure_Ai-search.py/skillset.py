
import os

from dotenv import load_dotenv
load_dotenv()

ai_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
ai_search_key = os.getenv("AZURE_SEARCH_API_KEY")

blob_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


document_intelligence_endpoint = os.getenv("AZURE_DI_ENDPOINT")
document_intelligence_key = os.getenv("AZURE_DI_KEY")


openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai_key = os.getenv("AZURE_OPENAI_API_KEY")


llm_model = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o")  
emd_model = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT",)  

# Keep indexer objects consistent
index_name = os.getenv("INDEX_NAME", "rag-index")
datasource_name = os.getenv("DATASOURCE_NAME", "blob-datasource")
skillset_name = os.getenv("SKILLSET_NAME", "rag-skillset")
indexer_name = os.getenv("INDEXER_NAME", "blob-indexer")


container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME","learning")


#----------------------------------------------------------------


from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    SearchIndexerSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    CognitiveServicesAccountKey,
    VectorSearchAlgorithmConfiguration,
)

# Clients
indexer_client = SearchIndexerClient(
    endpoint=ai_search_endpoint,
    credential=AzureKeyCredential(ai_search_key)
)

# Skillset definition
skillset = SearchIndexerSkillset(
    name=skillset_name,
    description="Multimodal skillset: extract text + images, verbalize images, embed text",
    skills=[
        # 1) Document Extraction Skill
        SearchIndexerSkill(
            odatatype="#Microsoft.Skills.Util.DocumentExtractionSkill",
            name="document-extraction-skill",
            description="Extract text & normalized images from PDFs",
            context="/document",
            inputs=[
                InputFieldMappingEntry(name="file_data", source="/document/file_data")
            ],
            outputs=[
                OutputFieldMappingEntry(name="content", target_name="extracted_content"),
                OutputFieldMappingEntry(name="normalized_images", target_name="normalized_images")
            ],
            configuration={
                "imageAction": "generateNormalizedImages",
                "normalizedImageMaxWidth": 2000,
                "normalizedImageMaxHeight": 2000
            }
        ),

        # 2) Text Split Skill
        SearchIndexerSkill(
            odatatype="#Microsoft.Skills.Text.SplitSkill",
            name="text-split-skill",
            description="Split long text into chunks",
            context="/document",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/extracted_content")
            ],
            outputs=[
                OutputFieldMappingEntry(name="text_chunks", target_name="text_chunks")
            ],
            configuration={
                "defaultLanguageCode": "en",
                "textSplitMode": "pages",
                "maximumPageLength": 2000,
                "pageOverlapLength": 200
            }
        ),

        # 3) GenAI Prompt Skill (Image Captioning)
        SearchIndexerSkill(
            odatatype="#Microsoft.Skills.Text.GenAIImageCaptionSkill",
            name="genai-image-caption-skill",
            description="Generate natural language captions for each image",
            context="/document/normalized_images/*",
            inputs=[
                InputFieldMappingEntry(name="image", source="/document/normalized_images/*/imageData")
            ],
            outputs=[
                OutputFieldMappingEntry(name="caption", target_name="image_captions")
            ],
            # configuration: specify your Azure OpenAI chat model
            configuration={
                "openAIResourceUri": openai_endpoint,
                "openAIKey": openai_key,
                "deploymentName": llm_model,
                "promptTemplate": "Describe this image in a concise manner:"
            }
        ),

        # 4) Embedding Skill (Azure OpenAI)
        SearchIndexerSkill(
            odatatype="#Microsoft.Skills.Vision.OpenAIEmbeddingSkill",
            name="openai-embedding-skill",
            description="Embed text chunks + image captions",
            context="/document",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/text_chunks"),
                InputFieldMappingEntry(name="text", source="/document/image_captions")
            ],
            outputs=[
                OutputFieldMappingEntry(name="vector", target_name="content_embedding")
            ],
            # configuration for embedding model deployment
            configuration={
                "model": emd_model
            }
        )
    ],
    # optional knowledge store configuration (store images in blob)
    knowledge_store={
        "storageConnectionString": blob_storage_connection_string,
        "projections": [
            {
                "source": "/document/normalized_images/*/imagePath",
                "target": "image_store"
            }
        ]
    }
)

# Create/Update skillset
indexer_client.create_or_update_skillset(skillset)
print(f"Skillset '{skillset_name}' created.")
