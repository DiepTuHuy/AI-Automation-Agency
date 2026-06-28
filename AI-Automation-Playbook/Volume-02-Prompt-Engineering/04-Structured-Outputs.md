# Chương 04: Trích xuất Dữ liệu cấu trúc (Structured Outputs) bằng Pydantic

## 1. Deep Dive (Phân tích chuyên sâu)

Trong xây dựng ứng dụng phần mềm thực tế, code Python của bạn không thể tự đọc hiểu một đoạn văn bản tự do do LLM sinh ra để làm logic điều kiện. Bạn cần cấu trúc dữ liệu chuẩn hóa như **JSON** hoặc **Object**.

### Tại sao Regex và JSON Mode cơ bản chưa đủ tốt?
- **JSON Mode cơ bản**: Bắt LLM trả về JSON bằng cách chèn chỉ thị vào prompt. Tuy nhiên, LLM vẫn có thể trả về JSON thiếu các trường bắt buộc, hoặc sai kiểu dữ liệu (ví dụ: trường `age` đáng lẽ là `int` nhưng LLM lại trả về `string` "ba mươi").
- **Structured Outputs (Schema Enforcement)**: OpenAI và các nhà cung cấp lớn hỗ trợ việc định nghĩa một cấu trúc JSON Schema chuẩn hóa. API sẽ ép buộc (enforce) mô hình sinh token tuân thủ nghiêm ngặt theo schema này. Nếu mô hình sinh sai cấu trúc, API sẽ tự động sửa đổi hoặc báo lỗi ngay lập tức.

---

## 2. Demo: Trích xuất thông tin Hợp đồng bằng Pydantic

### Mục tiêu
Trích xuất tên đối tác, ngày ký kết và tổng giá trị hợp đồng từ một đoạn văn bản thô không cấu trúc bằng cách sử dụng thư viện Pydantic kết hợp với API OpenAI.

### Mã nguồn (`structured_parser.py`)
Yêu cầu cài đặt: `pip install pydantic openai`

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Định nghĩa cấu trúc dữ liệu mong muốn bằng Pydantic
class ContractSchema(BaseModel):
    partner_name: str = Field(description="Tên đầy đủ của đối tác hoặc công ty ký kết hợp đồng.")
    signing_date: str = Field(description="Ngày ký kết hợp đồng dưới định dạng YYYY-MM-DD.")
    total_value_vnd: int = Field(description="Tổng giá trị của hợp đồng quy đổi ra đơn vị VND (số nguyên).")
    payment_milestones: List[str] = Field(description="Danh sách các đợt thanh toán được đề cập trong hợp đồng.")
    notes: Optional[str] = Field(None, description="Các lưu ý đặc biệt khác nếu có.")

raw_contract_text = """
Hôm nay, ngày 15 tháng 10 năm 2026, tại văn phòng Công ty TNHH Giải pháp AI Antigravity, chúng tôi tiến hành ký hợp đồng dịch vụ tư vấn triển khai AI Automation với Công ty Cổ phần Thương mại Hoàng Hà.
Tổng giá trị hợp đồng được thống nhất là 350.000.000 VNĐ.
Phương thức thanh toán được chia làm 2 đợt:
- Đợt 1: Thanh toán 50% ngay sau khi ký hợp đồng.
- Đợt 2: Thanh toán 50% còn lại sau khi nghiệm thu bàn giao hệ thống.
"""

def parse_contract(text: str) -> ContractSchema:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là chuyên gia phân tích tài liệu pháp lý. Hãy trích xuất thông tin hợp đồng chính xác."
    )
    response = model.generate_content(
        text,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": ContractSchema # Ép buộc mô hình trả về đúng cấu trúc Pydantic
        }
    )
    return ContractSchema.model_validate_json(response.text)

if __name__ == "__main__":
    print("Đang xử lý tài liệu hợp đồng...")
    contract_info = parse_contract(raw_contract_text)
    
    print("\nKết quả trích xuất cấu trúc dữ liệu:")
    print(f"Đối tác: {contract_info.partner_name}")
    print(f"Ngày ký: {contract_info.signing_date}")
    print(f"Tổng tiền: {contract_info.total_value_vnd:,} VND")
    print(f"Mốc thanh toán: {contract_info.payment_milestones}")
```

---

## 3. Mini Project
Hãy viết một chương trình Python nhận đầu vào là một chuỗi HTML thô chứa danh sách sản phẩm trên trang thương mại điện tử (bao gồm tên sản phẩm, giá tiền, đánh giá sao, và tình trạng còn hàng), sử dụng Pydantic để trích xuất danh sách này thành một mảng đối tượng JSON sạch sẽ, chuẩn kiểu dữ liệu để lưu vào cơ sở dữ liệu.
