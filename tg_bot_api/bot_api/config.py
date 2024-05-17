import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ENGINE = "sqlite+aiosqlite:///db.sqlite3"
ECHO = True
