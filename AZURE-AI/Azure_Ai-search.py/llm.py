
# create_skillset.py (Basic)
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset, SearchIndexerSkill,
    InputFieldMappingEntry, OutputFieldMappingEntry
)
from config import SEARCH_ENDPOINT, SEARCH_KEY, SKILLSET_NAME

client = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

skillset = SearchIndexerSkillset(
    name=SKILLSET_NAME,
    skills=[
        # Built-in extraction
        SearchIndexerSkill(
            name="documentExtraction",
            description="Extract text from PDFs",
            skill_type="DocumentExtractionSkill",
            inputs=[InputFieldMappingEntry(name="document", source="/document")],
            outputs=[OutputFieldMappingEntry(name="text", target_name="content")]
        ),
        # Chunking (simple)
        SearchIndexerSkill(
            name="textSplit",
            description="Split content into chunks",
            skill_type="TextSplitSkill",
            inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
            outputs=[OutputFieldMappingEntry(name="chunks", target_name="content")]
        )
    ]
)

client.create_or_update_skillset(skillset)
print("Skillset created:", SKILLSET_NAME)
``
