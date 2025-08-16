# import json
# import numpy as np
# import openai
# from sklearn.metrics.pairwise import cosine_similarity
# from pathlib import Path
# from utils.creds import OPEN_API_TOKEN

# openai.api_key = OPEN_API_TOKEN

# # Пути к JSON с программами
# PROGRAM_JSON_FILES = [
#     Path("data/ai_plan.json"),
#     Path("data/ai_product_control_plan.json")
# ]

# def get_embedding(text: str) -> list[float]:
#     resp = openai.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return resp.data[0].embedding

# def load_program(file_path: Path):
#     if not file_path.exists():
#         return [], []
#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     corpus = []
#     metadata = []
#     for course in data["courses"]:
#         text = f"{course['name']} ({course['type']}, семестр {course['semester']})"
#         corpus.append(text)
#         metadata.append(course)
#     embeddings = [get_embedding(chunk) for chunk in corpus]
#     return corpus, metadata, embeddings

# def select_program(question: str):
#     # Загружаем все программы и embeddings
#     program_scores = []
#     program_data = []
#     for file_path in PROGRAM_JSON_FILES:
#         corpus, metadata, embeddings = load_program(file_path)
#         program_data.append((file_path.stem, corpus, metadata, embeddings))
#         if corpus:
#             q_emb = get_embedding(question)
#             similarities = cosine_similarity([q_emb], embeddings).mean()
#             program_scores.append(similarities)
#         else:
#             program_scores.append(0)
#     # Выбираем программу с максимальным средним сходством
#     best_idx = np.argmax(program_scores)
#     return program_data[best_idx]

# def retrieve_relevant(question: str, corpus, embeddings, top_k=3):
#     if not corpus:
#         return []
#     q_emb = get_embedding(question)
#     similarities = cosine_similarity([q_emb], embeddings)[0]
#     top_indices = similarities.argsort()[-top_k:][::-1]
#     return [corpus[i] for i in top_indices]

# def recommend_courses(background: str, corpus, metadata, embeddings, top_k=3):
#     if not corpus:
#         return ["Нет доступных курсов."]
#     background_emb = get_embedding(background)
#     elective_indices = [i for i, course in enumerate(metadata) if course["type"] == "выборная"]
#     if not elective_indices:
#         return ["Нет выборных курсов."]
#     elective_embeddings = [embeddings[i] for i in elective_indices]
#     similarities = cosine_similarity([background_emb], elective_embeddings)[0]
#     top_indices = np.array(elective_indices)[similarities.argsort()[-top_k:][::-1]]
#     return [metadata[i]["name"] for i in top_indices]

# def get_answer(question: str, background: str = None) -> str:
#     program_name, corpus, metadata, embeddings = select_program(question)

#     if not corpus:
#         return "Программы еще не загружены или пусты."

#     relevant_chunks = retrieve_relevant(question, corpus, embeddings)
#     context = "\n\n".join(relevant_chunks) if relevant_chunks else "Извините, информации по этому вопросу нет."

#     prompt = f"""
# Ты эксперт по магистратурам ИТМО. Используй только информацию по программе {program_name} для ответа на вопрос студента:

# {context}

# Вопрос: {question}
# """

#     if background:
#         recommended = recommend_courses(background, corpus, metadata, embeddings)
#         prompt += f"\n\nБэкграунд студента: {background}\nРекомендуемые выборные курсы: {', '.join(recommended)}\n"

#     prompt += "\nОтвет:"

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2
#         )
#         answer = response.choices[0].message.content.strip()
#     except Exception as e:
#         answer = f"Произошла ошибка при генерации ответа: {e}"

#     return answer

############################################################################################################################################

# import json
# from pathlib import Path
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# # Загружаем модель для эмбеддингов
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def get_embedding(text):
#     """Возвращает эмбеддинг текста с помощью sentence-transformers"""
#     return model.encode(text).tolist()

# def load_program(file_path):
#     """
#     Загружает курсы из JSON и создаёт corpus, metadata и embeddings
#     JSON должен иметь структуру:
#     {
#         "courses": [
#             {"semester": "1", "block": null, "name": "Курс 1", "type": "", "credits": "3", "hours": "108"},
#             ...
#         ]
#     }
#     """
#     file_path = Path(file_path)
#     if not file_path.exists():
#         raise FileNotFoundError(f"Файл {file_path} не найден. Скачайте или сгенерируйте его.")

#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     corpus = []
#     metadata = []

#     for course in data.get('courses', []):
#         text = f"{course['name']} ({course.get('type','')}, семестр {course.get('semester','')})"
#         corpus.append(text)
#         metadata.append(course)

#     embeddings = [get_embedding(chunk) for chunk in corpus]

#     return corpus, metadata, embeddings

# def select_program(question, file_name='ai_plan.json'):
#     """
#     Загружает программу из папки data и возвращает corpus, metadata и embeddings
#     """
#     file_path = Path('data') / file_name
#     corpus, metadata, embeddings = load_program(file_path)
#     return corpus, metadata, embeddings

# def get_answer(question, file_name='ai_plan.json'):
#     """
#     Находит ближайший курс к вопросу пользователя
#     """
#     corpus, metadata, embeddings = select_program(question, file_name)

#     q_emb = get_embedding(question)
#     sims = cosine_similarity([q_emb], embeddings)[0]
#     best_idx = int(np.argmax(sims))
    
#     return f"Лучший курс для вас: {metadata[best_idx]['name']}"

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

