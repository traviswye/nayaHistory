# Flashing procedure — how NayaFlow flashes the Create, across all 25 releases

**Purpose.** Reverse-engineered map of how the official app talks to the keyboard and flashes it, from
the first release (v0.0.1, 2025-03-19) to the last (v1.25.1, 2026-07-21), so OpenFlow can reimplement
the flasher and support units on any firmware generation. This is the flashing counterpart to
`SECRET-HUNT.md` (keys/encryption) and `D:\NayaOS\docs\firmware-analysis.md` (image internals).

**How this was derived.** For every release, the macOS `.zip` was opened with Python (`zipfile`), the
`app.asar` parsed, the orchestration JS pulled out, and the native firmware service binary carved and
string-scanned. The macOS Mach-O is the authority for the native SMP symbol names — the Windows `.exe`
(MinGW build) strips those strings, so a Windows-only scan understates the middle era. The device-side
protocol (below) is standard MCUboot/SMP; the two on-device inference points are called out explicitly.

---

## Bottom line

- **The Create is flashed over standard Simple Management Protocol (SMP / mcumgr) on a USB serial port
  at 1,000,000 baud, with CBOR payloads.** The images are standard MCUboot images. This has been true,
  at 1 Mbaud, for the entire product history.
- **No key is needed to flash stock firmware.** The images ship pre-encrypted and pre-signed; the host
  uploads them as-is and the device decrypts and verifies against its baked-in key (the single key
  documented in `SECRET-HUNT.md`). OpenFlow can re-flash any unit with its matching stock image today.
- **The app is three layers:** an Electron UI, a native Qt "NayaCore" service that owns all
  serial/USB/SMP/crypto handling, and the device. The UI never touches firmware bytes; it sends the
  service high-level requests over a local IPC socket.
- **What changed over time** is the plumbing, not the device protocol: the SMP client was swapped from
  a bundled Apache `newtmgr` to Naya's own in-process implementation (at v1.11.0), the UI↔service IPC
  moved from a WebSocket to ZeroMQ, the service was renamed twice, and the firmware bundle grew
  (dial firmware, then a module bundle, then a second flash generation).
- **For a flasher targeting current hardware, target the v1.25.1 model** (native SMP, gen-A + gen-B,
  Create FW 3.41.0 / module FW 2.3.3). The rest is back-compat context.

---

## The current procedure (v1.25.1) — target this first

1. **Enumerate USB serial ports** and identify the Create half by its USB VID/PID. NayaCore does this
   natively (`QSerialPort` + `setCreateFlashGenerationFromPid`): the PID identifies both the half
   (left/right) and the **flash generation** (A vs B). The concrete VID/PID integers live in the
   native binary, not the JS (the JS carries only a `0xFFFF` placeholder) — **OpenFlow should read the
   real VID/PID off a live device**, since that is the ground truth and the binary only compares
   integer constants.
2. **Pick the matching embedded image.** NayaCore carries five firmware resources (see layout below)
   and selects the one image whose half + generation matches the detected PID. It refuses to flash if
   the generation is unknown.
3. **Open the serial port at 1,000,000 baud** and speak **SMP** (mcumgr). Payloads are CBOR; framing is
   the standard SMP serial framing. NayaCore's client functions: `uploadImageToSlot` /
   `uploadImageToCreateSlot` / `uploadImageToModulesSlot`, chunked via `uploadImageChunk`, framed by
   `sendFramedCommand`, parsed by `parseSMPResponse` (all also present in `…ERK` variants — see note).
4. **Upload the image to the secondary slot, then mark + reset.** This is the standard MCUboot flow:
   image upload (img-mgmt group), set the uploaded image pending (test or confirm), then an os-mgmt
   reset so MCUboot swaps and boots it. The device validates the RSA-2048 signature and AES-decrypts
   the payload itself during the swap.
5. **Modules and keymaps go the same way.** `uploadImageToModulesSlot` handles the module bundle
   (`FlashMemory.bin`, a LittleFS image), and `keymapUpload` pushes keymaps — both over the same SMP
   link.

**Key point for OpenFlow:** because the device side is stock MCUboot + SMP, you do **not** need to
reimplement Naya's client. Any standard SMP/mcumgr library (Zephyr `mcumgr`, `smpclient`, `mcumgr-web`,
etc.) pointed at the serial port at 1 Mbaud can upload the stock images. The Naya-specific work is only
(a) VID/PID → half/generation selection and (b) shipping the right stock image.

**Two on-device points to confirm** (not answerable from the installers): the exact VID/PIDs, and how
the device exposes the SMP server — whether the running Zephyr app advertises mcumgr over USB CDC-ACM
continuously, or whether a recovery/DFU entry step is required first. Both are one-plug-in checks on a
real unit.

---

## Architecture and its evolution

Three layers throughout:

```
Electron UI (renderer)  ──IPC──  NayaCore native service (Qt)  ──USB serial/SMP──  Create device
      (JS)                         (owns serial, USB, SMP, crypto)                  (MCUboot + app)
```

### Transport to the device (the important axis)

| releases | device-side SMP client | evidence |
|---|---|---|
| v0.0.1 – v1.6.10 | **bundled Apache mynewt `newtmgr`** (Go binary shipped as a Qt resource `nmgr_win/newtmgr.exe` / `nmgr_mac/newtmgr`); the service shells out to it | ~3,900 `newtmgr` refs + Codecoup Go build paths in the binary |
| v1.11.0 – v1.25.1 | **Naya's own in-process SMP client** (newtmgr dropped) | `sendFramedCommand`, `parseSMPResponse`, `uploadImageToSlot`, `uploadImageToCreateSlot`, `uploadImageToModulesSlot`, `uploadImageChunk`, `keymapUpload` |

Serial rate is **1,000,000 baud** in both eras (the newtmgr connection profiles and the native client
both use it). SMP payloads are CBOR-encoded in both.

Note on the `…ERK` variants: from v1.11.0 the native functions appear as `sendFramedCommandERK`,
`parseSMPResponseERK`, `uploadImageToSlotERK`, `uploadImageChunkERK` (an author/codename suffix). The
un-suffixed names appear alongside from v1.17.2 on. Same protocol; a refactor, not a wire change. These
symbol strings are visible in the macOS/Linux binaries and stripped from the Windows `.exe`.

### UI ↔ service IPC (local only, never leaves the machine)

| releases | IPC |
|---|---|
| v0.0.1 – ~v1.3.x | **WebSocket on 127.0.0.1:1024**, plain string commands (`sendCommand("mcb_kbl_start")`) |
| ~v1.6.x onward | **ZeroMQ** pub/sub (`libzmq`, `tcp://localhost:<port>`, `NAYA_CORE_PUB_TOPICS`), JSON messages (`.send(JSON…)`) |

The `:1024` port string persists in the JS into late versions. This IPC is internal glue; OpenFlow does
not need it — it can drive the device directly.

### Native service binary — name and location

| releases | binary | location |
|---|---|---|
| v0.0.1 – v1.6.10 | `naya_core_fw_service(.exe)` | inside `app.asar` (`dist/@naya-suite/naya-core/{Windows,mac}/`) |
| v1.11.0 – v1.11.11 | `naya_core_project(.exe)` | `app.asar.unpacked` + `Contents/core/…` (adds ZeroMQ, Qt Sql) |
| v1.14.3 – v1.17.3 | `NayaCore(.exe)` | inside `app.asar` |
| v1.19.1 – v1.25.1 | `NayaCore` | outside the asar, in `NayaFlow.app/Contents/core/NayaCore.app/` |

A **Linux** NayaCore first appears at v1.17.3 (`naya-core/linux/NayaCore/bin/NayaCore`); releases before
that have no Linux firmware service (`_getNayaCoreLinuxExePath()` returns `""`).

---

## Firmware bundle layout (what gets flashed) and its evolution

All images are AES-128-encrypted, RSA-2048-signed MCUboot (see `SECRET-HUNT.md`). Uploaded as-is.

| releases | Qt resource dir | images bundled |
|---|---|---|
| v0.0.1 – v0.0.2 | `:/resources/includes/kbfw/` | keyboard `fwl.bin`, `fwr.bin` |
| v0.1.0 – v1.6.10 | `:/resources/includes/kb_fw/` + `d_fw/` | keyboard `kb_fwl.bin`, `kb_fwr.bin` + **dial** `d_fw.bin` |
| v1.11.0 – v1.14.5 | `:/resources/includes/kb_fw/` + `m_fw/` | keyboard L/R + **module bundle** `FlashMemory.bin` (dial folded into modules) |
| v1.15.0 – v1.21.0 | `:/resources/Includes/kb_fw/` + `m_fw/` | keyboard L/R + `FlashMemory.bin` (dir capitalized) |
| v1.25.0 – v1.25.1 | `:/resources/Includes/kb_fw/` + `m_fw/` | keyboard L/R **gen-A** + `kb_fwl_64.bin`/`kb_fwr_64.bin` **gen-B** + `FlashMemory.bin` |

So the flasher must handle four keyboard images on current builds (left/right × gen-A/gen-B), select by
USB PID, plus one LittleFS module bundle. `FlashMemory.bin` contains the per-module userapps
(Touch/Track/Tune/Float/Query) — details in `firmware-analysis.md`.

## Command vocabulary by era

Early (v0.0.1 – v1.6.x), plain strings over the WebSocket. Sent by the UI:
`mcb_kbl_start`, `mcb_kbr_start` (MCUboot flash left/right), `prog_kbb_verify`, `prog_quit`,
`ble_pair_auto_start` (from v0.1.0). The service understands a wider set including dongle flashing
(`mcb_dongle_start/progress/success/fail`) and module userapp management (`fw_userapp_connect/search/
fw_version_*`).

Late (v1.14.3+), a higher-level `fw_update` state machine (carried in JSON over ZeroMQ):
`fw_update_init`, `fw_update_create_start`, `fw_update_create_pairing_start`, `fw_update_module_start`,
`fw_update_end`, `fw_update_status`, plus `fw_version`, `fw_version_number(_module)`, `fw_files`,
`fw_process_status_create/module`. This covers keyboard ("create"), module, and pairing in one flow.

These are the app's own high-level operations; underneath, each maps to standard SMP image upload +
reset on the device.

---

## Slot ids, vendor-exact (2026-09-16)

How NayaCore addresses an upload was recovered two ways that agree, and neither is an inference.

**From the device.** A production Create (left half, FW 3.41.0, gen A) rebooted into MCUboot answers
the `image slot info` read (image group, id 6):

| image | slot | size | upload_image_id |
|---|---|---|---|
| 0 | 0 (primary) | 663552 | 1 |
| 0 | 1 (secondary) | 663552 | 2 |

Only image 0 is listed, so the bootloader is a single-image swap build with
`MCUBOOT_SERIAL_DIRECT_IMAGE_UPLOAD` on: the `image` field of an upload is a **direct slot id**
(0/1 = primary, 2 = secondary, 3 = slot2_partition, 4 = slot3_partition), not the application-side
mcumgr image index. 663552 bytes is exactly the padded size of every keyboard image resource.

**From NayaCore 6.11.0** (both macOS builds, symbols intact; the wrappers are two instructions each):

| function | is | address (x86_64 / arm64) |
|---|---|---|
| `MCUBootWorker::uploadImageToCreateSlot(path)` | `uploadImageToSlot(path, 2)` | `0x100115d50` / `0x1000f3d14` |
| `MCUBootWorker::uploadImageToModulesSlot(path)` | `uploadImageToSlot(path, 4)` | `0x10011a140` / `0x1000f7938` |

The request keys sit together in the binary as `image`, `off`, `len`, `sha`, `data`, beside the
SMP console markers `06 09` / `04 14` and `sendFramedCommand`, with `hash`, `confirm` (the image
state write) next to them: stock mcumgr, exactly as documented above.

So: **keyboard image -> `image: 2`** (the secondary slot, then mark pending + reset, MCUboot swaps and
decrypts), **module bundle -> `image: 4`** (slot3_partition, the 1 MiB `M_Firmware` LittleFS partition;
no mark-pending, a reset is enough, and the app reports the stored bundle version afterwards via
`MODULE_FILE_FW_VERSION` 0xDE/0x100A, which only the LEFT half answers). The modules slot never
appears in the slot map because it is not an MCUboot image slot; the vendor constant is the only
source for it, and it should be used only on a bootloader whose map numbers the secondary slot 2.

The 2026-09-01 note above that recovery "self-recovers on timeout" did not hold on 2026-09-16: the
half stayed in MCUboot for well over a minute after an app-requested reset until an SMP `os reset`
was sent. Plan for the explicit reset (or a power cycle), not the timeout.

## Product ids, vendor-exact (2026-09-16)

`Naya_Device::setCreateFlashGenerationFromPid(uint16 pid)` (x86_64 `0x10017e600`, arm64 `0x10014d710`,
identical logic) is the whole PID table. It masks the pid with `0xEFFF`, accepts exactly two families
of three (a bitmask `0x400801` over `pid - 0x64` and `pid - 0xC8`, i.e. offsets 0, 11, 22), and reads
bit `0x1000` as the flash generation:

| `pid & 0xEFFF` | half | mode |
|---|---|---|
| `0x064` | left | application |
| `0x06F` | left | MCUboot recovery |
| `0x07A` | left | DFU |
| `0x0C8` | right | application |
| `0x0D3` | right | MCUboot recovery |
| `0x0DE` | right | DFU |

`pid & 0x1000` clear = **generation A**, set = **generation B** (so gen-B halves are `0x1064` /
`0x10C8`, and in recovery `0x106F` / `0x10D3`). A stored generation that disagrees with the pid is
logged as a mismatch. Confirmed on hardware: `0x0064`, `0x00C8`, `0x006F`. The dongle (`0x012C`) is
outside this table. The "read the real VID/PIDs off a live device" item above is therefore closed:
this is the table the binary compares against.

## What OpenFlow needs to do

1. **Use a standard SMP/mcumgr client** over serial at **1,000,000 baud**, CBOR payloads. No custom
   protocol required.
2. **Identify the device by USB VID/PID** to pick the correct image (left/right × gen-A/gen-B). Capture
   the real VID/PIDs from live hardware — they are native constants, not in the JS.
3. **Ship the stock encrypted images** carved from the releases (per generation). They upload and boot
   without any key; the device does the crypto.
4. **Flash sequence:** upload image to secondary slot → mark pending (test/confirm) → reset → let
   MCUboot swap. Same for the module bundle via the modules slot.
5. **Custom/unsigned firmware is out of scope for a pure host flasher** — MCUboot rejects unsigned
   images, so custom firmware needs the signing key (not recoverable from installers) or an SWD
   bootloader reconfigure. See `SECRET-HUNT.md`.
6. **Confirm on a live unit:** exact VID/PIDs, the SMP MTU/chunk size, and whether a recovery-mode
   entry is needed before the device accepts SMP.

---

## Appendix — per-release reference

| release | native binary | device transport | UI↔svc IPC | kb images | bundle extras |
|---|---|---|---|---|---|
| v0.0.1 | naya_core_fw_service | newtmgr | ws:1024 | 2 | — |
| v0.0.2 | naya_core_fw_service | newtmgr | ws:1024 | 2 | — |
| v0.1.0 | naya_core_fw_service | newtmgr | ws:1024 | 2 | dial |
| v0.1.1 | naya_core_fw_service | newtmgr | ws:1024 | 2 | dial |
| v1.3.8 | naya_core_fw_service | newtmgr | ws:1024 | 2 | dial |
| v1.3.11 | naya_core_fw_service | newtmgr | ws:1024 | 2 | dial |
| v1.6.4 | naya_core_fw_service | newtmgr | ws→zmq | 2 | dial |
| v1.6.5 | naya_core_fw_service | newtmgr | ws→zmq | 2 | dial |
| v1.6.10 | naya_core_fw_service | newtmgr | zmq | 2 | dial |
| v1.11.0 | naya_core_project | native-SMP | zmq | 2 | module |
| v1.11.8 | naya_core_project | native-SMP | zmq | 2 | module |
| v1.11.9 | naya_core_project | native-SMP | zmq | 2 | module |
| v1.11.10 | naya_core_project | native-SMP | zmq | 2 | module |
| v1.11.11 | naya_core_project | native-SMP | zmq | 2 | module |
| v1.14.3 | NayaCore | native-SMP | zmq | 2 | module |
| v1.14.5 | NayaCore | native-SMP | zmq | 2 | module |
| v1.15.0 | NayaCore | native-SMP | zmq | 2 | module (Includes/) |
| v1.15.1 | NayaCore | native-SMP | zmq | 2 | module |
| v1.17.2 | NayaCore | native-SMP | zmq | 2 | module |
| v1.17.3 | NayaCore | native-SMP | zmq | 2 | module (+Linux svc) |
| v1.19.1 | NayaCore (ext) | native-SMP | zmq | 2 | module |
| v1.20.0 | NayaCore (ext) | native-SMP | zmq | 2 | module |
| v1.21.0 | NayaCore (ext) | native-SMP | zmq | 2 | module |
| v1.25.0 | NayaCore (ext) | native-SMP | zmq | 4 | module + gen-B |
| v1.25.1 | NayaCore (ext) | native-SMP | zmq | 4 | module + gen-B |

"native binary (ext)" = shipped outside `app.asar` under `Contents/core/`. "kb images" counts MCUboot
keyboard images (the LittleFS module bundle is not MCUboot and is not counted). Transport for
v1.11.0–v1.15.1 is confirmed native-SMP from the macOS binary symbols (`…ERK` functions); the Windows
`.exe` strips those strings.

## Reproduce

```
# per-version flashing map (JSON), no binaries committed
python D:\NayaOS\extracted\early\_tools\flash_map.py v1.25.1 \
    D:\nayaHistory\releases\v1.25.1\NayaFlow-1.25.1-mac.zip
```

Reports for all 25: `D:\NayaOS\extracted\early\_run_flash\<tag>.json`.

_Firmware images are archived under `firmware-history/`; no keys are stored anywhere in this repo (none was found)._
