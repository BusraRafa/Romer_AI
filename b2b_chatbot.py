import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from openai import AuthenticationError as OpenAIAuthError
from typing import Dict, List

load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")

chatgpt_model = "openai/gpt-4-turbo" 

chatgpt_url=os.environ.get("OPENAI_URL")


system_prompt = {
    "role": "system",
    "content": (
        "You are a friendly, helpful, and professional customer service assistant. "
        "Greet the user warmly, answer questions clearly, and guide them step-by-step. "
        "Always be polite, supportive, and informative. If you don’t know something, kindly suggest contacting human support."
    )
}
max_tokens = 500

def generate_response(input_text: str, chat_history: List[Dict] = None) -> Dict:
#chatgpt
    if chat_history is None:
        chat_history = []

    responses = {}
    try:
            chatgpt_messages = [system_prompt]
            for chat in chat_history:
                if chat.get("user", "").strip():
                    chatgpt_messages.append({"role": "user", "content": chat["user"]})
                if chat.get("chatgpt", "").strip():
                    chatgpt_messages.append({"role": "assistant", "content": chat["chatgpt"]})

            chatgpt_messages.append({"role": "user", "content": input_text})

            client = OpenAI(api_key=openai_api_key, 
                            base_url=chatgpt_url)
            
            response_obj = client.chat.completions.create(
                model=chatgpt_model,
                max_tokens=max_tokens,
                messages=chatgpt_messages
            )
            chatgpt_response = response_obj.choices[0].message.content if response_obj and response_obj.choices else "No response generated."
        
    except OpenAIAuthError:
            chatgpt_response = "Invalid OpenAI API key."
    except Exception as e:
            chatgpt_response = f"ChatGPT error: {str(e)}"
    responses["chatgpt"] = chatgpt_response
    return responses

if __name__ == "__main__":
    input_text = "can someone assist me here"

   
    chat_history = [
        {
            "user": "Hello, I need some help.",
            "chatgpt": "Sure! I'm here to help. What do you need assistance with today?"
        },
    ] 

    
    result = generate_response(input_text, chat_history)
    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_output)
