import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class MultiAgentSystem:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
    def agent_translator(self, text: str) -> str:
        prompt = f"Dịch đoạn văn bản sau sang tiếng Việt sát nghĩa nhất:\n\n{text}"
        res = self.model.generate_content(prompt)
        return res.text.strip()
        
    def agent_editor(self, translated_text: str) -> str:
        prompt = f"Hãy sửa lỗi chính tả, ngữ pháp và tối ưu văn phong cho đoạn dịch sau tự nhiên hơn:\n\n{translated_text}"
        res = self.model.generate_content(prompt)
        return res.text.strip()
        
    def run_pipeline(self, english_text: str) -> str:
        print("-> Agent 1 (Translator) đang dịch bài...")
        translated = self.agent_translator(english_text)
        print("-> Agent 2 (Editor) đang tinh chỉnh bản dịch...")
        final_output = self.agent_editor(translated)
        return final_output

if __name__ == "__main__":
    system = MultiAgentSystem()
    input_text = "AI agents are transforming how we build software today."
    output = system.run_pipeline(input_text)
    print("\nKết quả cuối cùng:")
    print(output)