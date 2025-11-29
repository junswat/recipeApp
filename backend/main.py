import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for generated images
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage for jobs (replace with DB for production)
jobs = {}

class GenerateRequest(BaseModel):
    url: str

from backend.services.downloader import download_video
from backend.services.ai import analyze_recipe
from backend.services.extractor import extract_frame

def process_video(job_id: str, url: str):
    try:
        jobs[job_id]["status"] = "processing"
        
        # 1. Download Video/Metadata
        jobs[job_id]["progress"] = "Downloading video..."
        metadata = download_video(url)
        
        # 2. AI Analysis
        jobs[job_id]["progress"] = "Analyzing recipe..."
        recipe_data = analyze_recipe(metadata)
        
        # 3. Extract Images
        jobs[job_id]["progress"] = "Extracting images..."
        # Create images directory for this job
        job_dir = f"static/{job_id}"
        os.makedirs(job_dir, exist_ok=True)
        
        for i, step in enumerate(recipe_data.get("steps", [])):
            timestamp = step.get("timestamp")
            if timestamp is not None:
                image_filename = f"step_{i+1}.jpg"
                image_path = f"{job_dir}/{image_filename}"
                if extract_frame(metadata["file_path"], timestamp, image_path):
                    step["image_url"] = f"/static/{job_id}/{image_filename}"
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = recipe_data
        
        # Cleanup video file (optional, maybe keep for debugging for now)
        # os.remove(metadata["file_path"])
        
    except Exception as e:
        print(f"Job failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.post("/api/generate")
async def generate_recipe(request: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "progress": "Queued"}
    background_tasks.add_task(process_video, job_id, request.url)
    return {"job_id": job_id}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    if jobs[job_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    return jobs[job_id].get("result")

# Serve Frontend
try:
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
except RuntimeError:
    print("Warning: Frontend dist folder not found. Run 'npm run build' in frontend directory.")
