window.ThemeManager = {
    init() {
        this.applyTheme();
        this.renderToggle();
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
            if (!localStorage.theme) this.applyTheme();
        });
    },

    getTheme() {
        if (localStorage.theme === 'dark') return 'dark';
        if (localStorage.theme === 'light') return 'light';
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    },

    setTheme(theme) {
        if (theme === 'system') {
            localStorage.removeItem('theme');
        } else {
            localStorage.theme = theme;
        }
        this.applyTheme();
    },

    applyTheme() {
        const theme = this.getTheme();
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        this.updateIcon();
    },

    toggle() {
        const current = this.getTheme();
        this.setTheme(current === 'dark' ? 'light' : 'dark');
    },

    renderToggle() {
        // Implement in specific pages or globally if shared header exists
        const btn = document.getElementById('theme-toggle');
        if (btn) {
            // Remove old listeners to avoid duplicates if re-rendered (though usually new element)
            // But here we just add new one.
            // Since we use addEventListener, we might want to be careful.
            // However, replacing innerHTML destroys old elements, so listeners are gone.
            btn.onclick = () => this.toggle();
            this.updateIcon();
        }
    },

    updateIcon() {
        const btn = document.getElementById('theme-text');
        if (btn) {
            const theme = localStorage.theme ? localStorage.theme : 'System';
            // btn.innerText = theme.charAt(0).toUpperCase() + theme.slice(1);
        }
    }
};

window.LangManager = {
    current: 'ja',

    init() {
        // Priority: LocalStorage -> Default 'ja'
        this.current = localStorage.lang || 'ja';
        this.updateContent();
    },

    setLang(lang) {
        this.current = lang;
        localStorage.lang = lang; // Persist preference
        this.updateContent();
    },

    updateContent() {
        // Simple visibility toggle for dedicated blocks
        // Using style.display to toggle between block and none
        // Note: Elements might use 'hidden' class by default, so we toggle display style

        document.querySelectorAll('.lang-ja').forEach(el => {
            // If current is ja, remove display:none (revert to CSS default or block)
            // Using CSS class 'hidden' manipulation might be cleaner if Tailwind is used everywhere
            if (this.current === 'ja') {
                el.classList.remove('hidden');
                // Also ensure it doesn't have inline display:none from previous toggle
                el.style.display = '';
            } else {
                el.classList.add('hidden');
            }
        });

        document.querySelectorAll('.lang-en').forEach(el => {
            if (this.current === 'en') {
                el.classList.remove('hidden');
                el.style.display = '';
            } else {
                el.classList.add('hidden');
            }
        });

        // Handle data attributes if any legacy ones exist
        document.querySelectorAll('[data-ja]').forEach(el => {
            if (this.current === 'ja') {
                el.innerText = el.getAttribute('data-ja');
            }
        });
        document.querySelectorAll('[data-en]').forEach(el => {
            if (this.current === 'en') {
                el.innerText = el.getAttribute('data-en');
            }
        });
    }
}

// Initialize
// document.addEventListener('DOMContentLoaded', () => {
//     ThemeManager.init();
//     LangManager.init();
// });
// Manual initialization required after Layout Rendering

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Automatically determine path depth based on location or just use root absolute path
        // For User Pages (username.github.io), '/sw.js' works.
        // For local development or sub-path projects, relative might be safer but intricate.
        // We will try '/sw.js' assuming root deployment.
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('SW registered:', reg.scope))
            .catch(err => console.log('SW registration failed:', err));
    });
}
