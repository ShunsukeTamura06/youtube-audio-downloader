# 🎵 YouTube Audio Downloader - 2025年対応版

**重要**: 2025年のYouTubeボット検出対応版です。従来の方法では動作しません。

## ❗ 問題の原因

2025年、YouTubeは新しい「PO Token (Proof-of-Origin Token)」システムを導入し、従来のcookies・user-agentベースの回避方法では「Sign in to confirm you're not a bot」エラーが発生するようになりました。

## ✅ 解決策

**PO Tokenプラグイン**を使用して自動的にボット検出を回避します。

## 🚀 簡単インストール

### 方法1: 自動セットアップ（推奨）

```python
# youtube_downloader_2025.py をダウンロードして実行
python youtube_downloader_2025.py
```

### 方法2: 手動インストール

**Step 1**: 必要なパッケージをインストール

```bash
pip install -U yt-dlp>=2025.05.22
pip install -U bgutil-ytdlp-pot-provider
```

**Step 2**: PO Token サーバーを起動（Dockerが利用可能な場合）

```bash
docker run --name bgutil-provider -d -p 4416:4416 brainicism/bgutil-ytdlp-pot-provider
```

**Step 3**: 確認

```bash
yt-dlp -v https://www.youtube.com/watch?v=VIDEO_ID
```

ログに `[debug] [youtube] [pot] PO Token Providers: bgutil:http-1.1.0 (external)` が表示されれば成功です。

## 📝 使用方法

### Pythonで使用

```python
from youtube_downloader_2025 import download_youtube_audio_2025

url = "https://www.youtube.com/watch?v=VIDEO_ID"
download_youtube_audio_2025(url)
```

### コマンドラインで使用

```bash
yt-dlp --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=VIDEO_ID
```

## 🔧 Dockerなしでの利用

Dockerが利用できない場合、プラグインがスクリプトモードで自動動作します。

## ⚠️ 注意事項

- yt-dlp 2025.05.22以上が必要
- PO Tokenは12時間で期限切れになりますが、プラグインが自動更新します
- 大量ダウンロードは避けてください

## 🆘 トラブルシューティング

### エラーが続く場合

1. **プラグイン確認**:
   ```bash
   yt-dlp -v URL 2>&1 | grep "PO Token Providers"
   ```

2. **yt-dlpバージョン確認**:
   ```bash
   yt-dlp --version
   ```

3. **Docker再起動**（使用している場合）:
   ```bash
   docker restart bgutil-provider
   ```

### よくあるエラー

- `ModuleNotFoundError: No module named 'bgutil_ytdlp_pot_provider'`
  → `pip install -U bgutil-ytdlp-pot-provider`

- `PO Token Providers: (none)`
  → プラグインが正しくインストールされていません

## 🔗 技術詳細

- PO Tokenについて詳しくは [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#youtube)
- BgUtils プロジェクトによるBotGuard attestation実装を使用

---

**このバージョンで2025年のYouTubeボット検出を確実に回避できます！**
