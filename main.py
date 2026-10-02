import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from database import init_db
from routes import router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database tables
    init_db()
    print("🚀 FitBuddy DB initialized successfully.")
    yield

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="Full-stack AI fitness plan & nutrition generator powered by FastAPI and Google Gemini models.",
    version="1.0.0",
    lifespan=lifespan
)

# Ensure static/images directory exists
os.makedirs("static/images", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include application routes
app.include_router(router)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    print(f"⚡ Starting FitBuddy server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
