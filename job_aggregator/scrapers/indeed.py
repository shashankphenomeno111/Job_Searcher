import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Indeed.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
        experience: Experience level filter
        location: Location filter (e.g., "India")
    
    Returns:
        List of job dictionaries with title, company, location, date_posted, apply_url
    """
    logger.info(f"Indeed scraper called with query={query}, days={days}, location={location}")
    
    results = []
    base_url = "https://www.indeed.com/jobs"
    
    # Prepare search parameters
    params = {
        'q': query,
        'l': location,  # Location parameter
        'fromage': str(days),  # Filter by days
        'sort': 'date'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.indeed.com/',
    }
    
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards (Indeed's structure may vary)
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        if not job_cards:
            # Try alternative selectors
            job_cards = soup.find_all('td', class_='resultContent')
        
        logger.info(f"Found {len(job_cards)} job cards from Indeed")
        
        for card in job_cards[:20]:  # Limit to 20 results
            try:
                # Extract job title
                title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('span', class_='companyName')
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('div', class_='companyLocation')
                location = location_elem.get_text(strip=True) if location_elem else "Remote"
                
                # Extract apply URL
                link_elem = card.find('a', class_='jcs-JobTitle') or title_elem
                job_id = link_elem.get('data-jk', '') if link_elem else ''
                apply_url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else "https://www.indeed.com"
                
                # Date posted (approximation)
                date_posted = datetime.now().strftime('%Y-%m-%d')
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': date_posted,
                    'apply_url': apply_url,
                    'source': 'Indeed'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from Indeed: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping Indeed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping Indeed: {e}")
    
    return results