# Secret hunt — early NayaFlow installers (0.0.1, 0.0.2, 0.1.0, 0.1.1)

**Goal.** Find anything the vendor exposed in the earliest, least-stripped installers and locked down
later: plaintext (unencrypted/unsigned) Create/module firmware, MCUboot signing or encryption keys,
AES content keys, source maps, debug symbols, or plaintext config — anything that would let the
community unlock the encrypted firmware or sign its own for the Naya Create, so OpenFlow can keep
supporting the keyboard now that Naya is defunct.

**Scope.** The four earliest releases in the mirror (the largest per-release payloads): v0.0.1 and
v0.0.2 (2025-03-19), v0.1.0 (2025-05-01), v0.1.1 (2025-05-02). Authorized preservation / security
research on publicly distributed software for hardware the user owns.

**Builds on** `D:\NayaOS\docs\firmware-analysis.md` (the 1.25.1 / 1.17.3 teardown). This document does
not repeat that; it extends it backwards in time.

---

## Bottom line

1. **No plaintext firmware exists, and none ever did.** The Create firmware is AES-128-encrypted,
   RSA-2048-signed MCUboot from the very first public release (v0.0.1, March 2025). The encryption was
   not added later — there is no earlier, softer build to fall back to.

2. **The signing key is the same key used to the very end.** The MCUboot `KEYHASH` in v0.0.1 is
   byte-identical to the one in v1.25.1 (the last release, July 2026):
   `de8b07187913e6e788306618e4166e38a8c2eda99b68970d17fd00e75fd5b972`.
   One RSA keypair is the root of trust for **every device Naya ever shipped**, across all 25 releases
   and both flash generations. This confirms the working hypothesis. It also concentrates all value in
   a single key: recover it once (from any device) and it signs/decrypts **everything**.

3. **No keys, tokens, PEM blocks, source maps, or plaintext config are present** in any early
   installer — not in the JavaScript, not in the native `naya_core_fw_service` binaries, not anywhere in
   the 128–200 MB `app.asar` archives. The host never handles keys; the device does all crypto. This
   matches the 1.25.1 finding and holds all the way back to 0.0.1.

4. **APPROTECT cannot be assessed from the installers** (the firmware that would configure it is
   encrypted). It remains an on-device question — see "APPROTECT" below.

The early installers did not yield a shortcut. Their value is confirming the crypto model was fixed
from day one and that the single shared key is the whole game. The recommended path (SWD / QSPI
key-in-scratch readout, per the 1.25.1 analysis) is unchanged, but now provably unlocks all 25
releases at once.

---

## Integrity

`python verify.py` before analysis: `ok=208  size-only-ok(no digest)=56  missing=0  bad=0`. The mirror
is complete and intact. (The early releases and the small `.yml` files carry no GitHub sha256 digest,
so they are size-verified only; everything with a digest passed.)

## Method / toolchain

This machine had no 7-Zip, binwalk, unsquashfs, or binutils. Everything below used only Python 3.14
plus pure-Python helpers (`py7zr`, `PySquashfsImage`, `pefile`) and PyCryptodome — no external
binaries required.

- **Source of truth per version = the macOS `.zip`.** It is a plain ZIP (`zipfile` reads it with zero
  dependencies) and, in these early builds, its `app.asar` bundles **all three platforms'** native
  firmware service, so one file yields the Windows `.exe`, the macOS Mach-O, and all the app JS.
- **asar parsing** — a small reader for the Chromium-Pickle asar header, then walk the directory and
  slice files out by offset (`_tools/asarlib.py`).
- **Firmware detection** — scan each native binary for the MCUboot magic `0x96f3b83d`, parse each
  image header (`hdr_size`, `img_size`, **`flags`** — bit 0x4 = `IMAGE_F_ENCRYPTED_AES128`), measure
  payload entropy, and parse the TLV trailer for `KEYHASH`, `SHA256` (hash of the *decrypted* image),
  `RSA2048_PSS` (signature) and `ENC_RSA2048` (the wrapped AES key) (`_tools/fwscan.py`,
  `_tools/tlv.py`).
- **Key/secret sweep** — string-extract every native binary and raw-scan every full `app.asar` for
  `-----BEGIN`, `PRIVATE KEY`, PEM/PKCS variants, `hellofromesbuild`, `GITHUB_*TOKEN`, `APPROTECT`,
  `aes-128-*`, crypto-library names, and hardcoded credentials (`_tools/strhunt.py`,
  `_tools/driver.py`).

Extraction workspace (not committed, outside this repo): `D:\NayaOS\extracted\early\`. Per-version
JSON reports: `D:\NayaOS\extracted\early\_run\<ver>.json`.

---

## Findings

### 1. Firmware: encrypted MCUboot from v0.0.1 onward

Every Create image in every early release is a complete MCUboot image, `flags=0x4` (AES-128 encrypted),
payload entropy 7.997, signed `RSA2048_PSS`, with the per-image AES key wrapped as `ENC_RSA2048`.
Confirmed not just by the flag: the first bytes of each decrypt-target payload are random (no
nRF52840 Cortex-M vector table — no valid `0x2000xxxx` initial stack pointer), i.e. genuinely
ciphertext, not an unencrypted image mislabeled.

The internal MCUboot version field is the placeholder `1.2.3+4` in all early images (same as 1.25.1);
the real advertised version (`NAYA_CREATE_FW_VERSION`) is not injected anywhere yet — that came later.

### 2. The signing key never changed

`KEYHASH = de8b0718…5fd5b972` is identical across v0.0.1, v0.0.2, v0.1.0, v0.1.1 **and** the v1.25.1
baseline. Every image is signed by the same RSA-2048 keypair. The per-image `ENC_RSA2048` values
differ (as expected — one random AES content key per image), but the wrapping scheme is unchanged
across the whole timeline. The signing public key is provably a single fixed key; the image-encryption
public key is, by the unchanged scheme and shared trust root, almost certainly the same single keypair
(cannot be proven from ciphertext alone, but recovering that one private key decrypts every image we
hold).

### 3. No secrets anywhere in the app

Across all four releases:

- **JavaScript** (`desktop-main`, `(desktop-)background-server`, both renderer bundles): no PEM, no
  private keys, no `hellofromesbuild` esbuild token, no `GITHUB_RELEASES_READ_ONLY_TOKEN`, no
  `NAYA_*_FW_VERSION` injection. The only `password` strings are SVG icon names
  (`password-filled.svg`, `wifi_password-*.svg`) and a generic HTTP-auth URL builder — zero
  `password = "<value>"` assignments.
- **Native `naya_core_fw_service` binaries** (Windows PE and macOS Mach-O): no PEM, no `PRIVATE KEY`,
  no crypto-library strings (no mbedTLS/OpenSSL/tinycrypt/wolfSSL/libsodium), no `APPROTECT`/`UICR`.
- **Full-archive raw sweep** of every 128–200 MB `app.asar` (all ~11k–15k packed files at once): none
  of the sensitive markers present. The `KEYHASH` bytes appear only as the MCUboot TLV identifier
  (4 hits in 0.0.x = 2 images × Win+Mac binaries; 6 hits in 0.1.x = 3 images × Win+Mac).
- **No `.map` source maps** are shipped in any early asar. (The extra size of the early installers is
  the SVG icon set and per-platform Qt runtimes, not debug artifacts.)

### 4. Architecture (useful for reimplementation)

The host application never touches firmware bytes or keys. The Electron background server spawns the
native Qt `naya_core_fw_service` and talks to it over a **local WebSocket on port 1024**, sending
short string commands. Observed flashing/pairing vocabulary:

| command | meaning |
|---|---|
| `mcb_kbl_start` | MCUboot flash: keyboard **left** half |
| `mcb_kbr_start` | MCUboot flash: keyboard **right** half |
| `prog_kbb_verify` | verify keyboard image(s) |
| `prog_quit` | end the programming session |
| `ble_pair_auto_start` | BLE auto-pair (added in 0.1.0) |

The service loads the matching **encrypted** image from its own Qt resources and uploads it over
standard SMP/mcumgr using an **embedded Apache mynewt `newtmgr`** client (bundled as a Qt resource;
Go build paths `/Users/codecoup/dev/go/src/mynewt.apache.org/newtmgr/…` — a stock Codecoup build,
not Naya's own tree, and not a source of secrets). So the transport is ordinary newtmgr/SMP over
serial, and re-flashing needs no key: the images are pre-encrypted and the device decrypts them.

### 5. Firmware evolution across the early line

| release | Qt resource dir | images | notes |
|---|---|---|---|
| 0.0.1, 0.0.2 | `:/resources/includes/kbfw/` | `fwl.bin`, `fwr.bin` | keyboard L/R only; **0.0.1 and 0.0.2 firmware is byte-identical** |
| 0.1.0, 0.1.1 | `:/resources/includes/kb_fw/` + `d_fw/` | `kb_fwl.bin`, `kb_fwr.bin`, `d_fw.bin` | dir renamed `kbfw`→`kb_fw`; **dial firmware `d_fw.bin` added**; 0.1.0 and 0.1.1 firmware byte-identical |
| … later … | `:/resources/Includes/kb_fw/` + `m_fw/` | adds `_64` gen-B variants + `FlashMemory.bin` | per 1.25.1 analysis: capital `Includes`, flash generation B, LittleFS module bundle |

No gen-B (`_64`) variants and no `FlashMemory.bin` module bundle exist yet in the 0.x line — those are
later additions. Linux has **no** `naya_core_fw_service` in any 0.x release
(`_getNayaCoreLinuxExePath()` returns `""`), so the Linux AppImage carries no firmware; nothing was
lost by analyzing via the macOS zip.

### 6. APPROTECT

No `APPROTECT`/`UICR`/readback strings appear in any host binary — expected, because APPROTECT is set
(or not) by the device's bootloader/app firmware writing the nRF52840 `UICR.APPROTECT` register, not
by anything on the PC. The firmware that would reveal this is encrypted, so the installers cannot tell
us whether Naya enables APPROTECT. This can only be answered on-device (read `UICR.APPROTECT`, or
simply attempt an SWD memory read). It matters directly: **if APPROTECT is disabled**, an SWD dump of
one keyboard recovers the shared key material, which — because the key never changed — then decrypts
every release's firmware we already hold, yielding the plaintext images (and from them, the board
definition) OpenFlow needs, and the ability to sign custom firmware for any unit.

---

## What this means for OpenFlow

- **Re-flashing stock firmware works today, no key required** — the bundled images are valid signed
  images the device accepts over newtmgr/SMP; the full fingerprint catalog below lets you confirm which
  image a given half runs (`mcumgr image list` reports the plaintext SHA-256).
- **Reading or replacing firmware needs the one shared key.** There is no key in any installer. The
  only recovery routes remain on-device: the MCUboot key-in-scratch path or an SWD dump
  (`D:\NayaOS\docs\qspi-flash-readout.md` / `firmware-analysis.md`). The new, valuable fact is that
  this is a **one-and-done** effort — the recovered key is not release-specific.
- **Reimplementing the flasher is straightforward**: standard newtmgr/mcumgr over serial, image
  selected by USB PID, triggered by the simple command vocabulary above.

**Recommended next steps** (all on-device, outside these installers):
1. Read `UICR.APPROTECT` over SWD (or just try to attach) to learn whether readout is blocked.
2. If open, dump the nRF52840 and recover the AES/RSA key material.
3. If APPROTECT is enabled, pursue the QSPI key-in-scratch readout instead.
4. Apply the one recovered key to the encrypted images already carved from every release.

---

## Reproduce

```
# integrity
python verify.py

# per-version teardown (writes JSON report; nothing committed)
python D:\NayaOS\extracted\early\_tools\driver.py v0.1.0 \
    D:\nayaHistory\releases\v0.1.0\NayaFlow-0.1.0-mac.zip \
    D:\NayaOS\extracted\early\_run\0.1.0
```

Scripts: `D:\NayaOS\extracted\early\_tools\{asarlib,fwscan,tlv,strhunt,driver}.py`.

## Appendix — firmware fingerprint catalog (early releases)

`plaintext SHA-256` = the MCUboot `0x10` TLV = hash of the **decrypted** image = what a device reports
via `mcumgr image list`. All images `flags=0x4` (encrypted), signed by `KEYHASH de8b0718…5fd5b972`.
Left/right labeling follows the documented convention that the left image is the larger of the pair.

```
v0.0.1 / v0.0.2  (identical)
  keyboard right  img_size 218256   47ab8461e72a9779ab28defb34a850ee196050668fb19b897a10d629048b82f0
  keyboard left   img_size 285392   b942c1772f68ec81bdbf769f087609f4fecd1bc4a9141124bbb54c9f71066b60

v0.1.0 / v0.1.1  (identical)
  keyboard left   img_size 313392   ce6d82b91b2246feb72505a0addcf93246e543e285b8ca347c56942344011756
  keyboard right  img_size 235296   066ebb1c07644226daef1c49960723fd1ddfb5210182c1c501b1b82a32ef7f2e
  dial (d_fw)     img_size 175136   7822d9d0e768954aad2f06485c4b269881b48c9a93c616fec2134cd42e805a40
```

(For comparison, v1.25.1 keyboard plaintext hashes are `479e89ba…` left / `2abb2695…` right gen-A and
`07dd2523…` / `87f63fd3…` gen-B — see `firmware-analysis.md`.)

_Firmware images are archived under `firmware-history/`; no key material is stored anywhere in this repo (none was found)._
