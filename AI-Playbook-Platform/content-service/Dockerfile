FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY content-service/ /app/content-service/
WORKDIR /app/content-service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
