FROM python:3.11-slim

# FFmpeg kurulumu
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port
EXPOSE 10000

# Başlat
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "server:app"]
