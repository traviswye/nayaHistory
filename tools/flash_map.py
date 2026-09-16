import sys, os, re, json, struct, zipfile
MCUBOOT=struct.pack('<I',0x96f3b83d)

def walk_asar_bytes(buf):
    assert struct.unpack('<I', buf[:4])[0]==4
    hs=struct.unpack('<I', buf[4:8])[0]
    body=buf[8:8+hs]
    jl=struct.unpack('<I', body[4:8])[0]
    H=json.loads(body[8:8+jl].decode('utf-8'))
    ds=8+hs
    def w(node,prefix=""):
        for name,meta in node.get("files",{}).items():
            p=prefix+"/"+name
            if "files" in meta: yield from w(meta,p)
            else: yield p,meta
    return dict(w(H)), ds

def slist(b, pat, cap=60):
    return sorted(set(m.decode(errors='replace') for m in re.findall(pat, b)))[:cap]

def scan_native(b):
    r={'size':len(b)}
    imgs=[]
    for m in re.finditer(re.escape(MCUBOOT), b):
        off=m.start()
        if off+20>len(b): continue
        _,_,hdr,_,img,flags=struct.unpack('<IIHHII', b[off:off+20])
        if hdr not in (32,512) or img==0 or img>4_000_000: continue
        imgs.append((img,flags))
    r['n_images']=len(imgs); r['img_sizes']=sorted(set(i for i,_ in imgs))
    r['all_enc']=all((f&4) for _,f in imgs) if imgs else None
    r['qrc']=slist(b, rb'(?::/[Rr]esources/[A-Za-z0-9_./]{0,50}|(?:kb_?fw|d_fw|m_fw|kbfw)[A-Za-z0-9_./]{0,20}\.bin|FlashMemory\.bin)')
    r['newtmgr']=len(re.findall(rb'newtmgr', b))
    r['smp_funcs']=slist(b, rb'(?:uploadImageToSlot|sendFramedCommand|parseSMPResponse|smpUpload|imageUploadCmd|imageUploadRsp|SmpClient|McuMgr|mcumgr)[A-Za-z]*', 40)
    r['ipc']=slist(b, rb'(?:QWebSocket[A-Za-z]*|libzmq[A-Za-z0-9_.-]*|zmq_[a-z_]+|127\.0\.0\.1:[0-9]{2,5}|:1024)', 15)
    r['usb']=slist(b, rb'(?:vendorIdentifier|productIdentifier|VID_[0-9A-Fa-f]{4}|PID_[0-9A-Fa-f]{4}|usb[A-Za-z]*Id)', 25)
    r['serial']=slist(b, rb'(?:setBaudRate|QSerialPort|Baud[0-9]+|115200|1000000|921600|230400)', 15)
    r['flashgen']=slist(b, rb'(?:setCreateFlashGeneration[A-Za-z]*|FlashGeneration[A-Za-z]*|CreateFlashGen[A-Za-z]*|gen[_-]?[AB]|generation[A-Za-z]*)', 30)
    allc=slist(b, rb'(?:mcb|prog|ble|img|dfu|fw|kb|dongle)_[a-z0-9_]{2,}', 400)
    keep=('mcb_','prog_','fw_update','fw_version','fw_process','fw_files','dfu_','dongle_','kbb_','ble_pair')
    r['cmds']=[c for c in allc if c.startswith(keep)][:120]
    r['crypto']=slist(b, rb'(?:mbedtls|openssl|tinycrypt|wolfssl|libsodium|psa_crypto|BearSSL)[A-Za-z0-9_]*', 20)
    r['pem']=b.count(b'-----BEGIN')
    return r

def main(tag, zippath):
    z=zipfile.ZipFile(zippath); names=z.namelist()
    aname=[n for n in names if n.endswith('/Resources/app.asar') and '.unpacked' not in n][0]
    abuf=z.read(aname); files,ds=walk_asar_bytes(abuf)
    rep={'tag':tag}
    if '/package.json' in files:
        m=files['/package.json']; raw=abuf[int(m['offset'])+ds:int(m['offset'])+ds+int(m['size'])]
        try: rep['app_version']=json.loads(raw).get('version')
        except: pass
    jspaths=[p for p in files if p.endswith('/index.js') and '/dist/' in p and '/node_modules/' not in p
             and 'renderer' not in p and '/assets/' not in p and 'preload' not in p]
    jsb=b''
    for p in jspaths:
        m=files[p]; jsb+=abuf[int(m['offset'])+ds:int(m['offset'])+ds+int(m['size'])]+b'\n'
    rep['js_bundles']=jspaths
    rep['cmds_js']=sorted(set(x.decode(errors='replace') for x in re.findall(rb'sendCommand\("([^"]+)"', jsb)))
    rep['ws_port']=slist(jsb, rb'(?::1024|ws://[^"\']{0,25}|127\.0\.0\.1:[0-9]{2,5}|WebSocket|zeromq|zmq|tcp://[^"\']{0,20})', 15)
    rep['send_mech']=slist(jsb, rb'(?:sendCommand|\.send\(JSON|\.send\(|publish\(|\.emit\()', 12)
    rep['linux_path']=slist(jsb, rb'_getNayaCoreLinuxExePath\(\)\{return[^}]{0,80}\}', 3)
    rep['fw_versions']=slist(jsb, rb'NAYA_[A-Z_]+:"[^"]{0,24}"', 20)
    nat=None; natsrc=None
    NAMES=('naya_core_fw_service.exe','naya_core_fw_service','NayaCore.exe','NayaCore','naya_core_project.exe','naya_core_project')
    for p,m in files.items():
        if p.split('/')[-1] in NAMES and 'Frameworks' not in p:
            nat=abuf[int(m['offset'])+ds:int(m['offset'])+ds+int(m['size'])]; natsrc='asar:'+p
            if p.endswith('.exe'): break
    if nat is None:
        cand=[n for n in names if n.split('/')[-1] in NAMES and 'Frameworks' not in n]
        cand.sort(key=lambda n:(0 if n.endswith('.exe') else 1))
        if cand: nat=z.read(cand[0]); natsrc='zip:'+cand[0]
    rep['native_src']=natsrc
    rep['native']=scan_native(nat) if nat is not None else None
    return rep

if __name__=='__main__':
    print(json.dumps(main(sys.argv[1], sys.argv[2]), indent=1))
