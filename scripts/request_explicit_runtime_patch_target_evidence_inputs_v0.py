#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REQUEST_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_INPUTS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_input_request.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_INPUT_REQUEST"
MODE = "REQUEST / EXPLICIT_INPUT_FIELDS / NO_TARGET_SELECTION"
BUILD_MODE = "EXPLICIT_TARGET_EVIDENCE_INPUT_REQUEST_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "76b44fed"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0_receipts/76b44fed.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/target_evidence_packet_review_classification_v0.json"
SOURCE_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/proposed_runtime_patch_target_evidence_packet_template_v0.json"
SOURCE_SCHEMA_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json"
SOURCE_HINT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json"
SOURCE_REQUEST_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0_receipts"

INPUT_CONTRACT_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_contract_v0.json"
ENV_TEMPLATE_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_env_template.sh"
INPUT_READOUT_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_readout_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_request_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_request_profile_v0.json"
REPORT_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_request_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "explicit_runtime_patch_target_evidence_input_request_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_TEMPLATE_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    SOURCE_REQUEST_PACKET_PATH,
]

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
]

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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    template = read_json(SOURCE_TEMPLATE_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)

    if receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("source_review_terminal_not_missing_packet")
    if classification.get("review_status") != "TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("source_review_status_not_missing")
    if classification.get("target_candidate_declared_for_review") is not False:
        failures.append("source_review_declared_candidate_unexpectedly")
    if classification.get("target_candidate_ref") is not None:
        failures.append("source_review_has_candidate_ref_unexpectedly")
    if classification.get("target_selected_for_build") is not False:
        failures.append("source_review_selected_target_for_build")
    if classification.get("accepted_for_build") is not False:
        failures.append("source_review_accepted_for_build")
    if classification.get("runtime_patch_authorized") is not False:
        failures.append("source_review_authorized_runtime_patch")
    if template.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("template_wrong_packet_object_type")
    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("schema_wrong_packet_object_type")
    if inventory.get("hint_count") != 13:
        failures.append(f"hint_count_not_13:{inventory.get('hint_count')}")
    if inventory.get("target_selected") is not False:
        failures.append("inventory_target_selected_unexpectedly")
    return failures

def input_contract() -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_contract_v0",
        "contract_id": "explicit_target_evidence_inputs_" + sha8({"source": SOURCE_REVIEW_RECEIPT_ID, "fields": REQUIRED_ENV_FIELDS}),
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_review_receipt_ref": rel(SOURCE_REVIEW_RECEIPT_PATH),
        "source_template_ref": rel(SOURCE_TEMPLATE_PATH),
        "trigger_halt": "STOP_EXPLICIT_TARGET_REF_MISSING",
        "trigger_meaning": "The provider cannot run until one explicit selected target reference and the remaining evidence fields are supplied by the operator.",
        "required_env_fields": REQUIRED_ENV_FIELDS,
        "field_rules": {
            "SELECTED_TARGET_REF": "exactly one local bounded path; no latest lookup; no mtime tie-break; no directory preference",
            "SELECTED_TARGET_KIND": "explicit target kind string",
            "WHY_THIS_TARGET_IS_LOAD_BEARING": "explicit reason the selected target is load-bearing for the runtime patch target question",
            "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON": "JSON array explaining why other bounded hints are context rather than the selected target",
            "SOURCE_EVIDENCE_REFS_JSON": "JSON array of explicit source artifact refs supporting the target",
            "VERIFICATION_GATE_REF": "local bounded ref to the exact gate that would check this target",
            "ROLLBACK_OR_STOP_BOUNDARY_REF": "local bounded ref to the exact rollback-or-stop boundary for this target"
        },
        "accepted_output_if_filled": "provided_runtime_patch_target_evidence_packet_v0.json",
        "not_authorized": [
            "select target from 13 hints by preference",
            "guess target from latest file",
            "use mtime selection",
            "apply runtime patch",
            "modify target files",
            "open C5",
            "accept packet for build",
            "grant general Cell1 authority",
            "promote proposal status",
            "fabricate accepted proposal"
        ],
        "review_only": True,
        "target_candidate_declared": False,
        "target_selected_for_build": False,
        "runtime_patch_authorized": False,
        "recommended_next": "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_ENV_V0",
    }

def env_template() -> str:
    return """# Fill these explicitly, then rerun PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0.
# Do not use latest-file guessing, mtime selection, or preference collapse.

export SELECTED_TARGET_REF='exact/local/path.json'
export SELECTED_TARGET_KIND='runtime_patch_target'
export WHY_THIS_TARGET_IS_LOAD_BEARING='explain why this exact target is load-bearing'
export WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON='["explain why each non-selected bounded hint is not the target, or cite inventory rows"]'
export SOURCE_EVIDENCE_REFS_JSON='["exact/source/artifact.json"]'
export VERIFICATION_GATE_REF='exact/local/verification_gate.json'
export ROLLBACK_OR_STOP_BOUNDARY_REF='exact/local/rollback_or_stop_boundary.json'
"""

def input_readout(contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_readout_v0",
        "readout_status": "EXPLICIT_TARGET_EVIDENCE_INPUTS_REQUESTED",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "required_env_field_count": len(REQUIRED_ENV_FIELDS),
        "required_env_fields": REQUIRED_ENV_FIELDS,
        "first_missing_field_observed": "SELECTED_TARGET_REF",
        "target_selected": False,
        "target_candidate_declared": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "env_template_ref": rel(ENV_TEMPLATE_PATH),
        "contract_ref": rel(INPUT_CONTRACT_PATH),
        "recommended_next": contract["recommended_next"],
    }

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_authority_boundary_v0",
        "may_request_explicit_inputs": True,
        "may_emit_env_template": True,
        "may_select_target": False,
        "may_declare_target_candidate": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "must_not_infer": [
            "missing env means target can be guessed",
            "template placeholders are candidate evidence",
            "input request authorizes patching",
            "input request selects among the 13 hints"
        ],
    }

def rollup() -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_request_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "input_contract_emitted_count": 1,
        "env_template_emitted_count": 1,
        "required_env_field_count": len(REQUIRED_ENV_FIELDS),
        "target_candidate_declared_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_ENV_V0",
    }

def profile(roll: Dict[str, Any]) -> Dict[str, Any]:
    bad_keys = [
        "target_candidate_declared_count",
        "target_selected_for_build_count",
        "accepted_for_build_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "hidden_next_command_count",
        "unbounded_payload_inspection_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_request_profile_v0",
        "profile_id": "explicit_target_evidence_input_request_" + sha8({"source": SOURCE_REVIEW_RECEIPT_ID}),
        "status": "EXPLICIT_TARGET_EVIDENCE_INPUTS_REQUESTED",
        "target_candidate_declared": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in bad_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report(roll: Dict[str, Any], prof: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_request_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "profile_status": prof["status"],
        "required_env_field_count": roll["required_env_field_count"],
        "recommended_next_handling": roll["recommended_next"],
        "target_candidate_declared_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace() -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_evidence_input_request_transition_trace_v0",
        "trace": [
            {
                "step": "consume_target_evidence_packet_missing_surface",
                "question": "what blocked provider execution",
                "answer": "STOP_EXPLICIT_TARGET_REF_MISSING",
                "taken": "emit_explicit_input_contract",
            },
            {
                "step": "emit_env_template",
                "question": "can a target be chosen without explicit inputs",
                "answer": "no",
                "taken": "stop_without_target_selection",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_EXPLICIT_TARGET_EVIDENCE_INPUTS_REQUESTED",
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    contract = input_contract()
    readout = input_readout(contract)
    boundary = authority_boundary()
    roll = rollup()
    prof = profile(roll)
    rep = report(roll, prof)
    trace = transition_trace()

    write_json(INPUT_CONTRACT_PATH, contract)
    ENV_TEMPLATE_PATH.write_text(env_template())
    write_json(INPUT_READOUT_PATH, readout)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "EXPLICIT_INPUT_REQUEST_0_SOURCE_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "EXPLICIT_INPUT_REQUEST_1_INPUT_CONTRACT_EMITTED": INPUT_CONTRACT_PATH.exists(),
        "EXPLICIT_INPUT_REQUEST_2_ENV_TEMPLATE_EMITTED": ENV_TEMPLATE_PATH.exists(),
        "EXPLICIT_INPUT_REQUEST_3_INPUT_READOUT_EMITTED": INPUT_READOUT_PATH.exists(),
        "EXPLICIT_INPUT_REQUEST_4_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "EXPLICIT_INPUT_REQUEST_5_NO_TARGET_CANDIDATE_DECLARED": prof["target_candidate_declared"] is False,
        "EXPLICIT_INPUT_REQUEST_6_NO_TARGET_SELECTED_FOR_BUILD": prof["target_selected_for_build"] is False,
        "EXPLICIT_INPUT_REQUEST_7_NO_ACCEPTED_FOR_BUILD": prof["accepted_for_build"] is False,
        "EXPLICIT_INPUT_REQUEST_8_NO_RUNTIME_PATCH": prof["runtime_patch_applied"] is False,
        "EXPLICIT_INPUT_REQUEST_9_NO_TARGET_FILE_MODIFICATION": prof["target_file_modified"] is False,
        "EXPLICIT_INPUT_REQUEST_10_NO_C5_OPENED": prof["c5_opened"] is False,
        "EXPLICIT_INPUT_REQUEST_11_NO_GENERAL_CELL1_AUTHORITY": prof["general_cell1_authority_granted"] is False,
        "EXPLICIT_INPUT_REQUEST_12_NO_LATEST_FILE_GUESSING": roll["latest_file_guessing_count"] == 0,
        "EXPLICIT_INPUT_REQUEST_13_NO_MTIME_SELECTION": roll["mtime_selection_count"] == 0,
        "EXPLICIT_INPUT_REQUEST_14_NO_HIDDEN_NEXT_COMMAND": prof["next_command_goal"] is None,
        "EXPLICIT_INPUT_REQUEST_15_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {"type": "STOP", "stop_code": "STOP_EXPLICIT_TARGET_EVIDENCE_INPUT_REQUEST_GATE_FAIL", "next_command_goal": None}

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "source": SOURCE_REVIEW_RECEIPT_ID,
        "contract": contract,
        "terminal": terminal,
        "gate": gate,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "explicit_runtime_patch_target_evidence_input_request_receipt_v0",
        "receipt_type": "EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_INPUT_REQUEST_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "input_request_summary": {
            "status": prof["status"],
            "trigger_halt": "STOP_EXPLICIT_TARGET_REF_MISSING",
            "required_env_field_count": len(REQUIRED_ENV_FIELDS),
            "required_env_fields": REQUIRED_ENV_FIELDS,
            "target_candidate_declared": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": prof["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "input_contract": rel(INPUT_CONTRACT_PATH),
            "env_template": rel(ENV_TEMPLATE_PATH),
            "input_readout": rel(INPUT_READOUT_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"explicit_target_evidence_input_request_receipt_id={receipt_id}")
    print(f"explicit_target_evidence_input_request_receipt_path={rel(receipt_path)}")
    print(f"explicit_target_evidence_input_contract_path={rel(INPUT_CONTRACT_PATH)}")
    print(f"explicit_target_evidence_env_template_path={rel(ENV_TEMPLATE_PATH)}")
    print(f"explicit_target_evidence_input_request_rollup_path={rel(ROLLUP_PATH)}")
    print(f"explicit_target_evidence_input_request_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
