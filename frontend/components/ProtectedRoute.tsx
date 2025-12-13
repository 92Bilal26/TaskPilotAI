"use client";

import { ReactNode } from "react";
import { useAuth } from "@/lib/useAuth";

interface ProtectedRouteProps {
  children: ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoading } = useAuth();

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center animate-fade-in">
        <div className="animate-spin h-12 w-12 rounded-full border-4 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  // If not loading, the useAuth hook will handle redirect if not authenticated
  return <>{children}</>;
}
