



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
    SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),

    # Metadata & chunking
    # SearchField(name="chunk_id",    type=SearchFieldDataType.String,  searchable=False, filterable=True),
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






#-----------------------------
data_source = SearchIndexerDataSourceConnection(
    name=datasource_name,
    type="azureblob",
    connection_string=blob_storage_connection_string,
    container=SearchIndexerDataContainer(name=container_name),
)
print("Data source created:", datasource_name)


#------------------------------------------

