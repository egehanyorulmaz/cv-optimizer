"""File-based storage utilities for the Streamlit application."""

import json
import os
from pathlib import Path
from typing import Optional, Any

# Create temp directory if it doesn't exist
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def save_json(key: str, data: Any) -> None:
    """Save data as JSON to temp directory.
    
    :param key: Unique identifier for the data
    :type key: str
    :param data: Data to save
    :type data: Any
    """
    try:
        file_path = TEMP_DIR / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save {key}: {str(e)}")

def load_json(key: str) -> Optional[dict]:
    """Load JSON data from temp directory.
    
    :param key: Unique identifier for the data
    :type key: str
    :return: Loaded data or None if file doesn't exist
    :rtype: Optional[dict]
    """
    try:
        file_path = TEMP_DIR / f"{key}.json"
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {key}: {str(e)}")
        return None

def clear_data(key: str) -> None:
    """Delete stored data for a key.
    
    :param key: Unique identifier for the data
    :type key: str
    """
    try:
        file_path = TEMP_DIR / f"{key}.json"
        if file_path.exists():
            os.remove(file_path)
    except Exception as e:
        print(f"Failed to clear {key}: {str(e)}")

def clear_all() -> None:
    """Delete all stored data."""
    try:
        for file in TEMP_DIR.glob("*.json"):
            os.remove(file)
    except Exception as e:
        print(f"Failed to clear all data: {str(e)}") 