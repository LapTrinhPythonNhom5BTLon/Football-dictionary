import os
from dotenv import load_dotenv

load_dotenv() # chuyen du lieu tho trong .env -> py
SECRET_KEY = os.environ.get("KEY")
DB_URL = os.environ.get("DATABASE_URL")
TRACK_MODIFICATIONS = False