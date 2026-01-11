
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


# step 2: create index

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    # Index & fields
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    # Vector search configuration
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    # Optional exhaustive KNN (use for evaluation or ground-truth checks)
    ExhaustiveKnnAlgorithmConfiguration,
    # Semantic search configuration
    SemanticConfiguration, SemanticField, SemanticPrioritizedFields, SemanticSearch,
    # (Optional) built-in permission filters (requires preview SDK >= 11.6.0b12)
    PermissionFilter, SearchIndexPermissionFilterOption,
)

# ---- Connection
index_client  = SearchIndexClient(endpoint=ai_search_endpoint, credential=AzureKeyCredential(ai_search_key))

# ---- Fields
fields = [
    # Key
    SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True,analyzer_name="keyword"),
    SimpleField(name="parent_id", type=SearchFieldDataType.String, filterable=True),

    # Metadata & chunking
    SearchField(name="chunk_id",    type=SearchFieldDataType.String,  searchable=False, filterable=True),
    SearchField(name="source_file", type=SearchFieldDataType.String,  searchable=False, filterable=True),
    SearchField(name="page_number", type=SearchFieldDataType.Int32,   searchable=False, filterable=True),

    # Text
    SearchField(name="title",    type=SearchFieldDataType.String, searchable=True, filterable=True, sortable=True),
    SearchField(name="chunk",    type=SearchFieldDataType.String, searchable=True, filterable=False),
    SearchField(name="metadata", type=SearchFieldDataType.String, searchable=True, filterable=False),

    # Optional extra metadata (ensure these exist in your ingestion payload if you keep them)
    SearchableField(name="metadata_storage",        type=SearchFieldDataType.String, searchable=True, filterable=False),
    SearchableField(name="metadata_content_type",   type=SearchFieldDataType.String, searchable=True, filterable=False),
    SearchableField(name="metadata_storage_path",   type=SearchFieldDataType.String, searchable=True, filterable=True),

    # Vector (Float32 = Collection(Edm.Single)) — 1536 for ada-002/3-small, 3072 for 3-large
    SearchField(
        name="chunk_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,                        # adjust to your embedding model
        vector_search_profile_name="my-vector-profile",
        filterable=False,
        sortable=False,
        # stored=False,  # uncomment to reduce index size if you never return raw vectors
    ),

    SearchField(name="tables", type=SearchFieldDataType.Collection(SearchFieldDataType.String), searchable=False, filterable=False),
    SearchField(name="image_references", type=SearchFieldDataType.Collection(SearchFieldDataType.String), searchable=False, filterable=False),

    # Permission filters (preview)
    SearchField(
        name="groups",
        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
        filterable=True,
        permission_filter=PermissionFilter.GROUP_IDS
    ),
    SearchField(
        name="oids",
        type=SearchFieldDataType.Collection(SearchFieldDataType.String),
        filterable=True,
        permission_filter=PermissionFilter.USER_IDS
    ),
]

# ---- Vector search configuration
vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="my-hnsw-config"),# HNSW for fast ANN search
        ExhaustiveKnnAlgorithmConfiguration(name="my-exhaustive-config") # exhaustive KNN (brute-force) for evaluation/ground truth comparison
    ],
    profiles=[
        VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-hnsw-config"
        )
    ]
)


# ---- Semantic configuration (use your actual field names)
semantic_config = SemanticConfiguration(
    name="my-semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="title"),
        content_fields=[
            SemanticField(field_name="chunk"),
            SemanticField(field_name="metadata")
        ],
        keywords_fields=[
            SemanticField(field_name="source_file")
        ]
    )
)
semantic_search = SemanticSearch(configurations=[semantic_config])

# ---- Build the index (single definition)
index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search,
    semantic_search=semantic_search,
    # Enable built-in permission filtering at the index level (PREVIEW SDK required)
    # permission_filter_option=SearchIndexPermissionFilterOption.ENABLED
)


result = index_client.create_or_update_index(index)
print(f"Index '{result.name}' is ready.")






from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataSourceConnection,
    SearchIndexerDataContainer
)

indexer_client = SearchIndexerClient(endpoint=ai_search_endpoint, credential=AzureKeyCredential(ai_search_key))

datasource = SearchIndexerDataSourceConnection(
    name=datasource_name,
    type="azureblob",
    connection_string=blob_storage_connection_string,
    container=SearchIndexerDataContainer(name=container_name)
)

indexer_client.create_or_update_data_source_connection(datasource)
print('datasource is created successfully')




# STEP 4: CREATE SKILLSET (Document Intelligence → Chunking → Embeddings)

# STEP 4: CREATE CORRECTED SKILLSET (Document Intelligence → Chunking → Embeddings)

from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    DocumentIntelligenceLayoutSkill,
    SplitSkill,
    AzureOpenAIEmbeddingSkill,
    MergeSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    AIServicesAccountKey,
    AIServicesAccountIdentity
)

# ---------------------------------------------
# MODEL CONFIG
# ---------------------------------------------
embedding_model_name = "text-embedding-3-small"
embedding_dimensions = 1536

# ---------------------------------------------
# SKILL 1 — Document Intelligence Layout Skill
# Extracts text, structure, tables, images, headings
# ---------------------------------------------
layout_skill = DocumentIntelligenceLayoutSkill(
    name="layout-extractor",
    description="Extract full document structure (text, headings, tables, images)",
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

# ---------------------------------------------
# SKILL 2 — Chunking with SplitSkill
# Semantic markdown + fixed-length pages
# ---------------------------------------------
split_skill = SplitSkill(
    name="chunk-splitter",
    description="Split markdown into overlapping chunks",
    context="/document/markdownDocument/*",
    text_split_mode="pages",
    maximum_page_length=2000,
    page_overlap_length=500,
    inputs=[
        InputFieldMappingEntry(
            name="text",
            source="/document/markdownDocument/*/content"
        )
    ],
    outputs=[
        OutputFieldMappingEntry(name="textItems", target_name="chunks")
    ]
)

# ---------------------------------------------
# SKILL 3 — Merge full text (Optional fallback)
# ---------------------------------------------
merge_skill = MergeSkill(
    name="content-merger",
    description="Merge markdown content for fallback",
    context="/document",
    insert_pre_tag="",
    insert_post_tag="\n",
    inputs=[
        InputFieldMappingEntry(
            name="itemsToInsert",
            source="/document/markdownDocument/*/content"
        )
    ],
    outputs=[
        OutputFieldMappingEntry(name="mergedText", target_name="content")
    ]
)

# ---------------------------------------------
# SKILL 4 — Embedding Skill
# Uses Azure OpenAI to embed each chunk
# ---------------------------------------------
embedding_skill = AzureOpenAIEmbeddingSkill(
    name="aoai-embedder",
    description="Generate embeddings using Azure OpenAI",
    context="/document/markdownDocument/*/chunks/*",
    resource_url=openai_endpoint,
    deployment_name=emd_model,
    model_name=embedding_model_name,
    dimensions=embedding_dimensions,
    api_key=openai_key,
    inputs=[
        InputFieldMappingEntry(
            name="text",
            source="/document/markdownDocument/*/chunks/*"
        )
    ],
    outputs=[
        OutputFieldMappingEntry(name="embedding", target_name="vector")
    ]
)

# ------------------------------------------------------------
# INDEX PROJECTION (CORRECTED)
# Uses `parent_id` (NOT the key field)
# ------------------------------------------------------------
index_projection = SearchIndexerIndexProjection(
    selectors=[
        SearchIndexerIndexProjectionSelector(
            target_index_name=index_name,
            parent_key_field_name="parent_id",     # IMPORTANT: corrected
            source_context="/document/markdownDocument/*/chunks/*",
            mappings=[
                InputFieldMappingEntry(name="chunk", source="/document/markdownDocument/*/chunks/*"),
                InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),
                InputFieldMappingEntry(name="chunk_vector", source="/document/markdownDocument/*/chunks/*/vector"),
                InputFieldMappingEntry(name="tables", source="/document/tables"),
                InputFieldMappingEntry(name="image_references", source="/document/figures"),
                InputFieldMappingEntry(name="metadata", source="/document/metadata_storage_path"),
                InputFieldMappingEntry(name="source_file", source="/document/metadata_storage_name")
            ]
        )
    ],
    parameters=SearchIndexerIndexProjectionsParameters(
        projection_mode=IndexProjectionMode.INCLUDE_INDEXING_PARENT_DOCUMENTS
    )
)

# ------------------------------------------------------------
# FINAL SKILLSET OBJECT
# ------------------------------------------------------------
skillset = SearchIndexerSkillset(
    name=skillset_name,
    description="Skillset to extract layout, chunk content, and embed",
    skills=[layout_skill, split_skill, merge_skill, embedding_skill],
    index_projection=index_projection,
    cognitive_services_account=AIServicesAccountKey(
        key=document_intelligence_key,
        subdomain_url=document_intelligence_endpoint
    )
)

indexer_client.create_or_update_skillset(skillset)
print(f"Skillset '{skillset_name}' created successfully with corrected parent_id.")
