import asyncio
from src.services.ai_client import GeminiClient

async def main():
    client = GeminiClient()
    models = await client.list_models()
    print("Доступные модели:")
    for model in models:
        print(f"  - {model}")

if __name__ == "__main__":
    asyncio.run(main())