from ddgs import DDGS
import trafilatura
from core.utils.logger import get_logger

logger = get_logger(__name__)

def search_web(query, max_results=3):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if not results: return "No results found."
            
            summary = ""
            for i, res in enumerate(results):
                summary += f"[{i+1}] Title: {res['title']}\nSnippet: {res['body']}\nURL: {res['href']}\n\n"
            return summary
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Error: {e}"

def fetch_page_content(url):
    import requests
    from trafilatura import extract
    try:
        # Додаємо заголовки, щоб сайт не блокував нас
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        text = extract(response.text)
        
        if not text or len(text) < 100:
            return "This page seems empty or blocked. Try another source."
            
        return text[:4000]
    except Exception as e:
        return f"Failed to load page: {e}"