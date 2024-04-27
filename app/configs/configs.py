import os

from dotenv import load_dotenv

load_dotenv("../../.env")

APP_NAME = os.getenv("APP_NAME")
