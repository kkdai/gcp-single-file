# 使用 Python 3.9 slim 作為基礎映像
FROM python:3.9-slim

# 安裝 Node.js, npm, git 和 Chromium
RUN apt-get update && apt-get install -y nodejs npm git chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安裝 single-file-cli
RUN npm install -g single-file-cli

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程序代碼
COPY . .

# 設置環境變量
ENV PORT 8080

# 啟動應用程序
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app