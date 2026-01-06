import requests
import logging
from datetime import datetime
from typing import List, Dict
import os

logger = logging.getLogger(__name__)

def search_google_jobs(query: str, days: int = 7) -> List[Dict]:
    """Search for jobs using Google Custom Search API.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back (used for relevance)
    
    Returns:
        List of job dictionaries from search results
    """
    logger.info(f"Google Custom Search called with query={query}")
    
    # Google Custom Search API configuration
    api_key = os.environ.get('GOOGLE_API_KEY', '')
    search_engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID', '')
    
    if not api_key or not search_engine_id:
        logger.warning("Google API credentials not configured. Skipping web search.")
        return []
    
    results = []
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    # Enhance query to focus on job listings
    enhanced_query = f"{query} jobs apply hiring"
    
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': enhanced_query,
        'num': 10  # Max results per request
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        logger.info(f"Found {len(items)} results from Google Custom Search")
        
        for item in items:
            try:
                title = item.get('title', 'N/A')
                link = item.get('link', '')
                snippet = item.get('snippet', '')
                
                # Try to extract company name from snippet
                company = "N/A"
                if '-' in title:
                    parts = title.split('-')
                    if len(parts) >= 2:
                        company = parts[-1].strip()
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': 'Various',
                    'date_posted': datetime.now().strftime('%Y-%m-%d'),
                    'apply_url': link,
                    'source': 'Google Search',
                    'description': snippet[:200]  # First 200 chars
                })
                
            except Exception as e:
                logger.warning(f"Error parsing search result: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error during Google search: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during Google search: {e}")
    
    return results


def search_serpapi(query: str, days: int = 7) -> List[Dict]:
    """Search for jobs using SerpAPI (alternative to Google Custom Search).
    
    Args:
        query: Job search query
        days: Number of days to look back
    
    Returns:
        List of job dictionaries from search results
    """
    logger.info(f"SerpAPI called with query={query}")
    
    api_key = os.environ.get('SERPAPI_KEY', '')
    
    if not api_key:
        logger.warning("SerpAPI key not configured. Skipping.")
        return []
    
    results = []
    search_url = "https://serpapi.com/search"
    
    params = {
        'api_key': api_key,
        'engine': 'google_jobs',
        'q': query,
        'hl': 'en'
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        jobs = data.get('jobs_results', [])
        logger.info(f"Found {len(jobs)} jobs from SerpAPI")
        
        for job in jobs[:20]:
            try:
                results.append({
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company_name', 'N/A'),
                    'location': job.get('location', 'Remote'),
                    'date_posted': job.get('detected_extensions', {}).get('posted_at', datetime.now().strftime('%Y-%m-%d')),
                    'apply_url': job.get('share_link', job.get('link', '')),
                    'source': 'SerpAPI (Google Jobs)',
                    'description': job.get('description', '')[:200]
                })
                
            except Exception as e:
                logger.warning(f"Error parsing SerpAPI result: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error during SerpAPI search: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during SerpAPI search: {e}")
    
    return results


def fallback_search(query: str, days: int = 7) -> List[Dict]:
    """Fallback search that tries multiple search engines.
    
    Args:
        query: Job search query
        days: Number of days to look back
    
    Returns:
        Combined results from available search engines
    """
    results = []
    
    # Try SerpAPI first (has dedicated jobs engine)
    serpapi_results = search_serpapi(query, days)
    if serpapi_results:
        results.extend(serpapi_results)
        return results
    
    # Fall back to Google Custom Search
    google_results = search_google_jobs(query, days)
    if google_results:
        results.extend(google_results)
        return results
    
    logger.warning("All search engine fallbacks failed or not configured.")
    return results
