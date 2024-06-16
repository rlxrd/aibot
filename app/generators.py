from openai import AsyncOpenAI
from g4f.client import AsyncClient
from g4f.Provider import Blackbox, GeminiPro

from config import AI_TOKEN, GEMINI


class Generate:
    def __init__(self):
        self.blackbox = AsyncClient(provider=Blackbox)
        self.geminipro = AsyncClient(provider=GeminiPro, api_key=GEMINI)
        self.openai = AsyncOpenAI(api_key=AI_TOKEN)

    async def openai_text(self, model, text):
        response = await self.openai.chat.completions.create(
            model=model,
            messages=[{"role": "user","content": text}])
        return response

    async def blackbox_text(self, model, text):
        response = await self.blackbox.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}])
        return response

    async def geminipro_text(self, model, text):
        response = await self.geminipro.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}])
        return response

    async def get_model_text(self, company, model, text):
        if company == 'openai':
            response = await self.openai_text(model, text)
            return response.choices[0].message.content
        elif company == 'geminipro':
            response = await self.geminipro_text(model, text)
            return response.choices[0].message.content
        elif company == 'blackbox':
            response = await self.blackbox_text(model, text)
            return response.choices[0].message.content
