"""Check local files against a committed asset manifest without downloading anything."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def digest(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',default='storage/asset-manifest.json'); ap.add_argument('--root',default='.'); a=ap.parse_args()
    m=json.loads(Path(a.manifest).read_text()); root=Path(a.root); checked=[]
    for kind in ('datasets','models'):
        for x in m['assets'][kind]:
            p=root/x['local_path']
            if not p.is_file(): raise SystemExit(f'missing {kind}: {p}')
            got=digest(p)
            if got != x['sha256']: raise SystemExit(f'sha256 mismatch for {p}: {got} != {x["sha256"]}')
            checked.append(str(p))
    print(json.dumps({'status':'ok','checked':checked,'count':len(checked)},indent=2))

if __name__=='__main__': main()
