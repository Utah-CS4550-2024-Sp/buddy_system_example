import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./__tests_vitest.setup.js"],
    testMatch: ["./__tests__/**/*.test.jsx"],
    globals: true,
  },
})
