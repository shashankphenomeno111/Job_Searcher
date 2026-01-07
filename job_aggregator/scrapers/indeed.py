import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import time
import random

logger = logging.getLogger(__name__)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def scrape(query: str, days: int = 7, experience: str = "all", location: str = "India"):
    """Scrape job listings from Indeed.
    
    Args:
        query: Job search query (e.g., "Java Developer")
        days: Number of days to look back for postings
        experience: Experience level filter
        location: Location filter (e.g., "India", "Karnataka")
    
    Returns:
        List of job dictionaries with title, company, location, date_posted, apply_url
    """
    logger.info(f"Indeed scraper called with query={query}, days={days}, location={location}")
    
    results = []
    base_url = "https://in.indeed.com/jobs"
    
    # Prepare search parameters
    params = {
        'q': query,
        'l': location,
        'fromage': str(days),
        'sort': 'date'
    }
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://in.indeed.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple selector strategies
        job_cards = []
        
        # Strategy 1: Modern Indeed structure
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        if not job_cards:
            # Strategy 2: Alternative structure
            job_cards = soup.find_all('td', class_='resultContent')
        
        if not job_cards:
            # Strategy 3: Look for any div with job-related classes
            job_cards = soup.find_all('div', attrs={'data-jk': True})
        
        logger.info(f"Found {len(job_cards)} job cards from Indeed")
        
        for card in job_cards[:25]:  # Limit to 25 results
            try:
                # Extract job title - multiple strategies
                title_elem = (
                    card.find('h2', class_='jobTitle') or 
                    card.find('a', class_='jcs-JobTitle') or
                    card.find('span', attrs={'title': True}) or
                    card.find('h2')
                )
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    # Clean up title (remove "new" badges etc)
                    title = title.replace('new', '').strip()
                else:
                    title = "N/A"
                
                # Extract company name
                company_elem = (
                    card.find('span', class_='companyName') or
                    card.find('span', {'data-testid': 'company-name'}) or
                    card.find('div', class_='company')
                )
                company = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = (
                    card.find('div', class_='companyLocation') or
                    card.find('div', {'data-testid': 'text-location'}) or
                    card.find('span', class_='location')
                )
                job_location = location_elem.get_text(strip=True) if location_elem else location
                
                # Extract apply URL and job ID
                link_elem = (
                    card.find('a', class_='jcs-JobTitle') or
                    title_elem if title_elem and title_elem.name == 'a' else None or
                    card.find('a', href=True)
                )
                
                job_id = None
                if link_elem:
                    job_id = link_elem.get('data-jk') or link_elem.get('id', '').replace('job_', '')
                    href = link_elem.get('href', '')
                    if href.startswith('http'):
                        apply_url = href
                    elif href.startswith('/'):
                        apply_url = f"https://in.indeed.com{href}"
                    else:
                        apply_url = f"https://in.indeed.com/viewjob?jk={job_id}" if job_id else "https://in.indeed.com"
                else:
                    # Try to find job ID from card attributes
                    job_id = card.get('data-jk', '')
                    apply_url = f"https://in.indeed.com/viewjob?jk={job_id}" if job_id else "https://in.indeed.com"
                
                # Date posted (approximation)
                date_elem = card.find('span', class_='date')
                date_posted = datetime.now().strftime('%Y-%m-%d')
                
                # Only add if we have meaningful data
                if title != "N/A" and company != "N/A":
                    results.append({
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'date_posted': date_posted,
                        'apply_url': apply_url,
                        'source': 'Indeed'
                    })
                
            except Exception as e:
                logger.warning(f"Error parsing job card from Indeed: {e}")
                continue
        
        logger.info(f"Successfully extracted {len(results)} jobs from Indeed")
        
    except requests.RequestException as e:
        logger.error(f"HTTP error while scraping Indeed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping Indeed: {e}")
    
    return results
