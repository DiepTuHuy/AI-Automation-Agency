import os
from typing import List
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 1. Định nghĩa schema dữ liệu từng sản phẩm
class Product(BaseModel):
    name: str = Field(description="Tên sản phẩm đầy đủ.")
    price_usd: float = Field(description="Giá sản phẩm quy đổi ra USD (số thực).")
    rating_stars: float = Field(description="Số sao đánh giá (ví dụ: 4.5).")
    in_stock: bool = Field(description="Trình trạng còn hàng (True nếu còn, False nếu hết).")

# 2. Định nghĩa schema cho danh sách sản phẩm
class ProductList(BaseModel):
    products: List[Product]

html_content = """
<div class="product-card">
    <h2 class="title">Bàn phím cơ Keychron K2</h2>
    <span class="price">$79.99</span>
    <span class="rating">Đánh giá: 4.8/5 sao</span>
    <span class="status">Còn hàng</span>
</div>
<div class="product-card">
    <h2 class="title">Chuột không dây Logitech MX Master 3S</h2>
    <span class="price">$99.00</span>
    <span class="rating">Đánh giá: 4.9/5 sao</span>
    <span class="status">Hết hàng</span>
</div>
"""

def extract_products(html: str) -> ProductList:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là trợ lý AI chuyên trích xuất dữ liệu có cấu trúc từ mã nguồn HTML."
    )
    
    response = model.generate_content(
        f"Hãy trích xuất thông tin tất cả các sản phẩm có trong đoạn HTML sau:\n\n{html}",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": ProductList
        }
    )
    return ProductList.model_validate_json(response.text)

if __name__ == "__main__":
    print("Đang trích xuất dữ liệu...")
    extracted_data = extract_products(html_content)
    
    print("\nKết quả trích xuất JSON:")
    print(extracted_data.model_dump_json(indent=2))