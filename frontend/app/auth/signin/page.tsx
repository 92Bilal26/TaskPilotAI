"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiClient } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";

export default function SigninPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  // Prevent hydration mismatch
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleSignin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    const result = await apiClient.post("/auth/signin", { email, password });
    if (!result.success) {
      setError(result.error || "Signin failed");
    } else {
      const data = result.data as { access_token: string; refresh_token: string };
      localStorage.setItem("auth_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      router.push("/dashboard");
    }
    setLoading(false);
  };

  if (!isMounted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="animate-spin h-12 w-12 rounded-full border-4 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 flex-col justify-between p-12 relative overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full -mr-48 -mt-48"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-white/5 rounded-full -ml-36 -mb-36"></div>

        {/* Branding Content */}
        <div className="relative z-10">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-white/20 backdrop-blur-md rounded-2xl mb-8 border border-white/30 hover:bg-white/30 transition">
            <span className="text-white text-2xl font-bold">✓</span>
          </div>
          <h1 className="text-5xl font-bold text-white mb-4 leading-tight">
            Welcome Back to TaskPilotAI
          </h1>
          <p className="text-lg text-white/80 max-w-md">
            Stay focused, get things done. Manage your tasks with intelligent insights and seamless organization.
          </p>
        </div>

        {/* Features List */}
        <div className="relative z-10 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
              <span>📋</span>
            </div>
            <span className="text-white/90">Organize tasks effortlessly</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
              <span>🎯</span>
            </div>
            <span className="text-white/90">Track progress in real-time</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
              <span>⚡</span>
            </div>
            <span className="text-white/90">Boost your productivity</span>
          </div>
        </div>
      </div>

      {/* Right Side - Sign In Form */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center items-center px-6 py-12 sm:px-8 md:px-12">
        <div className="w-full max-w-md">
          {/* Header */}
          <div className="mb-8 sm:mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">Sign In</h2>
            <p className="text-gray-600">
              Don't have an account?{" "}
              <Link href="/auth/signup" className="text-primary-600 font-semibold hover:text-primary-700 transition">
                Create one
              </Link>
            </p>
          </div>

          {/* Error Alert */}
          {error && (
            <Alert variant="destructive" className="mb-6">
              {error}
            </Alert>
          )}

          {/* Form */}
          <form onSubmit={handleSignin} className="space-y-5">
            {/* Email Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                disabled={loading}
              />
            </div>

            {/* Password Input */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-semibold text-gray-700">Password</label>
                <Link href="#" className="text-xs text-primary-600 hover:text-primary-700 font-medium transition">
                  Forgot?
                </Link>
              </div>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>

            {/* Sign In Button */}
            <Button
              type="submit"
              disabled={loading}
              className="w-full mt-8"
              size="lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin h-4 w-4 rounded-full border-2 border-white border-t-transparent"></div>
                  Signing in...
                </span>
              ) : (
                "Sign In"
              )}
            </Button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-8 p-4 bg-primary-50 border border-primary-200 rounded-xl">
            <p className="text-xs font-semibold text-primary-900 mb-2">Demo Credentials:</p>
            <p className="text-xs text-primary-700">Email: demo@example.com</p>
            <p className="text-xs text-primary-700">Password: demo123</p>
          </div>

          {/* Footer */}
          <p className="text-center mt-8 text-sm text-gray-500">
            By signing in, you agree to our{" "}
            <Link href="#" className="text-primary-600 hover:text-primary-700 font-medium transition">
              Terms of Service
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
