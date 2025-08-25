class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || this.getSystemPreference();
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
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
        
        // Add subtle animation effect
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    updateToggleButton() {
        const button = document.getElementById('theme-toggle');
        if (!button) return;

        const icons = button.querySelectorAll('i');
        if (this.currentTheme === 'dark') {
            icons[0].style.display = 'none';
            icons[1].style.display = 'inline-block';
        } else {
            icons[0].style.display = 'inline-block';
            icons[1].style.display = 'none';
        }
    }

    bindEvents() {
        // Toggle button click event
        document.addEventListener('click', (e) => {
            if (e.target.closest('#theme-toggle')) {
                e.preventDefault();
                this.toggleTheme();
            }
        });

        // Watch for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!this.getStoredTheme()) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}