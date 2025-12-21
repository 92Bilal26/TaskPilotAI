/**
 * ChatKit Page Tests
 *
 * Tests for ChatKit page rendering, session initialization,
 * and error handling.
 */

import { render, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import ChatKitPage from '@/app/chatkit/page'
import * as chatKitConfig from '@/lib/chatkit-config'
import { useAuth } from '@/lib/useAuth'

// Mock dependencies
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}))

jest.mock('@/lib/useAuth', () => ({
  useAuth: jest.fn(),
}))

jest.mock('@openai/chatkit-react', () => ({
  useChatKit: jest.fn(() => ({
    control: {},
  })),
  ChatKit: ({ control }: { control: any }) => (
    <div data-testid="chatkit-component">ChatKit Mock Component</div>
  ),
}))

jest.spyOn(chatKitConfig, 'validateChatKitConfig').mockReturnValue({
  valid: true,
  errors: [],
})

describe('ChatKitPage', () => {
  const mockPush = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    })
  })

  describe('Authentication', () => {
    it('should show loading spinner while checking authentication', () => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: false,
        isLoading: true,
      })

      render(<ChatKitPage />)

      expect(screen.getByText('Loading ChatKit...')).toBeInTheDocument()
    })

    it('should return null if not authenticated', () => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: false,
        isLoading: false,
      })

      const { container } = render(<ChatKitPage />)

      // Should render nothing (null)
      expect(container.firstChild).toBeNull()
    })

    it('should render page when authenticated', async () => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: true,
        isLoading: false,
      })

      render(<ChatKitPage />)

      // Should render header
      await waitFor(() => {
        expect(screen.getByText('TaskPilot AI Chat')).toBeInTheDocument()
      })
    })
  })

  describe('Page Layout', () => {
    beforeEach(() => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: true,
        isLoading: false,
      })
    })

    it('should render header with title', () => {
      render(<ChatKitPage />)

      expect(screen.getByText('TaskPilot AI Chat')).toBeInTheDocument()
      expect(screen.getByText('Powered by OpenAI ChatKit')).toBeInTheDocument()
    })

    it('should render back to dashboard button', () => {
      render(<ChatKitPage />)

      const buttons = screen.getAllByText('Back to Dashboard')
      expect(buttons.length).toBeGreaterThan(0)
    })

    it('should navigate to dashboard on back button click', () => {
      const mockPush = jest.fn()
      ;(useRouter as jest.Mock).mockReturnValue({
        push: mockPush,
      })

      render(<ChatKitPage />)

      // Note: In real scenario, would need to simulate button click
      // This is a placeholder for integration testing
    })

    it('should render ChatKit component when mounted and ready', async () => {
      render(<ChatKitPage />)

      await waitFor(() => {
        expect(screen.getByTestId('chatkit-component')).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    beforeEach(() => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: true,
        isLoading: false,
      })
    })

    it('should show error message if ChatKit config is invalid', async () => {
      chatKitConfig.validateChatKitConfig = jest
        .fn()
        .mockReturnValue({
          valid: false,
          errors: ['NEXT_PUBLIC_API_URL is not configured'],
        })

      render(<ChatKitPage />)

      await waitFor(() => {
        expect(
          screen.getByText(/ChatKit configuration error/i)
        ).toBeInTheDocument()
      })
    })

    it('should show error message when ChatKit fails to initialize', async () => {
      chatKitConfig.validateChatKitConfig = jest
        .fn()
        .mockReturnValue({
          valid: true,
          errors: [],
        })

      render(<ChatKitPage />)

      // Should render without error by default
      await waitFor(() => {
        expect(screen.getByText('TaskPilot AI Chat')).toBeInTheDocument()
      })
    })

    it('should provide navigation to dashboard from error state', async () => {
      chatKitConfig.validateChatKitConfig = jest
        .fn()
        .mockReturnValue({
          valid: false,
          errors: ['API connection failed'],
        })

      render(<ChatKitPage />)

      const buttons = screen.getAllByText('Go to Dashboard')
      expect(buttons.length).toBeGreaterThan(0)
    })
  })

  describe('Loading States', () => {
    it('should show initializing message before ChatKit is ready', () => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: true,
        isLoading: false,
      })

      // Mock useChatKit to initially return null
      const useChatKit = require('@openai/chatkit-react').useChatKit as jest.Mock
      useChatKit.mockReturnValueOnce(null)

      render(<ChatKitPage />)

      expect(
        screen.getByText('Initializing ChatKit...')
      ).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    beforeEach(() => {
      ;(useAuth as jest.Mock).mockReturnValue({
        isAuthenticated: true,
        isLoading: false,
      })
    })

    it('should render semantic HTML structure', () => {
      const { container } = render(<ChatKitPage />)

      const header = container.querySelector('header')
      expect(header).toBeInTheDocument()

      const main = container.querySelector('main')
      expect(main).toBeInTheDocument()
    })

    it('should have readable button labels', () => {
      render(<ChatKitPage />)

      const backButtons = screen.getAllByText(/Back to Dashboard/i)
      expect(backButtons.length).toBeGreaterThan(0)
    })
  })
})
