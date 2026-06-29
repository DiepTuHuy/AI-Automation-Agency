import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ask_gemini():
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("AI Automation là gì? Giải thích ngắn gọn trong 2 câu.")
    print("AI trả lời:")
    print(response.text)

if __name__ == "__main__":
    ask_gemini()