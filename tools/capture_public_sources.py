#!/usr/bin/env python3
"""Read-only best-effort live HTTP capture of public primary Catalyst pages.

Usage: python tools/capture_public_sources.py --out /path/to/new-directory
Outputs are new local candidate source files, NOT verified comprehensive archives.
No JavaScript rendering, authentication, Drive capture, or payment verification.
"""
import argparse, hashlib, json, urllib.request, urllib.error, datetime
from pathlib import Path

SOURCES = {
    'fund-02-project-200008': 'https://projectcatalyst.io/funds/2/challenge/liqwidcardano-defi-lending-markets',
    'fund-08-project-800352': 'https://projectcatalyst.io/funds/8/accelerate-decentralized-identity/universal-resolver-for-didprism',
    'fund-14-project-1400065': 'https://projectcatalyst.io/funds/14/cardano-open-developers/hydra-point-of-sale-accept-ada-cnts-in-retail-and-invoicing',
    'fund-14-milestones-1400065': 'https://milestones.projectcatalyst.io/projects/1400065',
}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, help='An existing or new *empty* output directory')
    args=ap.parse_args()
    out=Path(args.out)
    if out.exists() and any(out.iterdir()):
        ap.error('Output directory must be empty; snapshots must not overwrite previous captures')
    out.mkdir(parents=True,exist_ok=True)
    results=[]
    for key,url in SOURCES.items():
        result={'id':key,'source_url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capture_method':'urllib direct HTTP; does not render JavaScript'}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'HTEP-Corpus-Source-Capture/0.1 (public research; contact repository maintainers)','Accept':'text/html,application/json;q=0.9,*/*;q=0.1'})
            with urllib.request.urlopen(req,timeout=25) as resp:
                body=resp.read(12_000_001)
                if len(body)>12_000_000: raise ValueError('Source exceeds 12 MB capture safety limit')
                result.update({'http_status':resp.status,'final_url':resp.geturl(),'content_type':resp.headers.get('Content-Type',''),'length_bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
                path=out/(key+'.response-body');path.write_bytes(body)
                result['local_file']=path.name
                # Size/text checks are only warnings, NEVER proof of full-page capture.
                low=body.lower()
                marker=key.split('project-')[-1].encode('ascii') if 'project-' in key else b'1400065'
                result['project_id_present_in_raw_body']=marker in body
                result['likely_js_shell_warning']=(b'<div id="root"' in low or b'__next' in low) and marker not in body
        except Exception as e:
            result.update({'error':str(e),'capture_state':'failed'})
        results.append(result)
    (out/'manifest.json').write_text(json.dumps({'notes':'Captured HTTP responses, NOT automatically verified full rendered pages. Check permission and record completeness before redistribution.','sources':results},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'successful':sum('sha256' in r for r in results),'attempted':len(results),'manifest':str(out/'manifest.json')}))
if __name__=='__main__':main()
