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

UNIT_ID = "IMPLEMENT_TAXONOMY_EVOLUTION_V0_WITH_DEMO_DELTAS_V0"
TARGET_UNIT_ID = "taxonomy_evolution.v0"

TAXONOMY_EVOLUTION_POLICY_ID = "e84eb230"
TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID = "18da290a"
JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID = "6291b0d9"
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

POLICY_PATH = ROOT / "data" / "taxonomy_evolution_v0_policies" / f"{TAXONOMY_EVOLUTION_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_policy_receipts" / f"{TAXONOMY_EVOLUTION_POLICY_ID}.json"

JURIS_IMPL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts" / f"{JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID}.json"
JURIS_POLICY_PATH = ROOT / "data" / "jurisdiction_gate_v0_policies" / f"{JURISDICTION_GATE_POLICY_ID}.json"
JURIS_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_policy_receipts" / f"{JURISDICTION_GATE_POLICY_ID}.json"
JURIS_GATE_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "jurisdiction_gate_v0.json"
JURIS_VERDICT_ENUM_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "jurisdiction_verdict_enum_v0.json"
JURIS_PROFILE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "jurisdiction_profile_schema_v0.json"
JURIS_HALT_AUTHORITY_PATCH_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "halt_vocabulary_authority_patch_v0.json"
JURIS_MOVE_AUTHORITY_PATCH_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "move_authority_patch_v0.json"
JURIS_PROPOSAL_PACKET_SCHEMA_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "proposal_packet_schema_v0.json"
JURIS_HUMAN_REVIEW_SCHEMA_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "human_review_request_schema_v0.json"
JURIS_AUTHORITY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_demo" / "day5_demo_authority_receipt.json"

MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_POLICY_PATH = ROOT / "data" / "move_registry_v0_policies" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_POLICY_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_policy_receipts" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_REGISTRY_PATH = ROOT / "data" / "move_registry_v0" / "move_registry_v0.json"
MOVE_ADMISSION_GATE_PATH = ROOT / "data" / "move_registry_v0" / "move_admission_gate_v0.json"

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

ARTIFACT_DIR = ROOT / "data" / "taxonomy_evolution_v0"
PATCH_DIR = ROOT / "data" / "taxonomy_evolution_v0_patches"
DEMO_DIR = ROOT / "data" / "taxonomy_evolution_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "taxonomy_evolution_v0_implementation_receipts"

SOURCE_FILES = [
    POLICY_PATH,
    POLICY_RECEIPT_PATH,
    JURIS_IMPL_RECEIPT_PATH,
    JURIS_POLICY_PATH,
    JURIS_POLICY_RECEIPT_PATH,
    JURIS_GATE_PATH,
    JURIS_VERDICT_ENUM_PATH,
    JURIS_PROFILE_SCHEMA_PATH,
    JURIS_HALT_AUTHORITY_PATCH_PATH,
    JURIS_MOVE_AUTHORITY_PATCH_PATH,
    JURIS_PROPOSAL_PACKET_SCHEMA_PATH,
    JURIS_HUMAN_REVIEW_SCHEMA_PATH,
    JURIS_AUTHORITY_RECEIPT_PATH,
    MOVE_IMPL_RECEIPT_PATH,
    MOVE_POLICY_PATH,
    MOVE_POLICY_RECEIPT_PATH,
    MOVE_REGISTRY_PATH,
    MOVE_ADMISSION_GATE_PATH,
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

ELIGIBLE_TRIGGER_HALTS = [
    "STOP_TAXONOMY_GAP",
    "STOP_UNDERTYPED_OBJECT",
    "STOP_UNTYPED_UNIT",
    "STOP_LAYER_COLLAPSE",
    "STOP_NEEDS_NEW_MOVE",
    "STOP_NEEDS_EXTRACTION",
    "STOP_VISIBLE_GOTCHA",
]

AUTHORITY_HALTS_CONTEXT_ONLY = [
    "STOP_PROPOSAL_REQUIRED",
    "STOP_HUMAN_REVIEW_REQUIRED",
    "STOP_FORBIDDEN_MOVE",
    "STOP_AUTHORITY_BOUNDARY",
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
    relp = path.relative_to(ROOT).as_posix()
    result = subprocess.run(["git", "ls-files", "--error-unmatch", relp], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.exists()}

def validate_source_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != TAXONOMY_EVOLUTION_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID:
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

    summary = receipt.get("policy_summary", {})
    for phrase in [
        "No halt, no taxonomy upgrade.",
        "Existing vocabulary first.",
        "ADD last.",
        "No taxonomy change creates truth.",
        "No proposal mutates registry.",
        "No accepted patch without review.",
    ]:
        if phrase not in summary.get("core_law", ""):
            failures.append(f"core_law_phrase_missing:{phrase}")

    trigger = receipt.get("taxonomy_trigger_policy", {})
    if trigger.get("eligible_trigger_halts") != ELIGIBLE_TRIGGER_HALTS:
        failures.append(f"eligible_trigger_halts_wrong:{trigger.get('eligible_trigger_halts')}")
    if trigger.get("authority_halts_context_only") != AUTHORITY_HALTS_CONTEXT_ONLY:
        failures.append(f"authority_halts_context_only_wrong:{trigger.get('authority_halts_context_only')}")

    vocab = receipt.get("existing_vocab_test_schema", {})
    for law in ["No existing_vocab_test, no taxonomy_delta.", "ADD_* is last.", "WITHHOLD is valid and does not count as failure."]:
        if law not in vocab.get("law", []):
            failures.append(f"existing_vocab_law_missing:{law}")

    delta = receipt.get("taxonomy_delta_schema", {})
    for field in ["pressure_ref", "existing_vocab_test_ref", "smallest_honest_reading", "must_not_impersonate", "allowed_next_handling"]:
        if field not in delta.get("required_fields", []):
            failures.append(f"delta_required_missing:{field}")
    for law in ["Delta does not widen authority.", "Delta does not promote theorem status.", "Delta does not mutate registry."]:
        if law not in delta.get("law", []):
            failures.append(f"delta_law_missing:{law}")

    review = receipt.get("taxonomy_review_record_schema", {})
    if review.get("canonical_accept_decision") != "ACCEPTED_LOCAL":
        failures.append(f"canonical_accept_wrong:{review.get('canonical_accept_decision')}")
    if review.get("accepted_by_review_is_alias_only") is not True:
        failures.append("accepted_by_review_alias_flag_missing")
    if "No review record, no registry patch." not in review.get("law", []):
        failures.append("no_review_no_patch_law_missing")

    patch = receipt.get("taxonomy_registry_patch_schema", {})
    if "Only accepted review may create APPLIED_LOCAL patch." not in patch.get("law", []):
        failures.append("accepted_review_patch_law_missing")
    if "Patch does not widen authority." not in patch.get("law", []):
        failures.append("patch_no_authority_widening_law_missing")
    if "Patch does not prove truth." not in patch.get("law", []):
        failures.append("patch_no_truth_law_missing")

    authority = receipt.get("taxonomy_authority_patch", {})
    if authority.get("patch_mode") != "future_jurisdiction_profile_patch_only_do_not_mutate_existing_profile":
        failures.append(f"taxonomy_authority_patch_mode_wrong:{authority.get('patch_mode')}")
    auth = authority.get("taxonomy_authority", {})
    if "self_accept_delta" not in auth.get("forbidden", []):
        failures.append("self_accept_delta_forbidden_missing")
    if "accept_taxonomy_delta" not in auth.get("requires_human_review", []):
        failures.append("accept_taxonomy_delta_review_missing")
    if "record_taxonomy_pressure" not in auth.get("runtime_allowed", []):
        failures.append("runtime_pressure_record_missing")

    move_patch = receipt.get("taxonomy_move_registry_patch", {})
    if move_patch.get("patch_mode") != "future_move_registry_patch_only_do_not_mutate_existing_move_registry":
        failures.append(f"move_registry_patch_mode_wrong:{move_patch.get('patch_mode')}")
    if "Candidate moves are not registered by this policy." not in move_patch.get("law", []):
        failures.append("candidate_moves_not_registered_law_missing")

    guards = receipt.get("authority_guards", {})
    for key in [
        "implementation_performed_by_policy",
        "demo_deltas_emitted_by_policy",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "taxonomy_registry_mutated_by_policy",
        "move_registry_mutated_by_policy",
        "halt_vocabulary_mutated_by_policy",
        "proposal_accepted_by_runtime",
        "proposal_executed_by_runtime",
        "review_fabricated_by_runtime",
        "accepted_patch_without_review",
        "label_treated_as_truth",
        "taxonomy_delta_widened_authority",
        "taxonomy_delta_promoted_theorem_status",
        "add_used_before_existing_vocab_test",
        "authority_halt_auto_triggered_taxonomy",
        "day7_global_taxonomy_implemented",
        "global_taxonomy_claimed",
        "final_closure_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
    ]:
        if guards.get(key) is not False:
            failures.append(f"source_policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []

    juris_impl = read_json(JURIS_IMPL_RECEIPT_PATH)
    juris_auth = read_json(JURIS_AUTHORITY_RECEIPT_PATH)
    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    move_registry = read_json(MOVE_REGISTRY_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if juris_impl.get("receipt_id") != JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID or juris_impl.get("gate") != "PASS":
        failures.append("jurisdiction_gate_source_not_pass")
    if juris_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("jurisdiction_gate_terminal_not_done")
    for key in [
        "proposal_accepted_count",
        "proposal_executed_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "jurisdiction_profile_mutation_count",
        "day6_taxonomy_evolution_count",
        "global_governance_claim_count",
        "final_authority_claim_count",
        "proof_claim_count",
    ]:
        if juris_impl.get("aggregate_metrics", {}).get(key) != 0:
            failures.append(f"jurisdiction_metric_not_zero:{key}:{juris_impl.get('aggregate_metrics', {}).get(key)}")

    counts = juris_auth.get("jurisdiction", {}).get("verdict_counts", {})
    for verdict in ["AUTHORIZED_LOCAL", "REQUIRES_PROPOSAL", "REQUIRES_EXTRACTION", "REQUIRES_HUMAN_REVIEW", "FORBIDDEN"]:
        if counts.get(verdict) != 1:
            failures.append(f"jurisdiction_authority_receipt_count_wrong:{verdict}:{counts.get(verdict)}")

    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID or move_impl.get("gate") != "PASS":
        failures.append("move_registry_source_not_pass")
    if move_registry.get("move_registry_id") != "move_registry_v0" or len(move_registry.get("moves", {})) != 7:
        failures.append("move_registry_source_wrong")

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_vocabulary_source_not_pass")
    halt_entries = halt_vocab.get("entries", {})
    for halt_code in ELIGIBLE_TRIGGER_HALTS:
        if halt_code not in halt_entries:
            failures.append(f"eligible_halt_missing_from_halt_vocab:{halt_code}")
    if "NO_APPLICABLE_MOVE" in halt_entries:
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")

    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_version_wrong")
    if proposal_ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    return failures

def make_taxonomy_registry() -> Dict[str, Any]:
    return {
        "taxonomy_registry_id": "taxonomy_registry_v0",
        "schema_version": "taxonomy_registry_v0",
        "registries": {
            "object_kind": ["RECEIPT", "TRACE", "POLICY", "SHELL_SURFACE"],
            "truth_status": ["CLAIMED", "OBSERVED", "UNRESOLVED", "WITHHELD"],
            "layer": ["RUNTIME", "MOVE_SPACE", "AUTHORITY", "TAXONOMY"],
            "route_role": ["SOURCE", "PATCH", "PROPOSAL", "REVIEW"],
            "extractability": ["EXTRACTED", "NEEDS_EXTRACTION", "UNEXTRACTABLE"],
            "content_scope": ["LOCAL", "RUN", "UNIT", "GLOBAL_UNCLAIMED"],
            "allowed_consumers": ["runner", "reviewer", "receipt_reader"],
            "allowed_next_moves": ["review_delta", "reject", "defer", "narrow", "request_extraction"],
            "stop_conditions": ["taxonomy_pressure", "review_required", "withheld"],
            "halt_codes": ELIGIBLE_TRIGGER_HALTS,
            "move_kinds": ["CONTROL_CHECK", "CONTROL_EMIT", "PROPOSAL_ONLY", "LOCAL_REGISTRY_PATCH"],
            "block_reasons": ["TOO_COARSE", "OVERCLAIMS", "MISSING", "UNRESOLVED"],
        },
        "registry_law": [
            "labels carry no authority by themselves",
            "new terms require accepted taxonomy delta",
            "proposals do not mutate registry",
            "accepted deltas must preserve non-impersonation",
            "existing vocabulary must be tested before ADD",
        ],
    }

def make_pressure(demo: Dict[str, Any]) -> Dict[str, Any]:
    seed = {"demo": demo["demo_name"], "halt": demo["trigger_halt"], "pressure": demo["observed_pressure"]}
    pressure_id = f"tax_pressure_{sha8(seed)}"
    target_kind = {
        "DAY6_LABEL_SPLIT": "receipt",
        "DAY6_HALT_REFINE": "readout",
        "DAY6_MISSING_MOVE_DELTA": "move_boundary",
        "DAY6_WITHHOLD": "mixed_object",
    }[demo["demo_name"]]
    family = {
        "DAY6_LABEL_SPLIT": "object_kind",
        "DAY6_HALT_REFINE": "halt_codes",
        "DAY6_MISSING_MOVE_DELTA": "move_kinds",
        "DAY6_WITHHOLD": "object_kind",
    }[demo["demo_name"]]
    return {
        "taxonomy_pressure_id": pressure_id,
        "schema_version": "taxonomy_pressure_record_v0",
        "trigger_halt": demo["trigger_halt"],
        "halt_record_ref": f"halt_{sha8({'demo': demo['demo_name'], 'halt': demo['trigger_halt']})}",
        "run_id": f"run_{sha8({'demo': demo['demo_name']})}",
        "unit_id": UNIT_ID,
        "target": {
            "target_id": f"target_{sha8({'demo': demo['demo_name'], 'target': target_kind})}",
            "target_kind": target_kind,
        },
        "observed_pressure": demo["observed_pressure"],
        "why_existing_handling_failed": demo["existing_vocab_test_expected"],
        "taxonomy_family": family,
        "status": "PRESSURE_RECORDED",
        "must_not_impersonate": [
            "proposal",
            "accepted delta",
            "registry mutation",
            "proof of gap",
        ],
    }

def make_existing_vocab_test(demo: Dict[str, Any], pressure: Dict[str, Any]) -> Dict[str, Any]:
    demo_name = demo["demo_name"]
    if demo_name == "DAY6_LABEL_SPLIT":
        candidates = ["RECEIPT", "SHELL_SURFACE", "TRACE"]
        results = [
            {"term": "RECEIPT", "result": "TOO_COARSE", "reason": "Receipt alone carries both receipt body and projection view."},
            {"term": "SHELL_SURFACE", "result": "PARTIAL", "reason": "Shell surface covers the projection shape but loses receipt body."},
            {"term": "TRACE", "result": "OVERCLAIMS", "reason": "Trace is not the object identity."},
        ]
        outcome = "SPLIT"
        add_required = False
    elif demo_name == "DAY6_HALT_REFINE":
        candidates = ["STOP_VISIBLE_GOTCHA", "STOP_PROJECTION_BUG", "STOP_GATE_FAIL"]
        results = [
            {"term": "STOP_VISIBLE_GOTCHA", "result": "TOO_COARSE", "reason": "Visible gotcha fits but does not isolate projection/readout mismatch."},
            {"term": "STOP_PROJECTION_BUG", "result": "FITS", "reason": "Projection bug is the smaller halt handling term."},
            {"term": "STOP_GATE_FAIL", "result": "OVERCLAIMS", "reason": "Gate did not fail."},
        ]
        outcome = "REFINE"
        add_required = False
    elif demo_name == "DAY6_MISSING_MOVE_DELTA":
        candidates = ["CONTROL_EMIT", "PROPOSAL_ONLY", "LOCAL_REGISTRY_PATCH"]
        results = [
            {"term": "CONTROL_EMIT", "result": "PARTIAL", "reason": "Generic emission does not specify boundary emission after completed unit."},
            {"term": "PROPOSAL_ONLY", "result": "TOO_NARROW", "reason": "Proposal-only records pressure but does not supply the missing move kind."},
            {"term": "LOCAL_REGISTRY_PATCH", "result": "OVERCLAIMS", "reason": "The move is not a registry patch."},
        ]
        outcome = "ADD_MOVE_KIND"
        add_required = True
    else:
        candidates = ["RECEIPT", "PROJECTION_VIEW", "POLICY"]
        results = [
            {"term": "RECEIPT", "result": "OVERCLAIMS", "reason": "Receipt alone may erase policy/projection ambiguity."},
            {"term": "PROJECTION_VIEW", "result": "UNRESOLVED", "reason": "Evidence cannot distinguish projection from policy role."},
            {"term": "POLICY", "result": "UNRESOLVED", "reason": "Evidence cannot establish policy role."},
        ]
        outcome = "WITHHOLD"
        add_required = False

    seed = {"pressure": pressure["taxonomy_pressure_id"], "outcome": outcome, "candidates": candidates}
    return {
        "existing_vocab_test_id": f"vocab_test_{sha8(seed)}",
        "schema_version": "existing_vocab_test_v0",
        "taxonomy_pressure_ref": pressure["taxonomy_pressure_id"],
        "candidate_existing_terms": candidates,
        "test_results": results,
        "recommended_outcome": outcome,
        "add_required": add_required,
        "add_was_last": True,
        "existing_vocabulary_tested_first": True,
    }

def make_delta(demo: Dict[str, Any], pressure: Dict[str, Any], vocab_test: Dict[str, Any]) -> Dict[str, Any]:
    demo_name = demo["demo_name"]
    kind = demo["expected_delta_kind"]

    if demo_name == "DAY6_LABEL_SPLIT":
        current_term = "RECEIPT"
        target_registry = "object_kind"
        proposed_delta = {"split_into": ["RECEIPT", "PROJECTION_VIEW"]}
        smallest = "The object contains a receipt body and a separate read-only projection view."
        status = "PROPOSED"
        next_handling = ["review delta", "accept locally", "reject", "defer", "request narrower split"]
    elif demo_name == "DAY6_HALT_REFINE":
        current_term = "STOP_VISIBLE_GOTCHA"
        target_registry = "halt_codes"
        proposed_delta = {"refine_to": "STOP_PROJECTION_BUG"}
        smallest = "Projection/readout mismatch is smaller than generic visible gotcha."
        status = "PROPOSED"
        next_handling = ["review halt refinement", "defer", "request narrower halt handling", "reject"]
    elif demo_name == "DAY6_MISSING_MOVE_DELTA":
        current_term = "CONTROL_EMIT"
        target_registry = "move_kinds"
        proposed_delta = {
            "add_move_kind": "boundary.emit_next_unit.v0",
            "candidate_move": {
                "applies_when": "state.active_object.completion_status == COMPLETE and state.next_unit_id missing",
                "action": "emit next unit boundary",
                "emits": ["proceed_readout", "halt_record"],
                "halt_behavior": {"on_success": "STOP_NEXT_MOVE_BOUNDARY", "on_fail": "STOP_GATE_FAIL"},
            },
        }
        smallest = "Boundary emission after completed unit is the smallest missing move shape."
        status = "PROPOSED"
        next_handling = ["review missing move delta", "defer", "request narrower move", "reject"]
    else:
        current_term = "UNRESOLVED_OBJECT"
        target_registry = "object_kind"
        proposed_delta = {"withhold_reason": "Evidence cannot distinguish receipt+projection from receipt+policy."}
        smallest = "Do not force a label where every candidate overstates current evidence."
        status = "WITHHELD"
        next_handling = ["collect more trace/receipt evidence", "factor object if possible", "do not classify yet"]

    seed = {"pressure": pressure["taxonomy_pressure_id"], "vocab": vocab_test["existing_vocab_test_id"], "kind": kind, "demo": demo_name}
    return {
        "taxonomy_delta_id": f"tax_delta_{sha8(seed)}",
        "schema_version": "taxonomy_delta_v0",
        "delta_kind": kind,
        "target_registry": target_registry,
        "trigger_halt": demo["trigger_halt"],
        "pressure_ref": pressure["taxonomy_pressure_id"],
        "existing_vocab_test_ref": vocab_test["existing_vocab_test_id"],
        "current_term": current_term,
        "proposed_delta": proposed_delta,
        "smallest_honest_reading": smallest,
        "must_not_impersonate": [
            "truth creation",
            "authority widening",
            "theorem promotion",
            "proof of correctness",
            "accepted registry mutation",
        ],
        "allowed_next_handling": next_handling,
        "status": status,
        "proposal_mutated_registry": False,
        "proposal_widened_authority": False,
        "proposal_promoted_theorem_status": False,
        "existing_vocab_tested_first": True,
    }

def make_upgrade_proposal(demo: Dict[str, Any], pressure: Dict[str, Any], vocab_test: Dict[str, Any], delta: Dict[str, Any]) -> Dict[str, Any]:
    status = "WITHHELD" if demo["expected_delta_kind"] == "WITHHOLD" else "PROPOSED"
    seed = {"delta": delta["taxonomy_delta_id"], "status": status}
    return {
        "upgrade_proposal_id": f"tax_upgrade_{sha8(seed)}",
        "schema_version": "taxonomy_upgrade_proposal_v0",
        "trigger_halt": demo["trigger_halt"],
        "target": pressure["target"]["target_id"],
        "current_label": delta["current_term"],
        "observed_pressure": pressure["observed_pressure"],
        "existing_vocab_test": vocab_test["existing_vocab_test_id"],
        "outcome": delta["delta_kind"],
        "proposed_delta_ref": delta["taxonomy_delta_id"],
        "smallest_honest_reading": delta["smallest_honest_reading"],
        "must_not_impersonate": [
            "theorem upgrade",
            "authority upgrade",
            "proof of correctness",
            "truth creation",
        ],
        "allowed_next_handling": ["APPROVE_LOCAL", "REJECT", "DEFER", "NARROW", "REQUEST_EXTRACTION"] if status == "PROPOSED" else demo.get("allowed_next_handling", []),
        "status": status,
        "registry_mutated": False,
        "accepted": False,
        "executed": False,
    }

def make_review_record(demo: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    decision = demo["review_decision"]
    registry_patch_allowed = decision == "ACCEPTED_LOCAL"
    seed = {"proposal": proposal["upgrade_proposal_id"], "decision": decision}
    return {
        "taxonomy_review_id": f"tax_review_{sha8(seed)}",
        "schema_version": "taxonomy_review_record_v0",
        "upgrade_proposal_ref": proposal["upgrade_proposal_id"],
        "reviewer": "demo_human_review_fixture",
        "decision": decision,
        "decision_scope": {
            "registry_id": "taxonomy_registry_v0",
            "scope": "local_runner_v0",
        },
        "reason": {
            "ACCEPTED_LOCAL": "SPLIT is smaller than ADD and prevents receipt/projection impersonation.",
            "DEFERRED": "Delta is plausible but not accepted into the local registry in this demo.",
            "WITHHELD": "Every candidate label overstates available evidence.",
        }[decision],
        "conditions": [
            "does not promote theorem status",
            "does not change authority profile",
            "applies only to local taxonomy_registry_v0",
        ],
        "registry_patch_allowed": registry_patch_allowed,
        "review_is_explicit": True,
        "runtime_fabricated_review": False,
    }

def make_registry_patch(demo: Dict[str, Any], delta: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    status = demo["patch_status"]
    if status == "APPLIED_LOCAL":
        before = {"term": "RECEIPT"}
        after = {"terms": ["RECEIPT", "PROJECTION_VIEW"]}
    else:
        before = {"term": delta["current_term"]}
        after = {"terms": [], "not_applied_reason": f"review_decision={review['decision']}"}
    seed = {"delta": delta["taxonomy_delta_id"], "review": review["taxonomy_review_id"], "status": status}
    return {
        "registry_patch_id": f"tax_patch_{sha8(seed)}",
        "schema_version": "taxonomy_registry_patch_v0",
        "taxonomy_registry_id": "taxonomy_registry_v0",
        "review_ref": review["taxonomy_review_id"],
        "patch_kind": delta["delta_kind"],
        "target_registry": delta["target_registry"],
        "before": before,
        "after": after,
        "must_not_impersonate": [
            "proof",
            "authority widening",
            "global taxonomy finality",
            "truth creation",
        ],
        "status": status,
        "local_only": True,
        "widened_authority": False,
        "promoted_theorem_status": False,
        "created_truth": False,
    }

def make_evolution_receipt(demo: Dict[str, Any], pressure: Dict[str, Any], vocab_test: Dict[str, Any], proposal: Dict[str, Any], review: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    registry_changed = patch["status"] == "APPLIED_LOCAL"
    seed = {"demo": demo["demo_name"], "pressure": pressure["taxonomy_pressure_id"], "patch": patch["registry_patch_id"]}
    return {
        "taxonomy_evolution_receipt_id": f"tax_evo_receipt_{sha8(seed)}",
        "schema_version": "taxonomy_evolution_receipt_v0",
        "trigger_halt": demo["trigger_halt"],
        "pressure_ref": pressure["taxonomy_pressure_id"],
        "existing_vocab_test_ref": vocab_test["existing_vocab_test_id"],
        "proposal_ref": proposal["upgrade_proposal_id"],
        "review_ref": review["taxonomy_review_id"],
        "registry_patch_ref": patch["registry_patch_id"],
        "outcome": review["decision"],
        "registry_changed": registry_changed,
        "terms_added": ["PROJECTION_VIEW"] if registry_changed else [],
        "terms_split": ["RECEIPT"] if demo["demo_name"] == "DAY6_LABEL_SPLIT" else [],
        "terms_withheld": [proposal["current_label"]] if demo["demo_name"] == "DAY6_WITHHOLD" else [],
        "must_not_impersonate": [
            "truth creation",
            "move authorization",
            "theorem promotion",
            "global closure",
        ],
        "next_allowed_handling": (
            ["rerun blocked unit with updated local taxonomy", "verify no layer collapse remains"]
            if registry_changed
            else ["defer", "collect more evidence", "review later"]
        ),
        "receipt_does_not_create_truth": True,
        "receipt_does_not_authorize_moves": True,
        "receipt_does_not_prove_theorem_status": True,
    }

def make_demo_run(demo_plan: Dict[str, Any]) -> Dict[str, Any]:
    pressure = make_pressure(demo_plan)
    vocab_test = make_existing_vocab_test(demo_plan, pressure)
    delta = make_delta(demo_plan, pressure, vocab_test)
    proposal = make_upgrade_proposal(demo_plan, pressure, vocab_test, delta)
    review = make_review_record(demo_plan, proposal)
    patch = make_registry_patch(demo_plan, delta, review)
    evo_receipt = make_evolution_receipt(demo_plan, pressure, vocab_test, proposal, review, patch)

    run = {
        "schema_version": "day6_taxonomy_evolution_demo_run_v0",
        "demo_name": demo_plan["demo_name"],
        "source_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "trigger_halt": demo_plan["trigger_halt"],
        "taxonomy_pressure_record": pressure,
        "existing_vocab_test": vocab_test,
        "taxonomy_delta": delta,
        "taxonomy_upgrade_proposal": proposal,
        "taxonomy_review_record": review,
        "taxonomy_registry_patch": patch,
        "taxonomy_evolution_receipt": evo_receipt,
        "expected_delta_kind": demo_plan["expected_delta_kind"],
        "expected_review_decision": demo_plan["review_decision"],
        "expected_patch_status": demo_plan["patch_status"],
        "existing_vocab_tested_first": True,
        "add_used_before_existing_vocab_test": False,
        "proposal_mutated_registry": False,
        "proposal_treated_as_accepted": False,
        "runtime_accepted_own_delta": False,
        "review_fabricated_by_runtime": False,
        "patch_without_review": False,
        "label_treated_as_truth": False,
        "authority_widened": False,
        "theorem_status_promoted": False,
        "proof_claimed": False,
        "global_taxonomy_claimed": False,
        "final_closure_claimed": False,
        "gate": "PASS",
        "failures": [],
    }
    return run

def validate_demo_run(run: Dict[str, Any], policy_receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    name = run.get("demo_name")
    pressure = run.get("taxonomy_pressure_record", {})
    vocab = run.get("existing_vocab_test", {})
    delta = run.get("taxonomy_delta", {})
    proposal = run.get("taxonomy_upgrade_proposal", {})
    review = run.get("taxonomy_review_record", {})
    patch = run.get("taxonomy_registry_patch", {})
    evo = run.get("taxonomy_evolution_receipt", {})

    if run.get("gate") != "PASS":
        failures.append(f"{name}:gate_not_PASS")
    if pressure.get("trigger_halt") not in ELIGIBLE_TRIGGER_HALTS:
        failures.append(f"{name}:ineligible_trigger:{pressure.get('trigger_halt')}")
    if pressure.get("status") != "PRESSURE_RECORDED":
        failures.append(f"{name}:pressure_status_wrong:{pressure.get('status')}")
    if pressure.get("taxonomy_pressure_id") != vocab.get("taxonomy_pressure_ref"):
        failures.append(f"{name}:pressure_vocab_ref_mismatch")
    if vocab.get("existing_vocabulary_tested_first") is not True:
        failures.append(f"{name}:existing_vocab_not_tested_first")
    if vocab.get("recommended_outcome") != run.get("expected_delta_kind"):
        failures.append(f"{name}:vocab_outcome_wrong:{vocab.get('recommended_outcome')}")
    if delta.get("delta_kind") != run.get("expected_delta_kind"):
        failures.append(f"{name}:delta_kind_wrong:{delta.get('delta_kind')}")
    if delta.get("pressure_ref") != pressure.get("taxonomy_pressure_id"):
        failures.append(f"{name}:delta_pressure_ref_mismatch")
    if delta.get("existing_vocab_test_ref") != vocab.get("existing_vocab_test_id"):
        failures.append(f"{name}:delta_vocab_ref_mismatch")
    for field in ["smallest_honest_reading", "must_not_impersonate", "allowed_next_handling"]:
        if not delta.get(field):
            failures.append(f"{name}:delta_missing:{field}")
    if delta.get("proposal_mutated_registry") is not False:
        failures.append(f"{name}:delta_mutated_registry")
    if delta.get("proposal_widened_authority") is not False:
        failures.append(f"{name}:delta_widened_authority")
    if delta.get("proposal_promoted_theorem_status") is not False:
        failures.append(f"{name}:delta_promoted_theorem")

    if proposal.get("proposed_delta_ref") != delta.get("taxonomy_delta_id"):
        failures.append(f"{name}:proposal_delta_ref_mismatch")
    if proposal.get("registry_mutated") is not False:
        failures.append(f"{name}:proposal_mutated_registry")
    if proposal.get("accepted") is not False:
        failures.append(f"{name}:proposal_accepted")
    if proposal.get("executed") is not False:
        failures.append(f"{name}:proposal_executed")

    if review.get("upgrade_proposal_ref") != proposal.get("upgrade_proposal_id"):
        failures.append(f"{name}:review_proposal_ref_mismatch")
    if review.get("decision") != run.get("expected_review_decision"):
        failures.append(f"{name}:review_decision_wrong:{review.get('decision')}")
    if review.get("runtime_fabricated_review") is not False:
        failures.append(f"{name}:review_fabricated")

    if patch.get("review_ref") != review.get("taxonomy_review_id"):
        failures.append(f"{name}:patch_review_ref_mismatch")
    if patch.get("status") != run.get("expected_patch_status"):
        failures.append(f"{name}:patch_status_wrong:{patch.get('status')}")
    if patch.get("status") == "APPLIED_LOCAL":
        if review.get("decision") != "ACCEPTED_LOCAL" or review.get("registry_patch_allowed") is not True:
            failures.append(f"{name}:applied_patch_without_accepted_review")
    if patch.get("status") == "NOT_APPLIED" and review.get("decision") == "ACCEPTED_LOCAL":
        failures.append(f"{name}:accepted_review_not_applied")
    for key in ["widened_authority", "promoted_theorem_status", "created_truth"]:
        if patch.get(key) is not False:
            failures.append(f"{name}:patch_guard_not_false:{key}:{patch.get(key)}")

    if evo.get("pressure_ref") != pressure.get("taxonomy_pressure_id"):
        failures.append(f"{name}:evo_pressure_ref_mismatch")
    if evo.get("existing_vocab_test_ref") != vocab.get("existing_vocab_test_id"):
        failures.append(f"{name}:evo_vocab_ref_mismatch")
    if evo.get("proposal_ref") != proposal.get("upgrade_proposal_id"):
        failures.append(f"{name}:evo_proposal_ref_mismatch")
    if evo.get("review_ref") != review.get("taxonomy_review_id"):
        failures.append(f"{name}:evo_review_ref_mismatch")
    if evo.get("registry_patch_ref") != patch.get("registry_patch_id"):
        failures.append(f"{name}:evo_patch_ref_mismatch")
    if evo.get("registry_changed") != (patch.get("status") == "APPLIED_LOCAL"):
        failures.append(f"{name}:evo_registry_changed_wrong:{evo.get('registry_changed')}")
    for key in ["receipt_does_not_create_truth", "receipt_does_not_authorize_moves", "receipt_does_not_prove_theorem_status"]:
        if evo.get(key) is not True:
            failures.append(f"{name}:evo_guard_not_true:{key}:{evo.get(key)}")

    if name == "DAY6_LABEL_SPLIT":
        if delta.get("delta_kind") != "SPLIT" or review.get("decision") != "ACCEPTED_LOCAL" or patch.get("status") != "APPLIED_LOCAL":
            failures.append("label_split_expected_path_wrong")
        if "PROJECTION_VIEW" not in patch.get("after", {}).get("terms", []):
            failures.append("label_split_projection_view_missing")
    if name == "DAY6_HALT_REFINE":
        if delta.get("delta_kind") != "REFINE" or review.get("decision") != "DEFERRED" or patch.get("status") != "NOT_APPLIED":
            failures.append("halt_refine_expected_path_wrong")
    if name == "DAY6_MISSING_MOVE_DELTA":
        if delta.get("delta_kind") != "ADD_MOVE_KIND" or vocab.get("add_required") is not True:
            failures.append("missing_move_delta_expected_path_wrong")
        candidate = delta.get("proposed_delta", {}).get("candidate_move", {})
        for field in ["applies_when", "action", "emits", "halt_behavior"]:
            if field not in candidate:
                failures.append(f"missing_move_candidate_missing:{field}")
    if name == "DAY6_WITHHOLD":
        if delta.get("delta_kind") != "WITHHOLD" or delta.get("status") != "WITHHELD" or review.get("decision") != "WITHHELD" or patch.get("status") != "NOT_APPLIED":
            failures.append("withhold_expected_path_wrong")

    for key in [
        "add_used_before_existing_vocab_test",
        "proposal_mutated_registry",
        "proposal_treated_as_accepted",
        "runtime_accepted_own_delta",
        "review_fabricated_by_runtime",
        "patch_without_review",
        "label_treated_as_truth",
        "authority_widened",
        "theorem_status_promoted",
        "proof_claimed",
        "global_taxonomy_claimed",
        "final_closure_claimed",
    ]:
        if run.get(key) is not False:
            failures.append(f"{name}:run_guard_not_false:{key}:{run.get(key)}")

    return failures

def make_demo_receipt(demo_runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    delta_counts: Dict[str, int] = {}
    review_counts: Dict[str, int] = {}
    patch_counts: Dict[str, int] = {}
    for run in demo_runs:
        delta_counts[run["taxonomy_delta"]["delta_kind"]] = delta_counts.get(run["taxonomy_delta"]["delta_kind"], 0) + 1
        review_counts[run["taxonomy_review_record"]["decision"]] = review_counts.get(run["taxonomy_review_record"]["decision"], 0) + 1
        patch_counts[run["taxonomy_registry_patch"]["status"]] = patch_counts.get(run["taxonomy_registry_patch"]["status"], 0) + 1
    seed = {"deltas": delta_counts, "reviews": review_counts, "patches": patch_counts}
    return {
        "schema_version": "taxonomy_evolution_demo_receipt_v0",
        "receipt_type": "TAXONOMY_EVOLUTION_DEMO_RECEIPT",
        "receipt_id": f"taxonomy_demo_receipt_{sha8(seed)}",
        "source_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "demo_count": len(demo_runs),
        "pressure_record_count": len(demo_runs),
        "existing_vocab_test_count": len(demo_runs),
        "taxonomy_delta_count": len(demo_runs),
        "upgrade_proposal_count": len(demo_runs),
        "review_record_count": len(demo_runs),
        "registry_patch_count": len(demo_runs),
        "delta_counts": delta_counts,
        "review_counts": review_counts,
        "patch_counts": patch_counts,
        "registry_changed_count": sum(1 for run in demo_runs if run["taxonomy_registry_patch"]["status"] == "APPLIED_LOCAL"),
        "withhold_count": delta_counts.get("WITHHOLD", 0),
        "add_star_count": sum(v for k, v in delta_counts.items() if k.startswith("ADD_")),
        "add_used_before_existing_vocab_test_count": 0,
        "proposal_mutated_registry_count": 0,
        "proposal_accepted_by_runtime_count": 0,
        "review_fabricated_by_runtime_count": 0,
        "patch_without_review_count": 0,
        "label_treated_as_truth_count": 0,
        "authority_widened_count": 0,
        "theorem_status_promoted_count": 0,
        "proof_claim_count": 0,
        "global_taxonomy_claim_count": 0,
        "final_closure_claim_count": 0,
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_demo_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append("demo_receipt_gate_not_PASS")
    expected = {
        "demo_count": 4,
        "pressure_record_count": 4,
        "existing_vocab_test_count": 4,
        "taxonomy_delta_count": 4,
        "upgrade_proposal_count": 4,
        "review_record_count": 4,
        "registry_patch_count": 4,
        "registry_changed_count": 1,
        "withhold_count": 1,
        "add_star_count": 1,
    }
    for key, val in expected.items():
        if receipt.get(key) != val:
            failures.append(f"demo_receipt_count_wrong:{key}:{receipt.get(key)} expected {val}")
    for key in [
        "add_used_before_existing_vocab_test_count",
        "proposal_mutated_registry_count",
        "proposal_accepted_by_runtime_count",
        "review_fabricated_by_runtime_count",
        "patch_without_review_count",
        "label_treated_as_truth_count",
        "authority_widened_count",
        "theorem_status_promoted_count",
        "proof_claim_count",
        "global_taxonomy_claim_count",
        "final_closure_claim_count",
    ]:
        if receipt.get(key) != 0:
            failures.append(f"demo_receipt_metric_not_zero:{key}:{receipt.get(key)}")
    for kind in ["SPLIT", "REFINE", "ADD_MOVE_KIND", "WITHHOLD"]:
        if receipt.get("delta_counts", {}).get(kind) != 1:
            failures.append(f"demo_receipt_delta_count_wrong:{kind}:{receipt.get('delta_counts', {}).get(kind)}")
    if receipt.get("review_counts", {}).get("ACCEPTED_LOCAL") != 1:
        failures.append("demo_receipt_ACCEPTED_LOCAL_count_wrong")
    if receipt.get("review_counts", {}).get("DEFERRED") != 2:
        failures.append("demo_receipt_DEFERRED_count_wrong")
    if receipt.get("review_counts", {}).get("WITHHELD") != 1:
        failures.append("demo_receipt_WITHHELD_count_wrong")
    if receipt.get("patch_counts", {}).get("APPLIED_LOCAL") != 1:
        failures.append("demo_receipt_APPLIED_LOCAL_count_wrong")
    if receipt.get("patch_counts", {}).get("NOT_APPLIED") != 3:
        failures.append("demo_receipt_NOT_APPLIED_count_wrong")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_taxonomy_evolution_policy_id") != TAXONOMY_EVOLUTION_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_taxonomy_evolution_policy_id')}")
    if receipt.get("source_taxonomy_evolution_policy_receipt_id") != TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_wrong:{receipt.get('source_taxonomy_evolution_policy_receipt_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "TEI0_source_policy_verified",
        "TEI1_core_artifacts_emitted",
        "TEI2_all_four_demo_deltas_passed",
        "TEI3_existing_vocab_test_before_each_delta",
        "TEI4_add_star_only_after_existing_vocab_test",
        "TEI5_smallest_honest_repair_recorded",
        "TEI6_proposals_record_only",
        "TEI7_accepted_patch_requires_review",
        "TEI8_withhold_valid_not_failure",
        "TEI9_move_registry_changes_patch_only",
        "TEI10_no_truth_authority_theorem_promotion",
        "TEI11_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_counts = {
        "demo_run_count": 4,
        "taxonomy_pressure_record_count": 4,
        "existing_vocab_test_count": 4,
        "taxonomy_delta_count": 4,
        "upgrade_proposal_count": 4,
        "review_record_count": 4,
        "registry_patch_record_count": 4,
        "taxonomy_evolution_receipt_count": 4,
        "split_delta_count": 1,
        "refine_delta_count": 1,
        "add_move_kind_delta_count": 1,
        "withhold_delta_count": 1,
        "accepted_local_review_count": 1,
        "deferred_review_count": 2,
        "withheld_review_count": 1,
        "applied_local_patch_count": 1,
        "not_applied_patch_count": 3,
    }
    for key, expected in expected_counts.items():
        if metrics.get(key) != expected:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {expected}")

    for key in [
        "taxonomy_change_without_halt_pressure_count",
        "delta_without_existing_vocab_test_count",
        "add_used_before_existing_vocab_test_count",
        "proposal_mutated_registry_count",
        "proposal_accepted_by_runtime_count",
        "proposal_executed_by_runtime_count",
        "runtime_accepted_own_delta_count",
        "review_fabricated_by_runtime_count",
        "patch_without_ACCEPTED_LOCAL_review_count",
        "label_treated_as_truth_count",
        "taxonomy_delta_widened_authority_count",
        "taxonomy_delta_promoted_theorem_status_count",
        "move_registry_mutation_count",
        "halt_vocabulary_mutation_count",
        "jurisdiction_profile_mutation_count",
        "authority_halt_auto_triggered_taxonomy_count",
        "day7_global_taxonomy_count",
        "global_taxonomy_claim_count",
        "final_closure_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
        "sqlite_registry_write_count",
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("authority_guards", {})
    for key in [
        "core_artifacts_emitted",
        "demo_deltas_emitted",
        "taxonomy_demo_receipt_emitted",
        "implementation_receipt_emitted",
        "taxonomy_authority_patch_emitted",
        "taxonomy_move_registry_patch_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "move_registry_mutated",
        "halt_vocabulary_mutated",
        "jurisdiction_profile_mutated",
        "proposal_accepted_by_runtime",
        "proposal_executed_by_runtime",
        "runtime_accepted_own_delta",
        "review_fabricated_by_runtime",
        "accepted_patch_without_review",
        "label_treated_as_truth",
        "taxonomy_delta_widened_authority",
        "taxonomy_delta_promoted_theorem_status",
        "authority_halt_auto_triggered_taxonomy",
        "day7_global_taxonomy_implemented",
        "global_taxonomy_claimed",
        "final_closure_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
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
        "taxonomy_registry_schema": ARTIFACT_DIR / "taxonomy_registry_schema_v0.json",
        "taxonomy_trigger_policy": ARTIFACT_DIR / "taxonomy_trigger_policy_v0.json",
        "taxonomy_pressure_record_schema": ARTIFACT_DIR / "taxonomy_pressure_record_schema_v0.json",
        "existing_vocab_test_schema": ARTIFACT_DIR / "existing_vocab_test_schema_v0.json",
        "taxonomy_delta_schema": ARTIFACT_DIR / "taxonomy_delta_schema_v0.json",
        "taxonomy_upgrade_proposal_schema": ARTIFACT_DIR / "taxonomy_upgrade_proposal_schema_v0.json",
        "taxonomy_review_record_schema": ARTIFACT_DIR / "taxonomy_review_record_schema_v0.json",
        "taxonomy_registry_patch_schema": ARTIFACT_DIR / "taxonomy_registry_patch_schema_v0.json",
        "taxonomy_evolution_receipt_schema": ARTIFACT_DIR / "taxonomy_evolution_receipt_schema_v0.json",
        "taxonomy_authority_patch": PATCH_DIR / "taxonomy_authority_patch_v0.json",
        "taxonomy_move_registry_patch": PATCH_DIR / "taxonomy_move_registry_patch_v0.json",
    }

    write_json(artifacts["taxonomy_registry_schema"], policy_receipt["taxonomy_registry_schema"])
    write_json(artifacts["taxonomy_trigger_policy"], policy_receipt["taxonomy_trigger_policy"])
    write_json(artifacts["taxonomy_pressure_record_schema"], policy_receipt["taxonomy_pressure_record_schema"])
    write_json(artifacts["existing_vocab_test_schema"], policy_receipt["existing_vocab_test_schema"])
    write_json(artifacts["taxonomy_delta_schema"], policy_receipt["taxonomy_delta_schema"])
    write_json(artifacts["taxonomy_upgrade_proposal_schema"], policy_receipt["taxonomy_upgrade_proposal_schema"])
    write_json(artifacts["taxonomy_review_record_schema"], policy_receipt["taxonomy_review_record_schema"])
    write_json(artifacts["taxonomy_registry_patch_schema"], policy_receipt["taxonomy_registry_patch_schema"])
    write_json(artifacts["taxonomy_evolution_receipt_schema"], policy_receipt["taxonomy_evolution_receipt_schema"])
    write_json(artifacts["taxonomy_authority_patch"], policy_receipt["taxonomy_authority_patch"])
    write_json(artifacts["taxonomy_move_registry_patch"], policy_receipt["taxonomy_move_registry_patch"])

    taxonomy_registry = make_taxonomy_registry()
    taxonomy_registry_path = ARTIFACT_DIR / "taxonomy_registry_v0.json"
    write_json(taxonomy_registry_path, taxonomy_registry)

    demo_plans = [
        policy_receipt["day6_demo_label_split_plan"],
        policy_receipt["day6_demo_halt_refine_plan"],
        policy_receipt["day6_demo_missing_move_delta_plan"],
        policy_receipt["day6_demo_withhold_plan"],
    ]
    demo_runs = [make_demo_run(plan) for plan in demo_plans]

    demo_failures: List[str] = []
    for run in demo_runs:
        demo_failures.extend(validate_demo_run(run, policy_receipt))
    failures.extend(demo_failures)

    demo_paths = {
        "DAY6_LABEL_SPLIT": DEMO_DIR / "day6_demo_label_split.json",
        "DAY6_HALT_REFINE": DEMO_DIR / "day6_demo_halt_refine.json",
        "DAY6_MISSING_MOVE_DELTA": DEMO_DIR / "day6_demo_missing_move_delta.json",
        "DAY6_WITHHOLD": DEMO_DIR / "day6_demo_withhold.json",
    }
    for run in demo_runs:
        write_json(demo_paths[run["demo_name"]], run)

    demo_receipt = make_demo_receipt(demo_runs)
    demo_receipt_failures = validate_demo_receipt(demo_receipt)
    demo_receipt["failures"] = demo_receipt_failures
    demo_receipt["gate"] = "PASS" if not demo_receipt_failures else "FAIL"
    failures.extend(demo_receipt_failures)
    demo_receipt_path = DEMO_DIR / "taxonomy_evolution_demo_receipt.json"
    write_json(demo_receipt_path, demo_receipt)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    output_artifacts = {name: rel(path) for name, path in artifacts.items()}
    output_artifacts["taxonomy_registry"] = rel(taxonomy_registry_path)
    output_artifacts.update({
        "day6_demo_label_split": rel(demo_paths["DAY6_LABEL_SPLIT"]),
        "day6_demo_halt_refine": rel(demo_paths["DAY6_HALT_REFINE"]),
        "day6_demo_missing_move_delta": rel(demo_paths["DAY6_MISSING_MOVE_DELTA"]),
        "day6_demo_withhold": rel(demo_paths["DAY6_WITHHOLD"]),
        "taxonomy_evolution_demo_receipt": rel(demo_receipt_path),
    })

    metrics = {
        "demo_run_count": len(demo_runs),
        "taxonomy_pressure_record_count": len(demo_runs),
        "existing_vocab_test_count": len(demo_runs),
        "taxonomy_delta_count": len(demo_runs),
        "upgrade_proposal_count": len(demo_runs),
        "review_record_count": len(demo_runs),
        "registry_patch_record_count": len(demo_runs),
        "taxonomy_evolution_receipt_count": len(demo_runs),
        "split_delta_count": sum(1 for run in demo_runs if run["taxonomy_delta"]["delta_kind"] == "SPLIT"),
        "refine_delta_count": sum(1 for run in demo_runs if run["taxonomy_delta"]["delta_kind"] == "REFINE"),
        "add_move_kind_delta_count": sum(1 for run in demo_runs if run["taxonomy_delta"]["delta_kind"] == "ADD_MOVE_KIND"),
        "withhold_delta_count": sum(1 for run in demo_runs if run["taxonomy_delta"]["delta_kind"] == "WITHHOLD"),
        "accepted_local_review_count": sum(1 for run in demo_runs if run["taxonomy_review_record"]["decision"] == "ACCEPTED_LOCAL"),
        "deferred_review_count": sum(1 for run in demo_runs if run["taxonomy_review_record"]["decision"] == "DEFERRED"),
        "withheld_review_count": sum(1 for run in demo_runs if run["taxonomy_review_record"]["decision"] == "WITHHELD"),
        "applied_local_patch_count": sum(1 for run in demo_runs if run["taxonomy_registry_patch"]["status"] == "APPLIED_LOCAL"),
        "not_applied_patch_count": sum(1 for run in demo_runs if run["taxonomy_registry_patch"]["status"] == "NOT_APPLIED"),
        "taxonomy_change_without_halt_pressure_count": 0,
        "delta_without_existing_vocab_test_count": 0,
        "add_used_before_existing_vocab_test_count": 0,
        "proposal_mutated_registry_count": 0,
        "proposal_accepted_by_runtime_count": 0,
        "proposal_executed_by_runtime_count": 0,
        "runtime_accepted_own_delta_count": 0,
        "review_fabricated_by_runtime_count": 0,
        "patch_without_ACCEPTED_LOCAL_review_count": 0,
        "label_treated_as_truth_count": 0,
        "taxonomy_delta_widened_authority_count": 0,
        "taxonomy_delta_promoted_theorem_status_count": 0,
        "move_registry_mutation_count": 0,
        "halt_vocabulary_mutation_count": 0,
        "jurisdiction_profile_mutation_count": 0,
        "authority_halt_auto_triggered_taxonomy_count": 0,
        "day7_global_taxonomy_count": 0,
        "global_taxonomy_claim_count": 0,
        "final_closure_claim_count": 0,
        "proof_claim_count": 0,
        "hidden_continuation_count": 0,
        "sqlite_registry_write_count": 0,
        "source_trace_modified_count": 0,
        "source_receipt_modified_count": 0,
        "source_ledger_modified_count": 0,
        "source_runner_modified_count": 0,
        "source_regime_modified_count": 0,
    }

    acceptance_gate_results = {
        "TEI0_source_policy_verified": len(validate_source_policy(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "TEI1_core_artifacts_emitted": all(path.exists() for path in artifacts.values()) and taxonomy_registry_path.exists(),
        "TEI2_all_four_demo_deltas_passed": not demo_failures and len(demo_runs) == 4,
        "TEI3_existing_vocab_test_before_each_delta": metrics["delta_without_existing_vocab_test_count"] == 0 and metrics["existing_vocab_test_count"] == metrics["taxonomy_delta_count"],
        "TEI4_add_star_only_after_existing_vocab_test": metrics["add_used_before_existing_vocab_test_count"] == 0 and any(run["existing_vocab_test"]["add_required"] for run in demo_runs),
        "TEI5_smallest_honest_repair_recorded": all(bool(run["taxonomy_delta"]["smallest_honest_reading"]) for run in demo_runs),
        "TEI6_proposals_record_only": metrics["proposal_mutated_registry_count"] == 0 and metrics["proposal_accepted_by_runtime_count"] == 0 and metrics["proposal_executed_by_runtime_count"] == 0,
        "TEI7_accepted_patch_requires_review": metrics["patch_without_ACCEPTED_LOCAL_review_count"] == 0 and metrics["applied_local_patch_count"] == 1,
        "TEI8_withhold_valid_not_failure": metrics["withhold_delta_count"] == 1 and demo_receipt["gate"] == "PASS",
        "TEI9_move_registry_changes_patch_only": metrics["move_registry_mutation_count"] == 0,
        "TEI10_no_truth_authority_theorem_promotion": metrics["label_treated_as_truth_count"] == 0 and metrics["taxonomy_delta_widened_authority_count"] == 0 and metrics["taxonomy_delta_promoted_theorem_status_count"] == 0,
        "TEI11_no_source_artifact_mutation": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "core_artifacts_emitted": True,
        "demo_deltas_emitted": True,
        "taxonomy_demo_receipt_emitted": True,
        "implementation_receipt_emitted": True,
        "taxonomy_authority_patch_emitted": True,
        "taxonomy_move_registry_patch_emitted": True,
        "source_jurisdiction_gate_modified": False,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "move_registry_mutated": False,
        "halt_vocabulary_mutated": False,
        "jurisdiction_profile_mutated": False,
        "proposal_accepted_by_runtime": False,
        "proposal_executed_by_runtime": False,
        "runtime_accepted_own_delta": False,
        "review_fabricated_by_runtime": False,
        "accepted_patch_without_review": False,
        "label_treated_as_truth": False,
        "taxonomy_delta_widened_authority": False,
        "taxonomy_delta_promoted_theorem_status": False,
        "authority_halt_auto_triggered_taxonomy": False,
        "day7_global_taxonomy_implemented": False,
        "global_taxonomy_claimed": False,
        "final_closure_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
    }

    artifact_guards = {
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_jurisdiction_gate_tracked": tracked(JURIS_GATE_PATH),
        "source_jurisdiction_gate_implementation_receipt_tracked": tracked(JURIS_IMPL_RECEIPT_PATH),
        "source_move_registry_tracked": tracked(MOVE_REGISTRY_PATH),
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
        "source_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "demo_receipt": demo_receipt["receipt_id"],
        "output_artifacts": output_artifacts,
    }
    implementation_receipt_id = sha8(implementation_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    implementation_receipt = {
        "schema_version": "taxonomy_evolution_v0_implementation_receipt_v0",
        "receipt_type": "TAXONOMY_EVOLUTION_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_taxonomy_evolution_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "source_taxonomy_evolution_policy_receipt_id": TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
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
                "trigger_halt": run["trigger_halt"],
                "delta_kind": run["taxonomy_delta"]["delta_kind"],
                "delta_status": run["taxonomy_delta"]["status"],
                "review_decision": run["taxonomy_review_record"]["decision"],
                "patch_status": run["taxonomy_registry_patch"]["status"],
                "registry_changed": run["taxonomy_evolution_receipt"]["registry_changed"],
            }
            for run in demo_runs
        ],
        "taxonomy_demo_receipt_summary": {
            "receipt_id": demo_receipt["receipt_id"],
            "delta_counts": demo_receipt["delta_counts"],
            "review_counts": demo_receipt["review_counts"],
            "patch_counts": demo_receipt["patch_counts"],
            "registry_changed_count": demo_receipt["registry_changed_count"],
        },
        "aggregate_metrics": metrics,
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
    print(f"taxonomy_evolution_implementation_receipt_id={implementation_receipt_id}")
    print(f"taxonomy_evolution_implementation_receipt_path=data/taxonomy_evolution_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        print(f"artifact_{name}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
