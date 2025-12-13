"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";

export default function AuthGuard({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true);
  const [isMounted, setIsMounted] = useState(false);

  // Public routes that don't require authentication
  const publicRoutes = ["/auth/signin", "/auth/signup"];
  const isPublicRoute = publicRoutes.some((route) => pathname.startsWith(route));

  useEffect(() => {
    setIsMounted(true);

    // Don't check auth on public routes
    if (isPublicRoute) {
      setIsLoading(false);
      return;
    }

    // Check if user has auth token
    const token = localStorage.getItem("auth_token");
    if (!token) {
      router.push("/auth/signin");
    } else {
      setIsLoading(false);
    }
  }, [router, pathname, isPublicRoute]);

  // Only render children after mounting to avoid hydration mismatch
  if (!isMounted || isLoading) {
    return <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>Loading...</div>;
  }

  return <>{children}</>;
}
