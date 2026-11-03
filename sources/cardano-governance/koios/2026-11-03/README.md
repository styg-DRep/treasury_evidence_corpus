# Koios governance-action snapshot — 2026-11-03

This directory preserves one dated Cardano **mainnet governance-action snapshot** and a reproducible extraction of Treasury Withdrawal governance actions (TWDs). It is an evidence contribution to the Treasury Evidence Corpus, prepared during the Observatory's Historical Treasury Evidence Probe (HTEP-001).

It documents what was available from the source at retrieval time. It does **not** classify funding initiatives, judge proposals, or adopt the Observatory's interpretations of budget processes.

## Source and observation boundary

| Property | Value |
|---|---|
| Source | [Koios API — `/api/v1/proposal_list`](https://api.koios.rest/api/v1/proposal_list) |
| Network | Cardano mainnet |
| Retrieved (UTC) | `2026-11-03T20:42:44.166123+00:00` |
| Chain tip reported at retrieval | Epoch `665` |
| Original record set | 162 governance actions of all types |
| TWD population extracted | 107 distinct `TreasuryWithdrawals` actions |
| Earliest / latest TWD submission epoch | `566` / `662` |
| Epoch table coverage | `537`–`665`, inclusive; includes zero-submission epochs |

The timestamp and chain tip are preserved in the wrapper of `koios-proposal-list-raw.json`. This is a **point-in-time indexed-source snapshot**, not a live query or independent validation of Koios against another node/indexer.

## Files

| File | Role |
|---|---|
| `koios-proposal-list-raw.json` | Preserved Koios response in a provenance wrapper (`retrieved_at_utc`, `source`, `tip_epoch`, `rows`). Contains all 162 returned governance actions; **source snapshot**. |
| `build_twd_inventory.py` | Transformation script for rebuilding the three outputs; **processing method**. |
| `twd-actions.csv` | One row per unique TWD governance-action ID, with submission/enactment epochs, derived snapshot status, withdrawal amount, recipient count, title and source pointers; **derived inventory**. |
| `twd-by-epoch.csv` | Counts by submission epoch, submission-cohort outcomes, enactment counts and enacted ADA, including zero-activity epochs; **derived aggregation**. |
| `twd-summary.json` | Source snapshot metadata, counts, lifecycle totals and reconciliation checks; **derived summary**. |

The raw source contains more fields than are projected into the CSVs, including proposal metadata, references and other governance-action types. Retain it without replacing it with the narrower extraction.

## Rebuild and verify

Requires Python 3 and its standard library; no third-party Python dependencies.

From this directory:

```bash
python build_twd_inventory.py --from-raw koios-proposal-list-raw.json
```

This offline command recreates `twd-actions.csv`, `twd-by-epoch.csv`, and `twd-summary.json` from the preserved wrapper, including the original retrieval timestamp and chain-tip epoch. It **overwrites** those output files. For a non-destructive comparison, run it in a temporary copy of the directory.

A live refresh can be obtained with:

```bash
python build_twd_inventory.py
```

**Do not run live refresh in this dated snapshot directory:** it would overwrite the preserved raw snapshot and derived files. Create a new date-stamped directory for a new retrieval. The live endpoint is a changing indexed data source, so later outputs need not reproduce this snapshot.

The initial extraction was regenerated from the provenance-wrapped raw JSON. The action and epoch CSVs reproduced identically; the corrected summary retained the timestamp and tip epoch that an earlier rebuild from a bare JSON array had lost.

## Snapshot checks

| Measure | Observed |
|---|---:|
| Governance actions of all types | 162 |
| Unique TWD actions | 107 |
| Enacted at snapshot | 70 |
| Expired at snapshot | 34 |
| Active / unresolved at snapshot | 3 |
| Total ADA specified in enacted TWD withdrawal entries | ₳804,427,136 |
| Epochs with at least one TWD submission | 33 |

All 107 TWD identifiers are unique in this extraction. A TWD governance action can contain multiple withdrawal entries: 105 actions have one recipient and two actions have five. Therefore, **action count is not recipient count**.

## Interpretation and limitations

- **Unit of observation:** one on-chain TWD governance action, not necessarily one funding initiative, recipient, submitted budget, or delivered project. Related or resubmitted actions have **not** been deduplicated into initiatives.
- **Lifecycle:** `derived_status` is inferred from the lifecycle fields present **at this snapshot**. The script prioritizes `enacted_epoch` over `expired_epoch`, then `dropped_epoch`, then `ratified_epoch`; Koios/db-sync may populate both `expired_epoch` and `dropped_epoch` for the same expired action. This is not a historical reconstruction of status at every epoch.
- **Temporal semantics:** `submitted_count` groups by `proposed_epoch`; `enacted_count` and `enacted_ada` group by `enacted_epoch`. Do not equate submission with enactment.
- **Amounts:** `withdrawal_lovelace` and `withdrawal_ada` are the per-action totals of ledger-described withdrawal entries. They are **not** evidence of subsequent administrator expenditures, milestone disbursements, completed delivery, or public value.
- **Metadata:** Proposal titles and descriptions are off-chain metadata returned by Koios and may be missing or unavailable. `meta_json.body.rationale` is the **proposal author's rationale**, not an individual DRep's voting rationale.
- **Completeness:** Counts reflect actions returned by the queried index at retrieval time, not an independently audited guarantee of universal completeness. Live/unresolved outcomes may change.
- **Scope:** This snapshot contains CIP-1694 governance actions; it is **not** a historical inventory of Project Catalyst allocations or all prior treasury spending mechanisms.

## Relationship to the Treasury Observatory

The Observatory's budget-process reconstructions, institutional-role hypotheses, resubmission analysis, and Net Change Limit interpretations are separate research products. They may **cite** these immutable source and derived records, but those interpretations are not embedded as facts in this snapshot.

If an evidence relationship becomes independently verified and reusable—such as a governance-action ID linked to a specific off-chain proposal—it can be contributed as a separately provenanced Corpus record without rewriting this source snapshot.

**Provenance principle:** retain the original record, make transformations reproducible, preserve missingness and uncertainty, and allow downstream investigators to reach different interpretations from the same evidence.
