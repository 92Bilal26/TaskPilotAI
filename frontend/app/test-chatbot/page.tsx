'use client'

/**
 * Test Chatbot Page - For Local Development
 *
 * Simple chatbot page without authentication requirement
 * Use this to test the chatbot locally
 */

import { useState } from 'react'
import { ChatWindow } from '@/components/Chat/ChatWindow'

export default function TestChatbotPage() {
  // Test user ID - consistent for testing
  const testUserId = 'test-user-demo'
  // For development, we use a test token in format: test-token-{user_id}
  // Backend will extract the user_id from this token when in development mode
  // In production, this would be a real JWT token
  const testToken = 'test-token-test-user-demo'

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">TaskPilot AI 🤖</h1>
              <p className="text-blue-100 mt-1">
                Chat-based task management powered by AI (Test Mode)
              </p>
            </div>
            <div className="bg-white bg-opacity-20 px-4 py-2 rounded-lg">
              <p className="text-sm font-medium">Test User</p>
              <p className="text-xs text-blue-100 truncate">{testUserId}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <div className="h-full flex gap-4 p-4 max-w-7xl mx-auto w-full">
          {/* Sidebar - Instructions */}
          <aside className="w-64 bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden flex flex-col">
            <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
              <h2 className="text-sm font-bold text-gray-900">💡 How to Use</h2>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm text-gray-700">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Add Tasks</h3>
                <p className="text-xs text-gray-600">
                  Try: "Add a task to buy groceries"
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">View Tasks</h3>
                <p className="text-xs text-gray-600">
                  Try: "Show me my pending tasks"
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Complete Tasks</h3>
                <p className="text-xs text-gray-600">
                  Try: "Mark task 1 as done"
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Delete Tasks</h3>
                <p className="text-xs text-gray-600">
                  Try: "Delete the groceries task"
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Update Tasks</h3>
                <p className="text-xs text-gray-600">
                  Try: "Change task 1 title to shopping list"
                </p>
              </div>

              <div className="pt-4 border-t border-gray-200 mt-4">
                <h3 className="font-semibold text-gray-900 mb-2">ℹ️ Backend Setup</h3>
                <p className="text-xs text-gray-600">
                  Make sure the backend is running:
                </p>
                <code className="text-xs bg-gray-100 p-2 rounded block mt-2 text-gray-800">
                  uvicorn main:app --reload
                </code>
              </div>

              <div className="pt-4 border-t border-gray-200 mt-4">
                <h3 className="font-semibold text-gray-900 mb-2">🔧 API Endpoint</h3>
                <code className="text-xs bg-gray-100 p-2 rounded block text-gray-800">
                  POST /api/{'{user_id}'}/chat
                </code>
              </div>
            </div>
          </aside>

          {/* Chat Window */}
          <div className="flex-1 bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden flex flex-col">
            <ChatWindow
              userId={testUserId}
              authToken={testToken}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 px-4 py-4 text-center text-sm">
        <p>
          🚀 TaskPilotAI Phase 3 - AI-Powered Todo Chatbot with OpenAI Integration
        </p>
      </footer>
    </div>
  )
}
