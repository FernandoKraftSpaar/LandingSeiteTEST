import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/LandingSeiteTEST/' : '/',
  server: {
    port: 3000,
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
