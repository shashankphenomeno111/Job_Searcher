# Job Aggregator Web Application

A powerful web application that aggregates job listings from multiple job boards and search engines in one place. Search for jobs across Indeed, LinkedIn, Glassdoor, Naukri, and more with advanced filtering capabilities.

## Features

- 🔍 **Multi-Platform Search**: Scrapes jobs from Indeed, LinkedIn, Glassdoor, and Naukri
- ⏰ **Time Filtering**: Filter jobs by posting date (24h, 7 days, 30 days, all time)
- 📊 **Smart Aggregation**: Automatically deduplicates job listings
- 🌐 **Web Search Fallback**: Uses search engines when scrapers fail (optional)
- 📥 **Export to CSV**: Download all job listings for offline viewing
- 🎨 **Modern UI**: Beautiful, responsive design with glassmorphism effects
- ⚡ **Real-time Sorting**: Sort by date, title, company, or source
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd job_aggregator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Configure search engine APIs**:
   
   For enhanced search fallback, set environment variables:
   ```bash
   # Google Custom Search API
   set GOOGLE_API_KEY=your_api_key_here
   set GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
   
   # OR SerpAPI (alternative)
   set SERPAPI_KEY=your_serpapi_key_here
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Search for jobs**:
   - Enter a job title (e.g., "Java Developer", "Data Scientist")
   - Select time filter (Last 24 hours, 7 days, 30 days, or All time)
   - Click "Search Jobs"
   - View aggregated results from multiple platforms
   - Sort and export as needed

## Project Structure

```
job_aggregator/
├── app.py                      # Flask application
├── aggregator.py               # Job aggregation logic
├── search_engine.py            # Search engine fallback
├── requirements.txt            # Python dependencies
├── scrapers/
│   ├── __init__.py
│   ├── indeed.py              # Indeed scraper
│   ├── linkedin.py            # LinkedIn scraper
│   ├── glassdoor.py           # Glassdoor scraper
│   └── naukri.py              # Naukri scraper
├── templates/
│   └── index.html             # Main web interface
└── static/
    ├── css/
    │   └── style.css          # Stylesheets
    └── js/
        └── main.js            # JavaScript functionality
```

## How It Works

1. **User Input**: User enters job search query and filters
2. **Parallel Scraping**: App simultaneously scrapes multiple job boards
3. **Data Aggregation**: Results are combined and deduplicated
4. **Fallback**: If scrapers fail, web search APIs are used (if configured)
5. **Display**: Jobs are displayed in a modern, sortable interface
6. **Export**: Users can export results to CSV for further analysis

## Important Notes

### Web Scraping Considerations
- Some job websites have anti-scraping measures
- Request delays are implemented to avoid rate limiting
- User-agent rotation helps prevent blocking
- For production use, consider using official APIs where available

### API Configuration
The search engine fallback is optional but recommended:
- **Google Custom Search**: Free tier provides 100 queries/day
- **SerpAPI**: Free tier provides 100 queries/month
- App works without APIs but with limited fallback capability

## Technologies Used

- **Backend**: Flask, Python 3.x
- **Web Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Custom CSS with glassmorphism and gradients
- **APIs** (Optional): Google Custom Search API, SerpAPI

## Future Enhancements

- [ ] User authentication and saved searches
- [ ] Email alerts for new job postings
- [ ] More job board integrations (Monster, ZipRecruiter, etc.)
- [ ] Advanced filters (salary, experience level, remote/hybrid)
- [ ] Job application tracking
- [ ] Chrome extension for quick searches

## License

This project is created for educational and personal use.

## Contributing

This is a personal project, but suggestions and improvements are welcome!

## Author

Built with ❤️ for job seekers everywhere

---

**Disclaimer**: This tool is for educational purposes. Always respect websites' terms of service and robots.txt files. Consider using official APIs for production applications.
