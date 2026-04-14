---
aliases: []
created: 2026-01-15 00:24:09
i18n:
  en: "README.md"
modified: 2026-04-14 17:01:30
parent: "README.md"
tags: []
title: ポートフォリオサイト仕様書
uid: 62f24516-31ce-4a3c-b725-b5c0896f187d
---

# ポートフォリオサイト仕様書

[ポートフォリオサイト](https://itsukikanai.github.io)

**[EN English (README.md)](./README.md)** | **JA 日本語 (このファイル)**

本書は、`itsukikanai.github.io` ポートフォリオサイトの技術仕様、ディレクトリ構造、および設計ガイドラインを概説するものです。

## <a id="0-目次"></a>0. 目次

- [0. 目次](#0-目次)
- [1. ディレクトリ構造](#1-ディレクトリ構造)
  - [1.1. ルール](#11-ルール)
- [2. 技術スタック](#2-技術スタック)
  - [2.1. コア](#21-コア)
  - [2.2. デザインシステム](#22-デザインシステム)
- [3. デプロイメント](#3-デプロイメント)
- [4. プロジェクト概要](#4-プロジェクト概要)
  - [4.1. AI Video Tool](#41-ai-video-tool)
  - [4.2. StealthText](#42-stealthtext)
  - [4.3. HTML Converter](#43-html-converter)
  - [4.4. URI Redirector](#44-uri-redirector)
  - [4.5. Private Projects](#45-private-projects)
  - [4.6. Sandbox](#46-sandbox)
- [5. その他](#5-その他)
  - [5.1. 免責事項](#51-免責事項)

## <a id="1-ディレクトリ構造"></a>1. ディレクトリ構造

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

### <a id="11-ルール"></a>1.1. ルール

- **厳格なルーティング**: ページレンダリングには `index.html` のみを使用してください。
  - 例: `about.html` は禁止です。`about/index.html` とする必要があります。
  - これは、全てのサブディレクトリ（例: `projects/stealthtext/history/index.html`）に適用されます。
- **ルート順序**: `index.html` > リソース (`css/`, `js/`, `img/`) > 設定ファイル。
- **セクショニング**: 独立したセクション（例: `projects/`）は、独自の `index.html` を含むディレクトリを持つ必要があります。
- **アセット**: 画像以外のバイナリ資産は、タイプ別に分類して `assets/` に配置します。

## <a id="2-技術スタック"></a>2. 技術スタック

### <a id="21-コア"></a>2.1. コア

- **HTML5**: セマンティックマークアップ。
- **TailwindCSS**: 全スタイリングに使用 (CDN via JavaScript)。
  - *設定*: カスタムカラーパレット（ダークモード重視）、フォント（Inter/Outfit）。
- **JavaScript (Vanilla)**:
  - `main.js`: グローバルロジック（テーマ、言語管理）。
  - `layout.js`: ヘッダー/フッターの動的レンダリング (`LayoutManager`)。

### <a id="22-デザインシステム"></a>2.2. デザインシステム

- **テーマ**: プレミアムダークモード。
  - 背景色: 深いスレート/ブラック (`#0a0a0a`, `#0f172a`)。
  - アクセント: 鮮やかなインディゴ、シアン、パープルのグラデーション。
- **タイポグラフィ**: `Outfit` (見出し) および `Inter` (本文)。
- **ビジュアル**: グラスモーフィズム（背景ぼかし）、スムーズなグラデーション、マイクロインタラクション。

## <a id="3-デプロイメント"></a>3. デプロイメント

- **プラットフォーム**: GitHub Pages。
- **URL構造**: `username.github.io/path/to/resource`。
- **セキュリティ**: 機密データ（`.env`、大規模データセット等）は `.gitignore` により除外されます。

## <a id="4-プロジェクト概要"></a>4. プロジェクト概要

[プロジェクト](https://itsukikanai.github.io/projects)

### <a id="41-ai-video-tool"></a>4.1. AI Video Tool

[AI Video Tool プロジェクト](https://itsukikanai.github.io/projects/ai-video-tool)

*場所: `/projects/ai-video-tool/`*
AI動画管理ツールのための専用ランディングページ。

- **主な機能**: スマートダウンロード (yt-dlp)、AI分析 (Google Gemini)、FTS5全文検索、FFmpegによる自動編集。
- **技術**: Python, Gradio, SQLite, Google GenAI。

### <a id="42-stealthtext"></a>4.2. StealthText

[StealthText プロジェクト](https://itsukikanai.github.io/projects/stealthtext)

*場所: `/projects/stealthtext/`*
不可視テキストを埋め込むクライアントサイド・ステガノグラフィツール。

- **主な機能**: ゼロ幅文字埋め込み、AES暗号化、整合性検証 (HMAC)、選択安全な埋め込み戦略。
- **技術**: JavaScript, Crypto.js, TailwindCSS。

### <a id="43-html-converter"></a>4.3. HTML Converter

[HTML Converter プロジェクト](https://itsukikanai.github.io/projects/html-converter)

*場所: `/projects/html-converter/`*
単一HTMLをCSS/JSに分割、または統合するユーティリティ。ZIP出力/PWA対応。

- **主な機能**: Live Preview, ZIP Download, PWA Installation Support, File Import/Export.
- **技術**: JSZip, File API, TailwindCSS.

### <a id="44-uri-redirector"></a>4.4. URI Redirector

[URI Redirector プロジェクト](https://itsukikanai.github.io/go)

*場所: `/go/`*
Obsidian, Notion, iA Writerなどのアプリ内リンクを外部ウェブリンクに変換・リダイレクトするツール。

- **主な機能**: URLスキームへのリダイレクト、Web用リンクの生成、アプリごとのテーマ適応。
- **技術**: Vanilla JS, CSS Variables.

### 4.5. Private Projects (非公開)

[Private Projects ディレクトリ](https://itsukikanai.github.io/projects/private)

*場所: `/projects/private/`*
未公開または開発中のプロジェクトのためのプレースホルダー。

### <a id="46-sandbox"></a>4.6. Sandbox

[Sandbox ディレクトリ](https://itsukikanai.github.io/projects/sandbox)

*場所: `/projects/sandbox/`*
ベータ版、未翻訳版などを仮で公開するためのディレクトリです。

## <a id="5-その他"></a>5. その他

### <a id="51-免責事項"></a>5.1. 免責事項

[免責事項](https://itsukikanai.github.io/disclaimer)

---

&copy; 2026- Itsuki Kanai. All rights reserved.
