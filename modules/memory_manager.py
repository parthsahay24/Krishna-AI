import json
import os

# Path to our "brain's notebook"
PROFILE_PATH = "data/user_profile.json"

def get_user_data():
    # 1. Create the folder if it's missing
    os.makedirs("data", exist_ok=True)
    """Reads the JSON file to see what Krishna knows."""
    # 2. If file doesn't exist, return empty data
    if not os.path.exists(PROFILE_PATH):
        return {}
    
    # 3. Read the file safely
    try:
        with open(PROFILE_PATH, "r") as f:
            content = f.read().strip()
            if not content: # If file is empty
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, Exception):
        # If the file is corrupted/broken, return empty data
        return {}


def save_user_name(name):
    os.makedirs("data", exist_ok=True)
    data = get_user_data()
    data["name"] = name
    data["first_run"] = False
    
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

