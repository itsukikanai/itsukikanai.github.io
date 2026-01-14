# ポートフォリオサイト仕様書

[English (README.md)](./README.md) | **[🇯🇵 日本語 (現在)](./README_ja.md)**

本書は、`itsukikanai.github.io` ポートフォリオサイトの技術仕様、ディレクトリ構造、および設計ガイドラインを概説するものです。

## 1. ディレクトリ構造

メンテナンス性と拡張性を確保するため、厳格なディレクトリ階層に従います。

```
site-root/
├── README.md             # プロジェクト仕様書 (英語)
├── README_ja.md          # プロジェクト仕様書 (日本語)
├── index.html            # メインエントリーポイント
├── css/                  # グローバルスタイルシート
├── js/                   # ロジックスクリプト (LayoutManager等)
├── img/                  # 画像アセット
├── assets/               # 静的リソース (PDF, 動画, 音声等)
├── projects/             # ポートフォリオプロジェクト・セクション
│   ├── index.html        # プロジェクト一覧
│   ├── private/          # 非公開/開発中プロジェクト
│   ├── ai-video-tool/    # AI Video Tool ランディングページ
│   └── stealthtext/      # StealthText ツール & 履歴
└── [config files]        # (favicon.ico, .gitignore, etc.)
```

### ルール
- **厳格なルーティング**: ページレンダリングには `index.html` のみを使用してください。
    - 例: `about.html` は禁止です。`about/index.html` とする必要があります。
    - これは、全てのサブディレクトリ（例: `projects/stealthtext/history/index.html`）に適用されます。
- **ルート順序**: `index.html` > リソース (`css/`, `js/`, `img/`) > 設定ファイル。
- **セクショニング**: 独立したセクション（例: `projects/`）は、独自の `index.html` を含むディレクトリを持つ必要があります。
- **アセット**: 画像以外のバイナリ資産は、タイプ別に分類して `assets/` に配置します。

## 2. 技術スタック

### コア
- **HTML5**: セマンティックマークアップ。
- **TailwindCSS**: 全スタイリングに使用 (CDN via JavaScript)。
    - *設定*: カスタムカラーパレット（ダークモード重視）、フォント（Inter/Outfit）。
- **JavaScript (Vanilla)**: 
    - `main.js`: グローバルロジック（テーマ、言語管理）。
    - `layout.js`: ヘッダー/フッターの動的レンダリング (`LayoutManager`)。

### デザインシステム
- **テーマ**: プレミアムダークモード。
    - 背景色: 深いスレート/ブラック (`#0a0a0a`, `#0f172a`)。
    - アクセント: 鮮やかなインディゴ、シアン、パープルのグラデーション。
- **タイポグラフィ**: `Outfit` (見出し) および `Inter` (本文)。
- **ビジュアル**: グラスモーフィズム（背景ぼかし）、スムーズなグラデーション、マイクロインタラクション。

## 3. デプロイメント
- **プラットフォーム**: GitHub Pages。
- **URL構造**: `username.github.io/path/to/resource`。
- **セキュリティ**: 機密データ（`.env`、大規模データセット等）は `.gitignore` により除外されます。

---

## プロジェクト概要

### 1. AI Video Tool
*場所: `/projects/ai-video-tool/`*
AI動画管理ツールのための専用ランディングページ。
- **主な機能**: スマートダウンロード (yt-dlp)、AI分析 (Google Gemini)、FTS5全文検索、FFmpegによる自動編集。
- **技術**: Python, Gradio, SQLite, Google GenAI。

### 2. StealthText
*場所: `/projects/stealthtext/`*
不可視テキストを埋め込むクライアントサイド・ステガノグラフィツール。
- **主な機能**: ゼロ幅文字埋め込み、AES暗号化、整合性検証 (HMAC)、選択安全な埋め込み戦略。
- **技術**: JavaScript, Crypto.js, TailwindCSS。

### 3. Private Projects (非公開)
*場所: `/projects/private/`*
未公開または開発中のプロジェクトのためのプレースホルダー。

---
© 2026 Itsuki Kanai
