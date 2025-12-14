// API client with automatic JWT token attachment
import { getApiUrl, config } from './config';

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  emailVerified: boolean;
  createdAt: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  status?: number;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    // Use provided baseUrl or get from centralized config
    this.baseUrl = baseUrl || getApiUrl();

    // Log API URL in development for debugging
    if (config.features.enableDebugLogging && typeof window !== 'undefined') {
      console.log('[API Client] Initialized with URL:', this.baseUrl);
      console.log('[API Client] Environment:', config.app.environment);
    }
  }

  private getToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("access_token");
    }
    return null;
  }

  private setToken(token: string): void {
    if (typeof window !== "undefined") {
      localStorage.setItem("access_token", token);
    }
  }

  private clearToken(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const token = this.getToken();

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

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          this.clearToken();
        }
        return {
          success: false,
          error: data?.detail || `API Error: ${response.statusText}`,
          status: response.status,
          data: data,
        };
      }

      return { success: true, data, status: response.status };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  // Authentication endpoints
  async signup(email: string, password: string, name: string): Promise<ApiResponse<AuthTokens>> {
    const response = await this.request<AuthTokens>("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    });

    if (response.success && response.data) {
      this.setToken(response.data.access_token);
      if (typeof window !== "undefined") {
        localStorage.setItem("refresh_token", response.data.refresh_token);
      }
    }

    return response;
  }

  async signin(email: string, password: string): Promise<ApiResponse<AuthTokens>> {
    const response = await this.request<AuthTokens>("/auth/signin", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (response.success && response.data) {
      this.setToken(response.data.access_token);
      if (typeof window !== "undefined") {
        localStorage.setItem("refresh_token", response.data.refresh_token);
      }
    }

    return response;
  }

  async logout(): Promise<void> {
    this.clearToken();
  }

  // Task endpoints
  async getTasks(): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>("/tasks", { method: "GET" });
  }

  async getTask(taskId: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/tasks/${taskId}`, { method: "GET" });
  }

  async createTask(title: string, description?: string): Promise<ApiResponse<Task>> {
    return this.request<Task>("/tasks", {
      method: "POST",
      body: JSON.stringify({ title, description }),
    });
  }

  async updateTask(
    taskId: string,
    updates: { title?: string; description?: string; completed?: boolean }
  ): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    });
  }

  async toggleTask(taskId: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  async deleteTask(taskId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  async getPendingTasks(): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>("/tasks/filter/pending", { method: "GET" });
  }

  async getCompletedTasks(): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>("/tasks/filter/completed", { method: "GET" });
  }

  // Generic HTTP methods for backward compatibility
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "GET" });
  }

  async post<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async patch<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }

  // Utility methods
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  getAuthToken(): string | null {
    return this.getToken();
  }
}

export const apiClient = new ApiClient();
