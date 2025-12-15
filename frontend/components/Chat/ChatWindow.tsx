'use client'

/**
 * ChatWindow Component - ChatKit Integration
 *
 * Wraps OpenAI's ChatKit React component for the chatbot interface.
 * Handles message sending, conversation management, and error handling.
 */

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { chatClient } from '@/lib/chat-client'

interface ChatWindowProps {
  conversationId?: number
  userId: string
  authToken: string
}

interface Message {
  id?: string
  role: 'user' | 'assistant'
  content: string
}

export function ChatWindow({
  conversationId,
  userId,
  authToken,
}: ChatWindowProps) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(
    conversationId || null
  )
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  /**
   * Handle message submission
   * @param message - User's message text
   */
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return

    setIsLoading(true)
    setError(null)

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
    }
    setMessages(prev => [...prev, userMessage])

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

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: response.message_id?.toString() || Date.now().toString(),
        role: 'assistant',
        content: response.response,
      }
      setMessages(prev => [...prev, assistantMessage])

      // Log tool calls for debugging
      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log('Tool calls executed:', response.tool_calls)
      }

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
      // Silently fail - conversations list is optional
      // The user can still send messages and create new conversations
      console.debug('Could not load conversations list (this is ok):', err)
    }
  }

  // Load initial data
  useEffect(() => {
    // Don't load conversations on mount for test chatbot
    // The test token doesn't have any existing conversations
    // Conversations will be created when user sends first message
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

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4">
        {messages.length === 0 && (
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <p className="text-gray-600 font-medium mb-2">
              👋 Welcome! I'm your AI task assistant. You can:
            </p>
            <ul className="space-y-2 text-sm text-gray-600 list-disc list-inside">
              <li>Say <code className="bg-gray-100 px-2 py-1 rounded">"add a task to buy groceries"</code></li>
              <li>Ask <code className="bg-gray-100 px-2 py-1 rounded">"show me my pending tasks"</code></li>
              <li>Say <code className="bg-gray-100 px-2 py-1 rounded">"mark task 1 as done"</code></li>
              <li>Ask <code className="bg-gray-100 px-2 py-1 rounded">"delete the groceries task"</code></li>
            </ul>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md rounded-lg p-4 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white text-gray-900 border border-gray-200 rounded-bl-none'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-900 border border-gray-200 rounded-lg rounded-bl-none p-4">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
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
    </div>
  )
}
