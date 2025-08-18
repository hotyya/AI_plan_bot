import os
import json
import requests
from utils.creds import OPEN_API_TOKEN, SAVE_PATH_PARSE_AI_JS, SAVE_PATH_PARSE_PRODUCT_JS

OPENAI_API_KEY = OPEN_API_TOKEN  # ключ из переменной окружения
MODEL_NAME = "gpt-4o-mini"

def load_program_json():
    """Читает оба учебных плана из папки data"""
    ai_plan_path = os.path.join("data", "ai_plan.json")
    ai_product_plan_path = os.path.join("data", "ai_product_plan.json")

    with open(SAVE_PATH_PARSE_AI_JS, "r", encoding="utf-8") as f:
        ai_plan = json.load(f)

    with open(SAVE_PATH_PARSE_PRODUCT_JS, "r", encoding="utf-8") as f:
        ai_product_plan = json.load(f)

    return ai_plan, ai_product_plan

def select_program(user_question):
    """Отправляет оба плана и вопрос пользователя в OpenAI, получает рекомендацию"""
    ai_plan, ai_product_plan = load_program_json()

    prompt = f"""
Ты — эксперт по учебным программам. 
У тебя есть две программы в формате JSON. 
Проанализируй их и определи, какая больше всего подходит под запрос пользователя.
Верни JSON с полями:
- "program": название выбранной программы
- "recommended_courses": список наиболее необходимых дисциплин (названия из JSON).

Запрос пользователя:
{user_question}

Программа 1:
{json.dumps(ai_plan, ensure_ascii=False)}

Программа 2:
{json.dumps(ai_product_plan, ensure_ascii=False)}
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Ты умный и аккуратный помощник."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Ошибка OpenAI API: {response.status_code}, {response.text}")

    result_text = response.json()["choices"][0]["message"]["content"]
    return result_text

def get_answer(user_question):
    return select_program(user_question)

