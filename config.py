import os

from redis import Redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEEK_DAYS_REGEXP = "Пн|Вт|Ср|Чт|Пт|Сб|Вс"

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)