# Railway deployment - Updated 2026-03-04
FROM python:3.11-slim

WORKDIR /app

# 确保 pip 可用
RUN python -m ensurepip --upgrade || true

# 进入 backend 目录并安装依赖
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# 复制 backend 代码
COPY backend/ ./

EXPOSE 8000

CMD ["python", "main_local.py"]
