import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=api_key)

def ask_ai(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 1.5
            }
        )
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi khi gọi API: {str(e)}"

if __name__ == "__main__":
    prompt = "Giải thích ngắn gọn về cơ chế hoạt động của LLM cho người mới học lập trình."
    result = ask_ai(prompt)
    print(result)