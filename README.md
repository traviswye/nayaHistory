# nayaHistory

A preservation archive of **NayaTech/NayaFlow-releases** — the full public release
history of the NayaFlow desktop configurator for the Naya Create keyboard, captured
after the company went dark so the catalog is not lost if the repo disappears.

- **Source:** https://github.com/NayaTech/NayaFlow-releases
- **Scope:** all 25 releases, v0.0.1 (2025-03-19) through v1.25.1 (2026-07-21), every
  asset verbatim (~21.5 GB): Windows `.exe`, macOS `.dmg` + `.zip` (x64 + arm64),
  Linux `.AppImage`, plus the `.blockmap` and `latest*.yml` update metadata.

## Layout

```
MANIFEST.json      every release + asset: name, size, GitHub sha256 digest, URL, date
CHANGELOG.md       all release notes, newest first (14 of 25 carry notes)
changelogs/        the same notes, one file per version
releases/<tag>/    the downloaded binaries (gitignored; not in git)
verify.py          re-check every downloaded file against the manifest digest/size
```

`MANIFEST.json`, `CHANGELOG.md`, `changelogs/` and this README are the git-tracked
record. The binaries themselves are vendor material and stay out of git (`.gitignore`).

## Why the binaries matter beyond preservation

NayaFlow bundles **NayaCore.exe**, which carries the Create firmware as Qt resources
(this is how firmware 3.41.0 was recovered from 1.25.1). Older installers are larger
and less stripped, so early versions (0.0.1–0.1.1, ~1.2 GB each) are the best place to
look for anything the vendor exposed and later locked down — unencrypted firmware,
signing material, source maps, or debug symbols.

## Flash generation A vs B (context for the firmware)

The four keyboard firmware images are two halves × two **flash generations**. Gen B
carries the `_64` suffix (`kb_fwl_64.bin`). It is a hardware revision of the QSPI flash
part, not a word size: NayaCore reads the connected half's USB PID
(`Naya_Device::setCreateFlashGenerationFromPid`), decides gen A vs gen B, and flashes
the matching image, refusing if the generation is unknown. A given physical half
matches exactly one of the four images; they are not interchangeable.
