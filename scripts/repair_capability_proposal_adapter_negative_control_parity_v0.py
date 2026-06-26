#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_V0"
TARGET_UNIT_ID = "capability_stop_packet_to_bounded_proposal.negative_control_parity_repair_v0"
NEXT_UNIT_ID = "CLOSE_CAPABILITY_PROPOSAL_ADAPTER_AS_REVIEWED_REFERENCE_V0"

SOURCE_REVIEW_RECEIPT_ID = "capability_adapter_review_receipt_9c306ed5"
SOURCE_ADAPTER_RECEIPT_ID = "capability_adapter_receipt_8c7f0905"

REVIEW_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0_receipts/capability_adapter_review_receipt_9c306ed5.json"
REPAIR_TARGET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0/capability_proposal_adapter_negative_control_parity_repair_target_v0.json"
PARITY_REVIEW_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0/capability_proposal_adapter_negative_control_parity_review_v0.json"

ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"
ADAPTER_ROLLUP_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_rollup_v0.json"
ADAPTER_SCRIPT_PATH = ROOT / "scripts/build_capability_stop_packet_to_bounded_proposal_v0.py"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
NORMALIZED_STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0"
RECEIPT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0_receipts"

BASIS_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_basis_v0.json"
BEFORE_AFTER_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_before_after_v0.json"
POST_REPAIR_REVIEW_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_post_repair_review_v0.json"
REPAIR_READOUT_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_readout_v0.json"
REPAIR_ROLLUP_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_rollup_v0.json"
REPAIR_PROFILE_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_profile_v0.json"
REPAIR_REPORT_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_report.json"
REPAIR_TRANSITION_TRACE_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_transition_trace.json"

MISSING_KEY = "runtime_adoption_authority_count"

REQUIRED_NEGATIVE_CONTROLS = [
    "implementation_started_count",
    "runtime_repaired_count",
    "schema_mutated_count",
    "move_added_count",
    "fixture_expanded_count",
    "runtime_patched_count",
    "live_hook_installed_count",
    "runtime_adoption_authority_count",
    "c8_authorized_count",
    "proposal_accepted_count",
    "hidden_next_command_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "ambient_workspace_inference_count",
    "prior_receipt_mutation_count",
]

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

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def patch_adapter_script(script_path: Path) -> Dict[str, Any]:
    text_before = script_path.read_text()
    already_present = f'"{MISSING_KEY}": 0' in text_before

    if already_present:
        return {
            "script_patch_status": "ALREADY_PRESENT",
            "script_changed": False,
            "script_sha256_before": hashlib.sha256(text_before.encode()).hexdigest(),
            "script_sha256_after": hashlib.sha256(text_before.encode()).hexdigest(),
        }

    needle = '    "live_hook_installed_count": 0,\n    "c8_authorized_count": 0,'
    replacement = '    "live_hook_installed_count": 0,\n    "runtime_adoption_authority_count": 0,\n    "c8_authorized_count": 0,'

    if needle not in text_before:
        raise RuntimeError("script_patch_anchor_missing")

    text_after = text_before.replace(needle, replacement, 1)
    script_path.write_text(text_after)

    return {
        "script_patch_status": "PATCHED",
        "script_changed": True,
        "script_sha256_before": hashlib.sha256(text_before.encode()).hexdigest(),
        "script_sha256_after": hashlib.sha256(text_after.encode()).hexdigest(),
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        REVIEW_RECEIPT_PATH,
        REPAIR_TARGET_PATH,
        PARITY_REVIEW_PATH,
        ADAPTER_RECEIPT_PATH,
        ADAPTER_ROLLUP_PATH,
        ADAPTER_SCRIPT_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        NORMALIZED_STOP_PACKET_PATH,
    ]

    failures: List[str] = []
    protected_files = [
        REVIEW_RECEIPT_PATH,
        REPAIR_TARGET_PATH,
        PARITY_REVIEW_PATH,
        ADAPTER_ROLLUP_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        NORMALIZED_STOP_PACKET_PATH,
    ]

    source_hashes_before = {}
    protected_hashes_before = {}

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")
        else:
            source_hashes_before[rel(p)] = file_sha256(p)

    for p in protected_files:
        if p.exists():
            protected_hashes_before[rel(p)] = file_sha256(p)

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    review_receipt = read_json(REVIEW_RECEIPT_PATH)
    repair_target = read_json(REPAIR_TARGET_PATH)
    parity_review = read_json(PARITY_REVIEW_PATH)
    adapter_receipt_before = read_json(ADAPTER_RECEIPT_PATH)
    adapter_rollup = read_json(ADAPTER_ROLLUP_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)

    review_summary = review_receipt.get("machine_readable_capability_proposal_adapter_review_summary", {})
    adapter_summary = adapter_receipt_before.get("machine_readable_capability_proposal_adapter_summary", {})

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review_receipt.get('receipt_id')}")
    if review_receipt.get("gate") != "PASS":
        failures.append("review_gate_not_pass")
    if review_summary.get("local_repair_required") is not True:
        failures.append("review_did_not_require_local_repair")
    if review_summary.get("repair_target_unit_id") != UNIT_ID:
        failures.append(f"repair_target_unit_wrong:{review_summary.get('repair_target_unit_id')}")
    if review_summary.get("missing_receipt_negative_control_keys") != [MISSING_KEY]:
        failures.append(f"review_missing_key_unexpected:{review_summary.get('missing_receipt_negative_control_keys')}")
    if review_summary.get("missing_rollup_negative_control_keys") != []:
        failures.append(f"rollup_missing_keys_unexpected:{review_summary.get('missing_rollup_negative_control_keys')}")

    if repair_target.get("target_status") != "READY":
        failures.append("repair_target_not_ready")
    if repair_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"repair_target_next_wrong:{repair_target.get('next_unit_id')}")
    if repair_target.get("repair_scope") != "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY":
        failures.append(f"repair_scope_wrong:{repair_target.get('repair_scope')}")
    if repair_target.get("missing_receipt_negative_control_keys") != [MISSING_KEY]:
        failures.append("repair_target_missing_keys_wrong")
    if repair_target.get("missing_rollup_negative_control_keys") != []:
        failures.append("repair_target_rollup_missing_keys_wrong")

    if parity_review.get("review_status") != "LOCAL_REPAIR_REQUIRED":
        failures.append("parity_review_status_wrong")
    if parity_review.get("receipt_missing_keys") != [MISSING_KEY]:
        failures.append("parity_review_missing_keys_wrong")
    if parity_review.get("rollup_missing_keys") != []:
        failures.append("parity_review_rollup_missing_keys_wrong")
    if parity_review.get("receipt_nonzero") not in ({}, None):
        failures.append("receipt_nonzero_not_empty")
    if parity_review.get("rollup_nonzero") not in ({}, None):
        failures.append("rollup_nonzero_not_empty")

    if adapter_receipt_before.get("receipt_id") != SOURCE_ADAPTER_RECEIPT_ID:
        failures.append(f"adapter_receipt_id_wrong:{adapter_receipt_before.get('receipt_id')}")
    if adapter_receipt_before.get("gate") != "PASS":
        failures.append("adapter_receipt_gate_not_pass")
    if adapter_summary.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append("proposal_status_not_candidate_only")
    if adapter_summary.get("proposal_accepted") is not False:
        failures.append("proposal_already_accepted")
    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "proposal_accepted",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(adapter_summary, key, failures)

    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append("proposal_artifact_not_candidate_only")
    if human_decision.get("default_decision") != "DEFER":
        failures.append("human_decision_default_not_defer")
    if human_decision.get("implementation_authorized") is not False:
        failures.append("human_decision_implementation_authorized")

    adapter_neg_before = dict(adapter_receipt_before.get("negative_controls", {}))
    rollup_neg = adapter_rollup.get("negative_controls", {})

    if MISSING_KEY in adapter_neg_before:
        failures.append("missing_key_already_present_before_repair")
    if MISSING_KEY not in rollup_neg:
        failures.append("rollup_key_missing_unexpected")
    if rollup_neg.get(MISSING_KEY) != 0:
        failures.append(f"rollup_key_nonzero:{rollup_neg.get(MISSING_KEY)}")

    if failures:
        gate = "FAIL"
        status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_GATE_FAIL"
        script_patch_result = {
            "script_patch_status": "NOT_ATTEMPTED",
            "script_changed": False,
        }
        adapter_receipt_after = adapter_receipt_before
    else:
        gate = "PASS"

        adapter_receipt_after = json.loads(json.dumps(adapter_receipt_before))
        adapter_receipt_after.setdefault("negative_controls", {})
        adapter_receipt_after["negative_controls"][MISSING_KEY] = 0
        adapter_receipt_after.setdefault("repair_history", [])
        adapter_receipt_after["repair_history"].append({
            "repair_unit_id": UNIT_ID,
            "repair_scope": "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY",
            "added_negative_control_key": MISSING_KEY,
            "added_value": 0,
            "source_review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
            "proposal_accepted": False,
            "implementation_authorized": False,
        })
        write_json(ADAPTER_RECEIPT_PATH, adapter_receipt_after)

        try:
            script_patch_result = patch_adapter_script(ADAPTER_SCRIPT_PATH)
        except Exception as e:
            gate = "FAIL"
            failures.append(f"script_patch_failed:{e}")
            status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_GATE_FAIL"
        else:
            status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIRED_REFERENCE_FREEZE_READY"

    # Validate after-state.
    adapter_receipt_after = read_json(ADAPTER_RECEIPT_PATH)
    adapter_neg_after = dict(adapter_receipt_after.get("negative_controls", {}))
    missing_after = [k for k in REQUIRED_NEGATIVE_CONTROLS if k not in adapter_neg_after]
    nonzero_after = {k: v for k, v in adapter_neg_after.items() if v != 0}

    if gate == "PASS":
        if missing_after:
            gate = "FAIL"
            status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_POST_CHECK_FAIL"
            failures.append(f"negative_controls_still_missing:{missing_after}")
        if nonzero_after:
            gate = "FAIL"
            status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_POST_CHECK_FAIL"
            failures.append(f"negative_controls_nonzero_after:{nonzero_after}")
        if f'"{MISSING_KEY}": 0' not in ADAPTER_SCRIPT_PATH.read_text():
            gate = "FAIL"
            status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_POST_CHECK_FAIL"
            failures.append("adapter_script_missing_new_counter_after_patch")

    protected_hashes_after = {rel(p): file_sha256(p) for p in protected_files}
    protected_mutations = [
        path for path, before_hash in protected_hashes_before.items()
        if protected_hashes_after.get(path) != before_hash
    ]

    if protected_mutations:
        gate = "FAIL"
        status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_PROTECTED_SOURCE_MUTATION_FAIL"
        failures.append(f"protected_sources_mutated:{protected_mutations}")

    before_after = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_before_after_v0",
        "adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
        "adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "negative_controls_before": adapter_neg_before,
        "negative_controls_after": adapter_neg_after,
        "added_keys": [MISSING_KEY] if MISSING_KEY not in adapter_neg_before and adapter_neg_after.get(MISSING_KEY) == 0 else [],
        "missing_after": missing_after,
        "nonzero_after": nonzero_after,
        "script_patch_result": script_patch_result,
        "protected_mutations": protected_mutations,
    }

    post_repair_review = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_post_repair_review_v0",
        "review_status": "PARITY_CLEAN" if gate == "PASS" else "PARITY_REPAIR_FAILED",
        "required_negative_controls": REQUIRED_NEGATIVE_CONTROLS,
        "adapter_receipt_negative_controls_present": sorted(adapter_neg_after.keys()),
        "adapter_receipt_missing_keys_after_repair": missing_after,
        "adapter_receipt_nonzero_after_repair": nonzero_after,
        "rollup_negative_controls_present": sorted(rollup_neg.keys()),
        "rollup_key_status": {
            MISSING_KEY: rollup_neg.get(MISSING_KEY),
        },
        "reference_freeze_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    basis = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "source_files_before": source_hashes_before,
        "repair_scope": "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY",
        "repair_claim": "Add runtime_adoption_authority_count=0 to the adapter receipt negative controls and patch the adapter harness so future receipts emit the same key.",
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

    rollup_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "repair_scope": "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY",
        "adapter_receipt_repaired": gate == "PASS",
        "adapter_script_patched": bool(script_patch_result.get("script_changed")) or script_patch_result.get("script_patch_status") == "ALREADY_PRESENT",
        "added_negative_control_keys": [MISSING_KEY] if gate == "PASS" else [],
        "negative_control_parity_clean": gate == "PASS",
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

    readout_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_readout_v0",
        "status": status,
        "adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "repaired_key": MISSING_KEY if gate == "PASS" else None,
        "repaired_value": 0 if gate == "PASS" else None,
        "reference_freeze_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "interpretation": "Local negative-control parity repaired. Adapter remains a proposal candidate bridge only; no proposal acceptance or implementation authority was created." if gate == "PASS" else "Parity repair failed typed gates.",
    }

    profile_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_profile_v0",
        "profile_status": status,
        "core_rule": "Repair local negative-control parity only; do not alter proposal semantics or authority boundaries.",
        "adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
        "repair_target_ref": rel(REPAIR_TARGET_PATH),
        "before_after_ref": rel(BEFORE_AFTER_PATH),
        "post_repair_review_ref": rel(POST_REPAIR_REVIEW_PATH),
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

    report_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "repair_result": "LOCAL_PARITY_REPAIRED" if gate == "PASS" else "REPAIR_FAILED",
            "added_counter": MISSING_KEY if gate == "PASS" else None,
            "added_value": 0 if gate == "PASS" else None,
            "adapter_bridge_semantics_changed": False,
            "proposal_accepted": False,
            "implementation_authorized": False,
            "reference_freeze_ready": gate == "PASS",
        },
        "failures": failures,
    }

    transition_trace_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "VALID_PROPOSAL_BRIDGE_NEEDS_LOCAL_PARITY_REPAIR",
                "edge": "add missing negative-control counter at zero",
                "to": "NEGATIVE_CONTROL_PARITY_REPAIRED" if gate == "PASS" else "REPAIR_GATE_FAIL",
            },
            {
                "from": "NEGATIVE_CONTROL_PARITY_REPAIRED" if gate == "PASS" else "REPAIR_GATE_FAIL",
                "edge": "post-repair parity check",
                "to": "REFERENCE_FREEZE_READY" if gate == "PASS" else "STOP_REPAIR_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (BEFORE_AFTER_PATH, before_after),
        (POST_REPAIR_REVIEW_PATH, post_repair_review),
        (REPAIR_READOUT_PATH, readout_out),
        (REPAIR_ROLLUP_PATH, rollup_out),
        (REPAIR_PROFILE_PATH, profile_out),
        (REPAIR_REPORT_PATH, report_out),
        (REPAIR_TRANSITION_TRACE_PATH, transition_trace_out),
    ]:
        write_json(path, obj)

    reason_codes = [
        "REVIEW_RECEIPT_CONSUMED",
        "REPAIR_TARGET_CONSUMED",
        "LOCAL_NEGATIVE_CONTROL_PARITY_SCOPE_CONFIRMED",
        "RUNTIME_ADOPTION_AUTHORITY_COUNT_ADDED_AT_ZERO",
        "ADAPTER_HARNESS_PATCHED_FOR_FUTURE_RECEIPTS",
        "NEGATIVE_CONTROL_PARITY_CLEAN",
        "PROPOSAL_CANDIDATE_ONLY_PRESERVED",
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

    receipt_out = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_receipt_v0",
        "receipt_type": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_REPAIR_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
        "source_adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "source_adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "REPAIR_0_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "REPAIR_1_REPAIR_TARGET_CONSUMED": gate == "PASS",
            "REPAIR_2_SCOPE_LOCAL_PARITY_ONLY": gate == "PASS",
            "REPAIR_3_MISSING_KEY_CONFIRMED": MISSING_KEY not in adapter_neg_before,
            "REPAIR_4_MISSING_KEY_ADDED_AT_ZERO": adapter_neg_after.get(MISSING_KEY) == 0,
            "REPAIR_5_ADAPTER_HARNESS_PATCHED": f'"{MISSING_KEY}": 0' in ADAPTER_SCRIPT_PATH.read_text(),
            "REPAIR_6_NEGATIVE_CONTROLS_ALL_ZERO": not nonzero_after,
            "REPAIR_7_PROPOSAL_CANDIDATE_ONLY_PRESERVED": adapter_receipt_after.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
            "REPAIR_8_NO_PROPOSAL_ACCEPTANCE": adapter_receipt_after.get("machine_readable_capability_proposal_adapter_summary", {}).get("proposal_accepted") is False,
            "REPAIR_9_NO_IMPLEMENTATION": adapter_receipt_after.get("implementation_authorized") is False,
            "REPAIR_10_NO_RUNTIME_ADOPTION_AUTHORITY": adapter_receipt_after.get("runtime_adoption_authorized") is False,
            "REPAIR_11_NO_SCHEMA_MUTATION": adapter_receipt_after.get("schema_mutation_authorized") is False,
            "REPAIR_12_NO_MOVE_ADDITION": adapter_receipt_after.get("move_addition_authorized") is False,
            "REPAIR_13_NO_C8_AUTHORIZATION": adapter_receipt_after.get("c8_authorized") is False,
            "REPAIR_14_PROTECTED_INPUTS_NOT_MUTATED": not protected_mutations,
            "REPAIR_15_NO_HIDDEN_NEXT_COMMAND": adapter_receipt_after.get("machine_readable_capability_proposal_adapter_summary", {}).get("hidden_next_command") is False,
        },
        "machine_readable_capability_proposal_adapter_negative_control_parity_repair_summary": {
            "status": status,
            "repair_scope": "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY",
            "adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
            "review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
            "added_negative_control_key": MISSING_KEY if gate == "PASS" else None,
            "added_negative_control_value": 0 if gate == "PASS" else None,
            "negative_control_parity_clean": gate == "PASS",
            "reference_freeze_ready": gate == "PASS",
            "proposal_status": adapter_receipt_after.get("proposal_status"),
            "proposal_id": adapter_receipt_after.get("proposal_id"),
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
            "before_after": rel(BEFORE_AFTER_PATH),
            "post_repair_review": rel(POST_REPAIR_REVIEW_PATH),
            "readout": rel(REPAIR_READOUT_PATH),
            "rollup": rel(REPAIR_ROLLUP_PATH),
            "profile": rel(REPAIR_PROFILE_PATH),
            "report": rel(REPAIR_REPORT_PATH),
            "transition_trace": rel(REPAIR_TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace_out["terminal"],
    }

    receipt_id = "capability_adapter_parity_repair_receipt_" + sig8(receipt_out)
    receipt_out["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_out["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_out)

    print(json.dumps(receipt_out, indent=2, sort_keys=True))
    print(f"capability_proposal_adapter_parity_repair_receipt_id={receipt_id}")
    print(f"capability_proposal_adapter_parity_repair_receipt_path={rel(receipt_path)}")
    print(f"capability_proposal_adapter_parity_repair_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
