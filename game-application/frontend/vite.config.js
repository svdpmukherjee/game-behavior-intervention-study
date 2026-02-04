import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Determine API URL based on mode
  const apiUrl =
    mode === "production"
      ? "https://anagram-solving-game-study.onrender.com"
      : "http://localhost:8000";

  return {
    plugins: [react(), tailwindcss()],
    // Define environment variables that will be statically replaced at build time
    define: {
      "import.meta.env.VITE_API_URL": JSON.stringify(apiUrl),
    },
    server: {
      proxy: {
        "/api": {
          target: apiUrl,
          changeOrigin: true,
        },
      },
    },
  };
});
