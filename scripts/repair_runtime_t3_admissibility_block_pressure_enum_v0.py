#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAILED_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0_receipts/1379a1e1.json"
EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
TARGET_SCRIPT_PATH = ROOT / "scripts/prepare_runtime_t3_admissibility_block_case_contract_v0.py"

def read_json(path: Path):
    return json.loads(path.read_text())

def pick_enum(enum_values, preferred, contains):
    for p in preferred:
        if p in enum_values:
            return p
    matches = [x for x in enum_values if contains in str(x)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        matches_sorted = sorted(matches, key=lambda x: (len(str(x)), str(x)))
        return matches_sorted[0]
    return None

failed = read_json(FAILED_RECEIPT_PATH)
contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)

failures = failed.get("failures", [])
if "ADMISSIBILITY_BLOCK_not_in_expected_pressure_enum" not in failures:
    raise SystemExit("STOP_REPAIR_NOT_MATCHING_FAILURE: expected ADMISSIBILITY_BLOCK_not_in_expected_pressure_enum")

pressure_enum = contract.get("closed_pressure_enum", [])
outcome_enum = contract.get("closed_outcome_enum", [])

pressure_token = pick_enum(
    pressure_enum,
    [
        "ADMISSIBILITY_FAIL",
        "ADMISSIBILITY_DENIED",
        "ADMISSIBILITY_DENY",
        "ADMISSIBILITY_REJECTED",
        "RUNTIME_ADMISSIBILITY_FAIL",
        "RUNTIME_ADMISSIBILITY_BLOCK",
    ],
    "ADMISSIBILITY",
)

outcome_token = pick_enum(
    outcome_enum,
    [
        "RUNTIME_SMOKE_BLOCKED_ADMISSIBILITY",
        "RUNTIME_SMOKE_ADMISSIBILITY_FAIL",
        "RUNTIME_SMOKE_ADMISSIBILITY_DENIED",
        "RUNTIME_BLOCKED_ADMISSIBILITY",
    ],
    "ADMISSIBILITY",
)

if not pressure_token:
    print(json.dumps({
        "repair_gate": "STOP",
        "reason": "NO_EXISTING_ADMISSIBILITY_PRESSURE_ENUM_TOKEN",
        "closed_pressure_enum": pressure_enum,
        "required_human_next": "decide whether taxonomy update is authorized",
    }, indent=2, sort_keys=True))
    raise SystemExit(2)

if not outcome_token:
    print(json.dumps({
        "repair_gate": "STOP",
        "reason": "NO_EXISTING_ADMISSIBILITY_OUTCOME_ENUM_TOKEN",
        "closed_outcome_enum": outcome_enum,
        "required_human_next": "decide whether taxonomy update is authorized",
    }, indent=2, sort_keys=True))
    raise SystemExit(2)

text = TARGET_SCRIPT_PATH.read_text()

# Replace the bad invented pressure token everywhere in the preparer.
text = text.replace('"ADMISSIBILITY_BLOCK"', json.dumps(pressure_token))
text = text.replace("'ADMISSIBILITY_BLOCK'", repr(pressure_token))

# Align stop code to the selected existing pressure token while preserving meaning.
stop_code = "STOP_RUNTIME_" + re.sub(r"[^A-Z0-9]+", "_", pressure_token).strip("_")
text = text.replace('"STOP_RUNTIME_ADMISSIBILITY_BLOCK"', json.dumps(stop_code))
text = text.replace("'STOP_RUNTIME_ADMISSIBILITY_BLOCK'", repr(stop_code))

# Align outcome token only if a different existing outcome is required.
text = text.replace('"RUNTIME_SMOKE_BLOCKED_ADMISSIBILITY"', json.dumps(outcome_token))
text = text.replace("'RUNTIME_SMOKE_BLOCKED_ADMISSIBILITY'", repr(outcome_token))

# Make status/summary names still readable; do not alter unit id.
TARGET_SCRIPT_PATH.write_text(text)

print(json.dumps({
    "repair_gate": "PASS",
    "failed_receipt_id": failed.get("receipt_id"),
    "failed_receipt_path": str(FAILED_RECEIPT_PATH.relative_to(ROOT)),
    "pressure_token_selected": pressure_token,
    "outcome_token_selected": outcome_token,
    "stop_code_selected": stop_code,
    "patched_script": str(TARGET_SCRIPT_PATH.relative_to(ROOT)),
    "repair_scope": "local enum alignment only",
    "taxonomy_created": False,
    "schema_created": False,
    "runtime_patched": False,
}, indent=2, sort_keys=True))
