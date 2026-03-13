from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    SemanticConfiguration, SemanticField, SemanticPrioritizedFields, SemanticSearch,
    AzureOpenAIVectorizerParameters
)

from config import ai_search_endpoint,ai_search_key,index_name,

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
    ],vectorizers=[  
         AzureOpenAIVectorizer(  
             vectorizer_name="myOpenAI",  
             kind="azureOpenAI",  
             parameters=AzureOpenAIVectorizerParameters(  
                 resource_url=AZURE_OPENAI_AI,  
                 deployment_name="text-embedding-3-large",
                 model_name="text-embedding-3-large"
             ),
         ),  
     ], 
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
