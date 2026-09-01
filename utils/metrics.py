import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Ensure necessary NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class CredibilityMetrics:
    def __init__(self):
        """Initialize the metrics analyzer"""
        # Manipulative language patterns
        self.manipulative_patterns = [
            r'(?i)you won\'t believe',
            r'(?i)shocking',
            r'(?i)mind-blowing',
            r'(?i)secret',
            r'(?i)they don\'t want you to know',
            r'(?i)doctors hate',
            r'(?i)miracle',
            r'(?i)exclusive',
            r'(?i)breaking',
            r'(?i)urgent',
            r'(?i)must see',
            r'(?i)unbelievable',
            r'(?i)jaw-dropping',
            r'(?i)amazing',
            r'(?i)incredible',
            r'(?i)insane',
            r'(?i)this will blow your mind',
            r'(?i)you\'ll never guess',
            r'(?i)what happens next will shock you',
            r'(?i)they tried to hide this',
            r'(?i)the truth exposed',
            r'(?i)what they don\'t want you to see'
        ]
        
        # Opinion words for bias detection
        self.opinion_words = [
            'believe', 'think', 'feel', 'opinion', 'should', 'must', 
            'always', 'never', 'best', 'worst', 'terrible', 'amazing',
            'obviously', 'clearly', 'undoubtedly', 'certainly', 'absolutely',
            'definitely', 'surely', 'undeniably', 'unquestionably', 'arguably',
            'supposedly', 'allegedly', 'apparently', 'seemingly', 'evidently',
            'presumably', 'ostensibly', 'purportedly', 'reputedly', 'reportedly'
        ]
        
        # Source reliability database (expanded)
        self.source_reliability = {
            # Major international news sources
            'bbc.com': 95,
            'bbc.co.uk': 95,
            'reuters.com': 96,
            'apnews.com': 96,
            'bloomberg.com': 93,
            'economist.com': 92,
            'ft.com': 93,
            'wsj.com': 91,
            
            # US news sources
            'nytimes.com': 92,
            'washingtonpost.com': 90,
            'latimes.com': 89,
            'npr.org': 91,
            'pbs.org': 92,
            'usatoday.com': 85,
            'cnn.com': 84,
            'nbcnews.com': 86,
            'cbsnews.com': 86,
            'abcnews.go.com': 85,
            'foxnews.com': 75,
            'msnbc.com': 78,
            
            # UK news sources
            'theguardian.com': 91,
            'independent.co.uk': 87,
            'telegraph.co.uk': 86,
            'thetimes.co.uk': 88,
            'dailymail.co.uk': 65,
            'express.co.uk': 68,
            'mirror.co.uk': 70,
            
            # Indian news sources
            'timesofindia.com': 85,
            'thehindu.com': 88,
            'hindustantimes.com': 86,
            'indianexpress.com': 86,
            'ndtv.com': 83,
            'news18.com': 80,
            
            # Other sources
            'buzzfeed.com': 70,
            'huffpost.com': 78,
            'vox.com': 80,
            'breitbart.com': 60,
            'infowars.com': 30,
            'theonion.com': 20,  # Satire
            'snopes.com': 92,    # Fact-checking
            'factcheck.org': 93, # Fact-checking
            'politifact.com': 92 # Fact-checking
        }
        
        # Academic and scientific sources
        academic_sources = [
            'nature.com', 'science.org', 'sciencedirect.com', 'springer.com', 
            'wiley.com', 'cell.com', 'nejm.org', 'thelancet.com', 'bmj.com',
            'pnas.org', 'nih.gov', 'cdc.gov', 'who.int', 'ieee.org', 'acm.org'
        ]
        
        # Add academic sources with high reliability
        for source in academic_sources:
            self.source_reliability[source] = 95
        
        # Stop words for text analysis
        self.stop_words = set(stopwords.words('english'))
    
    def get_sentiment_score(self, text):
        """
        Analyze the sentiment of the text
        Returns a score between -100 (very negative) and 100 (very positive)
        """
        # Enhanced sentiment analysis with more words
        positive_words = [
            'good', 'great', 'excellent', 'positive', 'amazing', 'wonderful', 
            'best', 'happy', 'correct', 'successful', 'legitimate', 'true',
            'accurate', 'factual', 'proven', 'verified', 'confirmed', 'authentic',
            'reliable', 'trustworthy', 'credible', 'valid', 'honest', 'genuine',
            'beneficial', 'helpful', 'effective', 'useful', 'valuable', 'important'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'negative', 'horrible', 'worst',
            'sad', 'wrong', 'fail', 'fake', 'false', 'hoax', 'conspiracy',
            'misleading', 'deceptive', 'fraudulent', 'dishonest', 'untrustworthy',
            'unreliable', 'biased', 'manipulative', 'propaganda', 'misinformation',
            'disinformation', 'inaccurate', 'unverified', 'unconfirmed', 'dubious',
            'questionable', 'suspicious', 'problematic', 'controversial'
        ]
        
        text_lower = text.lower()
        words = word_tokenize(text_lower)
        
        # Remove stop words
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Count positive and negative words
        positive_count = sum(1 for word in filtered_words if word in positive_words)
        negative_count = sum(1 for word in filtered_words if word in negative_words)
        
        # Calculate sentiment score
        total = positive_count + negative_count
        if total == 0:
            base_score = 0
        else:
            base_score = ((positive_count - negative_count) / total) * 100
        
        # Add some randomness but less than before
        variation = random.uniform(-5, 5)
        score = base_score + variation
        
        # Ensure score is between -100 and 100
        score = max(-100, min(100, score))
        
        return round(score, 1)
    
    def get_bias_score(self, text):
        """
        Analyze the bias in the text
        Returns a score between 0 (neutral) and 100 (highly biased)
        """
        text_lower = text.lower()
        words = word_tokenize(text_lower)
        
        # Remove stop words
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Count opinion words
        opinion_count = sum(1 for word in filtered_words if word in self.opinion_words)
        
        # Check for first-person pronouns (indicates personal opinion)
        first_person_pronouns = ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
        first_person_count = sum(1 for word in filtered_words if word in first_person_pronouns)
        
        # Calculate base score
        word_ratio = opinion_count / max(1, len(filtered_words))
        base_score = min(100, (word_ratio * 300) + (first_person_count * 5))
        
        # Add some randomness but less than before
        variation = random.uniform(-5, 5)
        score = max(0, min(100, base_score + variation))
        
        return round(score, 1)
    
    def get_fact_check_confidence(self, text):
        """
        Analyze the confidence in fact-checking the text
        Returns a score between 0 (low confidence) and 100 (high confidence)
        """
        # Look for specific, verifiable claims
        has_numbers = bool(re.search(r'\d+', text))
        has_quotes = bool(re.search(r'["\'](.*?)["\']', text))
        has_names = bool(re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', text))
        
        # Check for citations and references
        has_citations = bool(re.search(r'(?i)(according to|cited by|reported by|referenced by|source|study|research)', text))
        has_dates = bool(re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}\b', text))
        has_statistics = bool(re.search(r'\d+(\.\d+)?%', text))
        
        # Each factor adds to confidence
        base_score = 40
        if has_numbers:
            base_score += 10
        if has_quotes:
            base_score += 10
        if has_names:
            base_score += 10
        if has_citations:
            base_score += 15
        if has_dates:
            base_score += 10
        if has_statistics:
            base_score += 15
        
        # Add some randomness but less than before
        variation = random.uniform(-5, 5)
        score = max(0, min(100, base_score + variation))
        
        return round(score, 1)
    
    def get_manipulative_language_score(self, text):
        """
        Analyze the text for manipulative language
        Returns a score between 0 (not manipulative) and 100 (highly manipulative)
        """
        text_lower = text.lower()
        
        # Count matches for manipulative patterns
        pattern_count = 0
        for pattern in self.manipulative_patterns:
            if re.search(pattern, text_lower):
                pattern_count += 1
        
        # Calculate score based on the ratio of patterns to text length
        words = word_tokenize(text_lower)
        word_count = len(words)
        
        # Adjust score based on text length
        if word_count > 0:
            pattern_ratio = pattern_count / (word_count / 100)  # Normalize for 100 words
            base_score = min(100, pattern_ratio * 50)
        else:
            base_score = 0
        
        # Add some randomness but less than before
        variation = random.uniform(-3, 3)
        score = max(0, min(100, base_score + variation))
        
        return round(score, 1)
    
    def get_source_reliability_score(self, text):
        """
        Estimate the reliability of the source based on mentioned domains
        Returns a score between 0 (unreliable) and 100 (highly reliable)
        """
        # Extract domain names from the text
        domains = re.findall(r'https?://(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', text)
        domains.extend(re.findall(r'(?<!\S)([a-zA-Z0-9-]+\.(?:com|org|net|edu|gov|co\.uk|co\.in|io|ai))\b', text))
        
        # If no domains found, return a neutral score
        if not domains:
            return 50.0
        
        # Calculate average reliability of found domains
        reliability_scores = []
        for domain in domains:
            domain_lower = domain.lower()
            if domain_lower in self.source_reliability:
                reliability_scores.append(self.source_reliability[domain_lower])
            else:
                # For unknown domains, assign a slightly below neutral score
                reliability_scores.append(45)
        
        avg_score = sum(reliability_scores) / len(reliability_scores)
        
        return round(avg_score, 1)
    
    def get_detailed_metrics(self, text):
        """
        Get all detailed metrics for the news text
        Returns a dictionary of metrics
        """
        return {
            'sentiment_score': self.get_sentiment_score(text),
            'bias_score': self.get_bias_score(text),
            'fact_check_confidence': self.get_fact_check_confidence(text),
            'manipulative_language': self.get_manipulative_language_score(text),
            'source_reliability': self.get_source_reliability_score(text)
        }
