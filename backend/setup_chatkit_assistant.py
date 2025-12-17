#!/usr/bin/env python3
"""
Setup ChatKit Assistant on OpenAI

This script creates an OpenAI Assistant configured for ChatKit integration.
Run this ONCE to set up the assistant, then copy the ID to your config.

Usage:
    python setup_chatkit_assistant.py
"""

import os
import json
from openai import OpenAI
from config import settings

# Initialize OpenAI client
api_key = settings.OPENAI_API_KEY
if not api_key or api_key == "sk-test-key":
    print("❌ Error: OPENAI_API_KEY is not properly configured in backend/.env")
    exit(1)

client = OpenAI(api_key=api_key)

print("=" * 60)
print("ChatKit Assistant Setup")
print("=" * 60)

try:
    # Create assistant for ChatKit
    print("\n📝 Creating ChatKit assistant...")

    assistant = client.beta.assistants.create(
        name="TaskPilot ChatKit Assistant",
        description="AI assistant for managing tasks via ChatKit",
        instructions="""You are TaskPilot AI, a helpful task management assistant powered by OpenAI.

Your role is to help users manage their tasks through natural conversation.

When users ask you to:
1. Add tasks: Acknowledge and confirm the task details
2. List tasks: Summarize their current tasks
3. Complete/Delete tasks: Ask for clarification if needed
4. Update tasks: Confirm the changes made

Always be helpful, professional, and provide clear confirmations of actions.

Important:
- Be conversational and friendly
- Ask clarifying questions when needed
- Provide clear summaries of task actions
- Suggest related actions when appropriate""",
        model="gpt-4-turbo-preview",
        tools=[
            {
                "type": "code_interpreter"
            },
            {
                "type": "file_search"
            }
        ]
    )

    print(f"✅ Assistant created successfully!")
    print(f"\n📋 Assistant Details:")
    print(f"   Name: {assistant.name}")
    print(f"   ID: {assistant.id}")
    print(f"   Model: {assistant.model}")
    print(f"   Description: {assistant.description}")

    print(f"\n" + "=" * 60)
    print("🔧 Next Steps:")
    print("=" * 60)
    print(f"\n1. Copy the Assistant ID:")
    print(f"   {assistant.id}")

    print(f"\n2. Update backend/routes/chatkit.py:")
    print(f'   CHATKIT_ASSISTANT_ID = "{assistant.id}"')

    print(f"\n3. Save this ID for reference:")
    print(f'   Assistant ID: {assistant.id}')

    print(f"\n4. Restart your backend server")

    print(f"\n5. Test ChatKit at: http://localhost:3000/chatkit")

    print(f"\n" + "=" * 60)

    # Save to a config file
    config_file = "chatkit_assistant_config.json"
    config = {
        "assistant_id": assistant.id,
        "assistant_name": assistant.name,
        "model": assistant.model,
        "created_at": str(assistant.created_at),
    }

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n💾 Configuration saved to: {config_file}")

except Exception as e:
    print(f"\n❌ Error creating assistant: {e}")
    exit(1)
