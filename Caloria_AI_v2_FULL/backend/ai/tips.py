import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def generate_tip(stats: dict) -> str:
    """
    stats: {
      total_calories, total_protein, total_fat, total_carbs,
      goal_calories, goal_protein, goal_fat, goal_carbs
    }
    """

    prompt = f"""
Ты — умный фитнес-диетолог Caloria AI.
Дана статистика за день:

{stats}

Сделай короткий совет (1–2 предложения), дружелюбный, но честный.
Не пиши вступлений. Сразу совет по сути.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return resp.choices[0].message.content.strip()
