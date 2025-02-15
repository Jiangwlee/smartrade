import { fileURLToPath, URL } from 'node:url'

import { loadEnv, defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => { 
  const env = loadEnv(mode, process.cwd())
  console.log("当前模式：", mode)
  console.log("当前环境：", env)
  return {
    plugins: [
      vue(),
    ],
    define: {
      'import.meta.env': env
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: mode === 'development'? {
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
      },
    } : {},
    build: {
      // 生产环境打包的相关配置，例如设置输出路径、文件名等
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false, // 根据需要决定是否生成sourcemap
      rollupOptions: {
          // 配置打包时的模块处理等选项
          output: {
              // 可以设置 chunk文件和入口文件的命名规则等
              chunkFileNames: 'js/[name]-[hash].js',
              entryFileNames: 'js/[name]-[hash].js',
              assetFileNames: 'assets/[name]-[hash].[ext]'
          }
      }
    }
  }
})
