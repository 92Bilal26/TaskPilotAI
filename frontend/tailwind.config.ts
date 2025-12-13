import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom Color Palette
      colors: {
        // Primary: Blue
        primary: {
          50: "#F0F9FF",
          100: "#E0F2FE",
          200: "#BAE6FD",
          300: "#7DD3FC",
          400: "#38BDF8",
          500: "#0EA5E9",
          600: "#0284C7",
          700: "#0369A1",
          800: "#075985",
          900: "#0C4A6E",
        },
        // Secondary: Indigo
        secondary: {
          50: "#F0F4FF",
          100: "#E0E7FF",
          200: "#C7D2FE",
          300: "#A5B4FC",
          400: "#818CF8",
          500: "#6366F1",
          600: "#4F46E5",
          700: "#4338CA",
          800: "#3730A3",
          900: "#312E81",
        },
        // Success: Emerald
        success: {
          50: "#F0FDF4",
          100: "#DCFCE7",
          200: "#BBFCD9",
          300: "#86EFAC",
          400: "#4ADE80",
          500: "#22C55E",
          600: "#16A34A",
          700: "#15803D",
          800: "#166534",
          900: "#145231",
        },
        // Warning: Amber
        warning: {
          50: "#FFFBEB",
          100: "#FEF3C7",
          200: "#FDE68A",
          300: "#FCD34D",
          400: "#FBBF24",
          500: "#F59E0B",
          600: "#D97706",
          700: "#B45309",
          800: "#92400E",
          900: "#78350F",
        },
        // Error: Red
        error: {
          50: "#FEF2F2",
          100: "#FEE2E2",
          200: "#FECACA",
          300: "#FCA5A5",
          400: "#F87171",
          500: "#EF4444",
          600: "#DC2626",
          700: "#B91C1C",
          800: "#991B1B",
          900: "#7F1D1D",
        },
        // Info: Indigo (alias for notifications)
        info: "#6366F1",
      },

      // Typography Scale
      fontSize: {
        display: ["3.5rem", { lineHeight: "1.2", fontWeight: "700" }], // 56px
        h1: ["2.25rem", { lineHeight: "1.2", fontWeight: "700" }], // 36px
        h2: ["1.5rem", { lineHeight: "1.3", fontWeight: "600" }], // 24px
        h3: ["1.25rem", { lineHeight: "1.4", fontWeight: "600" }], // 20px
        body: ["1rem", { lineHeight: "1.5", fontWeight: "400" }], // 16px
        sm: ["0.875rem", { lineHeight: "1.25", fontWeight: "400" }], // 14px
        xs: ["0.75rem", { lineHeight: "1.4", fontWeight: "400" }], // 12px
      },

      // Spacing Scale (8px baseline)
      spacing: {
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
        "2xl": "48px",
        "3xl": "64px",
      },

      // Border Radius
      borderRadius: {
        none: "0",
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
        full: "9999px",
      },

      // Box Shadows
      boxShadow: {
        subtle: "0 1px 2px 0 rgba(0,0,0,0.05)",
        sm: "0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)",
        md: "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)",
        lg: "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)",
        xl: "0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)",
        elevated: "0 20px 25px -5px rgba(0,0,0,0.15), 0 8px 10px -6px rgba(0,0,0,0.2)",
      },

      // Container Sizes
      maxWidth: {
        xs: "320px",
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1536px",
      },

      // Animation & Transitions
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-in": "slideIn 0.2s ease-out",
        "scale-bounce": "scaleBounce 0.4s ease-in-out",
      },

      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideIn: {
          "0%": { transform: "translateY(4px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        scaleBounce: {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.05)" },
        },
      },

      // Transition Duration
      transitionDuration: {
        fast: "150ms",
        normal: "300ms",
        slow: "500ms",
      },

      // Z-Index
      zIndex: {
        dropdown: "100",
        sticky: "200",
        "modal-backdrop": "300",
        modal: "310",
        tooltip: "320",
      },
    },
  },
  darkMode: "class",
  plugins: [],
} satisfies Config;