import type { Config } from "tailwindcss";

// Tokens mirror the color system in docs/DESIGN.md.
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#070A0E",
        "bg-secondary": "#090D13",
        surface: "#0C1118",
        "surface-raised": "#10161F",
        "surface-hover": "#131A24",
        border: "rgba(255,255,255,0.08)",
        "border-strong": "rgba(255,255,255,0.12)",
        primary: "#F3F4F6",
        secondary: "#9CA3AF",
        muted: "#68707D",
        maroon: {
          DEFAULT: "#8A1538",
          hover: "#9E1B45",
          dark: "#64102A",
        },
        success: "#59C9A5",
        warning: "#D69A45",
        danger: "#D65A6F",
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "Inter", "-apple-system", "Segoe UI", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
