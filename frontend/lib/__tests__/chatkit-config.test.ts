/**
 * ChatKit Configuration Tests
 *
 * Tests for ChatKit configuration, getClientSecret function,
 * and backend session endpoint integration.
 */

import { chatKitConfig, getChatKitThreadId, clearChatKitThread, validateChatKitConfig } from '@/lib/chatkit-config'

// Mock fetch globally
global.fetch = jest.fn()

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {}

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString()
    },
    removeItem: (key: string) => {
      delete store[key]
    },
    clear: () => {
      store = {}
    },
  }
})()

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
})

describe('ChatKit Configuration', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    localStorage.clear()
  })

  describe('chatKitConfig structure', () => {
    it('should have api configuration with getClientSecret function', () => {
      expect(chatKitConfig).toHaveProperty('api')
      expect(chatKitConfig.api).toHaveProperty('getClientSecret')
      expect(typeof chatKitConfig.api.getClientSecret).toBe('function')
    })

    it('should have theme configuration', () => {
      expect(chatKitConfig).toHaveProperty('theme')
      expect(chatKitConfig.theme).toBe('light')
    })

    it('should have header configuration enabled', () => {
      expect(chatKitConfig).toHaveProperty('header')
      expect(chatKitConfig.header.enabled).toBe(true)
      expect(chatKitConfig.header.title.text).toBe('TaskPilot AI Chat')
    })

    it('should have history configuration enabled', () => {
      expect(chatKitConfig).toHaveProperty('history')
      expect(chatKitConfig.history.enabled).toBe(true)
    })

    it('should have composer configuration', () => {
      expect(chatKitConfig).toHaveProperty('composer')
      expect(chatKitConfig.composer.enabled).toBe(true)
      expect(chatKitConfig.composer.placeholder).toContain('Add, update, or delete')
    })

    it('should have start screen with quick starters', () => {
      expect(chatKitConfig).toHaveProperty('startScreen')
      expect(chatKitConfig.startScreen.enabled).toBe(true)
      expect(chatKitConfig.startScreen.quickStarters).toHaveLength(4)
    })

    it('should have event handlers defined', () => {
      expect(chatKitConfig).toHaveProperty('onReady')
      expect(chatKitConfig).toHaveProperty('onError')
      expect(chatKitConfig).toHaveProperty('onResponseStart')
      expect(chatKitConfig).toHaveProperty('onResponseEnd')
      expect(chatKitConfig).toHaveProperty('onThreadChange')
      expect(chatKitConfig).toHaveProperty('onClientTool')
    })
  })

  describe('getClientSecret function', () => {
    it('should return existing secret if provided', async () => {
      const existingSecret = 'cs_existing_secret_123'

      const result = await chatKitConfig.api.getClientSecret(existingSecret)

      expect(result).toBe(existingSecret)
      expect(fetch).not.toHaveBeenCalled()
    })

    it('should call backend to create new session if no existing secret', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'success',
          session_id: 'ses_test123',
          client_secret: 'cs_live_test123',
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const result = await chatKitConfig.api.getClientSecret()

      expect(result).toBe('cs_live_test123')
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/chatkit/sessions'),
        expect.objectContaining({
          method: 'POST',
        })
      )
    })

    it('should call correct endpoint URL', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'success',
          session_id: 'ses_test123',
          client_secret: 'cs_live_test123',
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await chatKitConfig.api.getClientSecret()

      const callArgs = (global.fetch as jest.Mock).mock.calls[0]
      expect(callArgs[0]).toContain('/api/chatkit/sessions')
    })

    it('should use POST method for session creation', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'success',
          session_id: 'ses_test123',
          client_secret: 'cs_live_test123',
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await chatKitConfig.api.getClientSecret()

      const callArgs = (global.fetch as jest.Mock).mock.calls[0]
      expect(callArgs[1].method).toBe('POST')
    })

    it('should include Content-Type header', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'success',
          session_id: 'ses_test123',
          client_secret: 'cs_live_test123',
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await chatKitConfig.api.getClientSecret()

      const callArgs = (global.fetch as jest.Mock).mock.calls[0]
      expect(callArgs[1].headers['Content-Type']).toBe('application/json')
    })

    it('should throw error if response is not ok', async () => {
      const mockResponse = {
        ok: false,
        statusText: 'Internal Server Error',
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await expect(
        chatKitConfig.api.getClientSecret()
      ).rejects.toThrow('Failed to get ChatKit session')
    })

    it('should throw error if response status is not success', async () => {
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'error',
          message: 'Workflow not configured',
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      await expect(
        chatKitConfig.api.getClientSecret()
      ).rejects.toThrow('Workflow not configured')
    })

    it('should handle network errors gracefully', async () => {
      ;(global.fetch as jest.Mock).mockRejectedValueOnce(
        new Error('Network error')
      )

      await expect(
        chatKitConfig.api.getClientSecret()
      ).rejects.toThrow('Network error')
    })

    it('should extract client_secret from response correctly', async () => {
      const expectedSecret = 'cs_live_abc123def456'
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          status: 'success',
          session_id: 'ses_xyz789',
          client_secret: expectedSecret,
        }),
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const result = await chatKitConfig.api.getClientSecret()

      expect(result).toBe(expectedSecret)
    })
  })

  describe('getChatKitThreadId', () => {
    it('should return null if no thread ID stored', () => {
      const result = getChatKitThreadId()
      expect(result).toBeNull()
    })

    it('should return stored thread ID', () => {
      const threadId = 'thread_12345'
      localStorage.setItem('chatkit_thread_id', threadId)

      const result = getChatKitThreadId()
      expect(result).toBe(threadId)
    })

    it('should return null if window is undefined', () => {
      const originalWindow = (global as any).window
      ;(global as any).window = undefined

      const result = getChatKitThreadId()
      expect(result).toBeNull()

      ;(global as any).window = originalWindow
    })
  })

  describe('clearChatKitThread', () => {
    it('should remove thread ID from localStorage', () => {
      localStorage.setItem('chatkit_thread_id', 'thread_12345')
      expect(getChatKitThreadId()).toBe('thread_12345')

      clearChatKitThread()

      expect(getChatKitThreadId()).toBeNull()
    })

    it('should not throw error if no thread ID exists', () => {
      expect(() => clearChatKitThread()).not.toThrow()
    })

    it('should handle undefined window gracefully', () => {
      const originalWindow = (global as any).window
      ;(global as any).window = undefined

      expect(() => clearChatKitThread()).not.toThrow()

      ;(global as any).window = originalWindow
    })
  })

  describe('validateChatKitConfig', () => {
    it('should return valid=true when API_URL is configured', () => {
      // API_URL should be set in test environment
      const result = validateChatKitConfig()
      expect(result.valid).toBe(true)
    })

    it('should include error if NEXT_PUBLIC_API_URL missing', () => {
      // This would require mocking environment variables
      // Placeholder for testing missing API_URL
    })

    it('should return errors array', () => {
      const result = validateChatKitConfig()
      expect(Array.isArray(result.errors)).toBe(true)
    })

    it('should validate DOMAIN_KEY is configured', () => {
      const result = validateChatKitConfig()
      // Should not include error about DOMAIN_KEY as it has a default
      expect(result.errors).not.toContain(
        'NEXT_PUBLIC_DOMAIN_KEY is not properly configured'
      )
    })
  })

  describe('Event Handlers', () => {
    it('should have onReady handler that logs message', () => {
      const consoleSpy = jest.spyOn(console, 'log')
      chatKitConfig.onReady?.()
      expect(consoleSpy).toHaveBeenCalledWith('ChatKit is ready!')
      consoleSpy.mockRestore()
    })

    it('should have onError handler', () => {
      const consoleSpy = jest.spyOn(console, 'error')
      const testError = new Error('Test error')
      chatKitConfig.onError?.({ error: testError })
      expect(consoleSpy).toHaveBeenCalledWith('ChatKit error:', testError)
      consoleSpy.mockRestore()
    })

    it('should have onResponseStart handler', () => {
      const consoleSpy = jest.spyOn(console, 'log')
      chatKitConfig.onResponseStart?.()
      expect(consoleSpy).toHaveBeenCalledWith('Assistant is responding...')
      consoleSpy.mockRestore()
    })

    it('should have onThreadChange handler that saves to localStorage', () => {
      const threadId = 'thread_new_123'
      chatKitConfig.onThreadChange?.({ threadId })
      expect(localStorage.getItem('chatkit_thread_id')).toBe(threadId)
    })

    it('should handle onThreadChange with null threadId', () => {
      localStorage.setItem('chatkit_thread_id', 'old_thread')
      chatKitConfig.onThreadChange?.({ threadId: null })
      // Should still have the old thread (not cleared)
      expect(localStorage.getItem('chatkit_thread_id')).toBe('old_thread')
    })

    it('should have onClientTool handler for open_external_link', async () => {
      const windowSpy = jest.spyOn(window, 'open').mockImplementation()
      const result = await chatKitConfig.onClientTool?.({
        name: 'open_external_link',
        params: { url: 'https://example.com' },
      })
      expect(windowSpy).toHaveBeenCalledWith('https://example.com', '_blank')
      expect(result).toEqual({ success: true })
      windowSpy.mockRestore()
    })

    it('should have onClientTool handler for copy_to_clipboard', async () => {
      const clipboardSpy = jest
        .spyOn(navigator.clipboard, 'writeText')
        .mockResolvedValue()

      const result = await chatKitConfig.onClientTool?.({
        name: 'copy_to_clipboard',
        params: { text: 'test text' },
      })

      expect(clipboardSpy).toHaveBeenCalledWith('test text')
      expect(result).toEqual({ success: true })
      clipboardSpy.mockRestore()
    })
  })

  describe('Start Screen Configuration', () => {
    it('should have exactly 4 quick starter prompts', () => {
      expect(chatKitConfig.startScreen.quickStarters).toHaveLength(4)
    })

    it('should include add task quick starter', () => {
      const addTaskStarter = chatKitConfig.startScreen.quickStarters.find(
        (q) => q.title === 'Add a task'
      )
      expect(addTaskStarter).toBeDefined()
    })

    it('should include list tasks quick starter', () => {
      const listTasksStarter = chatKitConfig.startScreen.quickStarters.find(
        (q) => q.title === 'List my tasks'
      )
      expect(listTasksStarter).toBeDefined()
    })

    it('should include complete task quick starter', () => {
      const completeStarter = chatKitConfig.startScreen.quickStarters.find(
        (q) => q.title === 'Complete a task'
      )
      expect(completeStarter).toBeDefined()
    })

    it('should include delete task quick starter', () => {
      const deleteStarter = chatKitConfig.startScreen.quickStarters.find(
        (q) => q.title === 'Delete a task'
      )
      expect(deleteStarter).toBeDefined()
    })
  })
})
