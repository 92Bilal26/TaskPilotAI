# OpenAI ChatKit Reference Documentation

**Last Updated**: December 14, 2025
**Source**: Official OpenAI ChatKit Documentation

## Overview

OpenAI ChatKit is a framework-agnostic, drop-in chat solution that eliminates the need to build custom chat UIs or manage low-level chat state. It provides a batteries-included framework for developers building AI-powered chat experiences.

## Official Resources

- **GitHub Repository**: https://github.com/openai/chatkit-js
- **React Package**: @openai/chatkit-react (npm)
- **Official Documentation**: https://platform.openai.com/docs/guides/chatkit
- **Domain Allowlist Settings**: https://platform.openai.com/settings/organization/security/domain-allowlist
- **Advanced Samples**: https://github.com/openai/openai-chatkit-advanced-samples

## What is ChatKit?

ChatKit is a pre-built, customizable chat UI framework that:
- Handles message display and user input
- Manages streaming responses
- Visualizes tool invocations and results
- Supports file attachments and uploads
- Shows chain-of-thought reasoning
- Works with any custom backend

## Key Features

### 1. UI Components
- Message display with sender identification
- User input area with auto-complete
- Message history management
- Responsive design (desktop, tablet, mobile)

### 2. Streaming Support
- Real-time message streaming as server sends chunks
- Progressive token-by-token display
- Reduced perceived latency

### 3. Tool Visualization
- Display tool names and parameters
- Show tool execution results
- Visualize multi-step tool chains
- Display reasoning steps

### 4. Rich Content Support
- Text messages
- Code blocks with syntax highlighting
- Links and formatting
- File attachments
- Image uploads and display

### 5. Customization
- CSS customization
- Component overrides
- Theme support
- Custom styling hooks

## Installation

### Step 1: Install React Package
```bash
cd frontend
npm install @openai/chatkit-react
```

### Step 2: Add ChatKit Script
```html
<!-- In HTML head or Next.js layout.tsx -->
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
```

### Step 3: Install with TypeScript Support
```bash
npm install @openai/chatkit-react --save-dev
npm install --save-dev @types/node
```

## Basic Usage

### Using useChatKit Hook

```typescript
'use client'; // Next.js client component

import { useChatKit } from '@openai/chatkit-react';
import { useAuth } from '@/lib/auth-client';

export function ChatWindow() {
  const { token } = useAuth(); // Get JWT token

  const { mounted, containerRef } = useChatKit({
    // Configuration
    apiBaseUrl: process.env.NEXT_PUBLIC_API_URL,

    // Generate client secret server-side
    getClientSecret: async () => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat/init`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      return data.clientSecret;
    },

    // Optional: customize appearance
    theme: 'light', // or 'dark'

    // Optional: handler for errors
    onError: (error) => {
      console.error('Chat error:', error);
    }
  });

  if (!mounted) {
    return <div>Loading chat...</div>;
  }

  return (
    <div
      ref={containerRef}
      style={{ height: '100vh', width: '100%' }}
    />
  );
}
```

## Domain Configuration (Production Required)

### Step 1: Deploy Frontend
Deploy your Next.js app to get a production URL:
```
Vercel: https://your-app.vercel.app
Custom domain: https://yourdomain.com
```

### Step 2: Register Domain
1. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Click "Add domain"
3. Enter your frontend URL (without trailing slash)
4. Save

### Step 3: Get Domain Key
After registering, OpenAI provides a domain key.

### Step 4: Configure Frontend
```typescript
const { mounted, containerRef } = useChatKit({
  apiBaseUrl: process.env.NEXT_PUBLIC_API_URL,
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY, // Production only
  getClientSecret: async () => { /* ... */ }
});
```

## Backend Integration

### Generate Client Secret (FastAPI Example)

```python
from fastapi import FastAPI, Depends, HTTPException
import os
import jwt
from datetime import datetime, timedelta

app = FastAPI()

def get_current_user(token: str = Depends(...)) -> str:
    """Extract user from JWT token."""
    payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    return payload.get("user_id")

@app.post("/api/chat/init")
async def init_chat(current_user: str = Depends(get_current_user)):
    """Generate client secret for ChatKit."""

    # Create JWT for ChatKit (client secret)
    secret = jwt.encode(
        {
            "user_id": current_user,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        os.getenv("OPENAI_API_KEY"),
        algorithm="HS256"
    )

    return {
        "clientSecret": secret,
        "expiresIn": 3600
    }
```

### Chat Endpoint (StreamingResponse)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai.agents import Agent

@app.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    message: str,
    conversation_id: Optional[int] = None,
    current_user: str = Depends(get_current_user)
):
    """Chat endpoint with streaming response."""

    # Verify user authorization
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Get or create conversation
    conversation = get_or_create_conversation(user_id, conversation_id)

    # Store user message
    store_message(conversation.id, "user", message)

    # Initialize agent with MCP tools
    agent = Agent(
        model="gpt-4o",
        mcp_server_url=os.getenv("MCP_SERVER_URL"),
        tools=["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    )

    # Stream response
    async def generate():
        full_response = ""
        async for chunk in agent.run(message, stream=True):
            full_response += chunk.text
            yield f"data: {json.dumps({'text': chunk.text})}\n\n"

        # Store assistant message
        store_message(conversation.id, "assistant", full_response)

        # Send final response with tool calls
        yield f"data: {json.dumps({'done': True, 'conversation_id': conversation.id})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
# Production only:
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

### Backend (.env)
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret
MCP_SERVER_URL=http://localhost:3000
```

## ChatKit Event Handlers

```typescript
const { mounted, containerRef } = useChatKit({
  // Called when message is sent
  onMessage: (message: string) => {
    console.log('User sent:', message);
  },

  // Called when response received
  onResponse: (response: any) => {
    console.log('Assistant response:', response);
  },

  // Called on error
  onError: (error: Error) => {
    console.error('Error:', error.message);
  },

  // Called when tool is invoked
  onToolCall: (tool: string, params: any) => {
    console.log(`Tool ${tool} invoked with`, params);
  }
});
```

## Customization Examples

### Custom Theme
```typescript
const { mounted, containerRef } = useChatKit({
  // Dark theme
  theme: 'dark',

  // Custom CSS class
  className: 'custom-chatkit',

  // Custom styles
  style: {
    backgroundColor: '#f5f5f5',
    borderRadius: '12px'
  }
});
```

### Custom Message Handler
```typescript
const { mounted, containerRef } = useChatKit({
  // Pre-process user messages
  beforeSendMessage: (message: string) => {
    return message.trim(); // Remove whitespace
  },

  // Post-process responses
  afterReceiveMessage: (message: string) => {
    return message; // Can transform response
  }
});
```

## Local vs Production Deployment

### Local Development (localhost)
- Domain allowlist **NOT required**
- Works without domainKey
- Useful for testing and development
- Example: `http://localhost:3000`

### Production Deployment
- Domain allowlist **REQUIRED**
- Must register domain at https://platform.openai.com/settings/organization/security/domain-allowlist
- Must include domainKey in configuration
- Example: `https://your-app.vercel.app`

## Accessibility Features

ChatKit includes built-in accessibility:
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Focus indicators on all interactive elements

## Performance Optimization

### 1. Code Splitting
```typescript
const ChatWindow = dynamic(() => import('@/components/ChatWindow'), {
  loading: () => <div>Loading chat...</div>
});
```

### 2. Message Virtualization
ChatKit automatically virtualizes long message lists for performance.

### 3. Image Optimization
If supporting file uploads, optimize images:
```typescript
// In backend
from PIL import Image
image = Image.open(file)
image.thumbnail((800, 800))
image.save(optimized_path)
```

## Error Handling

```typescript
const { mounted, containerRef } = useChatKit({
  onError: (error) => {
    // Handle different error types
    if (error.code === 'AUTHENTICATION_FAILED') {
      // Redirect to login
      window.location.href = '/signin';
    } else if (error.code === 'RATE_LIMITED') {
      // Show rate limit message
      toast.error('Too many requests. Please wait.');
    } else {
      // Generic error handler
      console.error('Chat error:', error.message);
    }
  }
});
```

## Integration with Phase 3

### Architecture
```
ChatKit (UI)
    ↓
/api/{user_id}/chat (Endpoint)
    ↓
OpenAI Agents SDK
    ↓
MCP Tools
    ↓
Database
```

### Flow
1. User types message in ChatKit
2. ChatKit sends to `/api/{user_id}/chat`
3. Backend creates Agent with MCP tools
4. Agent selects and invokes appropriate tools
5. Tools access database (user-isolated)
6. Response streamed back to ChatKit
7. ChatKit displays message and tools
8. Server has ZERO state (stateless)

## Troubleshooting

### ChatKit Not Loading
- Verify script tag is in head
- Check browser console for errors
- Ensure NEXT_PUBLIC_API_URL is correct

### Domain Allowlist Errors
- Verify domain in allowlist settings
- Include domainKey in configuration
- Use HTTPS in production
- Don't include trailing slash

### Client Secret Generation Fails
- Verify backend endpoint exists
- Check JWT token is valid
- Ensure Authorization header present
- Verify OPENAI_API_KEY set

## Best Practices

1. **User Isolation**: Always verify user_id from JWT token
2. **Error Messages**: Display user-friendly messages
3. **Loading States**: Show loading indicator while streaming
4. **Timeout Handling**: Set reasonable timeouts
5. **Log Management**: Keep logs for debugging
6. **Security**: Never expose API keys to frontend
7. **Performance**: Monitor streaming latency
8. **Testing**: Test on multiple devices/browsers

## Resources

- ChatKit-JS Repository: https://github.com/openai/chatkit-js
- Advanced Samples: https://github.com/openai/openai-chatkit-advanced-samples
- Platform Docs: https://platform.openai.com/docs/guides/chatkit
- Domain Allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist

## Version Information

- Latest Version: Check GitHub releases
- React Version: 16.8+ (hooks required)
- Node Version: 14+
- Next.js Version: 12+ (for Phase 3)
- TypeScript: Full support

## Next Steps for Phase 3

1. Install ChatKit React package
2. Add script tag to layout
3. Create ChatWindow component
4. Implement getClientSecret handler
5. Connect to /api/{user_id}/chat endpoint
6. Register domain for production
7. Configure domainKey
8. Test streaming and tool visualization
