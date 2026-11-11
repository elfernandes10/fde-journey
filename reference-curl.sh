#!/bin/bash
# Reference: raw Anthropic API call via curl.
# Reminds me that the SDK is just HTTP underneath.
#
# Prerequisite: ANTHROPIC_API_KEY in environment, loaded from .env:
#   export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d '=' -f2)

curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-5-5",
    "max_tokens": 300,
    "messages": [
      {"role": "user", "content": "In 3 sentences, explain what RAG is to a data engineer."}
    ]
  }' | python3 -m json.tool