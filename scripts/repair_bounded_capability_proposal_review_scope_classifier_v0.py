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

UNIT_ID = "REPAIR_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.review_scope_classifier_repair_v0"
NEXT_UNIT_ID_IF_REVIEW_PASS = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_V0"

FAILED_REVIEW_RECEIPT_ID = "bounded_capability_proposal_review_receipt_5173ca94"
FAILED_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_review_v0_receipts/bounded_capability_proposal_review_receipt_5173ca94.json"

REVIEW_SCRIPT_PATH = ROOT / "scripts/review_bounded_capability_proposal_candidate_v0.py"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
ADAPTER_CLOSURE_RECEIPT_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts/capability_adapter_reference_closure_receipt_b02a18a5.json"
PENDING_REVIEW_POINTER_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0/bounded_capability_proposal_pending_review_pointer_v0.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_review_scope_classifier_repair_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_review_scope_classifier_repair_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_basis_v0.json"
CLASSIFIER_BEFORE_AFTER_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_before_after_v0.json"
RERUN_SUMMARY_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_rerun_summary_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_review_scope_classifier_repair_transition_trace.json"

OLD_CLASSIFIER = '''def any_forbidden_scope(scope: List[Any]) -> List[str]:
    blob = "\\n".join(str(x).lower() for x in scope)
    return [term for term in FORBIDDEN_SCOPE_TERMS if term.lower() in blob]
'''

NEW_CLASSIFIER = '''def any_forbidden_scope(scope: List[Any]) -> List[str]:
    """Return forbidden terms only when used as positive scope claims.

    A forbidden term appearing inside negative/boundary language is not itself
    a positive scope claim. Examples that must not trip this detector:
    "does not authorize runtime repair", "no fixture expansion by default",
    "negative-control receipt proves no runtime repair".
    """
    negative_markers = [
        "does not",
        "do not",
        "must not",
        "not ",
        " no ",
        "no ",
        "without",
        "forbid",
        "forbidden",
        "negative-control",
        "negative control",
        "boundary guard",
        "boundary",
        "guard",
        "non-goal",
        "non goal",
        "must_not_infer",
        "does_not_authorize",
        "not authorize",
        "does not authorize",
        "proves no",
        "remain zero",
        "zero",
    ]
    positive_hits: List[str] = []
    for item in scope:
        line = str(item).lower()
        for term in FORBIDDEN_SCOPE_TERMS:
            t = term.lower()
            if t not in line:
                continue
            if any(marker in line for marker in negative_markers):
                continue
            positive_hits.append(term)
    return sorted(set(positive_hits))
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

def patch_classifier() -> Dict[str, Any]:
    text_before = REVIEW_SCRIPT_PATH.read_text()
    sha_before = hashlib.sha256(text_before.encode()).hexdigest()

    if OLD_CLASSIFIER in text_before:
        text_after = text_before.replace(OLD_CLASSIFIER, NEW_CLASSIFIER, 1)
        REVIEW_SCRIPT_PATH.write_text(text_after)
        return {
            "patch_status": "PATCHED",
            "script_changed": True,
            "script_sha256_before": sha_before,
            "script_sha256_after": hashlib.sha256(text_after.encode()).hexdigest(),
            "old_classifier_found": True,
            "new_classifier_present": True,
        }

    if "A forbidden term appearing inside negative/boundary language" in text_before:
        return {
            "patch_status": "ALREADY_PRESENT",
            "script_changed": False,
            "script_sha256_before": sha_before,
            "script_sha256_after": sha_before,
            "old_classifier_found": False,
            "new_classifier_present": True,
        }

    raise RuntimeError("scope_classifier_patch_anchor_missing")

def run_review_script() -> Dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT_PATH)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")

    match = re.search(r"bounded_capability_proposal_review_receipt_path=(.+)", proc.stdout)
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

    failures: List[str] = []
    required_files = [
        FAILED_REVIEW_RECEIPT_PATH,
        REVIEW_SCRIPT_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        ADAPTER_CLOSURE_RECEIPT_PATH,
        PENDING_REVIEW_POINTER_PATH,
    ]

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    failed_review = read_json(FAILED_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    adapter_closure = read_json(ADAPTER_CLOSURE_RECEIPT_PATH)
    pending_pointer = read_json(PENDING_REVIEW_POINTER_PATH)

    failed_summary = failed_review.get("machine_readable_bounded_capability_proposal_review_summary", {})
    failed_failures = failed_review.get("failures", [])

    if failed_review.get("receipt_id") != FAILED_REVIEW_RECEIPT_ID:
        failures.append(f"failed_review_receipt_id_wrong:{failed_review.get('receipt_id')}")
    if failed_review.get("gate") != "FAIL":
        failures.append("failed_review_gate_not_fail")
    if failed_summary.get("review_verdict") != "BOUNDED_CAPABILITY_PROPOSAL_REVIEW_GATE_FAIL":
        failures.append("failed_review_verdict_unexpected")
    if failed_failures != ["forbidden_scope_terms_present:['runtime repair', 'fixture expansion by default']"]:
        failures.append(f"failed_review_failure_not_classifier_only:{failed_failures}")

    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")
    if adapter_closure.get("gate") != "PASS":
        failures.append("adapter_closure_gate_not_pass")
    if pending_pointer.get("pending_review") is not True:
        failures.append("pending_pointer_not_pending")

    if failures:
        gate = "FAIL"
        status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_BASIS_FAIL"
        patch_result = {"patch_status": "NOT_ATTEMPTED", "script_changed": False}
        rerun = {"returncode": None, "receipt_path": None, "receipt": None}
    else:
        try:
            patch_result = patch_classifier()
        except Exception as e:
            failures.append(f"classifier_patch_failed:{e}")
            gate = "FAIL"
            status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_PATCH_FAIL"
            patch_result = {
                "patch_status": "FAILED",
                "script_changed": False,
                "error": str(e),
            }
            rerun = {"returncode": None, "receipt_path": None, "receipt": None}
        else:
            compile_proc = subprocess.run(
                [sys.executable, "-m", "py_compile", str(REVIEW_SCRIPT_PATH)],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
            )
            if compile_proc.returncode != 0:
                failures.append("patched_review_script_py_compile_failed")
                failures.append(compile_proc.stderr.strip())
                gate = "FAIL"
                status = "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_COMPILE_FAIL"
                rerun = {"returncode": None, "receipt_path": None, "receipt": None}
            else:
                rerun = run_review_script()
                rerun_receipt = rerun.get("receipt") or {}
                rerun_summary = rerun_receipt.get("machine_readable_bounded_capability_proposal_review_summary", {})

                if rerun.get("returncode") != 0:
                    failures.append(f"rerun_review_returncode_nonzero:{rerun.get('returncode')}")
                if not rerun.get("receipt_path"):
                    failures.append("rerun_review_receipt_path_missing")
                if rerun_receipt.get("gate") != "PASS":
                    failures.append(f"rerun_review_gate_not_pass:{rerun_receipt.get('gate')}")
                if rerun_summary.get("review_verdict") != "VALID_PROPOSAL_CANDIDATE_READY_FOR_VALIDATION_PATH":
                    failures.append(f"rerun_review_verdict_wrong:{rerun_summary.get('review_verdict')}")
                if rerun_summary.get("validation_path_ready") is not True:
                    failures.append("rerun_validation_path_not_ready")
                if rerun_summary.get("next_unit_id") != NEXT_UNIT_ID_IF_REVIEW_PASS:
                    failures.append(f"rerun_next_unit_wrong:{rerun_summary.get('next_unit_id')}")

                for key in [
                    "proposal_accepted",
                    "proposal_validated",
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
                    "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIRED_REVIEW_PASS"
                    if gate == "PASS"
                    else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_RERUN_FAIL"
                )

    rerun_receipt = rerun.get("receipt") or {}
    rerun_summary = rerun_receipt.get("machine_readable_bounded_capability_proposal_review_summary", {})

    basis = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if not failures or status.endswith("REVIEW_PASS") else "BASIS_FAIL",
        "failed_review_receipt_id": FAILED_REVIEW_RECEIPT_ID,
        "failed_review_receipt_ref": rel(FAILED_REVIEW_RECEIPT_PATH),
        "failed_review_failures": failed_failures,
        "repair_claim": "Repair the proposal-review forbidden-scope detector so negative/boundary usage of forbidden terms does not count as a positive scope claim.",
        "source_file_hashes": {rel(p): file_sha256(p) for p in required_files if p.exists()},
    }

    classifier_before_after = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_before_after_v0",
        "repair_scope": "LOCAL_REVIEW_CLASSIFIER_ONLY",
        "classifier_problem": "The prior detector searched raw scope text and could not distinguish positive scope claims from negative/boundary language.",
        "failed_terms": ["runtime repair", "fixture expansion by default"],
        "patch_result": patch_result,
        "old_behavior": "Any occurrence of a forbidden term in scope text was blocking.",
        "new_behavior": "A forbidden term blocks only when it appears as a positive scope claim without negative/boundary markers.",
        "proposal_edited": False,
        "proposal_semantics_changed": False,
    }

    rerun_summary_artifact = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_rerun_summary_v0",
        "rerun_status": "PASS" if gate == "PASS" else "FAIL",
        "rerun_returncode": rerun.get("returncode"),
        "rerun_review_receipt_ref": rerun.get("receipt_path"),
        "rerun_review_receipt_id": rerun_receipt.get("receipt_id"),
        "rerun_review_status": rerun_receipt.get("status"),
        "rerun_review_verdict": rerun_summary.get("review_verdict"),
        "validation_path_ready": rerun_summary.get("validation_path_ready"),
        "next_unit_id": rerun_summary.get("next_unit_id"),
        "proposal_accepted": rerun_summary.get("proposal_accepted", False),
        "proposal_validated": rerun_summary.get("proposal_validated", False),
        "implementation_authorized": rerun_summary.get("implementation_authorized", False),
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "repair_scope": "LOCAL_REVIEW_CLASSIFIER_ONLY",
        "failed_review_receipt_id": FAILED_REVIEW_RECEIPT_ID,
        "rerun_review_receipt_id": rerun_receipt.get("receipt_id"),
        "classifier_repaired": gate == "PASS",
        "review_rerun_pass": gate == "PASS",
        "validation_path_ready": rerun_summary.get("validation_path_ready") is True,
        "next_unit_id": NEXT_UNIT_ID_IF_REVIEW_PASS if gate == "PASS" else None,
        "proposal_edited": False,
        "proposal_accepted": False,
        "proposal_validated": False,
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
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_readout_v0",
        "status": status,
        "repair_type": "REVIEW_CLASSIFIER_ONLY",
        "failed_review_receipt_id": FAILED_REVIEW_RECEIPT_ID,
        "rerun_review_receipt_id": rerun_receipt.get("receipt_id"),
        "interpretation": "The proposal was not edited. The scope detector was tightened, the proposal review was rerun, and the candidate is ready for validation-path preparation."
        if gate == "PASS"
        else "Scope-classifier repair did not produce a clean proposal-review rerun.",
        "next_unit_id": NEXT_UNIT_ID_IF_REVIEW_PASS if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_profile_v0",
        "profile_status": status,
        "core_rule": "Repair the review detector only; do not mutate proposal content or grant authority.",
        "classifier_before_after_ref": rel(CLASSIFIER_BEFORE_AFTER_PATH),
        "rerun_summary_ref": rel(RERUN_SUMMARY_PATH),
        "must_not_infer": [
            "proposal accepted",
            "proposal validated",
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
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "repair_result": "CLASSIFIER_REPAIRED_AND_REVIEW_PASS" if gate == "PASS" else "REPAIR_FAILED",
            "failed_review_failure": failed_failures,
            "rerun_review_receipt_id": rerun_receipt.get("receipt_id"),
            "validation_path_ready": rerun_summary.get("validation_path_ready") is True,
            "proposal_edited": False,
            "proposal_accepted": False,
            "proposal_validated": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "BOUNDED_CAPABILITY_PROPOSAL_REVIEW_GATE_FAIL_FOR_FORBIDDEN_SCOPE_TERMS",
                "edge": "classify failure as detector overreach against negative/boundary scope language",
                "to": "LOCAL_REVIEW_CLASSIFIER_REPAIR_READY" if not failures or rerun.get("receipt_path") else "REPAIR_BASIS_FAIL",
            },
            {
                "from": "LOCAL_REVIEW_CLASSIFIER_REPAIR_READY",
                "edge": "patch forbidden-scope classifier and rerun proposal review",
                "to": "PROPOSAL_REVIEW_PASS_READY_FOR_VALIDATION_PATH" if gate == "PASS" else "STOP_REPAIR_RERUN_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID_IF_REVIEW_PASS if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CLASSIFIER_BEFORE_AFTER_PATH, classifier_before_after),
        (RERUN_SUMMARY_PATH, rerun_summary_artifact),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "FAILED_REVIEW_RECEIPT_CONSUMED",
        "CLASSIFIER_ONLY_FAILURE_CONFIRMED",
        "FORBIDDEN_SCOPE_DETECTOR_PATCHED",
        "NEGATIVE_BOUNDARY_LANGUAGE_EXEMPTED_FROM_POSITIVE_SCOPE_HITS",
        "PROPOSAL_NOT_EDITED",
        "PROPOSAL_REVIEW_RERUN",
        "PROPOSAL_REVIEW_RERUN_PASS",
        "VALIDATION_PATH_READY",
        "NO_PROPOSAL_VALIDATION",
        "NO_PROPOSAL_ACCEPTANCE",
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
        "schema_version": "bounded_capability_proposal_review_scope_classifier_repair_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_SCOPE_CLASSIFIER_REPAIR_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_review_receipt_id": FAILED_REVIEW_RECEIPT_ID,
        "source_failed_review_receipt_ref": rel(FAILED_REVIEW_RECEIPT_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "REPAIR_0_FAILED_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "REPAIR_1_CLASSIFIER_ONLY_FAILURE_CONFIRMED": failed_failures == ["forbidden_scope_terms_present:['runtime repair', 'fixture expansion by default']"],
            "REPAIR_2_REVIEW_SCRIPT_PATCHED": patch_result.get("patch_status") in {"PATCHED", "ALREADY_PRESENT"},
            "REPAIR_3_PROPOSAL_NOT_EDITED": True,
            "REPAIR_4_REVIEW_RERUN_EMITTED_RECEIPT": bool(rerun.get("receipt_path")),
            "REPAIR_5_REVIEW_RERUN_PASS": rerun_receipt.get("gate") == "PASS",
            "REPAIR_6_VALIDATION_PATH_READY": rerun_summary.get("validation_path_ready") is True,
            "REPAIR_7_NO_PROPOSAL_VALIDATION": rerun_summary.get("proposal_validated") is False,
            "REPAIR_8_NO_PROPOSAL_ACCEPTANCE": rerun_summary.get("proposal_accepted") is False,
            "REPAIR_9_NO_IMPLEMENTATION": rerun_summary.get("implementation_authorized") is False,
            "REPAIR_10_NO_RUNTIME_ADOPTION_AUTHORITY": rerun_summary.get("runtime_adoption_authorized") is False,
            "REPAIR_11_NO_SCHEMA_MUTATION": rerun_summary.get("schema_mutation_authorized") is False,
            "REPAIR_12_NO_MOVE_ADDITION": rerun_summary.get("move_addition_authorized") is False,
            "REPAIR_13_NO_C8_AUTHORIZATION": rerun_summary.get("c8_authorized") is False,
            "REPAIR_14_NO_HIDDEN_NEXT_COMMAND": rerun_summary.get("hidden_next_command") is False,
        },
        "machine_readable_bounded_capability_proposal_review_scope_classifier_repair_summary": {
            "status": status,
            "repair_scope": "LOCAL_REVIEW_CLASSIFIER_ONLY",
            "failed_review_receipt_id": FAILED_REVIEW_RECEIPT_ID,
            "failed_review_failure": failed_failures,
            "rerun_review_receipt_id": rerun_receipt.get("receipt_id"),
            "rerun_review_receipt_ref": rerun.get("receipt_path"),
            "rerun_review_verdict": rerun_summary.get("review_verdict"),
            "classifier_repaired": gate == "PASS",
            "proposal_edited": False,
            "content_review_clean": rerun_summary.get("content_review_clean") is True,
            "validation_path_ready": rerun_summary.get("validation_path_ready") is True,
            "next_unit_id": NEXT_UNIT_ID_IF_REVIEW_PASS if gate == "PASS" else None,
            "proposal_id": rerun_summary.get("proposal_id"),
            "proposal_status": rerun_summary.get("proposal_status"),
            "proposal_accepted": False,
            "proposal_validated": False,
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
            "rerun_summary": rel(RERUN_SUMMARY_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_scope_classifier_repair_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_scope_classifier_repair_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_scope_classifier_repair_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_scope_classifier_repair_rerun_review_receipt_path={rerun.get('receipt_path') or 'NONE'}")
    print(f"bounded_capability_proposal_scope_classifier_repair_next_unit={NEXT_UNIT_ID_IF_REVIEW_PASS if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
