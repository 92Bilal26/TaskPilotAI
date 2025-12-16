'use client'

/**
 * Chat Modal Component - For Dashboard Integration
 *
 * Displays chat interface in a modal overlay
 * Allows users to interact with AI chatbot while managing tasks
 */

import { useState, useEffect } from 'react'
import { ChatWindow } from './ChatWindow'

interface ChatModalProps {
  isOpen: boolean
  onClose: () => void
  userId: string
  authToken: string
}

export function ChatModal({
  isOpen,
  onClose,
  userId,
  authToken,
}: ChatModalProps) {
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted || !isOpen) {
    return null
  }

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
        aria-label="Close chat modal"
      />

      {/* Modal Container */}
      <div className="fixed bottom-4 right-4 w-96 h-[600px] bg-white rounded-lg shadow-2xl z-50 flex flex-col overflow-hidden md:bottom-6 md:right-6 md:w-full md:max-w-md">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-4 py-3 flex items-center justify-between">
          <h3 className="text-lg font-semibold">TaskPilot AI Chat</h3>
          <button
            onClick={onClose}
            className="text-white hover:bg-blue-800 p-1 rounded transition-colors"
            aria-label="Close chat"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Chat Content */}
        <div className="flex-1 overflow-hidden">
          <ChatWindow
            userId={userId}
            authToken={authToken}
          />
        </div>
      </div>
    </>
  )
}
