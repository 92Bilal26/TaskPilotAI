/**
 * ChatKit Page
 *
 * Integrates OpenAI's ChatKit React component for AI task management
 * Uses the official @openai/chatkit-react package
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useChatKit, ChatKit } from '@openai/chatkit-react'
import { chatKitConfig, validateChatKitConfig } from '@/lib/chatkit-config'
import { useAuth } from '@/lib/useAuth'

export default function ChatKitPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [isMounted, setIsMounted] = useState(false)

  // Early return if not authenticated to avoid hook violations
  if (!isAuthenticated && !isLoading) {
    return null
  }

  // Call hook at top level (must be done before any conditional returns)
  let chatKitResult
  try {
    chatKitResult = useChatKit(chatKitConfig)
    console.log('useChatKit result:', chatKitResult)
  } catch (e: any) {
    console.error('ChatKit hook error:', e)
  }

  // Validate ChatKit configuration and set mounted state
  useEffect(() => {
    setIsMounted(true)
    console.log('ChatKit page mounted, config:', chatKitConfig)

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
            ChatKit Configuration Error
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

  if (!chatKitResult) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="text-center max-w-md">
          <p className="text-gray-600 mb-4">Initializing ChatKit...</p>
          <p className="text-xs text-gray-500">Check console for details</p>
        </div>
      </div>
    )
  }

  const { control } = chatKitResult

  return (
    <div className="flex flex-col h-screen bg-white" style={{ overflow: 'hidden' }}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 shadow-md flex items-center justify-between flex-shrink-0">
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

      {/* ChatKit Component - Full Height */}
      <div className="flex-1 overflow-hidden" style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
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
