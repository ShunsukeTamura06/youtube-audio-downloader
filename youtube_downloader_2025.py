import yt_dlp
import os
import subprocess
import sys

def check_requirements():
    """必要な依存関係をチェックしてインストール"""
    print("=== 2025年YouTube Bot Detection 対応版 ===")
    print("PO Token プラグインをチェック中...")
    
    try:
        # yt-dlpのバージョンチェック
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'yt-dlp'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("yt-dlpをインストール中...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp>=2025.05.22'])
        
        # PO Token プラグインのインストール
        print("PO Token プラグインをインストール中...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'bgutil-ytdlp-pot-provider'], 
                      check=True)
        print("✓ PO Token プラグインインストール完了")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ インストールエラー: {e}")
        return False

def start_pot_server():
    """Dockerを使用してPO Token サーバーを起動"""
    try:
        print("PO Token サーバーを起動中...")
        # Dockerコンテナが既に動いているかチェック
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if 'bgutil-provider' in result.stdout:
            print("✓ PO Token サーバーは既に動作中")
            return True
        
        # Dockerでサーバー起動
        subprocess.run([
            'docker', 'run', '--name', 'bgutil-provider', 
            '-d', '-p', '4416:4416', 
            'brainicism/bgutil-ytdlp-pot-provider'
        ], check=True)
        print("✓ PO Token サーバー起動完了")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Docker未インストールまたはエラー - 代替方法を使用")
        return False

def download_youtube_audio_2025(url, output_path='./downloads'):
    """2025年対応版YouTube音声ダウンローダー"""
    os.makedirs(output_path, exist_ok=True)
    
    # 必要な依存関係をチェック
    if not check_requirements():
        print("依存関係のインストールに失敗しました")
        return False
    
    # PO Token サーバーを起動（可能な場合）
    server_running = start_pot_server()
    
    print(f"\n動画をダウンロード中: {url}")
    
    # 2025年対応設定
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'verbose': True,
    }
    
    # サーバーが動作している場合は何もしない（プラグインが自動処理）
    # 動作していない場合でもプラグインがフォールバック処理を行う
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✓ ダウンロード完了！")
        return True
    except Exception as e:
        print(f"✗ ダウンロードエラー: {e}")
        print("\nトラブルシューティング:")
        print("1. yt-dlp -v <URL> でverboseログを確認")
        print("2. PO Token プラグインが正しくインストールされているか確認")
        print("3. Dockerが利用可能な場合は再起動を試行")
        return False

def install_setup():
    """初回セットアップ用関数"""
    print("=== YouTube Audio Downloader 2025年版 初回セットアップ ===")
    
    print("\n1. yt-dlpとPO Tokenプラグインをインストール中...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp>=2025.05.22'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'bgutil-ytdlp-pot-provider'])
    
    print("\n2. Dockerの確認...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Docker利用可能")
            print("PO Token サーバーを起動中...")
            subprocess.run([
                'docker', 'run', '--name', 'bgutil-provider', 
                '-d', '-p', '4416:4416', 
                'brainicism/bgutil-ytdlp-pot-provider'
            ])
            print("✓ セットアップ完了！")
        else:
            print("⚠ Docker未インストール - プラグインのみで動作します")
    except FileNotFoundError:
        print("⚠ Docker未インストール - プラグインのみで動作します")
    
    print("\n=== セットアップ完了 ===")
    print("使用方法: download_youtube_audio_2025('https://www.youtube.com/watch?v=VIDEO_ID')")

# 使用例
if __name__ == "__main__":
    # 初回セットアップ（コメントアウトを外して実行）
    # install_setup()
    
    # 音声ダウンロード
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    download_youtube_audio_2025(url)
