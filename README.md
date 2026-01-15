# Portfolio Website Specification

[Portfolio Website](https://itsukikanai.github.io/index.html)


**EN English (This file)** | **[JA 日本語 (README_ja.md)](./README_ja.md)**

This document outlines the technical specifications, directory structure, and design guidelines for the `itsukikanai.github.io` portfolio website.

## 1. Directory Structure

The project follows a strict directory hierarchy to ensure maintainability and scalability.

```
site-root/
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

### Rules
- **Strict Routing**: Only `index.html` files are permitted for page rendering.
    - Example: `about.html` is prohibited. Must be `about/index.html`.
    - This applies to all subdirectories (e.g., `projects/stealthtext/history/index.html`).
- **Root Order**: `index.html` > Resources (`css/`, `js/`, `img/`) > Config files.
- **Sectioning**: Distinct sections (e.g., `projects/`) must have their own directory containing an `index.html`.
- **Assets**: All non-image binary assets reside in `assets/`, categorized by type.
- **Images**: All display images reside in `img/`. Editing sources reside in `img/raw/`.

## 2. Technology Stack

### Core
- **HTML5**: Semantic markup.
- **TailwindCSS**: Used for all styling (CDN).
    - *Configuration*: Custom color palette (Dark Mode focus), Fonts (Inter/Outfit).
- **JavaScript (Vanilla)**: For lightweight interactions and DOM manipulation.
    - `main.js`: Global logic (Theme, Language).
    - `layout.js`: Dynamic Header/Footer rendering (`LayoutManager`).

### Design System
- **Theme**: Premium Dark Mode.
    - Background: Deep Slate/Black (`#0a0a0a`, `#0f172a`).
    - Accents: Vibrant Indigo, Cyan, Purple gradients.
- **Typography**: `Outfit` (Headings) and `Inter` (Body).
- **Visuals**: Glassmorphism (Backdrop Blur), Smooth Gradients, Micro-interactions.

## 3. Deployment
- **Platform**: GitHub Pages.
- **URL Structure**: `username.github.io/path/to/resource`.
- **Security**: Sensitive data (e.g., `.env`, large datasets) is excluded via `.gitignore`.

## 4. Content Management
- **Markdown Mirroring**: For every HTML page, a corresponding Markdown (`.md`) file exists for documentation and accessibility purposes.

---

## Projects Overview
[Projects](https://itsukikanai.github.io/projects/index.html)

### 1. AI Video Tool
[Link](https://itsukikanai.github.io/projects/ai-video-tool/index.html)

*Location: `/projects/ai-video-tool/`*
A specialized landing page for the AI Video management tool.
- **Key Features**: Smart Download (yt-dlp), AI Analysis (Google Gemini), FTS5 Search, Auto-Editing via FFmpeg.
- **Tech**: Python, Gradio, SQLite, Google GenAI.

### 2. StealthText
[Link](https://itsukikanai.github.io/projects/stealthtext/index.html)

*Location: `/projects/stealthtext/`*
A client-side steganography tool for embedding invisible text.
- **Key Features**: Zero-width character embedding, AES Encryption, Integrity Check (HMAC), Selection-safe strategies.
- **Tech**: JavaScript, Crypto.js, TailwindCSS.

### 3. HTML Converter
[Link](https://itsukikanai.github.io/projects/html-converter/index.html)

*Location: `/projects/html-converter/`*
A utility to split single-file HTML (containing inline CSS/JS) into specialized structure (`index.html`, `css/style.css`, `js/main.js`) and vice-versa.
- **Key Features**: Live Preview, ZIP Download, PWA Installation Support, File Import/Export.
- **Tech**: JSZip, File API, TailwindCSS.

### 4. Private Projects
[Link](https://itsukikanai.github.io/projects/private/index.html)

*Location: `/projects/private/`*
Placeholder for unreleased or private developments.

### 5. Sandbox
[Link](https://itsukikanai.github.io/projects/sandbox/index.html)

*Location: `/projects/sandbox/`*
Directory for hosting beta versions, untranslated builds, and experimental projects temporarily.

---

[Disclaimer](https://itsukikanai.github.io/disclaimer/index.html)

&copy; 2026- Itsuki Kanai. All rights reserved.