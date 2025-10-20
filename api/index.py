import sys
from pathlib import Path
from mangum import Mangum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend and parent directories to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
backend_dir = parent_dir / "backend"

sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(backend_dir))

logger.info(f"Python path configured: {sys.path[:3]}")

# Import the FastAPI app
from main import app

# Log CORS configuration
from app.core.config import settings
logger.info(f"CORS origins configured: {settings.cors_origins}")

# Mangum adapter for Vercel serverless
handler = Mangum(app, lifespan="off")
