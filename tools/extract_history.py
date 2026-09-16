import os, re, sys, json, struct, zipfile, hashlib
sys.path.insert(0, r"D:\NayaOS\extracted\early\_tools")
import carve_fw

RELEASES = r"D:\nayaHistory\releases"
OUT = r"D:\nayaHistory\firmware-history"
NAMES = ('NayaCore.exe','NayaCore','naya_core_project.exe','naya_core_project',
         'naya_core_fw_service.exe','naya_core_fw_service')
KB = carve_fw.KB_NAMES
MODULE = {'d_fw.bin', 'FlashMemory.bin'}

def asar_walk(b):
    hs=struct.unpack('<I',b[4:8])[0]; body=b[8:8+hs]; jl=struct.unpack('<I',body[4:8])[0]
    H=json.loads(body[8:8+jl]); ds=8+hs
    def w(n,p=""):
        for k,m in n.get("files",{}).items():
            q=p+"/"+k
            if "files" in m: yield from w(m,q)
            else: yield q,m
    return dict(w(H)), ds

def platform_of(path):
    pl=path.lower()
    if path.endswith('.exe') or '/windows/' in pl: return 'win'
    if '/linux/' in pl: return 'linux'
    return 'mac'

def get_binaries(zp):
    z=zipfile.ZipFile(zp); names=z.namelist(); out={}
    an=[n for n in names if n.endswith('/Resources/app.asar') and '.unpacked' not in n]
    if an:
        b=z.read(an[0]); F,ds=asar_walk(b)
        for p,m in F.items():
            if p.split('/')[-1] in NAMES and 'Frameworks' not in p:
                out.setdefault(platform_of(p), b[int(m['offset'])+ds:int(m['offset'])+ds+int(m['size'])])
    for nn in names:
        if nn.split('/')[-1] in NAMES and 'Frameworks' not in nn:
            out.setdefault(platform_of(nn), z.read(nn))
    return out

def fw_names(binary):
    """firmware leaf .bin resource names from the qt resource path strings."""
    hits=set(re.findall(rb':/[Rr]esources/[A-Za-z0-9_./]*?([A-Za-z0-9_]+\.bin)', binary))
    return sorted(x.decode() for x in hits)

def sha(b): return hashlib.sha256(b).hexdigest()

def extract_version(tag, zp):
    bins=get_binaries(zp)
    # primary = mac (== windows); fall back to win, then anything non-linux
    primary_plat = 'mac' if 'mac' in bins else ('win' if 'win' in bins else next((p for p in bins if p!='linux'), None))
    if primary_plat is None:
        return {'tag':tag,'error':'no non-linux native binary found','platforms':list(bins.keys())}
    d = bins[primary_plat]
    names = fw_names(d)
    binding, mcb = carve_fw.carve(d, names)
    vdir=os.path.join(OUT, tag); os.makedirs(vdir, exist_ok=True)
    entries=[]
    for nm in names:
        if nm not in binding:
            entries.append({'name':nm,'status':'NOT_CARVED'}); continue
        info=binding[nm]; payload=info['bytes']
        cat = 'module' if nm in MODULE else ('keyboard' if nm in KB else 'other')
        subdir = os.path.join(vdir,'module') if cat=='module' else vdir
        os.makedirs(subdir, exist_ok=True)
        with open(os.path.join(subdir, nm),'wb') as f: f.write(payload)
        side = 'left' if ('fwl' in nm) else ('right' if ('fwr' in nm) else '')
        gen  = 'B' if '_64' in nm else ('A' if (nm in KB) else '')
        entries.append({'name':nm,'category':cat,'side':side,'flash_gen':gen,
            'resource_len':info['length'],'type':info['type'],
            'mcuboot_image_len':(mcb and next((x['image_len'] for x in mcb if x['prefix']==info['prefix']),None)),
            'img_size':info.get('img_size'),'encrypted':(info['type']=='mcuboot'),
            'plaintext_sha256':info.get('plaintext_sha256'),'keyhash':info.get('keyhash'),
            'resource_sha256':sha(payload)})
    result={'tag':tag,'source_platform':primary_plat,'firmware_names':names,'files':entries}
    # linux variant, if present and different
    if 'linux' in bins and primary_plat!='linux':
        lb=get_binaries.__self__ if False else None
        ld=bins['linux']; lbind,lmcb=carve_fw.carve(ld, fw_names(ld))
        differs=False; ldir=os.path.join(vdir,'linux-variant')
        lentries=[]
        for nm,info in lbind.items():
            base=binding.get(nm)
            if base and sha(info['bytes'])==sha(base['bytes']): continue
            differs=True
            cat='module' if nm in MODULE else 'keyboard'
            sub=os.path.join(ldir,'module') if cat=='module' else ldir
            os.makedirs(sub, exist_ok=True)
            with open(os.path.join(sub,nm),'wb') as f: f.write(info['bytes'])
            lentries.append({'name':nm,'category':cat,'img_size':info.get('img_size'),
                'plaintext_sha256':info.get('plaintext_sha256'),'resource_sha256':sha(info['bytes'])})
        if differs:
            result['linux_variant']={'note':'Linux build embedded DIFFERENT firmware than win/mac','files':lentries}
    json.dump(result, open(os.path.join(vdir,'manifest.json'),'w'), indent=2)
    return result

def main():
    tags=sorted(os.listdir(RELEASES), key=lambda s:[int(x) for x in s.lstrip('v').split('.')])
    os.makedirs(OUT, exist_ok=True)
    index=[]
    for t in tags:
        d=os.path.join(RELEASES,t)
        zips=[f for f in os.listdir(d) if f.endswith('.zip') and 'mac' in f and 'blockmap' not in f]
        pref=[z for z in zips if 'arm64' not in z] or zips
        zp=os.path.join(d, pref[0])
        r=extract_version(t, zp)
        index.append(r)
        nkb=sum(1 for e in r.get('files',[]) if e.get('category')=='keyboard')
        nmod=sum(1 for e in r.get('files',[]) if e.get('category')=='module')
        lv=' +linux-variant' if 'linux_variant' in r else ''
        print(f"{t:9s} src={r.get('source_platform','?'):5s} kb={nkb} module={nmod}{lv}  files={[e['name'] for e in r.get('files',[])]}")
    json.dump(index, open(os.path.join(OUT,'MANIFEST.json'),'w'), indent=2)
    print("\nWrote", os.path.join(OUT,'MANIFEST.json'))

if __name__=='__main__':
    main()
