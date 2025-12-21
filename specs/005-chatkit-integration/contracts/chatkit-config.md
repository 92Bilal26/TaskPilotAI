# API Contract: ChatKit Frontend Configuration

**Component**: `useChatKit()` React Hook Configuration
**Description**: Frontend ChatKit component initialization with session management
**Version**: 1.0
**Status**: Ready for Implementation

---

## Configuration Object Structure

```typescript
interface ChatKitConfig {
  api: {
    getClientSecret: (existing?: string) => Promise<string>
  }
  theme?: {
    primaryColor?: string
    darkMode?: boolean
  }
  onMessage?: (message: string) => void
  onError?: (error: Error) => void
}
```

---

## Required Configuration: getClientSecret()

### Function Signature

```typescript
async function getClientSecret(existing?: string): Promise<string>
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `existing` | string \| undefined | No | Previously issued client_secret (if available) |

### Return Value

**Type**: `Promise<string>`

**Value**: ChatKit client_secret from OpenAI

**Format**: Starts with `cs_`, 30-50 characters

### Behavior

#### Case 1: Reuse Existing Secret (Optimization)

```typescript
getClientSecret("cs_live_abc123...")
↓
Returns immediately: "cs_live_abc123..."
(No backend call)
```

#### Case 2: Create New Secret

```typescript
getClientSecret(undefined)  // or getClientSecret()
↓
POST /api/chatkit/sessions
↓
Receives: { status: "success", data: { client_secret: "cs_...", ... } }
↓
Returns: "cs_..."
```

#### Case 3: Reuse Within Session

```typescript
// First call
await getClientSecret() → calls backend → returns "cs_abc123"

// ChatKit uses "cs_abc123" internally
// Later, ChatKit needs to verify connection
await getClientSecret("cs_abc123") → returns "cs_abc123" (no backend call)
```

### Error Handling

```typescript
try {
  const secret = await getClientSecret()
  // Use secret for ChatKit
} catch (error) {
  console.error('Failed to get ChatKit session:', error)
  // Show user-friendly error message
  // Example: "Unable to start chat. Please try again."
}
```

---

## Usage Pattern

### In React Component

```typescript
import { useChatKit } from '@openai/chatkit-react'
import { chatKitConfig } from '@/lib/chatkit-config'

export function ChatWindow() {
  const { chat, isReady, error } = useChatKit(chatKitConfig)

  return (
    <div>
      {!isReady && <div>Loading chat...</div>}
      {error && <div>Error: {error.message}</div>}
      {isReady && (
        <div>
          {/* ChatKit renders here */}
          Chat interface loaded
        </div>
      )}
    </div>
  )
}
```

### In Config File (frontend/lib/chatkit-config.ts)

```typescript
import type { ChatKitConfig } from '@openai/chatkit-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const chatKitConfig: ChatKitConfig = {
  api: {
    async getClientSecret(existing?: string): Promise<string> {
      // Reuse existing secret if available
      if (existing) {
        console.log('Reusing existing ChatKit client secret')
        return existing
      }

      try {
        console.log('Creating new ChatKit session')

        // Call backend endpoint
        const response = await fetch(`${API_URL}/api/chatkit/sessions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // Optional: Add JWT token for user identification
            // 'Authorization': `Bearer ${jwtToken}`
          }
        })

        // Handle HTTP errors
        if (!response.ok) {
          throw new Error(`Session creation failed: ${response.statusText}`)
        }

        // Parse response
        const data = await response.json()
        const clientSecret = data.data?.client_secret

        if (!clientSecret) {
          throw new Error('No client secret in response')
        }

        console.log('Got ChatKit session:', data.data.session_id)
        return clientSecret
      } catch (error) {
        console.error('Error getting ChatKit session:', error)
        throw error
      }
    }
  },

  // Optional: Customize ChatKit appearance
  theme: {
    primaryColor: '#0070f3', // Next.js blue
    darkMode: false
  }
}
```

---

## Response Mapping

### Backend Response → Frontend Usage

**Backend returns**:
```json
{
  "status": "success",
  "data": {
    "client_secret": "cs_live_8a7b6c5d4e3f2g1h0i9j8k7l6m5n4o3p",
    "session_id": "ses_9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k"
  }
}
```

**Frontend extracts**:
```typescript
const clientSecret = response.data.data.client_secret
// Extract: "cs_live_8a7b6c5d4e3f2g1h0i9j8k7l6m5n4o3p"
```

**ChatKit uses**:
```typescript
useChatKit({
  api: {
    getClientSecret: async () => "cs_live_8a7b6c5d4e3f2g1h0i9j8k7l6m5n4o3p"
  }
})
// ChatKit initializes with client_secret
// Establishes WebSocket connection to OpenAI
// User can type and send messages
```

---

## Error Scenarios & Handling

### Scenario 1: Backend Returns Error

```typescript
// Backend response (401 Unauthorized)
{
  "status": "error",
  "message": "OpenAI authentication failed"
}
```

**Frontend handling**:
```typescript
const response = await fetch(`${API_URL}/api/chatkit/sessions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
})

if (!response.ok) {
  const error = await response.json()
  throw new Error(error.message)
  // catch block logs and shows user message
}
```

**User sees**: "Unable to start chat. Please check configuration."

### Scenario 2: Network Failure

```typescript
// Fetch throws network error
const response = await fetch(...)
// Error: "Failed to fetch"
```

**Frontend handling**:
```typescript
catch (error) {
  console.error('Network error:', error)
  // Show: "Network connection lost. Please check your internet."
}
```

### Scenario 3: Invalid Response Format

```typescript
// Backend returns valid HTTP but malformed JSON
{
  "client_secret": "missing"
}
```

**Frontend handling**:
```typescript
const clientSecret = data.data?.client_secret
if (!clientSecret) {
  throw new Error('Invalid response from server')
}
```

---

## Optional Features (Phase 3b+)

### With User Authentication

```typescript
async function getClientSecret(existing?: string): Promise<string> {
  if (existing) return existing

  // Get JWT token from auth context
  const jwtToken = useAuth().token

  const response = await fetch(`${API_URL}/api/chatkit/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`  // Add JWT
    }
  })

  // Backend will associate session with authenticated user
  // Enables: per-user conversation history, user-specific agents, etc.
}
```

### With Message Callbacks

```typescript
const config: ChatKitConfig = {
  api: { getClientSecret },

  // Called when user sends message
  onMessage: (message: string) => {
    console.log('User sent:', message)
    // Log to analytics, update UI, etc.
  },

  // Called when error occurs
  onError: (error: Error) => {
    console.error('Chat error:', error)
    // Send to error tracking, show notification, etc.
  }
}
```

---

## Testing

### Unit Test: getClientSecret()

```typescript
describe('getClientSecret()', () => {
  it('should create new session when no existing secret', async () => {
    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({
            status: 'success',
            data: {
              client_secret: 'cs_test_abc123',
              session_id: 'ses_test_xyz789'
            }
          })
        )
      )
    )

    const secret = await getClientSecret()

    expect(secret).toBe('cs_test_abc123')
    expect(global.fetch).toHaveBeenCalledWith(
      `${API_URL}/api/chatkit/sessions`,
      expect.objectContaining({ method: 'POST' })
    )
  })

  it('should reuse existing secret', async () => {
    const existingSecret = 'cs_existing_123'

    const secret = await getClientSecret(existingSecret)

    expect(secret).toBe(existingSecret)
    expect(global.fetch).not.toHaveBeenCalled()
  })

  it('should handle fetch errors', async () => {
    global.fetch = jest.fn(() =>
      Promise.reject(new Error('Network error'))
    )

    await expect(getClientSecret()).rejects.toThrow('Network error')
  })

  it('should handle backend errors', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({ status: 'error', message: 'Auth failed' }),
          { status: 401 }
        )
      )
    )

    await expect(getClientSecret()).rejects.toThrow()
  })
})
```

### Integration Test: Full Initialization

```typescript
describe('ChatKit initialization', () => {
  it('should initialize ChatKit with valid config', async () => {
    // Mock ChatKit hook
    const mockUseChatKit = jest.fn()

    // Render component with config
    render(<ChatWindow />)

    // Verify getClientSecret was called
    await waitFor(() => {
      expect(mockUseChatKit).toHaveBeenCalledWith(
        expect.objectContaining({
          api: expect.objectContaining({
            getClientSecret: expect.any(Function)
          })
        })
      )
    })
  })

  it('should display chat interface after initialization', async () => {
    render(<ChatWindow />)

    // Initially shows loading
    expect(screen.getByText('Loading chat...')).toBeInTheDocument()

    // After session created, shows chat interface
    await waitFor(() => {
      expect(screen.getByText('Chat interface loaded')).toBeInTheDocument()
    })
  })
})
```

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile (iOS) | 14+ | ✅ Full |
| Mobile (Android) | 9+ | ✅ Full |

---

## Environment Variables

**Required** (frontend/.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Optional** (Phase 3b+):
```
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=your_domain_key_here
```

---

## Related Documentation

- [Sessions API Contract](./sessions-api.md) - Backend endpoint documentation
- [Data Model](../data-model.md) - ChatKit Session entity definition
- [OpenAI ChatKit Docs](https://github.com/openai/chatkit-js) - Official ChatKit documentation

---

**Last Updated**: December 20, 2025
**Status**: Ready for Implementation
**Related**: [Sessions API Contract](./sessions-api.md)
