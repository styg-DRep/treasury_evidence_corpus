#!/usr/bin/env python3
"""HTEP-001: fetch a mainnet Koios governance snapshot and build TWD epoch counts.

Run (live):      python build_twd_inventory.py
Run (offline):   python build_twd_inventory.py --from-raw koios-proposal-list-raw.json
                 (also accepts a bare JSON array saved from the Koios URL in a browser)

Requires network access to https://api.koios.rest (live mode only).
No third-party Python packages required.

Revision notes (2026-11-03, vs. the untested first draft):
  * Status precedence is enacted > expired > dropped > ratified. In db-sync (which
    Koios serves), dropped_epoch is also populated when a proposal expires, so the
    first draft would have labelled every expired TWD as "dropped".
  * Pagination is ordered (proposal_tx_hash, proposal_index) so offset pages are stable.
  * Per-action withdrawal totals (lovelace and ADA) and recipient counts are captured,
    so the ~804.4M ADA enacted figure from third-party indexes can be reconciled.
  * The epoch table runs through the current chain epoch (from /tip), so trailing
    zero-submission epochs are included for burstiness work.
  * --from-raw rebuilds every output from a saved payload without touching the network.
"""
import argparse, csv, json, time, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

API = 'https://api.koios.rest/api/v1'
BASE = API + '/proposal_list'
OUT = Path(__file__).resolve().parent
PAGE = 500
PLOMIN_EPOCH = 537  # first epoch in which treasury withdrawals could be ratified
HEADERS = {'Accept': 'application/json', 'User-Agent': 'HTEP-001-recon/0.2'}


def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def pull():
    records = []
    for offset in range(0, 10000, PAGE):
        query = {'limit': PAGE, 'offset': offset, 'order': 'proposal_tx_hash.asc,proposal_index.asc'}
        chunk = get_json(BASE + '?' + urllib.parse.urlencode(query))
        if not isinstance(chunk, list):
            raise RuntimeError('Expected Koios /proposal_list array; got ' + type(chunk).__name__)
        records.extend(chunk)
        if len(chunk) < PAGE:
            return records
        time.sleep(0.15)
    raise RuntimeError('Unusually large result: pagination cap reached')


def current_epoch():
    try:
        tip = get_json(API + '/tip')
        return int(tip[0]['epoch_no'])
    except Exception as exc:  # non-fatal: table just stops at last submission epoch
        print('warning: could not read /tip (' + str(exc) + '); epoch table ends at last submission')
        return None


def field(o, *names):
    for n in names:
        if o.get(n) is not None:
            return o[n]
    return None


def withdrawal_entries(r):
    w = field(r, 'withdrawal', 'withdrawals')
    if w is None:
        return []
    if isinstance(w, dict):
        w = [w]
    if not isinstance(w, list):
        raise RuntimeError('Unexpected withdrawal shape: ' + repr(w)[:300])
    return w


def title_of(r):
    meta = r.get('meta_json')
    if isinstance(meta, dict):
        body = meta.get('body')
        if isinstance(body, dict) and isinstance(body.get('title'), str):
            return body['title'].strip()
    return ''


def save_csv(path, rows, names):
    with path.open('w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-raw', help='rebuild outputs from a saved Koios payload instead of fetching')
    args = ap.parse_args()

    if args.from_raw:
        payload = json.loads(Path(args.from_raw).read_text(encoding='utf-8'))
        if isinstance(payload, dict):
            raw, stamp, tip_epoch = payload['rows'], payload.get('retrieved_at_utc', 'unknown'), payload.get('tip_epoch')
        else:
            raw, stamp, tip_epoch = payload, 'unknown (offline file)', None
    else:
        stamp = datetime.now(timezone.utc).isoformat()
        raw = pull()
        tip_epoch = current_epoch()
        (OUT / 'koios-proposal-list-raw.json').write_text(
            json.dumps({'retrieved_at_utc': stamp, 'source': BASE, 'tip_epoch': tip_epoch, 'rows': raw}, indent=2),
            encoding='utf-8')

    kinds = Counter(str(field(r, 'proposal_type', 'type')) for r in raw)
    twds = [r for r in raw if str(field(r, 'proposal_type', 'type')).lower() in ('treasurywithdrawals', 'treasury_withdrawals')]
    if not twds:
        raise RuntimeError('No TWDs detected. Inspect raw Koios payload and type values: ' + repr(kinds))

    records, seen = [], set()
    for r in twds:
        proposal_id = field(r, 'proposal_id', 'governance_action_id', 'gov_action_id')
        tx_hash = field(r, 'proposal_tx_hash', 'tx_hash')
        index = field(r, 'proposal_index', 'cert_index', 'index')
        key = proposal_id or (f'{tx_hash}#{index}' if tx_hash is not None and index is not None else None)
        if key is None:
            raise RuntimeError('TWD without stable identifier: ' + repr(r)[:500])
        if key in seen:
            raise RuntimeError('Duplicate governance action identifier: ' + str(key))
        seen.add(key)
        submitted = field(r, 'proposed_epoch', 'submitted_epoch', 'submission_epoch')
        if submitted is None:
            raise RuntimeError('Missing proposed_epoch for ' + str(key))
        enacted, expired = field(r, 'enacted_epoch'), field(r, 'expired_epoch')
        dropped, ratified = field(r, 'dropped_epoch'), field(r, 'ratified_epoch')
        if enacted is not None: status = 'enacted'
        elif expired is not None: status = 'expired'
        elif dropped is not None: status = 'dropped'
        elif ratified is not None: status = 'ratified'
        else: status = 'active_or_unresolved'
        entries = withdrawal_entries(r)
        lovelace = sum(int(e.get('amount', 0)) for e in entries)
        records.append({
            'action_id': key, 'submitted_epoch': int(submitted),
            'enacted_epoch': '' if enacted is None else enacted,
            'ratified_epoch': '' if ratified is None else ratified,
            'expired_epoch': '' if expired is None else expired,
            'dropped_epoch': '' if dropped is None else dropped,
            'derived_status': status,
            'withdrawal_lovelace': lovelace, 'withdrawal_ada': f'{lovelace / 1_000_000:.6f}',
            'recipient_count': len(entries),
            'title': title_of(r),
            'tx_hash': tx_hash or '', 'proposal_index': '' if index is None else index,
            'block_time': field(r, 'block_time') or '',
            'metadata_url': field(r, 'meta_url', 'metadata_url') or '',
            'source': 'Koios /proposal_list'})
    records.sort(key=lambda r: (r['submitted_epoch'], r['action_id']))
    save_csv(OUT / 'twd-actions.csv', records, list(records[0]))

    submit_counts = Counter(r['submitted_epoch'] for r in records)
    enact_counts = Counter(int(r['enacted_epoch']) for r in records if r['enacted_epoch'] != '')
    lo = min(PLOMIN_EPOCH, min(submit_counts))
    hi = max([max(submit_counts)] + list(enact_counts) + ([tip_epoch] if tip_epoch else []))
    epochs = []
    for epoch in range(lo, hi + 1):
        rows = [r for r in records if r['submitted_epoch'] == epoch]
        epochs.append({
            'epoch': epoch, 'submitted_count': len(rows),
            'submitted_enacted_count': sum(r['derived_status'] == 'enacted' for r in rows),
            'submitted_expired_count': sum(r['derived_status'] == 'expired' for r in rows),
            'submitted_dropped_count': sum(r['derived_status'] == 'dropped' for r in rows),
            'submitted_other_count': sum(r['derived_status'] not in ('enacted', 'expired', 'dropped') for r in rows),
            'enacted_count': enact_counts[epoch],
            'enacted_ada': f"{sum(r['withdrawal_lovelace'] for r in records if r['enacted_epoch'] != '' and int(r['enacted_epoch']) == epoch) / 1_000_000:.6f}"})
    save_csv(OUT / 'twd-by-epoch.csv', epochs, list(epochs[0]))

    status_counts = Counter(r['derived_status'] for r in records)
    enacted_ada = sum(r['withdrawal_lovelace'] for r in records if r['derived_status'] == 'enacted') / 1_000_000
    summary = {
        'retrieved_at_utc': stamp, 'source': BASE, 'tip_epoch': tip_epoch,
        'all_governance_actions': len(raw), 'governance_action_types': dict(kinds),
        'twd_actions': len(records),
        'first_submitted_epoch': min(submit_counts), 'last_submitted_epoch': max(submit_counts),
        'first_enacted_epoch': min(enact_counts) if enact_counts else None,
        'nonzero_submission_epochs': len(submit_counts),
        'epoch_table_range': [lo, hi],
        'status_counts': dict(status_counts),
        'enacted_withdrawal_ada': round(enacted_ada, 6),
        'reconciliation_vs_third_party_2026_11_03': {
            'expected': {'twd_actions': 107, 'enacted': 70, 'not_approved': 34, 'live': 3, 'enacted_ada_approx': 804427136},
            'observed': {'twd_actions': len(records), 'enacted': status_counts['enacted'],
                         'not_approved': status_counts['expired'] + status_counts['dropped'],
                         'live': status_counts['active_or_unresolved'] + status_counts['ratified'],
                         'enacted_ada': round(enacted_ada)}},
        'notes': ['Derived statuses reflect latest lifecycle fields, not a reconstruction of status at each historic epoch.',
                  'Status precedence: enacted > expired > dropped > ratified (db-sync also sets dropped_epoch on expiry).',
                  'Enacted counts use enacted_epoch; all submission counts use proposed_epoch.',
                  'withdrawal_* columns are per governance action; one action can pay several recipients.',
                  'Third-party figures are checks, not targets; investigate gaps rather than forcing agreement.']}
    (OUT / 'twd-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
