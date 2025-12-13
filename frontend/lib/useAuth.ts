import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "./api";

export function useAuth() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if token exists in localStorage
    const token = apiClient.getAuthToken();

    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
      // Redirect to signin if no token
      router.push("/auth/signin");
    }

    setIsLoading(false);
  }, [router]);

  const logout = () => {
    apiClient.logout();
    setIsAuthenticated(false);
    router.push("/auth/signin");
  };

  return {
    isAuthenticated,
    isLoading,
    logout,
  };
}
