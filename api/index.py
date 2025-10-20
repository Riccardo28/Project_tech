import sys
from pathlib import Path
from mangum import Mangum

# Add backend and parent directories to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
backend_dir = parent_dir / "backend"

sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from main import app

# Mangum adapter for Vercel serverless
handler = Mangum(app, lifespan="off")
