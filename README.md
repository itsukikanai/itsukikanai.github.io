---
aliases: []
created: 2025-02-23 01:11:08
i18n:
  ja: "[[./README_ja.md]]"
modified: 2026-04-14 17:14:42
tags: []
title: Portfolio Website Specification
uid: 81fa8613-7cdd-48ea-9823-02f9322c80d0
---

# Portfolio Website Specification

[Portfolio Website](https://itsukikanai.github.io)

**EN English (This file)** | **[JA 日本語 (README_ja.md)](./README_ja.md)**

This document outlines the technical specifications, directory structure, and design guidelines for the `itsukikanai.github.io` portfolio website.

## <a id="0-table-of-contents"></a>0. Table of Contents

- [0. Table of Contents](#0-table-of-contents)
- [1. Directory Structure](#1-directory-structure)
  - [1.1. Rules](#11-rules)
- [2. Technology Stack](#2-technology-stack)
  - [2.1. Core](#21-core)
  - [2.2. Design System](#22-design-system)
- [3. Deployment](#3-deployment)
- [4. Content Management](#4-content-management)
- [5. Projects Overview](#5-projects-overview)
  - [5.1. AI Video Tool](#51-ai-video-tool)
  - [5.2. StealthText](#52-stealthtext)
  - [5.3. HTML Converter](#53-html-converter)
  - [5.4. URI Redirector](#54-uri-redirector)
  - [5.5. Private Projects](#55-private-projects)
  - [5.6. Sandbox](#56-sandbox)
- [6. Other](#6-other)
  - [6.1. Disclaimer](#61-disclaimer)

## <a id="1-directory-structure"></a>1. Directory Structure

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
├── notes/                # Digital Garden (Obsidian vault)
│   ├── README.md         # Notes specification (English)
│   ├── README_ja.md      # Notes specification (Japanese)
│   └── private/          # Private notes (Git ignored)
└── [config files]        # (favicon.ico, .gitignore, etc.)
```

### <a id="11-rules"></a>1.1. Rules

- **Strict Routing**: Only `index.html` files are permitted for page rendering.
  - Example: `about.html` is prohibited. Must be `about/index.html`.
  - This applies to all subdirectories (e.g., `projects/stealthtext/history/index.html`).
- **Root Order**: `index.html` > Resources (`css/`, `js/`, `img/`) > Config files.
- **Sectioning**: Distinct sections (e.g., `projects/`) must have their own directory containing an `index.html`.
- **Assets**: All non-image binary assets reside in `assets/`, categorized by type.
- **Images**: All display images reside in `img/`. Editing sources reside in `img/raw/`.

## <a id="2-technology-stack"></a>2. Technology Stack

### <a id="21-core"></a>2.1. Core

- **HTML5**: Semantic markup.
- **TailwindCSS**: Used for all styling (CDN).
  - *Configuration*: Custom color palette (Dark Mode focus), Fonts (Inter/Outfit).
- **JavaScript (Vanilla)**: For lightweight interactions and DOM manipulation.
  - `main.js`: Global logic (Theme, Language).
  - `layout.js`: Dynamic Header/Footer rendering (`LayoutManager`).

### <a id="22-design-system"></a>2.2. Design System

- **Theme**: Premium Dark Mode.
  - Background: Deep Slate/Black (`#0a0a0a`, `#0f172a`).
  - Accents: Vibrant Indigo, Cyan, Purple gradients.
- **Typography**: `Outfit` (Headings) and `Inter` (Body).
- **Visuals**: Glassmorphism (Backdrop Blur), Smooth Gradients, Micro-interactions.

## <a id="3-deployment"></a>3. Deployment

- **Platform**: GitHub Pages.
- **URL Structure**: `username.github.io/path/to/resource`.
- **Security**: Sensitive data (e.g., `.env`, large datasets) is excluded via `.gitignore`.

## <a id="4-content-management"></a>4. Content Management

- **Markdown Mirroring**: For every HTML page, a corresponding Markdown (`.md`) file exists for documentation and accessibility purposes.

---

## <a id="5-projects-overview"></a>5. Projects Overview

[Projects](https://itsukikanai.github.io/projects)

### <a id="51-ai-video-tool"></a>5.1. AI Video Tool

[AI Video Tool Project](https://itsukikanai.github.io/projects/ai-video-tool)

*Location: `/projects/ai-video-tool/`*
A specialized landing page for the AI Video management tool.

- **Key Features**: Smart Download (yt-dlp), AI Analysis (Google Gemini), FTS5 Search, Auto-Editing via FFmpeg.
- **Tech**: Python, Gradio, SQLite, Google GenAI.

### <a id="52-stealthtext"></a>5.2. StealthText

[StealthText Project](https://itsukikanai.github.io/projects/stealthtext)

*Location: `/projects/stealthtext/`*
A client-side steganography tool for embedding invisible text.

- **Key Features**: Zero-width character embedding, AES Encryption, Integrity Check (HMAC), Selection-safe strategies.
- **Tech**: JavaScript, Crypto.js, TailwindCSS.

### <a id="53-html-converter"></a>5.3. HTML Converter

[HTML Converter Project](https://itsukikanai.github.io/projects/html-converter)

*Location: `/projects/html-converter/`*
A utility to split single-file HTML (containing inline CSS/JS) into specialized structure (`index.html`, `css/style.css`, `js/main.js`) and vice-versa.

- **Key Features**: Live Preview, ZIP Download, PWA Installation Support, File Import/Export.
- **Tech**: JSZip, File API, TailwindCSS.

### <a id="54-uri-redirector"></a>5.4. URI Redirector

[URI Redirector Project](https://itsukikanai.github.io/go)

*Location: `/go/`*
A utility to convert and redirect in-app URIs (Obsidian, Notion, iA Writer) to shareable web links.

- **Key Features**: URI Scheme Redirection, Web Link Generation, App-specific Theming.
- **Tech**: Vanilla JS, CSS Variables.

### <a id="55-private-projects"></a>5.5. Private Projects

[Private Projects Directory](https://itsukikanai.github.io/projects/private)

*Location: `/projects/private/`*
Placeholder for unreleased or private developments.

### <a id="56-sandbox"></a>5.6. Sandbox

[Sandbox Directory](https://itsukikanai.github.io/projects/sandbox)

*Location: `/projects/sandbox/`*
Directory for hosting beta versions, untranslated builds, and experimental projects temporarily.

## <a id="6-other"></a>6. Other

### <a id="61-disclaimer"></a>6.1. Disclaimer

[Disclaimer](https://itsukikanai.github.io/disclaimer)

---

&copy; 2026- Itsuki Kanai. All rights reserved.
