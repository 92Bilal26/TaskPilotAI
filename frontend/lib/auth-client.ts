// Better Auth SDK client

import { createAuthClient } from "better-auth/client";

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const authClient = createAuthClient({
  baseURL: apiUrl,
  endpoints: {
    signUpEmail: `${apiUrl}/auth/signup`,
    signInEmail: `${apiUrl}/auth/signin`,
    signOut: `${apiUrl}/auth/signout`,
    getSession: `${apiUrl}/auth/session`,
  },
});

export async function getSession() {
  try {
    let token = "";

    if (typeof window !== "undefined" && typeof document !== "undefined") {
      token = localStorage.getItem("auth_token") || "";
    }

    const response = await fetch(`${apiUrl}/auth/session`, {
      headers: {
        "Authorization": token ? `Bearer ${token}` : "",
      },
    });
    if (response.ok) {
      return await response.json();
    }
    return null;
  } catch (error) {
    console.error("Failed to get session:", error);
    return null;
  }
}

export async function signOut() {
  try {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("refresh_token");
    }
  } catch (error) {
    console.error("Failed to sign out:", error);
  }
}
