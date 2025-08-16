import requests
from pathlib import Path
import logging
import json
import pdfplumber
from utils.creds import AI_PLAN_URL, SAVE_PATH_PARSE_AI, SAVE_PATH_PARSE_PRODUCT, AI_PRODUCT_CONTROL_PLAN, SAVE_PATH_PARSE_AI_JS, SAVE_PATH_PARSE_PRODUCT_JS

logger = logging.getLogger('bot_logger')

def download_pdf(url: str, save_path: Path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Файл сохранен в {save_path}")
    else:
        logger.error(f"Не удалось скачать PDF, статус: {response.status_code}")

def parse_pdf_to_json(pdf_path: Path, json_path: Path):
    plans = []
    
    with pdfplumber.open(pdf_path) as pdf:
        current_semester = None
        current_block = None
        
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table[1:]:  # пропускаем заголовок
                    # Пропускаем полностью пустые строки
                    if all(cell is None or cell.strip() == "" for cell in row):
                        continue
                    
                    # Проверяем, это блок/подзаголовок или дисциплина
                    first_cell = row[0].strip() if row[0] else ""
                    
                    if first_cell.lower().startswith("блок") or first_cell.lower().startswith("пул"):
                        current_block = first_cell
                        continue
                    
                    # Проверяем семестр (цифра в первой колонке)
                    if first_cell.isdigit():
                        current_semester = first_cell
                        course_name = row[1].strip() if len(row) > 1 else ""
                        course_type = ""  # Можно пытаться угадать по блоку
                        credits = row[2].strip() if len(row) > 2 else ""
                        hours = row[3].strip() if len(row) > 3 else ""
                        
                        course = {
                            "semester": current_semester,
                            "block": current_block,
                            "name": course_name,
                            "type": course_type,
                            "credits": credits,
                            "hours": hours
                        }
                        plans.append(course)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"courses": plans}, f, ensure_ascii=False, indent=2)

def update_plans():
    """Скачивает и парсит PDF в JSON."""
    download_pdf(AI_PLAN_URL, SAVE_PATH_PARSE_AI)
    download_pdf(AI_PRODUCT_CONTROL_PLAN, SAVE_PATH_PARSE_PRODUCT)
    parse_pdf_to_json(SAVE_PATH_PARSE_AI, SAVE_PATH_PARSE_AI_JS)
    parse_pdf_to_json(SAVE_PATH_PARSE_PRODUCT, SAVE_PATH_PARSE_PRODUCT_JS)
    logger.info("Учебные планы обновлены.")