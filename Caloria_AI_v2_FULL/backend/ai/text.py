# placeholder ai text
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def analyze_food_text(text: str):
    """
    GPT-4o анализирует описание еды.
    Выдаёт калории, БЖУ, тип блюда.
    """

    prompt = f"""
Ты — профессиональный нутриционист.
Проанализируй блюдо по тексту:

Описание: {text}

Определи:
- калории
- белки
- жиры
- углеводы
- тип блюда: meal / snack / drink / sweet / fruit / fastfood

Ответ строго в JSON:
{{
 "calories": число,
 "protein": число,
 "fat": число,
 "carbs": число,
 "food_type": "meal"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    data = response.choices[0].message.content
    return json.loads(data)
