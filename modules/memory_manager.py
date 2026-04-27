import json
import os

# Path to our "brain's notebook"
MEMORY_FILE = "data/user_profile.json"

def get_user_data():
    """Reads the JSON file to see what Krishna knows."""
    if not os.path.exists(MEMORY_FILE):
        return {"name": None, "first_run": True}
    
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_user_name(name):
    """Writes the name to the JSON file forever."""
    data = {"name": name, "first_run": False}
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return data
