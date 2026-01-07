from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from aggregator import search_jobs
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)  # Enable CORS for React development

@app.route('/')
def serve():
    """Serve the React app"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return jsonify({"error": "Frontend not built. Run 'npm run build' first."}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from React build"""
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle job search requests"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        query = data.get('query', '').strip()
        days = int(data.get('days', 7))
        experience = data.get('experience', 'all')
        location = data.get('location', 'India')
        platforms = data.get('platforms', [
            'indeed', 'linkedin', 'glassdoor', 'naukri', 
            'monster', 'simplyhired', 'angellist', 'internshala'
        ])
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not platforms or len(platforms) == 0:
            return jsonify({"error": "At least one platform must be selected"}), 400
        
        logger.info(f"Searching for: {query} in {location} (platforms: {platforms})")
        
        results = search_jobs(query, days, experience, location, platforms)
        
        logger.info(f"Found {len(results)} jobs")
        
        return jsonify(results)
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": "An error occurred while searching"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)