FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY quiz-service/ /app/quiz-service/
WORKDIR /app/quiz-service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
