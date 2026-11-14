# DDIA Ch 2 — Document vs Relational Databases + Locality

## Core comparison

Document databases model data as nested trees — one document holds all related data together. Relational databases model data as flat tables, with relationships expressed through foreign keys and resolved at query time via joins.

The headline tradeoff is **locality vs flexibility**: document DBs win for whole-document reads and schema evolution; relational DBs win for joins, normalization, and query optimization. **Neither is universally faster** — the winner depends on the dominant access pattern, which is why modern databases (Postgres JSONB, MongoDB with joins) increasingly blur the line.

## Where documents win

- **Schema flexibility (schema-on-read).** Documents don't enforce schemas at write time. The application interprets structure at read time. Fast schema evolution; validation is deferred to the application layer.
- **Locality for whole-document reads.** Data is stored contiguously (JSON, XML, or BSON). Fetching the whole document is one disk read, no joins. Big win when the access pattern consistently touches the full document.
- **Match for object-structured application code.** Document shape mirrors how objects live in application memory. Reduces the **object-relational impedance mismatch** — the translation cost between relational tables and in-memory object graphs that ORMs (Hibernate, SQLAlchemy) exist to solve.

## Where documents struggle

- **Many-to-many relationships.** Documents are trees; many-to-many relationships are graphs. Documents model trees well and fake graphs badly. *Example:* if LinkedIn stored company data inside each employee's document, changing Google's logo would require updating every Google employee's document. In a relational model, employees reference a shared company row — the logo update happens once, and every join picks it up automatically.
- **Partial updates (write amplification).** Updating a nested field often requires rewriting the full document, especially if encoded size changes. Write-heavy workloads suffer. Partial-update features exist (MongoDB's WiredTiger) but are optimizations, not guarantees.
- **Nested field access requires full paths.** Reading or filtering a deeply-nested field requires explicit path syntax (`user.education.0.institution`). More awkward than relational queries. Modern document DBs support projection (reading just specific nested fields), but updates and many-to-many filtering across embedded arrays remain hard.
- **Silent data quality issues.** No schema on write means bad data enters the system undetected and surfaces far from where it was introduced. For mission-critical data (payments, user accounts), rigid schema becomes a feature, not a bug.

## Locality — the deeper insight

**Locality is a physical storage concern, not a property of the data model.** The "documents have locality" argument confuses logical structure with physical layout. Relational databases can achieve locality too:

- **Google Spanner** supports interleaved tables — related rows from different tables can be physically stored next to each other. Relational schema with document-like locality.
- **Bigtable and Cassandra** use a wide-column model — related columns stored together in column families. A single row can have thousands of columns, grouped for locality.
- **Postgres with JSONB** is often the balanced choice in 2026: relational maturity + document-shaped columns where locality matters. Query planner + joins when needed, nested documents when the access pattern calls for it.

**Takeaway:** modern systems decouple logical model (relational / document / graph) from physical storage layout. Choosing a "document database" because you want locality is often a mistake — you can get locality in a relational DB by choosing the right physical schema.

## Key terminology

- **Schema-on-read vs schema-on-write** — when structure is validated
- **Impedance mismatch** — the gap between relational tables and in-memory object graphs
- **Locality** — related data physically stored together on disk
- **Write amplification** — small logical updates causing large physical writes
- **Wide-column** — Bigtable/Cassandra model with column families
- **BSON** — MongoDB's binary JSON encoding, faster to parse than text JSON

## My DE/AI lens

- **Bronze layer** = document-shaped (raw JSON events ingested without schema enforcement)
- **Silver/gold layers** = usually relational (normalized for analytics joins and BI tools)
- **Vector DBs** (Chroma, Qdrant, Weaviate) = document-shaped under the hood — each embedding is a vector plus nested metadata
- **Lakehouse formats** (Delta, Iceberg) = choice happens per column, not per database — you can store nested structures inside Parquet columns when it fits the access pattern

The "document vs relational" question rarely has a per-database answer anymore. **It's a per-table, per-column, per-access-pattern decision.**