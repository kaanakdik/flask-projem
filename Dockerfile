# Temel imaj: CPU uyumlu daha eski python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Gunicorn ile başlat
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
