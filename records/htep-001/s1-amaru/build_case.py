#!/usr/bin/env python3
"""Regenerate observable slices of the pinned Koios snapshot; relationships are reviewed assertions."""
import argparse,csv,hashlib,json,pathlib,re
EXPECTED_SHA256='8836d85e6530613d9042cc1f1d7e11e9e6e5a8e9391cda32be527f5a63e7fcd8'
ACTIONS=[('A0','gov_action1h4ygjv0hjfj3lmafcm76rpdzcm8vsvj9k5wejn3npyxwxm3fesnqqw9kxxz'),('A1','gov_action1vrkk4dpuss8l3z9g4uc2rmf8ks0f7j534zvz9v4k85dlc54wa3zsqq68rx0'),('A2','gov_action19uhuy5uame2s60yrh6n8cyds8ps5q7tkh05dqlzmpcfy429p9w4qq5ll3g0')]
def write(path,header,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(header);w.writerows(rows)
def main():
 p=argparse.ArgumentParser();p.add_argument('--snapshot',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
 if hashlib.sha256(a.snapshot.read_bytes()).hexdigest()!=EXPECTED_SHA256:raise ValueError('Snapshot checksum mismatch')
 d=json.loads(a.snapshot.read_text(encoding='utf-8'));rby={k:next(r for r in d['rows'] if r['proposal_id']==v) for k,v in ACTIONS}
 for k,v in ACTIONS:
  if sum(r['proposal_id']==v for r in d['rows'])!=1:raise ValueError('Ambiguous proposal ID: '+v)
 a.out.mkdir(parents=True,exist_ok=True)
 write(a.out/'actions.csv',['case_local_key','governance_action_id','action_type','submitted_epoch','ratified_epoch','enacted_epoch','expired_epoch','dropped_epoch','withdrawal_lovelace','withdrawal_recipient_count','source_metadata_title','metadata_url','scope_note'],[[k,r['proposal_id'],r['proposal_type'],r['proposed_epoch'],r.get('ratified_epoch') if r.get('ratified_epoch') is not None else '',r.get('enacted_epoch') if r.get('enacted_epoch') is not None else '',r.get('expired_epoch') if r.get('expired_epoch') is not None else '',r.get('dropped_epoch') if r.get('dropped_epoch') is not None else '',sum(int(w['amount']) for w in r['withdrawal']) if r['proposal_type']=='TreasuryWithdrawals' else '',len(r['withdrawal']) if r['proposal_type']=='TreasuryWithdrawals' else '',r['meta_json']['body'].get('title',''),r['meta_url'],'Koios snapshot; TWD withdrawal is not expenditure; InfoAction has no withdrawal field'] for k,r in rby.items()])
 write(a.out/'sources.csv',['case_local_key','governance_action_id','snapshot_locator','original_metadata_url','metadata_hash_reported_by_koios','snapshot_retrieved_at_utc','source_type','verification_boundary'],[[k,r['proposal_id'],f'rows[proposal_id={r["proposal_id"]}]',r['meta_url'],r.get('meta_hash') or '',d['retrieved_at_utc'],'koios_indexed_governance_action','Koios snapshot includes proposer-authored meta_json; independent IPFS verification not performed'] for k,r in rby.items()])
 write(a.out/'withdrawals.csv',['governance_action_id','withdrawal_index','stake_address','amount_lovelace','snapshot_locator'],[[r['proposal_id'],i,w['stake_address'],w['amount'],f'rows[proposal_id={r["proposal_id"]}].withdrawal[{i}]'] for k,r in rby.items() for i,w in enumerate(r['withdrawal'])])
 motivation=rby['A2']['meta_json']['body']['motivation'];section=motivation.split("#### Transition Into 2026 and 2025's Leftovers",1)[1].split('#### Treasury Management Transparency',1)[0]
 refunds=re.findall(r'- \[([^\]]+) = ₳([\d.]+)k\]\(https://explorer\.cardano\.org/tx/([0-9a-f]{64})\)',section)
 if len(refunds)!=5:raise ValueError('Expected five explicitly cited reported returns')
 write(a.out/'reported-returns.csv',['source_governance_action_id','scope_label','reported_amount_ada','referenced_transaction_hash','source_locator','claim_status'],[[rby['A2']['proposal_id'],name,round(float(amount)*1000),tx,f'rows[proposal_id={rby["A2"]["proposal_id"]}].meta_json.body.motivation > Transition Into 2026 and 2025\'s Leftovers','proposer_attested_not_ledger_verified'] for name,amount,tx in refunds])
 write(a.out/'action-index.csv',['governance_action_id','record_directory','record_kind'],[[v,'records/htep-001/s1-amaru','action_observations_and_source_pointers'] for k,v in ACTIONS])
if __name__=='__main__':main()
