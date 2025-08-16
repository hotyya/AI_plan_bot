import json
import os
from pathlib import Path

def load_config():
    if os.path.isfile("config.json"):
        with open("config.json", mode = 'r') as config:
            params = json.load(config)
    else:
        pass

    return params

config = load_config()

LOGS_PATH = config['utils_creds']['logs_path']
AI_PLAN_URL = config['parse_creds']['AI_plan']
AI_PRODUCT_CONTROL_PLAN = config['parse_creds']['AI_product_control_plan']
SAVE_PATH_PARSE_AI = config['parse_creds']['save_path_AI_plan']
SAVE_PATH_PARSE_PRODUCT = config['parse_creds']['save_path_ai_product_control_plan']
SAVE_PATH_PARSE_AI_JS = config['parse_creds']['save_path_AI_plan_js']
SAVE_PATH_PARSE_PRODUCT_JS = config['parse_creds']['save_path_ai_product_control_plan_js']
TELEGRAM_TOKEN = config['tokens']['tg_token']
OPEN_API_TOKEN = config['tokens']['open_api_key']
DEEPSEEK_API_KEY = config['tokens']['deepseek_api_key']