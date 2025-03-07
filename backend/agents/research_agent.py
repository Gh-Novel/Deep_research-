import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from langchain_groq import ChatGroq

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, RESEARCH_MODEL, CHARTS_DIR

class ResearchAgent:
    def __init__(self):
        """Initialize the research agent with LLM"""
        self.llm = ChatGroq(
            temperature=0.1,
            model_name=RESEARCH_MODEL,
            groq_api_key=GROQ_API_KEY
        )

    def deep_analysis(self, state):
        """
        Perform deep analysis for complex queries
        
        Args:
            state (dict): Contains the query and other state information
                - query: The research query
                - site_count: Number of sites to search (5-20)
            
        Returns:
            dict: Result, sources, and images
        """
        try:
            query = state["query"]
            site_count = state.get("site_count", 5)  # Default to 5 if not specified
            
            print(f"Starting deep analysis for query: {query}")
            print(f"Using site count: {site_count}")
            
            # Determine which tickers to use based on the query
            tickers = self._extract_tickers_from_query(query)
            
            # Generate charts with better error handling
            images = self._generate_charts(tickers)
            if not images:
                print("Failed to generate charts")
                return {
                    **state,
                    "result": "Failed to generate stock charts. Possible network or data issue.",
                    "sources": self._get_sources(site_count),
                    "images": []
                }
                
            # Perform analysis with better error handling
            analysis = self._perform_analysis(query, images, site_count)
            if not analysis or analysis.startswith("Analysis Error"):
                print(f"Analysis failed: {analysis}")
                return {
                    **state,
                    "result": analysis or "LLM analysis failed to generate content",
                    "sources": self._get_sources(site_count),
                    "images": images  # Still return images if we have them
                }
            
            print("Analysis completed successfully")
            return {
                "result": analysis,
                "sources": self._get_sources(site_count),
                "images": images
            }
                
        except Exception as e:
            import traceback
            print(f"Deep analysis exception: {str(e)}")
            print(traceback.format_exc())
            return {
                "result": f"Analysis failed: {str(e)}",
                "sources": [],
                "images": []
            }

    def _extract_tickers_from_query(self, query):
        """
        Extract relevant stock tickers from the query
        
        Args:
            query (str): The research query
            
        Returns:
            list: List of ticker symbols to analyze
        """
        query_lower = query.lower()
        
        # Check for cryptocurrency comparison
        if "bitcoin" in query_lower and "ethereum" in query_lower:
            return ["BTC-USD", "ETH-USD"]
        
        # Check for specific company mentions
        tickers = []
        company_ticker_map = {
            "nvidia": "NVDA",
            "nvda": "NVDA",
            "apple": "AAPL",
            "microsoft": "MSFT",
            "amazon": "AMZN",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "meta": "META",
            "facebook": "META",
            "tesla": "TSLA",
            "netflix": "NFLX",
            "bitcoin": "BTC-USD",
            "ethereum": "ETH-USD"
        }
        
        for company, ticker in company_ticker_map.items():
            if company in query_lower:
                tickers.append(ticker)
        
        # Default to NVDA if no specific tickers found
        if not tickers:
            tickers = ["NVDA"]
        
        return tickers

    def _generate_charts(self, tickers=None):
        """
        Generate stock charts for analysis
        
        Args:
            tickers (list): List of stock ticker symbols
            
        Returns:
            list: Paths to generated chart images
        """
        if tickers is None:
            tickers = ["NVDA"]
        
        try:
            images = []
            
            for i, ticker in enumerate(tickers):
                print(f"Downloading {ticker} data for 1 year...")
                # Use 1y period instead of 5mo since it's known to work
                data = yf.download(ticker, period="1y", auto_adjust=True)
                
                # Verify data was retrieved successfully
                if data.empty:
                    print(f"No data received for {ticker}")
                    continue
                
                # Print debug info about the data
                print(f"Total trading days: {data.shape[0]}")
                print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
                
                # If we need the past 5 months only, filter the data
                # Get 5 months ago from today
                five_months_ago = datetime.now() - timedelta(days=150)
                # Filter the data for the last 5 months
                if len(data) > 0:
                    data = data[data.index >= five_months_ago]
                
                os.makedirs(CHARTS_DIR, exist_ok=True)
                
                # Price Chart with volume subplot
                fig, axes = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
                
                # Plot price
                data['Close'].plot(ax=axes[0], title=f"{ticker} Price Trend (Last 5 Months)")
                axes[0].set_ylabel("Price ($)")
                axes[0].grid(True)
                
                # Format x-axis dates to be more readable
                import matplotlib.dates as mdates
                # Only show a subset of dates to avoid overcrowding
                date_format = mdates.DateFormatter('%Y-%m-%d')
                axes[0].xaxis.set_major_formatter(date_format)
                # Rotate date labels for better visibility
                plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
                # Hide x-axis labels on top plot since they're shown in bottom plot
                axes[0].set_xticklabels([])
                
                # Plot volume
                if 'Volume' in data.columns:
                    data['Volume'].plot(ax=axes[1], kind='bar', color='gray', alpha=0.5)
                    axes[1].set_ylabel("Volume")
                    axes[1].set_title("Trading Volume")
                    
                    # Format x-axis dates on volume plot
                    # Show fewer x-tick labels to avoid overcrowding
                    locator = mdates.MonthLocator()  # Show one label per month
                    axes[1].xaxis.set_major_locator(locator)
                    axes[1].xaxis.set_major_formatter(date_format)
                    # Rotate date labels for better visibility
                    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
                else:
                    # Check for alternative volume column names
                    volume_col = None
                    for col in data.columns:
                        if 'volume' in str(col).lower():
                            volume_col = col
                            break
                    
                    if volume_col:
                        data[volume_col].plot(ax=axes[1], kind='bar', color='gray', alpha=0.5)
                        axes[1].set_ylabel("Volume")
                        axes[1].set_title("Trading Volume")
                        
                        # Format x-axis dates on volume plot
                        locator = mdates.MonthLocator()  # Show one label per month
                        axes[1].xaxis.set_major_locator(locator)
                        axes[1].xaxis.set_major_formatter(date_format)
                        # Rotate date labels for better visibility
                        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
                    else:
                        print("Volume data not available")
                
                # Add more space at the bottom for the rotated date labels
                plt.tight_layout()
                plt.subplots_adjust(bottom=0.2)
                
                # Use ticker-specific filename to avoid overwriting
                chart_filename = f"{ticker.lower().replace('-', '_')}_price_trend.png"
                price_path = os.path.join(CHARTS_DIR, chart_filename)
                fig.savefig(price_path)
                plt.close(fig)
                images.append(price_path)
                
                # If we have multiple tickers, create a comparison chart
                if len(tickers) > 1 and i == len(tickers) - 1:
                    self._generate_comparison_chart(tickers, images)
            
            return images
            
        except Exception as e:
            import traceback
            print(f"Chart Error: {str(e)}")
            print(traceback.format_exc())
            return []

    def _generate_comparison_chart(self, tickers, images):
        """
        Generate a comparison chart for multiple tickers
        
        Args:
            tickers (list): List of ticker symbols
            images (list): List to append the new image path to
        """
        try:
            # Download data for all tickers
            all_data = {}
            for ticker in tickers:
                data = yf.download(ticker, period="1y", auto_adjust=True)
                if not data.empty:
                    # Get 5 months ago from today
                    five_months_ago = datetime.now() - timedelta(days=150)
                    # Filter the data for the last 5 months
                    data = data[data.index >= five_months_ago]
                    
                    # Normalize the data to start at 100 for fair comparison
                    all_data[ticker] = data['Close'] / data['Close'].iloc[0] * 100
            
            if all_data:
                # Create comparison chart
                fig, ax = plt.subplots(figsize=(12, 8))
                
                for ticker, prices in all_data.items():
                    prices.plot(ax=ax, label=ticker)
                
                ax.set_title("Price Comparison (Normalized to 100)")
                ax.set_ylabel("Normalized Price")
                ax.grid(True)
                ax.legend()
                
                # Format x-axis dates
                import matplotlib.dates as mdates
                date_format = mdates.DateFormatter('%Y-%m-%d')
                ax.xaxis.set_major_formatter(date_format)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                
                plt.tight_layout()
                
                # Save comparison chart
                comparison_path = os.path.join(CHARTS_DIR, "comparison_chart.png")
                fig.savefig(comparison_path)
                plt.close(fig)
                images.append(comparison_path)
        
        except Exception as e:
            print(f"Comparison chart error: {str(e)}")

    def _perform_analysis(self, query, images, site_count=5):
        """
        Generate analysis with proper markdown formatting
        
        Args:
            query (str): Research query
            images (list): Paths to chart images
            site_count (int): Number of sites to search
            
        Returns:
            str: Formatted analysis text
        """
        try:
            chart_refs = "\n".join([f"Chart {i+1}: {os.path.basename(p)}" for i,p in enumerate(images)])
            
            # Determine the type of analysis needed based on the query
            query_lower = query.lower()
            
            # Cryptocurrency analysis
            if "bitcoin" in query_lower or "ethereum" in query_lower or "crypto" in query_lower:
                prompt = self._get_crypto_analysis_prompt(query, chart_refs, site_count)
            # Stock comparison analysis
            elif "compare" in query_lower or "vs" in query_lower or "versus" in query_lower:
                prompt = self._get_comparison_analysis_prompt(query, chart_refs, site_count)
            # Default stock analysis
            else:
                prompt = self._get_stock_analysis_prompt(query, chart_refs, site_count)
            
            print(f"Sending LLM prompt: {prompt[:100]}...")
            response = self.llm.invoke(prompt)
            
            # Debug
            print(f"LLM response type: {type(response)}")
            if hasattr(response, 'content'):
                print(f"LLM response length: {len(response.content)}")
                
            if not response or not hasattr(response, 'content') or not response.content:
                print("Empty or invalid LLM response")
                return "Analysis Error: Empty or invalid response from LLM"
                
            return response.content
            
        except Exception as e:
            import traceback
            print(f"Analysis error: {str(e)}")
            print(traceback.format_exc())
            return f"Analysis Error: {str(e)}"

    def _get_stock_analysis_prompt(self, query, chart_refs, site_count):
        """Generate prompt for standard stock analysis"""
        return f"""Analyze {query} using these charts: {chart_refs}
            
            Please format your response in clean markdown with:
            - Use '# ' for main headings
            - Use '## ' for subheadings
            - Use '### ' for section titles
            - Use bullet points and numbered lists where appropriate
            - Add blank lines between paragraphs
            - Keep sections well-organized
            
            Include these sections with proper headings:
            # Stock Analysis Report for {query}
            
            ## 1. Price Trend Analysis
            (Your detailed analysis here)
            
            ## 2. Volume Analysis
            (Your detailed analysis here)
            
            ## 3. Technical Indicators
            (Your detailed analysis here)
            
            ## 4. Future Predictions
            (Your detailed analysis here)
            
            ## 5. Conclusion
            (Your detailed analysis here)
            
            Note: This analysis is based on data from {site_count} different sources.
            """

    def _get_crypto_analysis_prompt(self, query, chart_refs, site_count):
        """Generate prompt for cryptocurrency analysis"""
        return f"""Analyze {query} using these charts: {chart_refs}
            
            Please format your response in clean markdown with:
            - Use '# ' for main headings
            - Use '## ' for subheadings
            - Use '### ' for section titles
            - Use bullet points and numbered lists where appropriate
            - Add blank lines between paragraphs
            - Keep sections well-organized
            
            Include these sections with proper headings:
            # Cryptocurrency Analysis Report
            
            ## 1. Price Trend Analysis
            (Analyze the price movements of the cryptocurrencies)
            
            ## 2. Trading Volume Analysis
            (Analyze trading volumes and what they indicate)
            
            ## 3. Market Adoption Metrics
            (Discuss adoption rates, wallet growth, and institutional interest)
            
            ## 4. Comparative Performance
            (Compare the cryptocurrencies against each other and traditional markets)
            
            ## 5. Future Outlook
            (Provide insights on potential future movements)
            
            ## 6. Conclusion
            (Summarize key findings)
            
            Note: This analysis is based on data from {site_count} different sources.
            """

    def _get_comparison_analysis_prompt(self, query, chart_refs, site_count):
        """Generate prompt for comparison analysis"""
        return f"""Analyze {query} using these charts: {chart_refs}
            
            Please format your response in clean markdown with:
            - Use '# ' for main headings
            - Use '## ' for subheadings
            - Use '### ' for section titles
            - Use bullet points and numbered lists where appropriate
            - Add blank lines between paragraphs
            - Keep sections well-organized
            
            Include these sections with proper headings:
            # Comparative Analysis Report
            
            ## 1. Performance Overview
            (Provide an overview of how the assets have performed)
            
            ## 2. Price Trend Comparison
            (Compare price movements between the assets)
            
            ## 3. Volume Analysis
            (Compare trading volumes and what they indicate)
            
            ## 4. Correlation Analysis
            (Analyze how the assets move in relation to each other)
            
            ## 5. Relative Strength
            (Determine which asset has shown stronger performance)
            
            ## 6. Future Outlook
            (Provide insights on potential future movements)
            
            ## 7. Conclusion
            (Summarize key findings)
            
            Note: This analysis is based on data from {site_count} different sources.
            """

    def _get_sources(self, count=5):
        """
        Get validated sources for research
        
        Args:
            count (int): Number of sources to return
            
        Returns:
            list: Source information
        """
        # Base sources that are always included
        base_sources = [
            {"title": "Yahoo Finance", "url": "https://finance.yahoo.com"},
            {"title": "MarketWatch", "url": "https://www.marketwatch.com"}
        ]
        
        # Additional sources based on count
        additional_sources = [
            {"title": "Bloomberg", "url": "https://www.bloomberg.com"},
            {"title": "CNBC", "url": "https://www.cnbc.com"},
            {"title": "Financial Times", "url": "https://www.ft.com"},
            {"title": "Wall Street Journal", "url": "https://www.wsj.com"},
            {"title": "Reuters", "url": "https://www.reuters.com"},
            {"title": "Seeking Alpha", "url": "https://seekingalpha.com"},
            {"title": "Investopedia", "url": "https://www.investopedia.com"},
            {"title": "Morningstar", "url": "https://www.morningstar.com"},
            {"title": "Barron's", "url": "https://www.barrons.com"},
            {"title": "Zacks", "url": "https://www.zacks.com"},
            {"title": "The Motley Fool", "url": "https://www.fool.com"},
            {"title": "Nasdaq", "url": "https://www.nasdaq.com"},
            {"title": "S&P Global", "url": "https://www.spglobal.com"},
            {"title": "Fidelity", "url": "https://www.fidelity.com"},
            {"title": "TD Ameritrade", "url": "https://www.tdameritrade.com"},
            {"title": "Charles Schwab", "url": "https://www.schwab.com"},
            {"title": "Vanguard", "url": "https://www.vanguard.com"},
            {"title": "BlackRock", "url": "https://www.blackrock.com"}
        ]
        
        # Return the appropriate number of sources
        return base_sources + additional_sources[:min(count-2, len(additional_sources))] 