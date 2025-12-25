/**
 * ChatKit Configuration
 *
 * Configuration for OpenAI ChatKit integration
 * Handles API endpoints, authentication, and UI customization
 */

import type { UseChatKitOptions } from '@openai/chatkit-react'

// Get environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const OPENAI_API_KEY = process.env.NEXT_PUBLIC_OPENAI_API_KEY || ''

// Domain public key from OpenAI platform registration
// This is required for production domain verification
const DOMAIN_PUBLIC_KEY = process.env.NEXT_PUBLIC_DOMAIN_PUBLIC_KEY || 'domain_pk_694d951d300881908730eaa457e5605809652cfa18d7a99a'

// Domain key for ChatKit verification (required)
// This should be a unique identifier for your domain
// Default is acceptable for local development and testing
const DOMAIN_KEY = process.env.NEXT_PUBLIC_DOMAIN_KEY || 'taskpilot-production'

// ChatKit endpoint - Full path to the ChatKit protocol handler
// The ChatKit SDK sends requests to: {API_URL}/v1/chat/completions (internally managed)
// So we point it to the base endpoint and it handles the path
const API_URL = `${API_BASE_URL}/api/v1/chatkit`

/**
 * Get JWT token from Better Auth
 * Tries multiple locations where token might be stored
 */
function getAuthToken(): string | null {
  // Try access_token first (standard from API client)
  let token = localStorage.getItem('access_token')
  if (token) return token

  // Try auth_token (alternative)
  token = localStorage.getItem('auth_token')
  if (token) return token

  // Try the auth-token key (Better Auth)
  token = localStorage.getItem('authjs.session-token')
  if (token) return token

  // Try sessionStorage
  token = sessionStorage.getItem('access_token')
  if (token) return token

  token = sessionStorage.getItem('auth_token')
  if (token) return token

  return null
}

/**
 * Custom fetch function that adds JWT authentication
 * Signature matches standard fetch API for compatibility
 */
async function authenticatedFetch(
  input: string | URL | Request,
  options?: RequestInit
): Promise<Response> {
  // Get JWT token
  const token = getAuthToken()

  // Build headers as plain object
  const headers: Record<string, string> = {
    ...(options?.headers as Record<string, string> || {}),
  }

  // Add JWT token if available
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  // Add domain key for ChatKit verification
  headers['X-ChatKit-Domain-Key'] = DOMAIN_KEY

  // Return fetch with updated options
  return fetch(input, {
    ...options,
    headers,
  })
}

/**
 * ChatKit Configuration
 *
 * Custom Backend Integration (Advanced Pattern)
 *
 * Uses the official quickstart pattern with:
 * - api.url: Custom backend endpoint
 * - domainKey: Domain identifier for verification
 * - authenticatedFetch: Custom fetch wrapper for JWT auth
 */
export const chatKitConfig: UseChatKitOptions = {
  // ============================================
  // API Configuration for Custom Backend
  // ============================================
  api: {
    /**
     * Custom backend URL endpoint
     * Points to our FastAPI chatkit handler
     */
    url: API_URL,

    /**
     * Domain public key from OpenAI platform
     * Required for production domain verification
     */
    publicKey: DOMAIN_PUBLIC_KEY,

    /**
     * Domain key for ChatKit verification
     * Uniquely identifies this deployment
     */
    domainKey: DOMAIN_KEY,

    /**
     * Custom fetch function with JWT authentication
     * Wraps all API calls to add Bearer token
     */
    fetch: authenticatedFetch,
  },

  // ============================================
  // Theme & Appearance
  // ============================================
  theme: 'light',

  // ============================================
  // Header Configuration
  // ============================================
  header: {
    enabled: true,
    title: {
      enabled: true,
      text: 'TaskPilot AI Chat',
    },
  },

  // ============================================
  // History/Conversation Sidebar
  // ============================================
  history: {
    enabled: true,
    showDelete: true,
    showRename: true,
  },

  // ============================================
  // Composer Configuration
  // ============================================
  composer: {
    placeholder: 'Ask me to add, update, or delete tasks...',
  },

  // ============================================
  // Disclaimer
  // ============================================
  disclaimer: {
    text: 'ChatKit powered by OpenAI • Managed by TaskPilot AI',
  },

  // ============================================
  // Event Handlers (OPTIONAL)
  // ============================================

  /**
   * Handle client-side tool invocations
   * These are tools that run on the frontend instead of the backend
   */
  onClientTool: async (toolCall) => {
    console.log('Client tool invoked:', toolCall.name, toolCall.params)

    // Handle specific client tools if needed
    switch (toolCall.name) {
      case 'open_external_link':
        window.open(toolCall.params.url as string, '_blank')
        return { success: true }

      case 'copy_to_clipboard':
        const text = toolCall.params.text as string
        await navigator.clipboard.writeText(text)
        return { success: true }

      default:
        return { error: `Unknown client tool: ${toolCall.name}` }
    }
  },

  /**
   * Handle ChatKit ready event
   */
  onReady: () => {
    console.log('ChatKit is ready!')
  },

  /**
   * Handle errors
   */
  onError: (error: { error: Error }) => {
    console.error('ChatKit error:', error.error)
  },

  /**
   * Handle response start
   */
  onResponseStart: () => {
    console.log('Assistant is responding...')
  },

  /**
   * Handle response end
   */
  onResponseEnd: () => {
    console.log('Assistant response complete')
  },

  /**
   * Handle thread changes
   */
  onThreadChange: (event: { threadId: string | null }) => {
    console.log('Thread changed:', event.threadId)
    // Update local state with current thread ID
    if (event.threadId) {
      localStorage.setItem('chatkit_thread_id', event.threadId)
    }
  },

  /**
   * Handle effect (tool calls, widget actions)
   * Logged for debugging purposes
   */
  // onEffect handler commented out to avoid type issues
  // Effects are automatically handled by the ChatKit SDK
}

/**
 * Get the current ChatKit thread ID from localStorage
 */
export function getChatKitThreadId(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('chatkit_thread_id')
}

/**
 * Clear ChatKit thread from localStorage
 */
export function clearChatKitThread(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem('chatkit_thread_id')
}

/**
 * Verify ChatKit is properly configured
 */
export function validateChatKitConfig(): {
  valid: boolean
  errors: string[]
} {
  const errors: string[] = []

  if (!API_BASE_URL) {
    errors.push('NEXT_PUBLIC_API_URL is not configured')
  }

  if (!API_URL) {
    errors.push('ChatKit endpoint URL could not be constructed')
  }

  // Domain public key required for production
  if (!DOMAIN_PUBLIC_KEY || typeof DOMAIN_PUBLIC_KEY !== 'string') {
    errors.push('NEXT_PUBLIC_DOMAIN_PUBLIC_KEY is not configured (register domain at https://platform.openai.com/settings/organization/security/domain-allowlist)')
  }

  // DOMAIN_KEY just needs to exist and be a string
  // The default value is acceptable for local development
  if (!DOMAIN_KEY || typeof DOMAIN_KEY !== 'string') {
    errors.push('NEXT_PUBLIC_DOMAIN_KEY is not properly configured')
  }

  // OpenAI API key is optional - backend handles it
  // But warn if not present
  if (!OPENAI_API_KEY) {
    console.warn('NEXT_PUBLIC_OPENAI_API_KEY is not configured - backend will use server-side key')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}
