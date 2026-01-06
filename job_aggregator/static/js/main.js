// Global variables
let allJobs = [];
let displayedJobs = [];

// DOM Elements
const searchInput = document.getElementById('searchInput');
const locationInput = document.getElementById('locationInput');
const searchBtn = document.getElementById('searchBtn');
const timeFilter = document.getElementById('timeFilter');
const experienceFilter = document.getElementById('experienceFilter');
const sortBy = document.getElementById('sortBy');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const statsSection = document.getElementById('statsSection');
const resultsContainer = document.getElementById('resultsContainer');
const noResults = document.getElementById('noResults');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');

// Event Listeners
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});
sortBy.addEventListener('change', () => sortAndDisplayJobs());
exportBtn.addEventListener('click', exportToCSV);
clearBtn.addEventListener('click', clearResults);

// Platform selection buttons
document.getElementById('selectAllPlatforms').addEventListener('click', () => {
    document.querySelectorAll('input[name="platform"]').forEach(cb => cb.checked = true);
});

document.getElementById('deselectAllPlatforms').addEventListener('click', () => {
    document.querySelectorAll('input[name="platform"]').forEach(cb => cb.checked = false);
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Job Aggregator Initialized');
});

// Main search function
async function performSearch() {
    const query = searchInput.value.trim();
    const location = locationInput.value.trim() || 'India';
    const days = parseInt(timeFilter.value);
    const experience = experienceFilter.value;

    // Get selected platforms
    const selectedPlatforms = Array.from(document.querySelectorAll('input[name="platform"]:checked'))
        .map(cb => cb.value);

    if (!query) {
        alert('Please enter a job title or keywords');
        return;
    }

    if (selectedPlatforms.length === 0) {
        alert('Please select at least one platform to search');
        return;
    }

    // Show loading state
    showLoading();
    hideResults();

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, days, experience, location, platforms: selectedPlatforms })
        });

        if (!response.ok) {
            throw new Error('Search request failed');
        }

        const jobs = await response.json();
        allJobs = jobs;

        hideLoading();

        if (jobs.length > 0) {
            displayResults(jobs);
            updateStats(jobs);
        } else {
            showNoResults();
        }

    } catch (error) {
        console.error('Search error:', error);
        hideLoading();
        alert('An error occurred while searching. Please try again.');
    }
}

// Display results
function displayResults(jobs) {
    displayedJobs = jobs;
    sortAndDisplayJobs();
    resultsSection.style.display = 'block';
    statsSection.style.display = 'grid';
    noResults.style.display = 'none';
}

// Sort and display jobs
function sortAndDisplayJobs() {
    const sortValue = sortBy.value;
    let sortedJobs = [...displayedJobs];

    switch (sortValue) {
        case 'title':
            sortedJobs.sort((a, b) => a.title.localeCompare(b.title));
            break;
        case 'company':
            sortedJobs.sort((a, b) => a.company.localeCompare(b.company));
            break;
        case 'source':
            sortedJobs.sort((a, b) => a.source.localeCompare(b.source));
            break;
        case 'date':
        default:
            sortedJobs.sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted));
            break;
    }

    renderJobs(sortedJobs);
}

// Render job cards
function renderJobs(jobs) {
    resultsContainer.innerHTML = '';

    jobs.forEach((job, index) => {
        const jobCard = createJobCard(job, index);
        resultsContainer.appendChild(jobCard);
    });
}

// Create individual job card
function createJobCard(job, index) {
    const card = document.createElement('div');
    card.className = 'job-card';
    card.style.animationDelay = `${index * 0.05}s`;

    // Format date
    const dateObj = new Date(job.date_posted);
    const formattedDate = dateObj.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });

    card.innerHTML = `
        <div class="job-card-header">
            <div>
                <h3 class="job-title">${escapeHtml(job.title)}</h3>
                <div class="job-company">${escapeHtml(job.company)}</div>
            </div>
            <span class="job-source">${escapeHtml(job.source)}</span>
        </div>
        
        <div class="job-meta">
            <div class="job-meta-item">
                <span>📍</span>
                <span>${escapeHtml(job.location)}</span>
            </div>
            <div class="job-meta-item">
                <span>📅</span>
                <span>${formattedDate}</span>
            </div>
        </div>
        
        <div class="job-actions">
            <a href="${escapeHtml(job.apply_url)}" 
               class="apply-btn" 
               target="_blank" 
               rel="noopener noreferrer"
               onclick="event.stopPropagation()">
                Apply Now →
            </a>
        </div>
    `;

    // Make card clickable to open job
    card.addEventListener('click', () => {
        window.open(job.apply_url, '_blank', 'noopener,noreferrer');
    });

    return card;
}

// Update statistics
function updateStats(jobs) {
    const sources = new Set(jobs.map(job => job.source));

    document.getElementById('totalJobs').textContent = jobs.length;
    document.getElementById('totalSources').textContent = sources.size;

    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('latestUpdate').textContent = timeString;
}

// Export to CSV
function exportToCSV() {
    if (displayedJobs.length === 0) {
        alert('No jobs to export');
        return;
    }

    // Create CSV content
    const headers = ['Title', 'Company', 'Location', 'Date Posted', 'Source', 'Apply URL'];
    const rows = displayedJobs.map(job => [
        job.title,
        job.company,
        job.location,
        job.date_posted,
        job.source,
        job.apply_url
    ]);

    let csvContent = headers.join(',') + '\n';
    rows.forEach(row => {
        csvContent += row.map(field => `"${field}"`).join(',') + '\n';
    });

    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', `job_listings_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Clear results
function clearResults() {
    allJobs = [];
    displayedJobs = [];
    resultsContainer.innerHTML = '';
    hideResults();
    statsSection.style.display = 'none';
}

// Show/Hide states
function showLoading() {
    loadingState.style.display = 'block';
}

function hideLoading() {
    loadingState.style.display = 'none';
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function showNoResults() {
    resultsSection.style.display = 'block';
    noResults.style.display = 'block';
    resultsContainer.innerHTML = '';
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Add some visual feedback
document.querySelectorAll('.filter-select, .search-input').forEach(element => {
    element.addEventListener('focus', function () {
        this.style.transform = 'scale(1.01)';
    });

    element.addEventListener('blur', function () {
        this.style.transform = 'scale(1)';
    });
});
