from typing import List
import openai
from src.core.ports.ai_provider import AIProvider, AIOptions

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def complete(self, prompt: str, options: AIOptions) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=options.temperature,
            max_tokens=options.max_tokens,
            stop=options.stop_sequences
        )
        return response.choices[0].message.content

    async def embed(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding 