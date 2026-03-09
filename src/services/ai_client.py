import asyncio
from google import genai
from src.core.config import settings


class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = 'gemini-2.5-flash'

    async def ask(self, prompt: str, context: str = None) -> str:
        try:
            if context:
                full_prompt = f"""
                Ты — AI-ассистент, который отвечает на вопросы по предоставленным документам.

                КОНТЕКСТ ИЗ ДОКУМЕНТОВ:
                {context}

                ВОПРОС ПОЛЬЗОВАТЕЛЯ:
                {prompt}

                Инструкция:
                1. Отвечай ТОЛЬКО на основе предоставленного контекста
                2. Если ответа нет в контексте — скажи "В документах нет информации по этому вопросу"
                3. Отвечай на русском языке
                4. Будь краток и информативен
                """
            else:
                full_prompt = prompt

            loop = asyncio.get_event_loop()

            def generate():
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=2048
                    )
                )

            response = await loop.run_in_executor(None, generate)

            if response and hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                return "AI не сгенерировал ответ"

        except Exception as e:
            error_msg = f"Ошибка AI: {type(e).__name__}: {e}"
            print(error_msg)
            return error_msg

    async def list_models(self) -> list:
        try:
            models = self.client.models.list()
            return [m.name for m in models]
        except Exception as e:
            return [f"Ошибка: {e}"]