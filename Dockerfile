# Temel imaj
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# wait-for-db scriptini ekle
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Gunicorn'u script üzerinden başlat
CMD ["/wait-for-db.sh", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
