import pickle
import config
import os

def save_memory(data):
    os.makedirs(os.path.dirname(config.SETTINGS['memory_file']), exist_ok=True)
    with open(config.SETTINGS['memory_file'], 'wb') as f:
        pickle.dump(data, f)

def load_memory():
    try:
        with open(config.SETTINGS['memory_file'], 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        # If the file doesn't exist, is empty, or is corrupted, start with empty memory
        return {}
