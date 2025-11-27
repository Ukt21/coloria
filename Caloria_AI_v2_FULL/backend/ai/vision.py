import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def analyze_food_photo(path: str) -> dict:
    prompt = """
Ты — диетолог Caloria AI.
На фото — приём пищи. Определи примерные калории и БЖУ.

Ответ строго в JSON:

{
  "calories": 500,
  "protein": 20,
  "fat": 18,
  "carbs": 60,
  "food_type": "lunch"
}
"""

    with open(path, "rb") as f:
        img_bytes = f.read()

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": img_bytes},
                ],
            }
        ],
    )

    raw = resp.choices[0].message.content.strip()
    return json.loads(raw)

