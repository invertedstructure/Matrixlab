#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT"
MODE = "BRANCH_SPLIT_AND_REPAIR_SURFACE / PROPOSALS_HELD / AMBIGUITY_REPAIR / REQUIREMENT_GAP_REPAIR / NO_REBIND_APPLICATION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_ONLY"

SOURCE_PARTIAL_RECEIPT_ID = "3ea9c04c"
SOURCE_PARTIAL_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0_receipts/3ea9c04c.json"
SOURCE_PARTIAL_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_review_assessment_v0.json"
SOURCE_PROPOSAL_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_review_table_v0.json"
SOURCE_PROPOSAL_REVIEW_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_review_surface_v0.json"
SOURCE_AMBIGUITY_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_ambiguity_review_table_v0.json"
SOURCE_AMBIGUITY_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_ambiguity_repair_surface_v0.json"
SOURCE_REQUIREMENT_GAP_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_requirement_gap_review_table_v0.json"
SOURCE_REQUIREMENT_GAP_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_requirement_gap_repair_surface_v0.json"
SOURCE_BRANCH_SPLIT_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_branch_split_surface_v0.json"
SOURCE_PROPOSAL_HOLD_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_hold_contract_v0.json"
SOURCE_DOWNSTREAM_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_downstream_decision_table_v0.json"
SOURCE_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_review_packet_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_review_v0/typed_machine_readable_partial_schema_aware_rebind_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_branch_split_v0_receipts"

BRANCH_SPLIT_ROUTING_OBJECT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_routing_object_v0.json"
PROPOSAL_BRANCH_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_v0.json"
PROPOSAL_BRANCH_HOLD_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_packet_v0.json"
AMBIGUITY_BRANCH_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_branch_contract_v0.json"
AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_ambiguity_tie_breaker_evidence_surface_v0.json"
REQUIREMENT_GAP_BRANCH_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_branch_contract_v0.json"
REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_evidence_surface_v0.json"
BRANCH_PRECONDITION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_precondition_table_v0.json"
BRANCH_FORBIDDEN_ACTION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_forbidden_action_table_v0.json"
BRANCH_PRIORITY_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_priority_table_v0.json"
BRANCH_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_branch_split_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PARTIAL_RECEIPT_PATH,
    SOURCE_PARTIAL_REVIEW_ASSESSMENT_PATH,
    SOURCE_PROPOSAL_REVIEW_TABLE_PATH,
    SOURCE_PROPOSAL_REVIEW_SURFACE_PATH,
    SOURCE_AMBIGUITY_REVIEW_TABLE_PATH,
    SOURCE_AMBIGUITY_REPAIR_SURFACE_PATH,
    SOURCE_REQUIREMENT_GAP_REVIEW_TABLE_PATH,
    SOURCE_REQUIREMENT_GAP_REPAIR_SURFACE_PATH,
    SOURCE_BRANCH_SPLIT_SURFACE_PATH,
    SOURCE_PROPOSAL_HOLD_CONTRACT_PATH,
    SOURCE_DOWNSTREAM_DECISION_TABLE_PATH,
    SOURCE_REVIEW_PACKET_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEWED_BRANCH_SPLIT_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_SOURCE_REF_REBIND_REVIEWED_BRANCH_SPLIT_REQUIRED"
EXPECTED_SOURCE_NEXT = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"

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

def records(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    v = obj.get("records")
    return v if isinstance(v, list) else []

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_PARTIAL_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_summary", {})
    assessment = read_json(SOURCE_PARTIAL_REVIEW_ASSESSMENT_PATH)
    proposal_table = read_json(SOURCE_PROPOSAL_REVIEW_TABLE_PATH)
    proposal_surface = read_json(SOURCE_PROPOSAL_REVIEW_SURFACE_PATH)
    ambiguity_table = read_json(SOURCE_AMBIGUITY_REVIEW_TABLE_PATH)
    ambiguity_surface = read_json(SOURCE_AMBIGUITY_REPAIR_SURFACE_PATH)
    gap_table = read_json(SOURCE_REQUIREMENT_GAP_REVIEW_TABLE_PATH)
    gap_surface = read_json(SOURCE_REQUIREMENT_GAP_REPAIR_SURFACE_PATH)
    source_branch = read_json(SOURCE_BRANCH_SPLIT_SURFACE_PATH)
    hold = read_json(SOURCE_PROPOSAL_HOLD_CONTRACT_PATH)
    classif = read_json(SOURCE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_PARTIAL_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_partial_rebind_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    required_true = [
        "partial_schema_aware_rebind_review_complete",
        "branch_split_required",
        "proposal_hold_contract_emitted",
        "ambiguity_repair_surface_emitted",
        "requirement_gap_repair_surface_emitted",
        "schema_overlay_applied_for_this_contract",
    ]
    for key in required_true:
        if summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

    expected_counts = {
        "proposal_ready_count": 4,
        "proposal_review_failure_count": 0,
        "ambiguous_binding_count": 22,
        "requirement_gap_binding_count": 498,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"source_count_wrong:{key}:{summary.get(key)}")

    forbidden_false = [
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
        "rebinds_applied",
        "dominance_rule_applied",
        "values_authorized",
        "values_applied",
        "null_reasons_accepted",
        "source_packet_materialized_for_review",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]
    for key in forbidden_false:
        if summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    if assessment.get("branch_split_required") is not True:
        failures.append("assessment_branch_split_not_required")
    if proposal_table.get("proposal_ready_count") != 4 or len(records(proposal_table)) != 4:
        failures.append("proposal_table_not_4")
    if proposal_surface.get("proposal_ready_count") != 4:
        failures.append("proposal_surface_not_4")
    if ambiguity_table.get("ambiguous_binding_count") != 22 or len(records(ambiguity_table)) != 22:
        failures.append("ambiguity_table_not_22")
    if ambiguity_surface.get("ambiguous_binding_count") != 22:
        failures.append("ambiguity_surface_not_22")
    if gap_table.get("requirement_gap_binding_count") != 498 or len(records(gap_table)) != 498:
        failures.append("gap_table_not_498")
    if gap_surface.get("requirement_gap_binding_count") != 498:
        failures.append("gap_surface_not_498")
    if source_branch.get("branch_split_status") != "BRANCH_SPLIT_REQUIRED_BEFORE_ANY_REBIND_APPLICATION":
        failures.append("source_branch_split_status_wrong")
    if hold.get("hold_contract_status") != "PARTIAL_PROPOSALS_HELD_PENDING_BRANCH_SPLIT_REVIEW":
        failures.append("proposal_hold_contract_status_wrong")
    if hold.get("may_apply_proposals") is not False:
        failures.append("proposal_hold_allows_application")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if authority.get("may_build_branch_split_surface") is not True:
        failures.append("authority_does_not_allow_branch_split")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebinds")
    if rollup.get("branch_split_required_count") != 1:
        failures.append("rollup_branch_split_count_not_1")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if profile.get("branch_split_required") is not True:
        failures.append("profile_branch_split_not_true")
    if profile.get("rebinds_applied") is not False:
        failures.append("profile_rebinds_true")

    return failures, {
        "summary": summary,
        "proposal_records": records(proposal_table),
        "ambiguity_records": records(ambiguity_table),
        "gap_records": records(gap_table),
        "source_branch": source_branch,
        "hold": hold,
        "ambiguity_surface": ambiguity_surface,
        "gap_surface": gap_surface,
    }

def make_branch_ids(prefix: str, rows: List[Dict[str, Any]], key_name: str) -> List[str]:
    ids: List[str] = []
    for idx, row in enumerate(rows):
        key = row.get(key_name) or row.get("binding_key") or idx
        ids.append(prefix + "_" + sha8({"idx": idx, "key": key, "row": row}))
    return ids

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    proposal_records = src.get("proposal_records", [])
    ambiguity_records = src.get("ambiguity_records", [])
    gap_records = src.get("gap_records", [])

    proposal_branch_ids = make_branch_ids("proposal_binding", proposal_records, "binding_key")
    ambiguity_branch_ids = make_branch_ids("ambiguity_binding", ambiguity_records, "binding_key")
    gap_branch_ids = make_branch_ids("requirement_gap_binding", gap_records, "binding_key")

    proposal_binding_count = len(proposal_records)
    ambiguity_binding_count = len(ambiguity_records)
    requirement_gap_binding_count = len(gap_records)
    total_routed_binding_count = proposal_binding_count + ambiguity_binding_count + requirement_gap_binding_count

    gap_missing_requirement_counts = Counter()
    for row in gap_records:
        counts = row.get("missing_requirement_counts") or {}
        for k, v in counts.items():
            try:
                gap_missing_requirement_counts[k] += int(v)
            except Exception:
                gap_missing_requirement_counts[k] += 1

    ambiguity_top_candidate_distribution = Counter(str(row.get("top_candidate_count")) for row in ambiguity_records)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_BASIS_V0"
        review_ready = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_BUILT_REVIEW_REQUIRED"
        reason_codes = [
            "PARTIAL_SCHEMA_AWARE_BRANCH_SPLIT_ROUTING_OBJECT_BUILT",
            "PROPOSAL_BRANCH_CONTRACT_EMITTED",
            "PROPOSAL_HOLD_PACKET_EMITTED",
            "AMBIGUITY_BRANCH_CONTRACT_EMITTED",
            "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_EMITTED",
            "REQUIREMENT_GAP_BRANCH_CONTRACT_EMITTED",
            "REQUIREMENT_GAP_EVIDENCE_SURFACE_EMITTED",
            "BRANCH_PRECONDITIONS_AND_FORBIDDEN_ACTIONS_EMITTED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0"
        review_ready = True

    branch_split_routing_object = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_routing_object_v0",
        "routing_status": "BRANCH_SPLIT_ROUTING_OBJECT_BUILT_REVIEW_REQUIRED" if review_ready else "BRANCH_SPLIT_ROUTING_OBJECT_NOT_BUILT",
        "source_partial_schema_aware_rebind_receipt_id": SOURCE_PARTIAL_RECEIPT_ID,
        "total_routed_binding_count": total_routed_binding_count,
        "branches": [
            {
                "branch_id": "proposal_review_branch",
                "branch_status": "HELD_FOR_SEPARATE_REVIEW_NOT_APPLICATION",
                "binding_count": proposal_binding_count,
                "binding_ids": proposal_branch_ids,
                "allowed_next": "review proposal branch correctness and application preconditions",
                "forbidden_now": [
                    "apply rebinds",
                    "mark proposal accepted-for-build",
                    "populate metadata",
                    "extract values",
                    "discard unresolved branches",
                ],
            },
            {
                "branch_id": "ambiguity_tie_breaker_repair_branch",
                "branch_status": "TIE_BREAKER_EVIDENCE_REPAIR_REQUIRED",
                "binding_count": ambiguity_binding_count,
                "binding_ids": ambiguity_branch_ids,
                "allowed_next": "build tie-breaker evidence surface for tied candidates",
                "forbidden_now": [
                    "choose tied candidate by score alone",
                    "apply rebinds",
                    "collapse ambiguity into null",
                ],
            },
            {
                "branch_id": "requirement_gap_repair_branch",
                "branch_status": "MISSING_SCHEMA_EVIDENCE_REPAIR_REQUIRED",
                "binding_count": requirement_gap_binding_count,
                "binding_ids": gap_branch_ids,
                "allowed_next": "build missing schema-evidence repair surface",
                "forbidden_now": [
                    "invent missing evidence",
                    "populate metadata",
                    "treat gap as proof of absence",
                    "apply rebinds",
                ],
            },
        ],
        "branch_split_review_required": True,
        "rebinds_applied": False,
    }

    proposal_branch_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_contract_v0",
        "contract_status": "PROPOSAL_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED",
        "proposal_binding_count": proposal_binding_count,
        "proposal_ids": proposal_branch_ids,
        "source_proposal_review_table_path": rel(SOURCE_PROPOSAL_REVIEW_TABLE_PATH),
        "proposal_review_mode": "review_only_not_application",
        "may_review_proposal_correctness": True,
        "may_apply_rebinds": False,
        "may_mark_accepted_for_build": False,
        "must_preserve_residual_branches": True,
    }

    proposal_branch_hold_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_packet_v0",
        "hold_status": "PROPOSALS_HELD_PENDING_BRANCH_SPLIT_REVIEW",
        "proposal_ready_count": proposal_binding_count,
        "held_binding_ids": proposal_branch_ids,
        "held_reason": "partial proposal branch exists but unresolved ambiguity/gap branches remain",
        "release_requires": [
            "branch split review passes",
            "proposal-specific review passes",
            "separate authorization to apply rebinds",
        ],
        "released_now": False,
        "rebinds_applied": False,
    }

    ambiguity_branch_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_branch_contract_v0",
        "contract_status": "AMBIGUITY_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED",
        "ambiguous_binding_count": ambiguity_binding_count,
        "top_candidate_count_distribution": dict(sorted(ambiguity_top_candidate_distribution.items())),
        "source_ambiguity_review_table_path": rel(SOURCE_AMBIGUITY_REVIEW_TABLE_PATH),
        "repair_goal": "identify evidence capable of distinguishing tied schema-aware candidates",
        "may_build_tie_breaker_evidence_surface": True,
        "may_choose_candidate_now": False,
        "may_apply_rebinds": False,
    }

    ambiguity_tie_breaker_evidence_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_ambiguity_tie_breaker_evidence_surface_v0",
        "surface_status": "AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_BUILT_REVIEW_REQUIRED",
        "ambiguous_binding_count": ambiguity_binding_count,
        "evidence_requirements": [
            {
                "evidence_class": "ROW_IDENTITY_MATCH",
                "purpose": "distinguish tied candidate rows by explicit row identity, not filename or score alone",
            },
            {
                "evidence_class": "SOURCE_PACKET_LINEAGE_MATCH",
                "purpose": "prefer candidate whose lineage directly contains the binding source packet",
            },
            {
                "evidence_class": "FIELD_POLICY_SOURCE_OBJECT_MATCH",
                "purpose": "verify candidate source object matches field-policy expectation",
            },
            {
                "evidence_class": "ARTIFACT_PRODUCER_UNIT_MATCH",
                "purpose": "verify candidate artifact was produced by the expected source-producing unit",
            },
        ],
        "binding_refs": ambiguity_branch_ids,
        "selected_candidate_count": 0,
        "rebinds_applied": False,
    }

    requirement_gap_branch_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_branch_contract_v0",
        "contract_status": "REQUIREMENT_GAP_BRANCH_CONTRACT_BUILT_REVIEW_REQUIRED",
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "source_requirement_gap_review_table_path": rel(SOURCE_REQUIREMENT_GAP_REVIEW_TABLE_PATH),
        "missing_requirement_counts": dict(sorted(gap_missing_requirement_counts.items())),
        "repair_goal": "materialize missing schema-evidence surfaces without inventing values or applying metadata",
        "may_build_missing_evidence_surface": True,
        "may_invent_missing_evidence": False,
        "may_populate_metadata": False,
        "may_apply_rebinds": False,
    }

    requirement_gap_evidence_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_requirement_gap_evidence_surface_v0",
        "surface_status": "REQUIREMENT_GAP_EVIDENCE_SURFACE_BUILT_REVIEW_REQUIRED",
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "missing_requirement_counts": dict(sorted(gap_missing_requirement_counts.items())),
        "required_evidence_classes": [
            "source_role",
            "source_packet_lineage",
            "artifact_producer_unit",
            "field_policy_source_object_match",
            "row_identity_schema",
        ],
        "binding_refs": gap_branch_ids,
        "evidence_materialized_now": False,
        "metadata_populated": False,
        "rebinds_applied": False,
    }

    branch_precondition_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_precondition_table_v0",
        "precondition_status": "BRANCH_PRECONDITIONS_EMITTED",
        "records": [
            {
                "branch_id": "proposal_review_branch",
                "preconditions": [
                    "branch split review pass",
                    "proposal branch contract pass",
                    "proposal hold contract retained",
                    "separate apply authorization before any rebind",
                ],
            },
            {
                "branch_id": "ambiguity_tie_breaker_repair_branch",
                "preconditions": [
                    "branch split review pass",
                    "tie-breaker evidence surface review pass",
                    "no candidate selected by score alone",
                ],
            },
            {
                "branch_id": "requirement_gap_repair_branch",
                "preconditions": [
                    "branch split review pass",
                    "missing schema-evidence surface review pass",
                    "no invented evidence",
                    "no metadata population",
                ],
            },
        ],
    }

    forbidden_actions = [
        "apply rebinds",
        "authorize values",
        "apply values",
        "populate metadata",
        "mark discriminator ready",
        "select target for build",
        "apply runtime patch",
        "open C5",
        "promote schema to reusable",
        "treat schema as preapproved",
        "create validator registry entry",
        "allow future automatic use",
        "use latest-file guessing",
        "use mtime selection",
    ]

    branch_forbidden_action_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_forbidden_action_table_v0",
        "forbidden_action_status": "FORBIDDEN_ACTIONS_REAFFIRMED",
        "forbidden_actions": forbidden_actions,
        "applies_to_all_branches": True,
    }

    branch_priority_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_priority_table_v0",
        "priority_status": "BRANCH_PRIORITY_EMITTED_REVIEW_REQUIRED",
        "priority_order": [
            {
                "rank": 1,
                "branch_id": "review_branch_split_surface",
                "why": "the routing object itself must be reviewed before any branch execution",
            },
            {
                "rank": 2,
                "branch_id": "proposal_review_branch",
                "why": "4 proposal-ready bindings can be reviewed cheaply but must stay held",
            },
            {
                "rank": 3,
                "branch_id": "ambiguity_tie_breaker_repair_branch",
                "why": "22 tied bindings need better distinguishing evidence",
            },
            {
                "rank": 4,
                "branch_id": "requirement_gap_repair_branch",
                "why": "498 bindings need missing schema-evidence materialization surfaces",
            },
        ],
    }

    branch_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_decision_table_v0",
        "decision_status": "BRANCH_SPLIT_DECISION_TABLE_EMITTED",
        "records": [
            {
                "decision": "REVIEW_BRANCH_SPLIT_AND_REPAIR_SURFACE",
                "selected": True,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_AND_REPAIR_SURFACE_V0",
                "why": "branch routing was built and must be reviewed before branch execution",
            },
            {
                "decision": "EXECUTE_PROPOSAL_BRANCH_NOW",
                "selected": False,
                "next_unit": None,
                "why": "branch split review has not passed yet",
            },
            {
                "decision": "APPLY_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "forbidden in this unit",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_review_packet_v0",
        "review_packet_status": "BRANCH_SPLIT_AND_REPAIR_SURFACE_BUILT_REVIEW_REQUIRED" if review_ready else "BRANCH_SPLIT_REPAIR_REQUIRED",
        "summary": {
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
            "total_routed_binding_count": total_routed_binding_count,
            "branch_split_review_required": True,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "branch_split_surface_built": review_ready,
        "branch_split_review_required": True,
        "proposal_branch_contract_emitted": True,
        "proposal_branch_hold_packet_emitted": True,
        "ambiguity_branch_contract_emitted": True,
        "ambiguity_tie_breaker_evidence_surface_emitted": True,
        "requirement_gap_branch_contract_emitted": True,
        "requirement_gap_evidence_surface_emitted": True,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_authorized": False,
        "c5_authorized": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_authority_boundary_v0",
        "status": status,
        "may_review_branch_split_surface": True,
        "may_build_proposal_branch_contract": True,
        "may_build_ambiguity_repair_contract": True,
        "may_build_requirement_gap_repair_contract": True,
        "may_apply_rebinds": False,
        "may_release_proposal_hold": False,
        "may_choose_ambiguous_candidate": False,
        "may_invent_requirement_gap_evidence": False,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    rollup = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "branch_split_surface_built_count": 1 if review_ready else 0,
        "branch_split_review_required_count": 1,
        "proposal_branch_contract_emitted_count": 1,
        "proposal_branch_hold_packet_emitted_count": 1,
        "ambiguity_branch_contract_emitted_count": 1,
        "ambiguity_tie_breaker_evidence_surface_emitted_count": 1,
        "requirement_gap_branch_contract_emitted_count": 1,
        "requirement_gap_evidence_surface_emitted_count": 1,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "schema_overlay_applied_for_this_contract_count": 1,
        "schema_overlay_applied_globally_count": 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "dominance_rule_applied_count": 0,
        "refinements_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "null_reason_accepted_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
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
        "recommended_next": next_edge,
    }

    zero_keys = [
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_profile_v0",
        "profile_id": "partial_schema_aware_branch_split_profile_" + sha8(rollup),
        "status": status,
        "branch_split_surface_built": review_ready,
        "branch_split_review_required": True,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The partial schema-aware rebind split was materialized as a first-class routing object with proposal, ambiguity repair, and requirement-gap repair branches. This unit does not apply rebinds, release proposals, populate metadata, authorize values, select targets, patch runtime, open C5, or promote schema authority.",
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "total_routed_binding_count": total_routed_binding_count,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_transition_trace_v0",
        "trace": [
            {
                "step": "consume_partial_split",
                "question": "what split must be preserved",
                "answer": "4 proposals, 22 ambiguities, 498 requirement gaps",
                "taken": "materialize routing object",
            },
            {
                "step": "emit_branch_contracts",
                "question": "what branch contracts are needed",
                "answer": "proposal hold, ambiguity tie-breaker repair, requirement-gap evidence repair",
                "taken": "emit branch contracts and preconditions",
            },
            {
                "step": "retain_forbidden_boundary",
                "question": "can any rebind be applied now",
                "answer": "no",
                "taken": "review required before any branch execution",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(BRANCH_SPLIT_ROUTING_OBJECT_PATH, branch_split_routing_object)
    write_json(PROPOSAL_BRANCH_CONTRACT_PATH, proposal_branch_contract)
    write_json(PROPOSAL_BRANCH_HOLD_PACKET_PATH, proposal_branch_hold_packet)
    write_json(AMBIGUITY_BRANCH_CONTRACT_PATH, ambiguity_branch_contract)
    write_json(AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_PATH, ambiguity_tie_breaker_evidence_surface)
    write_json(REQUIREMENT_GAP_BRANCH_CONTRACT_PATH, requirement_gap_branch_contract)
    write_json(REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH, requirement_gap_evidence_surface)
    write_json(BRANCH_PRECONDITION_TABLE_PATH, branch_precondition_table)
    write_json(BRANCH_FORBIDDEN_ACTION_TABLE_PATH, branch_forbidden_action_table)
    write_json(BRANCH_PRIORITY_TABLE_PATH, branch_priority_table)
    write_json(BRANCH_DECISION_TABLE_PATH, branch_decision_table)
    write_json(REVIEW_PACKET_PATH, review_packet)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "BRANCH_SPLIT_0_SOURCE_RECEIPT_CONSUMED": SOURCE_PARTIAL_RECEIPT_PATH.exists(),
        "BRANCH_SPLIT_1_ROUTING_OBJECT_EMITTED": BRANCH_SPLIT_ROUTING_OBJECT_PATH.exists(),
        "BRANCH_SPLIT_2_PROPOSAL_BRANCH_CONTRACT_EMITTED": PROPOSAL_BRANCH_CONTRACT_PATH.exists(),
        "BRANCH_SPLIT_3_PROPOSAL_HOLD_PACKET_EMITTED": PROPOSAL_BRANCH_HOLD_PACKET_PATH.exists(),
        "BRANCH_SPLIT_4_AMBIGUITY_BRANCH_CONTRACT_EMITTED": AMBIGUITY_BRANCH_CONTRACT_PATH.exists(),
        "BRANCH_SPLIT_5_AMBIGUITY_TIE_BREAKER_SURFACE_EMITTED": AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_PATH.exists(),
        "BRANCH_SPLIT_6_REQUIREMENT_GAP_BRANCH_CONTRACT_EMITTED": REQUIREMENT_GAP_BRANCH_CONTRACT_PATH.exists(),
        "BRANCH_SPLIT_7_REQUIREMENT_GAP_EVIDENCE_SURFACE_EMITTED": REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH.exists(),
        "BRANCH_SPLIT_8_PRECONDITIONS_EMITTED": BRANCH_PRECONDITION_TABLE_PATH.exists(),
        "BRANCH_SPLIT_9_FORBIDDEN_ACTIONS_EMITTED": BRANCH_FORBIDDEN_ACTION_TABLE_PATH.exists(),
        "BRANCH_SPLIT_10_FOUR_PROPOSAL_BINDINGS_ROUTED": proposal_binding_count == 4,
        "BRANCH_SPLIT_11_TWENTY_TWO_AMBIGUITY_BINDINGS_ROUTED": ambiguity_binding_count == 22,
        "BRANCH_SPLIT_12_FOUR_NINETY_EIGHT_GAP_BINDINGS_ROUTED": requirement_gap_binding_count == 498,
        "BRANCH_SPLIT_13_TOTAL_ROUTED_BINDINGS_524": total_routed_binding_count == 524,
        "BRANCH_SPLIT_14_REVIEW_REQUIRED": classification["branch_split_review_required"] is True,
        "BRANCH_SPLIT_15_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "BRANCH_SPLIT_16_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "BRANCH_SPLIT_17_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "BRANCH_SPLIT_18_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "BRANCH_SPLIT_19_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "BRANCH_SPLIT_20_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "BRANCH_SPLIT_21_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "BRANCH_SPLIT_22_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "BRANCH_SPLIT_23_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "BRANCH_SPLIT_24_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "BRANCH_SPLIT_25_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "BRANCH_SPLIT_26_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "BRANCH_SPLIT_27_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "BRANCH_SPLIT_28_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "BRANCH_SPLIT_29_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "BRANCH_SPLIT_30_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "BRANCH_SPLIT_31_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "BRANCH_SPLIT_32_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "BRANCH_SPLIT_33_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "BRANCH_SPLIT_34_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "BRANCH_SPLIT_35_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "BRANCH_SPLIT_36_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal_binding_count,
        "ambiguity": ambiguity_binding_count,
        "gap": requirement_gap_binding_count,
        "total": total_routed_binding_count,
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_branch_split_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_BRANCH_SPLIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_partial_schema_aware_rebind_receipt_id": SOURCE_PARTIAL_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_branch_split_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "branch_split_surface_built": review_ready,
            "branch_split_review_required": True,
            "proposal_branch_contract_emitted": True,
            "proposal_branch_hold_packet_emitted": True,
            "ambiguity_branch_contract_emitted": True,
            "ambiguity_tie_breaker_evidence_surface_emitted": True,
            "requirement_gap_branch_contract_emitted": True,
            "requirement_gap_evidence_surface_emitted": True,
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
            "total_routed_binding_count": total_routed_binding_count,
            "schema_overlay_applied_for_this_contract": True,
            "schema_overlay_applied_globally": False,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
            "typing_rule_applied": False,
            "field_policy_modified": False,
            "candidate_artifact_modified": False,
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "dominance_rule_applied": False,
            "values_authorized": False,
            "values_applied": False,
            "null_reasons_accepted": False,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "branch_split_routing_object": rel(BRANCH_SPLIT_ROUTING_OBJECT_PATH),
            "proposal_branch_contract": rel(PROPOSAL_BRANCH_CONTRACT_PATH),
            "proposal_branch_hold_packet": rel(PROPOSAL_BRANCH_HOLD_PACKET_PATH),
            "ambiguity_branch_contract": rel(AMBIGUITY_BRANCH_CONTRACT_PATH),
            "ambiguity_tie_breaker_evidence_surface": rel(AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_PATH),
            "requirement_gap_branch_contract": rel(REQUIREMENT_GAP_BRANCH_CONTRACT_PATH),
            "requirement_gap_evidence_surface": rel(REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH),
            "branch_precondition_table": rel(BRANCH_PRECONDITION_TABLE_PATH),
            "branch_forbidden_action_table": rel(BRANCH_FORBIDDEN_ACTION_TABLE_PATH),
            "branch_priority_table": rel(BRANCH_PRIORITY_TABLE_PATH),
            "branch_decision_table": rel(BRANCH_DECISION_TABLE_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
            "classification": rel(CLASSIFICATION_PATH),
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
    print(f"partial_schema_aware_branch_split_receipt_id={receipt_id}")
    print(f"partial_schema_aware_branch_split_receipt_path={rel(receipt_path)}")
    print(f"partial_schema_aware_branch_split_routing_object_path={rel(BRANCH_SPLIT_ROUTING_OBJECT_PATH)}")
    print(f"partial_schema_aware_proposal_branch_contract_path={rel(PROPOSAL_BRANCH_CONTRACT_PATH)}")
    print(f"partial_schema_aware_proposal_branch_hold_packet_path={rel(PROPOSAL_BRANCH_HOLD_PACKET_PATH)}")
    print(f"partial_schema_aware_ambiguity_branch_contract_path={rel(AMBIGUITY_BRANCH_CONTRACT_PATH)}")
    print(f"partial_schema_aware_ambiguity_tie_breaker_evidence_surface_path={rel(AMBIGUITY_TIE_BREAKER_EVIDENCE_SURFACE_PATH)}")
    print(f"partial_schema_aware_requirement_gap_branch_contract_path={rel(REQUIREMENT_GAP_BRANCH_CONTRACT_PATH)}")
    print(f"partial_schema_aware_requirement_gap_evidence_surface_path={rel(REQUIREMENT_GAP_EVIDENCE_SURFACE_PATH)}")
    print(f"partial_schema_aware_branch_split_rollup_path={rel(ROLLUP_PATH)}")
    print(f"partial_schema_aware_branch_split_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
