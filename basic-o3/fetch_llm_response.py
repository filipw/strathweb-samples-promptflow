from openai import AzureOpenAI
from typing import Union
from promptflow.core import tool
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
            api_version="2025-01-01-preview",
        )
    return Client(**conn)

@tool
def fetch_llm_response(question: str, deployment_name: str, connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection] = None) -> str:
    client = get_client(connection)

    prompt = "You are a math expert. Answer the user's question in detail."

    response = client.chat.completions.create(
        messages=[
                    {"role": "developer", "content": prompt},
                    {"role": "user", "content": question}
                ],
        max_completion_tokens=5000,
        model=deployment_name,
        reasoning_effort="low"
    )

    txt = response.choices[0].message.content
    return txt