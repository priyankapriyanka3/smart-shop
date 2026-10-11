/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0066FF',
        'primary-dark': '#0052CC',
        success: '#00A86B',
        warning: '#FF8C00',
        error: '#DC2626',
        background: '#FAFAFA',
        surface: '#FFFFFF',
        border: '#E5E5E5',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
