# YouTube Audio Downloader

YouTubeから音声ファイル（MP3）をダウンロードするPythonスクリプト

## インストール

```bash
pip install yt-dlp>=2025.6.30
```

FFmpegも必要です（音声変換用）

## 使用方法

### 基本的な使用方法

```python
from youtube_downloader import download_youtube_audio

url = "https://www.youtube.com/watch?v=VIDEO_ID"
download_youtube_audio(url)
```

### ブラウザ指定での使用方法

```python
from youtube_downloader import download_with_browser_cookies

# Chrome/Firefox等のブラウザを閉じてから実行
download_with_browser_cookies(url, 'chrome')
```

## エラー対処法

「Sign in to confirm you're not a bot」エラーが出る場合：

1. **ブラウザを完全に閉じる**（特にChrome）
2. **VPNを無効にする**
3. **数時間後に再試行**
4. **別のネットワーク環境で試行**

## 解決策の仕組み

このスクリプトは以下の3段階で動作します：

1. **ブラウザクッキー使用**: `cookies_from_browser`でブラウザの認証情報を使用
2. **代替クライアント**: `android_testsuite`クライアントで認証回避
3. **最低品質フォールバック**: 最低品質で強制ダウンロード

## 注意事項

- 2025年以降、YouTubeのボット検出が厳しくなっています
- 大量ダウンロードは避けてください
- 利用規約を遵守してください
