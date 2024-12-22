import json
from pathlib import Path

CONFIG_PATH = Path('./conf/paths.json')

def ensure_config_exists():
    Path('./video').mkdir(exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        save_config({'paths': ['./video']})

def load_config():
    with CONFIG_PATH.open('r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with CONFIG_PATH.open('w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def modify_config(new_config):
    save_config(new_config)

ensure_config_exists()
config = load_config()
