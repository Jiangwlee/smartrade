import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: "0.0.0.0",
    // open: true,
    fs: {
      strict: true,
    },
    cors: true, // 允许跨域
    proxy: {
      "/smartrade": {
        target: "http://localhost:8000/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/smartrade/, ""),
      },
      // '/api': {
      //   target: 'http://localhost:8033',
      //   changeOrigin: true,
      //   rewrite: (path) => path.replace(/^\/backend/, '')
      // },
    },
  },
})
