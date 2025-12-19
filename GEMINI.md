# YTPro - Gemini CLI Kuralları

## 📁 Proje Yapısı

```
Youtube Downloader/
├── index.html       # Frontend (HTML + CSS + JS tek dosyada)
├── server.py        # Flask backend API
├── requirements.txt # Python bağımlılıkları
├── brain/           # Proje belgeleri ve görev takibi
└── docs/            # Ek dokümantasyon
```

## 🔧 Geliştirme Kuralları

### Backend (Python/Flask)

- Flask route'ları RESTful prensiplerine uygun olmalı
- yt-dlp işlemleri için try-except kullan
- Dosya işlemleri için geçici dizin kullan ve temizle
- API yanıtları JSON formatında olmalı

### Frontend (HTML/JS)

- Tailwind CSS sınıfları kullan
- JavaScript için vanilla JS tercih et
- Async/await ile API çağrıları yap
- Loading state'leri göster

### Kod Stili

```python
# Flask route örneği
@app.route('/api/info', methods=['POST'])
def get_video_info():
    try:
        url = request.json.get('url')
        # yt-dlp işlemleri
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

## 🚀 Deployment

### Render.com

- Dockerfile kullan
- Environment variables: Yok (gerekirse render.yaml'a ekle)
- Build command: Docker otomatik

### Yerel Geliştirme

```bash
python server.py
# http://localhost:5000
```

## 📋 Commit Mesajları

```
feat: yeni özellik
fix: bug düzeltmesi
docs: dokümantasyon
refactor: kod iyileştirme
```

## ⚠️ Dikkat Edilmesi Gerekenler

1. **yt-dlp güncellemesi:** YouTube API değişikliklerinde hata alınabilir
2. **FFmpeg:** MP3 dönüştürme için zorunlu
3. **Rate limiting:** YouTube tarafından engellenme riski
4. **Dosya boyutu:** Büyük videolar için timeout olabilir
