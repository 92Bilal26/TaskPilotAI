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

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { chatKitConfig, validateChatKitConfig } from '@/lib/chatkit-config'
import { useAuth } from '@/lib/useAuth'

// Type declaration for ChatKit window object
declare global {
  interface Window {
    OpenAIChatKit?: {
      default?: any
    }
  }
}

export default function ChatKitPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

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

  // Initialize ChatKit after mounting
  useEffect(() => {
    setMounted(true)
  }, [])

  // Load and initialize ChatKit
  useEffect(() => {
    if (!mounted || error || !isAuthenticated) return

    const initChatKit = async () => {
      try {
        // Wait for ChatKit script to load
        let attempts = 0
        const maxAttempts = 50

        while (!window.OpenAIChatKit && attempts < maxAttempts) {
          await new Promise(resolve => setTimeout(resolve, 100))
          attempts++
        }

        if (!window.OpenAIChatKit) {
          setError('ChatKit library failed to load. Please refresh the page.')
          return
        }

        // Initialize ChatKit
        const container = document.getElementById('chatkit-container')
        if (!container) {
          setError('ChatKit container not found')
          return
        }

        // Create ChatKit instance directly in the container
        const chatKitElement = document.createElement('openai-chatkit')

        // Set attributes
        chatKitElement.setAttribute('style', 'width: 100%; height: 100%; display: block;')

        // Set options through attributes
        Object.entries(chatKitConfig.api).forEach(([key, value]) => {
          if (typeof value === 'string') {
            chatKitElement.setAttribute(`data-api-${key}`, value)
          }
        })

        container.appendChild(chatKitElement)

      } catch (err) {
        console.error('Error initializing ChatKit:', err)
        setError(`Failed to initialize ChatKit: ${String(err)}`)
      }
    }

    initChatKit()
  }, [mounted, error, isAuthenticated])

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
            ChatKit Error
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

      {/* ChatKit Container */}
      <div className="flex-1 overflow-hidden" id="chatkit-container">
        {/* ChatKit web component will be injected here */}
      </div>
    </div>
  )
}
