import json
from config import UPLOAD_HISTORY_FILE

def save_upload_history(entry):
    """Save an upload event to the history JSON file."""
    history = []
    if UPLOAD_HISTORY_FILE.exists():
        with open(UPLOAD_HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass
    
    history.append(entry)
    
    with open(UPLOAD_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_upload_history():
    """Retrieve the upload history."""
    if UPLOAD_HISTORY_FILE.exists():
        with open(UPLOAD_HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
