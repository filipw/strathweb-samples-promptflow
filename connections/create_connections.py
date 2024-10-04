import os
from pathlib import Path

from promptflow.client import PFClient
from promptflow.entities import (
    AzureOpenAIConnection,
    OpenAIConnection,
    CustomConnection,
    CognitiveSearchConnection,
)
from dotenv import load_dotenv

load_dotenv()

pf = PFClient()

AZURE_OPENAI_KEY= os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_RESOURCE= os.environ["AZURE_OPENAI_RESOURCE"]
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-08-01-preview"
connection = AzureOpenAIConnection(
    name="open_ai_connection",
    api_key=AZURE_OPENAI_KEY,
    api_base=f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/",
    api_type="azure",
    api_version=API_VERSION,
)

print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)

# for an LM Studio host running at port 1234
local_connection = OpenAIConnection(
    name="local_open_ai_connection",
    api_key="sk-local",
    base_url="http://localhost:1234/v1",
)

print(f"Creating connection {local_connection.name}...")
result = pf.connections.create_or_update(local_connection)
print(result)

EMBEDDINGS_AZURE_OPENAI_KEY= os.environ["EMBEDDINGS_AZURE_OPENAI_KEY"]
EMBEDDINGS_AZURE_OPENAI_RESOURCE= os.environ["EMBEDDINGS_AZURE_OPENAI_RESOURCE"]
EMBEDDINGS_API_VERSION = os.getenv("EMBEDDINGS_API_VERSION") or "2024-08-01-preview"
embeddings_connection = AzureOpenAIConnection(
    name="embeddings_open_ai_connection",
    api_key=EMBEDDINGS_AZURE_OPENAI_KEY,
    api_base=f"https://{EMBEDDINGS_AZURE_OPENAI_RESOURCE}.openai.azure.com/",
    api_type="azure",
    api_version=EMBEDDINGS_API_VERSION,
)

print(f"Creating connection {embeddings_connection.name}...")
result = pf.connections.create_or_update(embeddings_connection)
print(result)

AZURE_AI_SEARCH_ENDPOINT = os.environ["AZURE_AI_SEARCH_ENDPOINT"]
AZURE_AI_SEARCH_KEY = os.environ["AZURE_AI_SEARCH_KEY"]
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-03-01-preview"
connection = CognitiveSearchConnection(
    name="ai_search_connection",
    api_key=AZURE_AI_SEARCH_KEY,
    api_base=AZURE_AI_SEARCH_ENDPOINT,
    api_version=API_VERSION,
)

print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)

AZURE_VISION_ENDPOINT = os.environ["AZURE_VISION_ENDPOINT"]
AZURE_VISION_KEY = os.environ["AZURE_VISION_KEY"]
connection = CustomConnection(
    name="vision_connection",
    configs={"api_base": AZURE_VISION_ENDPOINT},
    secrets={"api_key": AZURE_VISION_KEY},
)
print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)