Point 1: Login + cached credentials
I check “keep me logged in” → credentials cache in local storage → every subsequent app open auto-signs me in with cached creds.
Right direction, needs one critical sharpening.
Your actual password is almost never cached. That would be catastrophic — if someone stole your phone and extracted the storage, they’d have your Amazon password. Instead, this is what happens:
First login → you send email + password to Amazon
Amazon validates → returns a session token (a long opaque string) and a refresh token
The app stores the TOKENS in secure storage (iOS Keychain / Android Keystore — not plain local storage)
Every subsequent request → app sends the token, not your password
Token expires periodically (hours to days) → app uses refresh token to get a new one silently
Refresh token expires eventually (weeks to months) → you’re forced to log in again
Why this design:
Password compromise is catastrophic (works everywhere, forever). Token compromise is limited (works for one session, expires soon).
Amazon can revoke tokens instantly (log out from all devices). Can’t revoke a password that lives on your phone.
Different device = different token = better auditability (“you logged in from a new iPhone”)
Google interview phrasing to internalize: “The client holds session tokens issued by the auth service, not raw credentials. Tokens are short-lived and refreshable, giving the server unilateral revocation power.”
That one sentence demonstrates auth sophistication.
Point 2: API Gateway for cheap auth checks
Call goes through API gateway → cheap auth checks → decide whether to proceed
Correct. You’re reasoning about this correctly. A few additions that would make the answer Google-grade:
The API Gateway does more than auth. The full gateway responsibility list:
AuthN/AuthZ — who are you, what are you allowed to do
Rate limiting — don’t let one user/IP hammer the service
Request routing — figure out which microservice to send this to (Orders? Catalog? Reviews?)
Request/response transformation — convert external API format to internal format
TLS termination — decrypt HTTPS at the edge so internal services don’t need to
Logging/metrics — single chokepoint for observability
Caching — cheap repeated requests served without hitting backend
Circuit breaking — if a downstream service is dying, fail fast rather than piling on
Google frame: at Google, these functions are often split into separate services (Google Front End + ESF + etc.) because at Google’s scale, bundling them creates a monolith. The pattern is called “edge computing” — stuff that doesn’t need the full backend lives at the network edge.
Point 3: Location-based routing
API call carries my location → router sends to nearest datacenter
Right insight, but let me show you how this actually works — it’s cooler than you think.
The location-based routing happens at TWO layers, often before your request even gets to Amazon’s gateway:
Layer 1: DNS-based geographic routing (invisible to you)
When your app resolves www.amazon.com to an IP address, Amazon’s DNS doesn’t give the same answer to everyone
Amazon’s DNS looks at your resolver’s IP (approximation of your location) and returns the IP of the geographically-closest Amazon datacenter
You in Bangalore → gets IPs for Amazon’s Mumbai/Chennai AWS edge
Me in New York → gets IPs for Amazon’s Virginia edge
The routing decision happens BEFORE your HTTP request is even formed
Layer 2: CDN edge nodes
Static content (images, CSS, product thumbnails) is cached at thousands of edge locations
CloudFront (Amazon’s CDN) has nodes in ~400 cities worldwide
Your request for product-image.jpg hits a Bangalore edge node and never reaches a real datacenter
Only dynamic content (your cart, your search results) actually travels to a datacenter
You don’t send your location explicitly. Your IP address is the geographic signal, inferred by DNS. Mobile apps sometimes also send GPS coordinates for things like “stores near me,” but that’s a separate concern.
Google frame: this is called “anycast routing” at the IP level and “geo-DNS” at the DNS level. Google uses both aggressively — google.com in Bangalore resolves to a Google frontend in Mumbai or Chennai, which proxies to the nearest datacenter.
Point 4: TCP + TLS handshake (your explicit “vague” area)
Good self-awareness. Let me teach this properly because it’s genuinely important for Google interviews — they ask “what happens when you type a URL” every single level.
Breakdown of what’s actually happening
You said “TCS and TCP” — the correct names are TCP and TLS. Easy to confuse. Let me walk you through both.
Step 1: TCP three-way handshake (establishes a reliable connection between client and server)
TCP = Transmission Control Protocol. It’s the layer that makes “reliable” possible on top of unreliable packet-switched networks. The handshake:
Client                                Server
  │                                     │
  │   SYN (synchronize, "can we talk?") │
  ├────────────────────────────────────▶│
  │                                     │
  │   SYN-ACK (yes, let's talk)         │
  │◀────────────────────────────────────┤
  │                                     │
  │   ACK (great, confirmed)            │
  ├────────────────────────────────────▶│
  │                                     │
  │        ─── connection open ───      │
Three messages, each with sequence numbers. After this, both sides agree: “we have an open connection, data sent between us will be numbered, acknowledged, retransmitted if lost, delivered in order.”
Why it matters: your HTTP requests ride on top of TCP. TCP makes “I sent you a message” actually mean something — because at the raw network level, packets are dropped, reordered, duplicated all the time. TCP hides all that from you.
Step 2: TLS handshake (establishes an encrypted session on top of TCP)
TLS = Transport Layer Security (what used to be called SSL). This is the “S” in “HTTPS.” It layers encryption on top of the TCP connection.
Simplified handshake:
Client                                             Server
  │                                                  │
  │   "ClientHello: I support TLS 1.3,              │
  │    these cipher suites, this random number"      │
  ├─────────────────────────────────────────────────▶│
  │                                                  │
  │   "ServerHello: let's use TLS 1.3 and           │
  │    this cipher, here's my random, here's        │
  │    my certificate (signed by a CA)"             │
  │◀─────────────────────────────────────────────────┤
  │                                                  │
  │   Client verifies the certificate              │
  │   (signed by trusted CA → is for amazon.com)   │
  │                                                  │
  │   Client and server use the exchanged randoms  │
  │   + ephemeral keys to derive shared secret     │
  │   (Diffie-Hellman key exchange)                │
  │                                                  │
  │   "Finished" (encrypted)                        │
  ├─────────────────────────────────────────────────▶│
  │                                                  │
  │   "Finished" (encrypted)                        │
  │◀─────────────────────────────────────────────────┤
  │                                                  │
  │     ─── encrypted channel open ───              │
What TLS gives you:
Encryption — nobody between you and server can read the data (not your ISP, not your coffee shop WiFi admin, not any router along the way)
Integrity — nobody can tamper with the data in flight (if they do, you detect it and reject the message)
Authentication — the server’s certificate proves it’s actually amazon.com and not an impostor (because a trusted Certificate Authority signed it)
Point 4 corrections to your statement
You said: “Our request is converted into encrypted form, then it is broken into packets and given serial numbers.”
Partially right but inverted in a key way. The order is:
TCP connection opens first (SYN-SYN/ACK-ACK) — unencrypted
TLS handshake happens on top of TCP — negotiates encryption keys. Also unencrypted mostly, but no sensitive data is exchanged.
Now the HTTP request is composed, encrypted via TLS, and sent down the pipe
TCP breaks it into packets, numbers them, handles delivery
So: TCP wraps TLS wraps HTTP. Not TLS wraps TCP. Think of it as nested envelopes:
TCP packet (with headers, sequence numbers)
  └── TLS record (encrypted blob)
       └── HTTP request (plaintext once decrypted)
Google frame: “what happens when you type a URL” is possibly the most-asked system design warmup. The expected 5-minute answer touches DNS → TCP handshake → TLS handshake → HTTP request → server processing → response → TLS → TCP teardown → render. Fluency with this stack is table stakes. You’ve just started building it. I’ll push you to go deeper on this soon.
Point 5: “Every click = new API call?”
Once the connection is established every time I click something on the screen its a new API call, correct?
Almost right, with important nuances. Three realities to grasp:
Reality 1: Not every click triggers a network request
Modern apps do a lot of local state management. Opening a filter menu, scrolling a list you’ve already loaded, toggling a UI element — these often don’t hit the server at all. The server is only involved when the app needs data it doesn’t have, or needs to persist something.
Examples that DON’T hit the server:
Scrolling through products you’ve already loaded
Opening/closing menus
Toggling filters that work on already-loaded data
Typing in a search box (locally until you submit)
Examples that DO hit the server:
Submitting a search
Adding to cart (persistence)
Loading a product detail you haven’t seen
Checking out
Reality 2: One click often triggers MULTIPLE API calls
Opening a product page probably triggers:
GET /products/{id} → product details
GET /products/{id}/reviews → reviews
GET /products/{id}/recommendations → “customers also bought”
GET /users/me/wishlist → is this already in my wishlist?
POST /analytics/view → log that you viewed this product
One screen = many parallel requests. This is standard. Each service owns its data; the client composes them.
Reality 3: TCP connections are reused, not recreated per request
Here’s where your “once connection is established” phrasing shows a subtle misunderstanding. You implicitly assumed one long-lived TCP connection carries all your requests. Not quite — but closer than nothing.
The actual pattern depends on HTTP version:
HTTP/1.1: typically keeps one TCP connection open per server for a short time (keep-alive, usually 60-300 sec). Multiple requests reuse it sequentially.
HTTP/2: multiplexes many requests over a single TCP connection in parallel (great for the “many requests from one page load” pattern)
HTTP/3 (over QUIC): replaces TCP entirely with a UDP-based protocol that handles multiplexing + encryption together
Why this matters: TCP handshake + TLS handshake together take 100-300ms. Doing that per request would be catastrophic for user experience. Connection reuse is one of the biggest latency optimizations in modern web. Amazon’s app likely maintains persistent HTTP/2 connections to Amazon’s edge, and parallel requests multiplex over them.
Google frame: when a Google interviewer asks “how would you make this app faster,” connection pooling, HTTP/2, and HTTP/3 are classic answers. The ability to reason about “handshake cost amortized across many requests” is sign of networking depth.
What you just demonstrated
You walked through a 5-step mental model of Amazon’s architecture. Here’s what that showed:
Point 1: correct instinct about credentials, needs tightening around tokens
Point 2: correctly placed API Gateway, correctly understood auth-at-edge principle
Point 3: correct instinct about geographic routing, missed that it happens at DNS layer before HTTP
Point 4: honestly flagged your gap on TCP/TLS — exactly the right behavior
Point 5: partial understanding of connection lifecycle, which we just sharpened
This is a real system design walkthrough. Four months ago you wouldn’t have had the vocabulary to form these questions. Now you’re walking through architecture at the right level of abstraction.
What to do with this
Three concrete actions:
1. Save this to your systems-notes
cd ~/fde-journey
code systems-notes/03-amazon-app-walkthrough.md
Paste your 5 points + the key corrections I gave you + what you want to go deeper on. This is a portfolio artifact and interview prep in one.
2. Internalize the networking stack as a mental model
Draw this once by hand. Doesn’t have to be pretty:
┌─────────────────────────────────┐
│ HTTP (your request/response)    │  ← Layer 7: application
├─────────────────────────────────┤
│ TLS (encryption)                │  ← Layer 6ish
├─────────────────────────────────┤
│ TCP (reliable connection)       │  ← Layer 4
├─────────────────────────────────┤
│ IP (routing between networks)   │  ← Layer 3
├─────────────────────────────────┤
│ Physical (wires, radio, fiber)  │  ← Layer 1
└─────────────────────────────────┘
This is the networking stack. Each layer wraps the one above it, hiding its complexity. Keep this picture in your head. When someone says “the TLS handshake failed,” you know they mean one specific layer. When someone says “the TCP connection timed out,” you know what that implies.
3. We will deep-dive TCP/TLS soon
You flagged you’re vague on this. This is one of the system-concept-of-the-week topics coming up. Probably Week 3 or 4, when we start the DDIA sequence and I pair it with networking fundamentals. By end of month 2, “what happens when you type a URL” should be a 10-minute confident walkthrough from you.
