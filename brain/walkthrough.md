# Walkthrough

## Proje Hakkında

YTPro, YouTube videolarını MP4 ve MP3 formatında indirmenizi sağlayan bir web uygulamasıdır.

## Proje Yapısı

```
Youtube Downloader/
├── index.html       # Ana sayfa ve UI
├── server.py        # Flask backend API
├── requirements.txt # Python bağımlılıkları
├── Dockerfile       # Docker konfigürasyonu
├── Procfile         # Render.com için
├── render.yaml      # Render.com ayarları
└── brain/           # Proje belgeleri
```

## Kurulum

1. **Bağımlılıkları yükle:**

   ```bash
   pip install -r requirements.txt
   ```

2. **FFmpeg kurulumu:**

   ```bash
   winget install Gyan.FFmpeg  # Windows
   brew install ffmpeg         # Mac
   sudo apt install ffmpeg     # Linux
   ```

3. **Sunucuyu başlat:**

   ```bash
   python server.py
   ```

4. http://localhost:5000 adresinden erişin

## Önemli Dosyalar

- `server.py` - Flask API endpoints (/api/info, /api/download)
- `index.html` - Tüm frontend kodu (HTML, CSS, JS bir arada)

## API Endpoints

| Endpoint        | Method | Açıklama                |
| --------------- | ------ | ----------------------- |
| `/api/info`     | POST   | Video bilgilerini getir |
| `/api/download` | POST   | Video/ses indir         |

## Notlar

- yt-dlp düzenli olarak güncellenmeli (YouTube değişiklikleri için)
- FFmpeg, MP3 dönüştürme için zorunlu
- Render.com free tier'da 15 dakika inaktivite sonrası uyku moduna geçer
