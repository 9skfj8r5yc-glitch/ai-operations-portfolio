# AI Operations Portfolio — Barrett Tate

Production AI systems I designed, built, and operate. Everything here runs (or ran) in a live business.

## What's inside

### `/catch-app` — Catch App (live at catchapp.com)
A zero-dependency, single-file web app for fishing forecasts:
- Live NOAA/NWS + USGS Water Data API integration (keyless)
- Custom solunar/sunrise astronomy engine (pure JS)
- Evidence-weighted scoring model (temperature/stability 40%, light windows 30%, wind/precip 20%, solunar 10%)
- All 50 states, 180+ waters, custom lat/lon spots, regional spawn logic
- Pond habitat scanner, labeled catch/trip logging (14 auto-captured condition features), CSV/JSON training-data export, shareable forecast links via URL hash state

### `/data-pipeline` — Labeled training-data tooling
- `merge_dataset.py` — merges contributor CSVs into master datasets: dedupe, normalization, derived features, 80/20 train/validation split, dataset report
- `SCHEMA.md` — the dataset spec: feature types, label rules, collection protocol, quality gates (no fabricated rows, 30–50% negative samples)

## Also in production (not public here)
- Self-hosted LLM agent stack (OpenClaw + Moonshot/Kimi API): 10-role agent roster with scoped permissions, human-in-the-loop QC, approval gates, audit logs — running a real company's back office daily.

## Contact
Barrett Tate · Lakeland, FL · (863) 272-0602 · BarrettTate@hotmail.com
Open to remote AI operations / automation roles.
