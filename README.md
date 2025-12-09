# YTPro Video İndirici 🎬

YouTube videolarını MP4 ve MP3 formatında indirmenizi sağlayan web uygulaması.

## 🌐 Canlı Demo

**👉 [https://youtube-video-downloader-f7ae.onrender.com](https://youtube-video-downloader-f7ae.onrender.com)**

---

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Özellikler

- ✅ YouTube video bilgilerini çekme (başlık, thumbnail, kanal)
- ✅ YouTube Shorts desteği
- ✅ 1080p Full HD MP4 indirme
- ✅ 720p HD MP4 indirme
- ✅ 320kbps yüksek kalite MP3 indirme
- ✅ Modern ve responsive arayüz

## Yerel Kurulum

### 1. Gereksinimler

- Python 3.8+
- FFmpeg

### 2. FFmpeg Kurulumu

**Windows:**
```bash
winget install Gyan.FFmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 3. Python Bağımlılıkları

```bash
pip install -r requirements.txt
```

### 4. Sunucuyu Başlatın

```bash
python server.py
```

### 5. Tarayıcıda Açın

http://localhost:5000

## Kullanım

1. YouTube video URL'sini yapıştırın
2. "Başla" butonuna tıklayın
3. İstediğiniz formatı seçin (MP4 veya MP3)
4. İndirme tamamlanana kadar bekleyin

## Teknolojiler

- **Backend:** Python, Flask, yt-dlp
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Video İşleme:** FFmpeg
- **Hosting:** Render.com (Docker)

## Lisans

MIT License
