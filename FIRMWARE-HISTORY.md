# Firmware history — every bundled Create image, by release

Each keyboard/module firmware image that shipped inside a NayaFlow release, carved from the
native NayaCore service and organized by version. Use this to pull the exact image a given
release flashed, e.g. to test-flash a specific version onto a Create.

## Where the files are

```
firmware-history/<version>/
    kb_fwl.bin,  kb_fwr.bin          keyboard halves (left / right)
    kb_fwl_64.bin, kb_fwr_64.bin     flash generation B (only v1.25.0+)
    module/
        FlashMemory.bin              module bundle (LittleFS: Touch/Track/Tune/Float/Query userapps)
        d_fw.bin                     dial firmware (v0.1.0 - v1.6.10, before the module bundle)
    manifest.json                    per-file hashes + offsets
    linux-variant/                   only where the Linux build shipped DIFFERENT images
```

The `firmware-history/` tree is git-ignored (vendor binaries stay out of git); this catalogue
is the tracked record. Regenerate with `python D:/NayaOS/extracted/early/_tools/extract_history.py`.

## What these images are (read before flashing)

- **Naming.** `_64` = flash **generation B** hardware; no suffix = **generation A**. `l`/`r` = left/right half.
  NayaCore picks the image from the keyboard's USB PID and refuses a mismatched generation.
- **All encrypted + signed.** Every keyboard image is an AES-128-encrypted, RSA-2048-signed MCUboot
  image, signed by the same key across all 25 releases (`KEYHASH de8b0718...`). They upload and boot
  **without any key** - the device decrypts and verifies itself. See `SECRET-HUNT.md`.
- **`plaintext_sha256`** is the hash of the *decrypted* image = what a device reports via
  `mcumgr image list`. Matching it proves which image a keyboard is running. `resource_sha256`
  is the on-disk (encrypted, padded) file here.
- **Files are the full padded flash-slot resource** as shipped (e.g. 663552 B); the actual MCUboot
  image is smaller (`mcuboot_image_len` in each manifest.json). A standard SMP/mcumgr upload of the
  image is all the device needs. See `FLASHING-PROCEDURE.md`.
- **Source = the macOS build**, which is byte-identical to Windows. The Linux build of a few
  releases shipped different images - preserved under that version's `linux-variant/`.

## Catalogue

`sha` = first 16 hex of `plaintext_sha256` (full values in each version's manifest.json).

| Version | File | Half | Gen | Image bytes | Encrypted | plaintext_sha256 (16) |
|---|---|---|---|---|---|---|
| v0.0.1 | `fwl.bin` | left | A | 285392 | yes | `b942c1772f68ec81` |
| v0.0.1 | `fwr.bin` | right | A | 218256 | yes | `47ab8461e72a9779` |
| v0.0.2 | `fwl.bin` | left | A | 285392 | yes | `b942c1772f68ec81` |
| v0.0.2 | `fwr.bin` | right | A | 218256 | yes | `47ab8461e72a9779` |
| v0.1.0 | `kb_fwl.bin` | left | A | 313392 | yes | `ce6d82b91b2246fe` |
| v0.1.0 | `kb_fwr.bin` | right | A | 235296 | yes | `066ebb1c07644226` |
| v0.1.0 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v0.1.1 | `kb_fwl.bin` | left | A | 313392 | yes | `ce6d82b91b2246fe` |
| v0.1.1 | `kb_fwr.bin` | right | A | 235296 | yes | `066ebb1c07644226` |
| v0.1.1 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.3.8 | `kb_fwl.bin` | left | A | 352256 | yes | `ce51a353d7806494` |
| v1.3.8 | `kb_fwr.bin` | right | A | 239184 | yes | `31ceec1a3bf05a96` |
| v1.3.8 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.3.11 | `kb_fwl.bin` | left | A | 352256 | yes | `ce51a353d7806494` |
| v1.3.11 | `kb_fwr.bin` | right | A | 239184 | yes | `31ceec1a3bf05a96` |
| v1.3.11 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.6.4 | `kb_fwl.bin` | left | A | 352256 | yes | `ce51a353d7806494` |
| v1.6.4 | `kb_fwr.bin` | right | A | 239184 | yes | `31ceec1a3bf05a96` |
| v1.6.4 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.6.5 | `kb_fwl.bin` | left | A | 352256 | yes | `ce51a353d7806494` |
| v1.6.5 | `kb_fwr.bin` | right | A | 239184 | yes | `31ceec1a3bf05a96` |
| v1.6.5 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.6.10 | `kb_fwl.bin` | left | A | 352256 | yes | `ce51a353d7806494` |
| v1.6.10 | `kb_fwr.bin` | right | A | 239184 | yes | `31ceec1a3bf05a96` |
| v1.6.10 | `module/d_fw.bin` | - | - | 175136 | yes | `7822d9d0e768954a` |
| v1.11.0 | `kb_fwl.bin` | left | A | 356848 | yes | `83100f7b0f58c2ab` |
| v1.11.0 | `kb_fwr.bin` | right | A | 242704 | yes | `ec1bbca40c74f91c` |
| v1.11.0 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.11.8 | `kb_fwl.bin` | left | A | 358016 | yes | `e3a7afc4e765c631` |
| v1.11.8 | `kb_fwr.bin` | right | A | 243312 | yes | `93b050dcf560fa43` |
| v1.11.8 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.11.9 | `kb_fwl.bin` | left | A | 356848 | yes | `83100f7b0f58c2ab` |
| v1.11.9 | `kb_fwr.bin` | right | A | 242704 | yes | `ec1bbca40c74f91c` |
| v1.11.9 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.11.10 | `kb_fwl.bin` | left | A | 358016 | yes | `e3a7afc4e765c631` |
| v1.11.10 | `kb_fwr.bin` | right | A | 243312 | yes | `93b050dcf560fa43` |
| v1.11.10 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.11.11 | `kb_fwl.bin` | left | A | 358496 | yes | `735878524ad86f7b` |
| v1.11.11 | `kb_fwr.bin` | right | A | 243840 | yes | `e1577ee8be94501f` |
| v1.11.11 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.14.3 | `kb_fwl.bin` | left | A | 359200 | yes | `8c926ca7a710cbeb` |
| v1.14.3 | `kb_fwr.bin` | right | A | 244224 | yes | `baa94b1d062ac624` |
| v1.14.3 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.14.5 | `kb_fwl.bin` | left | A | 359312 | yes | `f52aec47c312efb8` |
| v1.14.5 | `kb_fwr.bin` | right | A | 244224 | yes | `fee82f0e07bc7a54` |
| v1.14.5 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.15.0 | `kb_fwl.bin` | left | A | 361632 | yes | `99e6f8b23b16b6a4` |
| v1.15.0 | `kb_fwr.bin` | right | A | 244336 | yes | `ce0f1317a096fa2f` |
| v1.15.0 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.15.0 | `linux-variant/kb_fwl.bin` | left | A | 359312 | yes | `f52aec47c312efb8` |
| v1.15.0 | `linux-variant/kb_fwr.bin` | right | A | 244224 | yes | `fee82f0e07bc7a54` |
| v1.15.0 | `linux-variant/module/FlashMemory.bin` | - | A |  | no (LittleFS) | `-` |
| v1.15.1 | `kb_fwl.bin` | left | A | 361632 | yes | `99e6f8b23b16b6a4` |
| v1.15.1 | `kb_fwr.bin` | right | A | 244336 | yes | `ce0f1317a096fa2f` |
| v1.15.1 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.15.1 | `linux-variant/kb_fwl.bin` | left | A | 359312 | yes | `f52aec47c312efb8` |
| v1.15.1 | `linux-variant/kb_fwr.bin` | right | A | 244224 | yes | `fee82f0e07bc7a54` |
| v1.15.1 | `linux-variant/module/FlashMemory.bin` | - | A |  | no (LittleFS) | `-` |
| v1.17.2 | `kb_fwl.bin` | left | A | 304448 | yes | `1b259d25983bb6db` |
| v1.17.2 | `kb_fwr.bin` | right | A | 218064 | yes | `90f98e4d8320b86c` |
| v1.17.2 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.17.2 | `linux-variant/kb_fwl.bin` | left | A | 359312 | yes | `f52aec47c312efb8` |
| v1.17.2 | `linux-variant/kb_fwr.bin` | right | A | 244224 | yes | `fee82f0e07bc7a54` |
| v1.17.2 | `linux-variant/module/FlashMemory.bin` | - | A |  | no (LittleFS) | `-` |
| v1.17.3 | `kb_fwl.bin` | left | A | 304448 | yes | `1b259d25983bb6db` |
| v1.17.3 | `kb_fwr.bin` | right | A | 218064 | yes | `90f98e4d8320b86c` |
| v1.17.3 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.17.3 | `linux-variant/kb_fwl.bin` | left | A | 359312 | yes | `f52aec47c312efb8` |
| v1.17.3 | `linux-variant/kb_fwr.bin` | right | A | 244224 | yes | `fee82f0e07bc7a54` |
| v1.17.3 | `linux-variant/module/FlashMemory.bin` | - | A |  | no (LittleFS) | `-` |
| v1.19.1 | `kb_fwl.bin` | left | A | 312272 | yes | `036059b2ecbd8926` |
| v1.19.1 | `kb_fwr.bin` | right | A | 220688 | yes | `959fbae1d8359ebe` |
| v1.19.1 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.20.0 | `kb_fwl.bin` | left | A | 312272 | yes | `036059b2ecbd8926` |
| v1.20.0 | `kb_fwr.bin` | right | A | 220688 | yes | `959fbae1d8359ebe` |
| v1.20.0 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.21.0 | `kb_fwl.bin` | left | A | 312272 | yes | `036059b2ecbd8926` |
| v1.21.0 | `kb_fwr.bin` | right | A | 220688 | yes | `959fbae1d8359ebe` |
| v1.21.0 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.25.0 | `kb_fwl.bin` | left | A | 328880 | yes | `479e89ba6c92ead9` |
| v1.25.0 | `kb_fwl_64.bin` | left | B | 328880 | yes | `07dd2523bf87ee13` |
| v1.25.0 | `kb_fwr.bin` | right | A | 226000 | yes | `2abb2695b9b6e948` |
| v1.25.0 | `kb_fwr_64.bin` | right | B | 226000 | yes | `87f63fd3be514538` |
| v1.25.0 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |
| v1.25.1 | `kb_fwl.bin` | left | A | 328880 | yes | `479e89ba6c92ead9` |
| v1.25.1 | `kb_fwl_64.bin` | left | B | 328880 | yes | `07dd2523bf87ee13` |
| v1.25.1 | `kb_fwr.bin` | right | A | 226000 | yes | `2abb2695b9b6e948` |
| v1.25.1 | `kb_fwr_64.bin` | right | B | 226000 | yes | `87f63fd3be514538` |
| v1.25.1 | `module/FlashMemory.bin` | - | - | 1048576 | no (LittleFS) | `-` |

## Firmware lineage (when the keyboard image actually changed)

- **v0.0.1** - v0.0.2: keyboard firmware unchanged across this run
- **v0.1.0** - v0.1.1: keyboard firmware unchanged across this run
- **v1.3.8** - v1.6.10: keyboard firmware unchanged across this run
- **v1.11.0**: keyboard firmware distinct from the previous release
- **v1.11.8**: keyboard firmware distinct from the previous release
- **v1.11.9**: keyboard firmware distinct from the previous release
- **v1.11.10**: keyboard firmware distinct from the previous release
- **v1.11.11**: keyboard firmware distinct from the previous release
- **v1.14.3**: keyboard firmware distinct from the previous release
- **v1.14.5**: keyboard firmware distinct from the previous release
- **v1.15.0** - v1.15.1: keyboard firmware unchanged across this run
- **v1.17.2** - v1.17.3: keyboard firmware unchanged across this run
- **v1.19.1** - v1.21.0: keyboard firmware unchanged across this run
- **v1.25.0** - v1.25.1: keyboard firmware unchanged across this run

_No key material is stored here or anywhere in this repo; images are encrypted as shipped._