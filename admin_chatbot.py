import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from openai import AuthenticationError as OpenAIAuthError
from typing import Dict, List

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
chatgpt_model = "openai/gpt-4-turbo"
chatgpt_url = os.environ.get("OPENAI_URL")
max_tokens = 500

admin_prompt = {
    "role": "system",
    "content": (
        "You are an expert AI assistant specialized in writing marketing content. "
        "Your job is to generate high-converting and engaging content for the business owner. "
        "You can write marketing emails, social media posts, and promotional copy. "
        "Be clear, persuasive, and match the tone of modern e-commerce and branding. "
        "Format emails with subject lines and body. For social media, make posts catchy and engaging."
    )
}

def generate_admin_content(input_text: str, chat_history: List[Dict] = None) -> Dict:
    if chat_history is None:
        chat_history = []

    responses = {}
    try:
        messages = [admin_prompt]

        for chat in chat_history:
            if chat.get("user", "").strip():
                messages.append({"role": "user", "content": chat["user"]})
            if chat.get("chatgpt", "").strip():
                messages.append({"role": "assistant", "content": chat["chatgpt"]})

        messages.append({"role": "user", "content": input_text})

        client = OpenAI(api_key=openai_api_key, base_url=chatgpt_url)

        response_obj = client.chat.completions.create(
            model=chatgpt_model,
            max_tokens=max_tokens,
            messages=messages
        )
        response_text = response_obj.choices[0].message.content if response_obj and response_obj.choices else "No response generated."

    except OpenAIAuthError:
        response_text = "Invalid OpenAI API key."
    except Exception as e:
        response_text = f"ChatGPT error: {str(e)}"

    responses["content_ai"] = response_text
    return responses

# Example test
if __name__ == "__main__":
    input_text = "Create a Facebook post for our summer sale - 25% off all products"
    #Write a promotional email for our eco-friendly kitchenware line.

    chat_history = [
        {
            "user": "Create a Facebook post for our summer sale.",
            "chatgpt": "Summer Sale is Here! Enjoy 25% off all items this weekend only. Shop now!"
        }
    ]

    result = generate_admin_content(input_text, chat_history)
    print(json.dumps(result, indent=2, ensure_ascii=False))
