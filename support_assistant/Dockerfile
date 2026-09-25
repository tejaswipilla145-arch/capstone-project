FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.6.0+cpu

RUN pip install --no-cache-dir sentence-transformers chromadb groq

COPY . .

CMD ["python", "main.py"]