# DDIA Ch 2: Data Models and Query Languages

## 3-sentence summary
Data models are the single most important design choice in software because every layer above is shaped by them. The relational model dominated for 40 years because of its generality, but document and graph models have resurged for specific use cases where relational hits friction. The choice between them depends on data shape (hierarchical vs networked vs tabular), query patterns, and how tightly coupled the data is to a single "owning" entity.

---

## Core insight: software is layers of data models

- Applications are built as **stacks of data models**, each layer translating the one below into something more useful for the one above
- Example stack:
  - Hardware: bytes in memory, blocks on disk
  - OS: files, processes
  - Database: rows, documents, nodes
  - Application: objects (User, Order, Product)
  - API: resources, DTOs
  - UI: screens, components

- Every layer is a translation. **Choosing the wrong model at one layer leaks pain into every layer above it.** This is why data modeling matters more than almost any other engineering decision.

---

## Why NoSQL emerged (circa 2010s)

Four forcing functions:

1. **Scalability needs** that relational DBs struggled with at the time (sharding was hard, cross-shard joins harder)
2. **Preference for open-source** over expensive enterprise systems (Oracle, DB2)
3. **Specific query patterns** that relational didn't fit well (full-text search, graph traversal, time-series)
4. **Developer frustration** with the object-relational impedance mismatch

**Important nuance:** "NoSQL" is not one thing. It's an umbrella covering:
- Document stores (MongoDB, Couchbase)
- Key-value stores (Redis, DynamoDB)
- Column-family stores (Cassandra, HBase)
- Graph databases (Neo4j, Neptune)

Each exists for a different reason. Lumping them is a mistake.

---

## The relational model

### What it is
- Data organized as **relations** (tables), each containing **tuples** (rows)
- Rows accessed by **primary key**; relationships between tables via **foreign keys**
- Multiple tables combined via **JOINs** to produce composite views
- Query language: SQL (declarative — you say WHAT you want, the engine decides HOW)

### Data types in a tuple
- Primitives: string, int, float, boolean, date
- Later additions: JSON columns (Postgres, MySQL) — allows semi-structured data within a relational schema

### Strengths
- Mature, understood, battle-tested for 40+ years
- Flexible joins — can combine data in ways not anticipated at design time
- Strong consistency guarantees (ACID)
- Rich tooling, universal query language

### Weaknesses
- **Impedance mismatch** with OOP applications (see below)
- Schema changes can be painful at scale
- Historically weaker at horizontal scaling (improving: Cockroach, Spanner, Aurora)
- JOINs become expensive on huge tables

---

## The document model

### What it is
- Data stored as **self-contained documents**, usually JSON or BSON
- Each document is a tree: nested objects, arrays, primitives
- No enforced schema (schema-on-read vs schema-on-write)
- Query via document paths, map-reduce, or vendor-specific DSLs

### Strengths
- **Natural fit for hierarchical data** owned by a single entity (a resume, a product listing, a blog post)
- **Better locality** — related data is physically stored together, one read gets everything
- **No impedance mismatch** — document maps directly to application objects
- Schema flexibility helps during rapid iteration

### Weaknesses
- **Poor at many-to-many** relationships (requires app-level joins)
- Updates to nested data can be awkward
- No standard query language across vendors
- Schema flexibility can become schema chaos without discipline

---

## The object-relational impedance mismatch

### The problem
Modern applications are written in object-oriented languages (Python, Java, TypeScript). Objects have:
- Nested structure (a User HAS-A list of Addresses)
- Inheritance
- Methods
- References/pointers

Relational databases have:
- Flat tables
- No nesting (natively)
- No inheritance
- Foreign keys (not pointers)

**Mapping between the two requires a translation layer** — this is what ORMs (SQLAlchemy, Hibernate, ActiveRecord) do. They never do it perfectly. The gap costs performance and developer time.

### The LinkedIn profile example (expanded)
A user has:
- One name, one DOB
- Multiple educations (one-to-many)
- Multiple past jobs (one-to-many)
- Multiple addresses (one-to-many)

**In relational:**
- `users` table (user_id, name, dob)
- `educations` table (education_id, user_id, school, year)
- `jobs` table (job_id, user_id, company, role, dates)
- `addresses` table (address_id, user_id, line1, city, country)

To render one profile → 4 queries (or 1 query with JOINs returning cartesian product).

**In document:**
- One JSON document containing name, dob, and nested arrays for educations, jobs, addresses
- One query returns the whole profile. Great locality.

### When document wins (one-to-many)
Data that is **owned** by one entity and almost always accessed together. Resumes, product listings, blog posts with comments.

### When document struggles (many-to-many)
Example: both users AND companies are entities. A job connects a user to a company. If stored in the user document, the company data is duplicated across every user who worked there. If the company changes name, you update N documents.

**This is where document models hit their limits.** Many-to-many relationships push you back toward normalization — i.e., toward the relational model.

---

## Normalization vs denormalization

### Normalization (the relational default)
Store each piece of data **once**, reference it via foreign keys. Benefits:
- Updates in one place → consistency
- Smaller storage footprint
- Changes to one entity don't cascade

### Denormalization (the document default)
**Duplicate data** across documents for faster reads. Benefits:
- One query returns everything you need
- Better locality (data physically together)
- No joins

### The tradeoff
- Reads vs writes
- Consistency vs performance
- Flexibility vs locality

**No universal answer.** The right choice depends on **read-to-write ratio**, **query patterns**, and **tolerance for inconsistency during updates**.

(Note on your "performance comparison I don't understand yet" — this is covered more in Ch 3 (Storage and Retrieval) and Ch 7 (Transactions). Mark it and keep moving. It'll click later.)

---

## Historical arc (why this matters)

- **1970s-80s:** Hierarchical and network databases (IMS, CODASYL) dominate. Pointers between records. Rigid.
- **1980s-2000s:** Relational wins decisively — flexibility, universal query language.
- **2000s-2010s:** Document and NoSQL emerge for scale + impedance pain.
- **2010s-today:** **Convergence.** Postgres adds JSON columns. MongoDB adds transactions. Boundaries blurring.

**Interview takeaway:** "relational vs NoSQL" is often a false binary now. Modern Postgres with JSONB handles 90% of document use cases. The real question is query shape, consistency needs, and scale.

---

## When I'd choose each

### Relational (Postgres, MySQL)
- Data has many-to-many relationships
- Queries are varied and unpredictable (ad-hoc analytics)
- Strong consistency matters (financial, inventory)
- Default choice when unsure — the ecosystem is unmatched

### Document (MongoDB, Couchbase)
- Data is naturally hierarchical and single-owner
- Schema evolves rapidly
- Reads are mostly "fetch one document's worth"
- Scale demands easy horizontal sharding

### Graph (Neo4j, Neptune)
- Data is highly interconnected (social, fraud, recommendations)
- Queries are "traverse N hops from X"
- Relationships are first-class citizens

---

## Aha moments
- **"Software is layers of data models"** — I'd never framed it this way. Explains why early schema decisions have outsized long-term cost.
- **Document vs relational isn't about "flexibility vs rigidity"** — it's about *what you're optimizing for in your access pattern.*
- **NoSQL isn't one thing** — I'd been using it as a monolith; the four categories do different jobs.

---

## Questions still open (to revisit later)
- Exact performance tradeoff: 4-table JOIN vs 1 denormalized document for a "fetch user profile" query. Covered in Ch 3?
- How do modern Postgres JSONB columns compare to native MongoDB performance? Is one strictly better?
- When should the SAME application use BOTH relational and document stores (polyglot persistence)?

---

## Where I've seen this at AB-InBev (my DE work)
- Snowflake tables we query are relational — many-to-many, ad-hoc queries, analytics
- Would the LinkedIn-profile use case fit better as documents? Probably — write-once per user, read-whole, one owner.

---

## Interview-grade summary — "When would you use document vs relational?"
"It depends on data shape and access pattern.

Choose **document** when the data is hierarchical and owned by a single entity — things that are naturally retrieved as a whole unit (profiles, product listings, blog posts with comments). You get better locality and no impedance mismatch with your application objects.

Choose **relational** when relationships are many-to-many, when queries are varied and ad-hoc, or when strong consistency across entities matters. The join flexibility is unmatched.

Modern caveat: the line has blurred. Postgres with JSONB columns covers many document use cases while keeping relational power. For most new projects I'd start relational and introduce document stores only for specific hot paths that justify them."

### Normalization vs duplication (expanded understanding)

**The core question:** store the thing, or a reference to the thing?

**Store the string directly:**
- "Alice lives in Greater Seattle Area" (string duplicated across 10M users)
- Pro: no join needed, simpler query, better locality
- Con: name change → update 10M rows → risk inconsistency; free-text leads to inconsistent spelling; localization is painful

**Store an ID referencing a central table:**
- Users hold `region_id: 42`; regions table holds `(42, "Greater Seattle Area")`
- Pro: single source of truth, atomic rename, canonical spelling, easy localization
- Con: requires a join to display; adds query complexity

**Rule of thumb:** if the value could be stored in one place, storing it in many places means the schema isn't normalized.

**The chapter's thesis around this:**
- Document DBs handle one-to-many (tree) data owned by one entity beautifully
- Document DBs struggle with many-to-one and many-to-many because joins are weak
- Relational DBs make normalization and joins the default — this is their strength
- Apps start tree-shaped, become graph-shaped as features are added — this is why document models often become painful over time

**For Google interviews:**
- When asked "design X's data model," always reason about which fields need to be normalized (likely to change, referenced by many) vs denormalized (truly owned, rarely changes)
- Example: LinkedIn's user.region → normalize (region names change, used by many). User.date_of_birth → store directly (immutable, owned by that user).