import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

sentences = [
    "Hệ thống AI Agent tự động hóa quy trình nghiệp vụ doanh nghiệp.",
    "Lập trình Python giúp xây dựng API nhanh chóng với FastAPI.",
    "Mô hình ngôn ngữ lớn hoạt động dựa trên cơ chế Attention.",
    "Phở bò Hà Nội là món ăn truyền thống nổi tiếng thế giới.",
    "Bánh mì kẹp thịt Việt Nam ngon và tiện lợi cho bữa sáng."
]

def save_embeddings_to_json(text_list: list, output_filepath: str):
    data_to_save = []
    
    for text in text_list:
        # Gọi Gemini embedding model
        response = genai.embed_content(
            model="models/text-embedding-004",
            contents=[text],
            task_type="retrieval_document"
        )
        vector = response['embedding'][0]
        data_to_save.append({
            "text": text,
            "embedding": vector
        })
        print(f"Đã nhúng câu: '{text[:20]}...' -> Vector {len(vector)} chiều.")
        
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    print(f"-> Đã lưu file: {output_filepath}")

if __name__ == "__main__":
    output_file = "embeddings.json"
    save_embeddings_to_json(sentences, output_file)