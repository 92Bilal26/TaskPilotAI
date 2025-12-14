// Centralized configuration for environment-specific settings

/**
 * Get the current environment
 */
export function getEnvironment(): 'development' | 'production' | 'test' {
  return (process.env.NODE_ENV as any) || 'development';
}

/**
 * Check if running in production
 */
export function isProduction(): boolean {
  return getEnvironment() === 'production';
}

/**
 * Check if running in development
 */
export function isDevelopment(): boolean {
  return getEnvironment() === 'development';
}

/**
 * Get the API base URL with automatic environment detection
 */
export function getApiUrl(): string {
  // Priority 1: Environment variable (set in .env.development or .env.production)
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // Priority 2: Auto-detect based on hostname (for cases where env var is missing)
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;

    // Check if running on Vercel or other production domain
    if (hostname.includes('vercel.app') || hostname.includes('taskpilot')) {
      return 'https://taskpilot-api-5l18.onrender.com';
    }

    // Check if running on localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
  }

  // Priority 3: Fallback based on NODE_ENV
  return isProduction()
    ? 'https://taskpilot-api-5l18.onrender.com'
    : 'http://localhost:8000';
}

/**
 * Application configuration
 */
export const config = {
  // API Configuration
  api: {
    baseUrl: getApiUrl(),
    timeout: 30000, // 30 seconds
  },

  // Authentication Configuration
  auth: {
    tokenKey: 'access_token',
    refreshTokenKey: 'refresh_token',
    tokenExpiry: 7 * 24 * 60 * 60, // 7 days in seconds
  },

  // App Configuration
  app: {
    name: 'TaskPilotAI',
    version: '2.0.0',
    environment: getEnvironment(),
  },

  // Feature Flags
  features: {
    enableDebugLogging: isDevelopment(),
    enableAnalytics: isProduction(),
  },
} as const;

/**
 * Log configuration in development
 */
if (isDevelopment() && typeof window !== 'undefined') {
  console.log('[Config] Application Configuration:', config);
}

export default config;
