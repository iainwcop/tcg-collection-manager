# TCG Collection Manager — Design Document

> Initial design for a full-stack, multi-user trading card collection management application.

## 1. Purpose

**TCG Collection Manager** is a web application for organizing, searching, and managing trading card collections across any supported game (Pokémon, Magic: The Gathering, Yu-Gi-Oh!, etc.). The primary audience is collectors who need flexible tooling to mirror how they physically store cards — binders, boxes, custom layouts — while gaining digital benefits: fast lookup, filtering, quantity tracking, live market values, and quick card intake via scanning.

The system is **multi-tenant by design**: every user owns isolated collections and organizational structures. There is no shared collection state between users unless explicitly introduced later (e.g. public trade lists).

### Core product offering

These three pillars define what the product *is*, not optional add-ons:

| Pillar | Description |
|--------|-------------|
| **Collection management** | Multi-user collections, flexible storage formats (binders, boxes, custom), rich sort & filter |
| **Card scanning** | Capture cards via camera or image upload; match to catalog and add to inventory |
| **Live market pricing** | Current and historical prices per card; collection value summaries |

Additional capabilities (deckbuilding, import/export, marketplace) may follow, but the above three are the core value proposition.

### Build phasing

We build in phases. **Phase 1 (initial build)** delivers collection management only — the foundation everything else depends on. Scanning and pricing are core offerings deferred to later phases, not descoped from the product.

| Phase | Scope | Rationale |
|-------|-------|-----------|
| **Phase 1** | Auth, catalog, collections, storage units, sort & filter | Establishes domain model and APIs that scanning/pricing plug into |
| **Phase 2** | Card scanning | Requires stable `CardDefinition` matching and instance creation flow |
| **Phase 3** | Live market pricing | Requires catalog linkage and collection inventory to surface value |
| **Later** | Deckbuilding, import/export, mobile apps, trading | Valuable extensions beyond the core trio |

### Phase 1 goals

| Goal | Description |
|------|-------------|
| **Multi-user collections** | Sign up, authenticate, and manage one or more personal collections |
| **Flexible organization** | Model real-world storage: binders (pages/slots), boxes, loose piles, custom groupings |
| **Rich sort & filter** | Find cards by name, set, rarity, location, condition, quantity, tags, etc. |
| **Card catalog** | Reference a shared card database (set, number, image) separate from owned copies |
| **Scan/pricing-ready schema** | Data model and APIs designed so scanning and pricing integrate without rework |
| **Local-first dev** | Run the full stack on a developer machine with minimal setup |
| **Cloud-ready** | Architecture and deployment path that scales to hosted production |

### Out of scope (all phases for now)

- Deckbuilding and legality checking
- Mobile-native apps
- Marketplace / trading between users

---

## 2. Core concepts

Understanding the domain model early keeps the schema and API stable as features grow.

```
User
 └── Collection(s)          # e.g. "Main Pokémon", "MTG Standard"
      └── StorageUnit(s)    # Binder, Box, Custom container
           └── Slot(s)      # Page/row position, box section, etc.
                └── CardInstance(s)   # A physical copy the user owns
```

| Concept | Description |
|---------|-------------|
| **User** | Account with auth credentials and preferences |
| **Collection** | A named grouping of cards (often one per game or purpose) |
| **StorageUnit** | A physical or logical container: binder, box, deck box, custom |
| **Slot** | A position within a storage unit (binder page + slot, box row, etc.) |
| **CardDefinition** | Canonical card data from a catalog (name, set, number, image URL) — shared across all users |
| **CardInstance** | A user-owned copy: links to CardDefinition + condition, quantity, notes, location (StorageUnit/Slot) |

**Key design choice:** separate **catalog** (what the card is) from **inventory** (what the user owns). Both **scanning** and **pricing** resolve against `CardDefinition`; collection management operates on `CardInstance`. Building this split in Phase 1 is intentional — it is what makes scanning and pricing straightforward to add in Phases 2 and 3.

---

## 3. Feature breakdown

### 3.1 Organization & storage formats

Users should be able to model how they actually store cards:

| Format | Structure | Example |
|--------|-----------|---------|
| **Binder** | Pages × slots per page | 9-pocket binder, page 3 slot 7 |
| **Box** | Sections or unordered pile | "Bulk rares box", "Set storage" |
| **Custom** | User-defined hierarchy | "Trade binder" → tabs → slots |
| **Unassigned** | Cards not yet placed | Inbox / staging area |

Operations: create/rename/delete units, move cards between slots, bulk move, duplicate detection (same card in multiple locations).

### 3.2 Sorting & filtering

**Sort** by: name, set, collector number, rarity, date added, location, quantity, custom order (manual drag within a view).

**Filter** by: game, set, rarity, condition, location (unit/slot), tags, text search (fuzzy), "unassigned only", quantity thresholds.

Views: table, grid (with card images), location tree (browse by binder → page → slot).

### 3.3 Multi-user & security

- Email/password auth (OAuth providers can be added later)
- All collection data scoped to `user_id`; API enforces ownership on every mutation
- Optional: admin interface for catalog curation and user support

### 3.4 Card catalog

A maintained reference database of card definitions, seeded from public APIs or import files (Scryfall for MTG, Pokémon TCG API, etc.). Users do not duplicate catalog data — they link instances to definitions.

### 3.5 Card scanning *(core offering — Phase 2)*

- Web or mobile camera capture, or image upload
- Image processing / recognition service matches against `CardDefinition`
- User confirms match, sets quantity/condition, assigns to collection location
- Bulk scan sessions for rapid inventory intake

### 3.6 Live market pricing *(core offering — Phase 3)*

- Scheduled jobs pull prices from game-specific APIs (Scryfall, TCGPlayer, etc.)
- Price snapshots stored per `CardDefinition` with timestamp and source
- Collection views show per-card and total portfolio value
- Historical price trends on card detail pages

---

## 4. Technology stack

### 4.1 Recommended stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Backend** | **Django 5** + **Django REST Framework** | Batteries-included auth, ORM, migrations, admin panel, and mature ecosystem suit a data-heavy management tool. Admin is valuable for catalog curation. |
| **Frontend** | **React 18** + **TypeScript** + **Vite** | Fast dev server, strong typing, large ecosystem. SPA fits rich interactive sorting/filtering UIs. |
| **Database** | **PostgreSQL 16** | Relational model fits hierarchical storage + inventory; JSONB for flexible metadata; excellent Django support; standard for cloud hosts. |
| **API style** | REST (JSON) | Simple, well-understood; GraphQL can be reconsidered if client query complexity grows |
| **Auth** | Django auth + JWT or session cookies | JWT suits SPA + API; sessions are simpler for same-origin deploys. Decide at boilerplate time. |
| **Local dev** | Docker Compose | Postgres + backend + frontend in one `docker compose up` |
| **Production** | Containerized deploy | Railway, Render, Fly.io, or AWS/GCP — all support Docker + Postgres |

### 4.2 Why Django over FastAPI (for this project)

Both are valid. **Django is recommended for v1** because:

- Built-in **user auth**, **permissions**, and **admin** reduce boilerplate for a multi-user management app
- **Migrations and ORM** handle complex relational models (users → collections → units → slots → instances) without assembling an async stack from scratch
- **Django REST Framework** provides serializers, viewsets, filtering (`django-filter`), and pagination out of the box

**FastAPI** would be a strong choice if the team prioritizes async I/O, OpenAPI-first design, or plans heavy real-time/WebSocket features early. It would require adding SQLAlchemy/Alembic, auth library, and admin separately. A migration path exists later if needed.

### 4.3 Why PostgreSQL

- Hierarchical and relational data map naturally to foreign keys and nested queries
- `JSONB` columns for extensible card metadata and user-defined fields without schema churn
- Full-text search (`tsvector`) for card name lookup before adding Elasticsearch
- Managed Postgres is cheap and ubiquitous on every cloud platform

**Alternatives considered:** SQLite (fine for solo dev, weak for concurrent multi-user production); MongoDB (flexible but weaker for relational inventory + location integrity).

### 4.4 Frontend tooling (planned)

| Tool | Purpose |
|------|---------|
| **TanStack Query** | Server state, caching, optimistic updates |
| **TanStack Table** | Sortable, filterable data grids |
| **React Router** | Client-side routing |
| **Tailwind CSS** or **shadcn/ui** | Consistent UI components |

---

## 5. High-level architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        React SPA (Vite)                      │
│   Collections · Binders · Search · Filters · Scan · Prices  │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS / JSON (REST)
┌────────────────────────────▼────────────────────────────────┐
│              Django + Django REST Framework                  │
│   Auth · Collections API · Catalog API · Pricing · Scan     │
└────────────────────────────┬────────────────────────────────┘
                             │ SQL
┌────────────────────────────▼────────────────────────────────┐
│                     PostgreSQL                               │
│   users · collections · storage_units · card_instances ·     │
│   card_definitions · price_snapshots · scan_sessions         │
└─────────────────────────────────────────────────────────────┘
```

### Repository layout (proposed)

```
tcg-collection-manager/
├── backend/                 # Django project
│   ├── apps/
│   │   ├── users/
│   │   ├── collections/     # storage units, slots, instances
│   │   └── catalog/         # card definitions, sets, games
│   ├── config/              # settings, urls, wsgi
│   └── manage.py
├── frontend/                # React + Vite + TypeScript
│   └── src/
├── docs/                    # design & ADRs
├── docker-compose.yml       # local full stack
└── README.md
```

### Deployment topology (production)

```
[CDN / static host]  →  React build artifacts
[App host]           →  Django (Gunicorn/Uvicorn) container
[Managed DB]         →  PostgreSQL
[Object storage]   →  Card images (optional; can hotlink catalog URLs initially)
```

Environment variables for secrets (`DATABASE_URL`, `SECRET_KEY`, `ALLOWED_HOSTS`). CI runs tests and builds Docker images.

---

## 6. Later expansion (beyond core offering)

| Feature | Integration approach |
|---------|---------------------|
| **Deckbuilding** | New `Deck` entity; cards pulled from `CardInstance` or catalog; format legality rules per game |
| **Import/export** | CSV and platform formats (Deckbox, TCGPlayer collection) |
| **Multi-game** | `Game` enum/table on catalog; collection scoped to one or more games |

Phase 1 schema should not block core scanning or pricing: keep `CardDefinition` game-agnostic with a `game` field, and reserve tables for `PriceSnapshot` and `ScanSession` keyed to definitions and users.

---

## 7. Initial data model (sketch)

```text
Game            id, name, slug
CardSet         id, game_id, name, code, release_date
CardDefinition  id, set_id, name, collector_number, rarity, image_url, metadata (JSONB)

User            id, email, password_hash, ...
Collection      id, user_id, name, game_id (optional), created_at
StorageUnit     id, collection_id, type (binder|box|custom), name, config (JSONB)
Slot            id, storage_unit_id, parent_slot_id (nullable), label, sort_order
CardInstance    id, collection_id, card_definition_id, slot_id (nullable),
                quantity, condition, notes, tags (JSONB), acquired_at

# Phase 2+
ScanSession     id, user_id, collection_id, status, created_at
ScanResult      id, scan_session_id, image_url, matched_definition_id, confidence, ...

# Phase 3+
PriceSnapshot   id, card_definition_id, source, price_usd, recorded_at
```

Indexes: `(collection_id)`, `(card_definition_id)`, `(slot_id)`, full-text on `CardDefinition.name`.

Phase 1 implements the first block only; later tables are documented here so the initial schema leaves room for them.

---

## 8. Success criteria

### Phase 1 (initial build)

- [ ] User can register, log in, and log out
- [ ] User can create a collection and add storage units (binder, box)
- [ ] User can search the catalog and add card instances to a collection
- [ ] User can assign instances to slots and move them between locations
- [ ] User can sort and filter their inventory in the UI
- [ ] Data model supports future scanning and pricing without migration rework
- [ ] Full stack runs locally via Docker Compose
- [ ] Application deploys to at least one cloud target with Postgres

### Phase 2 — scanning (core offering)

- [ ] User can scan or upload a card image and get catalog match suggestions
- [ ] Confirmed scan adds a `CardInstance` to the user's collection

### Phase 3 — pricing (core offering)

- [ ] Card detail and collection views show current market price
- [ ] Collection summary shows total estimated value

---

## 9. Open decisions

These should be resolved during boilerplate setup:

| Decision | Options | Notes |
|----------|---------|-------|
| Auth mechanism | JWT vs session cookies | JWT common for SPA; sessions simpler if same domain |
| Catalog seed source | Scryfall API, Pokémon TCG API, manual import | May start with one game (e.g. Pokémon or MTG) |
| UI component library | shadcn/ui, MUI, Chakra | shadcn + Tailwind is lightweight and customizable |
| Monorepo vs split repos | Single repo (recommended) | Easier local dev and shared docs |
| Testing strategy | pytest (backend), Vitest + RTL (frontend) | Set up in boilerplate |

---

## 10. References & inspiration

- [Scryfall API](https://scryfall.com/docs/api) — MTG card data
- [Pokémon TCG API](https://pokemontcg.io/) — Pokémon card data
- Physical collection managers: TCGPlayer collection, Deckbox, Delver Lens (scanning)

---

*Document version: 0.2 — core offering includes scanning & pricing; Phase 1 is collection management only. Update as decisions are made and ADRs are added under `docs/adr/`.*
