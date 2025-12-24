from google import genai
from google.genai.errors import ClientError

from config import config_obj

client = genai.Client(api_key=config_obj.gemini_api_key)


def get_answer_from_gemini(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except ClientError as e:
        if e.status == 429:
            return (
                "⚠️ Сэр, лимит запросов временно исчерпан.\n"
                "Рекомендую подождать или переключиться на резервный интеллект."
            )
