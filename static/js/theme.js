
class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || this.getSystemPreference();
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createToggleButton();
        this.bindEvents();
    }

    getSystemPreference() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    getStoredTheme() {
        return localStorage.getItem('fitai-theme');
    }

    storeTheme(theme) {
        localStorage.setItem('fitai-theme', theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.storeTheme(theme);
        this.updateToggleButton();
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
        
        //  subtle animation effect
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.id = 'themeToggle';
        button.setAttribute('aria-label', 'Toggle theme');
        button.setAttribute('title', 'Toggle between light and dark theme');
        
        document.body.appendChild(button);
        this.updateToggleButton();
    }

    updateToggleButton() {
        const button = document.getElementById('themeToggle');
        if (!button) return;

        if (this.currentTheme === 'dark') {
            button.innerHTML = '<i class="fas fa-sun"></i><span>Light</span>';
        } else {
            button.innerHTML = '<i class="fas fa-moon"></i><span>Dark</span>';
        }
    }

    bindEvents() {
        // Toggle button click event
        document.addEventListener('click', (e) => {
            if (e.target.closest('#themeToggle')) {
                e.preventDefault();
                this.toggleTheme();
            }
        });

        
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!this.getStoredTheme()) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });

        // Keyboard shortcut (Ctrl/Cmd + Shift + T)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.toggleTheme();
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}