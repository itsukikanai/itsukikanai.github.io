---
aliases: []
created: 2026-01-15 00:24:09
i18n:
  en: "[[README]]"
modified: 2026-04-14 17:01:30
parent: "[[README]]"
tags: []
title: ポートフォリオサイト仕様書
uid: 62f24516-31ce-4a3c-b725-b5c0896f187d
---

# ポートフォリオサイト仕様書

[ポートフォリオサイト](https://itsukikanai.github.io)

**[EN English (README.md)](./README.md)** | **JA 日本語 (このファイル)**

本書は、`itsukikanai.github.io` ポートフォリオサイトの技術仕様、ディレクトリ構造、および設計ガイドラインを概説するものです。

## 0. 目次 ^chapter-0

- [[README_ja#^chapter-0|0. 目次]]
- [[README_ja#^chapter-1|1. ディレクトリ構造]]
  - [[README_ja#^chapter-1-1|1.1. ルール]]
- [[README_ja#^chapter-2|2. 技術スタック]]
  - [[README_ja#^chapter-2-1|2.1. コア]]
  - [[README_ja#^chapter-2-2|2.2. デザインシステム]]
- [[README_ja#^chapter-3|3. デプロイメント]]
- [[README_ja#^chapter-4|4. プロジェクト概要]]
  - [[README_ja#^chapter-4-1|4.1. AI Video Tool]]
  - [[README_ja#^chapter-4-2|4.2. StealthText]]
  - [[README_ja#^chapter-4-3|4.3. HTML Converter]]
  - [[README_ja#^chapter-4-4|4.4. URI Redirector]]
  - [[README_ja#^chapter-4-5|4.5. Private Projects]]
  - [[README_ja#^chapter-4-6|4.6. Sandbox]]
- [[README_ja#^chapter-5|5. その他]]
  - [[README_ja#^chapter-5-1|5.1. 免責事項]]

## 1. ディレクトリ構造 ^chapter-1

メンテナンス性と拡張性を確保するため、厳格なディレクトリ階層に従います。

```text
root/
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
│   ├── stealthtext/      # StealthText ツール & 履歴
│   └── sandbox/          # ベータ版/未翻訳版
└── [config files]        # (favicon.ico, .gitignore, etc.)
```

### 1.1. ルール ^chapter-1-1

- **厳格なルーティング**: ページレンダリングには `index.html` のみを使用してください。
  - 例: `about.html` は禁止です。`about/index.html` とする必要があります。
  - これは、全てのサブディレクトリ（例: `projects/stealthtext/history/index.html`）に適用されます。
- **ルート順序**: `index.html` > リソース (`css/`, `js/`, `img/`) > 設定ファイル。
- **セクショニング**: 独立したセクション（例: `projects/`）は、独自の `index.html` を含むディレクトリを持つ必要があります。
- **アセット**: 画像以外のバイナリ資産は、タイプ別に分類して `assets/` に配置します。

## 2. 技術スタック ^chapter-2

### 2.1. コア ^chapter-2-1

- **HTML5**: セマンティックマークアップ。
- **TailwindCSS**: 全スタイリングに使用 (CDN via JavaScript)。
  - *設定*: カスタムカラーパレット（ダークモード重視）、フォント（Inter/Outfit）。
- **JavaScript (Vanilla)**:
  - `main.js`: グローバルロジック（テーマ、言語管理）。
  - `layout.js`: ヘッダー/フッターの動的レンダリング (`LayoutManager`)。

### 2.2. デザインシステム ^chapter-2-2

- **テーマ**: プレミアムダークモード。
  - 背景色: 深いスレート/ブラック (`#0a0a0a`, `#0f172a`)。
  - アクセント: 鮮やかなインディゴ、シアン、パープルのグラデーション。
- **タイポグラフィ**: `Outfit` (見出し) および `Inter` (本文)。
- **ビジュアル**: グラスモーフィズム（背景ぼかし）、スムーズなグラデーション、マイクロインタラクション。

## 3. デプロイメント ^chapter-3

- **プラットフォーム**: GitHub Pages。
- **URL構造**: `username.github.io/path/to/resource`。
- **セキュリティ**: 機密データ（`.env`、大規模データセット等）は `.gitignore` により除外されます。

## 4. プロジェクト概要 ^chapter-4

[プロジェクト](https://itsukikanai.github.io/projects)

### 4.1. AI Video Tool ^chapter-4-1

[AI Video Tool プロジェクト](https://itsukikanai.github.io/projects/ai-video-tool)

*場所: `/projects/ai-video-tool/`*
AI動画管理ツールのための専用ランディングページ。

- **主な機能**: スマートダウンロード (yt-dlp)、AI分析 (Google Gemini)、FTS5全文検索、FFmpegによる自動編集。
- **技術**: Python, Gradio, SQLite, Google GenAI。

### 4.2. StealthText ^chapter-4-2

[StealthText プロジェクト](https://itsukikanai.github.io/projects/stealthtext)

*場所: `/projects/stealthtext/`*
不可視テキストを埋め込むクライアントサイド・ステガノグラフィツール。

- **主な機能**: ゼロ幅文字埋め込み、AES暗号化、整合性検証 (HMAC)、選択安全な埋め込み戦略。
- **技術**: JavaScript, Crypto.js, TailwindCSS。

### 4.3. HTML Converter ^chapter-4-3

[HTML Converter プロジェクト](https://itsukikanai.github.io/projects/html-converter)

*場所: `/projects/html-converter/`*
単一HTMLをCSS/JSに分割、または統合するユーティリティ。ZIP出力/PWA対応。

- **主な機能**: Live Preview, ZIP Download, PWA Installation Support, File Import/Export.
- **技術**: JSZip, File API, TailwindCSS.

### 4.4. URI Redirector ^chapter-4-4

[URI Redirector プロジェクト](https://itsukikanai.github.io/go)

*場所: `/go/index.html`*
Obsidian, Notion, iA Writerなどのアプリ内リンクを外部ウェブリンクに変換・リダイレクトするツール。

- **主な機能**: URLスキームへのリダイレクト、Web用リンクの生成、アプリごとのテーマ適応。
- **技術**: Vanilla JS, CSS Variables.

### 4.5. Private Projects (非公開) ^chapter-4-5

[Private Projects ディレクトリ](https://itsukikanai.github.io/projects/private)

*場所: `/projects/private/`*
未公開または開発中のプロジェクトのためのプレースホルダー。

### 4.6. Sandbox ^chapter-4-6

[Sandbox ディレクトリ](https://itsukikanai.github.io/projects/sandbox)

*場所: `/projects/sandbox/`*
ベータ版、未翻訳版などを仮で公開するためのディレクトリです。

## 5. その他 ^chapter-5

### 5.1. 免責事項 ^chapter-5-1

[免責事項](https://itsukikanai.github.io/disclaimer)

---

&copy; 2026- Itsuki Kanai. All rights reserved.
