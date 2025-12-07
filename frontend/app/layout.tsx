"use client";

import { ReactNode } from "react";
import "./globals.css";
import AuthGuard from "@/components/Auth/AuthGuard";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthGuard>{children}</AuthGuard>
      </body>
    </html>
  );
}
