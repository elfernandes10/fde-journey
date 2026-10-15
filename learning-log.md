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

## Oct 15, 2026 — Day 1 (full day session)

### What I built
- Clean dev environment on freshly-reset MacBook
- `hello.py` — first Claude API call, env-based config
- Repo structure: .gitignore, .env, .env.example, README

### What I learned (conceptually)
- HTTP: methods, status codes (200, 401, 403, 404, 405, 429)
- JSON: 6 data types, nested navigation, pretty-printing
- Client/server pattern — client always speaks first; clients are preconfigured reusable connections
- Packages, pip, PyPI, dependency trees, sys.path
- Venvs: isolation per project, PATH manipulation under the hood
- Env vars: shell-level (~/.zshrc) vs project-level (.env), 12-Factor config
- API deprecation: aliases vs snapshots, pinning for production
- Git flow: stage/commit/push, divergent history, rebase vs merge, credential caching
- Systems view of an API call: load balancer → gateway → auth → authz → rate limit → billing → router → inference → response. Cheap checks before expensive compute. Stateless servers = scalability.

### The near-miss
- Pasted real API key into `.env.example` by copy-paste
- Caught by pre-commit `grep -r "sk-ant"` check
- Revoked key immediately, rotated, verified clean
- Lesson: real secrets live in exactly ONE file (.env). Never anywhere else. `cat <file>` is ground truth, not the editor.

### DSA diagnostic
- Started with "I'm bad at DSA; I can word solutions but not code them"
- Diagnostic: pseudocoded reverse-string correctly, translated to Python correctly
- Real gap identified: not thinking or algorithm — Python syntax hygiene (case sensitivity, keyword spelling, indentation)
- Fix: 30 min/day in VS Code with Python extension's red-squiggle feedback. 150-200 problems over 9 months, pseudocode-first always.
- Reframe: "untrained at Python syntax under pressure," not "bad at DSA"

### Target sharpened
- AI Systems Engineer at Google (Cloud AI, Vertex AI, Applied ML).
- Tier-2 landing first likely; Google in 18-month arc; Apple as stretch.
- Hybrid: design + build + deploy. Not pure research, not pure SA, not just-another-backend.

### Questions I'm sitting with
- (add your own)