# 🚀 Job Searcher - Quick Start Guide

## Welcome! 👋

Your job searcher has been completely transformed with:
- ✅ **India-only focus** - No country selection, only Indian states
- ✅ **Beautiful React UI** - Modern, premium design
- ✅ **Multi-platform support** - All job sites work correctly
- ✅ **State selection** - Choose from all Indian states
- ✅ **Enhanced scrapers** - Better job extraction

## 🎯 What Changed?

### 1. India-Specific
- Removed country selection completely
- Added dropdown for all Indian states and Union Territories
- Default location is Karnataka (you can change this)

### 2. Modern React UI
- Beautiful dark theme with gradients
- Smooth animations using Framer Motion
- Premium glassmorphism effects
- Fully responsive design

### 3. Improved Job Scrapers
- Better error handling
- Multiple selector strategies
- Support for all platforms (not just LinkedIn)
- Enhanced Indeed scraper for Indian job market

## 📦 Installation

### First Time Setup:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

That's it! You're ready to go.

## 🏃 Running the Application

### Option 1: Development Mode (Recommended for Testing)

**Windows:**
Simply double-click `start-dev.bat`

**Or manually:**
1. Open Terminal 1:
   ```bash
   python app.py
   ```

2. Open Terminal 2:
   ```bash
   npm run dev
   ```

3. Open browser: `http://localhost:5173`

### Option 2: Production Mode

**Windows:**
Double-click `start-production.bat`

**Or manually:**
```bash
npm run build
python app.py
```

Then open `http://localhost:5000`

## 🎨 Features Overview

### Search Options:
- **Job Title**: Enter keywords like "Software Developer", "Data Analyst"
- **State**: Select any Indian state (Karnataka, Maharashtra, Delhi, etc.)
- **Posted Within**: Last 24 hours, 7 days, 30 days, or all time
- **Experience Level**: All, Fresher, or Experienced
- **Sort By**: Date, Title, Company, or Source

### Platform Selection:
Choose which job boards to search:
- Indeed (India)
- LinkedIn
- Glassdoor
- Naukri
- Monster
- SimplyHired
- AngelList
- Internshala

### Results Actions:
- **Export CSV**: Download all results
- **Apply Now**: Click to visit job posting
- **Clear**: Remove all results

## 🔧 Customization

### Change Default State:
Edit `src/App.jsx`, line 17:
```javascript
const [state, setState] = useState('Karnataka')  // Change to any state
```

### Add/Remove States:
Edit `src/constants.js` - modify the `INDIAN_STATES` array

### Modify Platforms:
Edit `src/constants.js` - modify the `JOB_PLATFORMS` array

## 📱 How to Use

1. **Enter job title** - e.g., "React Developer"
2. **Select state** - e.g., "Karnataka" or "Maharashtra"
3. **Set filters** - Choose time range and experience level
4. **Select platforms** - Choose which sites to search (or Select All)
5. **Click "Search Jobs"** - Wait for results
6. **Browse & Apply** - Click on jobs to apply

## 💡 Tips for Best Results

1. **Use specific job titles** - "Python Developer" better than just "Developer"
2. **Try multiple states** - Jobs in nearby states might be remote-friendly
3. **Select all platforms** - More platforms = more results
4. **Export results** - Save as CSV for offline review
5. **Search regularly** - New jobs posted daily

## 🐛 Troubleshooting

### "Frontend not built" error
Run: `npm run build` first

### No servers starting with batch files
Run commands manually in separate terminals

### Very few or no results
- Try broader search terms
- Increase time range to 30 days
- Select all platforms
- Some scrapers may be temporarily blocked (this is normal)

### React app not loading
Make sure both servers are running:
- Flask on port 5000
- Vite on port 5173

## 📊 Understanding Results

### Job Card Information:
- **Title**: Job position name
- **Company**: Employer name
- **Location**: City/state in India
- **Date Posted**: When job was listed
- **Source**: Which platform (Indeed, Naukri, etc.)
- **Apply Button**: Direct link to application

### Statistics:
- **Jobs Found**: Total number of results
- **Sources**: How many platforms returned results
- **Updated At**: Time of last search

## 🎯 India-Focused Design

This application is **exclusively** for the Indian job market:
- All searches are India-specific
- States include all Indian states and UTs
- Job boards configured for Indian regions
- No international job results

## 📝 File Structure

```
job_aggregator/
├── src/                    # React application
│   ├── App.jsx            # Main component
│   ├── constants.js       # Indian states & config
│   └── ...
├── scrapers/              # Job scrapers
├── app.py                 # Flask backend
├── start-dev.bat          # Launch development
├── start-production.bat   # Launch production
└── README_NEW.md          # Full documentation
```

## 🚀 Next Steps

1. Run the development server
2. Try searching for jobs in your field
3. Adjust filters and states as needed
4. Export results you like
5. Apply to jobs!

## ❓ FAQ

**Q: Why only India?**
A: As requested, this app is focused exclusively on the Indian job market with state-level granularity.

**Q: Which platforms work best?**
A: Naukri, Indeed India, and Internshala typically have the most Indian jobs. LinkedIn is great for tech roles.

**Q: Can I add more job boards?**
A: Yes! Create a new scraper in `scrapers/` folder following the existing pattern.

**Q: Why aren't all jobs showing?**
A: Some websites have anti-scraping measures. Results vary by platform availability and rate limiting.

**Q: Can I change the default state?**
A: Yes, edit line 17 in `src/App.jsx`

## 🎉 Enjoy!

Your new India-focused job searcher is ready. Happy job hunting! 🇮🇳

For detailed documentation, see `README_NEW.md`
