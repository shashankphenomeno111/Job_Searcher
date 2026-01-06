import importlib
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of scraper module names (they must exist in the scrapers package)
SCRAPER_MODULES = [
    "scrapers.indeed",
    "scrapers.linkedin",
    "scrapers.glassdoor",
    "scrapers.naukri",
    "scrapers.monster",
    "scrapers.simplyhired",
    "scrapers.angellist",
    "scrapers.internshala",
]

def _load_scraper(module_name: str):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, "scrape")
    except Exception as e:
        logger.error(f"Failed to load scraper {module_name}: {e}")
        return None

def _fallback_search(query: str, days: int) -> List[Dict]:
    """Fallback to web search engines when scrapers fail or return no results.
    Uses Google Custom Search API or SerpAPI if configured.
    """
    logger.info("Fallback search invoked – trying web search engines.")
    try:
        from search_engine import fallback_search
        return fallback_search(query, days)
    except Exception as e:
        logger.error(f"Search engine fallback failed: {e}")
        return []

def search_jobs(query: str, days: int = 7, experience: str = "all", location: str = "India", platforms: List[str] = None) -> List[Dict]:
    """Aggregate job listings from selected scrapers.

    Args:
        query: Job title or keywords, e.g. "Java Developer".
        days:  Number of days to look back for postings.
        experience: Experience level filter ("fresher", "experienced", "all").
        location: Location filter (e.g., "India", "Bangalore").
        platforms: List of platforms to search (e.g., ['indeed', 'linkedin']).

    Returns:
        A list of dictionaries with keys: title, company, location,
        date_posted, apply_url.
    """
    # Default to all platforms if none specified
    if platforms is None:
        platforms = ['indeed', 'linkedin', 'glassdoor', 'naukri', 'monster', 'simplyhired', 'angellist', 'internshala']
    
    # Map platform names to scraper modules
    platform_map = {
        'indeed': 'scrapers.indeed',
        'linkedin': 'scrapers.linkedin',
        'glassdoor': 'scrapers.glassdoor',
        'naukri': 'scrapers.naukri',
        'monster': 'scrapers.monster',
        'simplyhired': 'scrapers.simplyhired',
        'angellist': 'scrapers.angellist',
        'internshala': 'scrapers.internshala',
    }
    
    # Filter to only selected platforms
    selected_modules = [platform_map[p] for p in platforms if p in platform_map]
    results: List[Dict] = []
    for module_name in selected_modules:
        scrape_fn = _load_scraper(module_name)
        if scrape_fn:
            try:
                # Try to pass all parameters, fallback if not supported
                try:
                    scraper_results = scrape_fn(query, days, experience, location)
                except TypeError:
                    try:
                        scraper_results = scrape_fn(query, days, experience)
                    except TypeError:
                        scraper_results = scrape_fn(query, days)
                if scraper_results:
                    results.extend(scraper_results)
            except Exception as e:
                logger.error(f"Error while scraping {module_name}: {e}")
    if not results:
        # If all scrapers failed or returned nothing, use fallback
        results = _fallback_search(query, days)
    # De‑duplicate by apply_url
    unique = {item["apply_url"]: item for item in results if "apply_url" in item}
    return list(unique.values())
