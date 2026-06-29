def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

if __name__ == "__main__":
    sample_text = "Học viện AI Automation đào tạo kỹ sư chất lượng cao. Khóa học thực chiến cung cấp đầy đủ lý thuyết và dự án thực tế doanh nghiệp."
    results = chunk_text(sample_text, chunk_size=50, overlap=10)
    for i, c in enumerate(results):
        print(f"Đoạn {i+1}: '{c}' (Độ dài: {len(c)} ký tự)")