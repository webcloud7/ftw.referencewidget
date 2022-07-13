import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: path.resolve(__dirname, "ftw/referencewidget/resources/dist"),
    lib: {
      entry: path.resolve(
        __dirname,
        "ftw/referencewidget/resources/src/main.js"
      ),
      name: "Referencewidget",
      fileName: (format) => `referencewidget.${format}.js`,
    },
    rollupOptions: {
      // make sure to externalize deps that shouldn"t be bundled
      // into your library
      external: [],
      output: {
        // Provide global variables to use in the UMD build
        // for externalized deps
        globals: {},
      },
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(
        new URL("./ftw/referencewidget/resources/src/widget", import.meta.url)
      ),
    },
  },
});
