import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_invoice_items(text, retry=False):
    base_prompt = f"""
You are an AI that extracts structured item details from invoices.

Return a JSON array. Each item should contain:
- "Item Name": preserve exactly as in text
- "Quantity": integer
- "Price": float

Strictly extract only from this text:
{text}

Return valid JSON only. No comments or explanations.
"""

    fallback_prompt = f"""
Extract invoice items from this text. Output valid JSON only:
Each object must include "Item Name", "Quantity", "Price".
Use exact item names. Return only the data.

Text:
{text}
"""

    prompt = fallback_prompt if retry else base_prompt

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Extract invoice data as JSON"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=3000
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except Exception as e:
        if not retry:
            return extract_invoice_items(text, retry=True)
        return {"error": str(e), "raw_output": content if 'content' in locals() else ''}