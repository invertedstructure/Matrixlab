#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_TAXONOMY_EVOLUTION_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_TAXONOMY_EVOLUTION_V0_WITH_DEMO_DELTAS_V0"
TARGET_UNIT_ID = "taxonomy_evolution.v0"

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

OUT_DIR = ROOT / "data" / "taxonomy_evolution_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "taxonomy_evolution_v0_policy_receipts"

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

DELTA_KINDS = [
    "ASSIGN",
    "WITHHOLD",
    "REFINE",
    "WEAKEN",
    "SPLIT",
    "MERGE",
    "DROP",
    "ADD_LABEL",
    "ADD_HALT",
    "ADD_MOVE_KIND",
    "ADD_BLOCK_REASON",
    "ADD_STOP_CONDITION",
]

REVIEW_DECISIONS = [
    "PROPOSED",
    "ACCEPTED_LOCAL",
    "REJECTED",
    "DEFERRED",
    "WITHHELD",
    "NEEDS_NARROWING",
    "NEEDS_EXTRACTION",
]

EXISTING_VOCAB_OUTCOMES = [
    "ASSIGN",
    "WITHHOLD",
    "REFINE",
    "WEAKEN",
    "SPLIT",
    "MERGE",
    "DROP",
    "ADD_LABEL",
    "ADD_HALT",
    "ADD_MOVE_KIND",
    "ADD_BLOCK_REASON",
    "ADD_STOP_CONDITION",
]

TAXONOMY_REGISTRY_SCHEMA = {
    "schema_version": "taxonomy_registry_schema_v0",
    "required_fields": [
        "taxonomy_registry_id",
        "schema_version",
        "registries",
        "registry_law",
    ],
    "typed_registries": [
        "object_kind",
        "truth_status",
        "layer",
        "route_role",
        "extractability",
        "content_scope",
        "allowed_consumers",
        "allowed_next_moves",
        "stop_conditions",
        "halt_codes",
        "move_kinds",
        "block_reasons",
    ],
    "registry_law": [
        "labels carry no authority by themselves",
        "new terms require accepted taxonomy delta",
        "proposals do not mutate registry",
        "accepted deltas must preserve non-impersonation",
        "existing vocabulary must be tested before ADD",
    ],
    "must_not_impersonate": [
        "truth registry",
        "authority source",
        "proof system",
        "global taxonomy",
        "final ontology",
    ],
}

TAXONOMY_TRIGGER_POLICY = {
    "schema_version": "taxonomy_trigger_policy_v0",
    "eligible_trigger_halts": ELIGIBLE_TRIGGER_HALTS,
    "authority_halts_context_only": AUTHORITY_HALTS_CONTEXT_ONLY,
    "core_law": [
        "No halt, no taxonomy upgrade.",
        "Authority boundary does not automatically imply vocabulary failure.",
        "STOP_AUTHORITY_VIOLATION is not an ordinary taxonomy trigger.",
    ],
}

TAXONOMY_PRESSURE_RECORD_SCHEMA = {
    "schema_version": "taxonomy_pressure_record_schema_v0",
    "required_fields": [
        "taxonomy_pressure_id",
        "schema_version",
        "trigger_halt",
        "halt_record_ref",
        "run_id",
        "unit_id",
        "target",
        "observed_pressure",
        "why_existing_handling_failed",
        "taxonomy_family",
        "status",
    ],
    "status_enum": ["PRESSURE_RECORDED"],
    "pressure_is_not_delta": True,
    "must_not_impersonate": [
        "proposal",
        "accepted delta",
        "registry mutation",
        "proof of gap",
    ],
}

EXISTING_VOCAB_TEST_SCHEMA = {
    "schema_version": "existing_vocab_test_schema_v0",
    "required_fields": [
        "existing_vocab_test_id",
        "schema_version",
        "taxonomy_pressure_ref",
        "candidate_existing_terms",
        "test_results",
        "recommended_outcome",
        "add_required",
    ],
    "test_result_values": [
        "FITS",
        "PARTIAL",
        "TOO_COARSE",
        "TOO_NARROW",
        "OVERCLAIMS",
        "MISSING",
        "UNRESOLVED",
    ],
    "recommended_outcomes": EXISTING_VOCAB_OUTCOMES,
    "law": [
        "No existing_vocab_test, no taxonomy_delta.",
        "ADD_* is last.",
        "WITHHOLD is valid and does not count as failure.",
        "Do not add terms because they sound cleaner.",
    ],
}

TAXONOMY_DELTA_SCHEMA = {
    "schema_version": "taxonomy_delta_schema_v0",
    "required_fields": [
        "taxonomy_delta_id",
        "schema_version",
        "delta_kind",
        "target_registry",
        "trigger_halt",
        "pressure_ref",
        "existing_vocab_test_ref",
        "current_term",
        "proposed_delta",
        "smallest_honest_reading",
        "must_not_impersonate",
        "allowed_next_handling",
        "status",
    ],
    "delta_kinds": DELTA_KINDS,
    "status_enum": [
        "PROPOSED",
        "WITHHELD",
        "NEEDS_NARROWING",
        "NEEDS_EXTRACTION",
    ],
    "law": [
        "Delta must cite pressure_ref.",
        "Delta must cite existing_vocab_test_ref.",
        "Delta must be the smallest honest repair.",
        "Delta does not widen authority.",
        "Delta does not promote theorem status.",
        "Delta does not mutate registry.",
    ],
}

TAXONOMY_UPGRADE_PROPOSAL_SCHEMA = {
    "schema_version": "taxonomy_upgrade_proposal_schema_v0",
    "required_fields": [
        "upgrade_proposal_id",
        "schema_version",
        "trigger_halt",
        "target",
        "current_label",
        "observed_pressure",
        "existing_vocab_test",
        "outcome",
        "proposed_delta_ref",
        "smallest_honest_reading",
        "must_not_impersonate",
        "allowed_next_handling",
        "status",
    ],
    "status_enum": ["PROPOSED", "WITHHELD", "NEEDS_NARROWING", "NEEDS_EXTRACTION"],
    "law": [
        "Upgrade proposal is not acceptance.",
        "Upgrade proposal is not registry mutation.",
        "Upgrade proposal is not truth creation.",
        "Upgrade proposal requires review before acceptance.",
    ],
}

TAXONOMY_REVIEW_RECORD_SCHEMA = {
    "schema_version": "taxonomy_review_record_schema_v0",
    "required_fields": [
        "taxonomy_review_id",
        "schema_version",
        "upgrade_proposal_ref",
        "reviewer",
        "decision",
        "decision_scope",
        "reason",
        "conditions",
        "registry_patch_allowed",
    ],
    "decision_enum": REVIEW_DECISIONS,
    "canonical_accept_decision": "ACCEPTED_LOCAL",
    "accepted_by_review_is_alias_only": True,
    "law": [
        "No review record, no registry patch.",
        "Only ACCEPTED_LOCAL may allow APPLIED_LOCAL patch.",
        "ACCEPTED_LOCAL is local to declared taxonomy registry.",
        "Human/review layer must be explicit.",
    ],
}

TAXONOMY_REGISTRY_PATCH_SCHEMA = {
    "schema_version": "taxonomy_registry_patch_schema_v0",
    "required_fields": [
        "registry_patch_id",
        "schema_version",
        "taxonomy_registry_id",
        "review_ref",
        "patch_kind",
        "target_registry",
        "before",
        "after",
        "must_not_impersonate",
        "status",
    ],
    "status_enum": ["APPLIED_LOCAL", "NOT_APPLIED"],
    "law": [
        "Only accepted review may create APPLIED_LOCAL patch.",
        "Patch is local, not global.",
        "Patch does not widen authority.",
        "Patch does not prove truth.",
    ],
}

TAXONOMY_EVOLUTION_RECEIPT_SCHEMA = {
    "schema_version": "taxonomy_evolution_receipt_schema_v0",
    "required_fields": [
        "taxonomy_evolution_receipt_id",
        "schema_version",
        "trigger_halt",
        "pressure_ref",
        "existing_vocab_test_ref",
        "proposal_ref",
        "review_ref",
        "registry_patch_ref",
        "outcome",
        "registry_changed",
        "terms_added",
        "terms_split",
        "terms_withheld",
        "must_not_impersonate",
        "next_allowed_handling",
    ],
    "law": [
        "Receipt records handling syntax improvement only.",
        "Receipt does not create truth.",
        "Receipt does not authorize moves.",
        "Receipt does not prove theorem status.",
        "Receipt does not claim global closure.",
    ],
}

TAXONOMY_AUTHORITY_PATCH = {
    "schema_version": "taxonomy_authority_patch_v0",
    "patch_mode": "future_jurisdiction_profile_patch_only_do_not_mutate_existing_profile",
    "taxonomy_authority": {
        "runtime_allowed": [
            "record_taxonomy_pressure",
            "test_existing_vocabulary",
            "emit_taxonomy_delta_proposal",
            "emit_upgrade_proposal",
            "emit_withhold_record",
        ],
        "requires_human_review": [
            "accept_taxonomy_delta",
            "apply_registry_patch",
            "add_halt_code",
            "add_move_kind",
            "change_promotion_rule",
            "change_authority_class",
        ],
        "forbidden": [
            "self_accept_delta",
            "self_authorize_registry_mutation",
            "promote_label_to_truth",
            "widen_authority_from_usefulness",
        ],
    },
}

TAXONOMY_MOVE_REGISTRY_PATCH = {
    "schema_version": "taxonomy_move_registry_patch_v0",
    "patch_mode": "future_move_registry_patch_only_do_not_mutate_existing_move_registry",
    "candidate_moves": [
        {
            "move_id": "taxonomy.pressure.record.v0",
            "move_kind": "PROPOSAL_ONLY",
            "applies_when": "halt_code in eligible_taxonomy_halts",
            "action": "emit taxonomy_pressure_record",
            "may_mutate_registry": False,
            "authority_required": "AUTHORIZED_LOCAL_FOR_RECORD_ONLY",
        },
        {
            "move_id": "taxonomy.delta.propose.v0",
            "move_kind": "PROPOSAL_ONLY",
            "applies_when": "taxonomy_pressure_record exists and existing_vocab_test exists",
            "action": "emit taxonomy_delta and taxonomy_upgrade_proposal",
            "may_mutate_registry": False,
            "authority_required": "AUTHORIZED_LOCAL_FOR_PROPOSAL_ONLY",
        },
        {
            "move_id": "taxonomy.registry.patch_after_review.v0",
            "move_kind": "LOCAL_REGISTRY_PATCH",
            "applies_when": "review.decision == ACCEPTED_LOCAL and review.registry_patch_allowed == true",
            "action": "apply local registry patch and emit taxonomy_evolution_receipt",
            "may_mutate_registry": True,
            "authority_required": "REQUIRES_HUMAN_REVIEW_SATISFIED_BY_REVIEW_RECORD",
        },
    ],
    "law": [
        "Candidate moves are not registered by this policy.",
        "Move-registry changes are patch-only.",
        "No move is added without applies_when/action/emits/halt behavior.",
    ],
}

DAY6_DEMO_LABEL_SPLIT_PLAN = {
    "schema_version": "day6_demo_label_split_plan_v0",
    "demo_name": "DAY6_LABEL_SPLIT",
    "trigger_halt": "STOP_UNDERTYPED_OBJECT",
    "observed_pressure": "Object labeled RECEIPT is carrying receipt body plus projection view.",
    "existing_vocab_test_expected": "RECEIPT alone overclaims; SPLIT is smallest honest repair.",
    "expected_delta_kind": "SPLIT",
    "expected_status": "PROPOSED",
    "review_decision": "ACCEPTED_LOCAL",
    "patch_status": "APPLIED_LOCAL",
    "must_not_impersonate": [
        "truth creation",
        "authority widening",
        "proof of receipt correctness",
    ],
}

DAY6_DEMO_HALT_REFINE_PLAN = {
    "schema_version": "day6_demo_halt_refine_plan_v0",
    "demo_name": "DAY6_HALT_REFINE",
    "trigger_halt": "STOP_VISIBLE_GOTCHA",
    "observed_pressure": "Readout reports repeated_states=true while trace state signatures are distinct.",
    "existing_vocab_test_expected": "STOP_VISIBLE_GOTCHA fits but is too coarse; STOP_PROJECTION_BUG is smaller.",
    "expected_delta_kind": "REFINE",
    "expected_current_term": "STOP_VISIBLE_GOTCHA",
    "expected_refined_term": "STOP_PROJECTION_BUG",
    "expected_status": "PROPOSED",
    "review_decision": "DEFERRED",
    "patch_status": "NOT_APPLIED",
}

DAY6_DEMO_MISSING_MOVE_DELTA_PLAN = {
    "schema_version": "day6_demo_missing_move_delta_plan_v0",
    "demo_name": "DAY6_MISSING_MOVE_DELTA",
    "trigger_halt": "STOP_NEEDS_NEW_MOVE",
    "observed_pressure": "State is valid and next lawful operation is clear, but no registered move exists.",
    "existing_vocab_test_expected": "Existing move kinds do not cover boundary emission after completed unit.",
    "expected_delta_kind": "ADD_MOVE_KIND",
    "candidate_move_id": "boundary.emit_next_unit.v0",
    "candidate_move_required_fields": [
        "applies_when",
        "action",
        "emits",
        "halt_behavior",
    ],
    "expected_status": "PROPOSED",
    "review_decision": "DEFERRED",
    "patch_status": "NOT_APPLIED",
}

DAY6_DEMO_WITHHOLD_PLAN = {
    "schema_version": "day6_demo_withhold_plan_v0",
    "demo_name": "DAY6_WITHHOLD",
    "trigger_halt": "STOP_TAXONOMY_GAP",
    "observed_pressure": "Object appears mixed, but evidence cannot distinguish receipt+projection from receipt+policy.",
    "existing_vocab_test_expected": "All candidate labels overstate.",
    "expected_delta_kind": "WITHHOLD",
    "expected_status": "WITHHELD",
    "review_decision": "WITHHELD",
    "patch_status": "NOT_APPLIED",
    "allowed_next_handling": [
        "collect more trace/receipt evidence",
        "factor object if possible",
        "do not classify yet",
    ],
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "taxonomy_registry_schema": "data/taxonomy_evolution_v0/taxonomy_registry_schema_v0.json",
    "taxonomy_trigger_policy": "data/taxonomy_evolution_v0/taxonomy_trigger_policy_v0.json",
    "taxonomy_pressure_record_schema": "data/taxonomy_evolution_v0/taxonomy_pressure_record_schema_v0.json",
    "existing_vocab_test_schema": "data/taxonomy_evolution_v0/existing_vocab_test_schema_v0.json",
    "taxonomy_delta_schema": "data/taxonomy_evolution_v0/taxonomy_delta_schema_v0.json",
    "taxonomy_upgrade_proposal_schema": "data/taxonomy_evolution_v0/taxonomy_upgrade_proposal_schema_v0.json",
    "taxonomy_review_record_schema": "data/taxonomy_evolution_v0/taxonomy_review_record_schema_v0.json",
    "taxonomy_registry_patch_schema": "data/taxonomy_evolution_v0/taxonomy_registry_patch_schema_v0.json",
    "taxonomy_evolution_receipt_schema": "data/taxonomy_evolution_v0/taxonomy_evolution_receipt_schema_v0.json",
    "taxonomy_authority_patch": "data/taxonomy_evolution_v0_patches/taxonomy_authority_patch_v0.json",
    "taxonomy_move_registry_patch": "data/taxonomy_evolution_v0_patches/taxonomy_move_registry_patch_v0.json",
    "day6_demo_label_split": "data/taxonomy_evolution_v0_demo/day6_demo_label_split.json",
    "day6_demo_halt_refine": "data/taxonomy_evolution_v0_demo/day6_demo_halt_refine.json",
    "day6_demo_missing_move_delta": "data/taxonomy_evolution_v0_demo/day6_demo_missing_move_delta.json",
    "day6_demo_withhold": "data/taxonomy_evolution_v0_demo/day6_demo_withhold.json",
    "taxonomy_evolution_demo_receipt": "data/taxonomy_evolution_v0_demo/taxonomy_evolution_demo_receipt.json",
    "implementation_receipt": "data/taxonomy_evolution_v0_implementation_receipts/<receipt_id>.json",
}

ACCEPTANCE_GATES = {
    "TEP0_source_surface_verified": {"required": True, "description": "Consumes Day 5 jurisdiction gate, Day 4 move registry, Day 3 halt vocabulary, proceed adapter, trace ledger, and local regime."},
    "TEP1_taxonomy_registry_schema_declared": {"required": True, "description": "Typed taxonomy registry schema is declared."},
    "TEP2_eligible_trigger_halt_set_declared": {"required": True, "description": "Taxonomy triggers are explicit; authority halts are context-only unless mapped."},
    "TEP3_taxonomy_pressure_record_schema_declared": {"required": True, "description": "Pressure record is separate from proposed delta."},
    "TEP4_existing_vocabulary_test_required_before_delta": {"required": True, "description": "No existing_vocab_test, no taxonomy_delta."},
    "TEP5_ADD_star_forbidden_before_existing_vocab_test": {"required": True, "description": "ADD_* is last and requires failed existing vocabulary test."},
    "TEP6_smallest_honest_repair_required": {"required": True, "description": "Deltas must carry smallest_honest_reading."},
    "TEP7_delta_includes_must_not_impersonate": {"required": True, "description": "Deltas must state what they do not mean."},
    "TEP8_delta_includes_allowed_next_handling": {"required": True, "description": "Deltas must specify lawful next handling."},
    "TEP9_proposal_does_not_mutate_registry": {"required": True, "description": "Upgrade proposal is record-only."},
    "TEP10_review_required_before_ACCEPTED_LOCAL": {"required": True, "description": "ACCEPTED_LOCAL requires explicit review record."},
    "TEP11_only_ACCEPTED_LOCAL_review_may_create_APPLIED_LOCAL_patch": {"required": True, "description": "Local registry patch requires accepted review."},
    "TEP12_taxonomy_patch_local_and_receipt_linked": {"required": True, "description": "Patch is local and receipt-linked."},
    "TEP13_taxonomy_upgrade_does_not_widen_authority": {"required": True, "description": "Vocabulary does not create authority."},
    "TEP14_taxonomy_upgrade_does_not_promote_truth_theorem_proof_status": {"required": True, "description": "Vocabulary does not create truth/proof/theorem status."},
    "TEP15_WITHHOLD_valid_not_failure": {"required": True, "description": "Withholding is lawful when labels would overstate."},
    "TEP16_move_registry_changes_patch_only": {"required": True, "description": "Taxonomy-related moves are future patch entries only."},
    "TEP17_day7_global_taxonomy_final_closure_not_implemented": {"required": True, "description": "No global taxonomy, no final closure."},
}

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
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def validate_inputs() -> List[str]:
    failures: List[str] = []

    juris_impl = read_json(JURIS_IMPL_RECEIPT_PATH)
    juris_policy = read_json(JURIS_POLICY_PATH)
    juris_policy_receipt = read_json(JURIS_POLICY_RECEIPT_PATH)
    juris_verdict = read_json(JURIS_VERDICT_ENUM_PATH)
    juris_authority_receipt = read_json(JURIS_AUTHORITY_RECEIPT_PATH)
    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    move_registry = read_json(MOVE_REGISTRY_PATH)
    move_admission = read_json(MOVE_ADMISSION_GATE_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime = read_json(LOCAL_REGIME_V1_PATH)

    if juris_impl.get("receipt_id") != JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"juris_impl_receipt_id_wrong:{juris_impl.get('receipt_id')}")
    if juris_impl.get("gate") != "PASS":
        failures.append(f"juris_impl_gate_not_PASS:{juris_impl.get('gate')}")
    if juris_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"juris_impl_terminal_not_DONE:{juris_impl.get('terminal')}")
    metrics = juris_impl.get("aggregate_metrics", {})
    if metrics.get("authority_verdict_record_count") != 5:
        failures.append(f"juris_verdict_count_wrong:{metrics.get('authority_verdict_record_count')}")
    for key in [
        "non_authorized_move_execution_count",
        "selector_from_admissible_without_authority_count",
        "proposal_accepted_count",
        "proposal_executed_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "jurisdiction_profile_mutation_count",
        "human_silence_authorized_count",
        "day6_taxonomy_evolution_count",
        "global_governance_claim_count",
        "final_authority_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"juris_metric_not_zero:{key}:{metrics.get(key)}")

    if juris_policy.get("policy_id") != JURISDICTION_GATE_POLICY_ID:
        failures.append(f"juris_policy_id_wrong:{juris_policy.get('policy_id')}")
    if juris_policy_receipt.get("receipt_id") != JURISDICTION_GATE_POLICY_RECEIPT_ID:
        failures.append(f"juris_policy_receipt_id_wrong:{juris_policy_receipt.get('receipt_id')}")
    if juris_policy_receipt.get("gate") != "PASS":
        failures.append(f"juris_policy_receipt_gate_not_PASS:{juris_policy_receipt.get('gate')}")
    if juris_verdict.get("verdict_to_halt", {}).get("REQUIRES_HUMAN_REVIEW") != "STOP_HUMAN_REVIEW_REQUIRED":
        failures.append("juris_verdict_human_review_mapping_wrong")
    if juris_authority_receipt.get("gate") != "PASS":
        failures.append("juris_authority_receipt_not_pass")
    counts = juris_authority_receipt.get("jurisdiction", {}).get("verdict_counts", {})
    for verdict in ["AUTHORIZED_LOCAL", "REQUIRES_PROPOSAL", "REQUIRES_EXTRACTION", "REQUIRES_HUMAN_REVIEW", "FORBIDDEN"]:
        if counts.get(verdict) != 1:
            failures.append(f"juris_authority_receipt_count_wrong:{verdict}:{counts.get(verdict)}")

    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID or move_impl.get("gate") != "PASS":
        failures.append("move_impl_source_not_pass")
    if move_registry.get("move_registry_id") != "move_registry_v0" or len(move_registry.get("moves", {})) != 7:
        failures.append("move_registry_source_wrong")
    if move_admission.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append("move_admission_not_deferred")

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_impl_source_not_pass")
    halt_entries = halt_vocab.get("entries", {})
    for code in ELIGIBLE_TRIGGER_HALTS:
        if code not in halt_entries:
            failures.append(f"halt_vocab_missing_taxonomy_trigger:{code}")
    for code in ["STOP_AUTHORITY_VIOLATION", "STOP_NEEDS_NEW_MOVE", "STOP_NEEDS_EXTRACTION"]:
        if code not in halt_entries:
            failures.append(f"halt_vocab_missing_required:{code}")
    if "NO_APPLICABLE_MOVE" in halt_entries:
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")

    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal_ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_wrong")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    for path in [
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
    ]:
        if not tracked(path):
            failures.append(f"source_artifact_not_tracked:{path.relative_to(ROOT).as_posix()}")

    return failures

def validate_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{policy.get('target_unit_id')}")
    if policy.get("policy_id") != receipt.get("policy_id"):
        failures.append("policy_receipt_id_mismatch")

    registry = policy.get("taxonomy_registry_schema", {})
    for field in ["taxonomy_registry_id", "schema_version", "registries", "registry_law"]:
        if field not in registry.get("required_fields", []):
            failures.append(f"taxonomy_registry_schema_required_missing:{field}")
    for law in [
        "labels carry no authority by themselves",
        "proposals do not mutate registry",
        "existing vocabulary must be tested before ADD",
    ]:
        if law not in registry.get("registry_law", []):
            failures.append(f"registry_law_missing:{law}")

    trigger = policy.get("taxonomy_trigger_policy", {})
    if trigger.get("eligible_trigger_halts") != ELIGIBLE_TRIGGER_HALTS:
        failures.append(f"eligible_trigger_halts_wrong:{trigger.get('eligible_trigger_halts')}")
    if trigger.get("authority_halts_context_only") != AUTHORITY_HALTS_CONTEXT_ONLY:
        failures.append(f"authority_context_only_wrong:{trigger.get('authority_halts_context_only')}")

    pressure = policy.get("taxonomy_pressure_record_schema", {})
    if pressure.get("pressure_is_not_delta") is not True:
        failures.append("pressure_record_not_separated_from_delta")

    vocab_test = policy.get("existing_vocab_test_schema", {})
    if "No existing_vocab_test, no taxonomy_delta." not in vocab_test.get("law", []):
        failures.append("existing_vocab_test_law_missing")
    if "ADD_* is last." not in vocab_test.get("law", []):
        failures.append("ADD_last_law_missing")
    if "WITHHOLD" not in vocab_test.get("recommended_outcomes", []):
        failures.append("WITHHOLD_outcome_missing")

    delta = policy.get("taxonomy_delta_schema", {})
    if delta.get("delta_kinds") != DELTA_KINDS:
        failures.append(f"delta_kinds_wrong:{delta.get('delta_kinds')}")
    for field in ["pressure_ref", "existing_vocab_test_ref", "smallest_honest_reading", "must_not_impersonate", "allowed_next_handling"]:
        if field not in delta.get("required_fields", []):
            failures.append(f"delta_required_missing:{field}")
    for law in [
        "Delta does not widen authority.",
        "Delta does not promote theorem status.",
        "Delta does not mutate registry.",
    ]:
        if law not in delta.get("law", []):
            failures.append(f"delta_law_missing:{law}")

    upgrade = policy.get("taxonomy_upgrade_proposal_schema", {})
    if "Upgrade proposal is not acceptance." not in upgrade.get("law", []):
        failures.append("upgrade_not_acceptance_law_missing")
    if "Upgrade proposal is not registry mutation." not in upgrade.get("law", []):
        failures.append("upgrade_not_mutation_law_missing")

    review = policy.get("taxonomy_review_record_schema", {})
    if review.get("canonical_accept_decision") != "ACCEPTED_LOCAL":
        failures.append(f"canonical_accept_wrong:{review.get('canonical_accept_decision')}")
    if review.get("accepted_by_review_is_alias_only") is not True:
        failures.append("accepted_by_review_alias_flag_missing")
    if "No review record, no registry patch." not in review.get("law", []):
        failures.append("no_review_no_patch_law_missing")

    patch = policy.get("taxonomy_registry_patch_schema", {})
    if "Only accepted review may create APPLIED_LOCAL patch." not in patch.get("law", []):
        failures.append("accepted_review_patch_law_missing")
    if "APPLIED_LOCAL" not in patch.get("status_enum", []):
        failures.append("APPLIED_LOCAL_status_missing")

    receipt_schema = policy.get("taxonomy_evolution_receipt_schema", {})
    for law in [
        "Receipt does not create truth.",
        "Receipt does not authorize moves.",
        "Receipt does not prove theorem status.",
        "Receipt does not claim global closure.",
    ]:
        if law not in receipt_schema.get("law", []):
            failures.append(f"receipt_law_missing:{law}")

    authority = policy.get("taxonomy_authority_patch", {})
    if authority.get("patch_mode") != "future_jurisdiction_profile_patch_only_do_not_mutate_existing_profile":
        failures.append(f"taxonomy_authority_patch_mode_wrong:{authority.get('patch_mode')}")
    if "self_accept_delta" not in authority.get("taxonomy_authority", {}).get("forbidden", []):
        failures.append("taxonomy_authority_missing_self_accept_forbidden")
    if "accept_taxonomy_delta" not in authority.get("taxonomy_authority", {}).get("requires_human_review", []):
        failures.append("taxonomy_authority_missing_accept_requires_review")

    move_patch = policy.get("taxonomy_move_registry_patch", {})
    if move_patch.get("patch_mode") != "future_move_registry_patch_only_do_not_mutate_existing_move_registry":
        failures.append(f"taxonomy_move_registry_patch_mode_wrong:{move_patch.get('patch_mode')}")
    move_ids = [m.get("move_id") for m in move_patch.get("candidate_moves", [])]
    for move_id in ["taxonomy.pressure.record.v0", "taxonomy.delta.propose.v0", "taxonomy.registry.patch_after_review.v0"]:
        if move_id not in move_ids:
            failures.append(f"taxonomy_candidate_move_missing:{move_id}")
    if "Candidate moves are not registered by this policy." not in move_patch.get("law", []):
        failures.append("candidate_moves_not_registered_law_missing")

    demo_expectations = {
        "day6_demo_label_split_plan": ("expected_delta_kind", "SPLIT"),
        "day6_demo_halt_refine_plan": ("expected_delta_kind", "REFINE"),
        "day6_demo_missing_move_delta_plan": ("expected_delta_kind", "ADD_MOVE_KIND"),
        "day6_demo_withhold_plan": ("expected_delta_kind", "WITHHOLD"),
    }
    for demo_key, (field, expected) in demo_expectations.items():
        if policy.get(demo_key, {}).get(field) != expected:
            failures.append(f"{demo_key}_{field}_wrong:{policy.get(demo_key, {}).get(field)}")
    if policy.get("day6_demo_label_split_plan", {}).get("review_decision") != "ACCEPTED_LOCAL":
        failures.append("label_split_review_not_ACCEPTED_LOCAL")
    if policy.get("day6_demo_withhold_plan", {}).get("patch_status") != "NOT_APPLIED":
        failures.append("withhold_patch_status_not_NOT_APPLIED")

    gates = policy.get("acceptance_gates", {})
    for gate_id in ACCEPTANCE_GATES:
        if gates.get(gate_id, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate_id}")

    guards = policy.get("authority_guards", {})
    for key in [
        "taxonomy_evolution_policy_built",
        "source_jurisdiction_gate_consumed",
        "source_move_registry_consumed",
        "source_halt_vocabulary_consumed",
        "source_proceed_adapter_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_deltas_emitted_by_policy",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
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
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != NEXT_GOAL:
        failures.append(f"terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"terminal_stop_not_null:{terminal.get('stop_code')}")

    return failures

def build_policy(write_outputs: bool = True) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    failures = validate_inputs()

    policy_seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_jurisdiction_impl": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "eligible_triggers": ELIGIBLE_TRIGGER_HALTS,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "taxonomy_evolution_policy_built": True,
        "source_jurisdiction_gate_consumed": True,
        "source_move_registry_consumed": True,
        "source_halt_vocabulary_consumed": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_deltas_emitted_by_policy": False,
        "source_jurisdiction_gate_modified": False,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "taxonomy_registry_mutated_by_policy": False,
        "move_registry_mutated_by_policy": False,
        "halt_vocabulary_mutated_by_policy": False,
        "proposal_accepted_by_runtime": False,
        "proposal_executed_by_runtime": False,
        "review_fabricated_by_runtime": False,
        "accepted_patch_without_review": False,
        "label_treated_as_truth": False,
        "taxonomy_delta_widened_authority": False,
        "taxonomy_delta_promoted_theorem_status": False,
        "add_used_before_existing_vocab_test": False,
        "authority_halt_auto_triggered_taxonomy": False,
        "day7_global_taxonomy_implemented": False,
        "global_taxonomy_claimed": False,
        "final_closure_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
    }

    policy = {
        "schema_version": "taxonomy_evolution_v0_policy_v0",
        "policy_type": "TAXONOMY_EVOLUTION_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_policy_id": JURISDICTION_GATE_POLICY_ID,
        "source_jurisdiction_gate_policy_receipt_id": JURISDICTION_GATE_POLICY_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Convert typed halt pressure into reviewable taxonomy deltas without self-authorized mutation.",
            "core_law": "No halt, no taxonomy upgrade. Existing vocabulary first. ADD last. No taxonomy change creates truth. No proposal mutates registry. No accepted patch without review.",
            "non_goal": "no final taxonomy, no runtime self-acceptance, no authority widening, no theorem/proof/truth promotion, no Day 7 global taxonomy",
            "interpretation": "Structured vocabulary pressure, not self-modification.",
        },
        "taxonomy_registry_schema": TAXONOMY_REGISTRY_SCHEMA,
        "taxonomy_trigger_policy": TAXONOMY_TRIGGER_POLICY,
        "taxonomy_pressure_record_schema": TAXONOMY_PRESSURE_RECORD_SCHEMA,
        "existing_vocab_test_schema": EXISTING_VOCAB_TEST_SCHEMA,
        "taxonomy_delta_schema": TAXONOMY_DELTA_SCHEMA,
        "taxonomy_upgrade_proposal_schema": TAXONOMY_UPGRADE_PROPOSAL_SCHEMA,
        "taxonomy_review_record_schema": TAXONOMY_REVIEW_RECORD_SCHEMA,
        "taxonomy_registry_patch_schema": TAXONOMY_REGISTRY_PATCH_SCHEMA,
        "taxonomy_evolution_receipt_schema": TAXONOMY_EVOLUTION_RECEIPT_SCHEMA,
        "taxonomy_authority_patch": TAXONOMY_AUTHORITY_PATCH,
        "taxonomy_move_registry_patch": TAXONOMY_MOVE_REGISTRY_PATCH,
        "day6_demo_label_split_plan": DAY6_DEMO_LABEL_SPLIT_PLAN,
        "day6_demo_halt_refine_plan": DAY6_DEMO_HALT_REFINE_PLAN,
        "day6_demo_missing_move_delta_plan": DAY6_DEMO_MISSING_MOVE_DELTA_PLAN,
        "day6_demo_withhold_plan": DAY6_DEMO_WITHHOLD_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_taxonomy_evolution_policy": True,
            "read_taxonomy_evolution_policy_receipt": True,
            "write_taxonomy_registry_schema_artifact": True,
            "write_taxonomy_trigger_policy_artifact": True,
            "write_taxonomy_pressure_record_schema_artifact": True,
            "write_existing_vocab_test_schema_artifact": True,
            "write_taxonomy_delta_schema_artifact": True,
            "write_taxonomy_upgrade_proposal_schema_artifact": True,
            "write_taxonomy_review_record_schema_artifact": True,
            "write_taxonomy_registry_patch_schema_artifact": True,
            "write_taxonomy_evolution_receipt_schema_artifact": True,
            "write_taxonomy_authority_patch_artifact": True,
            "write_taxonomy_move_registry_patch_artifact": True,
            "emit_day6_demo_label_split": True,
            "emit_day6_demo_halt_refine": True,
            "emit_day6_demo_missing_move_delta": True,
            "emit_day6_demo_withhold": True,
            "emit_taxonomy_evolution_demo_receipt": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "mutate_existing_jurisdiction_gate": True,
            "mutate_existing_move_registry": True,
            "mutate_existing_halt_vocabulary": True,
            "mutate_existing_trace_files": True,
            "mutate_existing_receipt_files": True,
            "mutate_existing_readout_files": True,
            "modify_trace_ledger_runner_module": True,
            "modify_proceed_adapter_module": True,
            "modify_local_regime_v1": True,
            "taxonomy_change_without_halt_pressure": True,
            "delta_without_existing_vocab_test": True,
            "ADD_before_existing_vocab_test": True,
            "proposal_treated_as_acceptance": True,
            "proposal_mutates_registry": True,
            "runtime_accepts_own_delta": True,
            "review_record_fabricated_by_runtime": True,
            "patch_without_ACCEPTED_LOCAL_review": True,
            "label_treated_as_truth": True,
            "taxonomy_patch_widens_authority": True,
            "taxonomy_patch_promotes_theorem_status": True,
            "move_kind_added_without_required_fields": True,
            "under_typed_object_forced_into_fake_label": True,
            "authority_halt_auto_triggers_taxonomy": True,
            "day7_global_taxonomy_implemented": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "global_taxonomy_claim": True,
            "final_closure_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_terminal": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_deltas": True,
            "does_not_mutate_existing_artifacts": True,
            "does_not_modify_source_modules": True,
            "does_not_modify_source_regime": True,
            "does_not_modify_move_registry": True,
            "does_not_modify_halt_vocabulary": True,
            "does_not_modify_jurisdiction_profile": True,
            "does_not_accept_or_execute_proposals": True,
            "does_not_fabricate_review": True,
            "does_not_apply_registry_patch": True,
            "does_not_treat_label_as_truth": True,
            "does_not_widen_authority": True,
            "does_not_promote_theorem_status": True,
            "does_not_implement_day7_global_taxonomy": True,
            "next_unit_required_for_implementation": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_jurisdiction_impl": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "taxonomy_evolution_v0_policy_receipt_v0",
        "receipt_type": "TAXONOMY_EVOLUTION_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_policy_id": JURISDICTION_GATE_POLICY_ID,
        "source_jurisdiction_gate_policy_receipt_id": JURISDICTION_GATE_POLICY_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "taxonomy_registry_schema": TAXONOMY_REGISTRY_SCHEMA,
        "taxonomy_trigger_policy": TAXONOMY_TRIGGER_POLICY,
        "taxonomy_pressure_record_schema": TAXONOMY_PRESSURE_RECORD_SCHEMA,
        "existing_vocab_test_schema": EXISTING_VOCAB_TEST_SCHEMA,
        "taxonomy_delta_schema": TAXONOMY_DELTA_SCHEMA,
        "taxonomy_upgrade_proposal_schema": TAXONOMY_UPGRADE_PROPOSAL_SCHEMA,
        "taxonomy_review_record_schema": TAXONOMY_REVIEW_RECORD_SCHEMA,
        "taxonomy_registry_patch_schema": TAXONOMY_REGISTRY_PATCH_SCHEMA,
        "taxonomy_evolution_receipt_schema": TAXONOMY_EVOLUTION_RECEIPT_SCHEMA,
        "taxonomy_authority_patch": TAXONOMY_AUTHORITY_PATCH,
        "taxonomy_move_registry_patch": TAXONOMY_MOVE_REGISTRY_PATCH,
        "day6_demo_label_split_plan": DAY6_DEMO_LABEL_SPLIT_PLAN,
        "day6_demo_halt_refine_plan": DAY6_DEMO_HALT_REFINE_PLAN,
        "day6_demo_missing_move_delta_plan": DAY6_DEMO_MISSING_MOVE_DELTA_PLAN,
        "day6_demo_withhold_plan": DAY6_DEMO_WITHHOLD_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    failures.extend(validate_policy(policy, receipt))
    policy["failures"] = failures
    receipt["failures"] = failures
    policy["gate"] = "PASS" if not failures else "FAIL"
    receipt["gate"] = policy["gate"]

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{policy_id}.json", policy)
        write_json(OUT_RECEIPT_DIR / f"{policy_id}.json", receipt)

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"taxonomy_evolution_policy_id={policy['policy_id']}")
    print(f"taxonomy_evolution_policy_receipt_id={receipt['receipt_id']}")
    print(f"taxonomy_evolution_policy_path=data/taxonomy_evolution_v0_policies/{policy['policy_id']}.json")
    print(f"taxonomy_evolution_policy_receipt_path=data/taxonomy_evolution_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
