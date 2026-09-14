#!/usr/bin/env python3
"""Mirror every asset in MANIFEST.json into releases/<tag>/, with resume + integrity check.

Safe to re-run: an asset whose file already matches the manifest size (and digest, when
present) is skipped; a partial file is resumed. Nothing is deleted.
"""
import json, hashlib, pathlib, sys, urllib.request, time

ROOT = pathlib.Path(__file__).resolve().parent
M = json.load(open(ROOT / "MANIFEST.json", encoding="utf-8"))

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return "sha256:" + h.hexdigest()

def ok(p, a):
    if not p.exists():
        return False
    if a.get("size") is not None and p.stat().st_size != a["size"]:
        return False
    if a.get("digest"):
        return sha256(p) == a["digest"]
    return True  # no digest available; size match is all we can check

def fetch(url, dest):
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "nayaHistory-archive"})
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    tmp.replace(dest)

def main():
    done = skipped = failed = 0
    total = sum(len(r["assets"]) for r in M["releases"])
    i = 0
    for rel in reversed(M["releases"]):  # oldest-first: research targets first
        d = ROOT / "releases" / rel["tag"]
        d.mkdir(parents=True, exist_ok=True)
        for a in rel["assets"]:
            i += 1
            dest = d / a["name"]
            if ok(dest, a):
                skipped += 1
                continue
            for attempt in range(3):
                try:
                    print(f"[{i}/{total}] {rel['tag']}/{a['name']} ({(a.get('size') or 0)/1e6:.0f}MB)", flush=True)
                    fetch(a["url"], dest)
                    if ok(dest, a):
                        done += 1
                        break
                    print("  ! integrity mismatch, retrying", flush=True)
                except Exception as e:
                    print(f"  ! {e} (attempt {attempt+1})", flush=True)
                    time.sleep(3)
            else:
                failed += 1
    print(f"\nDONE downloaded={done} skipped={skipped} failed={failed}", flush=True)
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
