#!/usr/bin/env python3
"""Re-verify every downloaded file against MANIFEST.json (size + GitHub sha256 digest)."""
import json, hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
M = json.load(open(ROOT / "MANIFEST.json", encoding="utf-8"))
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return "sha256:" + h.hexdigest()
missing = bad = good = nodigest = 0
for rel in M["releases"]:
    for a in rel["assets"]:
        p = ROOT / "releases" / rel["tag"] / a["name"]
        if not p.exists():
            print("MISSING", rel["tag"], a["name"]); missing += 1; continue
        if a.get("size") is not None and p.stat().st_size != a["size"]:
            print("SIZE   ", rel["tag"], a["name"]); bad += 1; continue
        if a.get("digest"):
            if sha256(p) != a["digest"]:
                print("DIGEST ", rel["tag"], a["name"]); bad += 1; continue
            good += 1
        else:
            nodigest += 1
print(f"\nok={good} size-only-ok(no digest)={nodigest} missing={missing} bad={bad}")
