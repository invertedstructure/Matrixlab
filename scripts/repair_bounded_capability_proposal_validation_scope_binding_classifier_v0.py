#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.validation_scope_binding_classifier_repair_v0"
NEXT_UNIT_ID_IF_RERUN_PASS = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_V0"

AUDIT_RECEIPT_ID = "bounded_capability_proposal_scope_binding_audit_receipt_a2c94558"
FAILED_VALIDATION_RUN_RECEIPT_ID = "bounded_capability_proposal_validation_path_run_receipt_f39ec164"
PROPOSAL_ID = "capability_proposal_57dda6e9"

AUDIT_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_admissibility_scope_binding_failure_audit_v0_receipts/bounded_capability_proposal_scope_binding_audit_receipt_a2c94558.json"
REPAIR_TARGET_PATH = ROOT / "data/bounded_capability_proposal_admissibility_scope_binding_failure_audit_v0/bounded_capability_proposal_admissibility_scope_binding_repair_target_v0.json"
FAILED_VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_f39ec164.json"

VALIDATION_RUN_SCRIPT_PATH = ROOT / "scripts/run_bounded_capability_proposal_validation_path_v0.py"
VALIDATION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0_receipts/bounded_capability_proposal_validation_path_prep_receipt_ec27c6e9.json"
VALIDATION_RUN_TARGET_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_validation_run_target_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_validation_scope_binding_classifier_repair_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_validation_scope_binding_classifier_repair_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_basis_v0.json"
CLASSIFIER_BEFORE_AFTER_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_before_after_v0.json"
STRUCTURAL_BINDING_POLICY_PATH = OUT_DIR / "bounded_capability_proposal_structural_scope_binding_policy_v0.json"
RERUN_SUMMARY_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_rerun_summary_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_validation_scope_binding_classifier_repair_transition_trace.json"

OLD_SNIPPET = '''    if "capability-boundary" not in scope_blob and "capability boundary" not in scope_blob:
        admissibility_failures.append("scope_missing_capability_boundary_binding")
'''

NEW_SNIPPET = '''    direct_scope_phrase_binding_present = "capability-boundary" in scope_blob or "capability boundary" in scope_blob
    structural_capability_boundary_binding_present = (
        proposal.get("proposal_id") == PROPOSAL_ID
        and proposal.get("proposal_kind") == EXPECTED_PROPOSAL_KIND
        and proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY"
        and proposal.get("source_stop_packet_id") == stop_packet.get("stop_packet_id")
        and stop_packet.get("stop_code") == "STOP_CAPABILITY_LAYER_REQUIRED"
        and proposal.get("missing_objects_addressed") == stop_packet.get("missing_objects") == EXPECTED_MISSING_OBJECTS
        and proposal.get("required_capability") == stop_packet.get("required_capability") == EXPECTED_REQUIRED_CAPABILITY
        and proposal.get("proposed_surface") == EXPECTED_PROPOSED_SURFACE
        and source_linkage_pass
        and schema_validation_pass
    )
    if not (direct_scope_phrase_binding_present or structural_capability_boundary_binding_present):
        admissibility_failures.append("scope_missing_capability_boundary_binding")
'''

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

def patch_validation_classifier() -> Dict[str, Any]:
    text_before = VALIDATION_RUN_SCRIPT_PATH.read_text()
    sha_before = hashlib.sha256(text_before.encode()).hexdigest()

    if OLD_SNIPPET in text_before:
        text_after = text_before.replace(OLD_SNIPPET, NEW_SNIPPET, 1)
        VALIDATION_RUN_SCRIPT_PATH.write_text(text_after)
        return {
            "patch_status": "PATCHED",
            "script_changed": True,
            "script_sha256_before": sha_before,
            "script_sha256_after": hashlib.sha256(text_after.encode()).hexdigest(),
            "old_phrase_only_classifier_found": True,
            "structural_classifier_present": True,
        }

    if "structural_capability_boundary_binding_present" in text_before:
        return {
            "patch_status": "ALREADY_PRESENT",
            "script_changed": False,
            "script_sha256_before": sha_before,
            "script_sha256_after": sha_before,
            "old_phrase_only_classifier_found": False,
            "structural_classifier_present": True,
        }

    raise RuntimeError("validation_scope_binding_classifier_patch_anchor_missing")

def run_validation_script() -> Dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATION_RUN_SCRIPT_PATH)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")

    match = re.search(r"bounded_capability_proposal_validation_path_run_receipt_path=(.+)", proc.stdout)
    receipt_path = None
    receipt = None

    if match:
        raw_path = match.group(1).strip()
        candidate = ROOT / raw_path
        if candidate.exists():
            receipt_path = candidate
            receipt = read_json(candidate)

    return {
        "returncode": proc.returncode,
        "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
        "receipt_path": rel(receipt_path) if receipt_path else None,
        "receipt": receipt,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        AUDIT_RECEIPT_PATH,
        REPAIR_TARGET_PATH,
        FAILED_VALIDATION_RUN_RECEIPT_PATH,
        VALIDATION_RUN_SCRIPT_PATH,
        VALIDATION_PATH_PREP_RECEIPT_PATH,
        VALIDATION_RUN_TARGET_PATH,
        PROPOSAL_PATH,
        STOP_PACKET_PATH,
        HUMAN_DECISION_PACKET_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    audit = read_json(AUDIT_RECEIPT_PATH)
    repair_target = read_json(REPAIR_TARGET_PATH)
    failed_run = read_json(FAILED_VALIDATION_RUN_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    audit_summary = audit.get("machine_readable_bounded_capability_proposal_admissibility_scope_binding_failure_audit_summary", {})
    failed_summary = failed_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    if audit.get("receipt_id") != AUDIT_RECEIPT_ID:
        failures.append(f"audit_receipt_id_wrong:{audit.get('receipt_id')}")
    if audit.get("gate") != "PASS":
        failures.append("audit_gate_not_pass")
    if audit_summary.get("classification") != "VALIDATOR_SCOPE_BINDING_PHRASE_OVERSTRICT_STRUCTURAL_BINDING_PRESENT":
        failures.append(f"audit_classification_wrong:{audit_summary.get('classification')}")
    if audit_summary.get("repair_target_kind") != "VALIDATOR_CLASSIFIER_REPAIR":
        failures.append(f"audit_repair_target_kind_wrong:{audit_summary.get('repair_target_kind')}")
    if audit_summary.get("structural_binding_present") is not True:
        failures.append("audit_structural_binding_not_true")
    if audit_summary.get("direct_scope_phrase_present") is not False:
        failures.append("audit_direct_scope_phrase_not_false")
    if audit.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"audit_terminal_next_wrong:{audit.get('terminal', {}).get('next_unit_id')}")

    if repair_target.get("target_status") != "READY":
        failures.append(f"repair_target_status_wrong:{repair_target.get('target_status')}")
    if repair_target.get("repair_target_kind") != "VALIDATOR_CLASSIFIER_REPAIR":
        failures.append(f"repair_target_kind_wrong:{repair_target.get('repair_target_kind')}")
    if repair_target.get("validator_repair_authorized") is not True:
        failures.append("validator_repair_not_authorized")
    if repair_target.get("proposal_edit_authorized") is not False:
        failures.append("proposal_edit_authorized_unexpected")
    if repair_target.get("proposal_validation_authorized") is not False:
        failures.append("proposal_validation_authorized_unexpected")
    if repair_target.get("proposal_acceptance_authorized") is not False:
        failures.append("proposal_acceptance_authorized_unexpected")
    if repair_target.get("implementation_authorized") is not False:
        failures.append("implementation_authorized_unexpected")

    if failed_run.get("receipt_id") != FAILED_VALIDATION_RUN_RECEIPT_ID:
        failures.append(f"failed_run_receipt_id_wrong:{failed_run.get('receipt_id')}")
    if failed_run.get("gate") != "FAIL":
        failures.append("failed_run_gate_not_fail")
    if failed_run.get("failures") != ["lawful_admissibility_failures:['scope_missing_capability_boundary_binding']"]:
        failures.append(f"failed_run_not_single_scope_binding_failure:{failed_run.get('failures')}")
    if failed_summary.get("source_linkage_pass") is not True:
        failures.append("failed_run_source_linkage_not_pass")
    if failed_summary.get("schema_validation_pass") is not True:
        failures.append("failed_run_schema_validation_not_pass")
    if failed_summary.get("boundary_guard_pass") is not True:
        failures.append("failed_run_boundary_guard_not_pass")
    if failed_summary.get("negative_control_pass") is not True:
        failures.append("failed_run_negative_control_not_pass")
    if failed_summary.get("human_decision_gate_pass") is not True:
        failures.append("failed_run_human_gate_not_pass")

    structural_policy = {
        "schema_version": "bounded_capability_proposal_structural_scope_binding_policy_v0",
        "policy_status": "READY" if not failures else "BLOCKED",
        "binding_policy": "A bounded capability proposal may satisfy capability-boundary scope binding either by direct scope phrase or by structural source-stop/capability linkage.",
        "direct_scope_phrase_binding": [
            "capability-boundary",
            "capability boundary",
        ],
        "structural_binding_requirements": [
            "proposal_id matches reviewed proposal",
            "proposal_kind is BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL",
            "proposal_status remains PROPOSAL_CANDIDATE_ONLY",
            "proposal source_stop_packet_id matches source stop packet",
            "source stop code is STOP_CAPABILITY_LAYER_REQUIRED",
            "proposal missing_objects_addressed equals source missing_objects",
            "proposal required_capability equals source required_capability",
            "proposal proposed_surface equals bounded v0 required capability surface",
            "source linkage validation passed",
            "schema validation passed",
        ],
        "does_not_authorize": [
            "proposal edit",
            "proposal acceptance",
            "human decision",
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

    if failures:
        patch_result = {"patch_status": "NOT_ATTEMPTED", "script_changed": False}
        rerun = {"returncode": None, "receipt_path": None, "receipt": None}
        gate = "FAIL"
        status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_BASIS_FAIL"
    else:
        try:
            patch_result = patch_validation_classifier()
        except Exception as e:
            failures.append(f"classifier_patch_failed:{e}")
            patch_result = {"patch_status": "FAILED", "script_changed": False, "error": str(e)}
            rerun = {"returncode": None, "receipt_path": None, "receipt": None}
            gate = "FAIL"
            status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_PATCH_FAIL"
        else:
            compile_proc = subprocess.run(
                [sys.executable, "-m", "py_compile", str(VALIDATION_RUN_SCRIPT_PATH)],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
            )
            if compile_proc.returncode != 0:
                failures.append("patched_validation_run_script_py_compile_failed")
                failures.append(compile_proc.stderr.strip())
                rerun = {"returncode": None, "receipt_path": None, "receipt": None}
                gate = "FAIL"
                status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_COMPILE_FAIL"
            else:
                rerun = run_validation_script()
                rerun_receipt = rerun.get("receipt") or {}
                rerun_summary = rerun_receipt.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

                if rerun.get("returncode") != 0:
                    failures.append(f"rerun_validation_returncode_nonzero:{rerun.get('returncode')}")
                if not rerun.get("receipt_path"):
                    failures.append("rerun_validation_receipt_path_missing")
                if rerun_receipt.get("gate") != "PASS":
                    failures.append(f"rerun_validation_gate_not_pass:{rerun_receipt.get('gate')}")
                if rerun_summary.get("lawful_admissibility_pass") is not True:
                    failures.append(f"rerun_lawful_admissibility_not_pass:{rerun_summary.get('lawful_admissibility_pass')}")
                if rerun_summary.get("proposal_validated_by_run") is not True:
                    failures.append("rerun_proposal_not_validated_by_run")
                if rerun_summary.get("proposal_admissible_for_human_decision") is not True:
                    failures.append("rerun_proposal_not_admissible_for_human_decision")
                if rerun_summary.get("human_decision_prep_target_ready") is not True:
                    failures.append("rerun_human_decision_prep_target_not_ready")
                if rerun_summary.get("next_unit_id") != NEXT_UNIT_ID_IF_RERUN_PASS:
                    failures.append(f"rerun_next_unit_wrong:{rerun_summary.get('next_unit_id')}")

                for key in [
                    "proposal_accepted",
                    "human_decision_taken",
                    "implementation_authorized",
                    "runtime_adoption_authorized",
                    "schema_mutation_authorized",
                    "move_addition_authorized",
                    "fixture_expansion_authorized",
                    "runtime_patch_authorized",
                    "hidden_next_command",
                    "c8_authorized",
                ]:
                    if rerun_summary.get(key) is not False:
                        failures.append(f"rerun_boundary_false_wrong:{key}:{rerun_summary.get(key)}")

                gate = "PASS" if not failures else "FAIL"
                status = (
                    "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIRED_VALIDATION_PASS"
                    if gate == "PASS"
                    else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_RERUN_FAIL"
                )

    rerun_receipt = rerun.get("receipt") or {}
    rerun_summary = rerun_receipt.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    basis = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "audit_receipt_id": AUDIT_RECEIPT_ID,
        "audit_receipt_ref": rel(AUDIT_RECEIPT_PATH),
        "failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "failed_validation_run_receipt_ref": rel(FAILED_VALIDATION_RUN_RECEIPT_PATH),
        "repair_target_ref": rel(REPAIR_TARGET_PATH),
        "repair_claim": "Repair the validation-run lawful admissibility classifier so structural source-stop/capability linkage satisfies capability-boundary scope binding.",
        "source_file_hashes": {rel(p): file_sha256(p) for p in required_files if p.exists()},
    }

    classifier_before_after = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_before_after_v0",
        "repair_scope": "LOCAL_VALIDATION_CLASSIFIER_ONLY",
        "classifier_problem": "The validation runner required a direct capability-boundary phrase in proposal scope and ignored structural source-stop/capability linkage.",
        "failed_term": "scope_missing_capability_boundary_binding",
        "patch_result": patch_result,
        "old_behavior": "Lawful admissibility failed unless proposal scope text directly contained capability-boundary/capability boundary.",
        "new_behavior": "Lawful admissibility accepts either direct phrase binding or structural binding through source stop packet, required capability, missing objects, proposed surface, source-linkage pass, and schema-validation pass.",
        "proposal_edited": False,
        "proposal_semantics_changed": False,
        "proposal_validation_authorized_by_repair": False,
        "human_decision_taken": False,
    }

    rerun_summary_artifact = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_rerun_summary_v0",
        "rerun_status": "PASS" if gate == "PASS" else "FAIL",
        "rerun_returncode": rerun.get("returncode"),
        "rerun_validation_receipt_ref": rerun.get("receipt_path"),
        "rerun_validation_receipt_id": rerun_receipt.get("receipt_id"),
        "rerun_validation_status": rerun_receipt.get("status"),
        "validation_path_id": rerun_summary.get("validation_path_id"),
        "validation_run_id": rerun_summary.get("validation_run_id"),
        "lawful_admissibility_pass": rerun_summary.get("lawful_admissibility_pass"),
        "proposal_validated_by_run": rerun_summary.get("proposal_validated_by_run"),
        "proposal_admissible_for_human_decision": rerun_summary.get("proposal_admissible_for_human_decision"),
        "human_decision_prep_target_ready": rerun_summary.get("human_decision_prep_target_ready"),
        "next_unit_id": rerun_summary.get("next_unit_id"),
        "proposal_accepted": rerun_summary.get("proposal_accepted", False),
        "human_decision_taken": rerun_summary.get("human_decision_taken", False),
        "implementation_authorized": rerun_summary.get("implementation_authorized", False),
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "repair_scope": "LOCAL_VALIDATION_CLASSIFIER_ONLY",
        "audit_receipt_id": AUDIT_RECEIPT_ID,
        "failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "rerun_validation_receipt_id": rerun_receipt.get("receipt_id"),
        "classifier_repaired": gate == "PASS",
        "validation_rerun_pass": gate == "PASS",
        "proposal_validated_by_run": rerun_summary.get("proposal_validated_by_run") is True,
        "proposal_admissible_for_human_decision": rerun_summary.get("proposal_admissible_for_human_decision") is True,
        "human_decision_prep_target_ready": rerun_summary.get("human_decision_prep_target_ready") is True,
        "next_unit_id": NEXT_UNIT_ID_IF_RERUN_PASS if gate == "PASS" else None,
        "proposal_edited": False,
        "proposal_accepted": False,
        "human_decision_taken": False,
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
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_readout_v0",
        "status": status,
        "repair_type": "VALIDATION_CLASSIFIER_ONLY",
        "audit_receipt_id": AUDIT_RECEIPT_ID,
        "failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "rerun_validation_receipt_id": rerun_receipt.get("receipt_id"),
        "interpretation": "The proposal was not edited. The validation classifier was repaired to recognize structural capability-boundary binding, validation was rerun, and the proposal is ready for human-decision prep."
        if gate == "PASS"
        else "Validation scope-binding classifier repair did not produce a clean validation rerun.",
        "next_unit_id": NEXT_UNIT_ID_IF_RERUN_PASS if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_profile_v0",
        "profile_status": status,
        "core_rule": "Repair the validation classifier only; do not mutate proposal content or grant implementation authority.",
        "structural_binding_policy_ref": rel(STRUCTURAL_BINDING_POLICY_PATH),
        "classifier_before_after_ref": rel(CLASSIFIER_BEFORE_AFTER_PATH),
        "rerun_summary_ref": rel(RERUN_SUMMARY_PATH),
        "must_not_infer": [
            "proposal edited",
            "proposal accepted",
            "human decision taken",
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
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "repair_result": "CLASSIFIER_REPAIRED_AND_VALIDATION_PASS" if gate == "PASS" else "REPAIR_FAILED",
            "audit_classification": audit_summary.get("classification"),
            "failed_validation_failure": failed_run.get("failures"),
            "rerun_validation_receipt_id": rerun_receipt.get("receipt_id"),
            "proposal_validated_by_run": rerun_summary.get("proposal_validated_by_run") is True,
            "proposal_admissible_for_human_decision": rerun_summary.get("proposal_admissible_for_human_decision") is True,
            "human_decision_prep_target_ready": rerun_summary.get("human_decision_prep_target_ready") is True,
            "proposal_edited": False,
            "proposal_accepted": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "ADMISSIBILITY_SCOPE_BINDING_FAILURE_AUDITED_AS_VALIDATOR_OVERSTRICT",
                "edge": "patch validation classifier to accept structural source-stop/capability binding",
                "to": "LOCAL_VALIDATION_CLASSIFIER_REPAIR_READY" if gate == "PASS" else "REPAIR_GATE_FAIL",
            },
            {
                "from": "LOCAL_VALIDATION_CLASSIFIER_REPAIR_READY" if gate == "PASS" else "REPAIR_GATE_FAIL",
                "edge": "rerun validation path without editing proposal",
                "to": "VALIDATION_PASS_HUMAN_DECISION_PREP_READY" if gate == "PASS" else "STOP_REPAIR_RERUN_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID_IF_RERUN_PASS if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CLASSIFIER_BEFORE_AFTER_PATH, classifier_before_after),
        (STRUCTURAL_BINDING_POLICY_PATH, structural_policy),
        (RERUN_SUMMARY_PATH, rerun_summary_artifact),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "AUDIT_RECEIPT_CONSUMED",
        "VALIDATOR_CLASSIFIER_REPAIR_TARGET_CONSUMED",
        "FAILED_VALIDATION_RUN_RECEIPT_CONSUMED",
        "VALIDATION_SCOPE_BINDING_CLASSIFIER_PATCHED",
        "STRUCTURAL_CAPABILITY_BOUNDARY_BINDING_POLICY_EMITTED",
        "PROPOSAL_NOT_EDITED",
        "VALIDATION_RERUN",
        "VALIDATION_RERUN_PASS",
        "LAWFUL_ADMISSIBILITY_PASS",
        "PROPOSAL_VALIDATED_BY_RUN",
        "PROPOSAL_ADMISSIBLE_FOR_HUMAN_DECISION",
        "HUMAN_DECISION_PREP_TARGET_READY",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_HUMAN_DECISION_TAKEN",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_capability_proposal_validation_scope_binding_classifier_repair_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_REPAIR_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_audit_receipt_id": AUDIT_RECEIPT_ID,
        "source_audit_receipt_ref": rel(AUDIT_RECEIPT_PATH),
        "source_failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "source_failed_validation_run_receipt_ref": rel(FAILED_VALIDATION_RUN_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "REPAIR_0_AUDIT_RECEIPT_CONSUMED": gate == "PASS",
            "REPAIR_1_VALIDATOR_REPAIR_AUTHORIZED": repair_target.get("validator_repair_authorized") is True,
            "REPAIR_2_PROPOSAL_EDIT_NOT_AUTHORIZED": repair_target.get("proposal_edit_authorized") is False,
            "REPAIR_3_CLASSIFIER_PATCHED": patch_result.get("patch_status") in {"PATCHED", "ALREADY_PRESENT"},
            "REPAIR_4_PROPOSAL_NOT_EDITED": True,
            "REPAIR_5_VALIDATION_RERUN_EMITTED_RECEIPT": bool(rerun.get("receipt_path")),
            "REPAIR_6_VALIDATION_RERUN_PASS": rerun_receipt.get("gate") == "PASS",
            "REPAIR_7_LAWFUL_ADMISSIBILITY_PASS": rerun_summary.get("lawful_admissibility_pass") is True,
            "REPAIR_8_PROPOSAL_VALIDATED_BY_RUN": rerun_summary.get("proposal_validated_by_run") is True,
            "REPAIR_9_HUMAN_DECISION_PREP_TARGET_READY": rerun_summary.get("human_decision_prep_target_ready") is True,
            "REPAIR_10_NO_PROPOSAL_ACCEPTANCE": rerun_summary.get("proposal_accepted") is False,
            "REPAIR_11_NO_HUMAN_DECISION_TAKEN": rerun_summary.get("human_decision_taken") is False,
            "REPAIR_12_NO_IMPLEMENTATION": rerun_summary.get("implementation_authorized") is False,
            "REPAIR_13_NO_RUNTIME_ADOPTION_AUTHORITY": rerun_summary.get("runtime_adoption_authorized") is False,
            "REPAIR_14_NO_SCHEMA_MUTATION": rerun_summary.get("schema_mutation_authorized") is False,
            "REPAIR_15_NO_MOVE_ADDITION": rerun_summary.get("move_addition_authorized") is False,
            "REPAIR_16_NO_C8_AUTHORIZATION": rerun_summary.get("c8_authorized") is False,
            "REPAIR_17_NO_HIDDEN_NEXT_COMMAND": rerun_summary.get("hidden_next_command") is False,
        },
        "machine_readable_bounded_capability_proposal_validation_scope_binding_classifier_repair_summary": {
            "status": status,
            "repair_scope": "LOCAL_VALIDATION_CLASSIFIER_ONLY",
            "audit_receipt_id": AUDIT_RECEIPT_ID,
            "audit_classification": audit_summary.get("classification"),
            "failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
            "failed_validation_failure": failed_run.get("failures"),
            "rerun_validation_receipt_id": rerun_receipt.get("receipt_id"),
            "rerun_validation_receipt_ref": rerun.get("receipt_path"),
            "validation_path_id": rerun_summary.get("validation_path_id"),
            "validation_run_id": rerun_summary.get("validation_run_id"),
            "classifier_repaired": gate == "PASS",
            "proposal_edited": False,
            "lawful_admissibility_pass": rerun_summary.get("lawful_admissibility_pass") is True,
            "proposal_validated_by_run": rerun_summary.get("proposal_validated_by_run") is True,
            "proposal_admissible_for_human_decision": rerun_summary.get("proposal_admissible_for_human_decision") is True,
            "human_decision_prep_target_ready": rerun_summary.get("human_decision_prep_target_ready") is True,
            "next_unit_id": NEXT_UNIT_ID_IF_RERUN_PASS if gate == "PASS" else None,
            "proposal_id": rerun_summary.get("proposal_id"),
            "proposal_status": rerun_summary.get("proposal_status"),
            "proposal_accepted": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "classifier_before_after": rel(CLASSIFIER_BEFORE_AFTER_PATH),
            "structural_binding_policy": rel(STRUCTURAL_BINDING_POLICY_PATH),
            "rerun_summary": rel(RERUN_SUMMARY_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_validation_scope_classifier_repair_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_validation_scope_classifier_repair_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_validation_scope_classifier_repair_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_validation_scope_classifier_repair_rerun_receipt_path={rerun.get('receipt_path') or 'NONE'}")
    print(f"bounded_capability_proposal_validation_scope_classifier_repair_next_unit={NEXT_UNIT_ID_IF_RERUN_PASS if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
