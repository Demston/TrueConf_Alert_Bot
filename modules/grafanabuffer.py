import os
import json
from config import CACHE_FILE


def load_cache():
    """Load the JSON graphana from the cache / Загрузим json графаны из кэша"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                content = f.read().strip()
                if not content:  # If the file is empty / Если файл пустой
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, Exception) as e:
            print(f"--- [!] Битый кэш: {e} ---")
            return {}
    return {}


def save_cache(cache_message):
    """Let's save the JSON graphana to the cache / Сохраним json графаны в кэш"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_message, f)
