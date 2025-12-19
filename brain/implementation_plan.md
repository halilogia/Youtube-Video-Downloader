# Uygulama Planı

## Mevcut Durum

Proje aktif ve canlı ortamda çalışıyor: [YTPro](https://youtube-video-downloader-f7ae.onrender.com)

## Mimari

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Flask API     │────▶│   yt-dlp        │
│   (HTML/JS)     │     │   (Python)      │     │   + FFmpeg      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Teknik Kararlar

| Karar        | Seçim      | Gerekçe                                    |
| ------------ | ---------- | ------------------------------------------ |
| Backend      | Flask      | Hafif, hızlı, yt-dlp ile kolay entegrasyon |
| Video İşleme | yt-dlp     | En güncel YouTube desteği                  |
| Codec        | FFmpeg     | Format dönüştürme için standart            |
| Hosting      | Render.com | Ücretsiz tier, Docker desteği              |
| Frontend     | Vanilla JS | Basitlik, bağımlılık yok                   |
| CSS          | Tailwind   | Hızlı prototipleme                         |

## Sonraki Adımlar

1. Playlist desteği ekle
2. İndirme geçmişi (localStorage)
3. PWA manifest ekle
4. Tema desteği
