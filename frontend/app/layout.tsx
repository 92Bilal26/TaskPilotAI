import { ReactNode } from "react";
import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";

// Primary font - Inter (sans-serif)
const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
  preload: true,
});

// Secondary font - Playfair Display (serif for headings)
const playfair = Playfair_Display({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-playfair",
  weight: ["400", "500", "600", "700", "800", "900"],
  preload: true,
});

export const metadata = {
  title: "TaskPilotAI - Intelligent Task Management",
  description: "A modern, intelligent task management application with AI assistance",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${playfair.variable}`}
    >
      <head>
        {/* OpenAI ChatKit JS Script - Required for ChatKit web component */}
        <script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          async
        ></script>
      </head>
      <body suppressHydrationWarning className="bg-color-background text-color-text transition-colors">
        {children}
      </body>
    </html>
  );
}
