/**
 * ChatKit Configuration
 *
 * Configuration for OpenAI ChatKit integration
 * Handles API endpoints, authentication, and UI customization
 */

import type { UseChatKitOptions } from '@openai/chatkit-react'

// Get environment variables
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const OPENAI_API_KEY = process.env.NEXT_PUBLIC_OPENAI_API_KEY || ''

// Domain key for ChatKit verification (required)
// This should be a unique identifier for your domain
// Default is acceptable for local development and testing
const DOMAIN_KEY = process.env.NEXT_PUBLIC_DOMAIN_KEY || 'taskpilot-local-dev'

/**
 * Get JWT token from Better Auth
 * Tries multiple locations where token might be stored
 */
function getAuthToken(): string | null {
  // Try localStorage first (standard)
  let token = localStorage.getItem('auth_token')
  if (token) return token

  // Try the auth-token key (Better Auth)
  token = localStorage.getItem('authjs.session-token')
  if (token) return token

  // Try sessionStorage
  token = sessionStorage.getItem('auth_token')
  if (token) return token

  return null
}

/**
 * Custom fetch function that adds JWT authentication
 */
async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  // Get JWT token
  const token = getAuthToken()

  // Build headers
  const headers = new Headers(options.headers || {})

  // Add JWT token if available
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  // Add domain key for ChatKit verification
  headers.set('X-ChatKit-Domain-Key', DOMAIN_KEY)

  // Return fetch with updated options
  return fetch(url, {
    ...options,
    headers,
  })
}

/**
 * ChatKit Configuration
 *
 * This configuration integrates OpenAI ChatKit with your backend
 */
export const chatKitConfig: UseChatKitOptions = {
  // ============================================
  // API Configuration (REQUIRED)
  // ============================================
  api: {
    /**
     * Get client secret from backend session endpoint
     * Frontend calls: POST /api/v1/chatkit/sessions (with JWT auth)
     * Backend returns: { client_secret: "...", session_id: "...", conversation_id: ... }
     */
    async getClientSecret(existing) {
      // If we already have a secret, reuse it
      if (existing) {
        console.log('Reusing existing ChatKit client secret')
        return existing
      }

      try {
        // Call backend session endpoint with JWT authentication
        const res = await authenticatedFetch(`${API_URL}/api/v1/chatkit/sessions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (!res.ok) {
          const errorData = await res.json().catch(() => ({}))
          throw new Error(`Failed to get ChatKit session: ${res.statusText} - ${JSON.stringify(errorData)}`)
        }

        const data = await res.json()
        console.log('Got ChatKit session:', {
          session_id: data.session_id,
          conversation_id: data.conversation_id,
        })

        // Store conversation ID for later use
        if (data.conversation_id) {
          sessionStorage.setItem('chatkit_conversation_id', String(data.conversation_id))
        }

        return data.client_secret
      } catch (error) {
        console.error('Error getting ChatKit session:', error)
        throw error
      }
    },
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
  // Start Screen (New Conversation)
  // ============================================
  startScreen: {
    title: 'Welcome to TaskPilot AI',
    subtitle: 'Manage your tasks with AI assistance',
    quickStarters: [
      {
        title: 'Add a task',
        subtitle: 'Create a new task',
        prompt: 'Add a task to buy groceries',
      },
      {
        title: 'List my tasks',
        subtitle: 'View all tasks',
        prompt: 'Show me all my pending tasks',
      },
      {
        title: 'Complete a task',
        subtitle: 'Mark task as done',
        prompt: 'Mark my first task as complete',
      },
      {
        title: 'Delete a task',
        subtitle: 'Remove a task',
        prompt: 'Delete my grocery shopping task',
      },
    ],
  },

  // ============================================
  // Composer Configuration
  // ============================================
  composer: {
    placeholder: 'Ask me to add, update, or delete tasks...',
    autoFocus: true,
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

  if (!API_URL) {
    errors.push('NEXT_PUBLIC_API_URL is not configured')
  }

  // DOMAIN_KEY just needs to exist and be a string
  // The default value is acceptable for local development
  if (!DOMAIN_KEY || typeof DOMAIN_KEY !== 'string') {
    errors.push('NEXT_PUBLIC_DOMAIN_KEY is not properly configured')
  }

  // OpenAI API key is optional - backend handles it
  // But warn if not present
  if (!OPENAI_API_KEY) {
    console.warn('NEXT_PUBLIC_OPENAI_API_KEY is not configured')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}
