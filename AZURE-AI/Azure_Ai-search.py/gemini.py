import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    SearchIndexerDataContainer, SearchIndexerDataSourceConnection,
    SearchIndexer, FieldMapping, OutputFieldMapping, 
    TextSplitSkill, AzureOpenAIEmbeddingSkill, Skillset,
    # Document Intelligence related skill (Layout extraction)
    AzureAIServicesDocumentExtractionSkill 
)

load_dotenv()

# Credential Loading
SEARCH_ENDPOINT = os.getenv("ai-search_enpoint")
SEARCH_KEY = os.getenv("ai-search_key")
BLOB_CONNECTION = f"DefaultEndpointsProtocol=https;AccountName={os.getenv('blob_shtorage_url').split('//')[1].split('.')[0]};AccountKey={os.getenv('blob_shtorage_key')};EndpointSuffix=core.windows.net"
CONTAINER_NAME = os.getenv("container_name")

index_name = "smart-knowledge-index"
index_client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))
indexer_client = SearchIndexerClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

def create_rag_pipeline():
    # 1. DATA SOURCE: Blob Storage ko connect karna
    data_source = SearchIndexerDataSourceConnection(
        name="blob-source",
        type="azureblob",
        connection_string=BLOB_CONNECTION,
        container=SearchIndexerDataContainer(name=CONTAINER_NAME)
    )
    indexer_client.create_or_update_data_source_connection(data_source)
    print("✅ 1. Data Source Created.")

    # 2. SKILLSET: Chunking aur Vectorization (Document Intelligence included)
    # Skill 1: Smart Text Extraction
    doc_extraction_skill = AzureAIServicesDocumentExtractionSkill(
        name="doc-intel-skill",
        context="/document",
        resource_uri=os.getenv("document_intellgence_endpoint"),
        api_key=os.getenv("document_intellgence_key"),
        outputs=[{"name": "content", "targetName": "extracted_text"}]
    )

    # Skill 2: Chunking (Text Split)
    split_skill = TextSplitSkill(
        name="chunking-skill",
        context="/document",
        text_split_mode="pages",
        maximum_page_length=2000, # Large docs ke liye best
        page_overlap_length=200,
        inputs=[{"name": "text", "source": "/document/extracted_text"}],
        outputs=[{"name": "textItems", "targetName": "pages"}]
    )

    # Skill 3: Vectorization (Azure OpenAI)
    embedding_skill = AzureOpenAIEmbeddingSkill(
        name="vector-skill",
        context="/document/pages/*",
        resource_uri=os.getenv("openai_endpoint"),
        api_key=os.getenv("openai_key"),
        deployment_id="text-embedding-3-small", # Make sure this matches your deployment name
        inputs=[{"name": "text", "source": "/document/pages/*"}],
        outputs=[{"name": "embedding", "targetName": "vector"}]
    )

    skillset = Skillset(name="rag-skillset", skills=[doc_extraction_skill, split_skill, embedding_skill])
    indexer_client.create_or_update_skillset(skillset)
    print("✅ 2. Skillset (AI Logic) Created.")

    # 3. INDEX: Schema define karna (Citations ke liye fields)
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(name="vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="my-hsnw-profile"),
        # Metadata fields for Citations
        SimpleField(name="source_name", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source_path", type=SearchFieldDataType.String)
    ]
    
    vector_search = VectorSearch(
        profiles=[VectorSearchProfile(name="my-hsnw-profile", algorithm_configuration_name="my-hsnw")],
        algorithms=[HnswAlgorithmConfiguration(name="my-hsnw")]
    )

    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    index_client.create_or_update_index(index)
    print("✅ 3. Search Index Schema Created.")

    # 4. INDEXER: Sab kuch ek saath jodna
    indexer = SearchIndexer(
        name="rag-indexer",
        data_source_name="blob-source",
        target_index_name=index_name,
        skillset_name="rag-skillset",
        # Mapping Citation info from Blob Metadata
        field_mappings=[
            FieldMapping(source_field_name="metadata_storage_name", target_field_name="source_name"),
            FieldMapping(source_field_name="metadata_storage_path", target_field_name="source_path")
        ],
        output_field_mappings=[
            OutputFieldMapping(source_field_name="/document/pages/*", target_field_name="content"),
            OutputFieldMapping(source_field_name="/document/pages/*/vector", target_field_name="vector")
        ]
    )
    indexer_client.create_or_update_indexer(indexer)
    print("🚀 4. Indexer is running! Check Azure Portal to see progress.")

if __name__ == "__main__":
    create_rag_pipeline()