import os
import requests
from typing import List
from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
    QueryType,
    QueryCaptionType,
    QueryAnswerType,
)
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import CognitiveSearchConnection

@tool
def do_search(
    question: str,
    index_name: str,
    search: CognitiveSearchConnection,
) -> str:
    search_client = SearchClient(
        endpoint=search.configs["api_base"],
        index_name=index_name,
        credential=AzureKeyCredential(search.secrets["api_key"]),
    )

    results = search_client.search(  
        top=5,
        search_text=question,  
        vector_queries=None,
        select=["description", "name", "category", "price"],
    )  
    
    docs = [
        {
            "name": doc["name"],
            "category": doc["category"],
            "price": doc["price"],
            "description": doc["description"],
            "score": doc["@search.score"]
        }
        for doc in results
    ]

    return docs