import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def analyze_food_text(text: str) -> dict:
    prompt = f"""
Ты — диетолог Caloria AI.
Пользователь описал приём пищи:

\"\"\"{text}\"\"\"

Определи:
- калории (целое число)
- белки (граммы)
- жиры (граммы)
- углеводы (граммы)
- тип приёма пищи: breakfast / lunch / dinner / snack

Ответ верни строго в JSON, без комментариев:

{{
  "calories": 450,
  "protein": 25,
  "fat": 15,
  "carbs": 50,
  "food_type": "lunch"
}}
"""

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = resp.choices[0].message.content.strip()
    return json.loads(raw)
