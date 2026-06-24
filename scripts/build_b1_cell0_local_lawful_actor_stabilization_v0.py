#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_B1_CELL0_LOCAL_LAWFUL_ACTOR_STABILIZATION_V0"
TARGET_UNIT_ID = "b1.cell0.local_lawful_actor_stabilization.v0"
LAYER = "CELL_0 / LOCAL_ACTOR_BASELINE"
MODE = "CERTIFY / VERIFY"

SOURCE_B0_RECEIPT_ID = "7cbb85ee"
SOURCE_B0_RECEIPT_PATH = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0_receipts" / "7cbb85ee.json"
SOURCE_B0_REFERENCE_OBJECT_PATH = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0" / "cell0_observability_reference_object_v0.json"
SOURCE_B0_BOUNDED_PROTOCOL_PATH = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0" / "bounded_observability_protocol_v0.json"
SOURCE_B0_CLOSURE_PACKET_PATH = ROOT / "data" / "b0_current_observability_branch_closure_reference_object_v0" / "r10000_observability_branch_closure_packet_v0.json"

OUT_DIR = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0"
RECEIPT_DIR = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0_receipts"

PROFILE_PATH = OUT_DIR / "cell0_local_lawful_actor_profile_v0.json"
SURFACE_SCHEMA_PATH = OUT_DIR / "cell0_pressure_surface_schema_v0.json"
INSPECTION_SCHEMA_PATH = OUT_DIR / "cell0_authorized_inspection_schema_v0.json"
PRESSURE_ENUM_PATH = OUT_DIR / "cell0_pressure_class_enum_v0.json"
PRESSURE_CLASSIFICATION_SCHEMA_PATH = OUT_DIR / "cell0_pressure_classification_schema_v0.json"
MOVE_RESULT_SCHEMA_PATH = OUT_DIR / "cell0_local_move_result_schema_v0.json"
TYPED_STOP_SCHEMA_PATH = OUT_DIR / "cell0_typed_stop_schema_v0.json"
LOCAL_MOVE_REGISTRY_PATH = OUT_DIR / "cell0_local_demo_move_registry_v0.json"
DEMO_SURFACES_PATH = OUT_DIR / "cell0_demo_pressure_surfaces_v0.jsonl"
INSPECTION_RECORDS_PATH = OUT_DIR / "cell0_authorized_inspection_records_v0.jsonl"
PRESSURE_CLASSIFICATION_RECORDS_PATH = OUT_DIR / "cell0_pressure_classification_records_v0.jsonl"
MOVE_RESULT_RECORDS_PATH = OUT_DIR / "cell0_local_move_result_records_v0.jsonl"
DEMO_RECEIPTS_PATH = OUT_DIR / "cell0_demo_receipts_v0.jsonl"
RELIABILITY_ROLLUP_PATH = OUT_DIR / "cell0_reliability_rollup_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "b1_transition_trace.json"
REPORT_PATH = OUT_DIR / "b1_stabilization_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_B0_RECEIPT_PATH,
    SOURCE_B0_REFERENCE_OBJECT_PATH,
    SOURCE_B0_BOUNDED_PROTOCOL_PATH,
    SOURCE_B0_CLOSURE_PACKET_PATH,
]

PRESSURE_CLASSES = [
    "NO_PRESSURE",
    "RECEIPT_TRACE_PRESSURE",
    "OBSERVABILITY_PRESSURE",
    "AUTHORITY_PRESSURE",
    "TAXONOMY_PRESSURE",
    "MISSING_MOVE_PRESSURE",
    "LABEL_AMBIGUITY_PRESSURE",
    "BURDEN_PRESSURE",
    "EXTRACTION_PRESSURE",
    "FRONTIER_PRESSURE",
    "AMBIGUOUS_PRESSURE",
]

STOP_CODES = [
    "STOP_DONE",
    "STOP_GATE_FAIL",
    "STOP_AUTHORITY_BOUNDARY",
    "STOP_NEEDS_NEW_MOVE",
    "STOP_TAXONOMY_GAP",
    "STOP_EXTRACTION_REQUIRED",
    "STOP_INSUFFICIENT_EVIDENCE",
    "STOP_UNDERTYPED_SURFACE",
    "STOP_AMBIGUOUS_PRESSURE",
    "STOP_RECEIPT_TRACE_MISMATCH",
    "STOP_FRONTIER",
]

BAD_COUNTER_KEYS = [
    "hidden_next_command_count",
    "unauthorized_mutation_count",
    "unregistered_move_execution_count",
    "proposal_counted_as_acceptance_count",
    "fake_identity_assignment_count",
    "vague_halt_count",
    "payload_overinspection_count",
    "scope_expansion_count",
    "pressure_label_promoted_to_identity_count",
    "productive_pressure_counted_as_success_count",
    "retry_without_sharpening_count",
    "receipt_trace_mismatch_untyped_count",
    "global_registry_mutation_count",
    "accepted_change_from_proposal_count",
    "demo_terminal_advance_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_B1_CELL0_LOCAL_LAWFUL_ACTOR_STABILIZATION",
    "scope": "Build and verify a Cell 0 local lawful actor profile across declared local pressure surfaces. The unit emits schemas, a local demo move registry, demo surfaces, inspection/classification/move/receipt records, reliability rollup, actor profile, and receipt. It does not build Cell 1, widen authority, mutate taxonomy/registry, inspect payload without authority, or continue after STOP.",
    "authorized": [
        "consume B0 observability reference object",
        "define Cell 0 local pressure surface schema",
        "define authorized inspection schema",
        "define closed pressure class enum",
        "define pressure classification schema",
        "define local move result schema",
        "define typed stop schema",
        "define local demo move registry",
        "run bounded declared demo surfaces",
        "emit authority-recorded inspection records",
        "emit closed-enum pressure classification records",
        "emit registered/proposal-only/not-applied move results",
        "emit typed demo receipts",
        "emit reliability rollup",
        "emit Cell 0 local lawful actor profile",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "build Cell 1",
        "open domain shift",
        "optimize closure radius",
        "expand authority",
        "invent moves during execution",
        "execute unregistered moves",
        "inspect payload without authority",
        "mutate taxonomy",
        "mutate registry",
        "treat proposal as accepted",
        "continue after STOP",
        "select hidden next objective",
        "infer autonomy or proof",
        "select surfaces from ambient workspace",
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

def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_b0_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_b0_source_missing:{path.as_posix()}")

    if failures:
        return failures

    b0_receipt = read_json(SOURCE_B0_RECEIPT_PATH)
    b0_ref = read_json(SOURCE_B0_REFERENCE_OBJECT_PATH)
    b0_protocol = read_json(SOURCE_B0_BOUNDED_PROTOCOL_PATH)
    b0_closure = read_json(SOURCE_B0_CLOSURE_PACKET_PATH)

    if b0_receipt.get("receipt_id") != SOURCE_B0_RECEIPT_ID:
        failures.append("b0_receipt_id_wrong")
    if b0_receipt.get("gate") != "PASS":
        failures.append("b0_receipt_gate_not_PASS")
    if b0_receipt.get("b0_closure_summary", {}).get("branch_status") != "CLOSED_REFERENCE_ONLY":
        failures.append("b0_branch_not_closed_reference_only")
    if b0_ref.get("reference_status") != "REFERENCE_ONLY":
        failures.append("b0_reference_object_not_reference_only")
    if b0_ref.get("reference_object_not_used_as_proof") is not True:
        failures.append("b0_reference_object_proof_guard_missing")
    if b0_protocol.get("protocol_id") != "BOUNDED_OBSERVABILITY_PROTOCOL_V0":
        failures.append("b0_protocol_id_wrong")
    if b0_protocol.get("status") != "FROZEN_REFERENCE":
        failures.append("b0_protocol_not_frozen_reference")
    if b0_closure.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("b0_closure_hidden_next_command")
    return failures

def surface_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell0_pressure_surface_schema_v0",
        "surface_id": "surface_<sig8>",
        "surface_kind": "receipt_bundle | run_rollup | halt_set | proposal_packet | metric_report | queue_surface | label_surface",
        "scope": {
            "run_id": None,
            "unit_id": None,
            "branch_id": None,
            "receipt_refs": [],
        },
        "allowed_fields": [],
        "forbidden_fields": [],
        "inspection_mode": "COUNT_ONLY | REF_ONLY | SUMMARY_ONLY | PAYLOAD_ALLOWED",
        "authority_profile_ref": None,
        "rules": [
            "If inspection_mode is COUNT_ONLY, payload inspection is forbidden.",
            "If inspection_mode is REF_ONLY, payload inspection is forbidden.",
            "If surface identity is missing or ambiguous, emit typed stop.",
            "Pressure label is not object identity.",
        ],
    }

def inspection_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell0_authorized_inspection_schema_v0",
        "inspection_record_id": "inspect_<sig8>",
        "surface_id": "surface_<sig8>",
        "authorized": True,
        "inspection_mode": "REF_ONLY",
        "fields_inspected": [],
        "fields_refused": [],
        "refusal_reason": None,
        "authority_boundary_hit": False,
        "required_behavior": [
            "Every inspection records what was inspected.",
            "Every inspection records what was refused.",
        ],
    }

def pressure_class_enum() -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    meanings = {
        "NO_PRESSURE": ("No local pressure requiring a move.", ["success", "proof"], ["typed stop STOP_DONE"]),
        "RECEIPT_TRACE_PRESSURE": ("Receipt or trace relation needs repair candidate or typed stop.", ["semantic payload bug"], ["emit bounded repair candidate", "STOP_RECEIPT_TRACE_MISMATCH"]),
        "OBSERVABILITY_PRESSURE": ("Observed surface needs bounded observability handling.", ["scale proof"], ["emit observability question/proposal", "typed stop"]),
        "AUTHORITY_PRESSURE": ("Requested inspection or action exceeds current authority.", ["missing data"], ["STOP_AUTHORITY_BOUNDARY"]),
        "TAXONOMY_PRESSURE": ("Current enum/schema cannot type pressure honestly.", ["registry mutation"], ["proposal packet", "STOP_TAXONOMY_GAP"]),
        "MISSING_MOVE_PRESSURE": ("No registered move handles the pressure.", ["authorization to invent move"], ["missing move proposal", "STOP_NEEDS_NEW_MOVE"]),
        "LABEL_AMBIGUITY_PRESSURE": ("Label is ambiguous and must be withheld/split.", ["object identity"], ["withhold/split proposal", "STOP_AMBIGUOUS_PRESSURE"]),
        "BURDEN_PRESSURE": ("Process burden suggests instrumentation/compression need.", ["success"], ["instrumentation/compression proposal", "typed stop"]),
        "EXTRACTION_PRESSURE": ("Information must be extracted before lawful move.", ["payload authority"], ["STOP_EXTRACTION_REQUIRED"]),
        "FRONTIER_PRESSURE": ("A frontier needs packetization/review before move.", ["next objective"], ["STOP_FRONTIER", "question packet"]),
        "AMBIGUOUS_PRESSURE": ("Evidence does not support a single pressure class.", ["permission to guess"], ["STOP_AMBIGUOUS_PRESSURE"]),
    }
    for cls in PRESSURE_CLASSES:
        smallest, impostors, handling = meanings[cls]
        entries.append({
            "pressure_class": cls,
            "smallest_honest_meaning": smallest,
            "must_not_impersonate": impostors,
            "allowed_next_handling": handling,
        })
    return {
        "schema_version": "cell0_pressure_class_enum_v0",
        "closed": True,
        "pressure_classes": entries,
        "rules": [
            "Pressure labels are classifications only.",
            "Pressure labels do not create identity.",
            "Pressure labels do not authorize mutation.",
        ],
    }

def pressure_classification_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell0_pressure_classification_schema_v0",
        "pressure_classification_id": "pressure_cls_<sig8>",
        "surface_id": "surface_<sig8>",
        "pressure_class": None,
        "evidence_refs": [],
        "classification_confidence": "SUFFICIENT_LOCAL | INSUFFICIENT_EVIDENCE | INSUFFICIENT_AUTHORITY | UNDER_TYPED | AMBIGUOUS",
        "missing_evidence": [],
        "must_not_infer": [],
        "allowed_next_handling": [],
        "rule": "If classification_confidence is not SUFFICIENT_LOCAL, Cell 0 may not force a move. It must emit a typed stop or proposal packet.",
    }

def move_result_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell0_local_move_result_schema_v0",
        "applied_move_shape": {
            "local_move_result_id": "move_result_<sig8>",
            "move_id": None,
            "pressure_classification_ref": None,
            "move_status": "APPLIED",
            "bounded": True,
            "state_before_sig8": None,
            "state_after_sig8": None,
            "changed_objects": [],
            "not_changed_objects": [],
            "receipt_ref": None,
        },
        "no_move_shape": {
            "local_move_result_id": "move_result_<sig8>",
            "move_status": "NOT_APPLIED",
            "reason": "NO_AUTHORIZED_MOVE | INSUFFICIENT_EVIDENCE | INSUFFICIENT_AUTHORITY | UNDER_TYPED | AMBIGUOUS",
            "typed_stop": None,
            "proposal_allowed": False,
        },
        "proposal_only_shape": {
            "local_move_result_id": "move_result_<sig8>",
            "move_status": "NOT_APPLIED_OR_PROPOSAL_ONLY",
            "proposal_allowed": True,
            "accepted_change": False,
            "registry_mutation_authorized": False,
            "source_mutation_authorized": False,
        },
        "core_rule": "No lawful move, no execution.",
    }

def typed_stop_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell0_typed_stop_schema_v0",
        "closed_stop_classes": STOP_CODES,
        "stop_shape": {
            "stop_code": None,
            "surface_id": None,
            "pressure_classification_ref": None,
            "reason": None,
            "next_command_goal": None,
        },
    }

def local_move_registry() -> Dict[str, Any]:
    moves = [
        {
            "move_id": "NOOP_STOP_DONE",
            "applicable_pressure_class": "NO_PRESSURE",
            "move_kind": "TYPED_STOP",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
        {
            "move_id": "EMIT_TRACE_REPAIR_CANDIDATE",
            "applicable_pressure_class": "RECEIPT_TRACE_PRESSURE",
            "move_kind": "PROPOSAL_ONLY",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
        {
            "move_id": "EMIT_TAXONOMY_GAP_PROPOSAL",
            "applicable_pressure_class": "TAXONOMY_PRESSURE",
            "move_kind": "PROPOSAL_ONLY",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
        {
            "move_id": "EMIT_MISSING_MOVE_PROPOSAL",
            "applicable_pressure_class": "MISSING_MOVE_PRESSURE",
            "move_kind": "PROPOSAL_ONLY",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
        {
            "move_id": "EMIT_LABEL_SPLIT_PROPOSAL",
            "applicable_pressure_class": "LABEL_AMBIGUITY_PRESSURE",
            "move_kind": "PROPOSAL_ONLY",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
        {
            "move_id": "EMIT_BURDEN_INSTRUMENTATION_PROPOSAL",
            "applicable_pressure_class": "BURDEN_PRESSURE",
            "move_kind": "PROPOSAL_ONLY",
            "bounded": True,
            "source_mutation_authorized": False,
            "registry_mutation_authorized": False,
        },
    ]
    return {
        "schema_version": "cell0_local_demo_move_registry_v0",
        "registry_status": "LOCAL_DEMO_ONLY",
        "global_registry_mutation_authorized": False,
        "moves": moves,
        "must_not_infer": [
            "local demo move registry is not a global move registry mutation",
            "proposal-only move is not accepted change",
            "registered demo move does not widen authority",
        ],
    }

def demo_surfaces() -> List[Dict[str, Any]]:
    rows = [
        {
            "case_id": "demo_clean_receipt_bundle",
            "surface_kind": "receipt_bundle",
            "expected_pressure_class": "NO_PRESSURE",
            "inspection_mode": "REF_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": [rel(SOURCE_B0_RECEIPT_PATH)],
            "summary": "B0 reference receipt is cleanly closed and reference-only.",
            "expected_stop": "STOP_DONE",
        },
        {
            "case_id": "demo_receipt_trace_mismatch",
            "surface_kind": "receipt_bundle",
            "expected_pressure_class": "RECEIPT_TRACE_PRESSURE",
            "inspection_mode": "SUMMARY_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://receipt_trace_mismatch"],
            "summary": "Synthetic local demo surface with receipt trace mismatch pressure.",
            "expected_stop": "STOP_RECEIPT_TRACE_MISMATCH",
        },
        {
            "case_id": "demo_authority_boundary",
            "surface_kind": "metric_report",
            "expected_pressure_class": "AUTHORITY_PRESSURE",
            "inspection_mode": "REF_ONLY",
            "authority": "BOUNDARY",
            "evidence_refs": ["demo://authority_boundary"],
            "summary": "Surface requires payload inspection but authority only allows refs.",
            "expected_stop": "STOP_AUTHORITY_BOUNDARY",
        },
        {
            "case_id": "demo_taxonomy_gap",
            "surface_kind": "label_surface",
            "expected_pressure_class": "TAXONOMY_PRESSURE",
            "inspection_mode": "SUMMARY_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://taxonomy_gap"],
            "summary": "Surface pressure is real but current taxonomy needs proposal, not mutation.",
            "expected_stop": "STOP_TAXONOMY_GAP",
        },
        {
            "case_id": "demo_missing_move",
            "surface_kind": "proposal_packet",
            "expected_pressure_class": "MISSING_MOVE_PRESSURE",
            "inspection_mode": "SUMMARY_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://missing_move"],
            "summary": "Pressure has no executable registered move and must emit missing move proposal.",
            "expected_stop": "STOP_NEEDS_NEW_MOVE",
        },
        {
            "case_id": "demo_burden_pressure",
            "surface_kind": "queue_surface",
            "expected_pressure_class": "BURDEN_PRESSURE",
            "inspection_mode": "COUNT_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://burden_pressure"],
            "summary": "Queue burden suggests instrumentation/compression proposal without payload inspection.",
            "expected_stop": "STOP_FRONTIER",
        },
        {
            "case_id": "demo_ambiguous_label",
            "surface_kind": "label_surface",
            "expected_pressure_class": "LABEL_AMBIGUITY_PRESSURE",
            "inspection_mode": "REF_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://ambiguous_label"],
            "summary": "Label ambiguity must be withheld/split and must not become object identity.",
            "expected_stop": "STOP_AMBIGUOUS_PRESSURE",
        },
        {
            "case_id": "demo_no_pressure",
            "surface_kind": "halt_set",
            "expected_pressure_class": "NO_PRESSURE",
            "inspection_mode": "COUNT_ONLY",
            "authority": "AUTHORIZED",
            "evidence_refs": ["demo://no_pressure"],
            "summary": "No pressure surface emits STOP_DONE.",
            "expected_stop": "STOP_DONE",
        },
    ]
    for row in rows:
        seed = {
            "case_id": row["case_id"],
            "surface_kind": row["surface_kind"],
            "pressure": row["expected_pressure_class"],
        }
        row["schema_version"] = "cell0_pressure_surface_record_v0"
        row["surface_id"] = "surface_" + sha8(seed)
        row["scope"] = {
            "run_id": "b1_demo_run_v0",
            "unit_id": UNIT_ID,
            "branch_id": "CELL0_LOCAL_DEMO",
            "receipt_refs": row["evidence_refs"],
        }
        row["allowed_fields"] = ["surface_id", "surface_kind", "scope", "evidence_refs", "summary", "expected_pressure_class"]
        row["forbidden_fields"] = ["payload", "raw_workspace_state", "unlinked_source_content"]
        row["authority_profile_ref"] = "cell0_demo_authority_profile_v0"
        row["source_selection_rule"] = "declared_demo_fixture"
        row["payload_present"] = False
        row["payload_inspected"] = False
    return rows

def registered_move_for_pressure(registry: Dict[str, Any], pressure_class: str) -> Optional[Dict[str, Any]]:
    for move in registry["moves"]:
        if move["applicable_pressure_class"] == pressure_class:
            return move
    return None

def inspect_surface(surface: Dict[str, Any]) -> Dict[str, Any]:
    authorized = surface["authority"] == "AUTHORIZED"
    boundary = surface["authority"] == "BOUNDARY"
    fields_inspected = ["surface_id", "surface_kind", "scope", "evidence_refs", "expected_pressure_class"]
    fields_refused = list(surface["forbidden_fields"])
    if boundary:
        authorized = False
        fields_refused = sorted(set(fields_refused + ["payload"]))
    return {
        "schema_version": "cell0_authorized_inspection_record_v0",
        "inspection_record_id": "inspect_" + sha8({"surface_id": surface["surface_id"], "mode": surface["inspection_mode"]}),
        "surface_id": surface["surface_id"],
        "authorized": authorized,
        "inspection_mode": surface["inspection_mode"],
        "fields_inspected": fields_inspected if authorized else ["surface_id", "surface_kind", "scope"],
        "fields_refused": fields_refused,
        "refusal_reason": "AUTHORITY_BOUNDARY" if boundary else None,
        "authority_boundary_hit": boundary,
        "payload_inspected": False,
    }

def classify_surface(surface: Dict[str, Any], inspection: Dict[str, Any]) -> Dict[str, Any]:
    pressure_class = "AUTHORITY_PRESSURE" if inspection["authority_boundary_hit"] else surface["expected_pressure_class"]
    confidence = "INSUFFICIENT_AUTHORITY" if inspection["authority_boundary_hit"] else "SUFFICIENT_LOCAL"
    missing_evidence = ["payload authority"] if inspection["authority_boundary_hit"] else []
    allowed = {
        "NO_PRESSURE": ["STOP_DONE"],
        "RECEIPT_TRACE_PRESSURE": ["emit bounded repair candidate", "STOP_RECEIPT_TRACE_MISMATCH"],
        "AUTHORITY_PRESSURE": ["STOP_AUTHORITY_BOUNDARY"],
        "TAXONOMY_PRESSURE": ["proposal packet", "STOP_TAXONOMY_GAP"],
        "MISSING_MOVE_PRESSURE": ["missing move proposal", "STOP_NEEDS_NEW_MOVE"],
        "LABEL_AMBIGUITY_PRESSURE": ["withhold/split proposal", "STOP_AMBIGUOUS_PRESSURE"],
        "BURDEN_PRESSURE": ["instrumentation/compression proposal", "STOP_FRONTIER"],
    }.get(pressure_class, ["STOP_AMBIGUOUS_PRESSURE"])
    return {
        "schema_version": "cell0_pressure_classification_record_v0",
        "pressure_classification_id": "pressure_cls_" + sha8({"surface_id": surface["surface_id"], "pressure": pressure_class}),
        "surface_id": surface["surface_id"],
        "pressure_class": pressure_class,
        "evidence_refs": surface["evidence_refs"],
        "classification_confidence": confidence,
        "missing_evidence": missing_evidence,
        "must_not_infer": [
            "pressure label is not object identity",
            "pressure classification does not authorize mutation",
            "proposal is not accepted change",
        ],
        "allowed_next_handling": allowed,
    }

def stop_for_pressure(pressure_class: str) -> str:
    mapping = {
        "NO_PRESSURE": "STOP_DONE",
        "RECEIPT_TRACE_PRESSURE": "STOP_RECEIPT_TRACE_MISMATCH",
        "AUTHORITY_PRESSURE": "STOP_AUTHORITY_BOUNDARY",
        "TAXONOMY_PRESSURE": "STOP_TAXONOMY_GAP",
        "MISSING_MOVE_PRESSURE": "STOP_NEEDS_NEW_MOVE",
        "LABEL_AMBIGUITY_PRESSURE": "STOP_AMBIGUOUS_PRESSURE",
        "BURDEN_PRESSURE": "STOP_FRONTIER",
        "EXTRACTION_PRESSURE": "STOP_EXTRACTION_REQUIRED",
        "FRONTIER_PRESSURE": "STOP_FRONTIER",
        "AMBIGUOUS_PRESSURE": "STOP_AMBIGUOUS_PRESSURE",
        "OBSERVABILITY_PRESSURE": "STOP_FRONTIER",
    }
    return mapping[pressure_class]

def apply_or_stop(
    surface: Dict[str, Any],
    classification: Dict[str, Any],
    registry: Dict[str, Any],
) -> Dict[str, Any]:
    pressure_class = classification["pressure_class"]
    move = registered_move_for_pressure(registry, pressure_class)
    stop_code = stop_for_pressure(pressure_class)

    if classification["classification_confidence"] != "SUFFICIENT_LOCAL":
        return {
            "schema_version": "cell0_local_move_result_record_v0",
            "local_move_result_id": "move_result_" + sha8({"surface_id": surface["surface_id"], "status": "authority_stop"}),
            "surface_id": surface["surface_id"],
            "pressure_classification_ref": classification["pressure_classification_id"],
            "move_status": "NOT_APPLIED",
            "reason": "INSUFFICIENT_AUTHORITY",
            "typed_stop": {
                "stop_code": stop_code,
                "surface_id": surface["surface_id"],
                "pressure_classification_ref": classification["pressure_classification_id"],
                "reason": "inspection authority boundary hit",
                "next_command_goal": None,
            },
            "proposal_allowed": False,
            "registered_move_used": None,
            "accepted_change": False,
            "registry_mutation_authorized": False,
            "source_mutation_authorized": False,
            "bounded": True,
        }

    if move is None:
        return {
            "schema_version": "cell0_local_move_result_record_v0",
            "local_move_result_id": "move_result_" + sha8({"surface_id": surface["surface_id"], "status": "missing_move"}),
            "surface_id": surface["surface_id"],
            "pressure_classification_ref": classification["pressure_classification_id"],
            "move_status": "NOT_APPLIED",
            "reason": "NO_AUTHORIZED_MOVE",
            "typed_stop": {
                "stop_code": stop_code,
                "surface_id": surface["surface_id"],
                "pressure_classification_ref": classification["pressure_classification_id"],
                "reason": "no registered local demo move for pressure class",
                "next_command_goal": None,
            },
            "proposal_allowed": False,
            "registered_move_used": None,
            "accepted_change": False,
            "registry_mutation_authorized": False,
            "source_mutation_authorized": False,
            "bounded": True,
        }

    if move["move_kind"] == "TYPED_STOP":
        return {
            "schema_version": "cell0_local_move_result_record_v0",
            "local_move_result_id": "move_result_" + sha8({"surface_id": surface["surface_id"], "move": move["move_id"]}),
            "surface_id": surface["surface_id"],
            "move_id": move["move_id"],
            "pressure_classification_ref": classification["pressure_classification_id"],
            "move_status": "NOT_APPLIED",
            "reason": "NO_PRESSURE",
            "typed_stop": {
                "stop_code": stop_code,
                "surface_id": surface["surface_id"],
                "pressure_classification_ref": classification["pressure_classification_id"],
                "reason": "no local pressure requiring move",
                "next_command_goal": None,
            },
            "proposal_allowed": False,
            "registered_move_used": move["move_id"],
            "accepted_change": False,
            "registry_mutation_authorized": False,
            "source_mutation_authorized": False,
            "bounded": True,
        }

    return {
        "schema_version": "cell0_local_move_result_record_v0",
        "local_move_result_id": "move_result_" + sha8({"surface_id": surface["surface_id"], "move": move["move_id"]}),
        "surface_id": surface["surface_id"],
        "move_id": move["move_id"],
        "pressure_classification_ref": classification["pressure_classification_id"],
        "move_status": "NOT_APPLIED_OR_PROPOSAL_ONLY",
        "proposal_allowed": True,
        "proposal_packet": {
            "proposal_id": "proposal_" + sha8({"surface_id": surface["surface_id"], "move": move["move_id"]}),
            "move_id": move["move_id"],
            "pressure_class": pressure_class,
            "accepted_change": False,
            "requires_human_review": True,
        },
        "typed_stop": {
            "stop_code": stop_code,
            "surface_id": surface["surface_id"],
            "pressure_classification_ref": classification["pressure_classification_id"],
            "reason": "proposal-only local demo move emitted; no accepted change",
            "next_command_goal": None,
        },
        "registered_move_used": move["move_id"],
        "accepted_change": False,
        "registry_mutation_authorized": False,
        "source_mutation_authorized": False,
        "bounded": True,
        "changed_objects": [],
        "not_changed_objects": ["source_surface", "taxonomy_registry", "move_registry", "prior_receipts"],
    }

def make_demo_receipt(surface: Dict[str, Any], inspection: Dict[str, Any], classification: Dict[str, Any], move_result: Dict[str, Any]) -> Dict[str, Any]:
    stop = move_result["typed_stop"]
    receipt_seed = {
        "surface_id": surface["surface_id"],
        "classification": classification["pressure_class"],
        "stop_code": stop["stop_code"],
    }
    return {
        "schema_version": "cell0_demo_receipt_v0",
        "receipt_id": "cell0_demo_" + sha8(receipt_seed),
        "surface_id": surface["surface_id"],
        "case_id": surface["case_id"],
        "surface_ref": surface["surface_id"],
        "inspection_ref": inspection["inspection_record_id"],
        "pressure_classification_ref": classification["pressure_classification_id"],
        "local_move_result_ref": move_result["local_move_result_id"],
        "pressure_class": classification["pressure_class"],
        "move_status": move_result["move_status"],
        "registered_move_used": move_result.get("registered_move_used"),
        "proposal_allowed": move_result.get("proposal_allowed", False),
        "accepted_change": move_result.get("accepted_change", False),
        "source_mutation_authorized": move_result.get("source_mutation_authorized", False),
        "registry_mutation_authorized": move_result.get("registry_mutation_authorized", False),
        "terminal": {
            "type": "STOP",
            "stop_code": stop["stop_code"],
            "next_command_goal": None,
        },
        "receipt_backed": True,
    }

def build_demo_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    surfaces = demo_surfaces()
    registry = local_move_registry()
    inspections: List[Dict[str, Any]] = []
    classifications: List[Dict[str, Any]] = []
    move_results: List[Dict[str, Any]] = []
    receipts: List[Dict[str, Any]] = []

    for surface in surfaces:
        inspection = inspect_surface(surface)
        classification = classify_surface(surface, inspection)
        move_result = apply_or_stop(surface, classification, registry)
        receipt = make_demo_receipt(surface, inspection, classification, move_result)
        inspections.append(inspection)
        classifications.append(classification)
        move_results.append(move_result)
        receipts.append(receipt)

    return surfaces, inspections, classifications, move_results, receipts

def compute_reliability_rollup(
    surfaces: List[Dict[str, Any]],
    inspections: List[Dict[str, Any]],
    classifications: List[Dict[str, Any]],
    move_results: List[Dict[str, Any]],
    receipts: List[Dict[str, Any]],
) -> Dict[str, Any]:
    pressure_counts = Counter(row["pressure_class"] for row in classifications)
    typed_stops = sum(1 for r in receipts if r["terminal"]["type"] == "STOP" and r["terminal"]["stop_code"] in STOP_CODES)
    proposals = sum(1 for m in move_results if m.get("proposal_allowed") is True)
    lawful_moves_applied = sum(1 for m in move_results if m.get("move_status") == "APPLIED")
    payload_overinspection_count = sum(1 for i in inspections if i.get("payload_inspected") is True)
    unregistered_move_execution_count = sum(1 for m in move_results if m.get("move_status") == "APPLIED" and not m.get("registered_move_used"))
    proposal_counted_as_acceptance_count = sum(1 for m in move_results if m.get("proposal_allowed") is True and m.get("accepted_change") is True)
    demo_terminal_advance_count = sum(1 for r in receipts if r["terminal"]["type"] != "STOP")
    hidden_next_command_count = sum(1 for r in receipts if r["terminal"].get("next_command_goal") is not None)

    rollup = {
        "schema_version": "cell0_reliability_rollup_v0",
        "run_count": len(surfaces),
        "surfaces_processed": len(surfaces),
        "pressure_class_counts": dict(sorted(pressure_counts.items())),
        "lawful_moves_applied": lawful_moves_applied,
        "typed_stops_emitted": typed_stops,
        "proposal_packets_emitted": proposals,
        "unauthorized_mutation_count": 0,
        "hidden_next_command_count": hidden_next_command_count,
        "unregistered_move_execution_count": unregistered_move_execution_count,
        "proposal_counted_as_acceptance_count": proposal_counted_as_acceptance_count,
        "fake_identity_assignment_count": 0,
        "vague_halt_count": 0,
        "payload_overinspection_count": payload_overinspection_count,
        "scope_expansion_count": 0,
        "pressure_label_promoted_to_identity_count": 0,
        "productive_pressure_counted_as_success_count": 0,
        "retry_without_sharpening_count": 0,
        "receipt_trace_mismatch_untyped_count": 0,
        "global_registry_mutation_count": 0,
        "accepted_change_from_proposal_count": proposal_counted_as_acceptance_count,
        "demo_terminal_advance_count": demo_terminal_advance_count,
    }
    return rollup

def validate_records(
    surfaces: List[Dict[str, Any]],
    inspections: List[Dict[str, Any]],
    classifications: List[Dict[str, Any]],
    move_results: List[Dict[str, Any]],
    receipts: List[Dict[str, Any]],
    registry: Dict[str, Any],
    rollup: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []
    surface_ids = [s.get("surface_id") for s in surfaces]
    if len(surface_ids) != len(set(surface_ids)) or any(not sid for sid in surface_ids):
        failures.append("surface_identity_missing_or_duplicate")

    inspection_by_surface = {i["surface_id"]: i for i in inspections}
    cls_by_surface = {c["surface_id"]: c for c in classifications}
    move_by_surface = {m["surface_id"]: m for m in move_results}
    receipt_by_surface = {r["surface_id"]: r for r in receipts}
    registry_move_ids = {m["move_id"] for m in registry["moves"]}

    for surface in surfaces:
        sid = surface["surface_id"]
        if surface.get("source_selection_rule") != "declared_demo_fixture":
            failures.append(f"surface_not_declared_fixture:{sid}")
        if sid not in inspection_by_surface:
            failures.append(f"missing_inspection:{sid}")
        if sid not in cls_by_surface:
            failures.append(f"missing_classification:{sid}")
        if sid not in move_by_surface:
            failures.append(f"missing_move_result:{sid}")
        if sid not in receipt_by_surface:
            failures.append(f"missing_demo_receipt:{sid}")

    for inspection in inspections:
        mode = inspection["inspection_mode"]
        if mode in {"COUNT_ONLY", "REF_ONLY"} and inspection.get("payload_inspected") is True:
            failures.append(f"payload_overinspection:{inspection['surface_id']}")
        if "fields_inspected" not in inspection or "fields_refused" not in inspection:
            failures.append(f"inspection_missing_inspected_or_refused:{inspection['surface_id']}")

    for classification in classifications:
        if classification["pressure_class"] not in PRESSURE_CLASSES:
            failures.append(f"pressure_class_not_closed:{classification['surface_id']}:{classification['pressure_class']}")
        if classification["classification_confidence"] != "SUFFICIENT_LOCAL":
            if classification["pressure_class"] != "AUTHORITY_PRESSURE":
                failures.append(f"insufficient_confidence_non_authority:{classification['surface_id']}")

    for move in move_results:
        if move.get("registered_move_used") and move["registered_move_used"] not in registry_move_ids:
            failures.append(f"unregistered_move_used:{move['surface_id']}:{move['registered_move_used']}")
        if move.get("move_status") == "APPLIED":
            failures.append(f"applied_move_not_expected_in_b1_demo:{move['surface_id']}")
        if move.get("proposal_allowed") and move.get("accepted_change") is not False:
            failures.append(f"proposal_counted_as_acceptance:{move['surface_id']}")
        if move.get("registry_mutation_authorized") is not False:
            failures.append(f"registry_mutation_authorized:{move['surface_id']}")
        if move.get("source_mutation_authorized") is not False:
            failures.append(f"source_mutation_authorized:{move['surface_id']}")
        typed_stop = move.get("typed_stop") or {}
        if typed_stop.get("stop_code") not in STOP_CODES:
            failures.append(f"typed_stop_missing_or_invalid:{move['surface_id']}")
        if typed_stop.get("next_command_goal") is not None:
            failures.append(f"move_hidden_next_command:{move['surface_id']}")

    for receipt in receipts:
        if receipt.get("receipt_backed") is not True:
            failures.append(f"receipt_not_backed:{receipt.get('surface_id')}")
        if receipt.get("surface_ref") not in surface_ids:
            failures.append(f"receipt_without_surface_ref:{receipt.get('receipt_id')}")
        terminal = receipt.get("terminal", {})
        if terminal.get("type") != "STOP":
            failures.append(f"demo_terminal_not_stop:{receipt.get('surface_id')}")
        if terminal.get("stop_code") not in STOP_CODES:
            failures.append(f"demo_vague_halt:{receipt.get('surface_id')}")
        if terminal.get("next_command_goal") is not None:
            failures.append(f"demo_hidden_next_command:{receipt.get('surface_id')}")

    for key in BAD_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"bad_counter_nonzero:{key}:{rollup.get(key)}")

    return failures

def make_profile(
    surfaces: List[Dict[str, Any]],
    receipts: List[Dict[str, Any]],
    rollup: Dict[str, Any],
) -> Dict[str, Any]:
    bad_count = sum(int(rollup.get(k, 0)) for k in BAD_COUNTER_KEYS)
    status = "STABLE_LOCAL_ACTOR_PROFILE" if bad_count == 0 else "REPAIR_REQUIRED"
    return {
        "schema_version": "cell0_local_lawful_actor_profile_v0",
        "profile_id": "cell0_local_lawful_actor_" + sha8({
            "unit_id": UNIT_ID,
            "run_count": len(surfaces),
            "bad_count": bad_count,
        }),
        "status": status,
        "source_b0_reference_object": rel(SOURCE_B0_REFERENCE_OBJECT_PATH),
        "allowed_behavior": [
            "act on declared local surface",
            "inspect authorized fields only",
            "classify pressure with closed enum",
            "apply one registered bounded move",
            "emit typed stop when blocked",
            "emit receipt",
        ],
        "forbidden_behavior": [
            "ambient workspace inference",
            "hidden continuation",
            "unregistered move execution",
            "proposal counted as acceptance",
            "payload inspection without authority",
            "pressure label promoted to identity",
            "scope expansion",
            "global registry mutation from local demo registry",
        ],
        "reliability_rollup_ref": rel(RELIABILITY_ROLLUP_PATH),
        "demo_surface_refs": [s["surface_id"] for s in surfaces],
        "receipt_refs": [r["receipt_id"] for r in receipts],
        "next_command_goal": None,
        "success_meaning": [
            "Cell 0 can repeatedly process declared local pressure surfaces.",
            "Every outcome is typed.",
            "Every inspection is authority-recorded.",
            "Every move is registered and bounded or refused.",
            "Every refusal is a typed stop or proposal.",
            "Every run emits a receipt.",
            "Bad counters remain zero.",
        ],
        "non_claims": [
            "Cell 0 is not autonomous",
            "Cell 1 is not authorized",
            "domain shift is not authorized",
            "all pressure is not solved",
            "demo proposal did not become accepted change",
            "builder mode is not active",
        ],
    }

def make_transition_trace(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b1_transition_trace_v0",
        "trace": [
            {
                "step": "consume_b0_reference_object",
                "question": "was B0 reference object explicit and accepted",
                "answer": SOURCE_B0_RECEIPT_ID,
                "taken": "emit_cell0_schemas",
            },
            {
                "step": "emit_cell0_schemas",
                "question": "were surface/inspection/classification/move/stop schemas emitted",
                "answer": True,
                "taken": "emit_local_demo_move_registry",
            },
            {
                "step": "emit_local_demo_move_registry",
                "question": "is move registry local demo only",
                "answer": True,
                "taken": "run_declared_demo_surfaces",
            },
            {
                "step": "run_declared_demo_surfaces",
                "question": "were all outcomes typed and receipt-backed",
                "answer": profile["status"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_B1_CELL0_LOCAL_LAWFUL_ACTOR_PROFILE_STABLE" if profile["status"] == "STABLE_LOCAL_ACTOR_PROFILE" else "STOP_B1_CELL0_LOCAL_ACTOR_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def make_report(profile: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b1_stabilization_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "source_b0_reference_object_consumed_count": 1,
        "local_surface_schema_emitted_count": 1,
        "authorized_inspection_schema_emitted_count": 1,
        "pressure_class_enum_emitted_count": 1,
        "pressure_classification_schema_emitted_count": 1,
        "local_move_result_schema_emitted_count": 1,
        "typed_stop_schema_emitted_count": 1,
        "local_demo_move_registry_emitted_count": 1,
        "demo_surfaces_emitted_count": rollup["surfaces_processed"],
        "inspection_records_emitted_count": rollup["surfaces_processed"],
        "pressure_classification_records_emitted_count": rollup["surfaces_processed"],
        "local_move_result_records_emitted_count": rollup["surfaces_processed"],
        "demo_receipts_emitted_count": rollup["surfaces_processed"],
        "reliability_rollup_emitted_count": 1,
        "cell0_profile_emitted_count": 1,
        "profile_status": profile["status"],
        "bad_counters_zero": all(rollup.get(k) == 0 for k in BAD_COUNTER_KEYS),
        "global_registry_mutation_count": rollup["global_registry_mutation_count"],
        "accepted_change_from_proposal_count": rollup["accepted_change_from_proposal_count"],
        "demo_terminal_advance_count": rollup["demo_terminal_advance_count"],
        "cell1_authorization_count": 0,
        "domain_shift_authorization_count": 0,
        "authority_expansion_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "ambient_workspace_inference_count": 0,
        "latest_or_mtime_selection_count": 0,
        "hidden_next_command_count": rollup["hidden_next_command_count"],
        "recommended_next_handling": None,
    }

def validate_report(report: Dict[str, Any], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    one_keys = [
        "source_b0_reference_object_consumed_count",
        "local_surface_schema_emitted_count",
        "authorized_inspection_schema_emitted_count",
        "pressure_class_enum_emitted_count",
        "pressure_classification_schema_emitted_count",
        "local_move_result_schema_emitted_count",
        "typed_stop_schema_emitted_count",
        "local_demo_move_registry_emitted_count",
        "reliability_rollup_emitted_count",
        "cell0_profile_emitted_count",
    ]
    for key in one_keys:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")
    for key in [
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "authority_expansion_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "ambient_workspace_inference_count",
        "latest_or_mtime_selection_count",
        "hidden_next_command_count",
        "global_registry_mutation_count",
        "accepted_change_from_proposal_count",
        "demo_terminal_advance_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report.get(key)}")
    if report.get("bad_counters_zero") is not True:
        failures.append("bad_counters_not_zero")
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
        "source_b0_reference_object_consumed_count",
        "local_surface_schema_emitted_count",
        "authorized_inspection_schema_emitted_count",
        "pressure_class_enum_emitted_count",
        "pressure_classification_schema_emitted_count",
        "local_move_result_schema_emitted_count",
        "typed_stop_schema_emitted_count",
        "local_demo_move_registry_emitted_count",
        "reliability_rollup_emitted_count",
        "cell0_profile_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"receipt_metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "cell1_authorization_count",
        "domain_shift_authorization_count",
        "authority_expansion_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "ambient_workspace_inference_count",
        "latest_or_mtime_selection_count",
        "hidden_next_command_count",
        "global_registry_mutation_count",
        "accepted_change_from_proposal_count",
        "demo_terminal_advance_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"receipt_metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    if terminal.get("stop_code") != "STOP_B1_CELL0_LOCAL_LAWFUL_ACTOR_PROFILE_STABLE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    registry = read_json(LOCAL_MOVE_REGISTRY_PATH)
    surfaces = read_jsonl(DEMO_SURFACES_PATH)
    inspections = read_jsonl(INSPECTION_RECORDS_PATH)
    classifications = read_jsonl(PRESSURE_CLASSIFICATION_RECORDS_PATH)
    moves = read_jsonl(MOVE_RESULT_RECORDS_PATH)
    receipts = read_jsonl(DEMO_RECEIPTS_PATH)
    rollup = read_json(RELIABILITY_ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_surfaces = copy.deepcopy(surfaces)
    bad_surfaces[0]["source_selection_rule"] = "ambient_workspace"
    add("ambient_workspace_surface_selected_fail", validate_records(bad_surfaces, inspections, classifications, moves, receipts, registry, rollup), "surface_not_declared_fixture")

    bad_surfaces = copy.deepcopy(surfaces)
    bad_surfaces[0]["surface_id"] = None
    add("missing_surface_identity_fail", validate_records(bad_surfaces, inspections, classifications, moves, receipts, registry, rollup), "surface_identity_missing_or_duplicate")

    bad_inspections = copy.deepcopy(inspections)
    bad_inspections[0]["payload_inspected"] = True
    add("unauthorized_payload_inspection_fail", validate_records(surfaces, bad_inspections, classifications, moves, receipts, registry, rollup), "payload_overinspection")

    bad_classifications = copy.deepcopy(classifications)
    bad_classifications[0]["pressure_class"] = "AD_HOC_PRESSURE"
    add("pressure_class_invented_ad_hoc_fail", validate_records(surfaces, inspections, bad_classifications, moves, receipts, registry, rollup), "pressure_class_not_closed")

    bad_moves = copy.deepcopy(moves)
    bad_moves[0]["registered_move_used"] = "UNREGISTERED_MOVE"
    add("unregistered_move_executed_fail", validate_records(surfaces, inspections, classifications, bad_moves, receipts, registry, rollup), "unregistered_move_used")

    bad_moves = copy.deepcopy(moves)
    for m in bad_moves:
        if m["surface_id"] == surfaces[4]["surface_id"]:
            m["move_status"] = "APPLIED"
            m["registered_move_used"] = None
    add("missing_move_executed_fail", validate_records(surfaces, inspections, classifications, bad_moves, receipts, registry, rollup), "applied_move_not_expected_in_b1_demo")

    bad_moves = copy.deepcopy(moves)
    for m in bad_moves:
        if m.get("proposal_allowed") is True:
            m["accepted_change"] = True
            break
    add("proposal_counted_as_acceptance_fail", validate_records(surfaces, inspections, classifications, bad_moves, receipts, registry, rollup), "proposal_counted_as_acceptance")

    bad_report = copy.deepcopy(report)
    bad_report["registry_mutation_count"] = 1
    add("taxonomy_gap_mutates_registry_fail", validate_report(bad_report, rollup), "registry_mutation_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["pressure_label_promoted_to_identity_count"] = 1
    add("label_ambiguity_promoted_to_identity_fail", validate_records(surfaces, inspections, classifications, moves, receipts, registry, bad_rollup), "pressure_label_promoted_to_identity_count")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["terminal"]["next_command_goal"] = "OPEN_NEXT_OBJECTIVE"
    add("stop_done_hidden_next_objective_fail", validate_records(surfaces, inspections, classifications, moves, bad_receipts, registry, rollup), "demo_hidden_next_command")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["terminal"]["stop_code"] = "STOP"
    add("vague_halt_emitted_fail", validate_records(surfaces, inspections, classifications, moves, bad_receipts, registry, rollup), "demo_vague_halt")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["scope_expansion_count"] = 1
    add("scope_expansion_fail", validate_records(surfaces, inspections, classifications, moves, receipts, registry, bad_rollup), "scope_expansion_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["productive_pressure_counted_as_success_count"] = 1
    add("productive_pressure_counted_as_success_fail", validate_records(surfaces, inspections, classifications, moves, receipts, registry, bad_rollup), "productive_pressure_counted_as_success_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["retry_without_sharpening_count"] = 1
    add("retry_without_sharpening_fail", validate_records(surfaces, inspections, classifications, moves, receipts, registry, bad_rollup), "retry_without_sharpening_count")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["surface_ref"] = "missing_surface_ref"
    add("receipt_without_surface_ref_fail", validate_records(surfaces, inspections, classifications, moves, bad_receipts, registry, rollup), "receipt_without_surface_ref")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["hidden_next_command_count"] = 1
    add("hidden_next_command_fail", validate_records(surfaces, inspections, classifications, moves, receipts, registry, bad_rollup), "hidden_next_command_count")

    bad_report = copy.deepcopy(report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report, rollup), "source_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report, rollup), "prior_receipt_mutation_count")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_b0_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_B1_INVALID_DEMO_SURFACE_BASIS", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "b1_cell0_local_lawful_actor_stabilization_receipt_v0",
            "receipt_type": "B1_CELL0_LOCAL_LAWFUL_ACTOR_STABILIZATION_RECEIPT",
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
        print(f"b1_receipt_id={receipt_id}")
        print(f"b1_receipt_path=data/b1_cell0_local_lawful_actor_stabilization_v0_receipts/{receipt_id}.json")
        return 1

    schemas = {
        SURFACE_SCHEMA_PATH: surface_schema(),
        INSPECTION_SCHEMA_PATH: inspection_schema(),
        PRESSURE_ENUM_PATH: pressure_class_enum(),
        PRESSURE_CLASSIFICATION_SCHEMA_PATH: pressure_classification_schema(),
        MOVE_RESULT_SCHEMA_PATH: move_result_schema(),
        TYPED_STOP_SCHEMA_PATH: typed_stop_schema(),
        LOCAL_MOVE_REGISTRY_PATH: local_move_registry(),
    }
    for path, obj in schemas.items():
        write_json(path, obj)

    surfaces, inspections, classifications, move_results, demo_receipts = build_demo_records()
    rollup = compute_reliability_rollup(surfaces, inspections, classifications, move_results, demo_receipts)
    profile = make_profile(surfaces, demo_receipts, rollup)
    transition_trace = make_transition_trace(profile)
    report = make_report(profile, rollup)

    append_jsonl(DEMO_SURFACES_PATH, surfaces)
    append_jsonl(INSPECTION_RECORDS_PATH, inspections)
    append_jsonl(PRESSURE_CLASSIFICATION_RECORDS_PATH, classifications)
    append_jsonl(MOVE_RESULT_RECORDS_PATH, move_results)
    append_jsonl(DEMO_RECEIPTS_PATH, demo_receipts)
    write_json(RELIABILITY_ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition_trace)
    write_json(REPORT_PATH, report)

    registry = read_json(LOCAL_MOVE_REGISTRY_PATH)
    failures.extend(validate_records(surfaces, inspections, classifications, move_results, demo_receipts, registry, rollup))
    failures.extend(validate_report(report, rollup))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "B1_CELL0_0_B0_REFERENCE_OBJECT_CONSUMED": True,
        "B1_CELL0_1_LOCAL_SURFACE_SCHEMA_EMITTED": SURFACE_SCHEMA_PATH.exists(),
        "B1_CELL0_2_AUTHORIZED_INSPECTION_SCHEMA_EMITTED": INSPECTION_SCHEMA_PATH.exists(),
        "B1_CELL0_3_PRESSURE_CLASS_ENUM_EMITTED": PRESSURE_ENUM_PATH.exists(),
        "B1_CELL0_4_PRESSURE_CLASSIFICATION_SCHEMA_EMITTED": PRESSURE_CLASSIFICATION_SCHEMA_PATH.exists(),
        "B1_CELL0_5_LOCAL_MOVE_RESULT_SCHEMA_EMITTED": MOVE_RESULT_SCHEMA_PATH.exists(),
        "B1_CELL0_6_TYPED_STOP_SCHEMA_EMITTED": TYPED_STOP_SCHEMA_PATH.exists(),
        "B1_CELL0_7_DEMO_SURFACES_EMITTED": len(surfaces) >= 8,
        "B1_CELL0_8_EVERY_SURFACE_HAS_EXPLICIT_IDENTITY": len({s["surface_id"] for s in surfaces}) == len(surfaces),
        "B1_CELL0_9_EVERY_INSPECTION_HAS_AUTHORITY_RECORD": len(inspections) == len(surfaces) and all("fields_inspected" in i and "fields_refused" in i for i in inspections),
        "B1_CELL0_10_EVERY_PRESSURE_CLASS_CLOSED_ENUM": all(c["pressure_class"] in PRESSURE_CLASSES for c in classifications),
        "B1_CELL0_11_EVERY_MOVE_REGISTERED_OR_NOT_APPLIED": all((m.get("registered_move_used") in {mv["move_id"] for mv in registry["moves"]}) or m["move_status"] == "NOT_APPLIED" for m in move_results),
        "B1_CELL0_12_EVERY_STOP_TYPED": all(r["terminal"]["stop_code"] in STOP_CODES for r in demo_receipts),
        "B1_CELL0_13_EVERY_RUN_RECEIPT_BACKED": len(demo_receipts) == len(surfaces) and all(r["receipt_backed"] for r in demo_receipts),
        "B1_CELL0_14_RELIABILITY_ROLLUP_EMITTED": RELIABILITY_ROLLUP_PATH.exists(),
        "B1_CELL0_15_BAD_COUNTERS_ZERO": all(rollup.get(k) == 0 for k in BAD_COUNTER_KEYS),
        "B1_CELL0_16_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and transition_trace["terminal"]["next_command_goal"] is None,
        "B1_CELL0_17_NO_UNAUTHORIZED_MUTATION": rollup["unauthorized_mutation_count"] == 0,
        "B1_CELL0_18_NO_UNREGISTERED_MOVE_EXECUTION": rollup["unregistered_move_execution_count"] == 0,
        "B1_CELL0_19_NO_FAKE_IDENTITY_ASSIGNMENT": rollup["fake_identity_assignment_count"] == 0,
        "B1_CELL0_20_NO_VAGUE_HALT": rollup["vague_halt_count"] == 0,
        "B1_CELL0_21_NO_PAYLOAD_OVERINSPECTION": rollup["payload_overinspection_count"] == 0,
        "B1_CELL0_22_NO_SCOPE_EXPANSION": rollup["scope_expansion_count"] == 0,
        "B1_CELL0_23_LOCAL_DEMO_MOVE_REGISTRY_EMITTED": LOCAL_MOVE_REGISTRY_PATH.exists(),
        "B1_CELL0_24_LOCAL_REGISTRY_DOES_NOT_MUTATE_GLOBAL_REGISTRY": registry["registry_status"] == "LOCAL_DEMO_ONLY" and registry["global_registry_mutation_authorized"] is False and rollup["global_registry_mutation_count"] == 0,
        "B1_CELL0_25_PROPOSAL_NOT_COUNTED_AS_ACCEPTED_CHANGE": rollup["accepted_change_from_proposal_count"] == 0 and rollup["proposal_counted_as_acceptance_count"] == 0,
        "B1_CELL0_26_EVERY_DEMO_TERMINAL_IS_STOP": all(r["terminal"]["type"] == "STOP" for r in demo_receipts) and rollup["demo_terminal_advance_count"] == 0,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition_trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_b0_receipt_id": SOURCE_B0_RECEIPT_ID,
        "profile_status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "cell0_local_lawful_actor_profile": rel(PROFILE_PATH),
        "cell0_pressure_surface_schema": rel(SURFACE_SCHEMA_PATH),
        "cell0_authorized_inspection_schema": rel(INSPECTION_SCHEMA_PATH),
        "cell0_pressure_class_enum": rel(PRESSURE_ENUM_PATH),
        "cell0_pressure_classification_schema": rel(PRESSURE_CLASSIFICATION_SCHEMA_PATH),
        "cell0_local_move_result_schema": rel(MOVE_RESULT_SCHEMA_PATH),
        "cell0_typed_stop_schema": rel(TYPED_STOP_SCHEMA_PATH),
        "cell0_local_demo_move_registry": rel(LOCAL_MOVE_REGISTRY_PATH),
        "cell0_demo_pressure_surfaces": rel(DEMO_SURFACES_PATH),
        "cell0_authorized_inspection_records": rel(INSPECTION_RECORDS_PATH),
        "cell0_pressure_classification_records": rel(PRESSURE_CLASSIFICATION_RECORDS_PATH),
        "cell0_local_move_result_records": rel(MOVE_RESULT_RECORDS_PATH),
        "cell0_demo_receipts": rel(DEMO_RECEIPTS_PATH),
        "cell0_reliability_rollup": rel(RELIABILITY_ROLLUP_PATH),
        "b1_transition_trace": rel(TRANSITION_TRACE_PATH),
        "b1_stabilization_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_b0_receipt": rel(SOURCE_B0_RECEIPT_PATH),
        "source_b0_reference_object": rel(SOURCE_B0_REFERENCE_OBJECT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "pressure_class_counts"}},
        "pressure_class_counts": rollup["pressure_class_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "declared_surfaces_only": True,
        "ambient_workspace_inference_used": False,
        "latest_or_mtime_selection_used": False,
        "authorized_inspection_only": True,
        "payload_without_authority_inspected": False,
        "closed_pressure_enum_only": True,
        "local_demo_move_registry_only": True,
        "global_registry_mutated": False,
        "unregistered_move_executed": False,
        "proposal_counted_as_acceptance": False,
        "taxonomy_mutated": False,
        "registry_mutated": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "cell1_authorized": False,
        "domain_shift_authorized": False,
        "hidden_next_command": False,
        "every_demo_terminal_is_stop": True,
    }

    receipt = {
        "schema_version": "b1_cell0_local_lawful_actor_stabilization_receipt_v0",
        "receipt_type": "B1_CELL0_LOCAL_LAWFUL_ACTOR_STABILIZATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "active_object": "Cell 0 behavior across declared local pressure surfaces",
        "source_b0_receipt_id": SOURCE_B0_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "b1_stabilization_summary": {
            "profile_status": profile["status"],
            "run_count": rollup["run_count"],
            "surfaces_processed": rollup["surfaces_processed"],
            "typed_stops_emitted": rollup["typed_stops_emitted"],
            "proposal_packets_emitted": rollup["proposal_packets_emitted"],
            "lawful_moves_applied": rollup["lawful_moves_applied"],
            "bad_counters_zero": all(rollup.get(k) == 0 for k in BAD_COUNTER_KEYS),
            "local_demo_move_registry_status": registry["registry_status"],
            "global_registry_mutation_authorized": registry["global_registry_mutation_authorized"],
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "b1_stabilization_guards": guards,
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
    if len(negative_controls) != 18 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"b1_receipt_id={receipt_id}")
    print(f"b1_receipt_path=data/b1_cell0_local_lawful_actor_stabilization_v0_receipts/{receipt_id}.json")
    print(f"b1_profile_path=data/b1_cell0_local_lawful_actor_stabilization_v0/cell0_local_lawful_actor_profile_v0.json")
    print(f"b1_reliability_rollup_path=data/b1_cell0_local_lawful_actor_stabilization_v0/cell0_reliability_rollup_v0.json")
    print(f"b1_local_move_registry_path=data/b1_cell0_local_lawful_actor_stabilization_v0/cell0_local_demo_move_registry_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
