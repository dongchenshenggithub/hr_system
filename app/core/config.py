from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
#DATABASE_URL = f"sqlite:///{BASE_DIR / 'hr.db'}"
#DATABASE_URL = f"sqlite:///{BASE_DIR / 'data' / 'hr.db'}"
DATABASE_URL =  os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'hr.db'}",
        )
