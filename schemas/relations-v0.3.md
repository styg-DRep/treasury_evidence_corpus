# Governance relationship assertions — vocabulary v0.3

**Status:** Minimal, provisional Evidence Corpus vocabulary. Extends the Amaru v0.2 terms; not a complete Cardano funding ontology. Version applies to relationship *classification*, not the ledger protocol. Records using this version should cite `schemas/relations-v0.3.md`.

## Principles

- A relation row is an **evidence-backed assertion** between identifiable records, not a ledger-native edge or an independently verified causal finding.
- `from_action` is the later/referencing action; `to_action` is the referenced earlier action. Both must use full governance-action IDs.
- `relationship` is a curator classification. `assertion_type` describes the source author's claim. The two must not be conflated.
- `evidence_action_id` and `source_locator` point to the record supporting a claim. `verification_boundary` limits the claim; `lookup_transformation` identifies any intermediary match.
- Multiple relations may coexist; shared projects, actors, or recipients do **not** themselves establish project continuity. Lack of a relation row does not mean absence of a relationship.
- Source metadata may report earlier awards, approvals, or concerns. Those claims are not independent verification of award outcomes, vote rationales, execution or actual spending.

## Terms

| Term | Meaning and boundary |
| --- | --- |
| `continuation_of` | A later request expressly describes itself as a subsequent/continuing funding request relative to an earlier action. Does not verify unchanged scope, delivery or outcomes. |
| `references_prior_budget` | The source explicitly references a prior budget Info Action by its governance-action ID. Does not prove approval in a governance-vote sense. |
| `follows_budget_statement` | A withdrawal links a prior budget statement by transaction hash, resolved to a specific Info Action through a documented hash-to-action lookup. |
| `references_prior_funding` | A later request names a prior funding award/action as part of its history, **without** asserting identical scope or continuation. |
| `revision_of` | A later action explicitly identifies an earlier request and describes its own changed terms, clarification or version. Actions remain distinct on-chain. |

`resubmission_of` is **not** needed for the Eternl sample; a new action that revises a previous request is documented with `revision_of`. Later probes may introduce additional distinctions when evidence requires them.

## Locator and version conventions

`rows[proposal_id=<full-id>].meta_json.body.<field>` means identify exactly one row in the pinned Koios `rows` array and inspect the named nested field. A suffix ` > <heading>` points to a heading inside that text, **not** a JSON key. A URL/transaction referenced by a proposer is separate from its independently verified ledger disposition.

The Amaru bundle originally defines a `v0.2` vocabulary inline. This `v0.3` file preserves those terms unchanged while adding `references_prior_funding` and `revision_of`. If Amaru's README is updated to reference v0.3, that is documentation maintenance, **not** a reclassification of its three reviewed relationships.
