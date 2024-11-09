# /backend/agents/news.py
import requests

class NewsAgent:
    def fetch_local_news(self, city):
        """Fetch local news for the city that may impact visit plans."""
        api_key = 'your_newsapi_key'
        url = f"https://newsapi.org/v2/everything?q={city}&apiKey={api_key}"
        response = requests.get(url)
        news_data = response.json()
        return [article['title'] for article in news_data['articles']]
