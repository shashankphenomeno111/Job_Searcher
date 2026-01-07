# Job Searcher - India Edition 🇮🇳

A beautiful, modern job aggregator specifically designed for the Indian job market. Search across multiple platforms including Indeed, LinkedIn, Glassdoor, Naukri, Monster, and more - all in one place!

## ✨ Features

- 🎯 **India-Focused**: Exclusively searches for jobs across Indian states
- 🌐 **Multi-Platform Search**: Aggregates jobs from 8+ platforms
  - Indeed
  - LinkedIn
  - Glassdoor
  - Naukri
  - Monster
  - SimplyHired
  - AngelList
  - Internshala
- 🎨 **Beautiful Modern UI**: Built with React and Framer Motion
- 🔍 **Advanced Filtering**:
  - Search by job title/keywords
  - Filter by Indian state
  - Posted within (1 day, 7 days, 30 days, all time)
  - Experience level (All, Fresher, Experienced)
  - Sort results by date, title, company, or source
- 📊 **Real-time Statistics**: See total jobs found and sources searched
- 📥 **Export to CSV**: Download your search results
- ⚡ **Fast & Responsive**: Optimized for performance

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install Node.js dependencies**:
```bash
npm install
```

### Development Mode

To run the application in development mode:

1. **Start the Flask backend** (in one terminal):
```bash
python app.py
```
This starts the Flask API server on `http://localhost:5000`

2. **Start the React frontend** (in another terminal):
```bash
npm run dev
```
This starts the Vite dev server on `http://localhost:5173`

Open your browser and navigate to `http://localhost:5173`

### Production Build

To build and run the production version:

1. **Build the React app**:
```bash
npm run build
```

2. **Run the Flask server**:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 📖 Usage

1. **Enter your search query** (e.g., "Software Developer", "Data Scientist")
2. **Select a state** from the dropdown (e.g., Karnataka, Maharashtra, Delhi)
3. **Choose filters**:
   - How recent you want the jobs
   - Experience level
   - Sort preference
4. **Select platforms** to search (or use "Select All")
5. **Click "Search Jobs"**
6. **Browse results** and click "Apply Now" to visit job postings

## 🛠️ Technology Stack

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **Flask** - Web framework
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP library
- **Flask-CORS** - Cross-origin support

## 📁 Project Structure

```
job_aggregator/
├── src/                    # React source files
│   ├── App.jsx            # Main React component
│   ├── App.css            # Component styles
│   ├── index.css          # Global styles
│   ├── main.jsx           # React entry point
│   └── constants.js       # Indian states and config
├── scrapers/              # Job scraper modules
│   ├── indeed.py
│   ├── linkedin.py
│   ├── glassdoor.py
│   ├── naukri.py
│   └── ...
├── static/                # Old static files (legacy)
├── templates/             # Old templates (legacy)
├── aggregator.py          # Job aggregation logic
├── app.py                 # Flask application
├── search_engine.py       # Fallback search
├── vite.config.js         # Vite configuration
├── package.json           # Node dependencies
├── requirements.txt       # Python dependencies
└── index.html             # HTML entry point
```

## 🔧 Configuration

### Adding More Scrapers

To add a new job platform:

1. Create a new scraper in `scrapers/yourplatform.py`
2. Implement the `scrape()` function
3. Add the platform to `SCRAPER_MODULES` in `aggregator.py`
4. Add platform info to `JOB_PLATFORMS` in `src/constants.js`

### Customizing States

Edit the `INDIAN_STATES` array in `src/constants.js` to modify available states.

## 🎨 Design Features

- **Dark Theme**: Modern dark mode design
- **Glassmorphism**: Beautiful glass effects
- **Smooth Animations**: Powered by Framer Motion
- **Gradient Accents**: Vibrant color gradients
- **Responsive**: Works on all device sizes
- **Premium Feel**: High-quality UI/UX

## 🐛 Troubleshooting

### "Frontend not built" error
Run `npm run build` before starting the Flask server in production mode.

### CORS errors in development
Make sure both Flask (port 5000) and Vite (port 5173) are running.

### No jobs found
- Try adjusting your search query
- Select more platforms
- Increase the time range
- Some platforms may have rate limiting

### Scraper not working
Job board websites frequently change their HTML structure. Check the scraper files and update selectors if needed.

## 📝 Notes

- This application is designed exclusively for searching jobs in India
- Country selection has been intentionally removed - all searches are India-specific
- State selection allows you to narrow down to specific regions
- Web scraping may be affected by website changes or rate limiting
- Some platforms may require additional configuration or API keys

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

ISC License

## ❤️ Made with Love

Built specifically for job seekers in India. Happy job hunting! 🎯

---

**Pro Tips:**
- Use specific job titles for better results
- Try multiple platforms for comprehensive search
- Export results to CSV for offline review
- Check back regularly as new jobs are posted daily
