'use client'

/**
 * ChatWindow Component - ChatKit Integration
 *
 * Integrates OpenAI's ChatKit React component for the chatbot interface.
 * Provides a professional chat UI powered by OpenAI's ChatKit.
 */

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'

// Dynamic import for ChatKit to handle SSR
const ChatKit = dynamic(
  () => import('@openai/chatkit-react').then(mod => ({ default: mod.ChatKit })),
  {
    loading: () => <div className="flex items-center justify-center h-full">Loading ChatKit...</div>,
    ssr: false
  }
)

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
 * 1. API Key: Your OpenAI API key (loaded from env or props)
 * 2. Endpoint: Your backend chat endpoint
 * 3. Headers: Authorization header with your token
 * 4. User ID: For tracking conversations
 */

export function ChatWindow({
  conversationId,
  userId,
  authToken,
}: ChatWindowProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [apiKey, setApiKey] = useState<string>('')

  useEffect(() => {
    // Get OpenAI API key from environment
    const key = process.env.NEXT_PUBLIC_OPENAI_API_KEY || ''
    setApiKey(key)
  }, [])

  // ChatKit Configuration
  const chatKitConfig = {
    endpoint: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/${userId}/chat`,
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
    apiKey: apiKey,
  }

  if (!apiKey) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-red-600 font-medium mb-4">
            OpenAI API key not configured
          </p>
          <p className="text-gray-600 text-sm">
            Please set NEXT_PUBLIC_OPENAI_API_KEY in your .env.local file
          </p>
        </div>
      </div>
    )
  }

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
        <ChatKit
          apiKey={apiKey}
          endpoint={chatKitConfig.endpoint}
          headers={chatKitConfig.headers}
          initialMessages={[
            {
              id: 'welcome',
              role: 'assistant',
              content: 'Welcome! I\'m your AI task assistant. You can ask me to:\n• Add tasks: "Add a task to buy groceries"\n• List tasks: "Show my pending tasks"\n• Complete tasks: "Mark task 1 as done"\n• Update tasks: "Change task 1 to shopping list"\n• Delete tasks: "Delete task 1"',
              created_at: new Date().toISOString(),
            }
          ]}
          onError={(error: Error) => console.error('ChatKit error:', error)}
          theme={{
            primary: '#2563eb',
            secondary: '#1f2937',
          }}
        />
      </div>
    </div>
  )
}
