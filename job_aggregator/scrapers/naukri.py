import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Naukri.com (Indian job portal).
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
        experience: Experience level filter
        location: Location within India (e.g., "Bangalore", "Mumbai")
    
    Returns:
        List of job dictionaries with title, company, location, date_posted, apply_url
    """
    logger.info(f"Naukri scraper called with query={query}, days={days}, location={location}")
    
    results = []
    base_url = "https://www.naukri.com/java-developer-jobs"
    
    # Format query for URL
    query_formatted = query.lower().replace(' ', '-')
    # Naukri is India-specific, optionally add city if not "India"
    if location.lower() != "india":
        location_formatted = location.lower().replace(' ', '-')
        search_url = f"https://www.naukri.com/{query_formatted}-jobs-in-{location_formatted}"
    else:
        search_url = f"https://www.naukri.com/{query_formatted}-jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.naukri.com/',
    }
    
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('article', class_='jobTuple')
        
        if not job_cards:
            job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')
        
        logger.info(f"Found {len(job_cards)} job cards from Naukri")
        
        for card in job_cards[:20]:  # Limit to 20 results
            try:
                # Extract job title
                title_elem = card.find('a', class_='title') or card.find('div', class_='title')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('a', class_='subTitle') or card.find('div', class_='companyInfo')
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('li', class_='location') or card.find('span', class_='loc')
                location = location_elem.get_text(strip=True) if location_elem else "India"
                
                # Extract apply URL
                link_elem = title_elem if title_elem and title_elem.name == 'a' else card.find('a')
                apply_url = link_elem.get('href', '') if link_elem else ''
                
                # Ensure full URL
                if apply_url and not apply_url.startswith('http'):
                    apply_url = 'https://www.naukri.com' + apply_url
                elif not apply_url:
                    apply_url = 'https://www.naukri.com'
                
                # Date posted
                date_posted = datetime.now().strftime('%Y-%m-%d')
                
                results.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'date_posted': date_posted,
                    'apply_url': apply_url,
                    'source': 'Naukri'
                })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from Naukri: {e}")
                continue
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping Naukri: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping Naukri: {e}")
    
    return results
