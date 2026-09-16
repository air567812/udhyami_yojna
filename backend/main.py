"""Main FastAPI application for Udhyami Yojna.

Serves the government scheme discovery API and static web frontend.
"""
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import settings, STATIC_DIR
from backend.routers.schemes import router as schemes_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("udhyami.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Gemini API key configured: {bool(settings.GEMINI_API_KEY)}")
    logger.info(f"Static assets directory: {STATIC_DIR}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title="Udhyami Yojna (उद्यमी योजना) API",
    description=(
        "Government Scheme Discovery & AI Subsidy Matching Platform for Marginalized Indian Entrepreneurs.\n\n"
        "Features:\n"
        "- Multilingual voice extraction via Gemini AI\n"
        "- Deterministic rule-based scheme scoring & eligibility verification\n"
        "- State-wise entrepreneurial discovery hub\n"
        "- Official Central and State scheme application links and checklists"
    ),
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(schemes_router)


@app.get(
    "/api/health",
    tags=["System"],
    summary="Application health check",
    description="Returns system operational status, model configuration, and version metadata."
)
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "gemini_active": bool(settings.GEMINI_API_KEY),
        "gemini_model": settings.GEMINI_MODEL
    }


# Ensure static directories exist
try:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    css_dir = STATIC_DIR / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir = STATIC_DIR / "js"
    js_dir.mkdir(parents=True, exist_ok=True)
    images_dir = STATIC_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
except OSError:
    css_dir = STATIC_DIR / "css"
    js_dir = STATIC_DIR / "js"
    images_dir = STATIC_DIR / "images"

# Mount subdirectories for direct root referencing (/css/*, /js/*, /images/*)
if css_dir.exists():
    app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
if js_dir.exists():
    app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
if images_dir.exists():
    app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
async def serve_index():
    """Serves the single-page application entry point."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(
        {"message": "Frontend static/index.html is being prepared."},
        status_code=200
    )


@app.get("/presentation", include_in_schema=False)
@app.get("/sih_presentation.html", include_in_schema=False)
async def serve_presentation():
    """Serves the official SIH 2026 presentation web deck."""
    presentation_file = STATIC_DIR / "sih_presentation.html"
    if presentation_file.exists():
        return FileResponse(presentation_file)
    return JSONResponse({"error": "Presentation file not found"}, status_code=404)


@app.get("/download/presentation", tags=["Presentation"], summary="Download SIH 2026 PPTX")
async def download_presentation():
    """Downloads the official SIH 2026 PowerPoint (.pptx) pitch deck."""
    from backend.config import BASE_DIR
    pptx_path = BASE_DIR / "Udhyami_Yojna_SIH_2026.pptx"
    if pptx_path.exists():
        return FileResponse(
            pptx_path,
            filename="Udhyami_Yojna_SIH_2026.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    return JSONResponse({"error": "PPTX file not found"}, status_code=404)


@app.get("/download/images", tags=["Media"], summary="Download All PNG & JPG Images (ZIP)")
async def download_images_zip():
    """Downloads all project flowcharts and SIH pitch deck slides in a ZIP file."""
    from backend.config import BASE_DIR
    zip_path = BASE_DIR / "udhyami_yojna_images.zip"
    if zip_path.exists():
        return FileResponse(
            zip_path,
            filename="udhyami_yojna_images.zip",
            media_type="application/zip"
        )
    return JSONResponse({"error": "Images ZIP not found"}, status_code=404)


@app.get("/download/code", tags=["Distribution"], summary="Download Clean Source Code (ZIP)")
async def download_code_zip():
    """Downloads the complete Udhyami Yojna v1.0.0 source code in a ZIP archive."""
    from backend.config import BASE_DIR
    zip_path = BASE_DIR / "udhyami_yojna_v1.0_code.zip"
    if not zip_path.exists():
        zip_path = BASE_DIR / "udhyami_yojna_code.zip"
    if zip_path.exists():
        return FileResponse(
            zip_path,
            filename="udhyami_yojna_v1.0_code.zip",
            media_type="application/zip"
        )
    return JSONResponse({"error": "Code ZIP not found"}, status_code=404)


@app.get("/download/bundle", tags=["Distribution"], summary="Download Full Bundle (Code + Images + PPTX)")
async def download_full_bundle():
    """Downloads the full project bundle including code, PPTX, and high-resolution slides."""
    from backend.config import BASE_DIR
    zip_path = BASE_DIR / "udhyami_yojna_v1.0_full_bundle.zip"
    if zip_path.exists():
        return FileResponse(
            zip_path,
            filename="udhyami_yojna_v1.0_full_bundle.zip",
            media_type="application/zip"
        )
    return JSONResponse({"error": "Full bundle ZIP not found"}, status_code=404)


# Mount extra images subdirectories if present without shadowing /images
from backend.config import BASE_DIR
extra_images_dir = BASE_DIR / "images"
if extra_images_dir.exists() and (extra_images_dir / "png").exists():
    app.mount("/images/png", StaticFiles(directory=str(extra_images_dir / "png")), name="images_png")
if extra_images_dir.exists() and (extra_images_dir / "jpg").exists():
    app.mount("/images/jpg", StaticFiles(directory=str(extra_images_dir / "jpg")), name="images_jpg")



