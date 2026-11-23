# pg-ops

Training project for the Motopp Rabobank interview preparation (Block 2: DBA DevOps Engineer).
A PostgreSQL primary and replica in Docker, plus a small Python package with database tools.

**Starter kit version 1.0** (from `block2-starter-v1.0.zip`). All data is invented.

## Start

```powershell
docker compose up -d
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS: source .venv/bin/activate
pip install -e ".[dev]"
python -m pg_ops.migrate
python -m pg_ops.load_data
```

Open psql on the primary: `docker compose exec primary psql -U postgres -d delivery`

Stop and delete everything (also the data): `docker compose down -v`
