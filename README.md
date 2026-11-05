# Treasury Evidence Corpus

The **Treasury Evidence Corpus** is a versioned, provenance-preserving collection of public treasury evidence accumulated through research, inquiry, and analysis.

Its purpose is to make treasury evidence easier to reuse without collapsing source material, normalization, analysis, and interpretation into the same layer.

The Corpus is intended to support researchers, governance participants, analysts, and other contributors working on questions about decentralized public funding.

It is not a canonical interpretation of treasury activity.

## Why This Exists

Historical treasury evidence is often distributed across:

- proposals;
- governance actions;
- metadata;
- supporting documents;
- milestone reports;
- audits;
- transaction records;
- funding histories;
- later proposals;
- delivery artifacts;
- outcome evidence.

Research repeatedly incurs the cost of locating, retrieving, interpreting, and restructuring the same source material.

The Corpus exists so that useful evidence work can compound.

A working principle is:

> **Collect once where practical, preserve provenance, interpret cautiously, and leave the evidence more reusable than you found it.**

## Relationship to the Treasury Observatory

The Corpus is related to, but conceptually distinct from, the **Treasury Observatory**.

The Treasury Observatory may investigate questions such as:

- what comparable work appears to cost;
- how estimates change over time;
- whether funding patterns are shifting;
- what trajectories are emerging across treasury activity.

The Corpus provides reusable evidence for such inquiries.

The Corpus itself should not decide what that evidence means.

This distinction allows the evidence base to remain useful even if the Observatory changes form, fragments, or disappears.

## Evidence Layers

The Corpus should preserve at least three distinct layers.

### 1. Source Record

A faithful preservation or structured capture of retrieved source material.

Examples may include:

- proposal text;
- governance metadata;
- linked budget documents;
- milestone reports;
- structured API responses;
- public transaction or funding records.

Where full preservation is not possible or appropriate, the source record should preserve enough identifying information for the original evidence to be recovered.

### 2. Provenance Record

A record of where the evidence came from.

This may include:

- canonical identifier;
- source URL;
- governance action ID;
- transaction hash;
- retrieval date;
- source type;
- source version or revision;
- retrieval method;
- related records.

Provenance should make it possible to trace normalized claims back toward their source.

### 3. Normalized Record

A structured interpretation of selected source evidence according to a versioned schema.

Examples may include:

- requested funding;
- denomination;
- project type;
- duration;
- major cost categories;
- milestone structure;
- prior related funding;
- later funding;
- delivery state.

Normalized records are analytical transformations.

They should never silently replace the underlying source evidence.

## Epistemic Separation

The Corpus should make the following distinctions visible:

**Observation**  
What a source states or records.

**Transformation**  
How source information was categorized, normalized, converted, or derived.

**Interpretation**  
What an analyst believes the transformed evidence may indicate.

**Judgment**  
A conclusion about desirability, pricing, governance action, or public value.

The Corpus primarily stewards the first two.

Interpretation and judgment should normally live in the research, inquiry, or Observatory context that uses the Corpus.

## Repository Structure

An initial structure may look like:

```text
/
├── README.md
├── schemas/
├── proposals/
│   └── <proposal-id>/
│       ├── source.*
│       ├── provenance.*
│       └── normalized.*
├── sources/
├── datasets/
└── docs/
    └── limitations.md
```

The exact structure is experimental and should remain open to revision.

## Schema Development

Schemas should be versioned.

A schema exists to support inquiry, not to maximize field count.

Every proposed field should be able to answer:

> **What inquiry becomes possible because this field exists?**

If a field does not support a meaningful use, its inclusion should be questioned.

Schema revisions should preserve compatibility or document breaking changes where practical.

Changes should not silently rewrite historical interpretation.

## Missing Data

Missing data is not necessarily an error.

A proposal may not provide:

- labor rates;
- explicit cost categories;
- duration;
- milestone detail;
- prior funding history;
- later outcome evidence.

These absences should be represented rather than inferred away.

Patterns of missingness may themselves become useful research evidence.

## Ambiguity

Where source material supports multiple reasonable interpretations, the Corpus should avoid forcing false precision.

Possible approaches include:

- explicit ambiguity markers;
- multiple candidate values;
- confidence or certainty fields;
- source notes;
- unresolved status.

Schema cleanliness should not take priority over epistemic integrity.

## Contribution Process

Evidence contributions should normally arrive through pull requests.

A Corpus PR should make it possible to check:

- whether the source record is faithful;
- whether provenance is sufficient;
- whether normalized fields are traceable to source evidence;
- whether assumptions are explicit;
- whether interpretation has been presented as observation;
- whether schema use is consistent with the declared version.

Reviewers do not need to agree with downstream analytical conclusions.

The primary concern is the quality and traceability of the evidence record.

## Reuse

Corpus records should be structured so that they can support questions that were not anticipated when the record was first created.

This does not require exhaustive collection.

It requires preserving enough source and provenance information that future contributors can extend or reinterpret the record without restarting intake from zero.

## Growth Model

The Corpus should grow through useful work rather than through a premature mandate to ingest everything.

For example:

- one probe needs 30 proposals;
- a later inquiry adds 20 more;
- another researcher contributes a new proposal class;
- repeated intake reveals a recurring need;
- only then might an automated ingestion process be justified.

This allows structure to follow demonstrated demand.

A complete treasury corpus may eventually become valuable.

Completeness is not required for the Corpus to be useful now.

## Relationship to Automation

Manual intake is expected during early formation.

Where repeated work reveals stable patterns, automation may later become appropriate for:

- source retrieval;
- identifier resolution;
- provenance capture;
- schema validation;
- change detection;
- dataset generation.

Automation should preserve traceability rather than obscuring it.

## Data Quality

The Corpus should not claim stronger quality than its evidence supports.

Useful quality dimensions may eventually include:

- source completeness;
- provenance completeness;
- normalization confidence;
- schema validity;
- freshness;
- cross-source consistency.

These should be treated as descriptive properties, not as guarantees of truth.

## Independence

The Corpus should remain usable by:

- independent researchers;
- governance participants;
- proposers;
- analysts;
- auditors;
- funding bodies;
- adjacent observatories;
- competing interpretations.

No single analytical institution should need to control access to the evidence.

## Current First Use

The initial Corpus records are expected to be created through the **Historical Treasury Evidence Probe**.

That probe will test whether approximately 30 historical treasury-funded proposals or governance actions can be represented in a reusable form while preserving provenance, ambiguity, and longitudinal context.

The probe is expected to leave behind:

- source records;
- provenance records;
- normalized records;
- an experimental schema;
- documented limitations.

Those records should remain useful beyond the probe itself.

## Working Principles

> **Evidence should outlive the inquiry that first collected it.**

> **Normalization is an interpretation, not a replacement for source evidence.**

> **Missingness and ambiguity are part of the evidence landscape.**

> **Grow through use; automate only when recurring need earns automation.**

> **The Corpus is a commons asset, not the property of any single interpretation.**
