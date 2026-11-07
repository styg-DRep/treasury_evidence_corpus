#!/usr/bin/env python3
"""Reconstruct Orion action and recipient observations from the pinned Koios snapshot.

External published claims in external-sources.csv and external-assertions.csv are
curated source-linked statements and are NOT machine-verified by this extractor.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = "8836d85e6530613d9042cc1f1d7e11e9e6e5a8e9391cda32be527f5a63e7fcd8"
ACTION_ID = "gov_action13qr78nhrhetywapvx2wpm63y9uxpc2dc45zsu9gkncasxqhuhltqqqfu32x"


def write_csv(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(args.snapshot.read_bytes()).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Pinned Koios snapshot SHA-256 mismatch")
    data = json.loads(args.snapshot.read_text(encoding="utf-8"))
    matches = [r for r in data["rows"] if r.get("proposal_id") == ACTION_ID]
    if len(matches) != 1:
        raise ValueError(f"Expected one matching action; found {len(matches)}")
    row = matches[0]
    if row["proposal_type"] != "TreasuryWithdrawals":
        raise ValueError("Unexpected action type")
    withdrawal = row.get("withdrawal") or []
    if len(withdrawal) != 1 or sum(int(w["amount"]) for w in withdrawal) != 50000000000000:
        raise ValueError("Unexpected withdrawal recipients or amount")
    args.out.mkdir(parents=True, exist_ok=True)
    epoch = lambda key: row[key] if row.get(key) is not None else ""
    write_csv(args.out / "actions.csv", [
        "governance_action_id", "action_tx_hash", "proposal_index", "action_type",
        "submitted_epoch", "ratified_epoch", "enacted_epoch", "expired_epoch", "dropped_epoch",
        "withdrawal_lovelace_requested", "withdrawal_recipient_count", "metadata_title", "metadata_url", "boundary"
    ], [[ACTION_ID, row["proposal_tx_hash"], row["proposal_index"], row["proposal_type"],
         epoch("proposed_epoch"), epoch("ratified_epoch"), epoch("enacted_epoch"),
         epoch("expired_epoch"), epoch("dropped_epoch"),
         sum(int(w["amount"]) for w in withdrawal), len(withdrawal),
         row["meta_json"]["body"].get("title", ""), row.get("meta_url", ""),
         "Action amount and enactment do not prove capital deployment to Xverse"]])
    write_csv(args.out / "withdrawals.csv", [
        "governance_action_id", "withdrawal_index", "stake_address", "amount_lovelace", "snapshot_locator"
    ], [[ACTION_ID, i, w["stake_address"], w["amount"],
         f"rows[proposal_id={ACTION_ID}].withdrawal[{i}]"] for i, w in enumerate(withdrawal)])
    write_csv(args.out / "sources.csv", [
        "source_id", "governance_action_id", "source_kind", "source_locator", "metadata_url",
        "metadata_hash_reported_by_koios", "snapshot_retrieved_at_utc", "boundary"
    ], [["K01", ACTION_ID, "pinned_koios_snapshot",
         f"rows[proposal_id={ACTION_ID}]", row.get("meta_url", ""),
         row.get("meta_hash", ""), data.get("retrieved_at_utc", ""),
         "Koios-derived action and proposer metadata; original IPFS bytes not separately hashed here"]])
    write_csv(args.out / "action-index-addition.csv", [
        "governance_action_id", "record_directory", "record_kind"
    ], [[ACTION_ID, "records/htep-001/s6-orion-xverse", "action_observations_and_source_pointers"]])


if __name__ == "__main__":
    main()
