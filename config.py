import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ENGINE = os.getenv("ENGINE")
ECHO = True
