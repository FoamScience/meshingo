import { defineConfig } from 'vite'

export default defineConfig({
  base: '/meshingo/',
  server: {
    watch: {
      usePolling: true,
      interval: 100,
    },
  },
})
