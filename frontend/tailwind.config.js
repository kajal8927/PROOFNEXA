/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0f172a',    // Dark navy (slate-900)
          darker: '#020617',  // Very dark (slate-950)
          purple: '#6d28d9',  // Deep purple (violet-700)
          light: '#8b5cf6',   // Light purple (violet-500)
          accent: '#c4b5fd',  // Accent purple (violet-300)
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
