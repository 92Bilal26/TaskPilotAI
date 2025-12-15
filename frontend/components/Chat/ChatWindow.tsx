'use client'

/**
 * ChatWindow Component - ChatKit Integration
 *
 * Wraps OpenAI's ChatKit React component for the chatbot interface.
 * Handles message sending, conversation management, and error handling.
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { chatClient } from '@/lib/chat-client'

interface ChatWindowProps {
  conversationId?: number
  userId: string
  authToken: string
}

export function ChatWindow({
  conversationId,
  userId,
  authToken,
}: ChatWindowProps) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(
    conversationId || null
  )

  /**
   * Handle message submission
   * @param message - User's message text
   */
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      // Send message to chat endpoint
      const response = await chatClient.sendMessage(
        userId,
        {
          content: message,
          conversation_id: currentConversationId || undefined,
        },
        authToken
      )

      // Update conversation ID if new conversation was created
      if (!currentConversationId && response.conversation_id) {
        setCurrentConversationId(response.conversation_id)
      }

      // Log tool calls for debugging
      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log('Tool calls executed:', response.tool_calls)
      }

      // Display assistant response
      console.log('Assistant:', response.response)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message'
      setError(errorMessage)
      console.error('Chat error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Load conversation history
   */
  const loadConversationHistory = async () => {
    if (!currentConversationId) return

    try {
      const response = await chatClient.getConversation(
        userId,
        currentConversationId,
        authToken
      )

      console.log('Loaded conversation:', response)
    } catch (err) {
      console.error('Failed to load conversation:', err)
    }
  }

  /**
   * Load conversations list
   */
  const loadConversations = async () => {
    try {
      const conversations = await chatClient.listConversations(userId, authToken)
      console.log('Conversations:', conversations)
    } catch (err) {
      console.error('Failed to load conversations:', err)
    }
  }

  // Load initial data
  useEffect(() => {
    loadConversations()
    if (currentConversationId) {
      loadConversationHistory()
    }
  }, [userId, authToken])

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900">
          TaskPilot AI Chatbot
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          Chat with AI to manage your tasks
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 m-4 rounded">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Chat Area - Will be replaced with ChatKit component */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        <div className="space-y-4">
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <p className="text-gray-600">
              Welcome! I'm your AI task assistant. You can:
            </p>
            <ul className="mt-2 space-y-1 text-sm text-gray-600 list-disc list-inside">
              <li>Say "add a task to buy groceries"</li>
              <li>Ask "show me my pending tasks"</li>
              <li>Say "mark task 1 as done"</li>
              <li>Ask "delete the groceries task"</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Type a message..."
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !isLoading) {
                handleSendMessage(e.currentTarget.value)
                e.currentTarget.value = ''
              }
            }}
            disabled={isLoading}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 disabled:bg-gray-100"
          />
          <button
            onClick={(e) => {
              const input = e.currentTarget.previousElementSibling as HTMLInputElement
              if (input && !isLoading) {
                handleSendMessage(input.value)
                input.value = ''
              }
            }}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="border-t border-gray-200 bg-gray-50 px-4 py-2 text-center text-sm text-gray-600">
          Processing message...
        </div>
      )}
    </div>
  )
}
