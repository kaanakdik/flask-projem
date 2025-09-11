# Temel imaj
FROM python:3.9-slim

# Çalışma dizini
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Gunicorn ile başlat
# app:app -> app.py dosyasındaki Flask instance adı
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
