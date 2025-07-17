import yt_dlp
import os
import sys

def download_youtube_audio(url, output_path='./downloads'):
    # ダウンロードフォルダを作成
    os.makedirs(output_path, exist_ok=True)
    
    print("方法1: ブラウザからクッキーを使用して試行中...")
    
    # 方法1: ブラウザからクッキーを直接読み取り（最も推奨）
    ydl_opts_cookies = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiesfrom': 'chrome',  # chrome, firefox, edge, safari等
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['web_creator', 'android_testsuite', 'android_music'],
                'skip': ['dash', 'hls']
            }
        },
        'sleep_interval': 3,
        'max_sleep_interval': 15,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_cookies) as ydl:
            ydl.download([url])
        print("✓ ブラウザクッキーでダウンロード完了")
        return
    except Exception as e:
        print(f"✗ ブラウザクッキー方法エラー: {e}")
        print("方法2: 代替設定で試行中...")
    
    # 方法2: android_testsuite クライアント（認証回避に効果的）
    ydl_opts_fallback = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android_testsuite'],
                'skip': ['dash', 'hls']
            }
        },
        'sleep_interval': 5,
        'max_sleep_interval': 20,
        'http_headers': {
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl:
            ydl.download([url])
        print("✓ 代替設定でダウンロード完了")
        return
    except Exception as e:
        print(f"✗ 代替設定エラー: {e}")
        print("方法3: 最低品質で試行中...")
    
    # 方法3: 最低品質でのフォールバック
    ydl_opts_minimal = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'worst',
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_minimal) as ydl:
            ydl.download([url])
        print("✓ 最低品質でダウンロード完了")
    except Exception as e:
        print(f"✗ 全ての方法が失敗: {e}")
        print("\n解決方法:")
        print("1. ブラウザ（Chrome/Firefox）を完全に閉じてから再実行")
        print("2. VPNを使用している場合は無効にする")
        print("3. 数時間後に再試行する")
        print("4. 別のネットワーク環境で試行する")

def download_with_browser_cookies(url, browser='chrome', output_path='./downloads'):
    """ブラウザを指定してクッキーを使用する方法"""
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiesfrom': browser,  # 'chrome', 'firefox', 'edge', 'safari'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✓ {browser}クッキーでダウンロード完了")
    except Exception as e:
        print(f"✗ {browser}クッキーエラー: {e}")

# 使用例
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    
    # 標準の方法で試行
    download_youtube_audio(url)
    
    # 特定のブラウザを指定する場合（注意：ブラウザを閉じること）
    # download_with_browser_cookies(url, 'firefox')
