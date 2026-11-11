# Experiment 01: Anthropic API via Raw HTTP

**Date:** Oct 17-19, 2026
**Goal:** Understand the Claude API at the HTTP level, independent of any SDK. Build intuition for the error modes and rate-limit contract.

## Setup

Loaded `ANTHROPIC_API_KEY` from `.env` into shell env:
```bash
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d '=' -f2)
```

## Baseline: successful call

(Insert working curl + the response structure you observed — content/stop_reason/usage.)

## Break 1: Invalid API key

- **Prediction:** 401 Unauthorized
- **Actual:** 401 Unauthorized
- **Takeaway:** Auth happens at the edge, before any model inference. Invalid keys never reach a GPU. No tokens billed.

## Break 2: Unknown model name

- **Prediction:** 400 Bad Request (expected 404 initially — corrected)
- **Actual:** 404 (Anthropic specifically treats unknown models as "resource not found")
- **Takeaway:** Status code meaning varies by API design. Most APIs would 400 here. Anthropic chose 404. Both defensible. Check the specific API's convention.

## Break 3: Missing required field (`messages`)

- **Prediction:** 400 Bad Request
- **Actual:** 400 Bad Request
- **Takeaway:** Validation errors return 400 with the specific field name. Good API design.

## Break 4: max_tokens too low

- **Prediction:** 200 with `stop_reason: max_tokens`
- **Actual:** 200 but response was consumed entirely by thinking block
- **Takeaway:** Discovered extended thinking in current Claude models. Thinking tokens count against max_tokens. For complex queries, even 500 tokens can be eaten by reasoning before any visible answer. Production implication: must handle `thinking` content type, must set max_tokens generously or disable thinking for latency-critical paths.
- See: `systems-notes/02-thinking-blocks-and-cost.md`

## Break 5: Malformed JSON

- **Prediction:** 400 with parse error
- **Actual:** 400, message "expected , or ] at line 5 column 3"
- **Takeaway:** Anthropic's error messages pinpoint exact position. Textbook good error design.

## Break 6: Rate limit headers (observed, not triggered)

My current tier (Tier 2) limits per minute:
- Requests: 10,000
- Input tokens: 10,000,000
- Output tokens: 2,000,000
- Combined tokens: 12,000,000

**Takeaways:**
- Three limits enforced independently; any one hitting zero causes 429
- Reset timestamps staggered by seconds (prevents thundering herd on reset)
- Production clients must track all three remaining budgets and preemptively throttle
- For solo projects, these limits are irrelevant (1000x more than any single developer needs)

## What I'd do differently in production

- **Never silently truncate on stop_reason != end_turn.** Check it explicitly.
- **Track rate limit headers on every response.** Preemptively throttle at ~10% remaining.
- **Model routing:** classify queries first, send simple ones to Haiku, hard ones to Sonnet/Opus. 10x cost savings.
- **Prompt caching** for repeated system prompts (reduces input cost ~90%).
- **Disable thinking** on latency-critical paths where reasoning quality < 500ms response time.

## Open questions
- How does prompt caching interact with thinking blocks?
- What's the server-side back-off recommendation when I DO hit 429? (Retry-After header? Fixed backoff? Exponential?)
- How do multi-model routing decisions get made in practice — static rules, learned classifier, or user-controlled?