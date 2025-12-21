'use client'

import { useEffect } from 'react'

export default function ChatKitTest() {
  useEffect(() => {
    console.log('Test page mounted')
    console.log('Window keys with "chat":', Object.keys(window).filter(k => k.toLowerCase().includes('chat')))
    console.log('window.ChatKit:', (window as any).ChatKit)
    console.log('All global window objects:', Object.getOwnPropertyNames(window).slice(0, 50))
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">ChatKit Test Page</h1>
      <p className="text-gray-600 mb-4">This is a test page to verify ChatKit integration</p>
      <p className="text-sm text-gray-500">Check console for ChatKit detection</p>
      <div className="mt-6 p-4 bg-gray-100 rounded">
        <p className="text-xs">Look for window.ChatKit or any ChatKit-related objects in console</p>
      </div>
    </div>
  )
}
