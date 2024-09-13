from promptflow.core import tool

@tool
def combine_results(
    summarized_papers: list,
    classified_papers: list,
) -> list:
    summaries_dict = {paper['id']: paper for paper in summarized_papers}
    combined_papers = []

    for paper in classified_papers:
        paper_id = paper['id']
        combined_paper = paper.copy()

        if paper_id in summaries_dict:
            combined_paper['summary_text'] = summaries_dict[paper_id].get('summary_text', '')
        else:
            combined_paper['summary_text'] = ''
        combined_papers.append(combined_paper)

    return combined_papers
