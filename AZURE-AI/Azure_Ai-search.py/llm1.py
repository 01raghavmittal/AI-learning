
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
