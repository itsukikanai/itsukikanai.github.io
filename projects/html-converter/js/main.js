document.addEventListener('DOMContentLoaded', () => {
    // === UI Elements ===
    const tabs = document.querySelectorAll('.tab-btn');
    const statusEl = document.getElementById('status');

    // === Localization Dictionary ===
    const I18N = {
        ja: {
            previewEmpty: 'プレビューする内容がありません',
            previewUpdated: 'プレビューを更新しました',
            zipDownloadStarted: 'ZIPダウンロードを開始しました',
            zipCreationFailed: 'ZIP作成に失敗しました',
            jsZipMissing: 'JSZip ライブラリがロードされていません',
            fileLoaded: 'ファイルを読み込みました',
            convertFirst: '先に変換を実行してください',
            enterHtml: 'HTMLを入力してください', // htmlRequired
            conversionComplete: '変換完了！',
            conversionError: '変換エラー: HTML構文を確認してください',
            downloadStarted: 'ダウンロードを開始しました'
        },
        en: {
            previewEmpty: 'Nothing to preview',
            previewUpdated: 'Preview updated',
            zipDownloadStarted: 'ZIP download started',
            zipCreationFailed: 'Failed to create ZIP',
            jsZipMissing: 'JSZip library not loaded',
            fileLoaded: 'File loaded',
            convertFirst: 'Please convert first',
            enterHtml: 'Please enter HTML',
            conversionComplete: 'Conversion Complete!',
            conversionError: 'Conversion Error: Check HTML syntax',
            downloadStarted: 'Download started'
        }
    };

    // Helper: Safe Text Retrieval
    function getLangText(key) {
        const lang = (window.LangManager && window.LangManager.current) || 'ja';
        return (I18N[lang] && I18N[lang][key]) || I18N['ja'][key];
    }

    // Helper: Download File
    function downloadFile(filename, content) {
        if (!content) return;
        const blob = new Blob([content], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        showStatus(getLangText('downloadStarted'));
    }

    // === Tabs Logic ===
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            tabs.forEach(t => {
                t.classList.remove('text-primary', 'border-primary', 'bg-primary/5');
                t.classList.add('text-slate-500', 'border-transparent');
                document.getElementById(t.dataset.tab).classList.add('hidden');
            });
            btn.classList.remove('text-slate-500', 'border-transparent');
            btn.classList.add('text-primary', 'border-primary', 'bg-primary/5');
            document.getElementById(btn.dataset.tab).classList.remove('hidden');
            showStatus('');
        });
    });

    // === Helpers ===
    function showStatus(msg, type = 'success') {
        if (!msg) {
            statusEl.textContent = '';
            statusEl.className = 'status text-center mt-4 h-6 text-sm';
            return;
        }
        statusEl.textContent = msg;
        statusEl.className = `status text-center mt-4 h-6 text-sm font-bold ${type === 'error' ? 'text-red-500' : 'text-green-500'}`;
        setTimeout(() => {
            if (statusEl.textContent === msg) statusEl.textContent = '';
        }, 3000);
    }

    async function copyToClipboard(text) {
        if (!text) return;
        try {
            await navigator.clipboard.writeText(text);
            showStatus('コピーしました', 'success');
        } catch (err) {
            console.error('Copy failed', err);
            showStatus('コピーに失敗しました', 'error');
        }
    }

    // === Button Listeners ===
    // Copy Buttons
    document.querySelectorAll('.btn-copy').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const textarea = document.getElementById(targetId);
            if (textarea) {
                copyToClipboard(textarea.value);
            }
        });
    });

    // Individual Download Buttons (Safe check as elements might not exist yet)
    const btnDownloadHtml = document.getElementById('btnDownloadHtml');
    if (btnDownloadHtml) {
        btnDownloadHtml.addEventListener('click', () => {
            downloadFile('index.html', document.getElementById('outIndexHtml').value);
        });
    }
    const btnDownloadCss = document.getElementById('btnDownloadCss');
    if (btnDownloadCss) {
        btnDownloadCss.addEventListener('click', () => {
            downloadFile('style.css', document.getElementById('outCss').value);
        });
    }
    const btnDownloadJs = document.getElementById('btnDownloadJs');
    if (btnDownloadJs) {
        btnDownloadJs.addEventListener('click', () => {
            downloadFile('main.js', document.getElementById('outJs').value);
        });
    }
    const btnDownloadSingle = document.getElementById('btnDownloadSingle');
    if (btnDownloadSingle) {
        btnDownloadSingle.addEventListener('click', () => {
            downloadFile('index.html', document.getElementById('outSingleHtml').value);
        });
    }

    // Clear Buttons
    document.getElementById('btnClearOne').addEventListener('click', () => {
        document.getElementById('singleInput').value = '';
        ['outIndexHtml', 'outCss', 'outJs'].forEach(id => document.getElementById(id).value = '');
        showStatus('クリアしました');
    });

    document.getElementById('btnClearSplit').addEventListener('click', () => {
        ['inIndexHtml', 'inCss', 'inJs'].forEach(id => document.getElementById(id).value = '');
        document.getElementById('outSingleHtml').value = '';
        showStatus('クリアしました');
    });

    // === Logic: One -> Split ===
    document.getElementById('btnConvertToSplit').addEventListener('click', () => {
        try {
            const raw = document.getElementById('singleInput').value;
            if (!raw.trim()) {
                showStatus(getLangText('enterHtml'), 'error');
                return;
            }

            // Get Custom Paths (Fallback to default)
            const cssPathInput = document.getElementById('inputCssPath');
            const jsPathInput = document.getElementById('inputJsPath');
            const cssPath = (cssPathInput && cssPathInput.value.trim()) ? cssPathInput.value.trim() : './css/style.css';
            const jsPath = (jsPathInput && jsPathInput.value.trim()) ? jsPathInput.value.trim() : './js/main.js';

            const parser = new DOMParser();
            const doc = parser.parseFromString(raw, "text/html");

            // 1. Extract CSS
            const styleNodes = Array.from(doc.querySelectorAll("style"));
            const css = styleNodes.map(n => `/* Extracted from <style> */\n${n.textContent.trim()}`).join("\n\n");
            styleNodes.forEach(n => n.remove());

            // 2. Extract JS (inline only)
            const scriptNodes = Array.from(doc.querySelectorAll("script:not([src])"));
            const js = scriptNodes.map(n => `// Extracted from <script>\n${n.textContent.trim()}`).join("\n\n");
            scriptNodes.forEach(n => n.remove());

            // 3. Inject Links to external files if not present
            // Ensure head and body exist
            if (!doc.head) doc.documentElement.insertBefore(doc.createElement("head"), doc.body);
            if (!doc.body) doc.documentElement.appendChild(doc.createElement("body"));

            // Check if link already exists (simple check)
            const hasCssLink = Array.from(doc.querySelectorAll('link[rel="stylesheet"]'))
                .some(l => (l.getAttribute('href') || '').includes(cssPath));

            if (!hasCssLink && css) {
                const link = doc.createElement("link");
                link.rel = "stylesheet";
                link.href = cssPath;
                doc.head.appendChild(link);
            }

            const hasJsScript = Array.from(doc.querySelectorAll('script[src]'))
                .some(s => (s.getAttribute('src') || '').includes(jsPath));

            if (!hasJsScript && js) {
                const s = doc.createElement("script");
                s.src = jsPath;
                doc.body.appendChild(s);
            }

            // 4. Output
            const outHtml = `<!DOCTYPE html>\n${doc.documentElement.outerHTML}`;

            document.getElementById('outIndexHtml').value = outHtml;
            document.getElementById('outCss').value = css || "/* No inline styles found */";
            document.getElementById('outJs').value = js || "// No inline scripts found";

            showStatus(getLangText('conversionComplete'));

        } catch (e) {
            console.error(e);
            showStatus(getLangText('conversionError'), 'error');
        }
    });


    // === Logic: ZIP Download ===
    document.getElementById('btnDownloadZip').addEventListener('click', async () => {
        const html = document.getElementById('outIndexHtml').value;
        const css = document.getElementById('outCss').value;
        const js = document.getElementById('outJs').value;

        if (!html) {
            showStatus(getLangText('convertFirst'), 'error');
            return;
        }

        try {
            if (typeof JSZip === 'undefined') {
                showStatus(getLangText('jsZipMissing'), 'error');
                return;
            }

            const zip = new JSZip();
            zip.file("index.html", html);
            zip.folder("css").file("style.css", css);
            zip.folder("js").file("main.js", js);

            const content = await zip.generateAsync({ type: "blob" });

            const a = document.createElement("a");
            a.href = URL.createObjectURL(content);
            a.download = "split-project.zip";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            showStatus(getLangText('zipDownloadStarted'));
        } catch (e) {
            console.error(e);
            showStatus(getLangText('zipCreationFailed'), 'error');
        }
    });


    // === Logic: File Import (Single) ===
    document.getElementById('fileImportSingle').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (ev) => {
            document.getElementById('singleInput').value = ev.target.result;
            showStatus(getLangText('fileLoaded'));
        };
        reader.readAsText(file);
    });


    // === Logic: Split -> One ===
    document.getElementById('btnConvertToOne').addEventListener('click', () => {
        try {
            const htmlRaw = document.getElementById('inIndexHtml').value;
            const cssRaw = document.getElementById('inCss').value;
            const jsRaw = document.getElementById('inJs').value;

            if (!htmlRaw.trim()) {
                showStatus(getLangText('enterHtml'), 'error');
                return;
            }

            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlRaw, "text/html");

            // 1. Remove specific external links
            Array.from(doc.querySelectorAll('link[rel="stylesheet"]')).forEach(l => {
                const href = l.getAttribute('href') || '';
                if (href.includes('style.css')) l.remove();
            });

            Array.from(doc.querySelectorAll('script[src]')).forEach(s => {
                const src = s.getAttribute('src') || '';
                if (src.includes('main.js')) s.remove();
            });

            // 2. Inject CSS
            if (cssRaw.trim()) {
                const style = doc.createElement('style');
                style.textContent = `\n${cssRaw.trim()}\n`;
                if (doc.head) doc.head.appendChild(style);
            }

            // 3. Inject JS
            if (jsRaw.trim()) {
                const script = doc.createElement('script');
                script.textContent = `\n${jsRaw.trim()}\n`;
                if (doc.body) doc.body.appendChild(script);
            }

            const outHtml = `<!DOCTYPE html>\n${doc.documentElement.outerHTML}`;
            document.getElementById('outSingleHtml').value = outHtml;

            showStatus(getLangText('conversionComplete'));

        } catch (e) {
            console.error(e);
            showStatus(getLangText('conversionError'), 'error');
        }
    });

    // === Logic: Preview (Split) ===
    document.getElementById('btnPreviewSplit').addEventListener('click', () => {
        const html = document.getElementById('outIndexHtml').value;
        const css = document.getElementById('outCss').value;
        const js = document.getElementById('outJs').value;

        if (!html.trim()) {
            showStatus(getLangText('previewEmpty'), 'error');
            return;
        }

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Inject CSS
        if (css.trim()) {
            const style = doc.createElement('style');
            style.textContent = css;
            if (doc.head) doc.head.appendChild(style);
        }

        // Inject JS
        if (js.trim()) {
            const script = doc.createElement('script');
            script.textContent = js;
            if (doc.body) doc.body.appendChild(script);
        }

        const previewFrame = document.getElementById('previewFrameSplit');
        previewFrame.srcdoc = `<!DOCTYPE html>\n${doc.documentElement.outerHTML}`;

        showStatus(getLangText('previewUpdated'));
    });

    // === Logic: Preview (Merge) ===
    document.getElementById('btnPreviewMerge').addEventListener('click', () => {
        const html = document.getElementById('outSingleHtml').value;

        if (!html.trim()) {
            showStatus(getLangText('previewEmpty'), 'error');
            return;
        }

        const previewFrame = document.getElementById('previewFrameMerge');
        previewFrame.srcdoc = html;

        showStatus(getLangText('previewUpdated'));
    });

});
