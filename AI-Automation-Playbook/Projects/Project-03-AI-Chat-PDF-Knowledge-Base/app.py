import os
import streamlit as st
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Khởi tạo thư mục DB
DB_PATH = Path("./chroma_knowledge_db")
chroma_client = chromadb.PersistentClient(path=str(DB_PATH))
collection = chroma_client.get_or_create_collection("pdf_documents")

st.set_page_config(page_title="AI Chat PDF & Knowledge Base", layout="wide")
st.title("📚 AI Chat PDF & Knowledge Base")
st.subheader("Tải lên tài liệu của bạn và đặt câu hỏi cho Trợ lý ảo AI")

# Sidebar cấu hình tải lên file
with st.sidebar:
    st.header("Tải tài liệu lên")
    uploaded_file = st.file_uploader("Chọn file tài liệu (.txt hoặc văn bản thô)", type=["txt"])
    
    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8")
        
        # 1. Thực hiện chia nhỏ văn bản (Chunking)
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        chunks = splitter.split_text(text_content)
        
        st.info(f"Đã phân tích file thành {len(chunks)} đoạn nhỏ.")
        
        # 2. Tạo vector và nạp vào ChromaDB
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Để đơn giản, ta dùng mô hình nhúng mặc định offline của ChromaDB
        # Nếu muốn chính xác hơn, có thể khai báo nhúng bằng OpenAI API
        collection.add(
            documents=chunks,
            ids=ids
        )
        st.success("Đã nạp tri thức vào Vector Database thành công!")

# Phần chat chính
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Nhập câu hỏi mới từ người dùng
if user_query := st.chat_input("Nhập câu hỏi của bạn về tài liệu..."):
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 3. TRUY XUẤT (Retrieval): Tìm kiếm ngữ cảnh tương đồng nhất từ ChromaDB
    try:
        search_results = collection.query(
            query_texts=[user_query],
            n_results=2
        )
        context = "\n\n".join(search_results["documents"][0]) if search_results["documents"] else ""
    except Exception as e:
        context = ""
        st.warning(f"Không có tài liệu nào được nạp hoặc lỗi truy vấn: {e}")

    # 4. SINH CÂU TRẢ LỜI (Generation)
    system_prompt = f"""Bạn là trợ lý AI chuyên nghiệp giải đáp thắc mắc tài liệu.
Hãy trả lời câu hỏi dựa trên phần tài liệu được cấp dưới đây. Nếu tài liệu không chứa câu trả lời, hãy báo là bạn không biết, không được bịa đặt.

Tài liệu tham khảo:
{context}
"""

    # Gộp lịch sử chat để gửi cùng ngữ cảnh
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages[-5:]: # Chỉ lấy 5 lượt chat gần nhất để tránh tràn context
        api_messages.append({"role": msg["role"], "content": msg["content"]})
        
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.2
            )
            answer = response.choices[0].message.content
            st.write(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
