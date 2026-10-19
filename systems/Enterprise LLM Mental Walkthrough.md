1. User logs into Web UI via corporate SSO (Okta). Receives session JWT.

2. User types query → UI sends HTTPS POST to backend API with:
   - Authorization: Bearer <session_jwt>
   - Body: {"query": "..."}

3. Request hits API Gateway:
   a. Validates JWT signature + expiry (local, no network).
   b. Checks session token in Redis cache (microseconds). On miss, 
      validates against auth service and repopulates cache.
   c. Checks rate limit for user_id in Redis.
   d. If any check fails → 401/403/429 returned, request dies.

4. Request reaches Orchestration layer with validated user_id attached.
   The orchestrator decides, based on query type and user tier:
   - Needs RAG? → trigger retrieval
   - Needs tools? → prepare tool definitions
   - Needs long-term memory? → fetch user prefs from DB
   - Which model tier? → Haiku/Sonnet/Opus by complexity

5. Retrieval (if needed):
   - Query embedded via embedding API
   - Vector search in Qdrant/Pinecone with metadata filters
     (filter: documents this user is allowed to see — critical for enterprise)
   - Top-k results reranked by cross-encoder
   - Top-N returned

6. Prompt assembly:
   - System prompt (defines assistant behavior)
   - Retrieved context (if RAG)
   - Conversation history (if multi-turn)
   - Current user query
   - Tool definitions (if applicable)
   - All packed into messages[] within token budget

7. Model call to Anthropic:
   - Uses backend's API key (NOT user's)
   - Streams response back
   - Retries on transient errors (429, 500)

8. Post-processing:
   - Parse any tool calls, execute them, loop back to model
   - PII redaction (enterprise requirement — no SSNs in logs)
   - Format for UI

9. Response streams back to UI, rendered token by token.

10. Observability sidechannel (parallel, async, non-blocking):
    - Log request + response (with PII redacted)
    - Metrics: latency, tokens in/out, model used, cost estimate
    - Traces: span across all services for debugging
    - Eval signals: thumbs up/down from user → eval dataset