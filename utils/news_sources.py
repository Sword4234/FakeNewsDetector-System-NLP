import random
import re
from datetime import datetime, timedelta

class NewsSourceComparison:
    def __init__(self):
        """Initialize the news source comparison module"""
        # Define trusted news sources by region
        self.trusted_sources = {
            'us': [
                {'name': 'The New York Times', 'url': 'https://www.nytimes.com', 'bias': 'center-left'},
                {'name': 'The Wall Street Journal', 'url': 'https://www.wsj.com', 'bias': 'center-right'},
                {'name': 'Reuters', 'url': 'https://www.reuters.com', 'bias': 'center'},
                {'name': 'Associated Press', 'url': 'https://apnews.com', 'bias': 'center'},
                {'name': 'NPR', 'url': 'https://www.npr.org', 'bias': 'center-left'}
            ],
            'uk': [
                {'name': 'BBC News', 'url': 'https://www.bbc.co.uk/news', 'bias': 'center'},
                {'name': 'The Guardian', 'url': 'https://www.theguardian.com', 'bias': 'center-left'},
                {'name': 'The Times', 'url': 'https://www.thetimes.co.uk', 'bias': 'center-right'},
                {'name': 'Financial Times', 'url': 'https://www.ft.com', 'bias': 'center'},
                {'name': 'The Independent', 'url': 'https://www.independent.co.uk', 'bias': 'center-left'}
            ],
            'eu': [
                {'name': 'Deutsche Welle', 'url': 'https://www.dw.com', 'bias': 'center'},
                {'name': 'Euronews', 'url': 'https://www.euronews.com', 'bias': 'center'},
                {'name': 'France 24', 'url': 'https://www.france24.com', 'bias': 'center'},
                {'name': 'Politico EU', 'url': 'https://www.politico.eu', 'bias': 'center'},
                {'name': 'The Local', 'url': 'https://www.thelocal.eu', 'bias': 'center'}
            ],
            'asia': [
                {'name': 'South China Morning Post', 'url': 'https://www.scmp.com', 'bias': 'center'},
                {'name': 'The Japan Times', 'url': 'https://www.japantimes.co.jp', 'bias': 'center'},
                {'name': 'The Straits Times', 'url': 'https://www.straitstimes.com', 'bias': 'center'},
                {'name': 'Al Jazeera', 'url': 'https://www.aljazeera.com', 'bias': 'center-left'},
                {'name': 'The Hindu', 'url': 'https://www.thehindu.com', 'bias': 'center-left'}
            ]
        }
        
        # Default to US sources if region not found
        self.default_region = 'us'

    def get_available_regions(self):
        """Return list of available regions"""
        return list(self.trusted_sources.keys())

    def get_sources_for_region(self, region):
        """Return sources for a given region"""
        return self.trusted_sources.get(region, self.trusted_sources[self.default_region])
    
    def get_related_articles(self, news_text, region='us'):
        """
        Get related articles from trusted sources for the given news text and region
        """
        # Ensure region is valid, default to US if not
        if region not in self.trusted_sources:
            region = self.default_region
        
        # Extract keywords from the news text
        keywords = self._extract_keywords(news_text)
        
        # Get sources for the region
        sources = self.trusted_sources[region]
        
        # Select 3 random sources
        selected_sources = random.sample(sources, min(3, len(sources)))
        
        # Generate related articles
        articles = []
        
        for source in selected_sources:
            # Generate a unique article for each source
            article = self._generate_article(news_text, keywords, source)
            articles.append(article)
        
        return {
            'region': region,
            'articles': articles
        }
    
    def _extract_keywords(self, text):
        """Extract important keywords from the text"""
        # Simple keyword extraction
        words = re.findall(r'\b[A-Za-z]{4,}\b', text)
        
        # Remove common words
        common_words = {'about', 'after', 'again', 'also', 'another', 'because', 'before', 'between', 'could', 'every', 'from', 'their', 'there', 'these', 'thing', 'think', 'this', 'those', 'through', 'what', 'when', 'where', 'which', 'while', 'with', 'would', 'your'}
        
        filtered_words = [word for word in words if word.lower() not in common_words]
        
        # Get unique words and limit to 10
        unique_words = list(set(filtered_words))
        keywords = unique_words[:10] if len(unique_words) > 10 else unique_words
        
        return keywords
    
    def _generate_article(self, original_text, keywords, source):
        """Generate a related article from a trusted source"""
        # Extract the first 150 characters as a base for the title
        base_text = original_text[:150].strip()
        
        # Create a unique title for each source
        if source['bias'] == 'center-left':
            # More progressive perspective
            title = self._generate_progressive_title(base_text, keywords)
        elif source['bias'] == 'center-right':
            # More conservative perspective
            title = self._generate_conservative_title(base_text, keywords)
        else:
            # Neutral perspective
            title = self._generate_neutral_title(base_text, keywords)
        
        # Generate a summary based on the source bias
        summary = self._generate_summary(original_text, keywords, source['bias'])
        
        # Generate a publication date (within the last week)
        days_ago = random.randint(0, 6)
        date = (datetime.now().date() - timedelta(days=days_ago)).strftime('%B %d, %Y')
        
        # Generate a URL for the article
        url = self._generate_article_url(source['url'], title)
        
        return {
            'source': source['name'],
            'title': title,
            'summary': summary,
            'date': date,
            'url': url,
            'bias': source['bias']
        }
    
    def _generate_progressive_title(self, base_text, keywords):
        """Generate a title with a progressive perspective"""
        # Extract potential subjects from the base text
        subjects = re.findall(r'\b[A-Z][a-z]+\b', base_text)
        subject = subjects[0] if subjects else 'Report'
        
        # Use keywords to create a progressive-leaning title
        if keywords:
            key = random.choice(keywords)
            templates = [
                f"Analysis: The Broader Implications of {subject}'s {key}",
                f"Understanding the Social Impact of {subject}'s Recent {key}",
                f"What {subject}'s {key} Means for Community Development",
                f"The Progressive Perspective on {subject}'s {key}",
                f"{subject}'s {key}: A Step Towards Progress?"
            ]
        else:
            templates = [
                f"Analysis: The Broader Implications of Recent {subject} Developments",
                f"Understanding the Social Impact of {subject}'s Recent Actions",
                f"What Recent {subject} Events Mean for Community Development",
                f"The Progressive Perspective on {subject}'s Recent Statements",
                f"{subject}: A Step Towards Progress?"
            ]
        
        return random.choice(templates)
    
    def _generate_conservative_title(self, base_text, keywords):
        """Generate a title with a conservative perspective"""
        # Extract potential subjects from the base text
        subjects = re.findall(r'\b[A-Z][a-z]+\b', base_text)
        subject = subjects[0] if subjects else 'Report'
        
        # Use keywords to create a conservative-leaning title
        if keywords:
            key = random.choice(keywords)
            templates = [
                f"Analysis: The Economic Implications of {subject}'s {key}",
                f"Traditional Values and {subject}'s Recent {key}",
                f"What {subject}'s {key} Means for Business and Markets",
                f"The Conservative Perspective on {subject}'s {key}",
                f"{subject}'s {key}: Balancing Innovation and Tradition"
            ]
        else:
            templates = [
                f"Analysis: The Economic Implications of Recent {subject} Developments",
                f"Traditional Values and {subject}'s Recent Actions",
                f"What Recent {subject} Events Mean for Business and Markets",
                f"The Conservative Perspective on {subject}'s Recent Statements",
                f"{subject}: Balancing Innovation and Tradition"
            ]
        
        return random.choice(templates)
    
    def _generate_neutral_title(self, base_text, keywords):
        """Generate a title with a neutral perspective"""
        # Extract potential subjects from the base text
        subjects = re.findall(r'\b[A-Z][a-z]+\b', base_text)
        subject = subjects[0] if subjects else 'Report'
        
        # Use keywords to create a neutral title
        if keywords:
            key = random.choice(keywords)
            templates = [
                f"Fact Check: {subject}'s Recent {key} Explained",
                f"Examining the Evidence: {subject}'s {key} in Context",
                f"Multiple Perspectives on {subject}'s {key}",
                f"Expert Analysis of {subject}'s Recent {key}",
                f"{subject}'s {key}: What You Need to Know"
            ]
        else:
            templates = [
                f"Fact Check: Recent {subject} Developments Explained",
                f"Examining the Evidence: {subject} in Context",
                f"Multiple Perspectives on Recent {subject} Events",
                f"Expert Analysis of {subject}'s Recent Statements",
                f"{subject}: What You Need to Know"
            ]
        
        return random.choice(templates)
    
    def _generate_summary(self, original_text, keywords, bias):
        """Generate a summary based on the source bias"""
        # Extract a portion of the original text
        max_length = min(len(original_text), 200)
        base_summary = original_text[:max_length].strip() + "..."
        
        # Add a perspective based on bias
        if bias == 'center-left':
            perspective = self._generate_progressive_perspective(keywords)
        elif bias == 'center-right':
            perspective = self._generate_conservative_perspective(keywords)
        else:
            perspective = self._generate_neutral_perspective(keywords)
        
        # Combine the base summary with the perspective
        summary = f"{base_summary} {perspective}"
        
        return summary
    
    def _generate_progressive_perspective(self, keywords):
        """Generate a progressive perspective"""
        if not keywords:
            return "Our analysis examines the social implications and community impact of these developments."
        
        key = random.choice(keywords)
        templates = [
            f"Our analysis examines the social implications of {key} and its impact on diverse communities.",
            f"Experts suggest that {key} could have significant implications for social equity and justice.",
            f"This development raises important questions about {key} in relation to community well-being and inclusivity.",
            f"Progressive analysts point to {key} as an indicator of changing social dynamics.",
            f"The social context of {key} deserves further examination from multiple perspectives."
        ]
        
        return random.choice(templates)
    
    def _generate_conservative_perspective(self, keywords):
        """Generate a conservative perspective"""
        if not keywords:
            return "Our analysis considers the economic implications and traditional values related to these developments."
        
        key = random.choice(keywords)
        templates = [
            f"Our analysis considers the economic implications of {key} and its impact on markets and businesses.",
            f"Experts suggest that {key} should be evaluated in the context of traditional values and fiscal responsibility.",
            f"This development raises important questions about {key} in relation to economic growth and stability.",
            f"Conservative analysts point to {key} as an area requiring careful consideration of costs and benefits.",
            f"The economic context of {key} deserves further examination from multiple perspectives."
        ]
        
        return random.choice(templates)
    
    def _generate_neutral_perspective(self, keywords):
        """Generate a neutral perspective"""
        if not keywords:
            return "Our fact-based analysis presents multiple perspectives on these developments, examining evidence from various sources."
        
        key = random.choice(keywords)
        templates = [
            f"Our fact-based analysis presents multiple perspectives on {key}, examining evidence from various sources.",
            f"Experts from different backgrounds offer varying interpretations of {key} and its significance.",
            f"This report aims to provide a balanced view of {key} by considering diverse expert opinions.",
            f"Analysis of {key} requires careful examination of facts and context from multiple angles.",
            f"We present various expert viewpoints on {key} to help readers form their own informed opinions."
        ]
        
        return random.choice(templates)
    
    def _generate_article_url(self, base_url, title):
        """Generate a URL for the article based on the title"""
        # Convert title to URL-friendly format
        url_title = title.lower()
        url_title = re.sub(r'[^a-z0-9\s]', '', url_title)  # Remove special characters
        url_title = re.sub(r'\s+', '-', url_title)  # Replace spaces with hyphens
        
        # Trim to reasonable length
        url_title = url_title[:50]
        
        # Add a random ID to ensure uniqueness
        random_id = random.randint(10000, 99999)
        
        # Construct the full URL
        if base_url.endswith('/'):
            article_url = f"{base_url}article/{url_title}-{random_id}"
        else:
            article_url = f"{base_url}/article/{url_title}-{random_id}"
        
        return article_url
