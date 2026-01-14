/**
 * Security Patch: Safer Zero Width Characters
 */
const ZW_CHARS = {
    '00': '\u200B', // Zero Width Space
    '01': '\u200C', // Zero Width Non-Joiner
    '10': '\u200D', // Zero Width Joiner
    '11': '\u2060'  // Word Joiner
};
const REVERSE_ZW_CHARS = Object.fromEntries(Object.entries(ZW_CHARS).map(([k, v]) => [v, k]));
const ZW_REGEX_GLOBAL = new RegExp(`[${Object.values(ZW_CHARS).join('')}]`, 'g');

/**
 * Security Patch: Modern Binary Handling
 */
class BinaryUtils {
    static stringToBinary(str) {
        const bytes = new TextEncoder().encode(str);
        let binary = '';
        for (let byte of bytes) {
            binary += byte.toString(2).padStart(8, '0');
        }
        return binary;
    }

    static binaryToString(binary) {
        const bytes = new Uint8Array(Math.ceil(binary.length / 8));
        for (let i = 0; i < bytes.length; i++) {
            bytes[i] = parseInt(binary.substr(i * 8, 8), 2);
        }
        return new TextDecoder().decode(bytes);
    }
}

/**
 * Security Patch: Integrity Check & Encryption Wrapper
 */
class CipherManager {
    static generateSignature(text, password) {
        if (password) {
            return CryptoJS.HmacSHA256(text, password).toString();
        } else {
            return CryptoJS.SHA256(text).toString();
        }
    }

    static encrypt(text, password) {
        const signature = this.generateSignature(text, password);
        const payloadObj = {
            d: text,
            s: signature,
            t: Date.now()
        };
        const payloadStr = JSON.stringify(payloadObj);

        if (password) {
            return CryptoJS.AES.encrypt(payloadStr, password).toString();
        }

        const words = CryptoJS.enc.Utf8.parse(payloadStr);
        return CryptoJS.enc.Base64.stringify(words);
    }

    static decrypt(ciphertext, password) {
        let decryptedStr = "";

        if (password) {
            try {
                const bytes = CryptoJS.AES.decrypt(ciphertext, password);
                decryptedStr = bytes.toString(CryptoJS.enc.Utf8);
            } catch (e) {
                throw new Error(LangManager.current === 'ja' ? "復号に失敗しました。パスワードが間違っています。" : "Decryption failed. Incorrect password.");
            }
        } else {
            try {
                const words = CryptoJS.enc.Base64.parse(ciphertext);
                decryptedStr = words.toString(CryptoJS.enc.Utf8);
            } catch (e) {
                decryptedStr = ciphertext;
            }
        }

        if (!decryptedStr) throw new Error(LangManager.current === 'ja' ? "データの復元に失敗しました（パスワード誤り、または破損）。" : "Failed to restore data (Incorrect password or corrupted).");

        let payload;
        try {
            payload = JSON.parse(decryptedStr);
        } catch (e) {
            throw new Error(LangManager.current === 'ja' ? "復号データが破損しています。パスワードが間違っている可能性があります。" : "Decrypted data is corrupted. Password might be incorrect.");
        }

        if (!payload.d || !payload.s) {
            throw new Error(LangManager.current === 'ja' ? "無効なデータ形式です。" : "Invalid data format.");
        }

        const calculatedSig = this.generateSignature(payload.d, password);
        if (calculatedSig !== payload.s) {
            throw new Error(LangManager.current === 'ja' ? "データの整合性エラー: 改ざんされているか、一部が欠落しています。" : "Integrity Error: Data has been tampered with or is incomplete.");
        }

        return payload.d;
    }
}

/**
 * Core Logic: Steganography Engine
 */
class SteganographyEngine {

    static binaryToZeroWidth(binaryString) {
        let hiddenStr = '';
        if (binaryString.length % 2 !== 0) binaryString += '0';
        for (let i = 0; i < binaryString.length; i += 2) {
            hiddenStr += ZW_CHARS[binaryString.substr(i, 2)];
        }
        return hiddenStr;
    }

    static zeroWidthToBinary(zwString) {
        let binary = '';
        for (const char of zwString) {
            if (REVERSE_ZW_CHARS[char]) binary += REVERSE_ZW_CHARS[char];
        }
        return binary;
    }

    static embed(coverText, hiddenMessage, password, strategy = 'punctuation') {
        coverText = coverText.normalize('NFC');
        hiddenMessage = hiddenMessage.normalize('NFC');

        const encryptedPayload = CipherManager.encrypt(hiddenMessage, password);
        const binary = BinaryUtils.stringToBinary(encryptedPayload);
        const hiddenChars = this.binaryToZeroWidth(binary);

        // --- UPDATED STRATEGIES v4 ---

        if (strategy === 'append') {
            if (coverText.length > 0) {
                const lastIndex = coverText.length - 1;
                const charArray = [...coverText];
                if (charArray.length > 0) {
                    const lastChar = charArray.pop();
                    return charArray.join('') + hiddenChars + lastChar;
                }
            }
            return coverText + hiddenChars;
        }
        else if (strategy === 'interleave') {
            const coverArray = [...coverText];
            let result = '';
            let payloadIndex = 0;
            const payloadArray = [...hiddenChars];

            for (const char of coverArray) {
                result += char;
                if (payloadIndex < payloadArray.length) {
                    result += payloadArray[payloadIndex++];
                }
            }
            if (payloadIndex < payloadArray.length) {
                result += payloadArray.slice(payloadIndex).join('');
            }
            return result;
        }
        else if (strategy === 'punctuation') {
            const punctuationRegex = /([。、.,!?])/g;

            let result = '';
            let lastIndex = 0;
            let match;
            const payloadArray = [...hiddenChars];
            let payloadIndex = 0;

            while ((match = punctuationRegex.exec(coverText)) !== null) {
                result += coverText.substring(lastIndex, match.index);

                if (payloadIndex < payloadArray.length) {
                    result += payloadArray[payloadIndex++];
                }

                result += match[0];
                lastIndex = punctuationRegex.lastIndex;
            }

            result += coverText.substring(lastIndex);

            if (payloadIndex < payloadArray.length) {
                const remainingPayload = payloadArray.slice(payloadIndex).join('');
                const charArray = [...result];
                if (charArray.length > 0) {
                    const lastChar = charArray.pop();
                    result = charArray.join('') + remainingPayload + lastChar;
                } else {
                    result += remainingPayload;
                }
            }

            return result;
        }

        return coverText + hiddenChars;
    }

    static decode(stegoText, password) {
        const matches = stegoText.match(ZW_REGEX_GLOBAL);
        if (!matches || matches.length === 0) {
            throw new Error(LangManager.current === 'ja' ? "隠しデータが見つかりませんでした。" : "No hidden data found.");
        }
        const zwString = matches.join('');

        try {
            const binary = this.zeroWidthToBinary(zwString);
            const encryptedPayload = BinaryUtils.binaryToString(binary);
            return CipherManager.decrypt(encryptedPayload, password);
        } catch (e) {
            throw e;
        }
    }

    static remove(stegoText, password) {
        this.decode(stegoText, password);
        return stegoText.replace(ZW_REGEX_GLOBAL, '');
    }
}

/**
 * UI Manager
 */
class UIManager {
    constructor() {
        this.tabs = ['embed', 'decode', 'remove'];
        // Note: Theme initialization is handled by global main.js
        this.initListeners();
    }

    initListeners() {
        const toggle = document.getElementById('password-toggle');
        const inputContainer = document.getElementById('password-input-container');
        const input = document.getElementById('embed-password');

        if (toggle) {
            toggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    inputContainer.classList.remove('hidden');
                    setTimeout(() => input.focus(), 100);
                } else {
                    inputContainer.classList.add('hidden');
                    input.value = '';
                }
            });
            toggle.addEventListener('change', () => this.updateCounters());
        }

        const embedCover = document.getElementById('embed-cover');
        const embedSecret = document.getElementById('embed-secret');

        if (embedCover) embedCover.addEventListener('input', () => this.updateCounters());
        if (embedSecret) embedSecret.addEventListener('input', () => this.updateCounters());

        const strategySelect = document.getElementById('embed-strategy');
        if (strategySelect) {
            strategySelect.addEventListener('change', () => this.updateStrategyVisual());
            this.updateStrategyVisual(); // Initial call
        }
    }

    updateStrategyVisual() {
        const strategy = document.getElementById('embed-strategy').value;
        const container = document.getElementById('strategy-description');

        const descriptions = {
            punctuation: {
                ja: '句読点（、。.,!?）の直前にデータを隠します。自然な文章構造を維持しやすく、最も検出されにくい推奨モードです。',
                en: 'Hides data immediately before punctuation marks (.,!?). Preserves natural sentence structure. Recommended for stealth.',
                visual: `<div class="font-mono text-center mb-2"><span class="text-slate-400">Natural Text</span><span class="text-primary font-bold">[Hidden]</span><span class="text-slate-900 dark:text-white">.</span> <span class="text-slate-400">Next Sentence</span></div>`
            },
            append: {
                ja: '文章の最後にまとめてデータを隠します。短い文章や、句読点がない場合に有効ですが、データ量が多いと不自然になる可能性があります。',
                en: 'Appends all hidden data at the very end of the text. Good for short texts without punctuation, but large data may handle poorly.',
                visual: `<div class="font-mono text-center mb-2"><span class="text-slate-400">Full Text Content</span><span class="text-primary font-bold">[HiddenData]</span></div>`
            },
            interleave: {
                ja: 'すべての文字の間にデータを分散させます。データ密度は高いですが、テキスト編集（コピペ等）で破損しやすいため非推奨です。',
                en: 'Distributes data between every character. High density but fragile. Not recommended as editing easily corrupts data.',
                visual: `<div class="font-mono text-center mb-2"><span class="text-slate-400">T</span><span class="text-primary font-bold">[h]</span><span class="text-slate-400">e</span><span class="text-primary font-bold">[i]</span><span class="text-slate-400">x</span><span class="text-primary font-bold">[d]</span><span class="text-slate-400">t</span></div>`
            }
        };

        const current = descriptions[strategy];
        if (current) {
            container.innerHTML = `
                ${current.visual}
                <p class="mt-2 text-slate-600 dark:text-slate-300">
                    <span class="lang-ja">${current.ja}</span>
                    <span class="lang-en hidden">${current.en}</span>
                </p>
            `;
            // Trigger language update for the newly injected content
            if (window.LangManager) window.LangManager.updateContent();
        }
    }

    updateCounters() {
        const cover = document.getElementById('embed-cover').value;
        const secret = document.getElementById('embed-secret').value;
        const warning = document.getElementById('embed-warning');
        const toggle = document.getElementById('password-toggle');

        const charsLabel = LangManager.current === 'ja' ? "文字" : "chars";

        document.getElementById('embed-cover-count').innerText = `${cover.length} ${charsLabel}`;

        const secretBytes = new TextEncoder().encode(secret).length;
        let estimatedBytes = secretBytes + 100;
        if (toggle && toggle.checked) {
            estimatedBytes = Math.ceil(estimatedBytes / 16) * 16;
        }
        const base64Bytes = Math.ceil(estimatedBytes * 1.33);
        const finalHiddenChars = base64Bytes * 4;

        const infoText = LangManager.current === 'ja'
            ? `${secret.length} 文字 (隠蔽後のデータ長: 約 ${secret.length ? finalHiddenChars : 0} 文字)`
            : `${secret.length} chars (Hidden length: approx ${secret.length ? finalHiddenChars : 0} chars)`;

        document.getElementById('embed-secret-count').innerText = infoText;

        if (secret.length > 0 && finalHiddenChars > cover.length * 5) {
            warning.classList.remove('hidden');
        } else {
            warning.classList.add('hidden');
        }
    }

    toggleAdvanced() {
        const el = document.getElementById('advanced-settings');
        const icon = document.getElementById('advanced-icon');
        el.classList.toggle('hidden');
        icon.classList.toggle('rotate-180');
    }

    switchTab(activeTab) {
        this.tabs.forEach(tab => {
            const btn = document.getElementById(`tab-${tab}`);
            const content = document.getElementById(`content-${tab}`);

            if (tab === activeTab) {
                btn.classList.replace('border-transparent', 'border-primary');
                btn.classList.replace('text-slate-500', 'text-primary');
                btn.classList.remove('dark:text-slate-400');
                content.classList.remove('hidden');
                content.classList.add('animate-fade-in');
            } else {
                btn.classList.replace('border-primary', 'border-transparent');
                btn.classList.replace('text-primary', 'text-slate-500');
                btn.classList.add('dark:text-slate-400');
                content.classList.add('hidden');
                content.classList.remove('animate-fade-in');
            }
        });
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const el = document.createElement('div');

        const styleClass = {
            success: 'bg-green-600 border-green-500 text-white',
            error: 'bg-red-600 border-red-500 text-white',
            info: 'bg-slate-700 border-slate-600 text-slate-200'
        }[type];

        const icon = {
            success: '<i class="fa-solid fa-check mr-2"></i>',
            error: '<i class="fa-solid fa-triangle-exclamation mr-2"></i>',
            info: '<i class="fa-solid fa-info-circle mr-2"></i>'
        }[type];

        el.className = `${styleClass} border rounded px-4 py-3 shadow-lg flex items-center text-sm font-bold transform transition-all duration-300 translate-y-10 opacity-0 pointer-events-auto min-w-[300px] z-50`;
        el.innerHTML = `${icon} ${message}`;

        container.appendChild(el);
        requestAnimationFrame(() => el.classList.remove('translate-y-10', 'opacity-0'));
        setTimeout(() => {
            el.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => el.remove(), 300);
        }, 4000);
    }

    async copyToClipboard(elementId) {
        const el = document.getElementById(elementId);
        el.select();
        const msg = LangManager.current === 'ja' ? 'クリップボードにコピーしました' : 'Copied to clipboard';
        try {
            await navigator.clipboard.writeText(el.value);
            this.showToast(msg, 'success');
        } catch (err) {
            document.execCommand('copy');
            this.showToast(msg, 'success');
        }
    }

    handleEmbed() {
        const cover = document.getElementById('embed-cover').value;
        const secret = document.getElementById('embed-secret').value;
        const usePassword = document.getElementById('password-toggle').checked;
        const password = usePassword ? document.getElementById('embed-password').value : null;
        const strategy = document.getElementById('embed-strategy').value;

        if (!cover) return this.showToast(LangManager.current === 'ja' ? 'カバーテキストを入力してください' : 'Please enter cover text', 'error');
        if (!secret) return this.showToast(LangManager.current === 'ja' ? '隠しメッセージを入力してください' : 'Please enter secret message', 'error');
        if (usePassword && !password) return this.showToast(LangManager.current === 'ja' ? 'パスワードを入力してください' : 'Please enter password', 'error');

        try {
            const result = SteganographyEngine.embed(cover, secret, password, strategy);
            const out = document.getElementById('embed-output');
            out.value = result;
            document.getElementById('embed-result-container').classList.remove('hidden');
            this.showToast(LangManager.current === 'ja' ? '埋め込み成功（整合性署名付き）' : 'Embedding successful (Signed)', 'success');
        } catch (e) {
            console.error(e);
            this.showToast('Error: ' + e.message, 'error');
        }
    }

    handleDecode() {
        const input = document.getElementById('decode-input').value;
        const password = document.getElementById('decode-password').value;

        if (!input) return this.showToast(LangManager.current === 'ja' ? 'テキストを入力してください' : 'Please enter text', 'error');

        try {
            const message = SteganographyEngine.decode(input, password);
            const out = document.getElementById('decode-output');
            out.value = message;
            document.getElementById('decode-result-container').classList.remove('hidden');
            this.showToast(LangManager.current === 'ja' ? 'メッセージを検出・整合性を確認しました' : 'Message detected and verified', 'success');
        } catch (e) {
            this.showToast(e.message, 'error');
            document.getElementById('decode-result-container').classList.add('hidden');
        }
    }

    handleRemove() {
        const input = document.getElementById('remove-input').value;
        const password = document.getElementById('remove-password').value;

        if (!input) return this.showToast(LangManager.current === 'ja' ? 'テキストを入力してください' : 'Please enter text', 'error');

        try {
            const cleanText = SteganographyEngine.remove(input, password);
            const out = document.getElementById('remove-output');
            out.value = cleanText;
            document.getElementById('remove-result-container').classList.remove('hidden');
            this.showToast(LangManager.current === 'ja' ? '不可視データを検証・除去しました' : 'Hidden data verified and removed', 'success');
        } catch (e) {
            this.showToast(e.message, 'error');
        }
    }
}

const ui = new UIManager();
