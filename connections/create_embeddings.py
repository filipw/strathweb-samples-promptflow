import json
import os
import openai

filename = "../rag-chat/data/metadata_structured.json"
with open(filename, "r") as file:
    metadata = json.load(file)

AZURE_OPENAI_KEY = os.environ["EMBEDDINGS_AZURE_OPENAI_KEY"]
AZURE_OPENAI_RESOURCE = os.environ["EMBEDDINGS_AZURE_OPENAI_RESOURCE"]
API_VERSION = os.getenv("EMBEDDINGS_AZURE_OPENAI_API_VERSION") or "2024-08-01-preview"

openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_KEY
openai.azure_endpoint = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
openai.api_version = API_VERSION

embedding_model = "text-embedding-3-small"

def get_description_vector(description: str):
    response = openai.embeddings.create(model=embedding_model, input=description)
    return response.data[0].embedding

for item in metadata:
    description = item.get("description")
    if description:
        print(f"Generating description vector for {item['name']}...")
        item["description_vector"] = get_description_vector(description)

with open(filename, "w") as file:
    json.dump(metadata, file, indent=4)

print("Metadata has been updated with description vectors.")
