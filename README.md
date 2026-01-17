# Team Optimiser (AI-Driven Team & Group Allocation)

A production-minded Python project that generates **fair, balanced teams** from a pool of players using an optimisation engine and a learning feedback loop.  
Built as a **real SaaS-style backend** (Django + REST API), with the optimisation logic kept **framework-agnostic** for portability and reuse.

> Initial domain: amateur football (5/7-a-side).  
> Long-term direction: a generic **team & resource optimisation platform** (events, sports, cohorts, staffing-like scenarios).

---

## Why this exists

Anyone who organises weekly games knows the pain:
- balancing teams fairly
- avoiding the “stacked team” arguments
- handling late dropouts
- tracking who is improving over time

This project automates the process with an explainable baseline algorithm, then improves over time using historical outcomes.

---

## Key capabilities (current + planned)

### Current
- Deterministic team generation (same input → same output)
- Fairness scoring and team breakdown reports
- Clean architecture: optimisation engine separated from web/API layer
- Tests + formatting (CI-ready structure)

### Planned “AI” / learning
- Elo-style player rating updates using match outcomes (win/loss/draw)
- Optional adaptive attribute weighting based on historical balance

### Planned SaaS features
- Multi-tenant orgs (multiple groups/leagues)
- Session history and analytics
- Admin UI for maintaining players/attributes
- Export formatting for sharing teams in WhatsApp-friendly text

### Planned deployment paths
- AWS managed deployment first (e.g., ECS/App Runner)
- Kubernetes later (local k3d/kind first; optional EKS path)

---

## Tech stack

**Core**
- Python 3.12
- Optimisation engine (pure Python, framework-agnostic)

**Backend (planned)**
- Django + Django REST Framework
- PostgreSQL (prod), SQLite (dev)

**DevOps**
- Docker (planned)
- GitHub Actions CI (planned: lint + tests)
- IaC (planned: Terraform or AWS CDK)
- Observability (planned: structured logs + basic metrics)

---

## Architecture

This repo is intentionally split into two layers:

- **`engine/`** — pure Python business logic  
  _Team generation, constraints, fairness metrics, learning updates_

- **`backend/`** — Django + API surface (planned)  
  _Auth, organisations, persistence, REST endpoints, admin UI_

This keeps the optimisation logic reusable (CLI, web, batch jobs, future services).

---

## Repository structure

```text
team-optimiser/
├── engine/               # Pure optimisation engine (no Django imports)
│   ├── models.py          # Domain models (Player, Attributes, etc.)
│   ├── optimiser.py       # Team generation algorithms
│   ├── metrics.py         # Fairness metrics and reports
│   └── learning.py        # (planned) Elo + weight tuning
│
├── scripts/              # Local runners / helpers
├── tests/                # Unit tests for engine
│
├── deploy/               # (planned) deployment artefacts
│   ├── ecs/
│   └── k8s/
│
└── README.md
