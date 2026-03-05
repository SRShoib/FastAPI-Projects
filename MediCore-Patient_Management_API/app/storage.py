from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Dict, Any, Optional

_DB_LOCK = Lock()

def _default_db_path() -> Path:
    # Default database location inside project
    return Path("database/patient_data.json").resolve()

def load_db(path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    path = (path or _default_db_path())
    if not path.exists():
        return {}
    with _DB_LOCK:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Database file must contain a JSON object mapping patient_id -> patient_data.")
    return data

def save_db(data: Dict[str, Dict[str, Any]], path: Optional[Path] = None) -> None:
    path = (path or _default_db_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    with _DB_LOCK:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
