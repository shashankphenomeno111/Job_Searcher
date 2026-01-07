import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
    Search, MapPin, Briefcase, Calendar, TrendingUp,
    Filter, Download, Trash2, CheckSquare, Square, Sparkles
} from 'lucide-react'
import axios from 'axios'
import {
    INDIAN_STATES, JOB_PLATFORMS, TIME_FILTERS,
    EXPERIENCE_LEVELS, SORT_OPTIONS
} from './constants'
import './App.css'

function App() {
    const [query, setQuery] = useState('Software Developer')
    const [state, setState] = useState('Karnataka')
    const [days, setDays] = useState(7)
    const [experience, setExperience] = useState('all')
    const [sortBy, setSortBy] = useState('date')
    const [selectedPlatforms, setSelectedPlatforms] = useState(
        JOB_PLATFORMS.map(p => p.id)
    )
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(false)
    const [searched, setSearched] = useState(false)

    const handlePlatformToggle = (platformId) => {
        setSelectedPlatforms(prev =>
            prev.includes(platformId)
                ? prev.filter(id => id !== platformId)
                : [...prev, platformId]
        )
    }

    const selectAllPlatforms = () => {
        setSelectedPlatforms(JOB_PLATFORMS.map(p => p.id))
    }

    const deselectAllPlatforms = () => {
        setSelectedPlatforms([])
    }

    const handleSearch = async () => {
        if (!query.trim()) {
            alert('Please enter a job title or keywords')
            return
        }

        if (selectedPlatforms.length === 0) {
            alert('Please select at least one platform')
            return
        }

        setLoading(true)
        setSearched(true)

        try {
            const response = await axios.post('/search', {
                query: query.trim(),
                days,
                experience,
                location: state,
                platforms: selectedPlatforms
            })

            setJobs(response.data || [])
        } catch (error) {
            console.error('Search error:', error)
            alert('An error occurred while searching. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch()
        }
    }

    const sortedJobs = [...jobs].sort((a, b) => {
        switch (sortBy) {
            case 'title':
                return a.title.localeCompare(b.title)
            case 'company':
                return a.company.localeCompare(b.company)
            case 'source':
                return a.source.localeCompare(b.source)
            case 'date':
            default:
                return new Date(b.date_posted) - new Date(a.date_posted)
        }
    })

    const exportToCSV = () => {
        if (jobs.length === 0) {
            alert('No jobs to export')
            return
        }

        const headers = ['Title', 'Company', 'Location', 'Date Posted', 'Source', 'Apply URL']
        const rows = jobs.map(job => [
            job.title,
            job.company,
            job.location,
            job.date_posted,
            job.source,
            job.apply_url
        ])

        let csvContent = headers.join(',') + '\n'
        rows.forEach(row => {
            csvContent += row.map(field => `"${field}"`).join(',') + '\n'
        })

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)

        link.setAttribute('href', url)
        link.setAttribute('download', `job_listings_${new Date().toISOString().split('T')[0]}.csv`)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    const clearResults = () => {
        setJobs([])
        setSearched(false)
    }

    const stats = {
        totalJobs: jobs.length,
        totalSources: new Set(jobs.map(job => job.source)).size,
        latestUpdate: new Date().toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    return (
        <div className="app">
            {/* Header */}
            <motion.header
                className="header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <div className="logo-section">
                    <motion.div
                        className="logo-icon"
                        animate={{ y: [0, -10, 0] }}
                        transition={{ duration: 3, repeat: Infinity }}
                    >
                        💼
                    </motion.div>
                    <h1 className="logo-text">
                        Job<span className="gradient-text">Searcher</span>
                    </h1>
                </div>
                <div className="tagline-container">
                    <Sparkles size={20} className="sparkle-icon" />
                    <p className="tagline">Find Your Dream Job Across India</p>
                    <Sparkles size={20} className="sparkle-icon" />
                </div>
            </motion.header>

            {/* Search Section */}
            <motion.section
                className="search-section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
            >
                <div className="search-container glass">
                    {/* Job Title Input */}
                    <div className="input-group">
                        <label className="input-label">
                            <Search size={18} />
                            <span>What job are you looking for?</span>
                        </label>
                        <div className="input-wrapper">
                            <Search size={20} className="input-icon" />
                            <input
                                type="text"
                                className="input-field"
                                placeholder="e.g., Software Developer, Data Scientist, Designer..."
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                        </div>
                    </div>

                    {/* State Selection */}
                    <div className="input-group">
                        <label className="input-label">
                            <MapPin size={18} />
                            <span>Select State</span>
                        </label>
                        <div className="input-wrapper">
                            <MapPin size={20} className="input-icon" />
                            <select
                                className="input-field select-field"
                                value={state}
                                onChange={(e) => setState(e.target.value)}
                            >
                                {INDIAN_STATES.map(stateName => (
                                    <option key={stateName} value={stateName}>
                                        {stateName}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Filters Row */}
                    <div className="filters-row">
                        <div className="filter-group">
                            <label className="filter-label">
                                <Calendar size={16} />
                                Posted Within
                            </label>
                            <select
                                className="filter-select"
                                value={days}
                                onChange={(e) => setDays(parseInt(e.target.value))}
                            >
                                {TIME_FILTERS.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="filter-group">
                            <label className="filter-label">
                                <Briefcase size={16} />
                                Experience Level
                            </label>
                            <select
                                className="filter-select"
                                value={experience}
                                onChange={(e) => setExperience(e.target.value)}
                            >
                                {EXPERIENCE_LEVELS.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="filter-group">
                            <label className="filter-label">
                                <TrendingUp size={16} />
                                Sort By
                            </label>
                            <select
                                className="filter-select"
                                value={sortBy}
                                onChange={(e) => setSortBy(e.target.value)}
                            >
                                {SORT_OPTIONS.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Platforms Section */}
                    <div className="platforms-section">
                        <div className="platforms-header">
                            <label className="platforms-label">
                                <Filter size={18} />
                                <span>Select Job Platforms</span>
                            </label>
                            <div className="platform-actions">
                                <button
                                    type="button"
                                    className="platform-action-btn"
                                    onClick={selectAllPlatforms}
                                >
                                    <CheckSquare size={16} />
                                    Select All
                                </button>
                                <button
                                    type="button"
                                    className="platform-action-btn"
                                    onClick={deselectAllPlatforms}
                                >
                                    <Square size={16} />
                                    Clear All
                                </button>
                            </div>
                        </div>

                        <div className="platforms-grid">
                            {JOB_PLATFORMS.map(platform => (
                                <motion.label
                                    key={platform.id}
                                    className={`platform-checkbox ${selectedPlatforms.includes(platform.id) ? 'checked' : ''
                                        }`}
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={selectedPlatforms.includes(platform.id)}
                                        onChange={() => handlePlatformToggle(platform.id)}
                                    />
                                    <span className="platform-name">{platform.name}</span>
                                </motion.label>
                            ))}
                        </div>
                    </div>

                    {/* Search Button */}
                    <motion.button
                        className="search-btn"
                        onClick={handleSearch}
                        disabled={loading}
                        whileHover={{ scale: 1.02, y: -2 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        <span className="btn-text">
                            {loading ? 'Searching...' : 'Search Jobs'}
                        </span>
                        <Search size={20} className="btn-icon" />
                    </motion.button>
                </div>
            </motion.section>

            {/* Stats Section */}
            <AnimatePresence>
                {searched && !loading && jobs.length > 0 && (
                    <motion.section
                        className="stats-section"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.4 }}
                    >
                        <div className="stat-card glass">
                            <div className="stat-value gradient-text">{stats.totalJobs}</div>
                            <div className="stat-label">Jobs Found</div>
                        </div>
                        <div className="stat-card glass">
                            <div className="stat-value gradient-text">{stats.totalSources}</div>
                            <div className="stat-label">Sources</div>
                        </div>
                        <div className="stat-card glass">
                            <div className="stat-value gradient-text">{stats.latestUpdate}</div>
                            <div className="stat-label">Updated At</div>
                        </div>
                    </motion.section>
                )}
            </AnimatePresence>

            {/* Loading State */}
            <AnimatePresence>
                {loading && (
                    <motion.div
                        className="loading-state"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <div className="loading-spinner" />
                        <p className="loading-text">
                            Searching across multiple job platforms...
                        </p>
                        <div className="loading-sources">
                            {selectedPlatforms.map(platformId => {
                                const platform = JOB_PLATFORMS.find(p => p.id === platformId)
                                return (
                                    <motion.span
                                        key={platformId}
                                        className="source-badge"
                                        animate={{ opacity: [0.5, 1, 0.5] }}
                                        transition={{ duration: 2, repeat: Infinity }}
                                    >
                                        {platform?.name}
                                    </motion.span>
                                )
                            })}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Results Section */}
            <AnimatePresence>
                {searched && !loading && (
                    <motion.section
                        className="results-section"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                    >
                        {jobs.length > 0 ? (
                            <>
                                <div className="results-header">
                                    <h2 className="results-title">
                                        Found {jobs.length} Job{jobs.length !== 1 ? 's' : ''}
                                    </h2>
                                    <div className="results-actions">
                                        <button className="action-btn" onClick={exportToCSV}>
                                            <Download size={18} />
                                            Export CSV
                                        </button>
                                        <button className="action-btn secondary" onClick={clearResults}>
                                            <Trash2 size={18} />
                                            Clear
                                        </button>
                                    </div>
                                </div>

                                <div className="jobs-grid">
                                    {sortedJobs.map((job, index) => (
                                        <motion.div
                                            key={`${job.apply_url}-${index}`}
                                            className="job-card glass"
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.05 }}
                                            whileHover={{ y: -4, scale: 1.01 }}
                                            onClick={() => window.open(job.apply_url, '_blank')}
                                        >
                                            <div className="job-card-header">
                                                <div className="job-info">
                                                    <h3 className="job-title">{job.title}</h3>
                                                    <p className="job-company">{job.company}</p>
                                                </div>
                                                <span className="job-source-badge">
                                                    {job.source}
                                                </span>
                                            </div>

                                            <div className="job-meta">
                                                <div className="job-meta-item">
                                                    <MapPin size={16} />
                                                    <span>{job.location}</span>
                                                </div>
                                                <div className="job-meta-item">
                                                    <Calendar size={16} />
                                                    <span>
                                                        {new Date(job.date_posted).toLocaleDateString('en-IN', {
                                                            year: 'numeric',
                                                            month: 'short',
                                                            day: 'numeric'
                                                        })}
                                                    </span>
                                                </div>
                                            </div>

                                            <motion.a
                                                href={job.apply_url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="apply-btn"
                                                onClick={(e) => e.stopPropagation()}
                                                whileHover={{ scale: 1.05 }}
                                                whileTap={{ scale: 0.95 }}
                                            >
                                                Apply Now →
                                            </motion.a>
                                        </motion.div>
                                    ))}
                                </div>
                            </>
                        ) : (
                            <div className="no-results">
                                <div className="no-results-icon">😕</div>
                                <h3>No jobs found</h3>
                                <p>Try adjusting your search query or filters</p>
                            </div>
                        )}
                    </motion.section>
                )}
            </AnimatePresence>

            {/* Footer */}
            <footer className="footer">
                <p className="footer-text">
                    Searching jobs across India from Indeed, LinkedIn, Glassdoor, Naukri, Monster, and more
                </p>
                <p className="footer-note">Made with ❤️ for job seekers in India</p>
            </footer>
        </div>
    )
}

export default App
