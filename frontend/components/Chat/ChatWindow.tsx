'use client'

/**
 * ChatWindow Component - ChatKit Integration
 *
 * Integrates OpenAI's ChatKit React component for the chatbot interface.
 * Provides a professional chat UI powered by OpenAI's ChatKit.
 */

import { useEffect } from 'react'
import { ChatKit, useChatKit } from '@openai/chatkit-react'

interface ChatWindowProps {
  conversationId?: number
  userId: string
  authToken: string
}

/**
 * ChatKit requires the @openai/chatkit-react package
 * It's a pre-built chat UI component from OpenAI
 *
 * Configuration:
 * 1. API Config: Custom endpoint with authorization
 * 2. Theme: Blue color scheme
 * 3. Locale: English
 */

export function ChatWindow({
  conversationId,
  userId,
  authToken,
}: ChatWindowProps) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const endpoint = `${apiUrl}/api/${userId}/chat`

  // Initialize ChatKit with custom backend endpoint
  const chatKitControl = useChatKit({
    api: {
      type: 'custom',
      url: endpoint,
      headers: () => ({
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json',
      }),
    },
    theme: {
      colorScheme: 'light',
      primaryColor: '#2563eb',
      secondaryColor: '#1f2937',
    },
    locale: 'en',
    initialThread: null,
  })

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900">
          TaskPilot AI Chatbot
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          Powered by OpenAI ChatKit - Chat with AI to manage your tasks
        </p>
      </div>

      {/* ChatKit Component - Active */}
      <div className="flex-1 overflow-hidden">
        <ChatKit control={chatKitControl.control} />
      </div>
    </div>
  )
}
