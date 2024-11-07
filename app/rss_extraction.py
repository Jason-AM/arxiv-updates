import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from ratelimit import limits, sleep_and_retry
from gemini_call import gemini_request

#TODO clean up the following function - its ugly
@sleep_and_retry
@limits(calls=1, period=3)
def get_title_link_abs_from_rss(topic: str):

    # Define your query parameters
    query = f"cat:{topic}"  # Example category: Computer Science - Artificial Intelligence
    start_date = "2024-11-05"  # Start date (YYYY-MM-DD)
    end_date = "2024-11-07"  # End date (YYYY-MM-DD)
    max_results = 50  # Number of results to retrieve

    # Construct the API URL
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    # Make the request
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the XML response
    root = ET.fromstring(response.content)

    # Define a function to convert arXiv's timestamp format to datetime
    def parse_arxiv_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    # Filter entries by date
    titles_and_links = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        published_date = parse_arxiv_date(entry.find("{http://www.w3.org/2005/Atom}published").text)
        if start_date <= published_date.strftime("%Y-%m-%d"): # <= end_date:
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            link = entry.find("{http://www.w3.org/2005/Atom}id").text

            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            summary = gemini_request(
                f"""Please provide a very simple summary of this abstract and try explain why this is useful
                Abstract {summary}
                """
            )
            if summary:
                summary = summary['candidates'][0]['content']['parts'][0]['text']
                titles_and_links.append((title, link, summary))

    return set(titles_and_links)

