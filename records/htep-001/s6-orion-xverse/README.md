# Orion Fund / Xverse — evidence record

**Evidence Corpus record, v0.1.** Originating investigation: HTEP-001 S6. The record is independently discoverable under the governance-action ID `gov_action13qr78nhrhetywapvx2wpm63y9uxpc2dc45zsu9gkncasxqhuhltqqqfu32x` through `records/action-index.csv`.

## Record identity and source

The on-chain part is reconstructed from the existing pinned Koios snapshot at `sources/cardano-governance/koios/2026-11-03/koios-proposal-list-raw.json`, SHA-256 `8836d85e6530613d9042cc1f1d7e11e9e6e5a8e9391cda32be527f5a63e7fcd8`. The record covers one enacted treasury withdrawal action and separately source-linked public statements about administration, fund financing, and the reported Xverse investment.

- `actions.csv`: action identity, on-chain status, requested withdrawal amount and metadata locator.
- `withdrawals.csv`: one withdrawal recipient and lovelace amount from the Koios snapshot.
- `sources.csv`: precise row and proposer metadata pointers within the pinned source.
- `external-sources.csv`: source URL, publisher, date, retrieval *inspection* date, and access limitations. **No raw web response bodies are claimed.**
- `external-assertions.csv`: small set of manually reviewed publisher assertions; not deterministic output of the extractor.
- `action-index-addition.csv`: one row to merge with existing repository action index (do not replace it).
- `build_case.py`: deterministic extractor for `actions.csv`, `withdrawals.csv`, `sources.csv`, `action-index-addition.csv`.

## Reproduction

From the repository root (use a temporary output directory):

```bash
python records/htep-001/s6-orion-xverse/build_case.py \
  --snapshot sources/cardano-governance/koios/2026-11-03/koios-proposal-list-raw.json \
  --out /tmp/orion-rebuilt

git diff --no-index records/htep-001/s6-orion-xverse/actions.csv /tmp/orion-rebuilt/actions.csv
```

Repeat the comparison for `withdrawals.csv`, `sources.csv`, and `action-index-addition.csv`. On Windows, supply a local temporary path instead of `/tmp/orion-rebuilt`. The script validates the source hash, reads UTF-8 explicitly, and writes LF-terminated CSV.

## Evidence boundaries

- **Ledger record:** Koios reports a 50,000,000 ADA withdrawal enacted in epoch 624. This does *not* establish deployment to Xverse or the amount transferred between entities.
- **Issuer and institutional statements:** The foundation, manager, company and SEC filing describe distinct roles and events. Their statements are recorded as such; they are not a single reconciled capital-flow ledger.
- **Fund financing:** SEC Form D's USD 80m offering and USD 75m sold refer to *fund interests* as reported by the issuer, not treasury expenditure, Orion's Xverse investment amount, or Xverse outcomes.
- **Missing evidence:** Capital calls, treasury-to-vehicle transfer reconciliation, Xverse ticket size, settlement/payment details, and realized returns were not verified. Absence of a recipient-level amount is intentional, not zero.
- **Published sources may change:** External links were inspected as rendered text on 2026-11-06; original web response bytes, timestamps at the HTTP transport level, and page hashes were not captured by this artifact. Future contributors can capture them separately with usage-rights review, but this is not a condition to believe the record is an original HTML archive.

No proposer quality, investment attractiveness, or governance recommendation is encoded. Do not use this bundle as a financial audit or infer that all assets invested by Orion originated with the Treasury.

## Cross-record conventions

`external-assertions.csv` uses a **local descriptive vocabulary** (`reported_investment_in`, `manager_role`, etc.), *not* the governance-action-to-action relationship vocabulary in `schemas/relations-v0.3.md`. A shared cross-institution relation schema is intentionally not introduced for one example. All listed relationship claims point to identified publishers.
