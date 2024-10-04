import requests
from typing import List
from typing import Union
from promptflow.core import tool
from promptflow.contracts.multimedia import Image as PFImage
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from utils import is_valid

@tool
def vectorize_query(query: str, connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]) -> List[float]:
    try:
        openai = get_client(connection)
        response = openai.embeddings.create(model="text-embedding-3-small", input=query)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return []

def get_client(connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]):
    conn = dict(connection)
    api_key = conn.get("api_key")
    if api_key.startswith("sk-"):
        from openai import OpenAI as Client
    else:
        from openai import AzureOpenAI as Client
        connection_dict = dict(connection)
        conn = dict(
            api_key=api_key,
        )
        conn.update(
            azure_endpoint=connection_dict.get("api_base"),
            api_version=connection_dict.get("api_version", "2023-07-01-preview"),
        )
    return Client(**conn)