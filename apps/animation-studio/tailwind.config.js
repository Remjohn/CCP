/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#1a1a1a',
        panel: '#242424',
        border: '#333333',
        accent: '#3b82f6',
      },
    },
  },
  plugins: [],
}
