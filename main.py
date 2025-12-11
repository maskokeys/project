# backend/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn
import webbrowser
import threading
import time

# Initialize FastAPI
app = FastAPI(title="Harun's Personal Website")

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

# Mount static folders
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/downloads", StaticFiles(directory=DOWNLOADS_DIR), name="downloads")
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ROUTES
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/resources", response_class=HTMLResponse)
async def resources(request: Request):
    return templates.TemplateResponse("resources.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(DOWNLOADS_DIR, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(path=file_path, filename=file_name)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/video/{video_name}")
async def get_video(video_name: str):
    video_path = os.path.join(VIDEOS_DIR, video_name)
    if os.path.exists(video_path) and os.path.isfile(video_path):
        return FileResponse(path=video_path, filename=video_name)
    raise HTTPException(status_code=404, detail="Video not found")


# ===========================
# AUTO OPEN BROWSER FUNCTION
# ===========================
def open_browser():
    """Wait a second and open the default web browser."""
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
