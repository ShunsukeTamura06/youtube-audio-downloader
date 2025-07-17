import yt_dlp
import os

def download_youtube_audio(url, output_path='./downloads'):
    # ダウンロードフォルダを作成
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extract_flat': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android_music', 'android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'sleep_interval': 2,
        'max_sleep_interval': 10,
        'cookiefile': None,
        'age_limit': None,
        'geo_bypass': True,
        'no_warnings': False,
        'ignoreerrors': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("ダウンロード完了")
    except Exception as e:
        print(f"エラー: {e}")
        print("別の方法を試行中...")
        
        # フォールバック設定
        ydl_opts_fallback = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'worst',
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_testsuite']
                }
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl:
                ydl.download([url])
            print("フォールバックでダウンロード完了")
        except Exception as e2:
            print(f"フォールバックもエラー: {e2}")

# 使用例
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    download_youtube_audio(url)
