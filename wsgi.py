import os, sys
from pathlib import Path

# Añade la carpeta del proyecto al PYTHONPATH
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Variables de entorno (opcional)
os.environ.setdefault("APP_TIMEZONE", "America/Santiago")

# Expone la aplicación WSGI
from app import app as application