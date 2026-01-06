import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Glassdoor.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
    
    Returns:
        List of job dictionaries with title, company, location, date_posted, apply_url
    """
    logger.info(f"Glassdoor scraper called with query={query}, days={days}")
    
    results = []
    base_url = "https://www.glassdoor.com/Job/jobs.htm"
    
    # Prepare search parameters
    params = {
        'sc.keyword': query,
        'fromAge': str(days),
        'sort': 'date_desc'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.glassdoor.com/',
    }
    
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('li', class_='react-job-listing')
        
        if not job_cards:
            job_cards = soup.find_all('div', attrs={'data-test': 'jobListing'})
        
        logger.info(f"Found {len(job_cards)} job cards from Glassdoor")
        
        for card in job_cards[:20]:  # Limit to 20 results
            try:
                # Extract job title
                title_elem = card.find('a', class_='job-title') or card.find('a', attrs={'data-test': 'job-link'})
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('div', class_='employer-name') or card.find('span', attrs={'data-test': 'employer-name'})
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('span', class_='location') or card.find('span', attrs={'data-test': 'emp-location'})
                location = location_elem.get_text(strip=True) if location_elem else "Remote"
                
                # Extract apply URL
                link_elem = title_elem
                apply_url = link_elem.get('href', '') if link_elem else ''
                
                # Ensure full URL
                if apply_url and not apply_url.startswith('http'):
                    apply_url = 'https://www.glassdoor.com' + apply_url
                elif not apply_url:
                    apply_url = 'https://www.glassdoor.com'
                
                # Date posted
                date_posted = datetime.now().strftime('%Y-%m-%d')
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': date_posted,
                    'apply_url': apply_url,
                    'source': 'Glassdoor'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from Glassdoor: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping Glassdoor: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping Glassdoor: {e}")
    
    return results
