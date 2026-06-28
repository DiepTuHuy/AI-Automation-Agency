import tiktoken

class ChatMemoryManager:
    def __init__(self, max_token_limit: int = 2000, model: str = "gpt-4o"):
        self.max_token_limit = max_token_limit
        self.encoding = tiktoken.encoding_for_model(model)
        self.history = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self._truncate_memory()

    def count_token_in_message(self, message: dict) -> int:
        """
        Đếm số lượng token trong một tin nhắn.
        """
        return len(self.encoding.encode(message["content"]))
    
    def _truncate_memory(self):
        """
        Cắt bớt lịch sử nếu vượt quá giới hạn token.
        """
        total_tokens = sum(self.count_token_in_message(msg) for msg in self.history)
        
        while total_tokens > self.max_token_limit and self.history:
            removed_message = self.history.pop(1)  # Xóa tin nhắn cũ nhất
            total_tokens -= self.count_token_in_message(removed_message)

    def get_messages_for_api(self):
        return self.history
    
if __name__ == "__main__":
    manager = ChatMemoryManager(max_token_limit=100) # Giới hạn cực thấp để test truncation
    manager.add_message("system", "Bạn là một trợ lý ảo.")
    manager.add_message("user", "Xin chào, tôi là Huy, tôi làm về AI Automation.")
    manager.add_message("assistant", "Chào Huy! Rất vui được hỗ trợ bạn.")
    manager.add_message("user", "Hãy kể cho tôi nghe một câu chuyện dài về công nghệ tương lai và cách nó thay đổi thế giới của chúng ta.")
    
    print("\nLịch sử gửi API cuối cùng:")
    for msg in manager.get_messages_for_api():
        print(f"{msg['role'].upper()}: {msg['content'][:50]}...")