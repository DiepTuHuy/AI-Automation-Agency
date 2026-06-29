import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

conn = sqlite3.connect("api_cache.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS cache (query TEXT PRIMARY KEY, response TEXT)")
conn.commit()

def ask_with_cache(query: str) -> str:
    # 1. Kiểm tra trong cache trước
    cursor.execute("SELECT response FROM cache WHERE query = ?", (query,))
    cached = cursor.fetchone()
    if cached:
        print("-> Trả về kết quả từ Cache (Miễn phí API!)")
        return cached[0]
        
    # 2. Gọi API thực tế nếu chưa có
    print("-> Gọi Gemini API thực tế...")
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(query)
    ans = response.text.strip()
    
    # 3. Lưu vào cache
    cursor.execute("INSERT OR REPLACE INTO cache (query, response) VALUES (?, ?)", (query, ans))
    conn.commit()
    return ans

if __name__ == "__main__":
    q = "Slogan ngắn cho quán cafe sạch"
    print("Lần 1:")
    print(ask_with_cache(q))
    print("\nLần 2:")
    print(ask_with_cache(q))
    conn.close()