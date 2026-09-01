import random
import re
from datetime import datetime, timedelta
from models.fake_news_ai import FakeNewsAI
from utils.news_sources import NewsSourceComparison
from utils.metrics import CredibilityMetrics

class FakeNewsDetector:
    def __init__(self):
        self.ai_model = FakeNewsAI()
        self.news_sources = NewsSourceComparison()
        self.metrics_analyzer = CredibilityMetrics()
    
    def analyze_news(self, news_text):
        """Analyze news text and return comprehensive results"""
        # Get AI analysis
        ai_analysis = self.ai_model.analyze_text(news_text)
        
        # Extract key metrics from AI analysis
        credibility_score = ai_analysis['credibility_score']
        
        # Ensure truth probability is consistent with credibility score
        # Truth probability should be the same as credibility score
        truth_probability = credibility_score
        
        # Adjust credibility score based on policy/economic indicators
        # Check if the text contains policy/economic terms that indicate legitimate news
        policy_economic_terms = [
            "policy", "economic", "trade", "bilateral", "diplomatic", 
            "government", "ministry", "department", "official", 
            "legislation", "regulatory", "fiscal", "monetary", "tax", 
            "budget", "international", "strategic", "negotiations"
        ]
        
        # Count policy/economic terms in the text
        policy_terms_count = sum(1 for term in policy_economic_terms if term.lower() in news_text.lower())
        
        # If multiple policy terms are found and no suspicious patterns, boost the credibility
        if policy_terms_count >= 2 and len(ai_analysis['pattern_matches']) == 0:
            # Check for credibility indicators that suggest legitimate news
            credibility_indicators = ai_analysis.get('credibility_indicators', [])
            policy_indicators = [ind for ind in credibility_indicators if any(term in ind.lower() for term in policy_economic_terms)]
            
            if len(policy_indicators) >= 1:
                # This is likely legitimate policy/economic news, ensure high credibility
                credibility_score = max(credibility_score, 85)
                truth_probability = credibility_score
        
        # Generate timeline data using the AI model's method
        timeline_data = self.ai_model.generate_timeline_data(credibility_score)
        
        # Detect region and get source comparison only if credibility score is above 80
        region = self._detect_region(news_text)
        source_comparison = None
        if credibility_score >= 80:
            source_comparison = self.news_sources.get_related_articles(news_text, region)
        else:
            source_comparison = []  # Empty list when credibility is too low
        
        # Get detailed metrics from both AI model and metrics analyzer
        ai_detailed_metrics = self._generate_detailed_metrics(news_text, ai_analysis)
        metrics_analysis = self.metrics_analyzer.get_detailed_metrics(news_text)
        
        # Combine metrics from both sources
        detailed_metrics = {
            'source_credibility': ai_detailed_metrics['source_credibility'],
            'fact_density': ai_detailed_metrics['fact_density'],
            'sentiment_score': metrics_analysis['sentiment_score'],
            'bias_score': metrics_analysis['bias_score'],
            'fact_check_confidence': metrics_analysis['fact_check_confidence'],
            'manipulative_language': metrics_analysis['manipulative_language'],
            'source_reliability': metrics_analysis['source_reliability'],
            'text_quality': ai_detailed_metrics['text_quality'],
            'linguistic_complexity': ai_analysis['text_stats']['linguistic_complexity']
        }
        
        # Generate conclusion based on analysis
        conclusion = self._generate_conclusion(ai_analysis)
        
        # Prepare AI insights
        ai_insights = {
            'pattern_matches': ai_analysis['pattern_matches'],
            'scientific_impossibilities': ai_analysis['scientific_impossibilities'],
            'credibility_indicators': ai_analysis.get('credibility_indicators', []),
            'model_confidence': ai_analysis['model_confidence'],
            'text_statistics': ai_analysis['text_stats'],
            'conclusion': conclusion
        }
        
        return {
            'credibility_score': credibility_score,
            'truth_probability': truth_probability,
            'detailed_metrics': detailed_metrics,
            'timeline_data': timeline_data,
            'source_comparison': source_comparison,
            'ai_insights': ai_insights
        }
    
    def _detect_region(self, text):
        """
        Detect the region of the news based on keywords
        """
        text = text.lower()
        
        # Region keywords
        us_keywords = ['united states', 'america', 'u.s.', 'usa', 'washington', 'new york', 'california', 'texas']
        uk_keywords = ['united kingdom', 'uk', 'britain', 'england', 'london', 'scotland', 'wales']
        eu_keywords = ['european union', 'eu', 'europe', 'brussels', 'germany', 'france', 'italy', 'spain']
        asia_keywords = ['asia', 'china', 'japan', 'india', 'korea', 'singapore', 'tokyo', 'beijing', 'delhi']
        
        # Count occurrences
        us_count = sum(1 for keyword in us_keywords if keyword in text)
        uk_count = sum(1 for keyword in uk_keywords if keyword in text)
        eu_count = sum(1 for keyword in eu_keywords if keyword in text)
        asia_count = sum(1 for keyword in asia_keywords if keyword in text)
        
        # Determine region based on highest count
        counts = {
            'us': us_count,
            'uk': uk_count,
            'eu': eu_count,
            'asia': asia_count
        }
        
        # Get region with highest count
        max_region = max(counts, key=counts.get)
        
        # If no region is detected, default to 'us'
        if counts[max_region] == 0:
            return 'us'
        
        return max_region
    
    def _generate_detailed_metrics(self, text, ai_analysis):
        """
        Generate detailed metrics for the news text
        """
        # Calculate metrics based on AI analysis and text characteristics
        
        # Text length score - longer articles tend to be more credible
        text_length = len(text)
        length_score = min(100, max(0, (text_length / 1000) * 100))
        
        # Sentiment analysis (simplified)
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'benefit', 'improve']
        negative_words = ['bad', 'terrible', 'negative', 'failure', 'harm', 'worsen', 'danger']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            sentiment_score = (positive_count / total_sentiment_words) * 100
        else:
            sentiment_score = 50  # Neutral
        
        # Clickbait detection (simplified)
        clickbait_patterns = [
            r'(?i)you won\'t believe',
            r'(?i)shocking',
            r'(?i)mind-?blowing',
            r'(?i)incredible',
            r'(?i)unbelievable',
            r'(?i)amazing',
            r'(?i)jaw-?dropping'
        ]
        
        clickbait_count = sum(1 for pattern in clickbait_patterns if re.search(pattern, text))
        clickbait_score = max(0, 100 - (clickbait_count * 20))
        
        # Fake news indicators from AI analysis
        fake_indicators = len(ai_analysis['pattern_matches']) + len(ai_analysis['scientific_impossibilities'])
        
        # Adjust for credibility indicators if they exist
        credibility_indicators = ai_analysis.get('credibility_indicators', [])
        credibility_boost = len(credibility_indicators) * 10
        
        fake_indicators_score = max(0, min(100, 100 - (fake_indicators * 15) + credibility_boost))
        
        # Calculate overall source credibility
        source_credibility = (fake_indicators_score * 0.7) + (clickbait_score * 0.3)
        
        # Calculate fact density (simplified)
        fact_patterns = [
            r'\d+%',  # Percentage
            r'\d+ (people|persons)',  # Count of people
            r'(according to|cited by|reported by)',  # Citations
            r'(study|research|survey|poll) (shows|found|suggests|indicates)',  # Research references
            r'(in|last|this) (year|month|week)'  # Time references
        ]
        
        fact_count = sum(1 for pattern in fact_patterns if re.search(pattern, text))
        fact_density = min(100, fact_count * 10)
        
        return {
            'source_credibility': round(source_credibility),
            'fact_density': round(fact_density),
            'sentiment_score': round(sentiment_score),
            'clickbait_score': round(clickbait_score),
            'text_quality': round(length_score)
        }

    def _generate_conclusion(self, ai_analysis):
        """
        Generate a conclusion based on the AI analysis
        """
        credibility_score = ai_analysis['credibility_score']
        pattern_matches = ai_analysis['pattern_matches']
        impossibilities = ai_analysis['scientific_impossibilities']
        
        if credibility_score >= 80:
            if not pattern_matches and not impossibilities:
                return "This content appears to be credible with no suspicious patterns detected."
            else:
                return "This content appears mostly credible but contains some elements that warrant verification."
        elif credibility_score >= 60:
            return "This content contains some questionable elements. Verify with trusted sources before sharing."
        elif credibility_score >= 40:
            return "This content contains several suspicious elements commonly found in misleading articles. Be skeptical."
        elif credibility_score >= 20:
            return "This content contains elements commonly found in fake news articles. Be skeptical and verify with trusted sources."
        else:
            return "This content contains many red flags typical of fake or highly misleading news. Extreme skepticism is warranted."
