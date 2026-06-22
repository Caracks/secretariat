import os
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
DB_PATH = os.getenv("DB_PATH")
APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
AUTHORIZED_GROUP_ID = os.getenv("AUTHORIZED_GROUP_ID")
PRIVATE_CONTACT_AUTO_REPLY = os.getenv("PRIVATE_CONTACT_AUTO_REPLY")
