---
aliases: []
created: 2025-02-23 01:11:08
i18n:
  ja: "[[README_ja]]"
modified: 2026-04-14 17:14:42
tags: []
title: Portfolio Website Specification
uid: 81fa8613-7cdd-48ea-9823-02f9322c80d0
---

# Portfolio Website Specification

[Portfolio Website](https://itsukikanai.github.io)

**EN English (This file)** | **[JA 日本語 (README_ja.md)](./README_ja.md)**

This document outlines the technical specifications, directory structure, and design guidelines for the `itsukikanai.github.io` portfolio website.

## 0. Table of Contents ^chapter-0

- [[README#^chapter-0|0. Table of Contents]]
- [[README#^chapter-1|1. Directory Structure]]
  - [[README#^chapter-1-1|1.1. Rules]]
- [[README#^chapter-2|2. Technology Stack]]
  - [[README#^chapter-2-1|2.1. Core]]
  - [[README#^chapter-2-2|2.2. Design System]]
- [[README#^chapter-3|3. Deployment]]
- [[README#^chapter-4|4. Content Management]]
- [[README#^chapter-5|5. Projects Overview]]
  - [[README#^chapter-5-1|5.1. AI Video Tool]]
  - [[README#^chapter-5-2|5.2. StealthText]]
  - [[README#^chapter-5-3|5.3. HTML Converter]]
  - [[README#^chapter-5-4|5.4. URI Redirector]]
  - [[README#^chapter-5-5|5.5. Private Projects]]
  - [[README#^chapter-5-6|5.6. Sandbox]]
- [[README#^chapter-6|6. Other]]
  - [[README#^chapter-6-1|6.1. Disclaimer]]

## 1. Directory Structure ^chapter-1

The project follows a strict directory hierarchy to ensure maintainability and scalability.

```text
root/
├── README.md             # Project documentation (English)
├── README_ja.md          # Project documentation (Japanese)
├── index.html            # Main Entry Point
├── css/                  # Global Stylesheets (Vanilla CSS + Tailwind Customizations)
│   ├── reset.css
│   └── style.css
├── js/                   # Logical scripts (LayoutManager, etc.)
│   └── main.js
├── img/                  # All image assets
│   ├── raw/              # Source files (PSD, TIF, etc. - not deployed)
│   └── [image files]     # Optimization formats (WebP, SVG, JPG)
├── assets/               # Static resources
│   ├── text/
│   ├── fonts/
│   ├── docs/
│   ├── audio/
│   ├── video/
│   ├── model/
│   └── archive/
├── projects/             # Portfolio Projects Section
│   ├── index.html        # Projects Overview List
│   ├── private/          # Private/Restricted Projects
│   ├── ai-video-tool/    # AI Video Tool Landing Page
│   ├── stealthtext/      # StealthText Tool & History
│   └── sandbox/          # Beta/Untranslated versions
└── [config files]        # (favicon.ico, .gitignore, etc.)
```

### 1.1. Rules ^chapter-1-1

- **Strict Routing**: Only `index.html` files are permitted for page rendering.
  - Example: `about.html` is prohibited. Must be `about/index.html`.
  - This applies to all subdirectories (e.g., `projects/stealthtext/history/index.html`).
- **Root Order**: `index.html` > Resources (`css/`, `js/`, `img/`) > Config files.
- **Sectioning**: Distinct sections (e.g., `projects/`) must have their own directory containing an `index.html`.
- **Assets**: All non-image binary assets reside in `assets/`, categorized by type.
- **Images**: All display images reside in `img/`. Editing sources reside in `img/raw/`.

## 2. Technology Stack ^chapter-2

### 2.1. Core ^chapter-2-1

- **HTML5**: Semantic markup.
- **TailwindCSS**: Used for all styling (CDN).
  - *Configuration*: Custom color palette (Dark Mode focus), Fonts (Inter/Outfit).
- **JavaScript (Vanilla)**: For lightweight interactions and DOM manipulation.
  - `main.js`: Global logic (Theme, Language).
  - `layout.js`: Dynamic Header/Footer rendering (`LayoutManager`).

### 2.2. Design System ^chapter-2-2

- **Theme**: Premium Dark Mode.
  - Background: Deep Slate/Black (`#0a0a0a`, `#0f172a`).
  - Accents: Vibrant Indigo, Cyan, Purple gradients.
- **Typography**: `Outfit` (Headings) and `Inter` (Body).
- **Visuals**: Glassmorphism (Backdrop Blur), Smooth Gradients, Micro-interactions.

## 3. Deployment ^chapter-3

- **Platform**: GitHub Pages.
- **URL Structure**: `username.github.io/path/to/resource`.
- **Security**: Sensitive data (e.g., `.env`, large datasets) is excluded via `.gitignore`.

## 4. Content Management ^chapter-4

- **Markdown Mirroring**: For every HTML page, a corresponding Markdown (`.md`) file exists for documentation and accessibility purposes.

---

## 5. Projects Overview ^chapter-5

[Projects](https://itsukikanai.github.io/projects)

### 5.1. AI Video Tool ^chapter-5-1

[AI Video Tool Project](https://itsukikanai.github.io/projects/ai-video-tool)

*Location: `/projects/ai-video-tool/`*
A specialized landing page for the AI Video management tool.

- **Key Features**: Smart Download (yt-dlp), AI Analysis (Google Gemini), FTS5 Search, Auto-Editing via FFmpeg.
- **Tech**: Python, Gradio, SQLite, Google GenAI.

### 5.2. StealthText ^chapter-5-2

[StealthText Project](https://itsukikanai.github.io/projects/stealthtext)

*Location: `/projects/stealthtext/`*
A client-side steganography tool for embedding invisible text.

- **Key Features**: Zero-width character embedding, AES Encryption, Integrity Check (HMAC), Selection-safe strategies.
- **Tech**: JavaScript, Crypto.js, TailwindCSS.

### 5.3. HTML Converter ^chapter-5-3

[HTML Converter Project](https://itsukikanai.github.io/projects/html-converter)

*Location: `/projects/html-converter/`*
A utility to split single-file HTML (containing inline CSS/JS) into specialized structure (`index.html`, `css/style.css`, `js/main.js`) and vice-versa.

- **Key Features**: Live Preview, ZIP Download, PWA Installation Support, File Import/Export.
- **Tech**: JSZip, File API, TailwindCSS.

### 5.4. URI Redirector ^chapter-5-4

[URI Redirector Project](https://itsukikanai.github.io/go)

*Location: `/go/index.html`*
A utility to convert and redirect in-app URIs (Obsidian, Notion, iA Writer) to shareable web links.

- **Key Features**: URI Scheme Redirection, Web Link Generation, App-specific Theming.
- **Tech**: Vanilla JS, CSS Variables.

### 5.5. Private Projects ^chapter-5-5

[Private Projects Directory](https://itsukikanai.github.io/projects/private)

*Location: `/projects/private/`*
Placeholder for unreleased or private developments.

### 5.6. Sandbox ^chapter-5-6

[Sandbox Directory](https://itsukikanai.github.io/projects/sandbox)

*Location: `/projects/sandbox/`*
Directory for hosting beta versions, untranslated builds, and experimental projects temporarily.

## 6. Other ^chapter-6

### 6.1. Disclaimer ^chapter-6-1

[Disclaimer](https://itsukikanai.github.io/disclaimer)

---

&copy; 2026- Itsuki Kanai. All rights reserved.
