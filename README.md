# Promptflow samples

## Getting started

Create a Python environment with the required dependencies. You can use `conda` or `venv` to create a new environment. Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Connections are defined in [create_connections.py](./create_connections.py) and must be created before running the samples.

```python
python ./connections/create_connections.py
```

## Overview

| Sample Name | Description | 
|-------------|-------------|
| 💻 [Basic Local](./basic-local/) | 📝 A simple single-step flow utilizing a local connection (a model running on the local HTTP endpoint) |
| 💻 [Basic o3](./basic-o3/) | 📝 A simple single-step flow showing how to use a reasoning model (not supported by PF directly yet) and how to switch between Azure OpenAI/OpenAI/Local models |
| 💻 [Arxiv Classification](./arxiv-classification-flow/) | 📝 Multi-step flow, fetching, classifying and generating a digest of Arxiv papers. |
| 💻 [RAG Chat](./rag-chat/) | 📝 A multi step RAG, including LLM-based query extraction, Python tool integration and performing look up in Azure AI Search via vector search |
| 💻 [Vision Chat](./rag-chat/) | 📝 A multi step RAG, including image vectorization in Azure Computer Vision API and image-based search in Azure AI Search |