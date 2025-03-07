import os
import sys
from tavily import TavilyClient

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TAVILY_API_KEY, MAX_RESEARCH_RESULTS

class ResearchTools:
    def __init__(self):
        """Initialize research tools with API clients"""
        self.tavily = TavilyClient(api_key=TAVILY_API_KEY)

    def web_search(self, query, max_results=None):
        """
        Perform web search using Tavily
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            list: Search results
        """
        try:
            if max_results is None:
                max_results = MAX_RESEARCH_RESULTS
                
            results = self.tavily.search(query, max_results=max_results)
            return results.get('results', [])
        except Exception as e:
            print(f"Web search error: {str(e)}")
            return []

    def extract_key_information(self, results):
        """
        Extract and format key information from search results
        
        Args:
            results (list): Raw search results
            
        Returns:
            list: Formatted search results
        """
        return [{
            'title': r.get('title', ''),
            'url': r.get('url', ''),
            'content': r.get('content', '')[:500] + '...' if r.get('content') else ''
        } for r in results] 