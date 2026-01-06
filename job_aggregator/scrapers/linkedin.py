import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from LinkedIn.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
    
    Returns:
        List of job dictionaries with title, company, location, date_posted, apply_url
    """
    logger.info(f"LinkedIn scraper called with query={query}, days={days}")
    
    results = []
    base_url = "https://www.linkedin.com/jobs/search"
    
    # Prepare search parameters
    params = {
        'keywords': query,
        'f_TPR': f'r{days*86400}',  # Time filter in seconds
        'sortBy': 'DD'  # Sort by date
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='base-card')
        
        if not job_cards:
            job_cards = soup.find_all('li', class_='result-card')
        
        logger.info(f"Found {len(job_cards)} job cards from LinkedIn")
        
        for card in job_cards[:20]:  # Limit to 20 results
            try:
                # Extract job title
                title_elem = card.find('h3', class_='base-search-card__title') or card.find('a', class_='result-card__full-card-link')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('h4', class_='base-search-card__subtitle') or card.find('a', class_='result-card__subtitle-link')
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('span', class_='job-search-card__location')
                location = location_elem.get_text(strip=True) if location_elem else "Remote"
                
                # Extract apply URL
                link_elem = card.find('a', class_='base-card__full-link') or title_elem
                apply_url = link_elem.get('href', 'https://www.linkedin.com/jobs/') if link_elem else 'https://www.linkedin.com/jobs/'
                
                # Ensure full URL
                if apply_url and not apply_url.startswith('http'):
                    apply_url = 'https://www.linkedin.com' + apply_url
                
                # Date posted
                date_posted = datetime.now().strftime('%Y-%m-%d')
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': date_posted,
                    'apply_url': apply_url,
                    'source': 'LinkedIn'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from LinkedIn: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping LinkedIn: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping LinkedIn: {e}")
    
    return results
