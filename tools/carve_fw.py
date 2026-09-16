import sys, os, re, struct, hashlib, json, zipfile
MAGIC = struct.pack('<I', 0x96f3b83d)

def be16(b, o): return struct.unpack('>H', b[o:o+2])[0]
def be32(b, o): return struct.unpack('>I', b[o:o+4])[0]

def mcuboot_blobs(d):
    """Every MCUboot image whose 4-byte big-endian Qt length prefix validates."""
    out = []
    for m in re.finditer(re.escape(MAGIC), d):
        off = m.start()
        if off < 4 or off + 20 > len(d):
            continue
        _, _, hdr, ptlv, img, flags = struct.unpack('<IIHHII', d[off:off+20])
        if hdr not in (32, 512) or img == 0 or img > 4_000_000:
            continue
        pos = off + hdr + img
        img_end = pos
        psha = kh = None
        for _ in range(2):
            if pos + 4 > len(d):
                break
            mg, tot = struct.unpack('<HH', d[pos:pos+4])
            if mg not in (0x6907, 0x6908):
                break
            q = pos + 4
            while q + 4 <= pos + tot:
                t, l = struct.unpack('<HH', d[q:q+4]); q += 4
                if t == 0x10: psha = d[q:q+l].hex()
                if t == 0x01: kh = d[q:q+l].hex()
                q += l
            img_end = pos + tot
            pos = img_end
        image_len = img_end - off           # header + image + TLV trailer
        prefix = off - 4
        blen = be32(d, prefix)              # stored Qt resource length (padded flash slot)
        # accept when the prefix length is a sane container for this image
        if blen < image_len or blen > 4_000_000:
            continue
        out.append({'prefix': prefix, 'blen': blen, 'image_len': image_len, 'magic_off': off,
                    'img': img, 'psha': psha, 'keyhash': kh, 'enc': bool(flags & 4)})
    return out

def name_entries(d, names):
    """name -> file offset of its RCC name entry ([u16 len][u32 hash][utf16be name])."""
    out = {}
    for nm in names:
        u = nm.encode('utf-16-be')
        for m in re.finditer(re.escape(u), d):
            p = m.start()
            if p - 6 >= 0 and be16(d, p - 6) == len(nm):
                out[nm] = p - 6
                break
    return out

KB_NAMES = {"kb_fwl.bin", "kb_fwr.bin", "kb_fwl_64.bin", "kb_fwr_64.bin", "fwl.bin", "fwr.bin"}

def _find_node_index(d):
    """small BE32 value -> [positions]; candidate nameOffset fields (offset into name array)."""
    occ = {}
    for q in range(0, len(d) - 14):
        v = be32(d, q)
        if 0 < v < 0x1000000:
            occ.setdefault(v, []).append(q)
    return occ

def bind_names(d, names, mcb):
    """Bind resource name -> {prefix,length} via the Qt RCC struct.

    RCC file node: nameOffset = BE32(node+0) (into name array), dataOffset = BE32(node+10)
    (into data array). The keyboard resources are contiguous siblings, so we find a run of
    len(kb) nodes whose dataOffsets equal {kb_prefix - D0} for one D0, then solve the name-array
    base N0 by sorted pairing, then read every requested name's node."""
    n = len(d)
    fN = name_entries(d, names)
    if not mcb or not fN:
        return {}
    kb_names = [nm for nm in names if nm in KB_NAMES and nm in fN]
    k = len(kb_names)
    if k == 0:
        return {}
    # keyboard data prefixes = the k largest MCUboot images (dial, if present, is the smallest)
    mcb_sorted = sorted(mcb, key=lambda x: -x['img'])
    kb_prefixes = sorted(x['prefix'] for x in mcb_sorted[:k])
    # locate a contiguous block of k nodes whose dataOffsets match the kb prefixes (any order)
    target_pairdiffs = sorted(a - b for i, a in enumerate(kb_prefixes) for b in kb_prefixes[:i])
    found = None
    for S in (22, 14, 20, 16):
        for q0 in range(0, n - k * S - 14):
            nos = [be32(d, q0 + i * S) for i in range(k)]
            if any(v == 0 or v >= 0x1000000 for v in nos):
                continue
            if max(nos) - min(nos) >= 4096:
                continue
            dds = [be32(d, q0 + i * S + 10) for i in range(k)]
            pd = sorted(a - b for i, a in enumerate(sorted(dds)) for b in sorted(dds)[:i])
            if pd == target_pairdiffs and min(dds) >= 0:
                D0 = min(kb_prefixes) - min(dds)
                if D0 < 0:
                    continue
                # verify each dataOffset+D0 is a real kb prefix
                if sorted(x + D0 for x in dds) == kb_prefixes:
                    found = (q0, S, D0, nos, dds)
                    break
        if found:
            break
    if not found:
        return {}
    q0, S, D0, nos, dds = found
    # solve N0 by sorted pairing of block nameOffsets to kb name entries
    node_no_sorted = sorted(nos)
    fN_kb_sorted = sorted(fN[nm] for nm in kb_names)
    N0s = [f - o for f, o in zip(fN_kb_sorted, node_no_sorted)]
    if len(set(N0s)) != 1:
        return {}
    N0 = N0s[0]
    res = {}
    # bind the kb names directly from the located block (nameOffset order == fN order)
    block = sorted(range(k), key=lambda i: nos[i])          # block node indices by nameOffset
    kb_by_fN = sorted(kb_names, key=lambda nm: fN[nm])       # kb names by fN
    for slot, nm in zip(block, kb_by_fN):
        prefix = dds[slot] + D0
        length = be32(d, prefix)
        res[nm] = {'prefix': prefix, 'length': length}
    # bind remaining names (dial, module) via N0/D0, preferring the node nearest the kb block
    occ = _find_node_index(d)
    for nm in names:
        if nm not in fN or nm in res:
            continue
        want = fN[nm] - N0
        if want not in occ:
            continue
        best = None
        for q in occ[want]:
            do = be32(d, q + 10)
            prefix = do + D0
            if prefix < 0 or prefix + 4 > n:
                continue
            length = be32(d, prefix)
            if length <= 0 or length > 4_000_000 or prefix + 4 + length > n:
                continue
            dist = abs(q - q0)
            if best is None or dist < best[0]:
                best = (dist, prefix, length)
        if best:
            res[nm] = {'prefix': best[1], 'length': best[2]}
    return res

def carve(nativebytes, names):
    d = nativebytes
    mcb = mcuboot_blobs(d)
    binding = bind_names(d, names, mcb)
    pref2 = {x['prefix']: x for x in mcb}
    for nm, info in binding.items():
        payload = d[info['prefix']+4: info['prefix']+4+info['length']]
        info['bytes'] = payload
        info['bytes_sha256'] = hashlib.sha256(payload).hexdigest()
        if info['prefix'] in pref2:
            info['type'] = 'mcuboot'
            info['plaintext_sha256'] = pref2[info['prefix']]['psha']
            info['keyhash'] = pref2[info['prefix']]['keyhash']
            info['img_size'] = pref2[info['prefix']]['img']
        else:
            info['type'] = 'other'
    return binding, mcb
