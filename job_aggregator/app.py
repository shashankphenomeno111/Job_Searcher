from flask import Flask, render_template, request, jsonify
from aggregator import search_jobs

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    days = data.get('days', 7)
    experience = data.get('experience', 'all')
    location = data.get('location', 'India')
    platforms = data.get('platforms', ['indeed', 'linkedin', 'glassdoor', 'naukri', 'monster', 'simplyhired', 'angellist', 'internshala'])
    results = search_jobs(query, days, experience, location, platforms)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)