#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_V0"
TARGET_UNIT_ID = "capability_stop_packet_to_bounded_proposal.parity_repair_packaging_v0"
NEXT_UNIT_ID = "CLOSE_CAPABILITY_PROPOSAL_ADAPTER_AS_REVIEWED_REFERENCE_V0"

SOURCE_PARITY_REPAIR_RECEIPT_ID = "capability_adapter_parity_repair_receipt_947614d6"

PARITY_REPAIR_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0_receipts/capability_adapter_parity_repair_receipt_947614d6.json"
PARITY_REPAIR_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0"
PARITY_REPAIR_RECEIPT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0_receipts"
PARITY_REPAIR_SCRIPT_PATH = ROOT / "scripts/repair_capability_proposal_adapter_negative_control_parity_v0.py"

ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"
ADAPTER_SCRIPT_PATH = ROOT / "scripts/build_capability_stop_packet_to_bounded_proposal_v0.py"
REVIEW_SCRIPT_PATH = ROOT / "scripts/review_capability_stop_packet_to_bounded_proposal_v0.py"

OUT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_parity_repair_packaging_v0"
RECEIPT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_parity_repair_packaging_v0_receipts"

BASIS_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_basis_v0.json"
PACKAGING_PLAN_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_plan_v0.json"
PACKAGING_READOUT_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_readout_v0.json"
PACKAGING_ROLLUP_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_rollup_v0.json"
PACKAGING_PROFILE_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_profile_v0.json"
PACKAGING_REPORT_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_report.json"
PACKAGING_TRANSITION_TRACE_PATH = OUT_DIR / "capability_proposal_adapter_parity_repair_packaging_transition_trace.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    required_files = [
        PARITY_REPAIR_RECEIPT_PATH,
        PARITY_REPAIR_SCRIPT_PATH,
        ADAPTER_RECEIPT_PATH,
        ADAPTER_SCRIPT_PATH,
        REVIEW_SCRIPT_PATH,
    ]

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if not PARITY_REPAIR_DIR.exists():
        failures.append(f"dependency_dir_missing:{rel(PARITY_REPAIR_DIR)}")
    if not PARITY_REPAIR_RECEIPT_DIR.exists():
        failures.append(f"dependency_dir_missing:{rel(PARITY_REPAIR_RECEIPT_DIR)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    repair_receipt = read_json(PARITY_REPAIR_RECEIPT_PATH)
    adapter_receipt = read_json(ADAPTER_RECEIPT_PATH)
    repair_summary = repair_receipt.get("machine_readable_capability_proposal_adapter_negative_control_parity_repair_summary", {})
    adapter_summary = adapter_receipt.get("machine_readable_capability_proposal_adapter_summary", {})
    adapter_neg = adapter_receipt.get("negative_controls", {})

    if repair_receipt.get("receipt_id") != SOURCE_PARITY_REPAIR_RECEIPT_ID:
        failures.append(f"repair_receipt_id_wrong:{repair_receipt.get('receipt_id')}")
    if repair_receipt.get("gate") != "PASS":
        failures.append("repair_receipt_gate_not_pass")
    if repair_summary.get("reference_freeze_ready") is not True:
        failures.append("reference_freeze_not_ready")
    if repair_summary.get("next_unit_id") != NEXT_UNIT_ID:
        failures.append(f"repair_next_unit_wrong:{repair_summary.get('next_unit_id')}")
    if adapter_neg.get("runtime_adoption_authority_count") != 0:
        failures.append("adapter_receipt_runtime_adoption_authority_count_not_zero")
    if adapter_summary.get("proposal_accepted") is not False:
        failures.append("proposal_accepted_should_be_false")
    if adapter_summary.get("implementation_authorized") is not False:
        failures.append("implementation_authorized_should_be_false")
    if adapter_summary.get("runtime_adoption_authorized") is not False:
        failures.append("runtime_adoption_authorized_should_be_false")
    if adapter_summary.get("schema_mutation_authorized") is not False:
        failures.append("schema_mutation_authorized_should_be_false")
    if adapter_summary.get("move_addition_authorized") is not False:
        failures.append("move_addition_authorized_should_be_false")
    if adapter_summary.get("fixture_expansion_authorized") is not False:
        failures.append("fixture_expansion_authorized_should_be_false")
    if adapter_summary.get("runtime_patch_authorized") is not False:
        failures.append("runtime_patch_authorized_should_be_false")
    if adapter_summary.get("hidden_next_command") is not False:
        failures.append("hidden_next_command_should_be_false")
    if adapter_summary.get("c8_authorized") is not False:
        failures.append("c8_authorized_should_be_false")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_READY_REFERENCE_FREEZE_NEXT"
        if gate == "PASS"
        else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_GATE_FAIL"
    )

    package_paths = [
        ".gitignore",
        rel(PARITY_REPAIR_SCRIPT_PATH),
        rel(ADAPTER_SCRIPT_PATH),
        rel(REVIEW_SCRIPT_PATH),
        rel(ADAPTER_RECEIPT_PATH),
        rel(PARITY_REPAIR_DIR),
        rel(PARITY_REPAIR_RECEIPT_DIR),
        rel(OUT_DIR),
        rel(RECEIPT_DIR),
    ]

    basis = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_parity_repair_receipt_id": SOURCE_PARITY_REPAIR_RECEIPT_ID,
        "source_parity_repair_receipt_ref": rel(PARITY_REPAIR_RECEIPT_PATH),
        "basis_claim": "Previous parity repair logic passed but packaging failed because an ignored receipt path was added without force-add.",
        "source_file_hashes": {rel(p): file_sha256(p) for p in required_files},
    }

    packaging_plan = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_plan_v0",
        "plan_status": "READY" if gate == "PASS" else "NOT_READY",
        "packaging_scope": "FORCE_ADD_ALREADY_EMITTED_PARITY_REPAIR_ARTIFACTS_ONLY",
        "paths_to_package": package_paths,
        "requires_force_add": [
            rel(ADAPTER_RECEIPT_PATH),
            rel(PARITY_REPAIR_DIR),
            rel(PARITY_REPAIR_RECEIPT_DIR),
            rel(OUT_DIR),
            rel(RECEIPT_DIR),
        ],
        "does_not_rerun": [
            "capability proposal adapter",
            "adapter review",
            "negative-control parity repair logic",
        ],
        "does_not_authorize": [
            "proposal acceptance",
            "implementation",
            "runtime repair",
            "runtime patch",
            "schema mutation",
            "move addition",
            "fixture expansion",
            "runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "packaging_repair_ready": gate == "PASS",
        "source_logic_result_preserved": repair_receipt.get("gate") == "PASS",
        "source_repair_receipt_id": repair_receipt.get("receipt_id"),
        "adapter_receipt_runtime_adoption_authority_count": adapter_neg.get("runtime_adoption_authority_count"),
        "reference_freeze_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "proposal_accepted": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    readout = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_readout_v0",
        "status": status,
        "repair_type": "PACKAGING_ONLY",
        "source_parity_repair_receipt_id": repair_receipt.get("receipt_id"),
        "source_parity_repair_status": repair_receipt.get("status"),
        "packaging_issue": "ignored receipt path required force-add",
        "reference_freeze_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "interpretation": "Semantic parity repair already passed; this unit only packages the ignored repaired receipt/artifacts."
        if gate == "PASS"
        else "Packaging repair failed typed gates.",
    }

    profile = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_profile_v0",
        "profile_status": status,
        "core_rule": "Package already-passed parity repair artifacts without semantic mutation.",
        "packaging_plan_ref": rel(PACKAGING_PLAN_PATH),
        "reference_freeze_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "must_not_infer": [
            "proposal accepted",
            "capability implementation authorized",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "logic_result": "PRESERVED_PASS" if gate == "PASS" else "NOT_READY",
            "packaging_result": "READY_FOR_FORCE_ADD" if gate == "PASS" else "GATE_FAIL",
            "reference_freeze_ready": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "proposal_accepted": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "NEGATIVE_CONTROL_PARITY_REPAIRED_REFERENCE_FREEZE_READY_BUT_PACKAGING_FAILED",
                "edge": "verify already-emitted repair receipt and packaging scope",
                "to": "PACKAGING_REPAIR_READY" if gate == "PASS" else "PACKAGING_REPAIR_GATE_FAIL",
            },
            {
                "from": "PACKAGING_REPAIR_READY" if gate == "PASS" else "PACKAGING_REPAIR_GATE_FAIL",
                "edge": "force-add ignored repair artifacts",
                "to": "REFERENCE_FREEZE_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (PACKAGING_PLAN_PATH, packaging_plan),
        (PACKAGING_READOUT_PATH, readout),
        (PACKAGING_ROLLUP_PATH, rollup),
        (PACKAGING_PROFILE_PATH, profile),
        (PACKAGING_REPORT_PATH, report),
        (PACKAGING_TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "PARITY_REPAIR_RECEIPT_CONSUMED",
        "PRIOR_REPAIR_LOGIC_PASS_PRESERVED",
        "PACKAGING_FAILURE_CLASSIFIED_AS_IGNORED_PATH_ADD",
        "PACKAGING_SCOPE_FORCE_ADD_ONLY",
        "NO_SEMANTIC_RERUN",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "REFERENCE_FREEZE_READY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "capability_proposal_adapter_parity_repair_packaging_receipt_v0",
        "receipt_type": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_parity_repair_receipt_id": SOURCE_PARITY_REPAIR_RECEIPT_ID,
        "source_parity_repair_receipt_ref": rel(PARITY_REPAIR_RECEIPT_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "PACKAGING_0_PARITY_REPAIR_RECEIPT_CONSUMED": gate == "PASS",
            "PACKAGING_1_PRIOR_REPAIR_LOGIC_PASS": repair_receipt.get("gate") == "PASS",
            "PACKAGING_2_REFERENCE_FREEZE_READY_PRESERVED": repair_summary.get("reference_freeze_ready") is True,
            "PACKAGING_3_ADAPTER_RECEIPT_PARITY_KEY_PRESENT": adapter_neg.get("runtime_adoption_authority_count") == 0,
            "PACKAGING_4_FORCE_ADD_SCOPE_DECLARED": gate == "PASS",
            "PACKAGING_5_NO_SEMANTIC_RERUN": gate == "PASS",
            "PACKAGING_6_NO_PROPOSAL_ACCEPTANCE": adapter_summary.get("proposal_accepted") is False,
            "PACKAGING_7_NO_IMPLEMENTATION": adapter_summary.get("implementation_authorized") is False,
            "PACKAGING_8_NO_RUNTIME_ADOPTION_AUTHORITY": adapter_summary.get("runtime_adoption_authorized") is False,
            "PACKAGING_9_NO_SCHEMA_MUTATION": adapter_summary.get("schema_mutation_authorized") is False,
            "PACKAGING_10_NO_MOVE_ADDITION": adapter_summary.get("move_addition_authorized") is False,
            "PACKAGING_11_NO_C8_AUTHORIZATION": adapter_summary.get("c8_authorized") is False,
            "PACKAGING_12_NO_HIDDEN_NEXT_COMMAND": adapter_summary.get("hidden_next_command") is False,
        },
        "machine_readable_capability_proposal_adapter_parity_repair_packaging_summary": {
            "status": status,
            "packaging_repair_type": "FORCE_ADD_IGNORED_PATHS_ONLY",
            "source_parity_repair_receipt_id": repair_receipt.get("receipt_id"),
            "source_parity_repair_status": repair_receipt.get("status"),
            "adapter_receipt_id": adapter_receipt.get("receipt_id"),
            "adapter_receipt_runtime_adoption_authority_count": adapter_neg.get("runtime_adoption_authority_count"),
            "prior_logic_result_preserved": repair_receipt.get("gate") == "PASS",
            "reference_freeze_ready": gate == "PASS",
            "proposal_status": adapter_receipt.get("proposal_status"),
            "proposal_id": adapter_receipt.get("proposal_id"),
            "proposal_accepted": False,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "packaging_plan": rel(PACKAGING_PLAN_PATH),
            "readout": rel(PACKAGING_READOUT_PATH),
            "rollup": rel(PACKAGING_ROLLUP_PATH),
            "profile": rel(PACKAGING_PROFILE_PATH),
            "report": rel(PACKAGING_REPORT_PATH),
            "transition_trace": rel(PACKAGING_TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "capability_adapter_packaging_repair_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"capability_proposal_adapter_packaging_repair_receipt_id={receipt_id}")
    print(f"capability_proposal_adapter_packaging_repair_receipt_path={rel(receipt_path)}")
    print(f"capability_proposal_adapter_packaging_repair_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
