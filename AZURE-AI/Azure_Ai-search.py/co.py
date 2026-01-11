
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
emd_model = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")

index_name = os.getenv("INDEX_NAME", "rag-index")
datasource_name = os.getenv("DATASOURCE_NAME", "blob-datasource")
skillset_name = os.getenv("SKILLSET_NAME", "rag-skillset")


# ======================================================
# STEP 2: CREATE INDEX
# ======================================================
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    SemanticConfiguration, SemanticField, SemanticPrioritizedFields, SemanticSearch
)

index_client = SearchIndexClient(endpoint=ai_search_endpoint, credential=AzureKeyCredential(ai_search_key))

fields = [
    # KEY FIELD — MUST HAVE KEYWORD ANALYZER
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
        analyzer_name="keyword"            # REQUIRED FOR PROJECTIONS
    ),

    # REQUIRED FOR PROJECTION
    SimpleField(name="parent_id", type=SearchFieldDataType.String, filterable=True),

    SearchField(name="chunk_id",    type=SearchFieldDataType.String,  filterable=True),
    SearchField(name="source_file", type=SearchFieldDataType.String,  filterable=True),
    SearchField(name="page_number", type=SearchFieldDataType.Int32,   filterable=True),

    SearchField(name="title",    type=SearchFieldDataType.String, searchable=True, sortable=True, filterable=True),
    SearchField(name="chunk",    type=SearchFieldDataType.String, searchable=True),
    SearchField(name="metadata", type=SearchFieldDataType.String, searchable=True),

    # Tables + Images
    SearchField(name="tables", type=SearchFieldDataType.Collection(SearchFieldDataType.String)),
    SearchField(name="image_references", type=SearchFieldDataType.Collection(SearchFieldDataType.String)),

    # Vector field
    SearchField(
        name="chunk_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-profile"
    ),
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="my-hnsw-config")
    ],
    profiles=[
        VectorSearchProfile(name="my-vector-profile", algorithm_configuration_name="my-hnsw-config")
    ]
)

semantic_config = SemanticConfiguration(
    name="my-semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="title"),
        content_fields=[SemanticField(field_name="chunk")],
    )
)

semantic_search = SemanticSearch(configurations=[semantic_config])

index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search,
    semantic_search=semantic_search
)

index_client.create_or_update_index(index)
print(f"Index '{index_name}' created successfully.")



# ======================================================
# STEP 3: CREATE DATA SOURCE
# ======================================================
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataSourceConnection, SearchIndexerDataContainer
)

indexer_client = SearchIndexerClient(endpoint=ai_search_endpoint, credential=AzureKeyCredential(ai_search_key))

datasource = SearchIndexerDataSourceConnection(
    name=datasource_name,
    type="azureblob",
    connection_string=blob_storage_connection_string,
    container=SearchIndexerDataContainer(name=container_name)
)

indexer_client.create_or_update_data_source_connection(datasource)
print("Datasource created successfully.")



# ======================================================
# STEP 4: CREATE SKILLSET (CORRECTED)
# ======================================================
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    DocumentIntelligenceLayoutSkill,
    SplitSkill,
    MergeSkill,
    AzureOpenAIEmbeddingSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    AIServicesAccountKey
)

embedding_model_name = "text-embedding-3-small"
embedding_dimensions = 1536

# 1. Layout skill
layout_skill = DocumentIntelligenceLayoutSkill(
    name="layout-extractor",
    description="Extract structure (text, headings, tables, images)",
    context="/document",
    output_mode="oneToMany",
    markdown_header_depth="h3",
    inputs=[
        InputFieldMappingEntry(name="file_data", source="/document/file_data")
    ],
    outputs=[
        OutputFieldMappingEntry(name="markdown_document", target_name="markdownDocument"),
        OutputFieldMappingEntry(name="tables", target_name="tables"),
        OutputFieldMappingEntry(name="figures", target_name="figures")
    ]
)

# 2. Split skill
split_skill = SplitSkill(
    name="chunk-splitter",
    description="Split markdown into chunks",
    context="/document/markdownDocument/*",
    text_split_mode="pages",
    maximum_page_length=2000,
    page_overlap_length=500,
    inputs=[
        InputFieldMappingEntry(name="text", source="/document/markdownDocument/*/content")
    ],
    outputs=[
        OutputFieldMappingEntry(name="textItems", target_name="chunks")
    ]
)

# 3. Merge skill
merge_skill = MergeSkill(
    name="content-merger",
    description="Merge markdown into full text",
    context="/document",
    insert_pre_tag="",
    insert_post_tag="\n",
    inputs=[
        InputFieldMappingEntry(name="itemsToInsert", source="/document/markdownDocument/*/content")
    ],
    outputs=[
        OutputFieldMappingEntry(name="mergedText", target_name="content")
    ]
)

# 4. Embedding skill
embedding_skill = AzureOpenAIEmbeddingSkill(
    name="aoai-embedder",
    description="Generate embeddings",
    context="/document/markdownDocument/*/chunks/*",
    resource_url=openai_endpoint,
    deployment_name=emd_model,
    model_name=embedding_model_name,
    dimensions=embedding_dimensions,
    api_key=openai_key,
    inputs=[
        InputFieldMappingEntry(name="text", source="/document/markdownDocument/*/chunks/*")
    ],
    outputs=[
        OutputFieldMappingEntry(name="embedding", target_name="vector")
    ]
)

# 5. INDEX PROJECTION (fixed using parent_id)
index_projection = SearchIndexerIndexProjection(
    selectors=[
        SearchIndexerIndexProjectionSelector(
            target_index_name=index_name,
            parent_key_field_name="parent_id",
            source_context="/document/markdownDocument/*/chunks/*",
            mappings=[
                InputFieldMappingEntry(name="chunk",    source="/document/markdownDocument/*/chunks/*"),
                InputFieldMappingEntry(name="chunk_vector", source="/document/markdownDocument/*/chunks/*/vector"),
                InputFieldMappingEntry(name="title",    source="/document/metadata_storage_name"),
                InputFieldMappingEntry(name="tables",   source="/document/tables"),
                InputFieldMappingEntry(name="image_references", source="/document/figures"),
                InputFieldMappingEntry(name="metadata", source="/document/metadata_storage_path"),
                InputFieldMappingEntry(name="source_file", source="/document/metadata_storage_name"),
            ]
        )
    ],
    parameters=SearchIndexerIndexProjectionsParameters(
        projection_mode=IndexProjectionMode.INCLUDE_INDEXING_PARENT_DOCUMENTS
    )
)

skillset = SearchIndexerSkillset(
    name=skillset_name,
    description="Skillset to extract layout, chunk, embed",
    skills=[layout_skill, split_skill, merge_skill, embedding_skill],
    index_projection=index_projection,
    cognitive_services_account=AIServicesAccountKey(
        key=document_intelligence_key,
        subdomain_url=document_intelligence_endpoint
    )
)

indexer_client.create_or_update_skillset(skillset)
print(f"Skillset '{skillset_name}' created successfully.")




