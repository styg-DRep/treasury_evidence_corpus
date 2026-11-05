# Catalyst HTTP source captures — 2026-11-05 UTC

These are **exact HTTP response bytes** supplied with a capture manifest, rather than historically original grant-submission versions. Retrieval occurred on 2026-11-05 UTC using direct `urllib` HTTP requests. The included `capture-manifest.json` records request URLs, timestamps, response status, final URLs, content types, byte lengths and SHA-256 hashes. `python verify_captures.py` checks integrity against that supplied manifest. It does not independently attest to the HTTP transactions or site authenticity.

| Capture | Content fidelity | Important boundary |
|---|---|---|
| Fund 2 project 200008 | Substantive server-rendered HTML plus `__NEXT_DATA__` page props | Linked closeout report not captured; displayed page may have been updated since award |
| Fund 8 project 800352 | Substantive server-rendered HTML plus `__NEXT_DATA__` page props | Linked monthly-report evidence attachments not captured |
| Fund 14 project 1400065 | Substantive server-rendered HTML plus `__NEXT_DATA__` page props | Does not prove milestone review decisions or payments |
| Fund 14 Milestone Module project 1400065 | **Only 546-byte JavaScript shell**, with empty `#app` | **No project-specific milestone records preserved**; success HTTP 200 and earlier manifest flag were misleading |

The milestone response remains in the directory as an honest record of the retrieval attempt. Its contents **cannot be used to independently reproduce** the milestone dates, signoffs, allocation warning, or other observations in `records/catalyst/fund-14/project-1400065/milestones.csv`. That table retains its existing public-rendering attribution, not source-byte substantiation. A separate browser-rendered or supported API capture would be needed, if proportional and permitted.

Do not treat the three captured project pages as immutable historical originals. Check licenses, site terms and reuse rights before redistributing HTML captures publicly; retaining checksums, identifiers and source pointers may be safer where publication rights are unclear.
