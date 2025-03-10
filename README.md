# Deep Research AI System
comprehensive research, data analysis, and report generation. The system leverages modern AI technologies, including LangChain and Groq LLM, Agentic AI, to provide users with in-depth analysis on a wide range of topics, with particular strength in financial and market research. An advanced AI-powered research system that leverages multiple specialized agents to perform comprehensive research, data analysis, and report generation.

![Deep Research AI System](![Screenshot 2025-03-08 004347](https://github.com/user-attachments/assets/a2ed4762-0813-494b-9d4c-4cd5b78fc097)
)

![Screenshot 2025-03-08 004422](https://github.com/user-attachments/assets/0336eb86-228a-445e-80ec-1a9090c66e41)


## Features

### Research Capabilities
- **Multi-Agent Architecture**: Specialized agents for general queries, deep research, and report generation
- **Web Research**: Comprehensive web crawling using Tavily API with configurable depth (5-20 sources)
- **Financial Analysis**: 
  - Real-time stock and cryptocurrency data analysis
  - Price trend visualization
  - Comparative performance analysis
  - Technical indicators and market insights

### User Interface
- **Dark/Light Mode**: 
  - Customizable theme preference
  - Persistent theme settings
  - Modern, responsive design
- **Search History**: 
  - Track and manage previous queries
  - One-click reuse of past searches
  - Search through history
  - Clear history option

### Data Visualization
- **Dynamic Charts**: 
  - Stock price trends
  - Cryptocurrency performance
  - Multi-asset comparisons
  - Technical analysis indicators
- **Interactive Graphs**: 
  - Zoom and pan capabilities
  - Tooltips with detailed information
  - Responsive design for all screen sizes

### Export Options
- **PDF Reports**: 
  - Professional formatting
  - Embedded charts and visualizations
  - Source citations
  - Unique filenames for easy tracking
- **Word Documents**: 
  - Editable format
  - Complete research findings
  - Charts and tables included

## Tech Stack

### Frontend
- React 18+
- Bootstrap 5
- Context API for state management
- Responsive design components

### Backend
- FastAPI
- LangChain with Groq LLM
- Matplotlib for visualizations
- ReportLab and python-docx for document generation

## Installation

### Prerequisites

1. **Python Environment**:
   - Python 3.10 or higher
   - pip package manager

2. **Node.js Environment**:
   - Node.js 14 or higher
   - npm package manager

3. **API Keys**:
   - Groq API key (for LLM)
   - Tavily API key (for web search)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Gh-Novel/Deep_research-.git
cd Deep-research
```

2. Create and activate a virtual environment (Windows):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install backend dependencies:
```powershell
cd backend
pip install -r requirements.txt
```

4. Create `.env` file in the backend directory:
```plaintext
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Frontend Setup

1. Install frontend dependencies:
```powershell
cd ../frontend
npm install
```

2. Create `.env` file in the frontend directory:
```plaintext
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend Server (Windows)

1. Navigate to backend directory:
```powershell
cd backend
```

2. Run the FastAPI server:
```powershell
python app.py
```

The backend will be available at `http://localhost:8000`

### Start Frontend Development Server

1. Navigate to frontend directory:
```powershell
cd frontend
```

2. Start the development server:
```powershell
npm start
```

The application will open automatically at `http://localhost:3000`

## Usage Guide

### Basic Research
1. Enter your query in the search box
2. Select research type:
   - **Normal**: Quick analysis with 5 sources
   - **Deep Research**: Comprehensive analysis with up to 20 sources
3. Click "Start Research"

### Financial Analysis
1. Enter stock symbols or cryptocurrency names
2. System will automatically:
   - Generate price charts
   - Compare performance
   - Analyze trends
   - Provide market insights

### Managing Results
1. View generated charts and analysis
2. Access source citations
3. Export options:
   - Generate PDF report
   - Export to Word document
4. Save to search history

### Using Search History
1. Access previous searches from history panel
2. Click on any history item to rerun the query
3. Search through history for specific queries
4. Clear individual items or entire history

## Development

### Project Structure
```
deep-research/
├── backend/
│   ├── agents/           # AI agents implementation
│   │   └── app.py           # Main FastAPI application
│   ├── routers/          # API endpoints
│   ├── utils/            # Helper functions
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── contexts/    # React contexts
│   │   ├── services/    # API services
│   │   └── assets/      # Styles and images
│   └── public/          # Static files
└── README.md
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - AI framework
- [Groq](https://groq.com/) - LLM API provider
- [Tavily](https://tavily.com/) - Web search API
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://reactjs.org/) - Frontend framework
