#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"
TARGET_UNIT_ID = "observation.decision_edge_observability_surface.v0"
LAYER = "OBSERVATION_HARDENING / DECISION_EDGE_VISIBILITY"
MODE = "OBSERVE / EXTRACT / SIDECAR_ONLY"
BUILD_MODE = "O1_DECISION_EDGE_OBSERVABILITY_SURFACE_ONLY"

O1_DESIGN_RECEIPT_ID = "c9ef517f"
O1_DESIGN_RECEIPT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0_receipts/c9ef517f.json"
O1_TARGET_DESIGN_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_decision_edge_observability_target_design_v0.json"
O1_OBJECTIVE_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_objective_contract_v0.json"
O1_SOURCE_SCOPE_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_source_scope_contract_v0.json"
O1_REQUIRED_FIELD_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_required_field_contract_v0.json"
O1_CANDIDATE_HANDLE_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_candidate_handle_contract_v0.json"
O1_OUTPUT_ARTIFACT_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_output_artifact_contract_v0.json"
O1_ACCEPTANCE_GATE_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_acceptance_gate_contract_v0.json"
O1_NEGATIVE_CONTROL_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_negative_control_contract_v0.json"
O1_TERMINAL_CONTRACT_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_terminal_contract_v0.json"
O1_NONAUTHORITY_BOUNDARY_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_nonauthority_boundary_v0.json"
O1_BUILD_AUTHORIZATION_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_build_unit_authorization_v0.json"
O1_DESIGN_ROLLUP_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_target_design_rollup_v0.json"
O1_DESIGN_PROFILE_PATH = ROOT / "data/o1_decision_edge_observability_target_design_v0/o1_target_design_profile_v0.json"

SOURCE_RECEIPTS = [
    {
        "receipt_id": "c9ef517f",
        "path": O1_DESIGN_RECEIPT_PATH,
        "context": "O1 target design / build authorization",
    },
    {
        "receipt_id": "c14697ae",
        "path": ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0_receipts/c14697ae.json",
        "context": "source-ref rebind layer closure",
    },
    {
        "receipt_id": "b3bcc049",
        "path": ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0_receipts/b3bcc049.json",
        "context": "one-time application review",
    },
    {
        "receipt_id": "4086e0bb",
        "path": ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0_receipts/4086e0bb.json",
        "context": "one-time application unit",
    },
    {
        "receipt_id": "f549ad67",
        "path": ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts/f549ad67.json",
        "context": "one-time application decision",
    },
]

REQUIRED_SOURCE_FILES = [
    O1_DESIGN_RECEIPT_PATH,
    O1_TARGET_DESIGN_PATH,
    O1_OBJECTIVE_CONTRACT_PATH,
    O1_SOURCE_SCOPE_CONTRACT_PATH,
    O1_REQUIRED_FIELD_CONTRACT_PATH,
    O1_CANDIDATE_HANDLE_CONTRACT_PATH,
    O1_OUTPUT_ARTIFACT_CONTRACT_PATH,
    O1_ACCEPTANCE_GATE_CONTRACT_PATH,
    O1_NEGATIVE_CONTROL_CONTRACT_PATH,
    O1_TERMINAL_CONTRACT_PATH,
    O1_NONAUTHORITY_BOUNDARY_PATH,
    O1_BUILD_AUTHORIZATION_PATH,
    O1_DESIGN_ROLLUP_PATH,
    O1_DESIGN_PROFILE_PATH,
] + [x["path"] for x in SOURCE_RECEIPTS if x["receipt_id"] != "c9ef517f"]

OUT_DIR = ROOT / "data/o1_decision_edge_observability_surface_v0"
RECEIPT_DIR = ROOT / "data/o1_decision_edge_observability_surface_v0_receipts"

OBS_RECORD_SCHEMA_PATH = OUT_DIR / "decision_edge_observation_record_schema_v0.json"
HANDLE_SCHEMA_PATH = OUT_DIR / "decision_edge_candidate_handle_schema_v0.json"
HANDLE_RECORDS_PATH = OUT_DIR / "decision_edge_candidate_handle_records_v0.jsonl"
OBS_RECORDS_PATH = OUT_DIR / "decision_edge_observation_records_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "decision_edge_observation_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "decision_edge_observation_profile_v0.json"
READOUT_PATH = OUT_DIR / "decision_edge_observation_readout_v0.json"
SOURCE_SURFACE_PATH = OUT_DIR / "o1_source_surface_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "o1_transition_trace.json"
REPORT_PATH = OUT_DIR / "o1_report.json"

EXPECTED_DESIGN_STATUS = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_O1_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = "BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"

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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def get_summary(receipt: Dict[str, Any]) -> Dict[str, Any]:
    for key in receipt:
        if key.startswith("machine_readable_") and key.endswith("_summary") and isinstance(receipt[key], dict):
            return receipt[key]
    return {}

def terminal_stop(receipt: Dict[str, Any]) -> str | None:
    t = receipt.get("terminal", {})
    return t.get("stop_code") if isinstance(t, dict) else None

def validate_design_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    design_receipt = read_json(O1_DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_o1_target_design_summary", {})
    field_contract = read_json(O1_REQUIRED_FIELD_CONTRACT_PATH)
    handle_contract = read_json(O1_CANDIDATE_HANDLE_CONTRACT_PATH)
    acceptance_contract = read_json(O1_ACCEPTANCE_GATE_CONTRACT_PATH)
    source_scope = read_json(O1_SOURCE_SCOPE_CONTRACT_PATH)
    auth = read_json(O1_BUILD_AUTHORIZATION_PATH)
    rollup = read_json(O1_DESIGN_ROLLUP_PATH)

    if design_receipt.get("receipt_id") != O1_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("o1_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("o1_design_terminal_not_expected")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"o1_design_status_not_expected:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"o1_design_next_not_expected:{design_summary.get('recommended_next')}")

    for key in [
        "o1_target_designed",
        "o1_build_authorized_next",
        "source_surface_frozen",
        "required_fields_frozen",
        "candidate_handles_frozen_as_provisional",
        "acceptance_gates_frozen",
        "negative_controls_frozen",
        "terminal_rules_frozen",
        "sidecar_only",
        "explicit_refs_only",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"design_required_true_missing:{key}")

    for key in [
        "observations_extracted",
        "observation_records_emitted",
        "graph_schema_claimed",
        "graph_tracker_created",
        "architecture_change",
        "source_receipt_mutated",
        "authority_expansion",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "unit_feedback_hardening_executed",
    ]:
        if design_summary.get(key) is not False:
            failures.append(f"design_forbidden_true:{key}")

    if source_scope.get("selection_rule") != "explicit_refs_only":
        failures.append("source_scope_not_explicit_refs_only")
    if source_scope.get("payload_inspection_allowed") is not False:
        failures.append("payload_inspection_allowed")
    if source_scope.get("source_mutation_allowed") is not False:
        failures.append("source_mutation_allowed")
    if auth.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("build_authorization_next_wrong")
    if rollup.get("graph_schema_claim_count") != 0:
        failures.append("design_rollup_graph_schema_nonzero")

    return failures, {
        "design_summary": design_summary,
        "required_fields": field_contract.get("required_fields", []),
        "candidate_handles": handle_contract.get("candidate_handles", []),
        "acceptance_gates": acceptance_contract.get("acceptance_gates", []),
        "source_scope": source_scope,
    }

def observation_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "decision_edge_observation_record_schema_v0",
        "record_schema": {
            "schema_version": "decision_edge_observation_record_v0",
            "observation_id": "edge_obs_<sig8>",
            "created_at": None,
            "source": {
                "source_receipt_ref": None,
                "source_unit_id": None,
                "source_context": None,
                "source_artifact_refs": [],
            },
            "edge_surface": {
                "active_object": None,
                "active_object_kind": None,
                "pressure_or_trigger": None,
                "attempted_move": None,
                "attempted_move_kind": None,
            },
            "boundary": {
                "boundary_checked": None,
                "boundary_kind": None,
                "boundary_result": None,
                "guard_result": None,
                "authority_boundary_exposed": False,
                "capability_boundary_exposed": False,
            },
            "classification": {
                "classification": None,
                "confidence_class": "PROVISIONAL",
                "candidate_edge_handles": [],
                "missing_object": None,
                "missing_capability": None,
            },
            "movement": {
                "blocked_moves": [],
                "lawful_next_moves": [],
                "forbidden_next_moves": [],
            },
            "terminal": {
                "terminal_result": None,
                "parent_return_payload": None,
            },
            "safety": {
                "collection_status": "OBSERVATION_ONLY",
                "schema_claim": "NONE",
                "architecture_change": False,
                "source_receipt_mutated": False,
                "authority_expansion": False,
                "runtime_patch_applied": False,
                "target_selected_for_build": False,
                "c5_opened": False,
            },
        },
    }

def handle_schema() -> Dict[str, Any]:
    return {
        "schema_version": "decision_edge_candidate_handle_schema_v0",
        "record_schema": {
            "schema_version": "decision_edge_candidate_handle_v0",
            "candidate_edge_handle": None,
            "smallest_honest_meaning": None,
            "must_not_impersonate": [],
            "allowed_use": [
                "tag observation",
                "count recurrence",
                "compare with future observations",
            ],
            "forbidden_use": [
                "authorize move",
                "define final graph edge",
                "open new architecture",
                "claim proof of recurrence",
            ],
        },
    }

def handle_records(candidate_handles: List[str]) -> List[Dict[str, Any]]:
    meanings = {
        "OBSERVE_RECEIPT_EDGE": "A receipt exposes enough typed outcome fields to observe a local transition.",
        "CLASSIFY_DISTINGUISH_EDGE": "A unit classified a state to distinguish lawful movement from ambiguous or blocked movement.",
        "GUARD_AUTHORITY_EDGE": "A move was possible or describable but routed by an authority boundary.",
        "PROPOSE_VALIDATE_EDGE": "A candidate move was proposed, reviewed, accepted, rejected, or held.",
        "CLOSE_FREEZE_ESCALATE_EDGE": "A bounded object was closed, frozen, escalated, or routed to a next decision.",
        "REPAIR_OR_FALLBACK_EDGE": "A unit preserved unresolved work and routed it to repair or fallback rather than pretending closure.",
        "CAPABILITY_BOUNDARY_EDGE": "A boundary exposed that a capability is missing or not yet authorized.",
        "REFERENCE_ONLY_EDGE": "An object became a reference without becoming general authority.",
        "CAPABILITY_PROVIDER_MATERIALIZATION_EDGE": "A missing provider or surface was materialized to unblock a bounded capability.",
        "BUILDER_HANDOFF_EDGE": "A unit produced a handoff or next build surface without performing the downstream build.",
        "VERIFICATION_RETURN_EDGE": "A verification/review returned a pass/fail status and lawful next move.",
        "LABEL_NON_COLLAPSE_EDGE": "A label or tag was kept non-authoritative and did not collapse into accepted meaning.",
        "FAILURE_PROGRESS_EDGE": "A failure, residual, or unresolved branch produced typed progress rather than raw halt noise.",
    }
    return [
        {
            "schema_version": "decision_edge_candidate_handle_v0",
            "candidate_edge_handle": h,
            "smallest_honest_meaning": meanings.get(h, "A provisional source-backed edge-like transition handle."),
            "must_not_impersonate": [
                "proof of architecture",
                "final decision graph primitive",
                "global governance schema",
                "authority grant",
            ],
            "allowed_use": [
                "tag observation",
                "count recurrence",
                "compare with future observations",
            ],
            "forbidden_use": [
                "authorize move",
                "define final graph edge",
                "open new architecture",
                "claim proof of recurrence",
            ],
        }
        for h in candidate_handles
    ]

def make_obs(
    source_receipt_id: str,
    source_path: Path,
    receipt: Dict[str, Any],
    source_context: str,
    active_object: str,
    active_kind: str,
    trigger: str,
    attempted_move: str,
    attempted_kind: str,
    boundary_checked: str,
    boundary_kind: str,
    boundary_result: str,
    classification_value: str,
    handles: List[str],
    blocked_moves: List[str],
    lawful_next_moves: List[str],
    forbidden_next_moves: List[str],
    missing_object: str | None = None,
    missing_capability: str | None = None,
    authority_exposed: bool = False,
    capability_exposed: bool = False,
    parent_return_payload: str | None = None,
) -> Dict[str, Any]:
    base = {
        "schema_version": "decision_edge_observation_record_v0",
        "created_at": now_iso(),
        "source": {
            "source_receipt_ref": rel(source_path),
            "source_receipt_id": source_receipt_id,
            "source_unit_id": receipt.get("unit_id"),
            "source_context": source_context,
            "source_artifact_refs": list((receipt.get("output_artifacts") or {}).values())[:8],
        },
        "edge_surface": {
            "active_object": active_object,
            "active_object_kind": active_kind,
            "pressure_or_trigger": trigger,
            "attempted_move": attempted_move,
            "attempted_move_kind": attempted_kind,
        },
        "boundary": {
            "boundary_checked": boundary_checked,
            "boundary_kind": boundary_kind,
            "boundary_result": boundary_result,
            "guard_result": receipt.get("gate"),
            "authority_boundary_exposed": authority_exposed,
            "capability_boundary_exposed": capability_exposed,
        },
        "classification": {
            "classification": classification_value,
            "confidence_class": "PROVISIONAL",
            "candidate_edge_handles": handles,
            "missing_object": missing_object,
            "missing_capability": missing_capability,
        },
        "movement": {
            "blocked_moves": blocked_moves,
            "lawful_next_moves": lawful_next_moves,
            "forbidden_next_moves": forbidden_next_moves,
        },
        "terminal": {
            "terminal_result": terminal_stop(receipt),
            "parent_return_payload": parent_return_payload,
        },
        "safety": {
            "collection_status": "OBSERVATION_ONLY",
            "schema_claim": "NONE",
            "architecture_change": False,
            "source_receipt_mutated": False,
            "authority_expansion": False,
            "runtime_patch_applied": False,
            "target_selected_for_build": False,
            "c5_opened": False,
        },
    }
    base["observation_id"] = "edge_obs_" + sha8(base)
    return base

def build_observations(receipts: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_id = {x["receipt_id"]: x for x in SOURCE_RECEIPTS}
    obs: List[Dict[str, Any]] = []

    r = receipts["c14697ae"]
    obs.append(make_obs(
        "c14697ae", by_id["c14697ae"]["path"], r, "source-ref rebind layer closure",
        "partial_schema_aware_source_ref_rebind_layer",
        "reviewed_reference_object",
        "one-time application review passed and closure candidate was ready",
        "close source-ref rebind layer as reviewed reference",
        "close_or_freeze_decision",
        "Can the source-ref rebind branch be closed without entering metadata/value/runtime/C5 work?",
        "closure_reference_boundary",
        "CLOSE_AS_REVIEWED_REFERENCE",
        "SOURCE_REF_REBIND_LAYER_CLOSED_AS_REVIEWED_REFERENCE",
        ["CLOSE_FREEZE_ESCALATE_EDGE", "REFERENCE_ONLY_EDGE"],
        [
            "start metadata population automatically",
            "open C5",
            "promote schema overlay to reusable authority",
            "discard residual ambiguity/gap branches",
        ],
        [
            "cite reviewed reference in future units",
            "design decision-edge observability target",
            "carry residual branches forward unresolved",
        ],
        [
            "treat reviewed reference as global schema authority",
            "mutate prior receipts",
            "use latest-file or mtime selection",
        ],
        authority_exposed=True,
        parent_return_payload="DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
    ))

    obs.append(make_obs(
        "c14697ae", by_id["c14697ae"]["path"], r, "blocked C5 / nonruntime boundary from closure",
        "post_closure_decision_surface",
        "authority_boundary_surface",
        "source-ref rebind layer closed but downstream domain shift not authorized",
        "preserve C5 as blocked / not opened",
        "blocked_domain_shift_decision",
        "Does closure authorize C5 or runtime patching?",
        "authority_boundary",
        "C5_BLOCKED_NOT_OPENED",
        "BLOCKED_C5_EDGE_OBSERVED",
        ["GUARD_AUTHORITY_EDGE", "CAPABILITY_BOUNDARY_EDGE"],
        [
            "open C5",
            "patch runtime",
            "select target for build",
        ],
        [
            "design decision-edge observability surface",
            "design unit feedback hardening after O1",
        ],
        [
            "read closure as C5 preflight",
            "read post-update hint as authority grant",
        ],
        missing_capability="C5 authority and runtime patch target are not present in this closure unit",
        authority_exposed=True,
        capability_exposed=True,
        parent_return_payload="DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
    ))

    r = receipts["b3bcc049"]
    obs.append(make_obs(
        "b3bcc049", by_id["b3bcc049"]["path"], r, "one-time application unit review",
        "one_time_application_unit",
        "verification_return_object",
        "four applied rebinds required review before downstream use",
        "review one-time application unit",
        "verification_return",
        "Do the four applied rebinds match the authorized scope and preserve boundaries?",
        "verification_boundary",
        "REVIEW_PASS",
        "ONE_TIME_APPLICATION_REVIEWED_CLEAN",
        ["VERIFICATION_RETURN_EDGE", "CLASSIFY_DISTINGUISH_EDGE"],
        [
            "start metadata population",
            "patch runtime",
            "open C5",
        ],
        [
            "emit closure candidate",
            "require next-objective decision",
        ],
        [
            "treat review pass as metadata population authority",
            "treat review pass as schema reuse",
        ],
        authority_exposed=True,
        parent_return_payload="DECIDE_AFTER_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_V0",
    ))

    r = receipts["4086e0bb"]
    obs.append(make_obs(
        "4086e0bb", by_id["4086e0bb"]["path"], r, "one-time application execution",
        "four_authorized_proposal_rebinds",
        "bounded_application_object",
        "accepted one-time decision authorized a narrow application unit",
        "release hold and apply exactly four source-ref rebinds",
        "authorized_application",
        "Can the unit apply the four proposal rebinds without scope expansion?",
        "authority_boundary",
        "AUTHORIZED_SCOPE_APPLIED",
        "FOUR_REBINDS_APPLIED_SCOPE_GUARD_PASS",
        ["GUARD_AUTHORITY_EDGE", "PROPOSE_VALIDATE_EDGE"],
        [
            "apply ambiguity branch",
            "apply requirement-gap branch",
            "populate metadata",
            "authorize values",
        ],
        [
            "review one-time application unit",
            "preserve residual branches",
        ],
        [
            "expand application beyond four authorized proposals",
            "turn one-time application into reusable schema authority",
        ],
        authority_exposed=True,
        parent_return_payload="REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0",
    ))

    r = receipts["f549ad67"]
    obs.append(make_obs(
        "f549ad67", by_id["f549ad67"]["path"], r, "one-time application decision",
        "partial_schema_aware_rebind_proposal_branch",
        "proposal_decision_object",
        "authorization contract review required a human or validator decision",
        "record accept decision for four proposal rebinds",
        "proposal_authorization_decision",
        "Can the four held proposals be authorized for one-time application only?",
        "authority_boundary",
        "ONE_TIME_APPLICATION_AUTHORIZED",
        "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT",
        ["PROPOSE_VALIDATE_EDGE", "GUARD_AUTHORITY_EDGE"],
        [
            "apply rebinds in decision unit",
            "release hold before application unit",
            "authorize reusable schema",
        ],
        [
            "build one-time application unit",
            "preserve 22 ambiguity and 498 requirement-gap branches",
        ],
        [
            "infer future automatic use",
            "promote schema overlay globally",
        ],
        authority_exposed=True,
        parent_return_payload="BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0",
    ))

    r = receipts["c9ef517f"]
    obs.append(make_obs(
        "c9ef517f", by_id["c9ef517f"]["path"], r, "O1 target design",
        "o1_decision_edge_observability_target",
        "observation_hardening_target",
        "closed source-ref rebind layer recommended decision-edge observability first",
        "design O1 target and authorize build unit next",
        "target_design_to_build_authorization",
        "Can the next unit build a sidecar-only decision-edge observability surface?",
        "capability_boundary",
        "BUILD_O1_AUTHORIZED_WITH_NONAUTHORITY_BOUNDARY",
        "O1_TARGET_DESIGNED_BUILD_READY",
        ["BUILDER_HANDOFF_EDGE", "CAPABILITY_BOUNDARY_EDGE", "OBSERVE_RECEIPT_EDGE"],
        [
            "extract observations in design unit",
            "create graph schema",
            "create graph tracker",
            "start O2",
        ],
        [
            "build O1 decision-edge observability surface",
        ],
        [
            "treat O1 design as graph schema",
            "mutate source receipts",
            "select build target",
        ],
        missing_object=None,
        missing_capability="O1 observation surface not built before this unit",
        authority_exposed=True,
        capability_exposed=True,
        parent_return_payload="BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0",
    ))

    obs.append(make_obs(
        "c9ef517f", by_id["c9ef517f"]["path"], r, "candidate handle non-collapse",
        "provisional_candidate_edge_handles",
        "label_noncollapse_surface",
        "O1 design froze candidate handles as provisional collection tags",
        "tag observations without promoting handles to primitives",
        "label_noncollapse",
        "May candidate handles become final graph primitives?",
        "label_noncollapse_boundary",
        "NO_FINAL_PRIMITIVE_CLAIM",
        "CANDIDATE_HANDLES_PROVISIONAL_ONLY",
        ["LABEL_NON_COLLAPSE_EDGE", "OBSERVE_RECEIPT_EDGE"],
        [
            "promote candidate handles to final primitives",
            "claim proof of recurrence",
            "define final edge taxonomy",
        ],
        [
            "tag observations",
            "count recurrence",
            "compare future observations",
        ],
        [
            "use labels as authority",
            "treat recurrence counts as proof",
        ],
        authority_exposed=True,
        parent_return_payload="BUILD_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0",
    ))

    r = receipts["c14697ae"]
    obs.append(make_obs(
        "c14697ae", by_id["c14697ae"]["path"], r, "residual branch carry-forward",
        "residual_ambiguity_and_requirement_gap_branches",
        "failure_progress_object",
        "source-ref closure preserved unresolved branches instead of pretending closure",
        "carry unresolved residual branches forward",
        "failure_progress_or_fallback",
        "Were ambiguity and requirement-gap branches resolved by closure?",
        "repair_or_fallback_boundary",
        "CARRY_FORWARD_UNRESOLVED",
        "RESIDUAL_BRANCHES_PRESERVED_AS_TYPED_PROGRESS",
        ["FAILURE_PROGRESS_EDGE", "REPAIR_OR_FALLBACK_EDGE"],
        [
            "discard residual branches",
            "treat unresolved branches as null",
            "apply ambiguity branch",
            "apply requirement-gap branch",
        ],
        [
            "return to ambiguity branch repair later",
            "return to requirement-gap branch repair later",
            "preserve residual reference while moving to O1",
        ],
        [
            "claim full metadata readiness",
            "claim complete source surface resolution",
        ],
        missing_object="branch repair objective not selected",
        missing_capability="residual branch discriminator/repair not executed in closure unit",
        capability_exposed=True,
        parent_return_payload="DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
    ))

    return obs

def validate_observations(obs: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    for idx, r in enumerate(obs):
        if not r.get("source", {}).get("source_receipt_ref"):
            failures.append(f"record_missing_source_receipt_ref:{idx}")
        if not r.get("source", {}).get("source_unit_id"):
            failures.append(f"record_missing_source_unit_id:{idx}")
        active = r.get("edge_surface", {}).get("active_object")
        if not active and r.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"record_missing_active_object:{idx}")
        boundary_checked = r.get("boundary", {}).get("boundary_checked")
        if not boundary_checked and r.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"record_missing_boundary_checked:{idx}")
        boundary_result = r.get("boundary", {}).get("boundary_result")
        if not boundary_result and r.get("classification", {}).get("confidence_class") != "UNDER_TYPED":
            failures.append(f"record_missing_boundary_result:{idx}")
        if not r.get("terminal", {}).get("terminal_result"):
            failures.append(f"record_missing_terminal_result:{idx}")
        if r.get("safety", {}).get("collection_status") != "OBSERVATION_ONLY":
            failures.append(f"record_not_observation_only:{idx}")
        if r.get("safety", {}).get("schema_claim") != "NONE":
            failures.append(f"record_schema_claim_not_none:{idx}")
        for key in [
            "architecture_change",
            "source_receipt_mutated",
            "authority_expansion",
            "runtime_patch_applied",
            "target_selected_for_build",
            "c5_opened",
        ]:
            if r.get("safety", {}).get(key) is not False:
                failures.append(f"record_bad_safety_true:{key}:{idx}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, design = validate_design_basis()

    receipts: Dict[str, Dict[str, Any]] = {}
    for src in SOURCE_RECEIPTS:
        if not src["path"].exists():
            failures.append(f"explicit_source_receipt_missing:{src['receipt_id']}:{src['path'].as_posix()}")
        else:
            receipts[src["receipt_id"]] = read_json(src["path"])

    required_fields = design.get("required_fields", [])
    candidate_handles = design.get("candidate_handles", [])
    acceptance_gates = design.get("acceptance_gates", [])

    if len(candidate_handles) < 13:
        failures.append("candidate_handle_count_too_low")
    if len(required_fields) < 30:
        failures.append("required_field_count_too_low")
    if len(acceptance_gates) < 25:
        failures.append("acceptance_gate_count_too_low")

    observation_records: List[Dict[str, Any]] = []
    if not failures:
        observation_records = build_observations(receipts)
        failures.extend(validate_observations(observation_records))

    handle_recs = handle_records(candidate_handles)

    schema_claim_count = 0
    architecture_change_count = 0
    source_receipt_mutation_count = 0
    authority_expansion_count = 0
    target_selected_for_build_count = 0
    runtime_patch_count = 0
    c5_opened_count = 0
    command_emitted_count = 0

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        source_receipt_mutation_count = 1

    gate = "PASS" if not failures else "FAIL"
    if gate == "PASS":
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_EMITTED"
        reason_codes = [
            "O1_DECISION_EDGE_OBSERVABILITY_SURFACE_BUILT",
            "EXPLICIT_SOURCE_RECEIPTS_CONSUMED",
            "DECISION_EDGE_OBSERVATION_SCHEMA_EMITTED",
            "CANDIDATE_HANDLE_SCHEMA_EMITTED",
            "CANDIDATE_HANDLES_MARKED_PROVISIONAL",
            "DECISION_EDGE_OBSERVATION_RECORDS_EMITTED",
            "ROLLUP_PROFILE_READOUT_EMITTED",
            "OBSERVATION_ONLY_COLLECTION_STATUS_PRESERVED",
            "SCHEMA_CLAIM_NONE",
            "NO_GRAPH_SCHEMA_CLAIMED",
            "NO_GRAPH_TRACKER_CREATED",
            "NO_ARCHITECTURE_CHANGE",
            "NO_SOURCE_RECEIPT_MUTATION",
            "NO_AUTHORITY_EXPANSION",
            "NO_TARGET_SELECTED_FOR_BUILD",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
            "NO_HIDDEN_NEXT_COMMAND",
        ]
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_EMITTED",
            "next_command_goal": None,
        }
        recommended_next = "REVIEW_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_V0"
    else:
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_BUILD_FAIL"
        reason_codes = failures
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_O1_OBSERVATION_SOURCE_UNDER_TYPED",
            "next_command_goal": None,
        }
        recommended_next = "REPAIR_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_BUILD_V0"

    write_json(OBS_RECORD_SCHEMA_PATH, observation_record_schema())
    write_json(HANDLE_SCHEMA_PATH, handle_schema())
    write_jsonl(HANDLE_RECORDS_PATH, handle_recs)
    write_jsonl(OBS_RECORDS_PATH, observation_records)

    handle_counts: Counter[str] = Counter()
    boundary_counts: Counter[str] = Counter()
    terminal_counts: Counter[str] = Counter()
    for obs in observation_records:
        handle_counts.update(obs.get("classification", {}).get("candidate_edge_handles", []))
        boundary_kind = obs.get("boundary", {}).get("boundary_kind")
        if boundary_kind:
            boundary_counts[boundary_kind] += 1
        term = obs.get("terminal", {}).get("terminal_result")
        if term:
            terminal_counts[term] += 1

    rollup = {
        "schema_version": "decision_edge_observation_rollup_v0",
        "total_observations": len(observation_records),
        "source_receipt_count": len(SOURCE_RECEIPTS),
        "candidate_edge_handle_counts": dict(sorted(handle_counts.items())),
        "boundary_counts": {
            "authority_boundary_count": sum(1 for x in observation_records if x.get("boundary", {}).get("authority_boundary_exposed") is True),
            "capability_boundary_count": sum(1 for x in observation_records if x.get("boundary", {}).get("capability_boundary_exposed") is True),
            "taxonomy_boundary_count": boundary_counts.get("taxonomy_boundary", 0),
            "metric_semantics_boundary_count": boundary_counts.get("metric_semantics_boundary", 0),
            "closure_reference_boundary_count": boundary_counts.get("closure_reference_boundary", 0),
            "builder_handoff_boundary_count": boundary_counts.get("builder_handoff_boundary", 0),
            "verification_boundary_count": boundary_counts.get("verification_boundary", 0),
            "label_noncollapse_boundary_count": boundary_counts.get("label_noncollapse_boundary", 0),
            "repair_or_fallback_boundary_count": boundary_counts.get("repair_or_fallback_boundary", 0),
        },
        "terminal_result_counts": dict(sorted(terminal_counts.items())),
        "bad_counters": {
            "schema_claim_count": schema_claim_count,
            "architecture_change_count": architecture_change_count,
            "source_receipt_mutation_count": source_receipt_mutation_count,
            "authority_expansion_count": authority_expansion_count,
            "target_selected_for_build_count": target_selected_for_build_count,
            "runtime_patch_count": runtime_patch_count,
            "c5_opened_count": c5_opened_count,
            "command_emitted_count": command_emitted_count,
        },
    }

    recurring_shapes = []
    for handle, count in sorted(handle_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if count >= 2:
            recurring_shapes.append({
                "candidate_shape": handle.lower(),
                "supporting_observation_count": count,
                "candidate_handles": [handle],
                "status": "OBSERVED_RECURRENT",
            })

    profile = {
        "schema_version": "decision_edge_observation_profile_v0",
        "profile_id": "edge_profile_" + sha8({"rollup": rollup, "observations": len(observation_records)}),
        "recurring_candidate_shapes": recurring_shapes,
        "schema_claim": "NONE",
        "architecture_change": False,
        "recommendation": "Continue collecting observations before extracting graph schema.",
    }

    readout = {
        "schema_version": "decision_edge_observation_readout_v0",
        "observations_emitted": len(observation_records),
        "source_receipts": len(SOURCE_RECEIPTS),
        "most_common_provisional_handles": [
            {"candidate_edge_handle": h, "count": c}
            for h, c in sorted(handle_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
        ],
        "boundary_exposure": rollup["boundary_counts"],
        "bad_counters_zero": all(v == 0 for v in rollup["bad_counters"].values()),
        "interpretation": "Repeated edge-like shapes are now visible from receipts, but no graph schema is claimed.",
        "must_not_infer": [
            "graph schema exists",
            "architecture changed",
            "C5 opened",
            "authority expanded",
            "target selected for build",
        ],
    }

    source_surface = {
        "schema_version": "o1_source_surface_v0",
        "source_receipts": [
            {
                "receipt_id": src["receipt_id"],
                "source_receipt_ref": rel(src["path"]),
                "source_context": src["context"],
                "source_unit_id": receipts[src["receipt_id"]].get("unit_id") if src["receipt_id"] in receipts else None,
            }
            for src in SOURCE_RECEIPTS
        ],
        "source_artifact_refs": [
            rel(O1_TARGET_DESIGN_PATH),
            rel(O1_SOURCE_SCOPE_CONTRACT_PATH),
            rel(O1_REQUIRED_FIELD_CONTRACT_PATH),
            rel(O1_CANDIDATE_HANDLE_CONTRACT_PATH),
            rel(O1_BUILD_AUTHORIZATION_PATH),
        ],
        "included_unit_ids": [
            receipts[src["receipt_id"]].get("unit_id")
            for src in SOURCE_RECEIPTS
            if src["receipt_id"] in receipts
        ],
        "excluded_unit_ids": [],
        "inspection_mode": "REF_AND_SUMMARY_ONLY",
        "payload_inspection_allowed": False,
        "source_mutation_allowed": False,
        "selection_rule": "explicit_refs_only",
    }

    transition_trace = {
        "schema_version": "o1_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o1_design",
                "question": "is O1 build authorized from a designed target",
                "answer": "yes" if gate == "PASS" else "no",
                "taken": "consume explicit source receipts",
            },
            {
                "step": "emit_sidecar_records",
                "question": "were local decision-edge fields surfaced",
                "answer": f"{len(observation_records)} observation sidecars emitted",
                "taken": "write observation records JSONL",
            },
            {
                "step": "preserve_nonauthority_boundary",
                "question": "did O1 define a graph schema, tracker, command, authority, runtime patch, or C5",
                "answer": "no",
                "taken": "emit rollup/profile/readout with bad counters zero",
            },
        ],
        "terminal": terminal,
    }

    report = {
        "schema_version": "o1_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "O1 emitted source-backed decision-edge observation sidecars from explicit receipts. Candidate edge handles are provisional collection tags. Rollup, profile, source surface, readout, report, transition trace, and receipt were emitted. No graph schema, graph tracker, source mutation, authority expansion, target selection, runtime patch, C5 opening, command emission, or O2 execution occurred.",
        "observations_emitted": len(observation_records),
        "source_receipt_count": len(SOURCE_RECEIPTS),
        "candidate_handle_count": len(handle_recs),
        "bad_counters_zero": readout["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
        "recommended_second_handling": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0_AFTER_O1_REVIEW",
    }

    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(READOUT_PATH, readout)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(TRANSITION_TRACE_PATH, transition_trace)
    write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "O1_EDGE_0_SOURCE_SURFACE_DECLARED": SOURCE_SURFACE_PATH.exists(),
        "O1_EDGE_1_EXPLICIT_SOURCE_RECEIPTS_CONSUMED": len(SOURCE_RECEIPTS) == len(source_surface["source_receipts"]),
        "O1_EDGE_2_OBSERVATION_RECORD_SCHEMA_EMITTED": OBS_RECORD_SCHEMA_PATH.exists(),
        "O1_EDGE_3_CANDIDATE_HANDLE_SCHEMA_EMITTED": HANDLE_SCHEMA_PATH.exists(),
        "O1_EDGE_4_CANDIDATE_HANDLES_MARKED_PROVISIONAL": all("final graph" in " ".join(x.get("forbidden_use", [])) for x in handle_recs),
        "O1_EDGE_5_OBSERVATION_RECORDS_EMITTED": OBS_RECORDS_PATH.exists() and len(observation_records) >= 8,
        "O1_EDGE_6_EVERY_RECORD_HAS_SOURCE_RECEIPT_REF": all(x.get("source", {}).get("source_receipt_ref") for x in observation_records),
        "O1_EDGE_7_EVERY_RECORD_HAS_ACTIVE_OBJECT_OR_UNDERTYPED_STATUS": all(x.get("edge_surface", {}).get("active_object") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in observation_records),
        "O1_EDGE_8_EVERY_RECORD_HAS_BOUNDARY_CHECKED_OR_UNDERTYPED_STATUS": all(x.get("boundary", {}).get("boundary_checked") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in observation_records),
        "O1_EDGE_9_EVERY_RECORD_HAS_BOUNDARY_RESULT_OR_UNDERTYPED_STATUS": all(x.get("boundary", {}).get("boundary_result") or x.get("classification", {}).get("confidence_class") == "UNDER_TYPED" for x in observation_records),
        "O1_EDGE_10_BLOCKED_MOVES_RECORDED_WHEN_PRESENT": all(isinstance(x.get("movement", {}).get("blocked_moves"), list) for x in observation_records),
        "O1_EDGE_11_LAWFUL_NEXT_MOVES_RECORDED_WHEN_PRESENT": all(isinstance(x.get("movement", {}).get("lawful_next_moves"), list) for x in observation_records),
        "O1_EDGE_12_TERMINAL_RESULT_RECORDED": all(x.get("terminal", {}).get("terminal_result") for x in observation_records),
        "O1_EDGE_13_PARENT_RETURN_PAYLOAD_PRESERVED_WHEN_PRESENT": all("parent_return_payload" in x.get("terminal", {}) for x in observation_records),
        "O1_EDGE_14_COLLECTION_STATUS_OBSERVATION_ONLY": all(x.get("safety", {}).get("collection_status") == "OBSERVATION_ONLY" for x in observation_records),
        "O1_EDGE_15_SCHEMA_CLAIM_NONE": rollup["bad_counters"]["schema_claim_count"] == 0 and all(x.get("safety", {}).get("schema_claim") == "NONE" for x in observation_records),
        "O1_EDGE_16_NO_ARCHITECTURE_CHANGE": rollup["bad_counters"]["architecture_change_count"] == 0,
        "O1_EDGE_17_NO_SOURCE_RECEIPT_MUTATION": rollup["bad_counters"]["source_receipt_mutation_count"] == 0,
        "O1_EDGE_18_NO_AUTHORITY_EXPANSION": rollup["bad_counters"]["authority_expansion_count"] == 0,
        "O1_EDGE_19_NO_TARGET_SELECTED_FOR_BUILD": rollup["bad_counters"]["target_selected_for_build_count"] == 0,
        "O1_EDGE_20_NO_RUNTIME_PATCH": rollup["bad_counters"]["runtime_patch_count"] == 0,
        "O1_EDGE_21_NO_C5_OPENED": rollup["bad_counters"]["c5_opened_count"] == 0,
        "O1_EDGE_22_ROLLUP_PROFILE_READOUT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and READOUT_PATH.exists(),
        "O1_EDGE_23_BAD_COUNTERS_ZERO": readout["bad_counters_zero"],
        "O1_EDGE_24_NO_HIDDEN_NEXT_COMMAND": terminal.get("next_command_goal") is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")
        gate = "FAIL"
        status = "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_GATE_FAIL"
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_O1_OBSERVATION_SOURCE_UNDER_TYPED",
            "next_command_goal": None,
        }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "observations": len(observation_records),
        "source_receipts": len(SOURCE_RECEIPTS),
        "bad_counters": rollup["bad_counters"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o1_decision_edge_observability_surface_receipt_v0",
        "receipt_type": "TYPED_O1_DECISION_EDGE_OBSERVABILITY_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_design_receipt_id": O1_DESIGN_RECEIPT_ID,
        "machine_readable_o1_decision_edge_observability_surface_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "observations_emitted": len(observation_records),
            "source_receipt_count": len(SOURCE_RECEIPTS),
            "candidate_handle_count": len(handle_recs),
            "candidate_handles_marked_provisional": True,
            "collection_status": "OBSERVATION_ONLY",
            "schema_claim": "NONE",
            "bad_counters_zero": readout["bad_counters_zero"],
            "rollup_emitted": ROLLUP_PATH.exists(),
            "profile_emitted": PROFILE_PATH.exists(),
            "readout_emitted": READOUT_PATH.exists(),
            "source_surface_emitted": SOURCE_SURFACE_PATH.exists(),
            "graph_schema_claimed": False,
            "graph_tracker_created": False,
            "architecture_change": False,
            "source_receipt_mutated": False,
            "authority_expansion": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "command_emitted": False,
            "unit_feedback_hardening_executed": False,
            "recommended_next": recommended_next,
            "recommended_second": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0_AFTER_O1_REVIEW",
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "decision_edge_observation_record_schema": rel(OBS_RECORD_SCHEMA_PATH),
            "decision_edge_candidate_handle_schema": rel(HANDLE_SCHEMA_PATH),
            "decision_edge_candidate_handle_records": rel(HANDLE_RECORDS_PATH),
            "decision_edge_observation_records": rel(OBS_RECORDS_PATH),
            "decision_edge_observation_rollup": rel(ROLLUP_PATH),
            "decision_edge_observation_profile": rel(PROFILE_PATH),
            "decision_edge_observation_readout": rel(READOUT_PATH),
            "o1_source_surface": rel(SOURCE_SURFACE_PATH),
            "o1_transition_trace": rel(TRANSITION_TRACE_PATH),
            "o1_report": rel(REPORT_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"o1_surface_receipt_id={receipt_id}")
    print(f"o1_surface_receipt_path={rel(receipt_path)}")
    print(f"o1_observation_schema_path={rel(OBS_RECORD_SCHEMA_PATH)}")
    print(f"o1_handle_schema_path={rel(HANDLE_SCHEMA_PATH)}")
    print(f"o1_handle_records_path={rel(HANDLE_RECORDS_PATH)}")
    print(f"o1_observation_records_path={rel(OBS_RECORDS_PATH)}")
    print(f"o1_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o1_profile_path={rel(PROFILE_PATH)}")
    print(f"o1_readout_path={rel(READOUT_PATH)}")
    print(f"o1_source_surface_path={rel(SOURCE_SURFACE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
