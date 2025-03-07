from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

# Import routers
from routers import research

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Deep Research API",
    description="API for AI-powered deep research system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router, prefix="/api")

# Mount static directories
# Ensure directories exist
os.makedirs("exports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Mount static files
app.mount("/exports", StaticFiles(directory="exports"), name="exports")
app.mount("/charts", StaticFiles(directory="charts"), name="charts")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Deep Research API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 