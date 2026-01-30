class LayoutManager {
    constructor(rootPath = './') {
        this.rootPath = rootPath;
    }

    renderHeader() {
        const headerHTML = `
        <header class="w-full py-6 px-6 md:px-12 flex justify-between items-center z-50 bg-white/80 dark:bg-dark/80 backdrop-blur-md fixed top-0 border-b border-gray-200 dark:border-white/5 transition-all duration-300">
            <div class="text-2xl font-bold tracking-tight">
                <a href="${this.rootPath}index.html">Itsuki<span class="text-primary">Kanai</span></a>
            </div>
            <div class="flex items-center space-x-6">
                <nav class="hidden md:flex space-x-6">
                    <a href="${this.rootPath}index.html" class="hover:text-primary transition-colors duration-300">
                        <span class="lang-ja">ホーム</span><span class="lang-en hidden">Home</span>
                    </a>
                    <a href="${this.rootPath}projects/index.html" class="hover:text-primary transition-colors duration-300">
                        <span class="lang-ja">プロジェクト</span><span class="lang-en hidden">Projects</span>
                    </a>
                    <a href="#" class="hover:text-primary transition-colors duration-300 text-gray-400 cursor-not-allowed" title="Coming Soon">
                        <span class="lang-ja">ブログ</span><span class="lang-en hidden">Blog</span>
                    </a>
                </nav>

                <!-- Controls -->
                <div class="flex items-center space-x-3 pl-6 border-l border-gray-200 dark:border-white/10">
                    <button id="theme-toggle"
                        class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-white/10 transition-colors"
                        title="Toggle Theme">
                        <svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z">
                            </path>
                        </svg>
                        <svg class="w-5 h-5 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z">
                            </path>
                        </svg>
                    </button>
                    <!-- Language Dropdown -->
                    <div class="relative group">
                        <button class="flex items-center space-x-1 text-sm font-medium hover:text-primary transition-colors">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129">
                                </path>
                            </svg>
                        </button>
                        <div
                            class="absolute right-0 mt-2 w-56 bg-white dark:bg-[#1a1a1a] rounded-lg shadow-xl border border-gray-100 dark:border-white/5 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 translate-y-2 group-hover:translate-y-0 text-gray-800 dark:text-gray-200 max-h-[80vh] overflow-y-auto">
                            <div class="py-1">
                                <button onclick="LangManager.setLang('ja')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5 font-medium">日本語 (Japanese)</button>
                                <button onclick="LangManager.setLang('en')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5 font-medium">English</button>
                                
                                <div class="border-t border-gray-100 dark:border-white/5 my-1"></div>
                                <div class="px-4 py-1 text-xs text-gray-400 font-semibold uppercase tracking-wider">Translate</div>
                                
                                <button onclick="LayoutManager.translate('zh-CN')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">简体中文 (Simplified)</button>
                                <button onclick="LayoutManager.translate('zh-TW')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">繁體中文 (Traditional)</button>
                                <button onclick="LayoutManager.translate('ko')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">한국어 (Korean)</button>
                                <button onclick="LayoutManager.translate('es')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">Español (Spanish)</button>
                                <button onclick="LayoutManager.translate('fr')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">Français (French)</button>
                                <button onclick="LayoutManager.translate('de')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">Deutsch (German)</button>
                                <button onclick="LayoutManager.translate('id')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">Bahasa Indonesia</button>
                                <button onclick="LayoutManager.translate('hi')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">हिन्दी (Hindi)</button>
                                <button onclick="LayoutManager.translate('pt')"
                                    class="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5">Português (Portuguese)</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        <!-- Spacer for fixed header -->
        <div class="h-24"></div>
        `;
        document.getElementById('header-container').innerHTML = headerHTML;
    }

    renderFooter() {
        const footerHTML = `
        <footer class="py-10 text-center text-gray-500 text-sm mt-auto border-t border-gray-200 dark:border-white/5 bg-gray-50 dark:bg-dark transition-colors duration-300">
            <div class="max-w-4xl mx-auto px-6 space-y-4">
                <div class="flex justify-center space-x-6 mb-4">
                     <a href="https://github.com/itsukikanai" target="_blank" class="hover:text-primary transition-colors">
                        <i class="fa-brands fa-github text-xl"></i> Github
                     </a>
                </div>
                
                <p class="text-xs text-gray-400">
                    <span class="lang-ja">※当サイトは日本語での動作を前提としています。その他の言語での動作は確認されていない可能性があります。</span>
                    <span class="lang-en hidden">* This site is designed to function in <button onclick="LangManager.setLang('ja')" class="underline hover:text-primary transition-colors">Japanese</button>. Operation in other languages may not have been verified.</span>
                </p>

                <div class="flex justify-center space-x-4 text-xs">
                     <a href="${this.rootPath}disclaimer/index.html" class="hover:text-primary transition-colors underline">
                        <span class="lang-ja">免責事項 (共通)</span>
                        <span class="lang-en hidden">Disclaimer (General)</span>
                     </a>
                </div>

                <p>&copy; 2026- Itsuki Kanai. All rights reserved.</p>
            </div>
        </footer>
        `;
        document.getElementById('footer-container').innerHTML = footerHTML;
    }

    init() {
        this.renderHeader();
        this.renderFooter();
        // Re-initialize managers because DOM has changed
        if (window.ThemeManager) ThemeManager.init();
        if (window.LangManager) LangManager.init();
    }

    static translate(code) {
        const path = window.location.pathname;
        const url = `https://itsukikanai-github-io.translate.goog${path}?_x_tr_sl=auto&_x_tr_tl=${code}&_x_tr_hl=ja`;
        window.location.href = url;
    }
}
