from google import genai

from config import config_obj

# SYSTEM_PROMPT = """
#     Ты — J.A.R.V.I.S, высокотехнологичный AI ассистент Тони Старка.
#
#     Правила:
#     - Обращайся к пользователю: "Сэр"
#     - Стиль: спокойный, ироничный, уверенный
#     - Отвечай кратко, но информативно
#     - Если запрос технический — используй списки
#     - Если данных недостаточно — прямо скажи об этом
#     - Не упоминай, что ты языковая модель
# """
SYSTEM_PROMPT = "Ты агрессивный AI ассистент."


class AIClient:
    """Клиент для взаимодействия с Gemini API."""

    def __init__(self):
        """Инициализирует клиента Gemini и выбирает модель."""
        self.client = genai.Client(api_key=config_obj.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.system_prompt = SYSTEM_PROMPT  # промпт модели, как она себя ведет
        self.history = []  # история предыдущих диалогов пользователь - ии

    def build_prompt(self, user_prompt: str) -> str:
        """
        Полный промпт с историей прошлых диалогов, поведением и настройкой модели и вопросом пользователя.
        Args:
            user_prompt: str.

        Returns:
            str
        """
        memory = "\n".join(self.history[-10:])
        return f"""
        Промпт модели и ее поведения:
        {self.system_prompt}
        
        История диалога:
        {memory}
        
        Вопрос пользователя:
        {user_prompt}
        """

    def ask(self, prompt: str) -> str:
        """Отправляет запрос Gemini и возвращает ответ.

        Returns:
        str: Ответ от Gemini текстом.
        """
        full_prompt = self.build_prompt(prompt)
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )
        print(response)
        answer_ai = response.text.strip()
        self.history.append(f"Пользователь: {prompt}")
        self.history.append(f"JARVIS: {answer_ai}")
        return answer_ai

client = AIClient()
if __name__ == '__main__':

    print(f"Ответ ии: {client.ask('ты кто?')}")
    print(f"История: {client.history}")

# class AIClient:
#     def __init__(self):
#         self.client = genai.Client(api_key=config_obj.gemini_api_key)
#         self.model = "gemini-2.5-flash"
#         self.system_prompt = SYSTEM_PROMPT
#         self.history: List[str] = []
#
#     def _build_prompt(self, user_prompt: str) -> str:
#         dialog = "\n".join(self.history[-6:])  # ограничение памяти
#         return f"""
#                 {self.system_prompt}
#
#                 История диалога:
#                 {dialog}
#
#                 Запрос пользователя:
#                 {user_prompt}
#                 """
#
#     def ask(self, prompt: str) -> str:
#         try:
#             full_prompt = self._build_prompt(prompt)
#
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=full_prompt
#             )
#
#             answer = response.text.strip()
#
#             # сохраняем память
#             self.history.append(f"Пользователь: {prompt}")
#             self.history.append(f"JARVIS: {answer}")
#
#             return answer
#         except ClientError as e:
#             if e.status == HTTPStatus.TOO_MANY_REQUESTS:
#                 return (
#                     "⚠️ Сэр, лимит запросов временно исчерпан.\n"
#                     "Рекомендую подождать или переключиться на резервный интеллект."
#                 )
#
#     def ask_stream(self, prompt: str):
#         full_prompt = self._build_prompt(prompt)
#
#         stream = self.client.models.generate_content_stream(
#             model=self.model,
#             contents=full_prompt
#         )
#
#         answer = ""
#         for chunk in stream:
#             if chunk.text:
#                 answer += chunk.text
#                 yield chunk.text
#
#         self.history.append(f"Пользователь: {prompt}")
#         self.history.append(f"JARVIS: {answer}")
#
#     def clear_memory(self):
#         self.history.clear()
