# CMF Director's Console

The visual approval interface for the Conscious Movie Factory.

## Quick Start

```bash
cd "CMF labo/director_console"
pip install -r requirements.txt
streamlit run app.py
```

## Features

- **Dashboard**: Overview of all projects and batch status
- **Scripts Approval**: Review premises and scripts (Stage 1)
- **Assets Gallery**: Browse generated images and videos (Stage 2)
- **Composition Review**: Check VFX renders (Stage 3)
- **Audio Approval**: Preview audio mix (Stage 4)
- **Batch Management**: Create and manage batch runs

## Database

Uses SQLite (`cmf_database.db`) for local storage.
Migration to PostgreSQL supported via `DATABASE_URL` env var.

## Integration

Works with `/cmf-batch` workflow for 4-stage approval process.
