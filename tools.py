from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search(query: str) -> str:
    """Search the web for recent information on a topic. Returns titles, URLs and brief snippets."""
    try:
        # max_results=3 (was 5) — saves ~40% of Tavily credits and reduces tokens sent to LLM
        results = tavily.search(query=query, max_results=3)
        out = []
        for r in results.get('results', []):
            # Snippet capped at 150 chars (was 300) — keeps context tight
            out.append(
                f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('content', '')[:150]}"
            )
        return "\n---\n".join(out) if out else "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool
def scrape_url(url: str) -> str:
    """Scrape clean text from a URL for deeper reading."""
    import re
    url = url.strip().strip("'\"<>")
    match = re.search(r'https?://[^\s\)\"\']+', url)
    if match:
        url = match.group(0)
    elif not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Try requests + BeautifulSoup FIRST (free, no API credit used)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        }
        resp = requests.get(url, timeout=6, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            if text and len(text.strip()) > 100:
                # Return only 1200 chars (was 2000/2500) — saves tokens
                return text[:1200]
    except Exception:
        pass

    # Fallback: Tavily extract (uses API credit — only if BS4 failed)
    try:
        res = tavily.extract(urls=[url])
        if res and 'results' in res and res['results']:
            raw = res['results'][0].get('raw_content', '')
            if raw and len(raw.strip()) > 50:
                return raw[:1200]
    except Exception:
        pass

    return f"Could not scrape content from {url}."