'use client'

/**
 * Chatbot Page - Main Chat Interface
 *
 * Provides the main chatbot interface for users to interact with AI-powered task management.
 * Includes authentication check and conversation management.
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ChatWindow } from '@/components/Chat/ChatWindow'

export default function ChatbotPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [authToken, setAuthToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Get user ID and auth token from local storage or session
    // In a real app, this would come from your auth provider (Better Auth, etc.)
    const storedUserId = localStorage.getItem('userId')
    const storedToken = localStorage.getItem('authToken')

    if (!storedUserId || !storedToken) {
      // Redirect to login if not authenticated
      router.push('/auth/signin')
      return
    }

    setUserId(storedUserId)
    setAuthToken(storedToken)
    setIsLoading(false)
  }, [router])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading chatbot...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium mb-4">{error}</p>
          <button
            onClick={() => router.push('/auth/signin')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go to Login
          </button>
        </div>
      </div>
    )
  }

  if (!userId || !authToken) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-gray-600 mb-4">Authenticating...</p>
          <button
            onClick={() => router.push('/auth/signin')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go to Login
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">TaskPilot AI</h1>
              <p className="text-sm text-gray-600 mt-1">
                Chat-based task management powered by AI
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">User ID</p>
                <p className="text-sm font-medium text-gray-900 truncate max-w-xs">
                  {userId}
                </p>
              </div>
              <button
                onClick={() => {
                  localStorage.removeItem('userId')
                  localStorage.removeItem('authToken')
                  router.push('/auth/signin')
                }}
                className="px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <div className="h-full flex gap-4 p-4">
          {/* Sidebar - Conversations List */}
          <aside className="w-64 bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden flex flex-col">
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-sm font-semibold text-gray-900">Conversations</h2>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {/* Conversations will be loaded here */}
              <p className="text-sm text-gray-600 text-center py-8">
                Start a new conversation to see it here
              </p>
            </div>
            <div className="p-4 border-t border-gray-200">
              <button
                onClick={() => {
                  // Clear conversation and start new one
                  window.location.reload()
                }}
                className="w-full px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700"
              >
                New Chat
              </button>
            </div>
          </aside>

          {/* Chat Window */}
          <div className="flex-1 bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <ChatWindow
              userId={userId}
              authToken={authToken}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-4 py-3">
        <div className="max-w-7xl mx-auto text-sm text-gray-600 text-center">
          <p>
            💡 Tip: Try saying "Add a task to buy groceries" or "Show my pending
            tasks"
          </p>
        </div>
      </footer>
    </div>
  )
}
