/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        'chat-user': '#e0f2fe',
        'chat-ai': '#f5f5f5',
        'chat-tool': '#fef3c7'
      }
    }
  },
  plugins: []
}