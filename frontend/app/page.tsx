"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
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

  // Show loading while redirecting
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
      <h1>Loading...</h1>
    </div>
  );
}
