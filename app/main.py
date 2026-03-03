"""
Main entry point for the Groundspeed Records API.
"""

from fastapi import FastAPI                 # Third Party: Web framework
from fastapi.middleware.cors import CORSMiddleware  # Third Party: Security
from fastapi.staticfiles import StaticFiles  # Third Party: File serving
from app.database import engine             # Local: DB engine
from app import models                      # Local: DB tables
from app.routers import aircraft, records      # Local: Modular routers

# Re-create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Groundspeed Records API")

# Setup CORS for Nuxt connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (photos)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the modular routes
app.include_router(aircraft.router)
app.include_router(records.router)


@app.get("/")
def read_root():
    """Welcome message for the API."""
    return {"status": "Modular API is running."}
