"""Vercel serverless entrypoint for Udhyami Yojna FastAPI application."""
import sys
from pathlib import Path

# Add repository root to Python path so 'backend' module is importable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.main import app
