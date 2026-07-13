#!/usr/bin/env python3
"""Independently verify an emitted Post-VS2 first execution decision receipt v0."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
AUTH_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"
SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    root = Path.cwd().resolve()
    failures: list[str] = []
    if str(root) != ROOT:
        failures.append(f"repo_root_wrong:{root}")
    auth_json = root / AUTH_JSON
    auth_md = root / AUTH_MD
    if not auth_json.exists() or not auth_md.exists():
        failures.append("authoritative_receipt_pair_missing")
    if not failures:
        receipt = json.loads(auth_json.read_text(encoding="utf-8"))
        payload = receipt.get("receipt_binding", {}).get("receipt_payload", {})
        if sha256_bytes(canonical_bytes(payload)) != receipt.get("receipt_binding", {}).get("receipt_sha256"):
            failures.append("receipt_hash_wrong")
        if not str(payload.get("receipt_id", "")).startswith(f"receipt::{SURFACE_HASH}::post_vs2_decision_event::"):
            failures.append("receipt_id_not_surface_bound")
        surface = json.loads((root / SURFACE_JSON).read_text(encoding="utf-8"))
        if surface.get("surface_payload_sha256") != SURFACE_HASH:
            failures.append("surface_hash_wrong")
        if payload.get("source_identity_count") != 44 or payload.get("source_linkage_count") != 11:
            failures.append("source_binding_counts_wrong")
    print(json.dumps({
        "authoritative_receipt_verifier_gate": "PASS" if not failures else "FAIL",
        "failures": failures,
    }, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
