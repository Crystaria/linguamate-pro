FROM python:3.11-slim

WORKDIR /app

# 确保 pip 可用
RUN python -m ensurepip --upgrade || true

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main_local.py"]
