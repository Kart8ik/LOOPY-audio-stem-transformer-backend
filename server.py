from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
import uuid
from loopy import separate_vocals

app = FastAPI()

# CORS middleware for frontend access
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", # Vite's default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a temp upload folder in your project directory
TEMP_UPLOAD_DIR = Path("temp_uploads")
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"mp3", "wav"}

@app.get("/trial")
def trial():
    return {"message": "Welcome to the loopy backend"}

@app.post("/upload-and-process")
async def upload_audio(file: UploadFile = File(...)):
    # Validate file extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .mp3 and .wav files are allowed.")

    # Generate a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = TEMP_UPLOAD_DIR / unique_filename

    # Save the uploaded file to the custom temp folder
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the file
    separate_vocals(file_path)

    # Correctly determine the output path
    unique_filename_stem = Path(unique_filename).stem
    processed_audio_path = Path(f"separated/mdx_extra/{unique_filename_stem}/no_vocals.mp3")

    if not processed_audio_path.exists():
        raise HTTPException(status_code=500, detail="Error processing file. Output not found.")

    # Return the processed audio file
    return FileResponse(path=processed_audio_path, media_type="audio/mpeg", filename="no_vocals.mp3")