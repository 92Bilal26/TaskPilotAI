/**
 * ChatKit Widget Component
 *
 * Wrapper component for OpenAI ChatKit integration.
 * Handles initialization, authentication, state management, and conversation history.
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useChatKit, ChatKit } from '@openai/chatkit-react'
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
 * ChatKitWidget Component
 *
 * Provides a ready-to-use ChatKit integration with:
 * - JWT authentication from Better Auth
 * - Session management and conversation persistence
 * - Error handling and loading states
 * - Customizable header and navigation
 */
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
  let token = localStorage.getItem('auth_token')
  if (token) return token
  token = localStorage.getItem('authjs.session-token')
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

  // Early return if not authenticated to avoid hook violations
  if (!isAuthenticated && !authLoading) {
    return null
  }

  // Call hook at top level (must be done before any conditional returns)
  let chatKitResult
  try {
    chatKitResult = useChatKit(chatKitConfig)
  } catch (e: any) {
    console.error('ChatKit hook error:', e)
  }

  // Initialize: Extract user ID and load conversation history
  useEffect(() => {
    setIsMounted(true)
    console.log('ChatKitWidget mounted with config:', chatKitConfig)

    const validation = validateChatKitConfig()
    if (!validation.valid) {
      setError(
        `ChatKit configuration error: ${validation.errors.join(', ')}`
      )
      return
    }

    // Extract user ID from JWT token
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
      // Load conversation history
      loadConversationHistory(extractedUserId, convId, token)
    }
  }, [propConversationId])

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
            ChatKit Configuration Error
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

  // ChatKit not initialized
  if (!chatKitResult) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center max-w-md">
          <p className="text-gray-600 mb-4">Initializing ChatKit...</p>
          <p className="text-xs text-gray-500">
            Please wait while we set up your chat session
          </p>
        </div>
      </div>
    )
  }

  const { control } = chatKitResult

  return (
    <div
      className="flex flex-col h-screen bg-white"
      style={{ overflow: 'hidden' }}
    >
      {/* Header */}
      {showHeader && (
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 shadow-md flex items-center justify-between flex-shrink-0">
          <div className="flex-1">
            <h1 className="text-2xl font-bold">{title}</h1>
            <p className="text-blue-100 text-sm">{subtitle}</p>
            {conversationHistory.length > 0 && (
              <p className="text-blue-100 text-xs mt-1">
                Loaded {conversationHistory.length} previous message(s)
              </p>
            )}
            {loadingHistory && (
              <p className="text-blue-100 text-xs mt-1">Loading conversation history...</p>
            )}
            {historyError && (
              <p className="text-blue-200 text-xs mt-1">⚠️ {historyError}</p>
            )}
          </div>

          {/* Conversation Switcher Button (T021) */}
          <div className="ml-4 relative">
            <button
              onClick={() => {
                setShowConversationList(!showConversationList)
                if (!showConversationList && userId) {
                  const token = getAuthToken()
                  loadConversations(userId, token)
                }
              }}
              className="px-3 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium text-sm mr-2"
              title="Switch conversation"
            >
              💬 {conversations.length}
            </button>

            {/* Conversation List Dropdown (T021) */}
            {showConversationList && (
              <div className="absolute top-full right-0 mt-2 bg-white text-gray-800 rounded-lg shadow-lg z-10 min-w-max max-h-64 overflow-y-auto">
                {loadingConversations ? (
                  <div className="px-4 py-3 text-center text-sm text-gray-500">
                    Loading...
                  </div>
                ) : conversations.length === 0 ? (
                  <div className="px-4 py-3 text-sm text-gray-500">
                    No conversations yet
                  </div>
                ) : (
                  conversations.map((conv) => (
                    <button
                      key={conv.id}
                      onClick={() => switchConversation(conv.id, getAuthToken())}
                      className={`block w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors border-b last:border-b-0 ${
                        conversationId === conv.id
                          ? 'bg-blue-50 font-semibold text-blue-600'
                          : ''
                      }`}
                    >
                      <div className="font-medium text-sm">{conv.title}</div>
                      <div className="text-xs text-gray-500">
                        {conv.message_count} messages
                      </div>
                    </button>
                  ))
                )}
              </div>
            )}
          </div>

          {showBackButton && (
            <button
              onClick={() => router.push(backRoute)}
              className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
              aria-label="Go back"
            >
              Back
            </button>
          )}
        </div>
      )}

      {/* ChatKit Component - Full Height */}
      <div
        className="flex-1 overflow-hidden"
        style={{ display: 'flex', flexDirection: 'column', width: '100%' }}
      >
        {isMounted && control && (
          <ChatKit
            control={control}
            style={{
              width: '100%',
              height: '100%',
              flex: 1,
            }}
          />
        )}
      </div>
    </div>
  )
}

export default ChatKitWidget
