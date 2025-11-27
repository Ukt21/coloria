# placeholder ai tips
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def generate_tip(stats: dict):
    """
    Создаёт короткий совет по питанию на основе потребления за день.
    """

    prompt = f"""
Ты — нутриционист Caloria AI.
Вот статистика дня:

{stats}

Дай короткую рекомендацию (1–2 предложения).
Будь простым и мотивирующим.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
