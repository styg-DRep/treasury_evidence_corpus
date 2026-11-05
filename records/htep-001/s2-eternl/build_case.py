#!/usr/bin/env python3
"""Extract exact action/recipient/source observations from a pinned Koios snapshot."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = '8836d85e6530613d9042cc1f1d7e11e9e6e5a8e9391cda32be527f5a63e7fcd8'
ACTIONS = [
    ('E1','gov_action13tfag48nf94rtjcdq7c06vhkslmxxw9h6c88sl7q5g5nnewcsvlpqx4t762'),
    ('E2','gov_action1ngpqafax5rvp8lcgey4asvqtycrh4e56fwp8cn2r9trx2ysryhtsqdm3w3z'),
    ('E3','gov_action1lwudrf9g66mzlrxhq62y5pvzhzzv9wgps7u04kne202udge7kknsqlgmhse'),
]

def write_csv(path, header, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(args.snapshot.read_bytes()).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Koios snapshot SHA-256 does not match pinned source')
    snapshot = json.loads(args.snapshot.read_text(encoding='utf-8'))
    rows = snapshot['rows']
    by_id = {}
    for key, action_id in ACTIONS:
        matches = [row for row in rows if row.get('proposal_id') == action_id]
        if len(matches) != 1:
            raise ValueError(f'Expected one row for {action_id}; found {len(matches)}')
        by_id[key] = matches[0]
        if matches[0]['proposal_type'] != 'TreasuryWithdrawals':
            raise ValueError(f'Unexpected action type for {action_id}')
    args.out.mkdir(parents=True, exist_ok=True)
    def epoch(r, name):
        return r[name] if r.get(name) is not None else ''
    write_csv(args.out/'actions.csv',
        ['case_local_key','governance_action_id','action_type','submitted_epoch','ratified_epoch','enacted_epoch','expired_epoch','dropped_epoch','withdrawal_lovelace_requested','withdrawal_recipient_count','source_metadata_title','metadata_url','scope_note'],
        [[key, r['proposal_id'], r['proposal_type'], r['proposed_epoch'], epoch(r,'ratified_epoch'), epoch(r,'enacted_epoch'), epoch(r,'expired_epoch'), epoch(r,'dropped_epoch'), sum(int(w['amount']) for w in r['withdrawal']),len(r['withdrawal']), r['meta_json']['body'].get('title',''), r['meta_url'], 'Action withdrawal field records requested ADA; enactment and execution must be evaluated separately'] for key,r in by_id.items()])
    write_csv(args.out/'sources.csv',
        ['case_local_key','governance_action_id','snapshot_locator','original_metadata_url','metadata_hash_reported_by_koios','snapshot_retrieved_at_utc','source_type','verification_boundary'],
        [[key,r['proposal_id'],f'rows[proposal_id={r["proposal_id"]}]',r['meta_url'],r.get('meta_hash') or '',snapshot['retrieved_at_utc'],'koios_indexed_governance_action','Koios includes proposer-authored metadata; independent IPFS content validation not performed'] for key,r in by_id.items()])
    write_csv(args.out/'withdrawals.csv',
        ['governance_action_id','withdrawal_index','stake_address','amount_lovelace','snapshot_locator'],
        [[r['proposal_id'], i, w['stake_address'], w['amount'],f'rows[proposal_id={r["proposal_id"]}].withdrawal[{i}]'] for r in by_id.values() for i,w in enumerate(r['withdrawal'])])
    write_csv(args.out/'action-index.csv',
        ['governance_action_id','record_directory','record_kind'],
        [[action_id,'records/htep-001/s2-eternl','action_observations_and_source_pointers'] for _,action_id in ACTIONS])

if __name__ == '__main__':
    main()
