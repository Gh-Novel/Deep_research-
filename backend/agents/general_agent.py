import os
import sys
from langchain_groq import ChatGroq

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tools import ResearchTools
from config import GROQ_API_KEY, GENERAL_MODEL, MAX_RESEARCH_RESULTS

class GeneralAgent:
    def __init__(self):
        """Initialize the general agent with LLM and research tools"""
        self.llm = ChatGroq(
            temperature=0.3,
            model_name=GENERAL_MODEL,
            groq_api_key=GROQ_API_KEY
        )
        self.research_tools = ResearchTools()

    def handle_query(self, state):
        """
        Handle general research queries
        
        Args:
            state (dict): Contains the query and other state information
                - query: The research query
                - site_count: Number of sites to search (5-20)
            
        Returns:
            dict: Result, sources, and images
        """
        query = state["query"]
        site_count = state.get("site_count", 5)  # Default to 5 if not specified
        
        print(f"Handling general query: {query}")
        print(f"Using site count: {site_count}")
        
        # Perform web search with specified site count
        results = self.research_tools.web_search(query, max_results=min(site_count, MAX_RESEARCH_RESULTS))
        processed = self.research_tools.extract_key_information(results)
        
        # Generate response using LLM
        prompt = f"""Answer the following query concisely and accurately:
        
        QUERY: {query}
        
        RESEARCH DATA:
        {processed}
        
        Provide a well-structured response with clear sections and bullet points where appropriate.
        Note: This research is based on data from {len(processed)} different sources.
        """
        
        response = self.llm.invoke(prompt)
        
        return {
            "result": response.content,
            "sources": processed,
            "images": []
        } 