#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_reuse_authority_probe.closure_packet.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_CREATED"
OUTCOME = "C8_SUCCESSOR_SURFACE_REUSE_AUTHORITY_PROBE_CLOSURE_READY_FOR_HUMAN_DECISION"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_READY_FOR_REVIEW"

PROBE_ID = "c8_successor_surface_reuse_authority_boundary_probe_v0"
PROBE_KIND = "REUSE_AUTHORITY_BOUNDARY_PROBE"
SELECTED_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
SELECTED_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
SELECTED_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0_receipts"

PROBE_RECEIPT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0_receipts/c8_successor_reuse_authority_probe_receipt_803165de.json"
PROBE_EVIDENCE = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0/c8_successor_surface_bounded_reuse_authority_probe_evidence_v0.json"
PROBE_RESULT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0/c8_successor_surface_bounded_reuse_authority_probe_result_v0.json"
PROBE_BOUNDARY_AUDIT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0/c8_successor_surface_bounded_reuse_authority_probe_boundary_audit_v0.json"
PROBE_REPORT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0/c8_successor_surface_bounded_reuse_authority_probe_report.json"

CLOSURE_PACKET = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_closure_packet_v0.json"
CLOSURE_DECISION_OPTIONS = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_closure_decision_options_v0.json"
CLOSURE_AUDIT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_closure_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_closure_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_closure_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "additional_probe_authorized_count",
    "instrument_build_count",
    "cell1_build_count",
    "verification_probe_count",
    "c8_rerun_count",
    "missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "reusable_schema_authorized_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
    "hidden_next_command_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    sources = {
        "probe_receipt": PROBE_RECEIPT,
        "probe_evidence": PROBE_EVIDENCE,
        "probe_result": PROBE_RESULT,
        "probe_boundary_audit": PROBE_BOUNDARY_AUDIT,
        "probe_report": PROBE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    probe_receipt = read_json(PROBE_RECEIPT)
    probe_evidence = read_json(PROBE_EVIDENCE)
    probe_result = read_json(PROBE_RESULT)
    probe_audit = read_json(PROBE_BOUNDARY_AUDIT)
    probe_report = read_json(PROBE_REPORT)
    summary = probe_receipt.get("machine_readable_probe_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_PASS",
        "outcome_class": "C8_SUCCESSOR_SURFACE_REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
        "receipt_id": "c8_successor_reuse_authority_probe_receipt_803165de",
    }

    for key, want in expected_receipt.items():
        chk(failures, f"probe_receipt_{key}", probe_receipt.get(key), want)

    expected_summary = {
        "probe_complete": True,
        "source_acceptance_receipt_id": "c8_successor_probe_execution_acceptance_receipt_31139bd1",
        "source_acceptance_packet_id": "c8_successor_probe_execution_acceptance_packet_2ffc6f0d",
        "source_acceptance_decision_id": "c8_successor_probe_execution_acceptance_decision_64e3fccf",
        "source_authority_id": "c8_successor_probe_execution_authority_52f56baf",
        "source_prep_packet_id": "c8_successor_probe_prep_packet_74a6c209",
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_execution_count": 1,
        "allowed_probe_execution_count": 1,
        "probe_output_class": "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
        "reuse_boundary_held": True,
        "new_authority_needed_now": False,
        "missing_reuse_authority_rule_exposed": False,
        "surface_too_broad_requires_narrowing": False,
        "source_context_missing_typed_stop": False,
        "local_discriminator_reusable_schema_authorized": False,
        "local_loop_pattern_reusable_schema_authorized": False,
        "later_promotion_authority_present": False,
        "probe_requires_review": True,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_RESULT_V0",
        "instrument_built_now": False,
        "cell1_built_now": False,
        "verification_probe_run_now": False,
        "c8_rerun_now": False,
        "missing_instrument_proposal_created_now": False,
        "research_mode_opened": False,
        "general_cell1_authority": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
    }

    for key, want in expected_summary.items():
        chk(failures, f"probe_summary_{key}", summary.get(key), want)

    chk(failures, "probe_result_id", probe_result.get("probe_result_id"), "c8_successor_reuse_authority_probe_result_3260762c")
    chk(failures, "probe_evidence_id", probe_evidence.get("probe_evidence_id"), "c8_successor_reuse_authority_probe_evidence_4f51ca49")
    chk(failures, "probe_boundary_audit_id", probe_audit.get("boundary_audit_id"), "c8_successor_reuse_authority_probe_boundary_72e5fd07")

    evidence_items = probe_evidence.get("evidence_items", [])
    if len(evidence_items) != 7:
        failures.append(f"evidence_items_count_wrong:{len(evidence_items)}!=7")
    if probe_evidence.get("failed_evidence") != []:
        failures.append(f"failed_evidence_not_empty:{probe_evidence.get('failed_evidence')}")

    false_evidence = [e.get("evidence_id") for e in evidence_items if e.get("value") is not True]
    if false_evidence:
        failures.append(f"false_evidence_items:{false_evidence}")

    probe_gates_false = sorted(k for k, v in probe_receipt.get("probe_gate_results", {}).items() if v is not True)
    if probe_gates_false:
        failures.append(f"probe_gates_false:{probe_gates_false}")

    receipt_forbidden = probe_receipt.get("forbidden_counters", {})
    forbidden_nonzero = {k: v for k, v in receipt_forbidden.items() if v != 0}
    if forbidden_nonzero:
        failures.append(f"probe_forbidden_counters_nonzero:{forbidden_nonzero}")

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    closure_class = (
        "BOUNDED_PROBE_RESULT_REVIEWED_REUSE_BOUNDARY_HELD"
        if not failures else
        "BOUNDED_PROBE_CLOSURE_PACKET_FAILED"
    )

    closure_packet = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_packet_v0",
        "closure_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "closure_status": "CLOSURE_PACKET_CREATED_FOR_REVIEW",
        "closure_class": closure_class,
        "source_probe_receipt_id": probe_receipt.get("receipt_id"),
        "source_probe_evidence_id": probe_evidence.get("probe_evidence_id"),
        "source_probe_result_id": probe_result.get("probe_result_id"),
        "source_probe_boundary_audit_id": probe_audit.get("boundary_audit_id"),
        "source_acceptance_receipt_id": summary.get("source_acceptance_receipt_id"),
        "source_authority_id": summary.get("source_authority_id"),
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_execution_count": summary.get("probe_execution_count"),
        "allowed_probe_execution_count": summary.get("allowed_probe_execution_count"),
        "probe_output_class": summary.get("probe_output_class"),
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "closure_recommendation": "CLOSE_SUCCESSOR_SURFACE_NO_NEW_AUTHORITY",
        "closure_recommendation_reason": "The bounded probe held the reuse boundary, all evidence items passed, and no missing authority rule or reusable schema authorization was exposed.",
        "human_decision_required": True,
        "closure_accepted_now": False,
        "additional_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    closure_packet["closure_packet_id"] = "c8_successor_reuse_authority_probe_closure_packet_" + sig8(closure_packet)
    write_json(CLOSURE_PACKET, closure_packet)

    decision_options = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_decision_options_v0",
        "closure_decision_options_id": None,
        "source_closure_packet_id": closure_packet["closure_packet_id"],
        "recommended_human_decision": "ACCEPT_CLOSURE_NO_NEW_AUTHORITY",
        "possible_human_decisions": [
            "ACCEPT_CLOSURE_NO_NEW_AUTHORITY",
            "REJECT_CLOSURE_PACKET",
            "REQUEST_NARROWER_CLOSURE_REVIEW",
        ],
        "decision_boundary": {
            "accept_closure_authorizes_new_probe": False,
            "accept_closure_authorizes_build": False,
            "accept_closure_authorizes_rerun": False,
            "accept_closure_authorizes_reusable_schema": False,
            "accept_closure_may_return_to_surface_selection": True,
        },
    }
    decision_options["closure_decision_options_id"] = "c8_successor_reuse_authority_probe_closure_options_" + sig8(decision_options)
    write_json(CLOSURE_DECISION_OPTIONS, decision_options)

    closure_gates = {
        "C8_REUSE_AUTHORITY_CLOSURE_0_PROBE_RECEIPT_VERIFIED": probe_receipt.get("gate") == "PASS",
        "C8_REUSE_AUTHORITY_CLOSURE_1_PROBE_RESULT_REVIEWED_AND_COMMITTED": probe_receipt.get("receipt_id") == "c8_successor_reuse_authority_probe_receipt_803165de",
        "C8_REUSE_AUTHORITY_CLOSURE_2_EXECUTION_COUNT_ONE": summary.get("probe_execution_count") == 1 and summary.get("allowed_probe_execution_count") == 1,
        "C8_REUSE_AUTHORITY_CLOSURE_3_REUSE_BOUNDARY_HELD": summary.get("reuse_boundary_held") is True,
        "C8_REUSE_AUTHORITY_CLOSURE_4_NO_NEW_AUTHORITY_NEEDED": summary.get("new_authority_needed_now") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_5_NO_MISSING_RULE_EXPOSED": summary.get("missing_reuse_authority_rule_exposed") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_6_NO_REUSABLE_SCHEMA_AUTHORIZED": summary.get("reusable_schema_authorized") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_7_NO_BUILD_RERUN_OR_PROPOSAL": summary.get("instrument_built_now") is False and summary.get("c8_rerun_now") is False and summary.get("missing_instrument_proposal_created_now") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_8_NO_GLOBAL_OR_FRONTIER_CLAIM": summary.get("global_solution_claim") is False and summary.get("frontier_solved_claim") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_9_EVIDENCE_COMPLETE": len(evidence_items) == 7 and probe_evidence.get("failed_evidence") == [],
        "C8_REUSE_AUTHORITY_CLOSURE_10_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_REUSE_AUTHORITY_CLOSURE_11_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "C8_REUSE_AUTHORITY_CLOSURE_12_HUMAN_DECISION_REQUIRED": closure_packet["human_decision_required"] is True,
    }

    false_closure_gates = [k for k, v in closure_gates.items() if v is not True]
    if false_closure_gates:
        failures.extend([f"closure_gate_false:{g}" for g in false_closure_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_FAILED"

    closure_audit = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_audit_v0",
        "closure_audit_id": None,
        "gate": gate,
        "closure_class": closure_class,
        "source_closure_packet_id": closure_packet["closure_packet_id"],
        "probe_id": PROBE_ID,
        "probe_execution_count": summary.get("probe_execution_count"),
        "allowed_probe_execution_count": summary.get("allowed_probe_execution_count"),
        "probe_output_class": summary.get("probe_output_class"),
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "closure_boundary": {
            "may_close_current_successor_surface_after_human_acceptance": True,
            "may_execute_additional_probe_now": False,
            "may_build_instrument_now": False,
            "may_rerun_c8_now": False,
            "may_authorize_reusable_schema_now": False,
            "may_claim_global_solution": False,
            "may_claim_frontier_solved": False,
        },
        "closure_gate_results": closure_gates,
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    closure_audit["closure_audit_id"] = "c8_successor_reuse_authority_probe_closure_audit_" + sig8(closure_audit)
    write_json(CLOSURE_AUDIT, closure_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_readout_v0",
        "title": "C8 successor surface bounded reuse-authority probe closure readout",
        "status": status,
        "outcome_class": outcome,
        "closure_packet_id": closure_packet["closure_packet_id"],
        "closure_class": closure_class,
        "source_probe_receipt_id": probe_receipt.get("receipt_id"),
        "probe_id": PROBE_ID,
        "probe_output_class": summary.get("probe_output_class"),
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "recommended_human_decision": decision_options["recommended_human_decision"],
        "human_decision_required": True,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "closure_packet_ref": rel(CLOSURE_PACKET),
        "closure_decision_options_ref": rel(CLOSURE_DECISION_OPTIONS),
        "closure_audit_ref": rel(CLOSURE_AUDIT),
        "source_probe_receipt_id": probe_receipt.get("receipt_id"),
        "source_probe_result_id": probe_result.get("probe_result_id"),
        "source_probe_evidence_id": probe_evidence.get("probe_evidence_id"),
        "source_probe_boundary_audit_id": probe_audit.get("boundary_audit_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_execution_count": summary.get("probe_execution_count"),
        "allowed_probe_execution_count": summary.get("allowed_probe_execution_count"),
        "probe_output_class": summary.get("probe_output_class"),
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "recommended_human_decision": decision_options["recommended_human_decision"],
        "human_decision_required": True,
        "additional_probe_authorized_now": False,
        "new_build_count": 0,
        "new_rerun_count": 0,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_closure_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "probe_receipt_ref": rel(PROBE_RECEIPT),
            "probe_evidence_ref": rel(PROBE_EVIDENCE),
            "probe_result_ref": rel(PROBE_RESULT),
            "probe_boundary_audit_ref": rel(PROBE_BOUNDARY_AUDIT),
            "probe_report_ref": rel(PROBE_REPORT),
        },
        "machine_readable_closure_summary": {
            "closure_packet_created": gate == "PASS",
            "closure_class": closure_class,
            "source_probe_receipt_id": probe_receipt.get("receipt_id"),
            "source_probe_evidence_id": probe_evidence.get("probe_evidence_id"),
            "source_probe_result_id": probe_result.get("probe_result_id"),
            "source_probe_boundary_audit_id": probe_audit.get("boundary_audit_id"),
            "source_acceptance_receipt_id": summary.get("source_acceptance_receipt_id"),
            "source_authority_id": summary.get("source_authority_id"),
            "source_prep_packet_id": summary.get("source_prep_packet_id"),
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_execution_count": summary.get("probe_execution_count"),
            "allowed_probe_execution_count": summary.get("allowed_probe_execution_count"),
            "probe_output_class": summary.get("probe_output_class"),
            "reuse_boundary_held": summary.get("reuse_boundary_held"),
            "new_authority_needed_now": summary.get("new_authority_needed_now"),
            "evidence_items_count": len(evidence_items),
            "failed_evidence_count": len(probe_evidence.get("failed_evidence", [])),
            "recommended_human_decision": decision_options["recommended_human_decision"],
            "possible_human_decisions": decision_options["possible_human_decisions"],
            "human_decision_required": True,
            "closure_accepted_now": False,
            "additional_probe_authorized_now": False,
            "instrument_built_now": False,
            "c8_rerun_now": False,
            "reusable_schema_authorized": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(local_nonzero),
            "next_command_goal": None,
        },
        "closure_gate_results": closure_gates,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "closure_packet": rel(CLOSURE_PACKET),
            "closure_decision_options": rel(CLOSURE_DECISION_OPTIONS),
            "closure_audit": rel(CLOSURE_AUDIT),
            "readout": rel(READOUT),
            "report": rel(REPORT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }

    receipt["receipt_id"] = "c8_successor_reuse_authority_probe_closure_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"closure_receipt_id={receipt['receipt_id']}")
    print(f"closure_receipt_path={rel(receipt_path)}")
    print(f"closure_packet_path={rel(CLOSURE_PACKET)}")
    print(f"closure_decision_options_path={rel(CLOSURE_DECISION_OPTIONS)}")
    print(f"closure_audit_path={rel(CLOSURE_AUDIT)}")
    print(f"source_probe_receipt_id={probe_receipt.get('receipt_id')}")
    print(f"source_probe_result_id={probe_result.get('probe_result_id')}")
    print(f"source_probe_evidence_id={probe_evidence.get('probe_evidence_id')}")
    print(f"source_probe_boundary_audit_id={probe_audit.get('boundary_audit_id')}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print(f"closure_class={closure_class}")
    print(f"probe_execution_count={summary.get('probe_execution_count')}")
    print(f"allowed_probe_execution_count={summary.get('allowed_probe_execution_count')}")
    print(f"probe_output_class={summary.get('probe_output_class')}")
    print(f"reuse_boundary_held={str(summary.get('reuse_boundary_held')).lower()}")
    print(f"new_authority_needed_now={str(summary.get('new_authority_needed_now')).lower()}")
    print(f"recommended_human_decision={decision_options['recommended_human_decision']}")
    print("human_decision_required=true")
    print("closure_accepted_now=false")
    print("additional_probe_authorized_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"closure_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
