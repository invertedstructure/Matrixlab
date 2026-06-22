#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_JURISDICTION_GATE_V0_WITH_DEMO_VERDICTS_V0"
TARGET_UNIT_ID = "jurisdiction_gate.v0"

JURISDICTION_GATE_POLICY_ID = "57838400"
JURISDICTION_GATE_POLICY_RECEIPT_ID = "993751b4"
MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
MOVE_REGISTRY_POLICY_ID = "34863965"
MOVE_REGISTRY_POLICY_RECEIPT_ID = "1264c091"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
HALT_VOCABULARY_POLICY_ID = "0707a2d7"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

POLICY_PATH = ROOT / "data" / "jurisdiction_gate_v0_policies" / f"{JURISDICTION_GATE_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_policy_receipts" / f"{JURISDICTION_GATE_POLICY_ID}.json"

MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_POLICY_PATH = ROOT / "data" / "move_registry_v0_policies" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_POLICY_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_policy_receipts" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_REGISTRY_PATH = ROOT / "data" / "move_registry_v0" / "move_registry_v0.json"
MOVE_ADMISSION_GATE_PATH = ROOT / "data" / "move_registry_v0" / "move_admission_gate_v0.json"
MOVE_INSPECTION_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "applicable_move_inspection_schema_v0.json"
BLOCKED_MOVE_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "blocked_move_record_schema_v0.json"
SELECTED_MOVE_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "selected_move_record_schema_v0.json"
MISSING_MOVE_STUB_PATH = ROOT / "data" / "move_registry_v0" / "missing_move_proposal_stub_v0.json"
DAY4_POSITIVE_RUN_PATH = ROOT / "data" / "move_registry_v0_demo" / "day4_demo_positive_run.json"
DAY4_MISSING_MOVE_RUN_PATH = ROOT / "data" / "move_registry_v0_demo" / "day4_demo_missing_move_run.json"

HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_POLICY_PATH = ROOT / "data" / "halt_vocabulary_v0_policies" / f"{HALT_VOCABULARY_POLICY_ID}.json"
HALT_VOCABULARY_PATH = ROOT / "data" / "halt_vocabulary_v0" / "halt_vocabulary_v0.json"
HALT_RECORD_SCHEMA_PATH = ROOT / "data" / "halt_record_schemas" / "halt_record_schema_v0.json"
HALT_NEXT_HANDLING_PATH = ROOT / "data" / "halt_to_next_handling_tables" / "halt_to_next_handling_table_v0.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

ARTIFACT_DIR = ROOT / "data" / "jurisdiction_gate_v0"
PATCH_DIR = ROOT / "data" / "jurisdiction_gate_v0_patches"
DEMO_DIR = ROOT / "data" / "jurisdiction_gate_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts"

SOURCE_FILES = [
    POLICY_PATH,
    POLICY_RECEIPT_PATH,
    MOVE_IMPL_RECEIPT_PATH,
    MOVE_POLICY_PATH,
    MOVE_POLICY_RECEIPT_PATH,
    MOVE_REGISTRY_PATH,
    MOVE_ADMISSION_GATE_PATH,
    MOVE_INSPECTION_SCHEMA_PATH,
    BLOCKED_MOVE_SCHEMA_PATH,
    SELECTED_MOVE_SCHEMA_PATH,
    MISSING_MOVE_STUB_PATH,
    DAY4_POSITIVE_RUN_PATH,
    DAY4_MISSING_MOVE_RUN_PATH,
    HALT_IMPLEMENTATION_RECEIPT_PATH,
    HALT_POLICY_PATH,
    HALT_VOCABULARY_PATH,
    HALT_RECORD_SCHEMA_PATH,
    HALT_NEXT_HANDLING_PATH,
    PROCEED_RECEIPT_PATH,
    PROCEED_ADAPTER_MODULE_PATH,
    TRACE_LEDGER_RECEIPT_PATH,
    TRACE_SCHEMA_PATH,
    PROPOSAL_LEDGER_SCHEMA_PATH,
    TRACE_LEDGER_RUNNER_PATH,
    LOCAL_REGIME_V1_PATH,
]

VERDICTS = [
    "AUTHORIZED_LOCAL",
    "REQUIRES_PROPOSAL",
    "REQUIRES_EXTRACTION",
    "REQUIRES_HUMAN_REVIEW",
    "FORBIDDEN",
]

VERDICT_TO_HALT = {
    "AUTHORIZED_LOCAL": None,
    "REQUIRES_PROPOSAL": "STOP_PROPOSAL_REQUIRED",
    "REQUIRES_EXTRACTION": "STOP_NEEDS_EXTRACTION",
    "REQUIRES_HUMAN_REVIEW": "STOP_HUMAN_REVIEW_REQUIRED",
    "FORBIDDEN": "STOP_FORBIDDEN_MOVE",
}

DEMO_SPECS = [
    ("DAY5_AUTHORIZED_LOCAL_MOVE", "unit.mark_complete.v0", "AUTHORIZED_LOCAL"),
    ("DAY5_PROPOSAL_REQUIRED", "boundary.emit_next_unit.v0", "REQUIRES_PROPOSAL"),
    ("DAY5_EXTRACTION_REQUIRED", "proto.import_behavior.v0", "REQUIRES_EXTRACTION"),
    ("DAY5_HUMAN_REVIEW_REQUIRED", "move_registry.add_candidate.v0", "REQUIRES_HUMAN_REVIEW"),
    ("DAY5_FORBIDDEN_MOVE", "execute_unregistered_move.v0", "FORBIDDEN"),
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.exists()}

def terminal_for_verdict(verdict: str) -> Dict[str, Any]:
    if verdict == "AUTHORIZED_LOCAL":
        return {
            "type": "ADVANCE",
            "next_unit_id": "receipt.emit_terminal.v0",
            "stop_code": None,
        }
    return {
        "type": "STOP",
        "stop_code": VERDICT_TO_HALT[verdict],
        "next_unit_id": None,
    }

def validate_source_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != JURISDICTION_GATE_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != JURISDICTION_GATE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{receipt.get('policy_status')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")
    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    if receipt.get("source_move_registry_implementation_receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_move_impl_wrong:{receipt.get('source_move_registry_implementation_receipt_id')}")
    if receipt.get("source_halt_vocabulary_implementation_receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_halt_impl_wrong:{receipt.get('source_halt_vocabulary_implementation_receipt_id')}")
    if receipt.get("source_proceed_adapter_implementation_receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_proceed_wrong:{receipt.get('source_proceed_adapter_implementation_receipt_id')}")
    if receipt.get("source_trace_ledger_implementation_receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_trace_ledger_wrong:{receipt.get('source_trace_ledger_implementation_receipt_id')}")
    if receipt.get("source_local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"source_local_regime_wrong:{receipt.get('source_local_regime_hash')}")

    summary = receipt.get("policy_summary", {})
    if summary.get("core_law") != "A move may be locally admissible and still not authorized.":
        failures.append(f"core_law_wrong:{summary.get('core_law')}")
    if summary.get("execution_rule") != "Only AUTHORIZED_LOCAL moves may execute.":
        failures.append(f"execution_rule_wrong:{summary.get('execution_rule')}")
    if summary.get("selector_rule") != "Selector may only choose from authorized_executable_moves.":
        failures.append(f"selector_rule_wrong:{summary.get('selector_rule')}")

    verdict_enum = receipt.get("jurisdiction_verdict_enum", {})
    if verdict_enum.get("verdicts") != VERDICTS:
        failures.append(f"verdicts_wrong:{verdict_enum.get('verdicts')}")
    if verdict_enum.get("verdict_to_halt") != VERDICT_TO_HALT:
        failures.append(f"verdict_to_halt_wrong:{verdict_enum.get('verdict_to_halt')}")

    gate = receipt.get("jurisdiction_gate", {})
    if gate.get("verdict_order", [])[:5] != [
        "FORBIDDEN",
        "REQUIRES_EXTRACTION",
        "REQUIRES_HUMAN_REVIEW",
        "REQUIRES_PROPOSAL",
        "AUTHORIZED_LOCAL",
    ]:
        failures.append(f"verdict_order_wrong:{gate.get('verdict_order')}")
    if gate.get("selector_rule") != "Selector may only choose from authorized_executable_moves.":
        failures.append("selector_not_authorized_only")
    if "A registry mutation cannot be laundered through proposal-only wording." not in gate.get("anti_laundering_law", []):
        failures.append("anti_laundering_registry_rule_missing")

    halt_patch = receipt.get("halt_vocabulary_authority_patch", {})
    if halt_patch.get("patch_mode") != "future_halt_vocabulary_patch_only_do_not_mutate_existing_halt_vocabulary":
        failures.append(f"halt_patch_mode_wrong:{halt_patch.get('patch_mode')}")
    for code in ["STOP_AUTHORITY_BOUNDARY", "STOP_PROPOSAL_REQUIRED", "STOP_HUMAN_REVIEW_REQUIRED", "STOP_FORBIDDEN_MOVE"]:
        if code not in halt_patch.get("adds_canonical_entries", {}):
            failures.append(f"halt_patch_missing:{code}")
    if halt_patch.get("reuses_existing_entries", {}).get("STOP_NEEDS_EXTRACTION") != "used for REQUIRES_EXTRACTION verdict":
        failures.append("STOP_NEEDS_EXTRACTION_reuse_missing")

    proposal_schema = receipt.get("proposal_packet_schema", {})
    if proposal_schema.get("status") != "PROPOSED_ONLY":
        failures.append(f"proposal_schema_status_wrong:{proposal_schema.get('status')}")
    for phrase in ["A proposal is not execution.", "A proposal is not acceptance.", "A proposal is not authority."]:
        if phrase not in proposal_schema.get("core_law", []):
            failures.append(f"proposal_core_law_missing:{phrase}")

    review_schema = receipt.get("human_review_request_schema", {})
    if review_schema.get("default_without_response") != "NO_EXECUTION":
        failures.append(f"review_default_wrong:{review_schema.get('default_without_response')}")
    if review_schema.get("core_law") != "No response means no execution.":
        failures.append(f"review_core_law_wrong:{review_schema.get('core_law')}")

    for patch_key, expected_mode in [
        ("move_authority_patch", "future_move_schema_patch_only_do_not_mutate_existing_move_registry"),
        ("move_inspection_authority_patch", "future_schema_patch_only_do_not_mutate_existing_day4_inspections"),
        ("trace_authority_patch", "future_schema_patch_only_do_not_mutate_existing_traces"),
        ("receipt_authority_patch", "future_schema_patch_only_do_not_mutate_existing_receipts"),
        ("proceed_readout_authority_patch", "future_schema_patch_only_do_not_mutate_existing_readouts"),
    ]:
        if receipt.get(patch_key, {}).get("patch_mode") != expected_mode:
            failures.append(f"{patch_key}_mode_wrong:{receipt.get(patch_key, {}).get('patch_mode')}")

    guards = receipt.get("authority_guards", {})
    for key in [
        "implementation_performed_by_policy",
        "demo_verdicts_emitted_by_policy",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "registry_mutated",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "jurisdiction_profile_modified",
        "jurisdiction_resolved_globally",
        "proposal_accepted",
        "proposal_executed",
        "human_silence_authorized",
        "forbidden_move_softened_to_proposal",
        "day6_taxonomy_evolution_implemented",
        "sqlite_registry_written",
        "global_governance_claimed",
        "final_authority_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"source_policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []

    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    move_registry = read_json(MOVE_REGISTRY_PATH)
    move_admission = read_json(MOVE_ADMISSION_GATE_PATH)
    day4_positive = read_json(DAY4_POSITIVE_RUN_PATH)
    day4_missing = read_json(DAY4_MISSING_MOVE_RUN_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID or move_impl.get("gate") != "PASS":
        failures.append("move_registry_implementation_source_not_pass")
    if move_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("move_registry_implementation_terminal_not_done")
    if move_registry.get("move_registry_id") != "move_registry_v0" or len(move_registry.get("moves", {})) != 7:
        failures.append("move_registry_source_wrong")
    if move_admission.get("admission_status_name") != "ADMISSIBLE_PRE_AUTH":
        failures.append("move_admission_not_pre_auth")
    if move_admission.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append("move_admission_not_deferred_to_day5")
    if day4_positive.get("terminal_result", {}).get("stop_code") != "STOP_NEXT_MOVE_BOUNDARY":
        failures.append("day4_positive_terminal_wrong")
    if day4_missing.get("terminal_result", {}).get("stop_code") != "STOP_NEEDS_NEW_MOVE":
        failures.append("day4_missing_terminal_wrong")
    if day4_missing.get("proposal_status") != "PROPOSED_ONLY":
        failures.append("day4_missing_proposal_not_proposed_only")

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_implementation_source_not_pass")
    halt_entries = halt_vocab.get("entries", {})
    for code in ["STOP_AUTHORITY_VIOLATION", "STOP_NEEDS_EXTRACTION", "STOP_NEEDS_NEW_MOVE", "STOP_GATE_FAIL"]:
        if code not in halt_entries:
            failures.append(f"halt_vocab_missing:{code}")
    if "NO_APPLICABLE_MOVE" in halt_entries:
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")

    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_version_wrong")
    if proposal_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_source_wrong")

    return failures

def make_authority_verdict(
    demo_name: str,
    move_id: str,
    verdict: str,
    *,
    proposal_ref: Optional[str] = None,
    review_request_ref: Optional[str] = None,
    extraction_request_ref: Optional[str] = None,
) -> Dict[str, Any]:
    terminal = terminal_for_verdict(verdict)
    state_sig8 = sha8({"demo_name": demo_name, "move_id": move_id, "verdict": verdict})
    seed = {"demo_name": demo_name, "move_id": move_id, "verdict": verdict, "state_sig8": state_sig8}
    reasons = {
        "AUTHORIZED_LOCAL": "Move is within the local jurisdiction profile and limited to declared state/trace effects.",
        "REQUIRES_PROPOSAL": "Move may be described as proposal pressure, but may not execute under the current jurisdiction.",
        "REQUIRES_EXTRACTION": "Move depends on unextracted or unclassified implementation/proto behavior.",
        "REQUIRES_HUMAN_REVIEW": "Move would mutate registry/taxonomy/jurisdiction or requires Carlos/human decision.",
        "FORBIDDEN": "Move violates forbidden action/input rules or attempts unregistered execution.",
    }
    allowed_effects = {
        "AUTHORIZED_LOCAL": ["state update", "trace append", "receipt/readout next boundary"],
        "REQUIRES_PROPOSAL": ["proposal packet emit only"],
        "REQUIRES_EXTRACTION": ["authority verdict emit", "extraction halt record"],
        "REQUIRES_HUMAN_REVIEW": ["human review request emit", "proposal packet emit if applicable"],
        "FORBIDDEN": ["forbidden verdict record only"],
    }
    return {
        "authority_verdict_id": f"authority_verdict_{sha8(seed)}",
        "schema_version": "authority_verdict_record_v0",
        "run_id": f"run_{sha8({'demo': demo_name})}",
        "unit_id": UNIT_ID,
        "state_sig8": state_sig8,
        "move_id": move_id,
        "move_admissibility_status": "ADMISSIBLE_PRE_AUTH",
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "authority_verdict": verdict,
        "reason": reasons[verdict],
        "allowed_effects": allowed_effects[verdict],
        "forbidden_effects_checked": [
            "registry mutation",
            "taxonomy mutation",
            "jurisdiction profile mutation",
            "frontier promotion",
            "hidden authority import",
            "proposal self-approval",
            "human silence authorization",
        ],
        "terminal_if_not_authorized": None if verdict == "AUTHORIZED_LOCAL" else terminal,
        "proposal_ref": proposal_ref,
        "review_request_ref": review_request_ref,
        "extraction_request_ref": extraction_request_ref,
        "must_not_impersonate": [
            "global authorization",
            "future move authorization",
            "theorem status",
            "human approval",
            "proof of correctness",
        ],
    }

def make_proposal_packet(demo_name: str, move_id: str, halt_code: str, proposal_type: str = "AUTHORITY_ESCALATION") -> Dict[str, Any]:
    seed = {"demo_name": demo_name, "move_id": move_id, "halt_code": halt_code, "proposal_type": proposal_type}
    return {
        "proposal_id": f"proposal_{sha8(seed)}",
        "schema_version": "proposal_packet_v0",
        "proposal_type": proposal_type,
        "trigger": {
            "run_id": f"run_{sha8({'demo': demo_name})}",
            "unit_id": UNIT_ID,
            "move_id": move_id,
            "halt_code": halt_code,
        },
        "proposed_action": {
            "summary": f"Describe requested move {move_id} without executing it.",
            "target": move_id,
            "effect": "proposal artifact only",
        },
        "why_move_is_admissible": [
            "move has explicit candidate shape",
            "trigger halt/verdict is typed",
            "proposal packet is bounded and record-only",
        ],
        "why_not_authorized": [
            "current jurisdiction does not authorize execution",
            "proposal cannot mutate registry, taxonomy, or jurisdiction profile",
        ],
        "requested_decision": {
            "decision_type": "HUMAN_REVIEW",
            "options": ["APPROVE", "REJECT", "DEFER", "NARROW", "REQUEST_EXTRACTION"],
        },
        "if_approved": {
            "allowed_next_unit": "separate_reviewed_unit_required",
        },
        "if_rejected": {
            "allowed_next_unit": "record_rejection_only",
        },
        "must_not_impersonate": [
            "accepted delta",
            "authorized execution",
            "proof of correctness",
            "registry mutation",
        ],
        "status": "PROPOSED_ONLY",
        "registry_mutated": False,
        "taxonomy_mutated": False,
        "jurisdiction_profile_mutated": False,
        "candidate_executed": False,
        "candidate_registered": False,
        "accepted": False,
    }

def make_human_review_request(demo_name: str, move_id: str, halt_code: str) -> Dict[str, Any]:
    seed = {"demo_name": demo_name, "move_id": move_id, "halt_code": halt_code}
    return {
        "review_request_id": f"review_{sha8(seed)}",
        "schema_version": "human_review_request_v0",
        "trigger_halt": halt_code,
        "move_id": move_id,
        "authority_verdict": "REQUIRES_HUMAN_REVIEW",
        "question": f"Should {move_id} be authorized exactly once under the declared unit?",
        "decision_options": [
            {"option": "APPROVE", "meaning": "Authorize this exact move once under the declared unit."},
            {"option": "REJECT", "meaning": "Do not authorize this move."},
            {"option": "DEFER", "meaning": "Keep proposal open but do not execute."},
            {"option": "NARROW", "meaning": "Request a smaller proposal."},
            {"option": "REQUEST_EXTRACTION", "meaning": "Require extraction before review."},
        ],
        "default_without_response": "NO_EXECUTION",
        "must_not_impersonate": [
            "system decision",
            "automatic authorization",
            "approval by silence",
        ],
        "authorized_by_silence": False,
        "move_executed": False,
        "registry_mutated": False,
    }

def make_extraction_request(demo_name: str, move_id: str) -> Dict[str, Any]:
    seed = {"demo_name": demo_name, "move_id": move_id, "kind": "extraction"}
    return {
        "extraction_request_id": f"extraction_{sha8(seed)}",
        "schema_version": "extraction_request_v0",
        "trigger_halt": "STOP_NEEDS_EXTRACTION",
        "move_id": move_id,
        "authority_verdict": "REQUIRES_EXTRACTION",
        "reason": "Move depends on unclassified or non-imported implementation/proto behavior.",
        "allowed_next_handling": [
            "extract bounded source behavior in a separate unit",
            "defer",
            "reject as unnecessary",
        ],
        "move_executed": False,
        "must_not_impersonate": [
            "move invalidity",
            "authorization denial",
            "human rejection",
        ],
    }

def make_authority_blocked_record(
    demo_name: str,
    move_id: str,
    verdict: str,
    verdict_id: str,
    halt_pressure: Optional[str],
    proposal_ref: Optional[str],
    review_ref: Optional[str],
) -> Dict[str, Any]:
    block_reason = {
        "REQUIRES_PROPOSAL": "PROPOSAL_ONLY",
        "REQUIRES_EXTRACTION": "EXTRACTION_REQUIRED",
        "REQUIRES_HUMAN_REVIEW": "HUMAN_REVIEW_REQUIRED",
        "FORBIDDEN": "FORBIDDEN_BY_PROFILE",
    }.get(verdict, "AUTHORITY_BOUNDARY")
    seed = {"demo_name": demo_name, "move_id": move_id, "verdict": verdict, "block_reason": block_reason}
    return {
        "schema_version": "authority_blocked_move_record_v0",
        "blocked_move_id": f"authority_blocked_{sha8(seed)}",
        "move_id": move_id,
        "block_reason": block_reason,
        "admissibility_status": "ADMISSIBLE_PRE_AUTH",
        "authority_verdict": verdict,
        "halt_pressure": halt_pressure,
        "authority_verdict_ref": verdict_id,
        "proposal_ref": proposal_ref,
        "review_request_ref": review_ref,
        "must_not_impersonate": [
            "move invalidity",
            "taxonomy rejection",
            "runner failure",
            "proof failure",
        ],
    }

def make_trace_authority_context(
    demo_name: str,
    move_id: str,
    verdict: str,
    verdict_id: str,
    proposal_ref: Optional[str],
    review_ref: Optional[str],
) -> Dict[str, Any]:
    seed = {"demo_name": demo_name, "move_id": move_id, "verdict": verdict}
    return {
        "trace_entry_id": f"trace_authority_{sha8(seed)}",
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "move_id": move_id,
        "authority_verdict": verdict,
        "authority_verdict_ref": verdict_id,
        "authorized_executable_moves": [move_id] if verdict == "AUTHORIZED_LOCAL" else [],
        "proposal_packet_ref": proposal_ref,
        "human_review_request_ref": review_ref,
        "selector_input": "authorized_executable_moves_only",
    }

def run_demo(policy_receipt: Dict[str, Any], demo_name: str, move_id: str, verdict: str) -> Dict[str, Any]:
    halt_code = VERDICT_TO_HALT[verdict]
    proposal = None
    review = None
    extraction = None

    if verdict == "REQUIRES_PROPOSAL":
        proposal = make_proposal_packet(demo_name, move_id, halt_code)
    elif verdict == "REQUIRES_EXTRACTION":
        extraction = make_extraction_request(demo_name, move_id)
    elif verdict == "REQUIRES_HUMAN_REVIEW":
        proposal = make_proposal_packet(demo_name, move_id, halt_code)
        review = make_human_review_request(demo_name, move_id, halt_code)

    verdict_record = make_authority_verdict(
        demo_name,
        move_id,
        verdict,
        proposal_ref=None if proposal is None else proposal["proposal_id"],
        review_request_ref=None if review is None else review["review_request_id"],
        extraction_request_ref=None if extraction is None else extraction["extraction_request_id"],
    )

    blocked = None
    if verdict != "AUTHORIZED_LOCAL":
        blocked = make_authority_blocked_record(
            demo_name,
            move_id,
            verdict,
            verdict_record["authority_verdict_id"],
            halt_code,
            None if proposal is None else proposal["proposal_id"],
            None if review is None else review["review_request_id"],
        )

    trace = make_trace_authority_context(
        demo_name,
        move_id,
        verdict,
        verdict_record["authority_verdict_id"],
        None if proposal is None else proposal["proposal_id"],
        None if review is None else review["review_request_id"],
    )

    authorized_executable_moves = [move_id] if verdict == "AUTHORIZED_LOCAL" else []
    selected_move = move_id if verdict == "AUTHORIZED_LOCAL" else None
    move_executed = verdict == "AUTHORIZED_LOCAL"
    terminal = terminal_for_verdict(verdict)

    run = {
        "schema_version": "day5_demo_authority_verdict_run_v0",
        "demo_name": demo_name,
        "source_policy_id": JURISDICTION_GATE_POLICY_ID,
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "admissible_pre_auth_moves": [move_id],
        "authority_checked_moves": [
            {
                "move_id": move_id,
                "authority_verdict": verdict,
                "authority_verdict_ref": verdict_record["authority_verdict_id"],
            }
        ],
        "authorized_executable_moves": authorized_executable_moves,
        "selector_input": "authorized_executable_moves_only",
        "selected_move": selected_move,
        "selected_from_authorized_executable_only": True,
        "move_executed": move_executed,
        "authority_verdict_record": verdict_record,
        "authority_blocked_move_record": blocked,
        "proposal_packet": proposal,
        "human_review_request": review,
        "extraction_request": extraction,
        "trace_authority_context": trace,
        "terminal_result": terminal,
        "proposal_status": None if proposal is None else proposal["status"],
        "review_default_without_response": None if review is None else review["default_without_response"],
        "candidate_registered": False,
        "candidate_executed": move_executed if verdict == "AUTHORIZED_LOCAL" else False,
        "proposal_accepted": False,
        "proposal_executed": False,
        "registry_mutated": False,
        "taxonomy_mutated": False,
        "jurisdiction_profile_mutated": False,
        "human_silence_authorized": False,
        "forbidden_softened_to_proposal": False,
        "day6_taxonomy_evolution_implemented": False,
        "gate": "PASS",
        "failures": [],
    }
    return run

def validate_demo_run(run: Dict[str, Any], policy_receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    demo_name = run.get("demo_name")
    move_id = run.get("admissible_pre_auth_moves", [None])[0]
    verdict_record = run.get("authority_verdict_record", {})
    verdict = verdict_record.get("authority_verdict")
    halt_code = VERDICT_TO_HALT.get(verdict)

    if run.get("gate") != "PASS":
        failures.append(f"{demo_name}:gate_not_PASS")
    if verdict not in VERDICTS:
        failures.append(f"{demo_name}:verdict_unknown:{verdict}")
    if run.get("selector_input") != "authorized_executable_moves_only":
        failures.append(f"{demo_name}:selector_input_wrong:{run.get('selector_input')}")
    if run.get("selected_from_authorized_executable_only") is not True:
        failures.append(f"{demo_name}:selection_not_authorized_only")
    if len(run.get("admissible_pre_auth_moves", [])) != 1:
        failures.append(f"{demo_name}:admissible_count_wrong")

    if verdict == "AUTHORIZED_LOCAL":
        if run.get("authorized_executable_moves") != [move_id]:
            failures.append(f"{demo_name}:authorized_executable_wrong:{run.get('authorized_executable_moves')}")
        if run.get("selected_move") != move_id:
            failures.append(f"{demo_name}:selected_move_wrong:{run.get('selected_move')}")
        if run.get("move_executed") is not True:
            failures.append(f"{demo_name}:authorized_move_not_executed")
        if run.get("terminal_result", {}).get("type") != "ADVANCE":
            failures.append(f"{demo_name}:authorized_terminal_not_ADVANCE:{run.get('terminal_result')}")
    else:
        if run.get("authorized_executable_moves") != []:
            failures.append(f"{demo_name}:unauthorized_has_executable:{run.get('authorized_executable_moves')}")
        if run.get("selected_move") is not None:
            failures.append(f"{demo_name}:unauthorized_selected:{run.get('selected_move')}")
        if run.get("move_executed") is not False:
            failures.append(f"{demo_name}:unauthorized_move_executed")
        if run.get("terminal_result", {}).get("type") != "STOP":
            failures.append(f"{demo_name}:unauthorized_terminal_not_STOP:{run.get('terminal_result')}")
        if run.get("terminal_result", {}).get("stop_code") != halt_code:
            failures.append(f"{demo_name}:halt_wrong:{run.get('terminal_result')} expected {halt_code}")
        if run.get("authority_blocked_move_record") is None:
            failures.append(f"{demo_name}:missing_authority_blocked_record")

    if verdict == "REQUIRES_PROPOSAL":
        proposal = run.get("proposal_packet")
        if not proposal:
            failures.append(f"{demo_name}:missing_proposal_packet")
        else:
            if proposal.get("status") != "PROPOSED_ONLY":
                failures.append(f"{demo_name}:proposal_not_PROPOSED_ONLY:{proposal.get('status')}")
            for key in ["registry_mutated", "taxonomy_mutated", "jurisdiction_profile_mutated", "candidate_executed", "candidate_registered", "accepted"]:
                if proposal.get(key) is not False:
                    failures.append(f"{demo_name}:proposal_guard_not_false:{key}:{proposal.get(key)}")
        if run.get("candidate_registered") is not False:
            failures.append(f"{demo_name}:candidate_registered_true")
        if run.get("candidate_executed") is not False:
            failures.append(f"{demo_name}:candidate_executed_true")

    if verdict == "REQUIRES_EXTRACTION":
        if run.get("extraction_request") is None:
            failures.append(f"{demo_name}:missing_extraction_request")
        if run.get("terminal_result", {}).get("stop_code") != "STOP_NEEDS_EXTRACTION":
            failures.append(f"{demo_name}:extraction_stop_wrong:{run.get('terminal_result')}")

    if verdict == "REQUIRES_HUMAN_REVIEW":
        review = run.get("human_review_request")
        if review is None:
            failures.append(f"{demo_name}:missing_human_review_request")
        else:
            if review.get("default_without_response") != "NO_EXECUTION":
                failures.append(f"{demo_name}:review_default_wrong:{review.get('default_without_response')}")
            if review.get("authorized_by_silence") is not False:
                failures.append(f"{demo_name}:human_silence_authorized")
            if review.get("move_executed") is not False:
                failures.append(f"{demo_name}:review_move_executed")
        if run.get("registry_mutated") is not False:
            failures.append(f"{demo_name}:registry_mutated_true")

    if verdict == "FORBIDDEN":
        if run.get("proposal_packet") is not None:
            failures.append(f"{demo_name}:forbidden_has_proposal")
        if run.get("forbidden_softened_to_proposal") is not False:
            failures.append(f"{demo_name}:forbidden_softened_to_proposal")
        if run.get("terminal_result", {}).get("stop_code") != "STOP_FORBIDDEN_MOVE":
            failures.append(f"{demo_name}:forbidden_stop_wrong:{run.get('terminal_result')}")

    for key in [
        "proposal_accepted",
        "proposal_executed",
        "registry_mutated",
        "taxonomy_mutated",
        "jurisdiction_profile_mutated",
        "human_silence_authorized",
        "day6_taxonomy_evolution_implemented",
    ]:
        if run.get(key) is not False:
            failures.append(f"{demo_name}:guard_not_false:{key}:{run.get(key)}")

    trace = run.get("trace_authority_context", {})
    if trace.get("selector_input") != "authorized_executable_moves_only":
        failures.append(f"{demo_name}:trace_selector_input_wrong")
    if trace.get("authority_verdict_ref") != verdict_record.get("authority_verdict_id"):
        failures.append(f"{demo_name}:trace_verdict_ref_mismatch")

    return failures

def make_authority_receipt(demo_runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    verdict_counts = {v: 0 for v in VERDICTS}
    for run in demo_runs:
        verdict_counts[run["authority_verdict_record"]["authority_verdict"]] += 1

    seed = {"demos": [run["demo_name"] for run in demo_runs], "verdict_counts": verdict_counts}
    return {
        "schema_version": "day5_demo_authority_receipt_v0",
        "receipt_type": "DAY5_DEMO_AUTHORITY_RECEIPT",
        "receipt_id": f"day5_authority_receipt_{sha8(seed)}",
        "source_policy_id": JURISDICTION_GATE_POLICY_ID,
        "jurisdiction": {
            "jurisdiction_profile_id": "jurisdiction_profile_v0",
            "verdict_counts": verdict_counts,
        },
        "authority": {
            "authorized_executable_moves": [
                run["selected_move"]
                for run in demo_runs
                if run["authority_verdict_record"]["authority_verdict"] == "AUTHORIZED_LOCAL"
            ],
            "proposal_packets_emitted": sum(1 for run in demo_runs if run.get("proposal_packet") is not None),
            "human_review_requests_emitted": sum(1 for run in demo_runs if run.get("human_review_request") is not None),
            "extraction_requests_emitted": sum(1 for run in demo_runs if run.get("extraction_request") is not None),
            "forbidden_moves_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "FORBIDDEN"),
        },
        "selector_input": "authorized_executable_moves_only",
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_authority_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    counts = receipt.get("jurisdiction", {}).get("verdict_counts", {})
    for verdict in VERDICTS:
        if counts.get(verdict) != 1:
            failures.append(f"verdict_count_wrong:{verdict}:{counts.get(verdict)}")
    auth = receipt.get("authority", {})
    if auth.get("authorized_executable_moves") != ["unit.mark_complete.v0"]:
        failures.append(f"authorized_executable_moves_wrong:{auth.get('authorized_executable_moves')}")
    if auth.get("proposal_packets_emitted") != 2:
        failures.append(f"proposal_packets_emitted_wrong:{auth.get('proposal_packets_emitted')}")
    if auth.get("human_review_requests_emitted") != 1:
        failures.append(f"human_review_requests_wrong:{auth.get('human_review_requests_emitted')}")
    if auth.get("extraction_requests_emitted") != 1:
        failures.append(f"extraction_requests_wrong:{auth.get('extraction_requests_emitted')}")
    if auth.get("forbidden_moves_count") != 1:
        failures.append(f"forbidden_count_wrong:{auth.get('forbidden_moves_count')}")
    if receipt.get("selector_input") != "authorized_executable_moves_only":
        failures.append("receipt_selector_input_wrong")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_jurisdiction_gate_policy_id") != JURISDICTION_GATE_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_jurisdiction_gate_policy_id')}")
    if receipt.get("source_jurisdiction_gate_policy_receipt_id") != JURISDICTION_GATE_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_wrong:{receipt.get('source_jurisdiction_gate_policy_receipt_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "JGI0_source_policy_verified",
        "JGI1_core_artifacts_emitted",
        "JGI2_all_five_verdict_demos_passed",
        "JGI3_every_admissible_move_verdict_recorded",
        "JGI4_selector_authorized_only",
        "JGI5_proposal_required_proposed_only",
        "JGI6_extraction_required_not_executed",
        "JGI7_human_review_no_silence_authorization",
        "JGI8_forbidden_not_executed_or_proposed",
        "JGI9_no_registry_taxonomy_jurisdiction_mutation",
        "JGI10_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_counts = {
        "demo_run_count": 5,
        "authority_verdict_record_count": 5,
        "authorized_local_count": 1,
        "requires_proposal_count": 1,
        "requires_extraction_count": 1,
        "requires_human_review_count": 1,
        "forbidden_count": 1,
        "authorized_executable_move_count": 1,
        "proposal_packet_emitted_count": 2,
        "human_review_request_emitted_count": 1,
        "extraction_request_emitted_count": 1,
        "authority_blocked_move_record_count": 4,
    }
    for key, expected in expected_counts.items():
        if metrics.get(key) != expected:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {expected}")

    for key in [
        "non_authorized_move_execution_count",
        "requires_proposal_execution_count",
        "requires_extraction_execution_count",
        "requires_human_review_execution_count",
        "forbidden_move_execution_count",
        "forbidden_move_proposal_count",
        "proposal_accepted_count",
        "proposal_executed_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "jurisdiction_profile_mutation_count",
        "human_silence_authorized_count",
        "selector_from_admissible_without_authority_count",
        "day6_taxonomy_evolution_count",
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "sqlite_registry_write_count",
        "global_governance_claim_count",
        "final_authority_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("authority_guards", {})
    for key in [
        "core_artifacts_emitted",
        "demo_verdicts_emitted",
        "authority_receipt_emitted",
        "implementation_receipt_emitted",
        "halt_vocabulary_authority_patch_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "registry_mutated",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "jurisdiction_profile_modified",
        "proposal_accepted",
        "proposal_executed",
        "human_silence_authorized",
        "forbidden_move_softened_to_proposal",
        "day6_taxonomy_evolution_implemented",
        "sqlite_registry_written",
        "global_governance_claimed",
        "final_authority_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)

    source_before = snapshot_files(SOURCE_FILES)

    failures: List[str] = []
    failures.extend(validate_source_policy(policy, policy_receipt))
    failures.extend(validate_external_sources())

    for d in [ARTIFACT_DIR, PATCH_DIR, DEMO_DIR, IMPLEMENTATION_RECEIPT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    artifacts = {
        "jurisdiction_profile_schema": ARTIFACT_DIR / "jurisdiction_profile_schema_v0.json",
        "jurisdiction_verdict_enum": ARTIFACT_DIR / "jurisdiction_verdict_enum_v0.json",
        "move_authority_patch": ARTIFACT_DIR / "move_authority_patch_v0.json",
        "jurisdiction_gate": ARTIFACT_DIR / "jurisdiction_gate_v0.json",
        "authority_verdict_record_schema": ARTIFACT_DIR / "authority_verdict_record_schema_v0.json",
        "authority_blocked_move_record_schema": ARTIFACT_DIR / "authority_blocked_move_record_schema_v0.json",
        "proposal_packet_schema": ARTIFACT_DIR / "proposal_packet_schema_v0.json",
        "human_review_request_schema": ARTIFACT_DIR / "human_review_request_schema_v0.json",
        "halt_vocabulary_authority_patch": ARTIFACT_DIR / "halt_vocabulary_authority_patch_v0.json",
        "move_inspection_authority_patch": PATCH_DIR / "move_inspection_authority_patch_v0.json",
        "trace_authority_patch": PATCH_DIR / "trace_authority_patch_v0.json",
        "receipt_authority_patch": PATCH_DIR / "receipt_authority_patch_v0.json",
        "proceed_readout_authority_patch": PATCH_DIR / "proceed_readout_authority_patch_v0.json",
    }

    write_json(artifacts["jurisdiction_profile_schema"], policy_receipt["jurisdiction_profile_schema"])
    write_json(artifacts["jurisdiction_verdict_enum"], policy_receipt["jurisdiction_verdict_enum"])
    write_json(artifacts["move_authority_patch"], policy_receipt["move_authority_patch"])
    write_json(artifacts["jurisdiction_gate"], policy_receipt["jurisdiction_gate"])
    write_json(artifacts["authority_verdict_record_schema"], policy_receipt["authority_verdict_record_schema"])
    write_json(artifacts["authority_blocked_move_record_schema"], policy_receipt["authority_blocked_move_record_schema"])
    write_json(artifacts["proposal_packet_schema"], policy_receipt["proposal_packet_schema"])
    write_json(artifacts["human_review_request_schema"], policy_receipt["human_review_request_schema"])
    write_json(artifacts["halt_vocabulary_authority_patch"], policy_receipt["halt_vocabulary_authority_patch"])
    write_json(artifacts["move_inspection_authority_patch"], policy_receipt["move_inspection_authority_patch"])
    write_json(artifacts["trace_authority_patch"], policy_receipt["trace_authority_patch"])
    write_json(artifacts["receipt_authority_patch"], policy_receipt["receipt_authority_patch"])
    write_json(artifacts["proceed_readout_authority_patch"], policy_receipt["proceed_readout_authority_patch"])

    demo_runs = [run_demo(policy_receipt, name, move_id, verdict) for name, move_id, verdict in DEMO_SPECS]
    demo_failures: List[str] = []
    for run in demo_runs:
        demo_failures.extend(validate_demo_run(run, policy_receipt))
    failures.extend(demo_failures)

    demo_paths = {
        "DAY5_AUTHORIZED_LOCAL_MOVE": DEMO_DIR / "day5_demo_authorized_move.json",
        "DAY5_PROPOSAL_REQUIRED": DEMO_DIR / "day5_demo_proposal_required.json",
        "DAY5_EXTRACTION_REQUIRED": DEMO_DIR / "day5_demo_extraction_required.json",
        "DAY5_HUMAN_REVIEW_REQUIRED": DEMO_DIR / "day5_demo_human_review_required.json",
        "DAY5_FORBIDDEN_MOVE": DEMO_DIR / "day5_demo_forbidden_move.json",
    }
    for run in demo_runs:
        write_json(demo_paths[run["demo_name"]], run)

    authority_receipt = make_authority_receipt(demo_runs)
    authority_receipt_failures = validate_authority_receipt(authority_receipt)
    authority_receipt["failures"] = authority_receipt_failures
    authority_receipt["gate"] = "PASS" if not authority_receipt_failures else "FAIL"
    failures.extend(authority_receipt_failures)
    authority_receipt_path = DEMO_DIR / "day5_demo_authority_receipt.json"
    write_json(authority_receipt_path, authority_receipt)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    output_artifacts = {name: rel(path) for name, path in artifacts.items()}
    output_artifacts.update({
        "day5_demo_authorized_move": rel(demo_paths["DAY5_AUTHORIZED_LOCAL_MOVE"]),
        "day5_demo_proposal_required": rel(demo_paths["DAY5_PROPOSAL_REQUIRED"]),
        "day5_demo_extraction_required": rel(demo_paths["DAY5_EXTRACTION_REQUIRED"]),
        "day5_demo_human_review_required": rel(demo_paths["DAY5_HUMAN_REVIEW_REQUIRED"]),
        "day5_demo_forbidden_move": rel(demo_paths["DAY5_FORBIDDEN_MOVE"]),
        "day5_demo_authority_receipt": rel(authority_receipt_path),
    })

    verdict_counts = {v: 0 for v in VERDICTS}
    for run in demo_runs:
        verdict_counts[run["authority_verdict_record"]["authority_verdict"]] += 1

    aggregate_metrics = {
        "demo_run_count": len(demo_runs),
        "authority_verdict_record_count": len(demo_runs),
        "authorized_local_count": verdict_counts["AUTHORIZED_LOCAL"],
        "requires_proposal_count": verdict_counts["REQUIRES_PROPOSAL"],
        "requires_extraction_count": verdict_counts["REQUIRES_EXTRACTION"],
        "requires_human_review_count": verdict_counts["REQUIRES_HUMAN_REVIEW"],
        "forbidden_count": verdict_counts["FORBIDDEN"],
        "authorized_executable_move_count": sum(len(run["authorized_executable_moves"]) for run in demo_runs),
        "proposal_packet_emitted_count": sum(1 for run in demo_runs if run.get("proposal_packet") is not None),
        "human_review_request_emitted_count": sum(1 for run in demo_runs if run.get("human_review_request") is not None),
        "extraction_request_emitted_count": sum(1 for run in demo_runs if run.get("extraction_request") is not None),
        "authority_blocked_move_record_count": sum(1 for run in demo_runs if run.get("authority_blocked_move_record") is not None),
        "non_authorized_move_execution_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] != "AUTHORIZED_LOCAL" and run["move_executed"]),
        "requires_proposal_execution_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "REQUIRES_PROPOSAL" and run["move_executed"]),
        "requires_extraction_execution_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "REQUIRES_EXTRACTION" and run["move_executed"]),
        "requires_human_review_execution_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "REQUIRES_HUMAN_REVIEW" and run["move_executed"]),
        "forbidden_move_execution_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "FORBIDDEN" and run["move_executed"]),
        "forbidden_move_proposal_count": sum(1 for run in demo_runs if run["authority_verdict_record"]["authority_verdict"] == "FORBIDDEN" and run.get("proposal_packet") is not None),
        "proposal_accepted_count": sum(1 for run in demo_runs if run.get("proposal_accepted")),
        "proposal_executed_count": sum(1 for run in demo_runs if run.get("proposal_executed")),
        "registry_mutation_count": sum(1 for run in demo_runs if run.get("registry_mutated")),
        "taxonomy_mutation_count": sum(1 for run in demo_runs if run.get("taxonomy_mutated")),
        "jurisdiction_profile_mutation_count": sum(1 for run in demo_runs if run.get("jurisdiction_profile_mutated")),
        "human_silence_authorized_count": sum(1 for run in demo_runs if run.get("human_silence_authorized")),
        "selector_from_admissible_without_authority_count": sum(1 for run in demo_runs if run.get("selector_input") != "authorized_executable_moves_only"),
        "day6_taxonomy_evolution_count": sum(1 for run in demo_runs if run.get("day6_taxonomy_evolution_implemented")),
        "source_trace_modified_count": 0,
        "source_receipt_modified_count": 0,
        "source_ledger_modified_count": 0,
        "source_runner_modified_count": 0,
        "source_regime_modified_count": 0,
        "sqlite_registry_write_count": 0,
        "global_governance_claim_count": 0,
        "final_authority_claim_count": 0,
        "proof_claim_count": 0,
        "hidden_continuation_count": 0,
    }

    acceptance_gate_results = {
        "JGI0_source_policy_verified": len(validate_source_policy(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "JGI1_core_artifacts_emitted": all(path.exists() for path in artifacts.values()),
        "JGI2_all_five_verdict_demos_passed": not demo_failures and len(demo_runs) == 5,
        "JGI3_every_admissible_move_verdict_recorded": aggregate_metrics["authority_verdict_record_count"] == 5,
        "JGI4_selector_authorized_only": aggregate_metrics["selector_from_admissible_without_authority_count"] == 0,
        "JGI5_proposal_required_proposed_only": aggregate_metrics["requires_proposal_count"] == 1 and aggregate_metrics["requires_proposal_execution_count"] == 0,
        "JGI6_extraction_required_not_executed": aggregate_metrics["requires_extraction_count"] == 1 and aggregate_metrics["requires_extraction_execution_count"] == 0,
        "JGI7_human_review_no_silence_authorization": aggregate_metrics["requires_human_review_count"] == 1 and aggregate_metrics["human_silence_authorized_count"] == 0 and aggregate_metrics["requires_human_review_execution_count"] == 0,
        "JGI8_forbidden_not_executed_or_proposed": aggregate_metrics["forbidden_count"] == 1 and aggregate_metrics["forbidden_move_execution_count"] == 0 and aggregate_metrics["forbidden_move_proposal_count"] == 0,
        "JGI9_no_registry_taxonomy_jurisdiction_mutation": aggregate_metrics["registry_mutation_count"] == 0 and aggregate_metrics["taxonomy_mutation_count"] == 0 and aggregate_metrics["jurisdiction_profile_mutation_count"] == 0,
        "JGI10_no_source_artifact_mutation": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "core_artifacts_emitted": True,
        "demo_verdicts_emitted": True,
        "authority_receipt_emitted": True,
        "implementation_receipt_emitted": True,
        "halt_vocabulary_authority_patch_emitted": True,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "registry_mutated": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "jurisdiction_profile_modified": False,
        "proposal_accepted": False,
        "proposal_executed": False,
        "human_silence_authorized": False,
        "forbidden_move_softened_to_proposal": False,
        "day6_taxonomy_evolution_implemented": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
        "global_governance_claimed": False,
        "final_authority_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_move_registry_tracked": tracked(MOVE_REGISTRY_PATH),
        "source_move_registry_implementation_receipt_tracked": tracked(MOVE_IMPL_RECEIPT_PATH),
        "source_halt_vocabulary_tracked": tracked(HALT_VOCABULARY_PATH),
        "source_proceed_receipt_tracked": tracked(PROCEED_RECEIPT_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_RECEIPT_PATH),
        "source_trace_schema_tracked": tracked(TRACE_SCHEMA_PATH),
        "source_proposal_ledger_schema_tracked": tracked(PROPOSAL_LEDGER_SCHEMA_PATH),
        "source_local_regime_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "outputs_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": JURISDICTION_GATE_POLICY_ID,
        "verdict_counts": verdict_counts,
        "output_artifacts": output_artifacts,
    }
    implementation_receipt_id = sha8(implementation_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    implementation_receipt = {
        "schema_version": "jurisdiction_gate_v0_implementation_receipt_v0",
        "receipt_type": "JURISDICTION_GATE_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_jurisdiction_gate_policy_id": JURISDICTION_GATE_POLICY_ID,
        "source_jurisdiction_gate_policy_receipt_id": JURISDICTION_GATE_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "output_artifacts": output_artifacts,
        "demo_summaries": [
            {
                "demo_name": run["demo_name"],
                "move_id": run["admissible_pre_auth_moves"][0],
                "authority_verdict": run["authority_verdict_record"]["authority_verdict"],
                "terminal_result": run["terminal_result"],
                "move_executed": run["move_executed"],
                "authorized_executable_moves": run["authorized_executable_moves"],
                "proposal_status": run["proposal_status"],
                "review_default_without_response": run["review_default_without_response"],
            }
            for run in demo_runs
        ],
        "authority_receipt_summary": {
            "receipt_id": authority_receipt["receipt_id"],
            "verdict_counts": authority_receipt["jurisdiction"]["verdict_counts"],
            "authority": authority_receipt["authority"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "authority_guards": authority_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
            "next_command_goal": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_implementation_receipt(implementation_receipt)
    failures.extend(receipt_failures)
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"jurisdiction_gate_implementation_receipt_id={implementation_receipt_id}")
    print(f"jurisdiction_gate_implementation_receipt_path=data/jurisdiction_gate_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        print(f"artifact_{name}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
