def estimate_cost(word_count: int):
    # Quy đổi ước lượng: 1 từ tiếng Việt ~ 1.5 đến 2.0 tokens
    estimated_tokens = int(word_count * 1.8)
    
    # Bảng giá gemini-2.5-flash: $0.075 / 1 triệu input tokens
    input_price_per_million = 0.075
    estimated_cost_usd = (estimated_tokens / 1_000_000) * input_price_per_million
    
    print(f"Số từ đầu vào: {word_count} từ")
    print(f"Ước lượng số tokens: {estimated_tokens:,} tokens")
    print(f"Chi phí ước tính: ${estimated_cost_usd:.6f} USD")
    print(f"Quy đổi VND: {estimated_cost_usd * 25400:.2f} VND")

if __name__ == "__main__":
    estimate_cost(2000)