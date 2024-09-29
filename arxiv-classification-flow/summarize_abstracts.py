import os
from promptflow.core import tool
from dotenv import load_dotenv
from typing import Union
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection

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

@tool
def summarize_abstracts(
    papers: list,
    deployment_name: str,
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection] = None,
) -> list:
    if not papers:
        raise ValueError("No papers provided.")

    openai = get_client(connection)

    enriched_papers = []
    for paper in papers:
        abstract = paper.get('summary', '')
        if not abstract:
            summary_text = "No abstract available."
        else:
            prompt = f"Summarize the following abstract in simple terms. Use 2 sentences maximum. Take a third person point of view.\n\nABSTRACT:\n{abstract}"

        response = openai.chat.completions.create(   
            model=deployment_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        summary_text = response.choices[0].message.content
        
        enriched_paper = paper.copy()
        enriched_paper['summary_text'] = summary_text
        enriched_papers.append(enriched_paper)

    return enriched_papers
