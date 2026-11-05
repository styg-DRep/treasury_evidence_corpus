# Amaru source-linked record — HTEP-001 / S1

**Status:** Experimental Corpus handoff; reproducible observational slice, **not** a validated project accounting record.  
**As-of:** Koios snapshot retrieved `2026-11-03T20:42:44.166123+00:00` (tip epoch 665).

## Parent source (already in the Evidence Corpus)

`sources/cardano-governance/koios/2026-11-03/koios-proposal-list-raw.json`

SHA-256: `8836d85e6530613d9042cc1f1d7e11e9e6e5a8e9391cda32be527f5a63e7fcd8`

Original indexed source: `https://api.koios.rest/api/v1/proposal_list`; indexed action IDs and metadata URLs appear in `sources.csv`. This Corpus contribution **does not** duplicate the full original snapshot and **does not** independently fetch or authenticate the metadata IPFS documents.

## Included

- `actions.csv`: three Koios action-level observations (2025 budget Info Action; 2025 and 2026 TWDs). Zero lovelace on Info Action is not a claim of a zero-size budget. Epoch and amount fields are observations from the dated Koios index.
- `sources.csv`: reproducible action-to-source pointers and provenance caveats.
- `relationships.csv`: two *proposer-attested* documentary links, with their own source pointers and limits. These are reviewed assertions, **not** fields computed from on-chain relationships.
- `build_case.py`: standard-library extraction for `actions.csv` and `sources.csv`; checks the exact parent snapshot hash and rejects silently substituted data.

## Reproduce

From repository root:

```bash
python records/htep-001/s1-amaru/build_case.py \
  --snapshot sources/cardano-governance/koios/2026-11-03/koios-proposal-list-raw.json \
  --out /tmp/amaru-check

diff -u records/htep-001/s1-amaru/actions.csv /tmp/amaru-check/actions.csv
diff -u records/htep-001/s1-amaru/sources.csv /tmp/amaru-check/sources.csv
```

`relationships.csv` must be reviewed against source metadata; the extractor does not auto-validate the meaning of text.

## Boundaries

The snapshot is a Koios-indexed view, not an independently reconstructed ledger; status and amounts reflect the snapshot at retrieval. Metadata text is proposer-authored. Withdrawal amounts are **not** expenditures or recipient-level payments. One action may have multiple withdrawal recipients, and the five reported refunds in the 2026 proposal are **not ledger-verified here**. Refunded funds, costs, contingent reserves, outcomes, and governance motivations are intentionally not reduced to standardized economic fields.

## Independent use

Use the source IDs, structured action observations, and metadata provenance without adopting the Observatory's findings. The case memo, analysis of returned funds, and hypothesis interpretations remain in the **Treasury Observatory** repository. A reader can independently inspect the three source records and form a different interpretation.

## Status relative to HTEP closure

This is **one** candidate case-level handoff. Its contribution to the Evidence Corpus is not accomplished until these files are committed and reviewed; the five other HTEP histories still require an explicit preservation disposition. No claim of complete probe-level Corpus handoff is made.
