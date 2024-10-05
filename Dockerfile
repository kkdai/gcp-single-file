# Dockerfile
FROM python:3.9-slim

# 安裝 Node.js 和 npm
RUN apt-get update && apt-get install -y nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安裝 single-file-cli
RUN npm install -g single-file-cli

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 設置環境變量
ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
