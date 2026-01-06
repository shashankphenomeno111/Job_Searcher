import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Monster.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
        experience: Experience level filter
    
    Returns:
        List of job dictionaries
    """
    logger.info(f"Monster scraper called with query={query}, days={days}")
    
    results = []
    base_url = "https://www.monster.com/jobs/search"
    
    # Format query for URL
    query_formatted = query.replace(' ', '-').lower()
    search_url = f"https://www.monster.com/jobs/search?q={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='card-content')
        
        if not job_cards:
            job_cards = soup.find_all('article', class_='job-card')
        
        logger.info(f"Found {len(job_cards)} job cards from Monster")
        
        for card in job_cards[:20]:
            try:
                # Extract job title
                title_elem = card.find('h2', class_='title') or card.find('a', class_='job-title')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('div', class_='company') or card.find('span', class_='company-name')
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('div', class_='location')
                location = location_elem.get_text(strip=True) if location_elem else "Various"
                
                # Extract apply URL
                link_elem = title_elem if title_elem and title_elem.name == 'a' else card.find('a')
                if link_elem:
                    apply_url = link_elem.get('href', '')
                    if apply_url and not apply_url.startswith('http'):
                        apply_url = 'https://www.monster.com' + apply_url
                else:
                    apply_url = 'https://www.monster.com'
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': datetime.now().strftime('%Y-%m-%d'),
                    'apply_url': apply_url,
                    'source': 'Monster'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from Monster: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping Monster: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping Monster: {e}")
    
    return results
