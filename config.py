import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ENGINE = os.getenv("ENGINE")
ECHO = True
