# AI Video Tool

YouTube動画のダウンロード、管理、AI分析、そして切り抜き動画の作成（モンタージュ）を支援するツールです。
Google Gemini (Flashモデル) を活用し、動画の字幕やチャットコメントを解析して、効率的に動画の内容を把握・編集できます。

## 主な機能

### 1. 動画収集 (Archive)
- **YouTube動画ダウンロード**: `yt-dlp` を使用して高画質で保存。
- **字幕・チャット取得**:
  - 字幕 (Subtitles) を自動取得し、検索可能なデータとして保存。
  - ライブ配信のアーカイブ等の場合、`chat-downloader` を使用してチャットリプレイを取得し、AI分析のコンテキストに使用。

### 2. ライブラリ管理 (Library)
- **動画一覧**: 保存済み動画の管理。
- **全文検索**: SQLite FTS5 を使用した字幕の高速全文検索。
- **スマートフィルタ**: AIが生成したタグでの絞り込み。
- **プレビュー**: 検索ヒット箇所からの即時再生。

### 3. AI分析 (Analysis)
Gemini 2.5 Flash を使用し、動画を多角的に分析します。
- **自動タグ付け**: コンテンツに基づいたタグ生成。
- **要約**: 動画全体の簡潔な日本語要約。
- **ハイライト抽出**: 盛り上がりシーンや重要な箇所を自動検出し、Start/End時間を特定。

### 4. 編集・モンタージュ (Editor)
- **ハイライト編集**: AIが抽出したハイライト、または手動で検索・指定した区間をリスト化。
- **結合動画の作成**: 複数の動画クリップを1本の動画に結合（FFmpeg使用）。
- **字幕のエクスポート**: `srt` / `vtt` 形式での書き出し。

## 必要条件

- **OS**: Windows (推奨), Mac, Linux
- **Python**: 3.10 以上
- **FFmpeg**: インストール済みでPATHが通っていること
- **Gemini API Key**: Google AI Studio で取得したもの

## セットアップ手順

### 1. Pythonの準備
Python 3.10以上がインストールされていない場合は [公式サイト](https://www.python.org/downloads/) からインストールしてください。
※ Windowsの方はインストール時に **"Add Python to PATH"** にチェックを入れてください。

### 2. FFmpegのインストール
動画処理に必須です。
1. [FFmpeg公式サイト](https://ffmpeg.org/download.html) からビルド済みバイナリをダウンロード。
2. 解凍し、`bin` フォルダへのパスをシステム環境変数 Path に追加。
3. ターミナルで `ffmpeg -version` が通ればOKです。

### 3. プロジェクトのセットアップ
リポジトリをクローンまたはダウンロードし、ディレクトリ内でターミナルを開きます。

**仮想環境の作成と有効化:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**依存ライブラリのインストール:**
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
プロジェクトルートに `.env` ファイルを作成し、GeminiのAPIキーを設定します。

`.env` 例:
```ini
API_KEY_GEMINI=your_api_key_here
```
※ アプリ起動後の設定画面からも入力可能です。

## 使い方

1. **アプリの起動**
   ```bash
   python main.py
   ```
2. **ブラウザでアクセス**
   自動的にブラウザが開きます（開かない場合は `http://127.0.0.1:7860` にアクセス）。

3. **操作フロー**
   - **Settings**: APIキーの設定、モデルの選択。
   - **Archive**: 動画URLを入力してダウンロード。
   - **Library**: 動画の検索、AI分析の実行（"Analyze"ボタン）、プレビュー。
   - **Editor**: 分析結果のハイライトを確認、微調整して「Render Montage」で動画書き出し。

## Google Colabでの実行

強力なGPU環境（Google Colab）でも実行可能です。

1. [Google Colab](https://colab.research.google.com/) を開きます。
2. 以下のいずれかの方法でノートブックを開きます。
   - **GitHubから**: このリポジトリのURLを指定して `ai_video_tool.ipynb` を開く。
   - **アップロード**: ローカルにある `ai_video_tool.ipynb` をアップロードする。
3. ノートブックの上から順にセルを実行します。
   - 途中でAPIキーの入力を求められます。
4. 最後に表示される `public URL` (例: `https://xxxx.gradio.live`) にアクセスします。

## ディレクトリ構成

- `app/`: アプリケーションのソースコード
- `data/`: ダウンロードした動画やデータベース (`db.sqlite3`) の保存先 (Git管理外)
- `tools/`: メンテナンス用スクリプト (DBリセット、インポート/エクスポート等)
- `exports/`: 作成されたモンタージュ動画や字幕ファイルの出力先

## メンテナンス

データベースをリセットしたい場合などは `tools/` 内のスクリプトを使用できます。
例: `python tools/reset_db.py`

## 技術スタック
- Gradio (UI)
- SQLite + FTS5 (Database)
- Google Gemini (AI)
- yt-dlp & chat-downloader (Crawler)
- FFmpeg (Video Processing)
