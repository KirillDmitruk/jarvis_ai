from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    gemini_api_key = os.getenv('API_KEY')


config_obj = Config()
