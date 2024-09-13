import os
from promptflow.core import tool
from dotenv import load_dotenv
from typing import Union
from promptflow.connections import CustomConnection, AzureOpenAIConnection

def to_bool(value) -> bool:
    return str(value).lower() == "true"

def get_client(connection: Union[CustomConnection, AzureOpenAIConnection]):
    connection_dict = dict(connection)
    api_key = connection_dict.get("api_key")
    conn = dict(
        api_key=api_key,
    )
    if api_key.startswith("sk-"):
        from openai import OpenAI as Client
    else:
        from openai import AzureOpenAI as Client
        conn.update(
            azure_endpoint=connection_dict.get("api_base"),
            api_version=connection_dict.get("api_version", "2023-07-01-preview"),
        )
    return Client(**conn)

@tool
def classify_papers(
    papers: list,
    deployment_name: str,
    categories: list,
    connection: Union[CustomConnection, AzureOpenAIConnection] = None,
) -> list:
    if not papers:
        raise ValueError("No papers provided.")

    # Initialize OpenAI client
    openai = get_client(connection)

    classified_papers = []
    for paper in papers:
        abstract = paper.get('summary', '')
        if not abstract:
            classification = "Unknown"
        else:
            prompt = f"""Based on the following abstract, classify the paper into one of the following subfields:
            {", ".join(categories)}

            Abstract:
            {abstract}

            Please provide only the subfield name."""


            response = openai.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            classification = response.choices[0].message.content.strip()

        # Add the classification to the paper
        classified_paper = paper.copy()
        classified_paper['classification'] = classification
        classified_papers.append(classified_paper)

    return classified_papers
