"""
hello.py — my first Claude API call.
Sends one message to Claude and prints the response.
"""

import anthropic

# Create the client. By default, it looks for the ANTHROPIC_API_KEY
# environment variable. If missing, it raises an error immediately.
client = anthropic.Anthropic()

# Build and send the request.
# Under the hood: HTTPS POST to api.anthropic.com/v1/messages
# with headers (auth, version, content-type) and a JSON body.
message = client.messages.create(
    model="claude-sonnet-5-5",      # which model to use
    max_tokens=300,                  # cap the response length (budget guard)
    messages=[                       # conversation history (just 1 turn here)
        {
            "role": "user",
            "content": "In 3 sentences, explain what RAG (Retrieval Augmented Generation) is to a data engineer."
        }
    ]
)

# Response is a structured object. Pull out what we want:
# - content is a list of content blocks (text, tool calls, images, etc.)
# - [0] = first block; .text = the actual string
print("--- Claude says ---")
print(message.content[0].text)

# Diagnostics worth printing — you'll want these all the time
print("\n--- Metadata ---")
print(f"Model: {message.model}")
print(f"Stop reason: {message.stop_reason}")
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")