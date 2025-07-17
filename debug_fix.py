import yt_dlp
import os
import subprocess
import sys
import time
import json

def diagnose_setup():
    """セットアップ状況を詳細診断"""
    print("=== 詳細診断中 ===\n")
    
    # 1. yt-dlpバージョン確認
    try:
        result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                              capture_output=True, text=True)
        print(f"✓ yt-dlp バージョン: {result.stdout.strip()}")
    except Exception as e:
        print(f"✗ yt-dlp エラー: {e}")
        return False
    
    # 2. プラグイン確認
    try:
        result = subprocess.run([sys.executable, '-c', 
                               "import bgutil_ytdlp_pot_provider; print('PO Token プラグイン: OK')"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ PO Token プラグインインストール済み")
        else:
            print("✗ PO Token プラグインが見つからない")
            return False
    except Exception as e:
        print(f"✗ プラグインエラー: {e}")
        return False
    
    # 3. Dockerサーバー確認
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if 'bgutil-provider' in result.stdout and 'Up' in result.stdout:
            print("✓ PO Token サーバー動作中")
            server_running = True
        else:
            print("⚠ PO Token サーバー未起動")
            server_running = False
    except:
        print("⚠ Docker未利用")
        server_running = False
    
    # 4. プラグイン認識テスト
    print("\n=== プラグイン認識テスト ===")
    try:
        # ダミーURLでプラグイン認識確認
        result = subprocess.run([
            sys.executable, '-m', 'yt_dlp', '-v', '--no-download',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        ], capture_output=True, text=True, timeout=30)
        
        output = result.stdout + result.stderr
        
        if 'PO Token Providers:' in output:
            print("✓ PO Token プラグイン認識済み")
            # プラグイン詳細を抽出
            for line in output.split('\n'):
                if 'PO Token Providers:' in line:
                    print(f"  → {line.strip()}")
            working = True
        else:
            print("✗ PO Token プラグインが認識されていない")
            print("デバッグ情報:")
            print(output[-500:])  # 最後の500文字を表示
            working = False
    except subprocess.TimeoutExpired:
        print("⚠ テストタイムアウト")
        working = False
    except Exception as e:
        print(f"✗ テストエラー: {e}")
        working = False
    
    return working

def force_install_fix():
    """強制的に問題を修正"""
    print("\n=== 強制修正中 ===")
    
    # 1. 完全にクリーンインストール
    print("1. 既存パッケージを削除...")
    subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'yt-dlp', 'bgutil-ytdlp-pot-provider'])
    
    # 2. 最新版を再インストール
    print("2. 最新版をインストール...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp>=2025.05.22'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'bgutil-ytdlp-pot-provider'])
    
    # 3. Dockerサーバー再起動
    print("3. PO Token サーバー再起動...")
    try:
        subprocess.run(['docker', 'stop', 'bgutil-provider'], capture_output=True)
        subprocess.run(['docker', 'rm', 'bgutil-provider'], capture_output=True)
        subprocess.run([
            'docker', 'run', '--name', 'bgutil-provider', 
            '-d', '-p', '4416:4416', 
            'brainicism/bgutil-ytdlp-pot-provider'
        ])
        print("✓ Dockerサーバー再起動完了")
    except:
        print("⚠ Docker再起動スキップ")
    
    print("=== 修正完了 ===\n")

def debug_download(url, output_path='./downloads'):
    """デバッグ情報付きダウンロード"""
    os.makedirs(output_path, exist_ok=True)
    
    print(f"=== デバッグダウンロード開始 ===")
    print(f"URL: {url}")
    
    # 最大限詳細なログ設定
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'verbose': True,
        'debug': True,
        'print_traffic': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("--- yt-dlp詳細ログ開始 ---")
            ydl.download([url])
        print("✓ ダウンロード成功！")
        return True
    except Exception as e:
        print(f"\n✗ ダウンロードエラー: {e}")
        print("\n=== エラー分析 ===")
        
        error_str = str(e)
        if "Sign in to confirm you're not a bot" in error_str:
            print("🔍 分析: PO Token プラグインが動作していません")
            print("💡 解決策:")
            print("  1. force_install_fix() を実行してください")
            print("  2. Dockerを再起動してください")
            print("  3. 別のネットワークで試してください")
        elif "HTTP Error 403" in error_str:
            print("🔍 分析: アクセス拒否エラー")
            print("💡 解決策: PO Token サーバーが必要です")
        elif "module" in error_str:
            print("🔍 分析: モジュールエラー")
            print("💡 解決策: pip install を再実行してください")
        
        return False

def test_specific_video():
    """特定の動画でテスト"""
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (確実に存在)
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
    ]
    
    print("=== 複数動画テスト ===")
    for i, url in enumerate(test_urls, 1):
        print(f"\nテスト {i}: {url}")
        success = debug_download(url)
        if success:
            print(f"✓ テスト {i} 成功")
            return True
        else:
            print(f"✗ テスト {i} 失敗")
    
    return False

# メイン診断・修正関数
def fix_bot_detection_issue():
    """ボット検出問題を完全解決"""
    print("🔧 YouTube Bot Detection 問題 完全診断・修正ツール")
    print("=" * 60)
    
    # Step 1: 診断
    if not diagnose_setup():
        print("\n❌ セットアップに問題があります。修正します...")
        force_install_fix()
        time.sleep(5)
        
        # 再診断
        if not diagnose_setup():
            print("❌ 修正後も問題が続いています。手動確認が必要です。")
            return False
    
    # Step 2: 実際のダウンロードテスト
    print("\n🧪 実際のダウンロードテスト...")
    if not test_specific_video():
        print("\n❌ ダウンロードテストに失敗しました。")
        print("\n🔧 最終手段を試行中...")
        force_install_fix()
        time.sleep(10)
        
        if not test_specific_video():
            print("\n💀 全ての修正方法が失敗しました。")
            print("\n📋 最終確認事項:")
            print("1. インターネット接続確認")
            print("2. VPN無効化")
            print("3. 数時間後に再試行")
            print("4. 別のPCまたはネットワークで試行")
            return False
    
    print("\n🎉 修正完了！正常にダウンロードできるようになりました。")
    return True

# 使用例
if __name__ == "__main__":
    # 完全診断・修正実行
    fix_bot_detection_issue()
