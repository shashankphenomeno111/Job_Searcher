import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Internshala (for freshers/internships in India).
    
    Args:
        query: Job search query
        days: Number of days to look back
        experience: Experience level filter
    
    Returns:
        List of job dictionaries
    """
    logger.info(f"Internshala scraper called with query={query}")
    
    results = []
    # Internshala has both internships and jobs
    search_url = f"https://internshala.com/jobs/{query.lower().replace(' ', '-')}-jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_cards = soup.find_all('div', class_='individual_internship')
        
        if not job_cards:
            job_cards = soup.find_all('div', class_='internship_meta')
        
        logger.info(f"Found {len(job_cards)} listings from Internshala")
        
        for card in job_cards[:20]:
            try:
                title_elem = card.find('h3', class_='job-internship-name') or card.find('a', class_='view_detail_button')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                company_elem = card.find('p', class_='company-name') or card.find('a', class_='link_display_like_text')
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                location_elem = card.find('div', class_='locations')
                location = location_elem.get_text(strip=True) if location_elem else "Work from Home"
                
                link_elem = card.find('a', class_='view_detail_button')
                apply_url = link_elem.get('href', '') if link_elem else ''
                if apply_url and not apply_url.startswith('http'):
                    apply_url = 'https://internshala.com' + apply_url
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': datetime.now().strftime('%Y-%m-%d'),
                    'apply_url': apply_url if apply_url else 'https://internshala.com',
                    'source': 'Internshala'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing Internshala listing: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error scraping Internshala: {e}")
    
    return results
