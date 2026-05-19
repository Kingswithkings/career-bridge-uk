import asyncio

from openai import AsyncOpenAI

from ..config import (
    OPENAI_API_KEY,
    OPENAI_MAX_OUTPUT_TOKENS,
    OPENAI_MODEL,
    OPENAI_TIMEOUT_SECONDS,
)

client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


async def ask_ai(system_prompt: str, user_prompt: str) -> str:
    if client is None:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    response = await asyncio.wait_for(
        client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=OPENAI_MAX_OUTPUT_TOKENS,
        ),
        timeout=OPENAI_TIMEOUT_SECONDS,
    )

    return response.choices[0].message.content or ""
