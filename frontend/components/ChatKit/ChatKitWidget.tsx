/**
 * ChatKit Widget Component
 *
 * Wrapper component for OpenAI ChatKit integration using React hook pattern.
 * Uses the official ChatKit React package with custom backend configuration.
 * Handles authentication and conversation state.
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ChatKit, useChatKit } from '@openai/chatkit-react'
import { chatKitConfig, validateChatKitConfig } from '@/lib/chatkit-config'
import { useAuth } from '@/lib/useAuth'
import { chatClient } from '@/lib/chat-client'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  tool_calls?: any[]
  created_at: string
}

interface ConversationDetail {
  id: number
  title: string
  created_at: string
  updated_at: string
  messages: ChatMessage[]
}

interface ChatKitWidgetProps {
  /**
   * Show header with back button
   * @default true
   */
  showHeader?: boolean

  /**
   * Custom title for the header
   * @default 'TaskPilot AI Chat'
   */
  title?: string

  /**
   * Custom subtitle for the header
   * @default 'Powered by OpenAI ChatKit'
   */
  subtitle?: string

  /**
   * Show back button
   * @default true
   */
  showBackButton?: boolean

  /**
   * Route to navigate to when back button is clicked
   * @default '/dashboard'
   */
  backRoute?: string

  /**
   * Conversation ID to load history for
   * If not provided, will try to load from sessionStorage or create new
   * @optional
   */
  conversationId?: number
}

/**
 * Extract user ID from JWT token
 */
function extractUserIdFromToken(token: string | null): string | null {
  if (!token) return null
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null
    const decoded = JSON.parse(atob(parts[1]))
    return decoded.user_id || decoded.sub || null
  } catch (e) {
    console.error('Failed to decode JWT:', e)
    return null
  }
}

/**
 * Get JWT token from storage
 */
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null
  let token = localStorage.getItem('access_token')
  if (token) return token
  token = localStorage.getItem('auth_token')
  if (token) return token
  token = localStorage.getItem('authjs.session-token')
  if (token) return token
  token = sessionStorage.getItem('access_token')
  if (token) return token
  token = sessionStorage.getItem('auth_token')
  return token
}

export function ChatKitWidget({
  showHeader = true,
  title = 'TaskPilot AI Chat',
  subtitle = 'Powered by OpenAI ChatKit',
  showBackButton = true,
  backRoute = '/dashboard',
  conversationId: propConversationId,
}: ChatKitWidgetProps) {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const [isMountedClient, setIsMountedClient] = useState(false)

  // Only render on client side to prevent server-side rendering issues
  useEffect(() => {
    setIsMountedClient(true)
  }, [])

  // IMPORTANT: All hooks must be called unconditionally before any conditional returns
  // This hook must be called every render to comply with React's Rules of Hooks
  const chatkit = useChatKit(chatKitConfig)

  const [error, setError] = useState<string | null>(null)
  const [isMounted, setIsMounted] = useState(false)

  // Conversation history state
  const [conversationId, setConversationId] = useState<number | null>(propConversationId || null)
  const [conversationHistory, setConversationHistory] = useState<ChatMessage[]>([])
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [historyError, setHistoryError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)

  // Conversation switcher state (T021)
  const [conversations, setConversations] = useState<Array<{
    id: number
    title: string
    message_count: number
    created_at: string
    updated_at: string
  }>>([])
  const [showConversationList, setShowConversationList] = useState(false)
  const [loadingConversations, setLoadingConversations] = useState(false)

  // Initialize ChatKit using the React hook
  useEffect(() => {
    if (!isAuthenticated || authLoading) {
      return
    }

    setIsMounted(true)
    console.log('ChatKitWidget mounting with React hook configuration')

    const validation = validateChatKitConfig()
    if (!validation.valid) {
      setError(
        `ChatKit configuration error: ${validation.errors.join(', ')}`
      )
      return
    }

    // Extract user ID from JWT token for conversation history loading
    const token = getAuthToken()
    const extractedUserId = extractUserIdFromToken(token)
    if (!extractedUserId) {
      setError('Failed to authenticate: No user ID found in token')
      return
    }
    setUserId(extractedUserId)

    // Try to load conversation from sessionStorage or use provided prop
    let convId = propConversationId
    if (!convId && typeof window !== 'undefined') {
      const storedConvId = sessionStorage.getItem('chatkit_conversation_id')
      if (storedConvId) {
        convId = parseInt(storedConvId, 10)
      }
    }

    if (convId) {
      setConversationId(convId)
      loadConversationHistory(extractedUserId, convId, token)
    }
  }, [isAuthenticated, authLoading, propConversationId])

  // Load conversation history from backend
  async function loadConversationHistory(
    userId: string,
    convId: number,
    authToken: string | null
  ) {
    if (!authToken) {
      setHistoryError('No authentication token available')
      return
    }

    setLoadingHistory(true)
    try {
      const history = await chatClient.getConversation(userId, convId, authToken)
      setConversationHistory(history.messages || [])
      console.log(`Loaded ${history.messages?.length || 0} messages for conversation ${convId}`)
    } catch (err) {
      console.error('Failed to load conversation history:', err)
      setHistoryError(err instanceof Error ? err.message : 'Failed to load conversation history')
      // Don't block ChatKit initialization if history loading fails
    } finally {
      setLoadingHistory(false)
    }
  }

  // Load list of conversations for switcher (T021)
  async function loadConversations(
    userId: string,
    authToken: string | null
  ) {
    if (!authToken) return

    setLoadingConversations(true)
    try {
      const convList = await chatClient.listConversations(userId, authToken)
      setConversations(convList || [])
      console.log(`Loaded ${convList?.length || 0} conversations`)
    } catch (err) {
      console.error('Failed to load conversations:', err)
      // Silently fail - this is not critical
    } finally {
      setLoadingConversations(false)
    }
  }

  // Switch to a different conversation (T021)
  async function switchConversation(
    convId: number,
    authToken: string | null
  ) {
    setConversationId(convId)
    setShowConversationList(false)
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('chatkit_conversation_id', String(convId))
    }
    if (userId) {
      await loadConversationHistory(userId, convId, authToken)
    }
  }

  // Don't render on server side
  if (!isMountedClient) {
    return null
  }

  // Loading state
  if (authLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading ChatKit...</p>
        </div>
      </div>
    )
  }

  // Not authenticated
  if (!isAuthenticated) {
    return null
  }

  // Configuration error
  if (error) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center max-w-md">
          <div className="text-red-600 text-lg font-semibold mb-2">
            ChatKit Error
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push(backRoute)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  // Render ChatKit component
  return (
    <div
      className="flex flex-col h-screen bg-white"
      style={{ overflow: 'hidden' }}
    >
      {/* ChatKit Component initialized via hook */}
      <ChatKit control={chatkit.control} />
    </div>
  )
}

export default ChatKitWidget
