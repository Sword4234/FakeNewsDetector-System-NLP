# Fake News Detector System

A modern, AI-powered system for detecting fake news using advanced NLP techniques and machine learning models.

## Features

1. **Modern UI & Design**
   - Dark and blue themed interface
   - Interactive dashboard with real-time updates
   - Toggle for enhanced dark mode

2. **Advanced NLP Model**
   - TF-IDF and word embeddings
   - BERT-based deep learning model
   - Analysis of linguistic patterns and source credibility

3. **Comprehensive Output Metrics**
   - Credibility Score
   - Truth Probability
   - Real-time credibility timeline
   - Detailed analysis (sentiment, bias, fact-checking)

4. **News Source Comparison**
   - Region-based source selection
   - Article linking and summarization
   - Confidence scoring

5. **API Integration**
   - Flask-based REST API
   - Support for external application integration

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

## Usage

1. Access the web interface at `http://localhost:5000`
2. Enter or paste news text for analysis
3. View comprehensive analysis results

## API Documentation

The API endpoints are available at `/api/v1/` with the following methods:

- `POST /api/v1/analyze` - Analyze news text
- `GET /api/v1/sources` - Get available news sources by region

## Technologies Used

- Python
- Flask
- TensorFlow
- Transformers (BERT)
- Scikit-learn
- HTML/CSS/JavaScript
- Plotly/Dash for visualizations
