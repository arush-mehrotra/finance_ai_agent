/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        accent: '#8B5CF6',
        success: '#10B981',
        error: '#EF4444',
        dark: '#0F172A',
        card: '#1E293B'
      }
    },
  },
  plugins: [],
}
