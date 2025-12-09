// API client with automatic JWT token attachment

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;

      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string> | undefined),
      };

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
      return { success: true, data: await response.json() };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : "Unknown error" };
    }
  }

  async get<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: "GET" });
  }

  async post<T>(endpoint: string, data: any) {
    return this.request<T>(endpoint, { method: "POST", body: JSON.stringify(data) });
  }

  async patch<T>(endpoint: string, data?: any) {
    return this.request<T>(endpoint, { method: "PATCH", body: data ? JSON.stringify(data) : undefined });
  }

  async put<T>(endpoint: string, data: any) {
    return this.request<T>(endpoint, { method: "PUT", body: JSON.stringify(data) });
  }

  async delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: "DELETE" });
  }
}

export const apiClient = new ApiClient();
