# Learning log

## Oct 15, 2026 — Session 1: APIs from scratch

### What I learned
- HTTP: methods, status codes, headers, body
- JSON: 6 data types, nested navigation
- Auth: API keys, environment variables, 401 vs 403 vs 405
- PATH, shells, startup files (.zprofile vs .zshrc)
- System design: an API call isn't one thing — it's 5-10 microservices
  chained together. Auth is a cache/DB lookup. Cheap checks before
  expensive compute.

### What I built
- Clean dev environment on reset MacBook
- GitHub repo wired up

### Questions I'm sitting with
- (Add your own as they come)

## Oct 15, 2026 — Day 1: first API call shipped

### What I built
- Working dev environment (Python 3.11, git, VS Code) on freshly-wiped MacBook
- `hello.py` — first Claude API call, reads config from .env
- Public GitHub repo with proper .gitignore and .env.example

### What I learned
- HTTP, JSON, status codes (200, 401, 403, 404, 405, 429)
- Client/server pattern — the client always speaks first
- Clients are preconfigured reusable connections, not just function wrappers
- Packages, pip, PyPI, dependency trees, sys.path
- Why venvs exist and how they manipulate PATH
- Env vars: shell-level vs project-level (.env)
- 12-Factor config: never mix config with code
- API deprecation: alias vs snapshot, pinning in production
- Git: stage/commit/push, divergent history, rebase vs merge, credential caching

### The near-miss
- Pasted real API key into .env.example by copy-paste
- Caught by `grep -r "sk-ant"` pre-commit check
- Revoked key within minutes, created new one, cleaned up
- Rules I now live by:
  - Secrets live in exactly ONE file: .env
  - Always `grep -r "sk-ant"` before every commit
  - `cat <file>` is ground truth; the editor shows a buffer
  - Revoke-first, debug-second

### Why the architect lens matters
- An API call isn't one thing — it's a chain of microservices (auth, rate limit, billing, inference)
- Cheap checks run before expensive compute
- Statelessness enables scale; stateful clients hold session + connection
- Dreaming about solutions requires foundational understanding — AI amplifies, not substitutes

### Questions I'm sitting with
- (Add your own as they come up)