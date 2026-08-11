# Catch App Training Dataset — Schema & Protocol v1
*Shared dataset: Barrett (Polk County, FL) + Nick (Texas). Goal: a labeled fishing-outcome dataset good enough to train a local model — the asset no app sells.*

## The record (one row per fishing event)
Every entry is a labeled example: **features** (conditions) → **label** (result).

### Label
| field | values | meaning |
|---|---|---|
| `result` | `catch` / `none` | catch = fish landed; none = skunked trip (REQUIRED — a model can't learn without negatives) |

### Features (auto-captured by the app at log time)
| field | type | source |
|---|---|---|
| `tempF` | float | NOAA hourly |
| `windMph` | float | NOAA hourly |
| `cloudPct` | float | NOAA hourly |
| `precipPct` | float | NOAA hourly |
| `moonAge` | float (days) | astronomical calc |
| `moonIllum` | float 0–1 | astronomical calc |
| `solunarTransitHr` | float | astronomical calc |
| `sunriseHr` / `sunsetHr` | float | solar calc |
| `spawn` | 0/1 | regional spawn rule |
| `predictedScore` | int 0–100 | app scoring engine |
| `hour` | int 0–23 | device clock |
| `month` | int 1–12 | device clock |
| `lat` / `lon` | float | lake/custom spot |
| `species` | string | user select |
| `lure` | string | user text |
| `size` | string | user text (catch only) |
| `notes` | string | user text |
| `contributor` | string | added at merge: barrett / nick |

### Derived features (computed at merge, not logged)
- `lightWindow` — 1 if hour within 1.5h of sunrise/sunset, else 0
- `windBand` — calm (<4) / light (4–12) / high (>12)

## Collection protocol (weekly)
1. **Fish, then log immediately** — catch OR trip. Logging tomorrow from memory corrupts the conditions.
2. **Run the forecast first** before logging when possible — entries without `predictedScore` lose their most useful feature.
3. **Sunday night:** Nick hits **Export Training Data** → texts the CSV to Barrett.
4. Merge: `python3 merge_dataset.py barrett.csv nick.csv` → produces `master.csv`, `master.json`, `dataset_report.txt`.

## Quality rules
- **No fabricated entries, ever.** Fifty real rows beat five hundred fake ones. A poisoned dataset is worse than none.
- No PII in `notes` — no customer names, no addresses. Water names are fine.
- Skunked trips should be roughly 30–50% of the dataset. If you're at 100% catches, the model will learn nonsense.
- Same lake = same name every time (the merge tool normalizes case/whitespace).

## Milestones
- **50 rows:** first pattern read (best hours, best lakes per contributor)
- **200 rows:** simple model viable (logistic regression / decision tree on `result`)
- **500+ rows:** per-lake models — the actual product
