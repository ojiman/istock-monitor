import json
import os

# The name of the file used to store the application's state.
STATE_FILE = "state.json"

def read_state():
    """
    Reads the current state from the state.json file.

    If the file does not exist or contains invalid JSON, it gracefully
    returns an empty dictionary.

    Returns:
        dict: The last saved state, or an empty dictionary on failure.
    """
    if not os.path.exists(STATE_FILE):
        return {}
    
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            # Handle cases where the file might be empty
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        # If the file is corrupted, unreadable, or other IO issues occur
        return {}

def write_state(state: dict):
    """
    Writes the given state dictionary to the state.json file.

    The file is written with an indent of 2 spaces for readability and
    ensure_ascii=False to correctly handle non-ASCII characters.

    Args:
        state (dict): The current state dictionary to be saved.
    """
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except IOError as e:
        # This will catch issues like permissions errors
        print(f"Error: Could not write to state file at {STATE_FILE}. Error: {e}")

