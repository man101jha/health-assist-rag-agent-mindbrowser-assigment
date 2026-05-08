from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import ingest
from app.routers import ask


settings=get_settings()

app=FastAPI(
    title=settings.APP_NAME,
    description="Healthcare RAG Assistant",
    version="1.0.0"
)
app.include_router(ingest.router)
app.include_router(ask.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "1.0.0"

    }

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")

# Serve Angular Static Files
if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_angular(full_path: str):
        # Skip API routes
        if full_path.startswith(("ask", "ingest", "health")):
            return None
            
        # If the path exists in static, serve it (for .js, .css files)
        file_path = os.path.join("static", full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Otherwise, serve index.html (for Angular routing)
        return FileResponse("static/index.html")
