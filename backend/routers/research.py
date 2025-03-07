from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import agents
from agents.general_agent import GeneralAgent
from agents.research_agent import ResearchAgent
from agents.export_agent import ExportAgent

# Create router
router = APIRouter(
    prefix="/research",
    tags=["research"],
    responses={404: {"description": "Not found"}},
)

# Models
class ResearchRequest(BaseModel):
    query: str
    search_type: str = "normal"  # "normal" or "deep"
    site_count: int = 5  # Number of sites to search (5-20)

class ResearchResponse(BaseModel):
    result: str
    sources: List[Dict[str, str]]
    images: List[str]
    status: str

class ExportRequest(BaseModel):
    content: str
    images: List[str]
    format: str = "pdf"

class ExportResponse(BaseModel):
    filepath: str
    status: str

# Initialize agents
general_agent = GeneralAgent()
research_agent = ResearchAgent()
export_agent = ExportAgent()

# Routes
@router.post("/query", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct research based on the provided query
    """
    try:
        # Validate site count
        site_count = max(5, min(20, request.site_count))  # Ensure between 5-20
        
        # Determine if this is a forced deep search or check complexity
        if request.search_type == "deep":
            analysis_type = "complex"
        else:
            # For normal search, still check if query is complex
            query_lower = request.query.lower()
            complex_keywords = ["analyze", "trend", "compare", "forecast", "technical"]
            analysis_type = "complex" if any(kw in query_lower for kw in complex_keywords) else "general"
        
        # Perform analysis based on type
        if analysis_type == "general":
            result = general_agent.handle_query({
                "query": request.query,
                "site_count": site_count
            })
        else:
            result = research_agent.deep_analysis({
                "query": request.query,
                "site_count": site_count
            })
        
        # Extract results
        return {
            "result": result.get("result", ""),
            "sources": result.get("sources", []),
            "images": result.get("images", []),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export", response_model=ExportResponse)
async def export_report(request: ExportRequest):
    """
    Export research results to PDF or Word document
    """
    try:
        if request.format.lower() == "pdf":
            filepath = export_agent.export_pdf(request.content, request.images)
        elif request.format.lower() == "docx":
            filepath = export_agent.export_word(request.content, request.images)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        # Return relative path for frontend
        relative_path = os.path.relpath(filepath, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return {
            "filepath": relative_path,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images")
async def get_images():
    """
    Get list of available chart images
    """
    try:
        charts_dir = "charts"
        if not os.path.exists(charts_dir):
            return {"images": []}
        
        images = [os.path.join(charts_dir, f) for f in os.listdir(charts_dir) if f.endswith(('.png', '.jpg'))]
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 