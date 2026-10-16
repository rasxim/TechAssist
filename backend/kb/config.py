"""Settings for the knowledge base pipeline. Read from the environment (and .env); never hardcoded."""

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
KB_PACKAGE_DIR = Path(__file__).resolve().parent
KB_DATA_DIR = REPO_ROOT / "kb_data"
GID_MAP_PATH = KB_PACKAGE_DIR / "gid_map.yaml"

load_dotenv(REPO_ROOT / ".env")


def workbook_path(override: str | None = None) -> Path:
    value = override or os.environ.get("WORKBOOK_PATH")
    if not value:
        raise SystemExit("Set WORKBOOK_PATH in .env or pass --workbook PATH.")
    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        raise SystemExit(f"Workbook not found: {path}")
    return path


def database_url() -> str:
    value = os.environ.get("DATABASE_URL")
    if not value:
        raise SystemExit("Set DATABASE_URL in .env (Supabase: Project Settings -> Database -> connection string).")
    return value
