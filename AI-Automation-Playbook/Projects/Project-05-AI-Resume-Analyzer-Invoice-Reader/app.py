import os
import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Central config load
    from pathlib import Path
    load_dotenv(Path(__file__).resolve().parents[3] / "AI-Playbook-Platform" / ".env")
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# 1. Định nghĩa Schema cho Hóa Đơn
class InvoiceData(BaseModel):
    invoice_number: str = Field(description="Số hóa đơn (Invoice Number).")
    vendor_name: str = Field(description="Tên đơn vị bán (Vendor).")
    buyer_name: str = Field(description="Tên đơn vị mua (Buyer).")
    tax_code: str = Field(description="Mã số thuế bên mua.")
    total_amount_vnd: float = Field(description="Tổng số tiền thanh toán cuối cùng đã bao gồm VAT.")

# 2. Định nghĩa Schema cho CV
class ResumeData(BaseModel):
    candidate_name: str = Field(description="Họ tên đầy đủ của ứng viên.")
    email: str = Field(description="Địa chỉ email liên hệ.")
    skills: list[str] = Field(description="Danh sách các kỹ năng kỹ thuật chính.")
    years_of_experience: int = Field(description="Số năm kinh nghiệm làm việc thực tế.")

st.set_page_config(page_title="AI Document & Resume Extractor", layout="centered")
st.title("💼 AI B2B Document Parser")

tab1, tab2 = st.tabs(["📄 Trích xuất Hóa Đơn", "👤 Phân Tích CV Ứng Viên"])

with tab1:
    st.header("Trích xuất Hóa đơn tự động")
    invoice_file = st.file_uploader("Tải lên tệp hóa đơn văn bản (.txt)", type=["txt"], key="invoice")
    
    if invoice_file is not None:
        raw_text = invoice_file.read().decode("utf-8")
        st.text_area("Nội dung hóa đơn gốc:", value=raw_text, height=150)
        
        if st.button("Phân tích Hóa Đơn"):
            with st.spinner("AI đang xử lý..."):
                try:
                    model = genai.GenerativeModel(
                        "gemini-2.5-flash",
                        system_instruction="Bạn là kế toán ảo chuyên nghiệp. Hãy trích xuất dữ liệu hóa đơn chính xác."
                    )
                    response = model.generate_content(
                        raw_text,
                        generation_config={
                            "response_mime_type": "application/json",
                            "response_schema": InvoiceData,
                            "temperature": 0.0
                        }
                    )
                    data = InvoiceData.model_validate_json(response.text)
                    
                    st.success("Trích xuất thành công!")
                    st.write(f"**Số hóa đơn:** {data.invoice_number}")
                    st.write(f"**Bên bán:** {data.vendor_name}")
                    st.write(f"**Bên mua:** {data.buyer_name}")
                    st.write(f"**Mã số thuế bên mua:** {data.tax_code}")
                    st.write(f"**Tổng tiền thanh toán:** {data.total_amount_vnd:,} VND")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {e}")

with tab2:
    st.header("Phân tích CV Ứng Viên")
    resume_file = st.file_uploader("Tải lên tệp CV văn bản (.txt)", type=["txt"], key="resume")
    
    if resume_file is not None:
        raw_resume = resume_file.read().decode("utf-8")
        st.text_area("Nội dung CV gốc:", value=raw_resume, height=150)
        
        if st.button("Phân tích CV"):
            with st.spinner("AI đang phân tích..."):
                try:
                    model = genai.GenerativeModel(
                        "gemini-2.5-flash",
                        system_instruction="Bạn là chuyên viên nhân sự AI chuyên sàng lọc CV ứng viên."
                    )
                    response = model.generate_content(
                        raw_resume,
                        generation_config={
                            "response_mime_type": "application/json",
                            "response_schema": ResumeData,
                            "temperature": 0.0
                        }
                    )
                    data = ResumeData.model_validate_json(response.text)
                    
                    st.success("Phân tích CV thành công!")
                    st.write(f"**Họ và tên:** {data.candidate_name}")
                    st.write(f"**Email:** {data.email}")
                    st.write(f"**Kỹ năng:** {', '.join(data.skills)}")
                    st.write(f"**Số năm kinh nghiệm:** {data.years_of_experience} năm")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {e}")
