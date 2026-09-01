from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from models.detector import FakeNewsDetector
from utils.news_sources import NewsSourceComparison
from utils.metrics import CredibilityMetrics

app = Flask(__name__)
CORS(app)

# Initialize models
detector = FakeNewsDetector()
news_comparator = NewsSourceComparison()
metrics_analyzer = CredibilityMetrics()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        data = request.get_json()
        news_text = data.get('news_text', '')
        
        if not news_text:
            return jsonify({'error': 'No news text provided'}), 400
        
        # Use the new comprehensive analysis method
        analysis_results = detector.analyze_news(news_text)
        
        # Generate timeline data if not already included
        if 'timeline_data' not in analysis_results:
            timeline_data = detector.ai_model.generate_timeline_data(analysis_results['credibility_score'])
            analysis_results['timeline_data'] = timeline_data
        
        return jsonify(analysis_results)

# API Routes
@app.route('/api/v1/analyze', methods=['POST'])
def api_analyze():
    if request.method == 'POST':
        data = request.get_json()
        news_text = data.get('news_text', '')
        
        if not news_text:
            return jsonify({'error': 'No news text provided'}), 400
        
        # Use the new comprehensive analysis method
        analysis_results = detector.analyze_news(news_text)
        
        return jsonify(analysis_results)

@app.route('/api/v1/sources', methods=['GET'])
def api_sources():
    regions = news_comparator.get_available_regions()
    sources = {}
    
    for region in regions:
        sources[region] = news_comparator.get_sources_for_region(region)
    
    return jsonify(sources)

if __name__ == '__main__':
    app.run(debug=True)
