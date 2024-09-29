import time
from promptflow.core import tool
import requests
import xml.etree.ElementTree as ET

@tool
def fetch_and_parse_arxiv_papers(search_query: str, date: str = None, start: int = 0, max_results: int = 10, retries: int = 3, backoff_factor: float = 1.0) -> list:
    """
    Fetches papers from the arXiv API based on the search query and parses the response with retry mechanism.

    Args:
        search_query (str): The search query for the arXiv API.
        date (str): The date to restrict the search to, in 'YYYY-MM-DD' format.
        start (int): The starting index of results.
        max_results (int): The maximum number of results to fetch.
        retries (int): Number of retry attempts in case of failure.
        backoff_factor (float): The factor to multiply the wait time after each retry.

    Returns:
        list: A list of dictionaries containing paper details.
    """
    base_query = search_query

    if date:
        date_formatted = date.replace('-', '')
        date_range = f"submittedDate:[{date_formatted}000000 TO {date_formatted}235959]"
        query = f"({base_query}) AND {date_range}"
    else:
        query = base_query

    api_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results
    }

    attempt = 0
    while attempt <= retries:
        try:
            response = requests.get(api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                namespace = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }

                papers = []
                for entry in root.findall('atom:entry', namespace):
                    paper = {}
                    paper['id'] = entry.find('atom:id', namespace).text
                    paper['title'] = entry.find('atom:title', namespace).text.strip()
                    paper['summary'] = entry.find('atom:summary', namespace).text.strip()
                    paper['published'] = entry.find('atom:published', namespace).text

                    authors = entry.findall('atom:author', namespace)
                    paper['authors'] = [author.find('atom:name', namespace).text for author in authors]

                    papers.append(paper)
                return papers
            else:
                raise Exception(f"Failed to fetch data from arXiv API. Status code: {response.status_code}")

        except (requests.ConnectionError, requests.Timeout) as e:
            attempt += 1
            if attempt > retries:
                raise Exception(f"Failed to fetch data from arXiv API after {retries} attempts. Last error: {str(e)}")
            wait_time = backoff_factor * (2 ** (attempt - 1))
            print(f"Attempt {attempt} failed. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    raise Exception("Unexpected error occurred while fetching data from arXiv API")
