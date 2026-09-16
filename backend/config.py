"""Application configuration for Udhyami Yojna."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
STATIC_DIR = BASE_DIR / "static"


class Settings(BaseSettings):
    """Configuration settings loaded from environment or defaults."""
    APP_NAME: str = "Udhyami Yojna"
    APP_TAGLINE: str = "Government Scheme Discovery Platform for Marginalized Entrepreneurs"
    VERSION: str = "1.0.0"

    # Gemini AI configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # CORS configuration
    ALLOWED_ORIGINS_RAW: str = os.getenv("ALLOWED_ORIGINS", "*")

    @property
    def allowed_origins(self) -> list[str]:
        if not self.ALLOWED_ORIGINS_RAW or self.ALLOWED_ORIGINS_RAW.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

    # Data files
    SCHEMES_FILE: Path = DATA_DIR / "schemes.json"
    STATES_FILE: Path = DATA_DIR / "states.json"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")


settings = Settings()
