"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiClient } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  // Prevent hydration mismatch
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    setLoading(true);
    setError("");
    const result = await apiClient.post("/auth/signup", { email, password, name });
    if (!result.success) {
      setError(result.error || "Signup failed");
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
      <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-primary-50 flex items-center justify-center">
        <div className="animate-spin h-12 w-12 rounded-full border-4 border-secondary-200 border-t-secondary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-primary-50 flex flex-col lg:flex-row">
      {/* Left Side - Features (Hidden on Mobile) */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-secondary-600 via-secondary-700 to-primary-600 flex-col justify-between p-12 relative overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full -mr-48 -mt-48"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-white/5 rounded-full -ml-36 -mb-36"></div>

        {/* Features Content */}
        <div className="relative z-10">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-white/20 backdrop-blur-md rounded-2xl mb-8 border border-white/30 hover:bg-white/30 transition">
            <span className="text-white text-2xl font-bold">✓</span>
          </div>
          <h1 className="text-5xl font-bold text-white mb-4 leading-tight">
            Join TaskPilotAI Today
          </h1>
          <p className="text-lg text-white/80 max-w-md">
            Experience the future of task management with AI-powered insights and intelligent organization.
          </p>
        </div>

        {/* Benefits List */}
        <div className="relative z-10 space-y-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center flex-shrink-0 mt-1">
              <span>🚀</span>
            </div>
            <div>
              <p className="text-white font-semibold">Quick Setup</p>
              <p className="text-white/70 text-sm">Get started in seconds</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center flex-shrink-0 mt-1">
              <span>🤖</span>
            </div>
            <div>
              <p className="text-white font-semibold">AI Insights</p>
              <p className="text-white/70 text-sm">Smart task recommendations</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center flex-shrink-0 mt-1">
              <span>🔒</span>
            </div>
            <div>
              <p className="text-white font-semibold">Secure & Private</p>
              <p className="text-white/70 text-sm">Your data is encrypted</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center flex-shrink-0 mt-1">
              <span>📱</span>
            </div>
            <div>
              <p className="text-white font-semibold">Multi-Device</p>
              <p className="text-white/70 text-sm">Access anywhere, anytime</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Sign Up Form */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center items-center px-4 py-8 sm:px-6 sm:py-12 md:px-8">
        <div className="w-full max-w-sm sm:max-w-md">
          {/* Header */}
          <div className="mb-8 sm:mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">Create Account</h2>
            <p className="text-gray-600">
              Already have an account?{" "}
              <Link href="/auth/signin" className="text-secondary-600 font-semibold hover:text-secondary-700 transition">
                Sign in
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
          <form onSubmit={handleSignup} className="space-y-5">
            {/* Full Name Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
              <Input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                required
                disabled={loading}
              />
            </div>

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
              <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                disabled={loading}
              />
              <p className="text-xs text-gray-500 mt-1">Minimum 8 characters</p>
            </div>

            {/* Confirm Password Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Confirm Password</label>
              <Input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>

            {/* Sign Up Button */}
            <Button
              type="submit"
              disabled={loading}
              className="w-full mt-8"
              size="lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin h-4 w-4 rounded-full border-2 border-white border-t-transparent"></div>
                  Creating account...
                </span>
              ) : (
                "Create Account"
              )}
            </Button>
          </form>

          {/* Terms & Privacy */}
          <p className="text-center mt-8 text-xs text-gray-500">
            By creating an account, you agree to our{" "}
            <Link href="#" className="text-secondary-600 hover:text-secondary-700 font-medium transition">
              Terms of Service
            </Link>
            {" "}and{" "}
            <Link href="#" className="text-secondary-600 hover:text-secondary-700 font-medium transition">
              Privacy Policy
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
