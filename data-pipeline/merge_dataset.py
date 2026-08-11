#!/usr/bin/env python3
"""
merge_dataset.py — Merge Catch App training CSVs into a master dataset.
Usage: python3 merge_dataset.py <file1.csv> [file2.csv ...]
Outputs: master.csv, master.json, dataset_report.txt (in current directory)
Contributor name is inferred from filename (barrett*.csv -> barrett, nick*.csv -> nick).
"""
import csv, json, sys, os, re
from collections import Counter

FEATURE_COLS = ['tempF','windMph','cloudPct','precipPct','moonAge','moonIllum',
                'solunarTransitHr','spawn','predictedScore','hour','month','lat','lon']
ALL_COLS = ['when','lake','species','size','lure','result'] + FEATURE_COLS + \
           ['sunriseHr','sunsetHr','notes','contributor','lightWindow','windBand']

def contributor_of(path):
    base = os.path.basename(path).lower()
    m = re.match(r'([a-z]+)', base)
    return m.group(1) if m else 'unknown'

def fnum(v):
    try: return float(v)
    except: return None

def wind_band(w):
    if w is None: return ''
    return 'calm' if w < 4 else ('light' if w <= 12 else 'high')

def light_window(hour, rise, set_):
    if hour is None or rise is None or set_ is None: return ''
    return 1 if (abs(hour - rise) <= 1.5 or abs(hour - set_) <= 1.5) else 0

def load(path):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            row = {c: (r.get(c) or '').strip() for c in ALL_COLS}
            row['lake'] = re.sub(r'\s+', ' ', row['lake']).strip()
            row['result'] = row['result'].lower()
            if row['result'] not in ('catch','none'): continue
            row['contributor'] = contributor_of(path)
            hr = fnum(row['hour']); rise = fnum(row['sunriseHr']); set_ = fnum(row['sunsetHr'])
            row['lightWindow'] = light_window(hr, rise, set_)
            row['windBand'] = wind_band(fnum(row['windMph']))
            rows.append(row)
    return rows

def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        key = (r['when'], r['lake'].lower(), r['result'], r['contributor'])
        if key in seen: continue
        seen.add(key); out.append(r)
    return out

def main():
    files = sys.argv[1:]
    if not files:
        print(__doc__); sys.exit(1)
    rows = dedupe([r for f in files for r in load(f)])
    if not rows:
        print('No valid rows found.'); sys.exit(1)
    # deterministic 80/20 split
    rows_sorted = sorted(rows, key=lambda r: (r['when'], r['lake'], r['result']))
    split = max(1, int(len(rows_sorted) * 0.8))
    train, valid = rows_sorted[:split], rows_sorted[split:]
    with open('master.csv','w',newline='') as f:
        w = csv.DictWriter(f, fieldnames=ALL_COLS); w.writeheader()
        w.writerows(rows_sorted)
    with open('master.json','w') as f:
        json.dump({'train': train, 'validation': valid, 'total': len(rows)}, f, indent=1)
    # report
    res = Counter(r['result'] for r in rows)
    con = Counter(r['contributor'] for r in rows)
    lakes = Counter(r['lake'] for r in rows)
    catches = [r for r in rows if r['result']=='catch']
    scored = [float(r['predictedScore']) for r in catches if fnum(r['predictedScore']) is not None]
    lines = [
        f"DATASET REPORT — {len(files)} file(s) merged",
        f"Total rows: {len(rows)}  (train {len(train)} / validation {len(valid)})",
        f"Labels: catch={res['catch']} none={res['none']}  (neg ratio {res['none']/len(rows):.0%})",
        f"Contributors: {dict(con)}",
        f"Top waters: {lakes.most_common(5)}",
    ]
    if scored:
        lines.append(f"Avg predictedScore on catches: {sum(scored)/len(scored):.1f} (model check)")
    with open('dataset_report.txt','w') as f:
        f.write('\n'.join(lines))
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
