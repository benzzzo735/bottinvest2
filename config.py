# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 🔥 ВАЖНО: загружаем .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TINKOFF_TOKEN = os.getenv("TINKOFF_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not found in .env")

if not TINKOFF_TOKEN:
    raise RuntimeError("TINKOFF_TOKEN not found in .env")
