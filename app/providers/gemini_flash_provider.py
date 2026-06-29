from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings
from app.config.llm_config import ROOT_CAUSE_MODEL
from app.providers.llm_provider import LLMProvider


class GeminiFlashProvider(LLMProvider):

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=ROOT_CAUSE_MODEL,
            google_api_key=settings.GEMINI_API_KEY, 
            temperature=0.2,
        )

    async def generate(self, prompt: str) -> str:

        response = await self.llm.ainvoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):
                    text_parts.append(item.get("text", ""))

                else:
                    text_parts.append(str(item))

            return "\n".join(text_parts)

        return str(content)