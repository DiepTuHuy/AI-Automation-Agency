import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

long_text = "Văn bản mẫu dài..." * 500  # Giả lập văn bản dài

def summarize_chunks(text: str, chunk_size: int = 3000) -> str:
    # 1. Phân đoạn văn bản thô theo số ký tự
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    model = genai.GenerativeModel("gemini-2.5-flash")
    chunk_summaries = []
    
    # 2. Tóm tắt từng đoạn
    for idx, chunk in enumerate(chunks):
        print(f"Đang tóm tắt đoạn {idx+1}/{len(chunks)}...")
        res = model.generate_content(f"Tóm tắt đoạn văn sau ngắn gọn trong 1 câu: \n\n{chunk}")
        chunk_summaries.append(res.text.strip())
        
    # 3. Tổng hợp các bản tóm tắt
    combined_prompt = "Hãy tổng hợp các ý chính sau thành một bản tóm tắt hoàn chỉnh:\n\n" + "\n".join(chunk_summaries)
    final_res = model.generate_content(combined_prompt)
    return final_res.text

if __name__ == "__main__":
    summary = summarize_chunks(long_text)
    print("\nBản tóm tắt cuối cùng:")
    print(summary)