# PyPI Readiness Audit for meta-rag

## Context

The package is structurally sound (src-layout, hatchling, tests, types, good README) but is missing PyPI metadata that affects discoverability, and has a few usability gaps that would trip up users installing from PyPI.

---

## 1. Add missing PyPI metadata to `pyproject.toml`

**File:** `pyproject.toml`

Add the following fields after the existing `requires-python` line:

- **`license`** — `"Apache-2.0"` (SPDX identifier, PEP 639 style)
- **`keywords`** — `["rag", "retrieval-augmented-generation", "metadata", "llm", "openai", "chromadb", "schema", "sql"]`
- **`classifiers`** — Development Status Alpha, Python 3.11/3.12/3.13, Apache License, AI topic, Typing :: Typed
- **`[project.urls]`** — Homepage, Repository, Changelog, Issues (all pointing to `github.com/cagriy/meta-rag`)

---

## 2. Pin dependency version floors

**File:** `pyproject.toml`

The code uses `openai.OpenAI()` (v1+ only) and ChromaDB's `PersistentClient` (v0.4+ only). Without floors, `pip install meta-rag` could resolve ancient versions that fail at runtime.

```toml
dependencies = [
    "openai>=1.0",
    "chromadb>=0.4",
    "python-dotenv>=0.19",
]
```

No upper bounds — they cause dependency hell for libraries.

---

## 3. Add `[project.optional-dependencies]` for pip users

**File:** `pyproject.toml`

```toml
[project.optional-dependencies]
dev = ["pytest"]
```

Keeps existing `[dependency-groups]` for `uv` users, adds `pip install meta-rag[dev]` support.

---

## 4. Fix stale README API reference

**File:** `README.md`

- Fix `llm_model` default: table says `"gpt-4o"` but code says `"gpt-4o-mini"`
- Add missing `extraction_model` parameter (added in v0.1.3) to both the signature block and the parameter table
- Update description of `llm_model` (no longer used for extraction)

---

## 5. Complete the `RelationalStore` ABC

**File:** `src/meta_rag/stores/base.py`

`MetaRAG` calls 6 methods on `relational_store` that aren't in the ABC:

- `get_schema_from_db()`
- `add_column(field)`
- `drop_column(field_name)`
- `get_empty_fields()`
- `get_unpopulated_fields(schema)`
- `update_metadata_field(doc_id, field_name, value)`

Plus 2 more called by `IngestionPipeline`:

- `get_document_hash(doc_id)`
- `set_document_hash(doc_id, content_hash)`

Add these as `@abstractmethod` stubs. Without this, anyone implementing a custom store would pass type checks but get `AttributeError` at runtime.

---

## 6. Widen constructor type hints to abstract base classes

**Files:** `src/meta_rag/__init__.py`, `README.md`

Change `MetaRAG.__init__` signature:

```python
# Before
vector_store: ChromaVectorStore | None = None,
relational_store: SQLiteRelationalStore | None = None,

# After
vector_store: VectorStore | None = None,
relational_store: RelationalStore | None = None,
```

- Import `VectorStore` and `RelationalStore` from `meta_rag.stores.base`
- Export them in `__all__`
- Update README API reference table to use abstract type names

---

## Verification

1. Run `uv run pytest` — all existing tests must pass
2. Run `uv build` — confirm the package builds without errors
3. Spot-check: `uv run python -c "from meta_rag import MetaRAG, VectorStore, RelationalStore; print('OK')"` — confirm new exports work
