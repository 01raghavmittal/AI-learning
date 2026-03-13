from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
    SearchIndexerDataSourceConnection, SearchIndexerDataContainer
)

from config import ai_search_endpoint,ai_search_key,datasource_name,blob_storage_connection_string,container_name

indexer_client = SearchIndexerClient(endpoint=ai_search_endpoint, credential=AzureKeyCredential(ai_search_key))

datasource = SearchIndexerDataSourceConnection(
    name=datasource_name,
    type="azureblob",
    connection_string=blob_storage_connection_string,
    container=SearchIndexerDataContainer(name=container_name)
)

indexer_client.create_or_update_data_source_connection(datasource)
print("Datasource created successfully.")