/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./static/**/*.{css,js}",
    "./src/**/*.{js,jsx,ts,tsx}",
    "./*.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--text-accent)",
        bg: {
          primary: "var(--bg-primary)",
          secondary: "var(--bg-secondary)",
          tertiary: "var(--bg-tertiary)",
        },
        text: {
          primary: "var(--text-primary)",
          secondary: "var(--text-secondary)",
        },
        border: "var(--border-color)",
        card: "var(--card-bg)",
        input: "var(--input-bg)",
      },
      boxShadow: {
        light: "0 4px 8px var(--shadow-light)",
        medium: "0 4px 15px var(--shadow-medium)",
        heavy: "0 6px 20px var(--shadow-heavy)",
      }
    },
  },
  plugins: [],
}
