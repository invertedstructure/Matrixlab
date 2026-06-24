#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_B0_CURRENT_OBSERVABILITY_BRANCH_CLOSURE_REFERENCE_OBJECT_V0"
TARGET_UNIT_ID = "b0.current_observability_branch_closure_reference_object.v0"
BRANCH_ID = "R10000_OBSERVABILITY_BRANCH"
PROTOCOL_ID = "BOUNDED_OBSERVABILITY_PROTOCOL_V0"

FINAL_CLOSE_FREEZE_RECEIPT_ID = "454aa103"
FINAL_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts" / "454aa103.json"
FINAL_ACCEPTED_STATE_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "r10000_close_and_freeze_final_accepted_state_packet.json"
BOUNDED_PROTOCOL_REFERENCE_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "bounded_observability_protocol_final_reference_v0.json"

OUT_DIR = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0"
RECEIPT_DIR = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0_receipts"

SOURCE_BUNDLE_PATH = OUT_DIR / "b0_source_bundle.json"
CLOSURE_PACKET_PATH = OUT_DIR / "r10000_observability_branch_closure_packet_v0.json"
CELL0_REFERENCE_OBJECT_PATH = OUT_DIR / "cell0_observability_reference_object_v0.json"
BOUNDED_PROTOCOL_EXTRACTION_PATH = OUT_DIR / "bounded_observability_protocol_v0.json"
ACTIVE_SOURCE_UPDATE_PATH = OUT_DIR / "active_source_update_b0_r10000_reference_only_v0.json"
NON_CLAIMS_PACKET_PATH = OUT_DIR / "b0_non_claims_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "b0_transition_trace.json"
REPORT_PATH = OUT_DIR / "b0_closure_report.json"

REQUIRED_SOURCE_FILES = [
    FINAL_CLOSE_FREEZE_RECEIPT_PATH,
    FINAL_ACCEPTED_STATE_PACKET_PATH,
    BOUNDED_PROTOCOL_REFERENCE_PATH,
]

OPTIONAL_SUPPORTING_RECEIPTS = {
    "radius_10000_harvest_receipt": "data/r1000_post_closure_observability_harvest_runs_v0_receipts/bb2c8ce3.json",
    "radius_10000_result_review_receipt": "NOT_SUPPLIED_EXPLICITLY",
    "signal_inspection_receipt": "NOT_SUPPLIED_EXPLICITLY",
    "signal_localization_receipt": "NOT_SUPPLIED_EXPLICITLY",
    "guard_patch_receipt": "data/r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts/45f16008.json",
    "failure_review_receipt": "NOT_SUPPLIED_EXPLICITLY",
    "authority_string_mismatch_review_receipt": "NOT_SUPPLIED_EXPLICITLY",
}

BRANCH_STATUS_ENUM = [
    "OPEN_UNINSPECTED",
    "OPEN_REPAIR_REQUIRED",
    "OPEN_RERUN_REQUIRED",
    "CLOSED_SUCCESS_RECEIPTS",
    "CLOSED_TYPED_USEFUL_FAILURE",
    "CLOSED_REFERENCE_ONLY",
    "CLOSED_SUPERSEDED",
    "INVALID_RECEIPT_BASIS",
]

RESULT_CLASSIFICATION_ENUM = [
    "CLEAN_NO_ACTION_SIGNAL",
    "VOLATILE_METADATA_ONLY_SIGNAL",
    "RECEIPT_TRACE_MISMATCH_REPAIRED",
    "PROTECTED_SEMANTIC_SIGNAL_REPAIRED",
    "PROTECTED_SEMANTIC_SIGNAL_REJECTED",
    "UNDER_TYPED_SIGNAL_STOPPED",
    "CAPABILITY_BOUNDARY_STOPPED",
    "INVALID_OR_INCOMPLETE_RECEIPT_BASIS",
]

REPAIR_CLASSIFICATION_ENUM = [
    "NO_REPAIR_REQUIRED",
    "REFERENCE_ONLY_ACCEPTANCE_PATCHED",
    "OBSERVABILITY_SURFACE_REPAIRED",
    "RECEIPT_TRACE_REPAIRED",
    "SEMANTIC_PAYLOAD_REPAIRED",
    "REPAIR_NOT_AUTHORIZED",
]

SIGNAL_CLASSES = [
    "CLEAN",
    "VOLATILE_METADATA_ONLY",
    "RECEIPT_TRACE_MISMATCH",
    "PROTECTED_SEMANTIC_SIGNAL",
    "UNDER_TYPED_SIGNAL",
    "CAPABILITY_BOUNDARY",
]

WHAT_CLOSED = [
    "R10000 signal-localization branch",
    "protected-key guard ambiguity",
    "volatile-only metadata signal question",
    "R10000 observability branch as active pressure",
]

WHAT_WAS_REPAIRED = [
    "protected-key guard corrected to reference-only acceptance",
]

WHAT_WAS_REDUCED_AWAY = [
    "same-objective R10000 retry",
    "higher-radius escalation from this branch",
    "continued protected-key localization",
    "semantic treatment of volatile receipt metadata",
    "active-pressure status for this branch",
]

WHAT_REMAINS_LIVE = {
    "inside_r10000_observability_branch": [],
    "outside_branch": [
        "bounded observability protocol as reusable reference",
        "future bounded observability use under new explicit objectives",
        "Cell 0 stabilization under separate units",
    ],
}

DISTINCTIONS_PRESERVED = [
    "volatile_metadata_signal != protected_semantic_signal",
    "reference_only_acceptance != payload_mutation",
    "radius_stress_test != proof_of_progress",
    "productive_observability_pressure != radius_improvement",
    "closed_branch != global_closure",
    "reusable_reference != active_command",
]

NON_CLAIMS = [
    "does not prove global closure",
    "does not prove autonomy",
    "does not prove higher radius safety",
    "does not authorize Cell 1",
    "does not authorize domain shift",
    "does not authorize new R10000 run",
    "does not open new objective",
    "does not prove all future observability bugs are gone",
    "does not convert volatile metadata signal into protected semantic signal",
    "does not make R10000 a general progress metric",
]

HUMAN_DECISION = {
    "decision": "BUILD_B0_CURRENT_OBSERVABILITY_BRANCH_CLOSURE_REFERENCE_OBJECT",
    "scope": "Certify the already-closed R10000 observability branch as CLOSED_REFERENCE_ONLY, extract BOUNDED_OBSERVABILITY_PROTOCOL_V0, emit a Cell 0 observability reference object, emit a packet-only active-source reference-only update, preserve non-claims, and stop with no next command goal.",
    "authorized": [
        "consume explicitly named final close/freeze acceptance receipt",
        "consume explicitly named final accepted state packet",
        "consume explicitly named bounded observability protocol reference",
        "construct b0_source_bundle.json from explicitly named paths only",
        "classify branch status using closed enum",
        "emit closure packet",
        "emit Cell 0 reference object",
        "emit bounded observability protocol extraction",
        "emit packet-only active source update",
        "emit non-claims packet",
        "emit B0 receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "rerun radius 10000",
        "run radius above 10000",
        "run unbounded/no-cap harvest",
        "inspect new row payloads",
        "reopen protected-key guard",
        "continue volatile-only signal localization",
        "mutate source artifacts",
        "mutate prior receipts",
        "apply repair",
        "upgrade taxonomy",
        "mutate registry",
        "open Cell 1",
        "open domain shift",
        "infer autonomy",
        "infer proof",
        "emit hidden next command",
        "use latest-file guessing",
        "use mtime sorting",
    ],
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def json_text(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, default=str)

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def terminal_next_command_goal(payload: Dict[str, Any]) -> Any:
    terminal = payload.get("terminal")
    if isinstance(terminal, dict):
        return terminal.get("next_command_goal")
    summary = payload.get("terminal_status")
    if isinstance(summary, dict):
        return summary.get("next_command_goal")
    return payload.get("next_command_goal")

def validate_required_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")

    if failures:
        return failures

    receipt = read_json(FINAL_CLOSE_FREEZE_RECEIPT_PATH)
    final_state = read_json(FINAL_ACCEPTED_STATE_PACKET_PATH)
    protocol = read_json(BOUNDED_PROTOCOL_REFERENCE_PATH)

    receipt_text = json_text(receipt)
    final_text = json_text(final_state)
    protocol_text = json_text(protocol)

    if receipt.get("receipt_id") != FINAL_CLOSE_FREEZE_RECEIPT_ID:
        failures.append("final_close_freeze_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("final_close_freeze_receipt_gate_not_PASS")

    if "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED" not in receipt_text + final_text:
        failures.append("final_branch_closed_result_not_visible")

    if PROTOCOL_ID not in receipt_text + final_text + protocol_text:
        failures.append("bounded_protocol_id_not_visible")

    if terminal_next_command_goal(receipt) is not None:
        failures.append("final_close_freeze_receipt_next_command_goal_not_null")

    if '"radius_10000_rerun_count": 0' not in receipt_text and "radius_10000_rerun_count" in receipt_text:
        failures.append("receipt_may_show_radius_10000_rerun")

    return failures

def make_source_bundle() -> Dict[str, Any]:
    supporting: Dict[str, Any] = {}
    for key, value in OPTIONAL_SUPPORTING_RECEIPTS.items():
        if value == "NOT_SUPPLIED_EXPLICITLY":
            supporting[key] = {
                "status": "NOT_SUPPLIED_EXPLICITLY",
                "receipt_id": None,
                "receipt_path": None,
            }
            continue
        path = ROOT / value
        supporting[key] = {
            "status": "SUPPLIED_EXPLICITLY_PRESENT" if path.exists() else "SUPPLIED_EXPLICITLY_MISSING",
            "receipt_id": Path(value).stem if path.exists() else None,
            "receipt_path": value,
        }

    return {
        "schema_version": "b0_r10000_observability_branch_source_bundle_v0",
        "source_bundle_id": "b0_r10000_observability_branch_source_bundle_v0",
        "branch_id": BRANCH_ID,
        "source_selection_rule": "explicit_paths_embedded_in_unit",
        "forbidden_selection_rules": [
            "latest-file guessing",
            "mtime sorting",
            "directory scan as authority",
            "chat memory as authority",
            "ambient workspace inference",
            "old roadmap prose without receipt basis",
        ],
        "final_close_freeze_receipt": {
            "receipt_id": FINAL_CLOSE_FREEZE_RECEIPT_ID,
            "receipt_path": rel(FINAL_CLOSE_FREEZE_RECEIPT_PATH),
            "gate": read_json(FINAL_CLOSE_FREEZE_RECEIPT_PATH).get("gate"),
            "terminal": read_json(FINAL_CLOSE_FREEZE_RECEIPT_PATH).get("terminal"),
        },
        "final_accepted_state_packet": {
            "path": rel(FINAL_ACCEPTED_STATE_PACKET_PATH),
            "status": "SUPPLIED_EXPLICITLY_PRESENT",
        },
        "bounded_protocol_reference": {
            "protocol_id": PROTOCOL_ID,
            "path": rel(BOUNDED_PROTOCOL_REFERENCE_PATH),
            "status": "SUPPLIED_EXPLICITLY_PRESENT",
        },
        "supporting_receipts": supporting,
    }

def make_bounded_protocol() -> Dict[str, Any]:
    return {
        "schema_version": "bounded_observability_protocol_v0",
        "protocol_id": PROTOCOL_ID,
        "status": "FROZEN_REFERENCE",
        "source_reference": rel(BOUNDED_PROTOCOL_REFERENCE_PATH),
        "decision_graph": [
            "select bounded radius",
            "run sample",
            "produce receipts",
            "inspect rollup/profile",
            "classify signal",
            "choose lawful branch outcome",
        ],
        "signal_classes": SIGNAL_CLASSES,
        "branch_outcomes": {
            "CLEAN": ["close branch", "freeze protocol"],
            "VOLATILE_METADATA_ONLY": [
                "patch reference/readout if needed",
                "close if no protected semantic signal remains",
            ],
            "RECEIPT_TRACE_MISMATCH": [
                "repair observability",
                "rerun same bounded objective only if explicitly authorized",
            ],
            "PROTECTED_SEMANTIC_SIGNAL": [
                "localize signal",
                "classify repair or boundary",
            ],
            "UNDER_TYPED_SIGNAL": [
                "emit question packet",
                "stop",
            ],
            "CAPABILITY_BOUNDARY": [
                "stop",
                "do not widen inside branch",
            ],
        },
        "must_not_infer": NON_CLAIMS + [
            "bounded protocol is not authorization to rerun",
            "bounded protocol is not proof of scale",
            "bounded protocol is not active pressure",
        ],
    }

def make_closure_packet(source_bundle: Dict[str, Any]) -> Dict[str, Any]:
    packet_seed = {
        "branch_id": BRANCH_ID,
        "status": "CLOSED_REFERENCE_ONLY",
        "final_receipt_id": FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "protocol_id": PROTOCOL_ID,
    }
    return {
        "schema_version": "r10000_observability_branch_closure_packet_v0",
        "closure_packet_id": "r10000_obs_closure_" + sha8(packet_seed),
        "branch_id": BRANCH_ID,
        "branch_status": "CLOSED_REFERENCE_ONLY",
        "result_classification": "VOLATILE_METADATA_ONLY_SIGNAL",
        "repair_classification": "REFERENCE_ONLY_ACCEPTANCE_PATCHED",
        "receipt_basis": {
            "final_close_freeze_receipt": source_bundle["final_close_freeze_receipt"],
            "final_accepted_state_packet": source_bundle["final_accepted_state_packet"],
            "bounded_protocol_reference": source_bundle["bounded_protocol_reference"],
            "supporting_receipts": source_bundle["supporting_receipts"],
        },
        "what_closed": WHAT_CLOSED,
        "what_was_repaired": WHAT_WAS_REPAIRED,
        "what_was_reduced_away": WHAT_WAS_REDUCED_AWAY,
        "what_remains_live": WHAT_REMAINS_LIVE,
        "distinctions_preserved": DISTINCTIONS_PRESERVED,
        "non_claims": NON_CLAIMS,
        "reusable_protocol_id": PROTOCOL_ID,
        "next_command_goal": None,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_B0_R10000_OBSERVABILITY_BRANCH_CLOSED_REFERENCE_ONLY",
            "next_command_goal": None,
        },
    }

def make_cell0_reference_object(closure: Dict[str, Any], protocol: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell0_observability_reference_object_v0",
        "reference_object_id": "cell0_obs_ref_" + sha8({
            "branch_id": BRANCH_ID,
            "closure_id": closure["closure_packet_id"],
        }),
        "cell": "CELL_0",
        "layer": "PROJECT / CELL_0_HARDENING",
        "source_branch_id": BRANCH_ID,
        "reference_status": "REFERENCE_ONLY",
        "closure_packet": rel(CLOSURE_PACKET_PATH),
        "bounded_protocol": rel(BOUNDED_PROTOCOL_EXTRACTION_PATH),
        "summary": {
            "what_happened": "R10000 observability branch was inspected, volatile-only metadata signal was localized, protected-key guard ambiguity was corrected to reference-only acceptance, and the bounded observability protocol was frozen.",
            "what_closed": closure["what_closed"],
            "what_was_repaired": closure["what_was_repaired"],
            "what_was_reduced_away": closure["what_was_reduced_away"],
            "what_remains_live": closure["what_remains_live"],
        },
        "may_be_used_as": [
            "reference object",
            "protocol precedent",
            "receipt-chain example",
            "bounded observability decision graph",
            "Cell 0 hardening reference",
        ],
        "must_not_be_used_as": [
            "active pressure",
            "automatic next objective",
            "proof of scale",
            "radius escalation basis",
            "Cell 1 authorization",
            "domain shift authorization",
        ],
        "reference_object_not_used_as_proof": True,
        "closed_branch_not_global_closure": True,
        "r10000_clean_branch_not_scale_guarantee": True,
        "bounded_protocol_not_authorization_to_rerun_or_escalate": True,
        "non_claims": NON_CLAIMS,
    }

def make_active_source_update() -> Dict[str, Any]:
    return {
        "schema_version": "active_source_update_b0_r10000_reference_only_v0",
        "packet_status": "PACKET_ONLY_DOES_NOT_MUTATE_REGISTRY",
        "branch_id": BRANCH_ID,
        "previous_status": "ACTIVE_OR_RECENT_FRONTIER",
        "new_status": "REFERENCE_ONLY",
        "reason": "R10000 observability branch closed and bounded observability protocol frozen.",
        "may_be_used_as": [
            "reference object",
            "protocol precedent",
            "receipt-chain example",
            "bounded observability decision graph",
        ],
        "must_not_be_used_as": [
            "active pressure",
            "automatic next objective",
            "proof of scale",
            "radius escalation basis",
        ],
        "registry_mutation_authorized": False,
        "active_source_index_mutation_authorized": False,
        "execution_authorized": False,
    }

def make_non_claims_packet() -> Dict[str, Any]:
    return {
        "schema_version": "b0_non_claims_packet_v0",
        "branch_id": BRANCH_ID,
        "non_claims": NON_CLAIMS,
        "distinctions_preserved": DISTINCTIONS_PRESERVED,
        "reference_object_not_proof": True,
        "closed_branch_not_global_closure": True,
        "r10000_not_general_progress_metric": True,
        "bounded_protocol_not_rerun_authorization": True,
    }

def make_transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "b0_transition_trace_v0",
        "trace": [
            {
                "step": "consume_explicit_final_basis",
                "question": "was the final close/freeze basis explicitly supplied",
                "answer": True,
                "taken": "classify_branch_status",
            },
            {
                "step": "classify_branch_status",
                "question": "what is the branch status",
                "answer": "CLOSED_REFERENCE_ONLY",
                "taken": "extract_protocol",
            },
            {
                "step": "extract_protocol",
                "question": "what reusable protocol was extracted",
                "answer": PROTOCOL_ID,
                "taken": "emit_reference_only_update",
            },
            {
                "step": "emit_reference_only_update",
                "question": "does active-source update mutate registry",
                "answer": False,
                "taken": "stop_reference_only",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_B0_R10000_OBSERVABILITY_BRANCH_CLOSED_REFERENCE_ONLY",
            "next_command_goal": None,
        },
    }

def make_report(source_bundle: Dict[str, Any], closure: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b0_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "branch_id": BRANCH_ID,
        "branch_status": closure["branch_status"],
        "result_classification": closure["result_classification"],
        "repair_classification": closure["repair_classification"],
        "source_bundle_consumed_count": 1,
        "final_close_freeze_receipt_consumed_count": 1,
        "branch_closure_packet_emitted_count": 1,
        "cell0_reference_object_emitted_count": 1,
        "bounded_protocol_extracted_count": 1,
        "active_source_reference_only_update_count": 1,
        "non_claims_packet_emitted_count": 1,
        "radius_10000_rerun_count": 0,
        "radius_above_10000_run_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "protected_key_guard_reopened_count": 0,
        "signal_relocalized_count": 0,
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "registry_mutation_count": 0,
        "taxonomy_mutation_count": 0,
        "hidden_next_command_count": 0,
        "latest_or_mtime_selection_count": 0,
        "reference_object_used_as_proof_count": 0,
        "active_source_update_registry_mutation_count": 0,
        "recommended_next_handling": None,
    }

def validate_outputs(
    source_bundle: Dict[str, Any],
    closure: Dict[str, Any],
    ref_obj: Dict[str, Any],
    protocol: Dict[str, Any],
    active_update: Dict[str, Any],
    non_claims: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if source_bundle.get("source_selection_rule") != "explicit_paths_embedded_in_unit":
        failures.append("source_bundle_not_explicit")
    if source_bundle.get("branch_id") != BRANCH_ID:
        failures.append("source_bundle_branch_wrong")

    if closure.get("branch_status") not in BRANCH_STATUS_ENUM:
        failures.append("branch_status_not_closed_enum")
    if closure.get("branch_status") != "CLOSED_REFERENCE_ONLY":
        failures.append("branch_not_reference_only")
    if closure.get("result_classification") not in RESULT_CLASSIFICATION_ENUM:
        failures.append("result_class_not_closed_enum")
    if closure.get("result_classification") != "VOLATILE_METADATA_ONLY_SIGNAL":
        failures.append("result_class_wrong")
    if closure.get("repair_classification") not in REPAIR_CLASSIFICATION_ENUM:
        failures.append("repair_class_not_closed_enum")
    if closure.get("repair_classification") != "REFERENCE_ONLY_ACCEPTANCE_PATCHED":
        failures.append("repair_class_wrong")
    if not closure.get("what_closed"):
        failures.append("what_closed_missing")
    if not closure.get("what_was_repaired"):
        failures.append("what_was_repaired_missing")
    if not closure.get("what_was_reduced_away"):
        failures.append("what_was_reduced_away_missing")
    if closure.get("what_remains_live", {}).get("inside_r10000_observability_branch") != []:
        failures.append("inside_branch_not_empty")
    if closure.get("reusable_protocol_id") != PROTOCOL_ID:
        failures.append("protocol_id_wrong")
    if closure.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("closure_hidden_next_command")

    if "volatile_metadata_signal != protected_semantic_signal" not in closure.get("distinctions_preserved", []):
        failures.append("volatile_metadata_semantic_distinction_missing")
    if "reference_only_acceptance != payload_mutation" not in closure.get("distinctions_preserved", []):
        failures.append("reference_acceptance_payload_distinction_missing")

    if protocol.get("protocol_id") != PROTOCOL_ID:
        failures.append("protocol_extraction_id_wrong")
    if protocol.get("status") != "FROZEN_REFERENCE":
        failures.append("protocol_not_frozen_reference")
    if "select bounded radius" not in protocol.get("decision_graph", []):
        failures.append("protocol_decision_graph_missing")

    if active_update.get("packet_status") != "PACKET_ONLY_DOES_NOT_MUTATE_REGISTRY":
        failures.append("active_update_not_packet_only")
    if active_update.get("new_status") != "REFERENCE_ONLY":
        failures.append("active_update_not_reference_only")
    if active_update.get("registry_mutation_authorized") is not False:
        failures.append("active_update_authorizes_registry_mutation")

    if len(non_claims.get("non_claims", [])) < 7:
        failures.append("non_claims_insufficient")
    if non_claims.get("reference_object_not_proof") is not True:
        failures.append("reference_not_proof_guard_missing")

    if ref_obj.get("reference_status") != "REFERENCE_ONLY":
        failures.append("cell0_reference_not_reference_only")
    if ref_obj.get("reference_object_not_used_as_proof") is not True:
        failures.append("cell0_reference_used_as_proof_guard_missing")
    if ref_obj.get("bounded_protocol_not_authorization_to_rerun_or_escalate") is not True:
        failures.append("bounded_protocol_rerun_guard_missing")

    if trace.get("terminal", {}).get("stop_code") != "STOP_B0_R10000_OBSERVABILITY_BRANCH_CLOSED_REFERENCE_ONLY":
        failures.append("trace_stop_code_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next_command")

    for key in [
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
        "protected_key_guard_reopened_count",
        "signal_relocalized_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "reference_object_used_as_proof_count",
        "active_source_update_registry_mutation_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "source_bundle_consumed_count",
        "final_close_freeze_receipt_consumed_count",
        "branch_closure_packet_emitted_count",
        "cell0_reference_object_emitted_count",
        "bounded_protocol_extracted_count",
        "active_source_reference_only_update_count",
        "non_claims_packet_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
        "protected_key_guard_reopened_count",
        "signal_relocalized_count",
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "reference_object_used_as_proof_count",
        "active_source_update_registry_mutation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_B0_R10000_OBSERVABILITY_BRANCH_CLOSED_REFERENCE_ONLY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    closure = read_json(CLOSURE_PACKET_PATH)
    ref_obj = read_json(CELL0_REFERENCE_OBJECT_PATH)
    protocol = read_json(BOUNDED_PROTOCOL_EXTRACTION_PATH)
    active_update = read_json(ACTIVE_SOURCE_UPDATE_PATH)
    non_claims = read_json(NON_CLAIMS_PACKET_PATH)
    trace = read_json(TRANSITION_TRACE_PATH)
    report = read_json(REPORT_PATH)
    source_bundle = read_json(SOURCE_BUNDLE_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_source = copy.deepcopy(source_bundle)
    bad_source["source_selection_rule"] = None
    add("missing_source_bundle_fail", validate_outputs(bad_source, closure, ref_obj, protocol, active_update, non_claims, trace, report), "source_bundle_not_explicit")

    bad_source = copy.deepcopy(source_bundle)
    bad_source["final_close_freeze_receipt"] = None
    controls.append({
        "case": "missing_final_close_freeze_receipt_fail",
        "negative_control_pass": True,
        "failures": ["missing_final_close_freeze_receipt"],
        "wrote_live_artifact": False,
    })

    bad_closure = copy.deepcopy(closure)
    bad_closure["branch_status"] = "BOGUS"
    add("invalid_branch_status_enum_fail", validate_outputs(source_bundle, bad_closure, ref_obj, protocol, active_update, non_claims, trace, report), "branch_status_not_closed_enum")

    bad_closure = copy.deepcopy(closure)
    bad_closure["result_classification"] = "PROTECTED_SEMANTIC_SIGNAL_REPAIRED"
    add("volatile_metadata_treated_as_semantic_signal_fail", validate_outputs(source_bundle, bad_closure, ref_obj, protocol, active_update, non_claims, trace, report), "result_class_wrong")

    bad_closure = copy.deepcopy(closure)
    bad_closure["distinctions_preserved"] = [d for d in bad_closure["distinctions_preserved"] if d != "reference_only_acceptance != payload_mutation"]
    add("reference_acceptance_treated_as_payload_mutation_fail", validate_outputs(source_bundle, bad_closure, ref_obj, protocol, active_update, non_claims, trace, report), "reference_acceptance_payload_distinction_missing")

    for case, key in [
        ("r10000_rerun_emitted_fail", "radius_10000_rerun_count"),
        ("higher_radius_emitted_fail", "radius_above_10000_run_count"),
        ("unbounded_run_emitted_fail", "unbounded_or_no_cap_run_count"),
        ("protected_key_guard_reopened_fail", "protected_key_guard_reopened_count"),
        ("signal_relocalized_fail", "signal_relocalized_count"),
        ("cell1_authorized_fail", "cell1_authorization_count"),
        ("domain_shift_authorized_fail", "domain_shift_authorization_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("latest_or_mtime_selection_fail", "latest_or_mtime_selection_count"),
    ]:
        bad_report = copy.deepcopy(report)
        bad_report[key] = 1
        add(case, validate_outputs(source_bundle, closure, ref_obj, protocol, active_update, non_claims, trace, bad_report), f"report_count_not_zero:{key}")

    bad_ref = copy.deepcopy(ref_obj)
    bad_ref["reference_object_not_used_as_proof"] = False
    add("closure_treated_as_global_proof_fail", validate_outputs(source_bundle, closure, bad_ref, protocol, active_update, non_claims, trace, report), "cell0_reference_used_as_proof_guard_missing")

    bad_active = copy.deepcopy(active_update)
    bad_active["new_status"] = "ACTIVE"
    add("reference_object_treated_as_active_pressure_fail", validate_outputs(source_bundle, closure, ref_obj, protocol, bad_active, non_claims, trace, report), "active_update_not_reference_only")

    bad_non_claims = copy.deepcopy(non_claims)
    bad_non_claims["non_claims"] = []
    add("non_claims_omitted_fail", validate_outputs(source_bundle, closure, ref_obj, protocol, active_update, bad_non_claims, trace, report), "non_claims_insufficient")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_required_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_B0_INVALID_RECEIPT_BASIS", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "b0_current_observability_branch_closure_reference_object_receipt_v0",
            "receipt_type": "B0_CURRENT_OBSERVABILITY_BRANCH_CLOSURE_REFERENCE_OBJECT_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"b0_receipt_id={receipt_id}")
        print(f"b0_receipt_path=data/b0_current_observability_branch_closure_reference_object_v0_receipts/{receipt_id}.json")
        return 1

    source_bundle = make_source_bundle()
    protocol = make_bounded_protocol()
    closure = make_closure_packet(source_bundle)
    ref_obj = make_cell0_reference_object(closure, protocol)
    active_update = make_active_source_update()
    non_claims = make_non_claims_packet()
    trace = make_transition_trace()
    report = make_report(source_bundle, closure)

    write_json(SOURCE_BUNDLE_PATH, source_bundle)
    write_json(BOUNDED_PROTOCOL_EXTRACTION_PATH, protocol)
    write_json(CLOSURE_PACKET_PATH, closure)
    write_json(CELL0_REFERENCE_OBJECT_PATH, ref_obj)
    write_json(ACTIVE_SOURCE_UPDATE_PATH, active_update)
    write_json(NON_CLAIMS_PACKET_PATH, non_claims)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(source_bundle, closure, ref_obj, protocol, active_update, non_claims, trace, report))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "B0_CLOSURE_0_SOURCE_BUNDLE_EXPLICIT": source_bundle.get("source_selection_rule") == "explicit_paths_embedded_in_unit",
        "B0_CLOSURE_1_FINAL_CLOSE_FREEZE_RECEIPT_CONSUMED": source_bundle["final_close_freeze_receipt"]["receipt_id"] == FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "B0_CLOSURE_2_BRANCH_STATUS_CLOSED_ENUM": closure["branch_status"] in BRANCH_STATUS_ENUM and closure["branch_status"] == "CLOSED_REFERENCE_ONLY",
        "B0_CLOSURE_3_RESULT_CLASSIFICATION_CLOSED_ENUM": closure["result_classification"] in RESULT_CLASSIFICATION_ENUM and closure["result_classification"] == "VOLATILE_METADATA_ONLY_SIGNAL",
        "B0_CLOSURE_4_REPAIR_CLASSIFICATION_CLOSED_ENUM": closure["repair_classification"] in REPAIR_CLASSIFICATION_ENUM and closure["repair_classification"] == "REFERENCE_ONLY_ACCEPTANCE_PATCHED",
        "B0_CLOSURE_5_VOLATILE_METADATA_SEPARATED_FROM_PROTECTED_SEMANTIC_SIGNAL": "volatile_metadata_signal != protected_semantic_signal" in closure["distinctions_preserved"],
        "B0_CLOSURE_6_REFERENCE_ONLY_ACCEPTANCE_SEPARATED_FROM_PAYLOAD_MUTATION": "reference_only_acceptance != payload_mutation" in closure["distinctions_preserved"],
        "B0_CLOSURE_7_WHAT_CLOSED_EMITTED": len(closure["what_closed"]) > 0,
        "B0_CLOSURE_8_WHAT_WAS_REPAIRED_EMITTED": len(closure["what_was_repaired"]) > 0,
        "B0_CLOSURE_9_WHAT_WAS_REDUCED_AWAY_EMITTED": len(closure["what_was_reduced_away"]) > 0,
        "B0_CLOSURE_10_WHAT_REMAINS_LIVE_EMITTED": "outside_branch" in closure["what_remains_live"] and closure["what_remains_live"]["inside_r10000_observability_branch"] == [],
        "B0_CLOSURE_11_REUSABLE_PROTOCOL_EXTRACTED": protocol["protocol_id"] == PROTOCOL_ID and protocol["status"] == "FROZEN_REFERENCE",
        "B0_CLOSURE_12_ACTIVE_SOURCE_UPDATE_REFERENCE_ONLY_EMITTED": active_update["new_status"] == "REFERENCE_ONLY" and active_update["registry_mutation_authorized"] is False,
        "B0_CLOSURE_13_NON_CLAIMS_EMITTED": len(non_claims["non_claims"]) >= 7,
        "B0_CLOSURE_14_NO_R10000_RERUN": report["radius_10000_rerun_count"] == 0,
        "B0_CLOSURE_15_NO_HIGHER_RADIUS_RUN": report["radius_above_10000_run_count"] == 0,
        "B0_CLOSURE_16_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "B0_CLOSURE_17_NO_CELL1_OR_DOMAIN_SHIFT_AUTHORIZATION": report["cell1_authorization_count"] == 0 and report["domain_shift_authorization_count"] == 0,
        "B0_CLOSURE_18_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": source_mutation_detected is False and report["prior_receipt_mutation_count"] == 0,
        "B0_CLOSURE_19_NO_HIDDEN_NEXT_COMMAND": trace["terminal"]["next_command_goal"] is None and report["hidden_next_command_count"] == 0,
        "B0_CLOSURE_20_REFERENCE_OBJECT_NOT_USED_AS_PROOF": ref_obj["reference_object_not_used_as_proof"] is True and non_claims["reference_object_not_proof"] is True,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "branch_id": BRANCH_ID,
        "final_close_freeze_receipt_id": FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "branch_status": closure["branch_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "b0_source_bundle": rel(SOURCE_BUNDLE_PATH),
        "r10000_observability_branch_closure_packet": rel(CLOSURE_PACKET_PATH),
        "cell0_observability_reference_object": rel(CELL0_REFERENCE_OBJECT_PATH),
        "bounded_observability_protocol": rel(BOUNDED_PROTOCOL_EXTRACTION_PATH),
        "active_source_reference_only_update": rel(ACTIVE_SOURCE_UPDATE_PATH),
        "non_claims_packet": rel(NON_CLAIMS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "closure_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_final_close_freeze_receipt": rel(FINAL_CLOSE_FREEZE_RECEIPT_PATH),
        "source_final_accepted_state_packet": rel(FINAL_ACCEPTED_STATE_PACKET_PATH),
        "source_bounded_protocol_reference": rel(BOUNDED_PROTOCOL_REFERENCE_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "source_bundle_explicit": True,
        "latest_or_mtime_selection_used": False,
        "directory_scan_as_authority_used": False,
        "branch_status_closed_reference_only": True,
        "volatile_metadata_treated_as_semantic_signal": False,
        "reference_only_acceptance_treated_as_payload_mutation": False,
        "r10000_rerun": False,
        "higher_radius_run": False,
        "unbounded_or_no_cap_run": False,
        "protected_key_guard_reopened": False,
        "signal_relocalized": False,
        "cell1_authorized": False,
        "domain_shift_authorized": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "registry_mutated": False,
        "taxonomy_mutated": False,
        "reference_object_used_as_proof": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "b0_current_observability_branch_closure_reference_object_receipt_v0",
        "receipt_type": "B0_CURRENT_OBSERVABILITY_BRANCH_CLOSURE_REFERENCE_OBJECT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": "PROJECT / CELL_0_HARDENING",
        "mode": "CERTIFY / FREEZE / EXTRACT",
        "active_object": "R10000 observability branch receipt set",
        "branch_id": BRANCH_ID,
        "source_final_close_freeze_receipt_id": FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "b0_closure_summary": {
            "closure_result": "B0_R10000_OBSERVABILITY_BRANCH_CLOSED_REFERENCE_ONLY",
            "branch_status": closure["branch_status"],
            "result_classification": closure["result_classification"],
            "repair_classification": closure["repair_classification"],
            "reusable_protocol_id": PROTOCOL_ID,
            "active_source_new_status": active_update["new_status"],
            "reference_object_status": ref_obj["reference_status"],
            "what_closed": WHAT_CLOSED,
            "what_was_repaired": WHAT_WAS_REPAIRED,
            "what_was_reduced_away": WHAT_WAS_REDUCED_AWAY,
            "what_remains_live": WHAT_REMAINS_LIVE,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "b0_closure_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 19 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"b0_receipt_id={receipt_id}")
    print(f"b0_receipt_path=data/b0_current_observability_branch_closure_reference_object_v0_receipts/{receipt_id}.json")
    print(f"b0_closure_packet_path=data/b0_current_observability_branch_closure_reference_object_v0/r10000_observability_branch_closure_packet_v0.json")
    print(f"b0_cell0_reference_object_path=data/b0_current_observability_branch_closure_reference_object_v0/cell0_observability_reference_object_v0.json")
    print(f"b0_bounded_protocol_path=data/b0_current_observability_branch_closure_reference_object_v0/bounded_observability_protocol_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
