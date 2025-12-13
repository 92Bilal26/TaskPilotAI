"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);

    // Check if user is authenticated
    const token = localStorage.getItem("auth_token");

    if (token) {
      // User is logged in, go to dashboard
      router.push("/dashboard");
    } else {
      // User is not logged in, go to signin
      router.push("/auth/signin");
    }
  }, [router]);

  // Don't render anything until client is mounted to avoid hydration mismatch
  if (!isMounted) {
    return null;
  }

  // Show loading while redirecting
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
      <h1>Loading...</h1>
    </div>
  );
}
