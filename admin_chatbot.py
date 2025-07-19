import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from openai import AuthenticationError as OpenAIAuthError
from typing import Dict

# Load environment variables
load_dotenv()

# === Configuration ===
openai_api_key = os.getenv("OPENAI_API_KEY")
chatgpt_model = "gpt-4-turbo"
chatgpt_url = os.getenv("OPENAI_URL")
max_tokens = 500

# === Generate Content Function ===
def generate_admin_content(input_text: str, tile: str = None, key_words: str = None, details: str = None) -> Dict[str, str]:
    try:
        # Build prompt dynamically
        prompt = f"""
You are an expert AI assistant specialized in writing marketing content.
Your job is to generate high-converting and engaging content for the business owner.
You can write marketing emails, social media posts, and promotional copy.
Be clear, persuasive, and match the tone of modern e-commerce and branding.
Format emails with subject lines and body. For social media, make posts catchy and engaging.

Input Text: {input_text}
Title: {tile}
Keywords: {key_words}
Details: {details}
"""

        messages = [
            {"role": "system", "content": "You are a professional marketing copywriter."},
            {"role": "user", "content": prompt}
        ]

        client = OpenAI(api_key=openai_api_key, base_url=chatgpt_url)

        response_obj = client.chat.completions.create(
            model=chatgpt_model,
            max_tokens=max_tokens,
            messages=messages
        )

        response_text = response_obj.choices[0].message.content.strip() if response_obj.choices else "No response generated."
        return {"content_ai": response_text}

    except OpenAIAuthError:
        return {"error": "Invalid OpenAI API key."}
    except Exception as e:
        return {"error": f"ChatGPT error: {str(e)}"}

# === Example Test ===
if __name__ == "__main__":
    input_text = "Write a promotional email for our eco-friendly kitchenware line."
    tile = "Eco-Kitchen Essentials"
    key_words = "eco-friendly, sustainable, kitchenware, green living"
    details = "Our new product line offers biodegradable utensils, reusable storage, and energy-efficient cooking tools."

    result = generate_admin_content(input_text, tile, key_words, details)
    print(json.dumps(result, indent=2, ensure_ascii=False))
