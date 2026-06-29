import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class ChatWithMemory:
    def __init__(self, max_memory: int = 3):
        self.max_memory = max_memory
        self.history = []
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
    def chat(self, user_message: str) -> str:
        # 1. Ghép lịch sử hội thoại giới hạn vào prompt
        prompt = ""
        for turn in self.history[-self.max_memory:]:
            prompt += f"User: {turn['user']}\nAI: {turn['ai']}\n"
        prompt += f"User: {user_message}\nAI:"
        
        res = self.model.generate_content(prompt)
        ai_reply = res.text.strip()
        
        # 2. Lưu vào lịch sử bộ nhớ
        self.history.append({"user": user_message, "ai": ai_reply})
        return ai_reply

if __name__ == "__main__":
    bot = ChatWithMemory(max_memory=2)
    print("Bot:", bot.chat("Chào bạn, tôi tên là Huy."))
    print("Bot:", bot.chat("Tôi làm việc trong ngành AI Automation."))
    print("Bot:", bot.chat("Tên tôi là gì và tôi làm ngành gì?"))