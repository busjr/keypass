import os
import json
from setting import APP_NAME, DEFAULT_SETTINGS

def get_config_dir():
    """Путь к папке с настройками в Документах"""
    documents = os.path.join(os.path.expanduser("~"), "Documents", APP_NAME)
    os.makedirs(documents, exist_ok=True)
    return documents

def get_config_path():
    """Путь к JSON файлу"""
    return os.path.join(get_config_dir(), "settings.json")

def load_settings():
    """Загрузка JSON или создание с дефолтом"""
    path = get_config_path()
    if not os.path.exists(path):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(data):
    """Сохранение JSON"""
    with open(get_config_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
