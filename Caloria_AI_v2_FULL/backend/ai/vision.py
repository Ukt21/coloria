# placeholder ai vision
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


async def analyze_food_photo(path: str):
    """
    GPT-4o Vision определяет еду по фотографии.
    """

    with open(path, "rb") as img:
        img_bytes = img.read()

    prompt = """
Определи, что изображено на фото: блюдо, продукт или напиток.
Оцени примерные нутриенты.

Ответ строго в JSON:
{
 "calories": число,
 "protein": число,
 "fat": число,
 "carbs": число,
 "food_type": "meal"
}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": img_bytes}
                ]
            }
        ],
        max_tokens=300
    )

    data = response.choices[0].message.content
    return json.loads(data)
