from typing import List

from google import genai
from google.genai.errors import ClientError

from config import config_obj

client = genai.Client(api_key=config_obj.gemini_api_key)

SYSTEM_PROMPT = """
    Ты — J.A.R.V.I.S, высокотехнологичный AI ассистент Тони Старка.

    Правила:
    - Обращайся к пользователю: "Сэр"
    - Стиль: спокойный, ироничный, уверенный
    - Отвечай кратко, но информативно
    - Если запрос технический — используй списки
    - Если данных недостаточно — прямо скажи об этом
    - Не упоминай, что ты языковая модель
"""


class AIClient:
    def __init__(self):
        self.client = genai.Client(api_key=config_obj.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.system_prompt = SYSTEM_PROMPT
        self.history: List[str] = []

    def _build_prompt(self, user_prompt: str) -> str:
        dialog = "\n".join(self.history[-6:])  # ограничение памяти
        return f"""
                {self.system_prompt}

                История диалога:
                {dialog}

                Запрос пользователя:
                {user_prompt}
                """

    def ask(self, prompt: str) -> str:
        try:
            full_prompt = self._build_prompt(prompt)

            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )

            answer = response.text.strip()

            # сохраняем память
            self.history.append(f"Пользователь: {prompt}")
            self.history.append(f"JARVIS: {answer}")

            return answer
        except ClientError as e:
            if e.status == 429:
                return (
                    "⚠️ Сэр, лимит запросов временно исчерпан.\n"
                    "Рекомендую подождать или переключиться на резервный интеллект."
                )

    def ask_stream(self, prompt: str):
        full_prompt = self._build_prompt(prompt)

        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=full_prompt
        )

        answer = ""
        for chunk in stream:
            if chunk.text:
                answer += chunk.text
                yield chunk.text

        self.history.append(f"Пользователь: {prompt}")
        self.history.append(f"JARVIS: {answer}")

    def clear_memory(self):
        self.history.clear()
