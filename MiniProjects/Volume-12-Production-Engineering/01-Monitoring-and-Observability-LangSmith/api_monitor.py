import os
import time
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

logging.basicConfig(filename="api_metrics.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def monitored_call(prompt: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    start_time = time.time()
    
    try:
        response = model.generate_content(prompt)
        latency = time.time() - start_time
        
        # Ghi log metrics
        logging.info(
            f"Prompt: '{prompt[:20]}...' | Status: SUCCESS | "
            f"Latency: {latency:.2f}s | Response length: {len(response.text)} chars"
        )
        return response.text
    except Exception as e:
        latency = time.time() - start_time
        logging.error(f"Prompt: '{prompt[:20]}...' | Status: FAILED | Latency: {latency:.2f}s | Error: {e}")
        return None

if __name__ == "__main__":
    monitored_call("Giải thích về tính năng giám sát hệ thống AI.")