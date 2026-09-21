# nayaHistory

A preservation archive of **NayaTech/NayaFlow-releases** — the full public release
history of the NayaFlow desktop configurator for the Naya Create keyboard, captured
after the company went dark so the catalog is not lost if the repo disappears.

- **Source:** https://github.com/NayaTech/NayaFlow-releases
- **Scope:** all 25 releases, v0.0.1 (2025-03-19) through v1.25.1 (2026-07-21), every
  asset verbatim (~21.5 GB): Windows `.exe`, macOS `.dmg` + `.zip` (x64 + arm64),
  Linux `.AppImage`, plus the `.blockmap` and `latest*.yml` update metadata.
- **Also the firmware library for [OpenFlow](https://github.com/traviswye/openflow)**, which
  downloads images from `firmware-history/` at runtime — see
  [Firmware library for OpenFlow](#firmware-library-for-openflow) below for the contract that
  keeps that working.

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

## Firmware library for OpenFlow

`firmware-history/` is not only a preservation copy — it is the live source OpenFlow fetches
firmware from. OpenFlow ships a catalogue of every image (versions, sides, flash generations,
hashes) and none of the binaries: they are vendor material, and bundling 23 MB of them in an
installer is not a decision to make by accident. So the app holds the index and downloads the
file on demand, from here.

```
https://raw.githubusercontent.com/traviswye/nayaHistory/main/firmware-history/<path>
```

where `<path>` is the catalogue's `historyPath` for that image — `v1.25.1/kb_fwl.bin`,
`v1.21.0/module/FlashMemory.bin`, and so on. The repository is public, so no token is involved
and OpenFlow ships no credential of any kind.

**Every download is verified.** OpenFlow checks the bytes against the `blobSha256` its catalogue
recorded when the image was carved out of its release, and writes nothing that does not match.
A truncated transfer, a redirect to an HTML error page or a mirror holding a different build all
fail the same check. That is what makes fetching firmware over the network acceptable at all, and
it means this archive cannot silently hand anyone a different image than the one they asked for
— but it also means a file that MOVES becomes a file that cannot be found.

### The contract

The catalogue pins each image by **path and hash**. To keep OpenFlow working against this repo:

- **Do not move, rename or delete anything under `firmware-history/`.** A path is an identifier,
  not a location. Deleting one takes a version away from everybody running OpenFlow; renaming one
  does the same and looks like a network error while doing it.
- **Do not rewrite the contents of an existing file.** The hash is the identity. A file whose
  bytes change is a different image and must be a new path, not an edit.
- **Adding is always safe.** New releases, newly carved images, new firmware of our own: add the
  file, then add its catalogue entry in OpenFlow (`docs/reference/firmware-catalog.json`, with
  `historyPath` and `blobSha256`). An image with no catalogue entry is simply not offered; an
  entry with no file is reported as missing rather than breaking anything.

Verified 2026-09-21: 33 distinct images (the archive's 89 binaries deduplicated — the same image
ships in several releases), every one downloaded anonymously and every hash matching the
catalogue.

### What is downloadable and what is flashable

They are different questions, and OpenFlow keeps them apart:

- **Downloadable** — anything here with a catalogue entry. That includes the module bundles, the
  dial/dongle images and the two pre-production keyboard images, none of which OpenFlow will
  write to a keyboard. Keeping a copy of a file is not writing it to hardware.
- **Flashable** — an image OpenFlow is prepared to write, which today means a keyboard image
  whose side and flash generation are both confirmed. The module path is withheld until it has
  been proven on a donor unit, and the 0.0.x images are withheld because nobody can say which
  side they are.

### Custom firmware, later

The images here are Naya's, signed with Naya's key, and the Create's bootloader verifies that
signature — so a firmware built by anyone else cannot boot today, whatever tooling exists. The
plan is a community-signed bootloader and an open firmware to go with it. When that happens it
belongs in its own repository with its own trust root, and OpenFlow gains a second source
alongside this one rather than loosening what it checks about this one.
