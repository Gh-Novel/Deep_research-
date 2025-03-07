# Configuration constants and global settings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Research settings
MAX_RESEARCH_RESULTS = int(os.getenv("MAX_RESEARCH_RESULTS", "5"))
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.3"))

# API keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
GENERAL_MODEL = os.getenv("GENERAL_MODEL", "mixtral-8x7b-32768")
RESEARCH_MODEL = os.getenv("RESEARCH_MODEL", "llama3-70b-8192")

# File paths
CHARTS_DIR = "charts"
EXPORTS_DIR = "exports"

# Ensure directories exist
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True) 