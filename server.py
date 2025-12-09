"""
YouTube Video İndirici - Flask Backend
========================================
yt-dlp kullanarak YouTube videolarını indiren REST API.

Kullanım:
    pip install -r requirements.txt
    python server.py

Gereksinimler:
    - Python 3.8+
    - FFmpeg (sistem düzeyinde kurulu olmalı)
      Windows: winget install Gyan.FFmpeg
      Mac: brew install ffmpeg
"""

import os
import re
import uuid
import shutil
from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Geçici indirme klasörü
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def sanitize_filename(filename):
    """Dosya adından geçersiz karakterleri temizle"""
    # Windows'ta geçersiz karakterler
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Başındaki ve sonundaki boşlukları/noktaları temizle
    filename = filename.strip('. ')
    return filename[:200]  # Max 200 karakter


@app.route('/')
def serve_index():
    """Ana sayfa - index.html'i serve et"""
    return send_file('index.html')


@app.route('/api/info', methods=['GET'])
def get_video_info():
    """
    Video bilgilerini getir (metadata)
    
    Query Params:
        url: YouTube video URL'si
        
    Returns:
        JSON: {title, author, thumbnail, duration, formats}
    """
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL parametresi gerekli"}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Mevcut formatları analiz et
            formats = []
            has_audio = False
            
            for f in info.get('formats', []):
                # Video formatları
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    height = f.get('height', 0)
                    if height >= 1080:
                        formats.append({
                            'id': 'best[height<=1080]',
                            'label': '1080p Full HD',
                            'type': 'mp4',
                            'quality': '1080p'
                        })
                    if height >= 720:
                        formats.append({
                            'id': 'best[height<=720]',
                            'label': '720p HD', 
                            'type': 'mp4',
                            'quality': '720p'
                        })
                
                # Ses formatları
                if f.get('acodec') != 'none':
                    has_audio = True
            
            # Varsayılan formatları ekle
            unique_formats = []
            seen_qualities = set()
            
            # 1080p
            if '1080p' not in seen_qualities:
                unique_formats.append({
                    'id': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                    'label': '1080p Full HD',
                    'type': 'mp4',
                    'quality': '1080p',
                    'size': '~145 MB'
                })
                seen_qualities.add('1080p')
            
            # 720p
            if '720p' not in seen_qualities:
                unique_formats.append({
                    'id': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                    'label': '720p HD',
                    'type': 'mp4', 
                    'quality': '720p',
                    'size': '~85 MB'
                })
                seen_qualities.add('720p')
            
            # MP3 (ses)
            if has_audio or True:  # Her zaman MP3 seçeneği sun
                unique_formats.append({
                    'id': 'bestaudio/best',
                    'label': '320kbps Yüksek Kalite',
                    'type': 'mp3',
                    'quality': '320kbps',
                    'size': '~5 MB'
                })
            
            return jsonify({
                "success": True,
                "title": info.get('title', 'Bilinmeyen Video'),
                "author": info.get('uploader', info.get('channel', 'Bilinmeyen Kanal')),
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration_string', ''),
                "view_count": info.get('view_count', 0),
                "formats": unique_formats
            })
            
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Video bulunamadı: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": f"Bir hata oluştu: {str(e)}"}), 500


@app.route('/api/download', methods=['GET'])
def download_video():
    """
    Video indir ve stream olarak gönder
    
    Query Params:
        url: YouTube video URL'si
        format_id: Format seçici (ör: 'bestvideo+bestaudio', 'bestaudio')
        type: 'mp4' veya 'mp3'
        
    Returns:
        Video/Audio dosyası (stream)
    """
    url = request.args.get('url')
    format_id = request.args.get('format_id', 'bestvideo+bestaudio/best')
    file_type = request.args.get('type', 'mp4')
    
    if not url:
        return jsonify({"error": "URL parametresi gerekli"}), 400
    
    # Benzersiz dosya adı oluştur
    unique_id = str(uuid.uuid4())[:8]
    temp_filename = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.%(ext)s')
    
    try:
        # yt-dlp ayarları
        ydl_opts = {
            'format': format_id,
            'outtmpl': temp_filename,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4' if file_type == 'mp4' else None,
        }
        
        # MP3 için sadece ses indir (henüz dönüştürme yapma)
        if file_type == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
        
        # Video bilgisini al ve indir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = sanitize_filename(info.get('title', 'video'))
        
        # İndirilen dosyayı bul
        extension = 'mp3' if file_type == 'mp3' else 'mp4'
        downloaded_file = None
        
        for f in os.listdir(DOWNLOAD_FOLDER):
            if f.startswith(unique_id):
                downloaded_file = os.path.join(DOWNLOAD_FOLDER, f)
                extension = f.split('.')[-1]
                break
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            return jsonify({"error": "Dosya indirilemedi"}), 500
        
        # MP3 için FFmpeg ile manuel dönüşüm yap (her zaman)
        if file_type == 'mp3':
            import subprocess
            mp3_file = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}_converted.mp3')
            
            # FFmpeg ile gerçek MP3'e dönüştür
            result = subprocess.run([
                'ffmpeg', '-y', '-i', downloaded_file,
                '-vn',  # Video yok
                '-acodec', 'libmp3lame', 
                '-ab', '320k',
                '-ar', '44100',  # Sample rate
                mp3_file
            ], capture_output=True)
            
            # Eski dosyayı sil, yeni dosyayı kullan
            if os.path.exists(mp3_file) and os.path.getsize(mp3_file) > 0:
                try:
                    os.remove(downloaded_file)
                except:
                    pass
                downloaded_file = mp3_file
                extension = 'mp3'
            else:
                # FFmpeg hatası varsa logla
                print(f"FFmpeg error: {result.stderr.decode() if result.stderr else 'unknown'}")
        
        # Dosyayı gönder
        safe_filename = f"{video_title}.{extension}"
        
        # İstek tamamlandıktan sonra dosyayı sil
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(downloaded_file):
                    os.remove(downloaded_file)
            except Exception as e:
                print(f"Cleanup hatası: {e}")
            return response
        
        # Response oluştur ve Content-Disposition header'ını manuel ayarla
        from flask import Response
        from urllib.parse import quote
        
        # Dosyayı oku
        with open(downloaded_file, 'rb') as f:
            file_data = f.read()
        
        # Dosya adını URL encode et (Türkçe karakterler için)
        encoded_filename = quote(safe_filename)
        
        response = Response(
            file_data,
            mimetype='video/mp4' if file_type == 'mp4' else 'audio/mpeg'
        )
        
        # Content-Disposition header - hem ASCII hem UTF-8 destekle
        response.headers['Content-Disposition'] = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
        response.headers['Content-Length'] = len(file_data)
        response.headers['X-Filename'] = encoded_filename  # Frontend için yedek
        
        # Dosyayı sil
        try:
            os.remove(downloaded_file)
        except:
            pass
        
        return response
        
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"İndirme hatası: {str(e)}"}), 500
    except Exception as e:
        # Hata durumunda temp dosyayı temizle
        for f in os.listdir(DOWNLOAD_FOLDER):
            if f.startswith(unique_id):
                try:
                    os.remove(os.path.join(DOWNLOAD_FOLDER, f))
                except:
                    pass
        return jsonify({"error": f"Bir hata oluştu: {str(e)}"}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """API sağlık kontrolü"""
    # FFmpeg kontrolü
    ffmpeg_installed = shutil.which('ffmpeg') is not None
    
    return jsonify({
        "status": "ok",
        "ffmpeg": ffmpeg_installed,
        "message": "FFmpeg kurulu değil! MP3 dönüşümü çalışmayabilir." if not ffmpeg_installed else "Tüm sistemler hazır."
    })


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🎬 YTPro Video İndirici                     ║
║                     Backend Sunucusu                         ║
╠══════════════════════════════════════════════════════════════╣
║  Sunucu başlatılıyor...                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # FFmpeg kontrolü
    if not shutil.which('ffmpeg'):
        print("⚠️  UYARI: FFmpeg bulunamadı! MP3 dönüşümü çalışmayabilir.")
        print("   Kurulum için: https://ffmpeg.org/download.html\n")
    else:
        print("✅ FFmpeg bulundu.\n")
    
    # Production için PORT environment variable kullan
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Adres: http://localhost:{port}\n")
    app.run(debug=False, port=port, host='0.0.0.0')

