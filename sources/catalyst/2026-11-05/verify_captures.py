#!/usr/bin/env python3
"""Verify original HTTP response bodies against the handoff manifest (stdlib only)."""
import hashlib, json
from pathlib import Path
here = Path(__file__).resolve().parent
manifest = json.loads((here / "capture-manifest.json").read_text(encoding="utf-8"))
for source in manifest["sources"]:
    path = here / source["local_file"]
    data = path.read_bytes()
    assert len(data) == source["length_bytes"], path
    digest = hashlib.sha256(data).hexdigest()
    assert digest == source["sha256"], path
    print("PASS", source["id"], len(data), digest)
print("Hash checks pass. This does not independently verify site authenticity or record completeness.")
