"""Carve the Create firmware images out of the NayaFlow BETA-channel installers.

Beta counterpart of extract_history.py. The carve is the same code (extract_history.extract_version,
which is get_binaries + fw_names + carve_fw.carve on the macOS zip) and every file entry keeps the
same shape, but the output goes to firmware-history-beta/<tag>/ and never to firmware-history/.
OpenFlow's firmware fetcher and catalogue builder read only firmware-history/, so nothing here can
reach a flasher by accident.

INPUT. The beta mirror (default D:/NayaOS/mirror/github/NayaFlow-beta-releases, or --mirror /
$NAYA_BETA_MIRROR): releases.json plus one folder per tag holding the installers and their .sha256
sidecars. It is read only. The zip is opened in place with zipfile, as extract_history does, its
digest is checked against the sidecar first, and the carve is staged in a temp folder that is
removed afterwards. Where a release has both an Intel and an arm64 macOS zip, the arm64 one is
carved too and must give the same bytes.

DE-DUPLICATION. An image byte-identical (same resource_sha256) to a file already in
firmware-history/, or to one an earlier beta release stored, is not written again: its entry says
`duplicate_of` with the path of the kept copy. The kept copy is the official one when there is one
(earliest official release holding those bytes, main folder before linux-variant/), otherwise the
earliest beta release that carried it.

VERSIONS. The encrypted images carry no readable version (the MCUboot header version is MCUboot's
sample 1.2.3+4 in every release), so every witness is recorded, strongest first: the same plaintext
hash as an image whose version is known (OpenFlow's firmware catalogue, or an earlier beta), the
module bundle's own LittleFS VERSION file, NayaCore's version literal, the app JS constant
(flash_map.py), and last the beta release note's heading. `firmware_version` is the first of them;
`firmware_version_conflict` is true when they disagree.

Header facts (MCUboot header version, KEYHASH TLV, the pre-written swap trailer, the module
bundle's VERSION) come from the catalogue builder in the NayaOS tree, tools/build_firmware_catalog.py.

    python tools/extract_beta.py            # writes firmware-history-beta/ (refuses if it exists)
    python tools/extract_beta.py --force    # replace an existing firmware-history-beta/
"""
import argparse, hashlib, json, os, re, shutil, sys, tempfile, zipfile

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_TOOLS)
sys.path.insert(0, _TOOLS)
import extract_history, carve_fw, flash_map  # noqa: E402

NAYAOS = os.environ.get("NAYAOS", r"D:\NayaOS")
sys.path.insert(0, os.path.join(NAYAOS, "tools"))
import build_firmware_catalog as bfc  # noqa: E402

OFFICIAL = os.path.join(_ROOT, "firmware-history")
OUT = os.path.join(_ROOT, "firmware-history-beta")
CATALOG = os.path.join(NAYAOS, "docs", "reference", "firmware-catalog.json")
MIRROR_DEFAULT = os.environ.get("NAYA_BETA_MIRROR",
                                os.path.join(NAYAOS, "mirror", "github", "NayaFlow-beta-releases"))

# "## <emoji> [BETA] NayaCreate (v0.3.29.1 -> v0.3.31.1)" or "## <emoji> NayaCreate v3.39.3"
NOTE_RE = re.compile(r"Naya(Create|Modules)\s*\(?\s*v?([\d.]+)(?:\s*(?:\u2192|-->|->)\s*v?([\d.]+))?")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, _ROOT).replace("\\", "/")


def pick_zips(d):
    """The zip extract_history.main would pick (Intel mac first, else arm64), plus the other one."""
    zips = sorted(f for f in os.listdir(d) if f.endswith(".zip") and "mac" in f)
    pref = [z for z in zips if "arm64" not in z] or zips
    primary = pref[0]
    other = next((z for z in zips if z != primary), None)
    return primary, other


def declared_versions(body):
    out = {}
    for line in (body or "").splitlines():
        if not line.lstrip().startswith("#"):
            continue
        m = NOTE_RE.search(line)
        if m:
            key = "create" if m.group(1) == "Create" else "modules"
            out[key] = bfc.norm_fw_version(m.group(3) or m.group(2))
    return out


# NayaCore carries the firmware versions it knows as UTF-16 literals "0.3.41.0". The highest 0.3.x.y
# is the keyboard image it embeds and the highest 0.2.x.y the module bundle: checked against every
# stable release whose version is known (1.14.5, 1.15.0, 1.17.2, 1.19.1, 1.25.0, 1.25.1).
VER16 = re.compile(rb"(?:(?:[0-9]\x00){1,3}\.\x00){3}(?:[0-9]\x00){1,3}")


def core_literals(zp):
    bins = extract_history.get_binaries(zp)
    d = bins.get("mac") or bins.get("win")
    if d is None:
        return []
    return sorted({tuple(int(x) for x in m.decode("utf-16-le").split(".")) for m in VER16.findall(d)})


def core_version(lits, major):
    """'3.41.0' from the highest literal 0.<major>.x.y, in the catalogue's three-part form."""
    top = max((v for v in lits if v[:2] == (0, major)), default=None)
    return ".".join(str(x) for x in top[1:]) if top else None


def official_index():
    """resource sha256 -> repo path of the official copy to point at."""
    rows = []
    for dirpath, _dirs, files in os.walk(OFFICIAL):
        for f in files:
            if f.endswith(".bin"):
                p = os.path.join(dirpath, f)
                tag = rel(p).split("/")[1]
                rows.append((bfc.vtuple(tag), "linux-variant" in p, rel(p), sha256_file(p)))
    idx = {}
    for _v, _lv, path, digest in sorted(rows):
        idx.setdefault(digest, path)
    return idx


def catalogue_versions():
    """plaintext sha256 -> (version or None, label, historyPath) from OpenFlow's catalogue."""
    try:
        cat = json.load(open(CATALOG, encoding="utf-8"))
    except OSError:
        return {}
    out = {}
    for im in cat.get("images", []):
        if im.get("plaintextSha256"):
            out[im["plaintextSha256"]] = (im.get("createFirmware"), im.get("versionLabel"),
                                          "firmware-history/" + (im.get("historyPath") or ""))
    return out


def header_facts(raw, entry):
    """What the catalogue builder reads from an image without decrypting it."""
    if entry["type"] != "mcuboot":
        return {"mcuboot_header_version": None, "trailer": None}
    hdr = bfc.parse_header(raw)
    tlv = bfc.parse_tlvs(raw, hdr)
    if tlv.get("plaintextSha256") != entry["plaintext_sha256"]:
        raise SystemExit(f"{entry['name']}: TLV sha256 disagrees with the carve")
    if tlv.get("signingKeyHash") != entry["keyhash"]:
        raise SystemExit(f"{entry['name']}: TLV keyhash disagrees with the carve")
    magic = "good" if raw[-16:] == bfc.BOOT_MAGIC else "unset" if raw[-16:] == b"\xff" * 16 else "other"
    return {"mcuboot_header_version": hdr["headerVersion"],
            "trailer": {"present": magic == "good", "magic": magic, "image_ok": raw[-24] == 0x01,
                        "swap_on_upload": ("permanent" if raw[-24] == 0x01 else "test")
                        if magic == "good" else None}}


def carve_other(zp, names_bytes):
    """Carve the second macOS zip and compare it, name by name, with the primary carve."""
    bins = extract_history.get_binaries(zp)
    d = bins.get("mac")
    if d is None:
        return {"asset": os.path.basename(zp), "identical": False, "note": "no macOS binary"}
    binding, _ = carve_fw.carve(d, extract_history.fw_names(d))
    got = {nm: hashlib.sha256(info["bytes"]).hexdigest() for nm, info in binding.items()}
    return {"asset": os.path.basename(zp), "identical": got == names_bytes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mirror", default=MIRROR_DEFAULT)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if os.path.commonpath([os.path.abspath(OUT), os.path.abspath(OFFICIAL)]) == os.path.abspath(OFFICIAL):
        raise SystemExit("refusing: the beta output would land inside firmware-history/")
    if os.path.exists(OUT) and not args.force:
        raise SystemExit(f"{OUT} exists; pass --force to replace it")

    notes = {r["tag_name"]: r for r in json.load(open(os.path.join(args.mirror, "releases.json"),
                                                      encoding="utf-8"))}
    tags = sorted((t for t in os.listdir(args.mirror) if t.startswith("v")
                   and os.path.isdir(os.path.join(args.mirror, t))), key=bfc.vtuple)
    off = official_index()
    cat = catalogue_versions()
    stage = tempfile.mkdtemp(prefix="naya-beta-")
    extract_history.OUT = stage                     # extract_version writes here, never firmware-history/
    beta_bytes, beta_plain = {}, {}                 # sha -> kept path; plaintext -> (version, path)
    index, to_copy = [], []
    try:
        for tag in tags:
            d = os.path.join(args.mirror, tag)
            primary, other = pick_zips(d)
            zp = os.path.join(d, primary)
            digest = sha256_file(zp)
            side = open(zp + ".sha256", encoding="utf-8").read().split()[0].lower()
            if side != digest:
                raise SystemExit(f"{tag}: {primary} does not match its .sha256 sidecar")
            r = extract_history.extract_version(tag, zp)
            note = notes.get(tag, {})
            fm = flash_map.main(tag, zp)
            js = dict(re.match(r'(\w+):"([^"]*)"', s).groups() for s in fm.get("fw_versions") or [])
            if fm.get("app_version") and fm["app_version"] != tag.lstrip("v"):
                raise SystemExit(f"{tag}: the zip's package.json says {fm['app_version']}")
            decl = declared_versions(note.get("body"))
            lits = core_literals(zp)
            rec = {"tag": tag, "channel": "beta", "published_at": note.get("published_at"),
                   "prerelease": bool(note.get("prerelease")), "app_version": fm.get("app_version"),
                   "source_asset": primary, "source_asset_sha256": digest,
                   "source_platform": r.get("source_platform"),
                   "note_declares": decl, "app_js_declares": js,
                   "nayacore_version_literals": [".".join(map(str, v)) for v in lits]}
            if "error" in r:
                rec["error"] = r["error"]
                index.append(rec)
                continue
            rec["firmware_names"] = r["firmware_names"]
            if not r["firmware_names"]:
                rec["note"] = ("No firmware in this release: its NayaCore embeds no Qt firmware "
                               "resources and no MCUboot image, so there is nothing to carve.")
            vdir = os.path.join(stage, tag)
            names_bytes = {}
            files = []
            for e in r["files"]:
                if e.get("status") == "NOT_CARVED":
                    files.append(e)
                    continue
                sub = "module/" if e["category"] == "module" else ""
                raw = open(os.path.join(vdir, sub + e["name"]), "rb").read()
                if hashlib.sha256(raw).hexdigest() != e["resource_sha256"]:
                    raise SystemExit(f"{tag}/{e['name']}: staged file differs from the carve")
                names_bytes[e["name"]] = e["resource_sha256"]
                e.update(header_facts(raw, e))
                # --- version: every witness, strongest first (static before the release note) ---
                cands = []
                if e["category"] == "module" and e["name"] == "FlashMemory.bin":
                    mb = bfc.read_module_bundle(raw)
                    e["module_bundle"] = {"version": mb["version"], "lfs": mb["lfs"],
                                          "apps": {k: v["sha256"] for k, v in sorted(mb["files"].items())}}
                    cands += [(mb["version"], "LittleFS VERSION file in the bundle"),
                              (core_version(lits, 2), "NayaCore version literal (highest 0.2.x.y)"),
                              (js.get("NAYA_MODULE_FW_VERSION"), "app JS NAYA_MODULE_FW_VERSION"),
                              (decl.get("modules"), f"beta note {tag} (NayaModules heading)")]
                elif e["category"] == "keyboard":
                    ps = e.get("plaintext_sha256")
                    if ps in cat and cat[ps][0]:
                        cands.append((cat[ps][0], f"same plaintext as {cat[ps][2]} (OpenFlow catalogue)"))
                    elif ps in beta_plain and beta_plain[ps][0]:
                        cands.append((beta_plain[ps][0], f"same plaintext as {beta_plain[ps][1]}"))
                    cands += [(core_version(lits, 3), "NayaCore version literal (highest 0.3.x.y)"),
                              (js.get("NAYA_CREATE_FW_VERSION"), "app JS NAYA_CREATE_FW_VERSION"),
                              (decl.get("create"), f"beta note {tag} (NayaCreate heading)")]
                cands = [(v, s) for v, s in cands if v]
                e["firmware_version"] = cands[0][0] if cands else None
                e["firmware_version_source"] = cands[0][1] if cands else None
                e["firmware_version_evidence"] = [{"version": v, "source": s} for v, s in cands]
                e["firmware_version_conflict"] = len({v for v, _ in cands}) > 1
                # --- de-duplication ---
                h = e["resource_sha256"]
                own = f"firmware-history-beta/{tag}/{sub}{e['name']}"
                if h in off:
                    e["stored"], e["path"], e["duplicate_of"] = False, off[h], off[h]
                elif h in beta_bytes:
                    e["stored"], e["path"], e["duplicate_of"] = False, beta_bytes[h], beta_bytes[h]
                else:
                    e["stored"], e["path"], e["duplicate_of"] = True, own, None
                    beta_bytes[h] = own
                    to_copy.append((os.path.join(vdir, sub + e["name"]), os.path.join(_ROOT, own)))
                ps = e.get("plaintext_sha256")
                if ps and e["stored"]:
                    # new bytes, known plaintext: the same firmware packaged (encrypted) again
                    same = ([cat[ps][2]] if ps in cat else []) + ([beta_plain[ps][1]] if ps in beta_plain else [])
                    if same:
                        e["same_plaintext_as"] = same
                if ps:
                    beta_plain.setdefault(ps, (e["firmware_version"], e["path"]))
                files.append(e)
            rec["files"] = files
            if other:
                rec["cross_check"] = carve_other(os.path.join(d, other), names_bytes)
                if not rec["cross_check"]["identical"]:
                    raise SystemExit(f"{tag}: {other} carves different bytes from {primary}")
            index.append(rec)
            n_st = sum(1 for e in files if e.get("stored"))
            print(f"{tag:8s} {primary:40s} files={[e['name'] for e in files]} stored={n_st} "
                  f"versions={sorted({str(e.get('firmware_version')) for e in files})}")

        # --- write: only after every release carved cleanly ---
        if os.path.exists(OUT):
            shutil.rmtree(OUT)
        for src, dst in to_copy:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        for rec in index:
            vdir = os.path.join(OUT, rec["tag"])
            if os.path.isdir(vdir):
                with open(os.path.join(vdir, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
                    json.dump(rec, f, indent=2)
                    f.write("\n")
        with open(os.path.join(OUT, "MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(index, f, indent=2)
            f.write("\n")
        print(f"\nstored {len(to_copy)} image(s), {sum(os.path.getsize(d) for _, d in to_copy)} bytes; "
              f"wrote {rel(os.path.join(OUT, 'MANIFEST.json'))}")
    finally:
        shutil.rmtree(stage, ignore_errors=True)


if __name__ == "__main__":
    main()
