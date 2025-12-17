/**
 * ChatKit Page
 *
 * Integrates OpenAI's ChatKit component for AI task management
 * Features:
 * - Thread-based conversation management
 * - Multi-turn AI interactions
 * - Task management through natural language
 * - Conversation history
 */

'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useChatKit } from '@openai/chatkit-react'
import ChatKit from '@openai/chatkit-react/dist/index.d.ts'
import { chatKitConfig, validateChatKitConfig } from '@/lib/chatkit-config'
import { useAuth } from '@/lib/useAuth'

export default function ChatKitPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()
  const { control, ref } = useChatKit(chatKitConfig)
  const [error, setError] = useState<string | null>(null)

  // Check authentication
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/signin')
    }
  }, [isAuthenticated, isLoading, router])

  // Validate ChatKit configuration
  useEffect(() => {
    const validation = validateChatKitConfig()
    if (!validation.valid) {
      setError(
        `ChatKit configuration error: ${validation.errors.join(', ')}`
      )
    }
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading ChatKit...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center max-w-md">
          <div className="text-red-600 text-lg font-semibold mb-2">
            Configuration Error
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 shadow-md flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">TaskPilot AI Chat</h1>
          <p className="text-blue-100 text-sm">Powered by OpenAI ChatKit</p>
        </div>
        <button
          onClick={() => router.push('/dashboard')}
          className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-medium"
        >
          Back to Dashboard
        </button>
      </div>

      {/* ChatKit Component */}
      <div className="flex-1 overflow-hidden">
        <div className="w-full h-full">
          <openai-chatkit
            ref={ref}
            style={{
              width: '100%',
              height: '100%',
            }}
          />
        </div>
      </div>
    </div>
  )
}
