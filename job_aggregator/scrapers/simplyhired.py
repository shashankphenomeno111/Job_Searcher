import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from SimplyHired.
    
    Args:
        query: Job search query
        days: Number of days to look back
        experience: Experience level filter
    
    Returns:
        List of job dictionaries
    """
    logger.info(f"SimplyHired scraper called with query={query}")
    
    results = []
    search_url = f"https://www.simplyhired.com/search?q={query.replace(' ', '+')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_cards = soup.find_all('div', attrs={'data-testid': 'searchSerpJob'})
        
        if not job_cards:
            job_cards = soup.find_all('article', class_='JobPosting')
        
        logger.info(f"Found {len(job_cards)} job cards from SimplyHired")
        
        for card in job_cards[:20]:
            try:
                title_elem = card.find('a', attrs={'data-testid': 'job-link'}) or card.find('h2')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                company_elem = card.find('span', attrs={'data-testid': 'companyName'})
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                location_elem = card.find('span', attrs={'data-testid': 'searchLocation'})
                location = location_elem.get_text(strip=True) if location_elem else "Various"
                
                link_elem = title_elem
                apply_url = link_elem.get('href', '') if link_elem else ''
                if apply_url and not apply_url.startswith('http'):
                    apply_url = 'https://www.simplyhired.com' + apply_url
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': datetime.now().strftime('%Y-%m-%d'),
                    'apply_url': apply_url if apply_url else 'https://www.simplyhired.com',
                    'source': 'SimplyHired'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing SimplyHired job: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error scraping SimplyHired: {e}")
    
    return results
