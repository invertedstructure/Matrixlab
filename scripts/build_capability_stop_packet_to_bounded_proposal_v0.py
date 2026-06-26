#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_CAPABILITY_STOP_PACKET_TO_BOUNDED_PROPOSAL_V0"
TARGET_UNIT_ID = "capability_stop_packet_to_bounded_proposal.v0"
SOURCE_T6_SURFACE_AUDIT_RECEIPT_ID = "82726f6b"

SOURCE_RECEIPT_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0_receipts/82726f6b.json"
SOURCE_STOP_PACKET_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_capability_stop_packet_v0.json"
SOURCE_PARENT_RETURN_PAYLOAD_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_parent_return_payload_v0.json"
SOURCE_MISSING_OBJECT_DIAGNOSIS_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_missing_object_diagnosis_v0.json"
SOURCE_CAPABILITY_BOUNDARY_ASSESSMENT_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_capability_boundary_assessment_v0.json"
SOURCE_CURRENT_SURFACE_INVENTORY_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_current_surface_inventory_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_capability_boundary_surface_audit_profile_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0/runtime_t6_capability_boundary_surface_audit_rollup_v0.json"

OUT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0"
RECEIPT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts"

INTAKE_REVIEW_PATH = OUT_DIR / "capability_stop_packet_intake_review_v0.json"
NORMALIZED_STOP_PACKET_PATH = OUT_DIR / "capability_stop_packet_v0.json"
PROPOSAL_PATH = OUT_DIR / "bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = OUT_DIR / "human_capability_decision_packet_v0.json"
TRACE_PATH = OUT_DIR / "capability_proposal_adapter_trace_v0.jsonl"
READOUT_PATH = OUT_DIR / "capability_proposal_adapter_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "capability_proposal_adapter_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "capability_proposal_adapter_profile_v0.json"
REPORT_PATH = OUT_DIR / "capability_proposal_adapter_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "capability_proposal_adapter_transition_trace.json"

ALLOWED_STOP_CODES = {
    "STOP_CAPABILITY_LAYER_REQUIRED",
}

ALLOWED_AUDIT_RESULT_KINDS = {
    "STOP_CAPABILITY_LAYER_REQUIRED",
    "CAPABILITY_BOUNDARY_REACHED",
    "MISSING_CAPABILITY_STOP",
}

PROPOSAL_KIND_ENUM = {
    "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_EVIDENCE_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_REFERENCE_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_OBSERVABILITY_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_FEEDBACK_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_CLASSIFICATION_CAPABILITY_PROPOSAL",
    "BOUNDED_VALIDATION_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_ADMISSIBILITY_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_RUNTIME_STATE_SURFACE_CAPABILITY_PROPOSAL",
    "BOUNDED_MOVE_REGISTRY_SURFACE_CAPABILITY_PROPOSAL",
}

NEGATIVE_CONTROLS_ZERO = {
    "implementation_started_count": 0,
    "runtime_repaired_count": 0,
    "schema_mutated_count": 0,
    "move_added_count": 0,
    "fixture_expanded_count": 0,
    "runtime_patched_count": 0,
    "live_hook_installed_count": 0,
    "runtime_adoption_authority_count": 0,
    "c8_authorized_count": 0,
    "proposal_accepted_count": 0,
    "hidden_next_command_count": 0,
    "latest_file_selection_count": 0,
    "mtime_selection_count": 0,
    "ambient_workspace_inference_count": 0,
    "prior_receipt_mutation_count": 0,
}

RECEIPT_NEGATIVE_CONTROLS_ZERO = {
    "implementation_started_count": 0,
    "runtime_repaired_count": 0,
    "schema_mutated_count": 0,
    "move_added_count": 0,
    "fixture_expanded_count": 0,
    "runtime_patched_count": 0,
    "live_hook_installed_count": 0,
    "c8_authorized_count": 0,
    "proposal_accepted_count": 0,
    "hidden_next_command_count": 0,
    "latest_file_selection_count": 0,
    "mtime_selection_count": 0,
    "ambient_workspace_inference_count": 0,
    "prior_receipt_mutation_count": 0,
}

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

def append_trace(rows: List[Dict[str, Any]], adapter_run_id: str, action: str, input_ref: str | None, output_ref: str | None, decision: str | None, stop_code: str | None, boundary_guard: str | None) -> None:
    rows.append({
        "schema_version": "capability_proposal_adapter_trace_step_v0",
        "adapter_run_id": adapter_run_id,
        "step_index": len(rows),
        "action": action,
        "input_ref": input_ref,
        "output_ref": output_ref,
        "decision": decision,
        "stop_code": stop_code,
        "boundary_guard": boundary_guard,
    })

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def safe_choice_strings(raw: Any) -> List[str]:
    out: List[str] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                choice = item.get("choice")
                if choice:
                    out.append(str(choice))
            elif item:
                out.append(str(item))
    return out

def choose_proposal_kind(required_capability: str, missing_objects: List[str], shared_missing_boundary: Any) -> str | None:
    blob = " ".join([required_capability, str(shared_missing_boundary), " ".join(missing_objects)]).lower()
    if "trigger" in blob or "tie" in blob or "loop" in blob:
        return "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL"
    if "evidence" in blob:
        return "BOUNDED_EVIDENCE_SURFACE_CAPABILITY_PROPOSAL"
    if "reference" in blob:
        return "BOUNDED_REFERENCE_SURFACE_CAPABILITY_PROPOSAL"
    if "observability" in blob:
        return "BOUNDED_OBSERVABILITY_SURFACE_CAPABILITY_PROPOSAL"
    if "feedback" in blob:
        return "BOUNDED_FEEDBACK_SURFACE_CAPABILITY_PROPOSAL"
    if "classification" in blob:
        return "BOUNDED_CLASSIFICATION_CAPABILITY_PROPOSAL"
    if "validation" in blob:
        return "BOUNDED_VALIDATION_SURFACE_CAPABILITY_PROPOSAL"
    if "admissibility" in blob:
        return "BOUNDED_ADMISSIBILITY_SURFACE_CAPABILITY_PROPOSAL"
    if "runtime state" in blob or "state" in blob:
        return "BOUNDED_RUNTIME_STATE_SURFACE_CAPABILITY_PROPOSAL"
    if "move registry" in blob or "registry" in blob:
        return "BOUNDED_MOVE_REGISTRY_SURFACE_CAPABILITY_PROPOSAL"
    return None

def deterministic_surface_name(required_capability: str) -> str | None:
    if not required_capability:
        return None
    cleaned = required_capability.strip()
    if not cleaned:
        return None
    if cleaned.endswith("_v0"):
        return cleaned
    return cleaned + "_v0"

def normalize_stop_packet(
    source_receipt: Dict[str, Any],
    source_stop_packet: Dict[str, Any],
    parent_payload: Dict[str, Any],
    missing_diag: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    failures: List[str] = []
    notes: List[str] = []

    summary = source_receipt.get("machine_readable_t6_capability_boundary_surface_audit_summary", {})

    stop_code = source_stop_packet.get("stop_code") or summary.get("stop_code")
    audit_result_kind = summary.get("audit_result_kind") or source_stop_packet.get("audit_result_kind")

    missing_objects = summary.get("missing_objects")
    if not isinstance(missing_objects, list):
        raw_missing = source_stop_packet.get("missing_objects", source_stop_packet.get("missing_object", []))
        if isinstance(raw_missing, list):
            missing_objects = [m for m in raw_missing if m != "bounded_t6_trigger_surface_capability"]
        else:
            missing_objects = []

    shared_missing_boundary = None
    shared = missing_diag.get("shared_missing_boundary", {})
    if isinstance(shared, dict):
        shared_missing_boundary = shared.get("missing_object")
    if not shared_missing_boundary:
        raw_missing = source_stop_packet.get("missing_object", [])
        if isinstance(raw_missing, list):
            for item in raw_missing:
                if item == "bounded_t6_trigger_surface_capability":
                    shared_missing_boundary = item
                    break

    required_capability = source_stop_packet.get("required_capability") or summary.get("required_capability")
    why = source_stop_packet.get("why_current_capability_cannot_proceed")
    safe_human_choices = safe_choice_strings(source_stop_packet.get("safe_next_human_choices")) or safe_choice_strings(parent_payload.get("safe_next_human_choices"))

    boundary_flags = {
        "repair_authorized": bool(summary.get("repair_authorized")),
        "implementation_authorized": False,
        "schema_mutation_authorized": bool(summary.get("schema_archive_mutated")),
        "move_addition_authorized": bool(summary.get("move_addition_authorized")),
        "runtime_patch_authorized": bool(summary.get("runtime_patched")),
        "fixture_expansion_authorized": bool(summary.get("fixture_expanded_by_default")),
        "c8_authorized": bool(summary.get("c8_authorized")),
    }

    candidate_id = "capability_candidate_" + sig8({
        "source_receipt_id": source_receipt.get("receipt_id"),
        "stop_code": stop_code,
        "missing_objects": missing_objects,
        "required_capability": required_capability,
    })

    stop_packet_id = "cap_stop_" + sig8({
        "source_unit_id": source_receipt.get("unit_id"),
        "source_receipt_ref": rel(SOURCE_RECEIPT_PATH),
        "source_stop_packet_ref": rel(SOURCE_STOP_PACKET_PATH),
        "stop_code": stop_code,
        "audit_result_kind": audit_result_kind,
        "missing_objects": missing_objects,
        "shared_missing_boundary": shared_missing_boundary,
        "required_capability": required_capability,
    })

    normalized = {
        "schema_version": "capability_stop_packet_v0",
        "stop_packet_id": stop_packet_id,
        "source_unit_id": source_receipt.get("unit_id"),
        "source_receipt_ref": rel(SOURCE_RECEIPT_PATH),
        "source_case_id": "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT",
        "candidate_id": candidate_id,
        "stop_code": stop_code,
        "audit_result_kind": audit_result_kind,
        "missing_objects": missing_objects,
        "shared_missing_boundary": shared_missing_boundary,
        "required_capability": required_capability,
        "why_current_capability_cannot_proceed": why,
        "within_current_capability": False,
        "authorized": False,
        "safe_human_choices": safe_human_choices,
        "boundary_flags": boundary_flags,
        "source_trace_ref": source_receipt.get("output_artifacts", {}).get("transition_trace"),
        "source_readout_ref": rel(SOURCE_STOP_PACKET_PATH),
        "source_profile_ref": rel(SOURCE_PROFILE_PATH),
        "source_rollup_ref": rel(SOURCE_ROLLUP_PATH),
        "observed_evidence_refs": [
            rel(SOURCE_CURRENT_SURFACE_INVENTORY_PATH),
            rel(SOURCE_MISSING_OBJECT_DIAGNOSIS_PATH),
            rel(SOURCE_CAPABILITY_BOUNDARY_ASSESSMENT_PATH),
        ],
        "failed_relative_to": "runtime registry reachability profile / T6 trigger surface boundary",
        "current_capability_summary": "Current capability can inspect and classify available evidence, but cannot lawfully create, infer, or authorize the missing T6 trigger surface.",
        "forbidden_next_actions": [
            "repair automatically",
            "implement missing capability",
            "mutate schema archive",
            "add move",
            "patch runtime",
            "expand fixtures by default",
            "authorize C8",
        ],
    }

    required_fields = [
        "stop_packet_id",
        "source_unit_id",
        "source_receipt_ref",
        "stop_code",
        "audit_result_kind",
        "missing_objects",
        "shared_missing_boundary",
        "required_capability",
        "why_current_capability_cannot_proceed",
        "within_current_capability",
        "authorized",
        "safe_human_choices",
        "boundary_flags",
        "source_case_id",
        "candidate_id",
    ]

    for field in required_fields:
        value = normalized.get(field)
        if value is None or value == "" or value == []:
            failures.append(f"required_stop_packet_field_missing:{field}")

    if normalized.get("stop_code") not in ALLOWED_STOP_CODES:
        failures.append("stop_code_not_capability_boundary")
    if normalized.get("audit_result_kind") not in ALLOWED_AUDIT_RESULT_KINDS:
        failures.append("audit_result_kind_not_allowed")
    if normalized.get("required_capability") in (None, ""):
        failures.append("required_capability_unnamed")
    if not normalized.get("missing_objects"):
        failures.append("missing_objects_unnamed")
    if any(boundary_flags.values()):
        failures.append("boundary_flags_authority_claim_detected")

    notes.append("Source runtime stop packet normalized into adapter packet using fixed source receipt/path references only.")
    notes.append("No latest, mtime, or ambient workspace selection used.")

    return normalized, failures, notes

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        SOURCE_RECEIPT_PATH,
        SOURCE_STOP_PACKET_PATH,
        SOURCE_PARENT_RETURN_PAYLOAD_PATH,
        SOURCE_MISSING_OBJECT_DIAGNOSIS_PATH,
        SOURCE_CAPABILITY_BOUNDARY_ASSESSMENT_PATH,
        SOURCE_CURRENT_SURFACE_INVENTORY_PATH,
        SOURCE_PROFILE_PATH,
        SOURCE_ROLLUP_PATH,
    ]

    failures: List[str] = []
    source_hashes_before = {}

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")
        else:
            source_hashes_before[rel(p)] = file_sha256(p)

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    source_receipt = read_json(SOURCE_RECEIPT_PATH)
    source_stop_packet = read_json(SOURCE_STOP_PACKET_PATH)
    parent_payload = read_json(SOURCE_PARENT_RETURN_PAYLOAD_PATH)
    missing_diag = read_json(SOURCE_MISSING_OBJECT_DIAGNOSIS_PATH)
    boundary_assessment = read_json(SOURCE_CAPABILITY_BOUNDARY_ASSESSMENT_PATH)
    surface_inventory = read_json(SOURCE_CURRENT_SURFACE_INVENTORY_PATH)
    source_profile = read_json(SOURCE_PROFILE_PATH)
    source_rollup = read_json(SOURCE_ROLLUP_PATH)

    source_summary = source_receipt.get("machine_readable_t6_capability_boundary_surface_audit_summary", {})

    if source_receipt.get("receipt_id") != SOURCE_T6_SURFACE_AUDIT_RECEIPT_ID:
        failures.append(f"source_receipt_id_wrong:{source_receipt.get('receipt_id')}")
    if source_receipt.get("gate") != "PASS":
        failures.append("source_receipt_gate_not_pass")
    if source_receipt.get("terminal", {}).get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("source_terminal_not_capability_layer_required")
    if source_summary.get("audit_result_kind") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("source_audit_result_kind_wrong")
    if source_summary.get("capability_stop_packet_emitted") is not True:
        failures.append("source_capability_stop_packet_not_emitted")
    if source_summary.get("bounded_proposition_emitted") is not False:
        failures.append("source_already_emitted_bounded_proposition")
    if source_summary.get("required_capability") != "bounded_structured_t6_trigger_surface_capability":
        failures.append("source_required_capability_wrong")

    for key in [
        "ready_for_live_runtime_adoption",
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "repair_authorized",
        "move_addition_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(source_summary, key, failures)

    normalized_packet, normalize_failures, normalize_notes = normalize_stop_packet(
        source_receipt,
        source_stop_packet,
        parent_payload,
        missing_diag,
    )
    failures.extend(normalize_failures)

    proposal_kind = choose_proposal_kind(
        str(normalized_packet.get("required_capability") or ""),
        normalized_packet.get("missing_objects") or [],
        normalized_packet.get("shared_missing_boundary"),
    )

    proposed_surface = deterministic_surface_name(str(normalized_packet.get("required_capability") or ""))

    pressure_class = "NO_PROPOSAL_PRESSURE"
    outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_PASS_CANDIDATE_EMITTED"
    terminal_stop_code = "STOP_CAPABILITY_PROPOSAL_CANDIDATE_EMITTED"

    if normalized_packet.get("stop_code") not in ALLOWED_STOP_CODES:
        pressure_class = "NOT_CAPABILITY_BOUNDARY_PACKET"
        outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_NOT_CAPABILITY_BOUNDARY"
        terminal_stop_code = "STOP_NOT_CAPABILITY_BOUNDARY_PACKET"
    elif normalize_failures:
        if any("required_capability" in f or "required_capability_unnamed" in f for f in normalize_failures):
            pressure_class = "REQUIRED_CAPABILITY_UNNAMED"
            outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_REQUIRED_CAPABILITY_UNNAMED"
            terminal_stop_code = "STOP_REQUIRED_CAPABILITY_UNNAMED"
        elif any("missing_objects" in f for f in normalize_failures):
            pressure_class = "MISSING_OBJECTS_UNNAMED"
            outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_MISSING_OBJECTS_UNNAMED"
            terminal_stop_code = "STOP_MISSING_OBJECTS_UNNAMED"
        else:
            pressure_class = "CAPABILITY_STOP_PACKET_UNDER_SPECIFIED"
            outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_UNDER_SPECIFIED_STOP_PACKET"
            terminal_stop_code = "STOP_CAPABILITY_STOP_PACKET_UNDER_SPECIFIED"
    elif proposal_kind is None:
        pressure_class = "CAPABILITY_PROPOSAL_KIND_UNRESOLVED"
        outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_PROPOSAL_KIND_UNRESOLVED"
        terminal_stop_code = "STOP_CAPABILITY_PROPOSAL_KIND_UNRESOLVED"
        failures.append("proposal_kind_unresolved")
    elif proposal_kind not in PROPOSAL_KIND_ENUM:
        pressure_class = "CAPABILITY_PROPOSAL_KIND_UNRESOLVED"
        outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_PROPOSAL_KIND_UNRESOLVED"
        terminal_stop_code = "STOP_CAPABILITY_PROPOSAL_KIND_UNRESOLVED"
        failures.append("proposal_kind_not_in_enum")
    elif proposed_surface is None:
        pressure_class = "PROPOSED_SURFACE_NAME_UNRESOLVED"
        outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_SURFACE_NAME_UNRESOLVED"
        terminal_stop_code = "STOP_PROPOSED_SURFACE_NAME_UNRESOLVED"
        failures.append("proposed_surface_name_unresolved")

    gate = "PASS" if not failures else "FAIL"

    adapter_run_id = "capability_adapter_" + sig8({
        "unit_id": UNIT_ID,
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "source_receipt_id": source_receipt.get("receipt_id"),
        "proposal_kind": proposal_kind,
        "proposed_surface": proposed_surface,
    })

    trace_rows: List[Dict[str, Any]] = []
    append_trace(trace_rows, adapter_run_id, "LOAD_SOURCE_STOP_PACKET", rel(SOURCE_STOP_PACKET_PATH), rel(INTAKE_REVIEW_PATH), "fixed source path consumed", None, "no latest/mtime")
    append_trace(trace_rows, adapter_run_id, "VALIDATE_STOP_PACKET_SHAPE", rel(INTAKE_REVIEW_PATH), rel(NORMALIZED_STOP_PACKET_PATH), "required fields present" if gate == "PASS" else "typed block", terminal_stop_code if gate != "PASS" else None, "no field invention from ambient context")
    append_trace(trace_rows, adapter_run_id, "VERIFY_CAPABILITY_BOUNDARY_STOP", rel(NORMALIZED_STOP_PACKET_PATH), None, "capability boundary stop verified" if normalized_packet.get("stop_code") in ALLOWED_STOP_CODES else "not capability boundary", None if normalized_packet.get("stop_code") in ALLOWED_STOP_CODES else "STOP_NOT_CAPABILITY_BOUNDARY_PACKET", "source stop code fixed")
    append_trace(trace_rows, adapter_run_id, "EXTRACT_MISSING_OBJECTS", rel(NORMALIZED_STOP_PACKET_PATH), None, ",".join(normalized_packet.get("missing_objects", [])), None, "missing objects preserved")
    append_trace(trace_rows, adapter_run_id, "EXTRACT_REQUIRED_CAPABILITY", rel(NORMALIZED_STOP_PACKET_PATH), None, str(normalized_packet.get("required_capability")), None, "required capability preserved")
    append_trace(trace_rows, adapter_run_id, "EXTRACT_BOUNDARY_FLAGS", rel(NORMALIZED_STOP_PACKET_PATH), None, "all authority flags false", None, "boundary flags preserved")
    append_trace(trace_rows, adapter_run_id, "CHECK_PROPOSAL_FORMATION_AUTHORITY", rel(NORMALIZED_STOP_PACKET_PATH), None, "proposal candidate only; no implementation authority", None, "no authorization")
    append_trace(trace_rows, adapter_run_id, "FORM_BOUNDED_PROPOSAL_CANDIDATE", rel(NORMALIZED_STOP_PACKET_PATH), rel(PROPOSAL_PATH), proposal_kind if gate == "PASS" else "not emitted", terminal_stop_code if gate != "PASS" else None, "scope narrow/source-bound")
    append_trace(trace_rows, adapter_run_id, "EMIT_HUMAN_DECISION_PACKET", rel(PROPOSAL_PATH) if gate == "PASS" else None, rel(HUMAN_DECISION_PACKET_PATH), "decision required; default defer" if gate == "PASS" else "not emitted", None if gate == "PASS" else terminal_stop_code, "proposal not accepted")
    append_trace(trace_rows, adapter_run_id, "EMIT_ADAPTER_RECEIPT", rel(PROPOSAL_PATH) if gate == "PASS" else None, None, "receipt pending id", None, "negative controls zero")

    proposal_id = "capability_proposal_" + sig8({
        "adapter_run_id": adapter_run_id,
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "proposal_kind": proposal_kind,
        "proposed_surface": proposed_surface,
        "missing_objects": normalized_packet.get("missing_objects"),
        "required_capability": normalized_packet.get("required_capability"),
    })

    human_decision_options = [
        "accept proposal for bounded implementation",
        "reject proposal",
        "edit proposal and resubmit",
        "defer proposal",
        "freeze proposal as reference only",
        "request narrower proposal",
        "request alternate proposal",
        "close source branch for current registry only",
    ]

    proposal = {
        "schema_version": "bounded_capability_proposal_v0",
        "proposal_id": proposal_id if gate == "PASS" else None,
        "proposal_kind": proposal_kind if gate == "PASS" else None,
        "proposal_status": "PROPOSAL_CANDIDATE_ONLY" if gate == "PASS" else "NOT_EMITTED",
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "source_unit_id": normalized_packet.get("source_unit_id"),
        "source_receipt_ref": normalized_packet.get("source_receipt_ref"),
        "source_case_id": normalized_packet.get("source_case_id"),
        "candidate_id": normalized_packet.get("candidate_id"),
        "required_capability": normalized_packet.get("required_capability"),
        "missing_objects_addressed": normalized_packet.get("missing_objects", []),
        "shared_missing_boundary": normalized_packet.get("shared_missing_boundary"),
        "proposed_surface": proposed_surface if gate == "PASS" else None,
        "purpose": "Expose structured evidence for T6 loop-trigger and move-tie conditions without inferring triggers from weak text/noise evidence.",
        "scope": [
            "create a bounded structured T6 trigger evidence surface",
            "define minimal input fields for loop and move-tie trigger inspection",
            "define minimal output fields distinguishing trigger present, trigger absent, and trigger under-specified",
            "define acceptance receipt shape proving missing-object distinction is preserved",
            "define one demo/audit case for current registry replay",
            "define negative controls for no runtime repair, no move addition, and no fixture expansion by default",
            "define human review path before implementation",
        ],
        "non_goals": [
            "does not implement the capability",
            "does not repair the source unit",
            "does not add runtime moves",
            "does not mutate schema archive",
            "does not expand fixtures by default",
            "does not patch runtime",
            "does not authorize runtime adoption",
            "does not authorize C8",
            "does not create live control authority",
            "does not add loop handling",
            "does not add tie-breaking policy",
            "does not make T6 pass directly",
        ],
        "required_receipts": [
            "capability design receipt",
            "capability build receipt",
            "capability review receipt",
            "capability closure receipt if frozen as reference",
            "negative-control receipt",
            "acceptance-gate receipt",
            "source-stop linkage receipt",
            "demo-case receipt",
            "audit receipt",
            "validator receipt",
            "human decision receipt",
        ],
        "acceptance_conditions": [
            "future T6 audit can distinguish loop trigger present, loop trigger absent, and loop trigger under-specified",
            "future T6 audit can distinguish structured move-tie evidence from text-only detector noise",
            "missing object loop_trigger_surface_missing becomes explicitly representable",
            "missing object structured_tie_evidence_missing becomes explicitly representable",
            "source stop can be re-run and produce a more specific terminal without inventing a trigger",
            "new evidence surface emits required fields for trigger presence, trigger absence, and under-specification",
            "receipt proves no authority widening",
            "negative controls remain zero",
        ],
        "boundary_guards": {
            "implementation_authorized": False,
            "runtime_patch_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "c8_authorized": False,
        },
        "human_decision_options": human_decision_options,
        "validator_requirements": [
            "proposal is well formed",
            "proposal is typed",
            "proposal cites source stop packet",
            "proposal preserves missing-object distinction",
            "proposal avoids unauthorized repair",
            "proposal declares scope and non-goals",
            "proposal exposes human decision options",
            "proposal preserves boundary flags",
        ],
        "must_not_infer": [
            "proposal accepted",
            "implementation authorized",
            "runtime repair authorized",
            "schema mutation authorized",
            "move addition authorized",
            "runtime adoption authorized",
            "C8 authorized",
        ],
    }

    human_decision_packet = {
        "schema_version": "human_capability_decision_packet_v0",
        "proposal_id": proposal_id if gate == "PASS" else None,
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "decision_required": gate == "PASS",
        "available_decisions": [
            "ACCEPT_FOR_BOUNDED_IMPLEMENTATION",
            "REJECT",
            "EDIT_AND_RESUBMIT",
            "DEFER",
            "FREEZE_AS_REFERENCE_ONLY",
            "REQUEST_NARROWER_PROPOSAL",
            "REQUEST_ALTERNATE_PROPOSAL",
            "CLOSE_SOURCE_BRANCH_FOR_CURRENT_REGISTRY_ONLY",
        ],
        "default_decision": "DEFER",
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "c8_authorized": False,
    }

    intake_review = {
        "schema_version": "capability_stop_packet_intake_review_v0",
        "adapter_run_id": adapter_run_id,
        "source_stop_packet_ref": rel(SOURCE_STOP_PACKET_PATH),
        "source_receipt_ref": rel(SOURCE_RECEIPT_PATH),
        "source_fixed_by_explicit_path": True,
        "latest_file_selection_used": False,
        "mtime_selection_used": False,
        "ambient_workspace_inference_used": False,
        "source_stop_packet_consumed": True,
        "normalized_stop_packet_ref": rel(NORMALIZED_STOP_PACKET_PATH),
        "normalized_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "intake_notes": normalize_notes,
        "intake_failures": normalize_failures,
        "stop_code": normalized_packet.get("stop_code"),
        "audit_result_kind": normalized_packet.get("audit_result_kind"),
        "required_capability": normalized_packet.get("required_capability"),
        "missing_objects": normalized_packet.get("missing_objects"),
        "boundary_flags": normalized_packet.get("boundary_flags"),
        "packet_is_capability_boundary": normalized_packet.get("stop_code") in ALLOWED_STOP_CODES,
        "proposal_formation_lawful": gate == "PASS",
    }

    readout = {
        "schema_version": "capability_proposal_adapter_readout_v0",
        "adapter_run_id": adapter_run_id,
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "stop_code": normalized_packet.get("stop_code"),
        "required_capability": normalized_packet.get("required_capability"),
        "missing_objects": normalized_packet.get("missing_objects", []),
        "proposal_emitted": gate == "PASS",
        "proposal_id": proposal_id if gate == "PASS" else None,
        "proposal_kind": proposal_kind if gate == "PASS" else None,
        "proposed_surface": proposed_surface if gate == "PASS" else None,
        "human_decision_required": gate == "PASS",
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop_code,
            "next_command_goal": None,
        },
        "interpretation": "Typed capability-boundary stop was converted into a bounded proposal candidate. This does not authorize implementation." if gate == "PASS" else "Capability proposal adapter stopped typed before emitting a proposal candidate.",
    }

    rollup = {
        "schema_version": "capability_proposal_adapter_rollup_v0",
        "runs": 1,
        "source_stop_packet_consumed": True,
        "proposal_emitted": gate == "PASS",
        "human_decision_packet_emitted": gate == "PASS",
        "missing_objects_count": len(normalized_packet.get("missing_objects", [])),
        "required_capability_named": bool(normalized_packet.get("required_capability")),
        "proposal_kind": proposal_kind if gate == "PASS" else None,
        "proposed_surface": proposed_surface if gate == "PASS" else None,
        "outcome_class": outcome_class,
        "pressure_class": pressure_class,
        "negative_controls": NEGATIVE_CONTROLS_ZERO,
    }

    profile = {
        "schema_version": "capability_proposal_adapter_profile_v0",
        "profile_id": adapter_run_id,
        "status": "CAPABILITY_PROPOSAL_ADAPTER_PASS" if gate == "PASS" else "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED",
        "core_rule": "Convert typed capability-boundary stops into bounded proposal candidates without authorizing implementation.",
        "source_stop_packet_ref": rel(NORMALIZED_STOP_PACKET_PATH),
        "proposal_ref": rel(PROPOSAL_PATH) if gate == "PASS" else None,
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH) if gate == "PASS" else None,
        "outcome_class": outcome_class,
        "pressure_class": pressure_class,
        "bad_counters_zero": True,
        "must_not_infer": [
            "proposal accepted",
            "capability implementation authorized",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "capability_proposal_adapter_report_v0",
        "adapter_run_id": adapter_run_id,
        "unit_id": UNIT_ID,
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "source_receipt_ref": rel(SOURCE_RECEIPT_PATH),
        "result": "BOUNDED_CAPABILITY_PROPOSAL_CANDIDATE_EMITTED" if gate == "PASS" else "TYPED_STOP",
        "proposal_id": proposal_id if gate == "PASS" else None,
        "proposal_kind": proposal_kind if gate == "PASS" else None,
        "proposed_surface": proposed_surface if gate == "PASS" else None,
        "human_decision_required": gate == "PASS",
        "default_human_decision": "DEFER" if gate == "PASS" else None,
        "summary": {
            "source_stop": "STOP_CAPABILITY_LAYER_REQUIRED",
            "source_missing_objects": normalized_packet.get("missing_objects", []),
            "source_required_capability": normalized_packet.get("required_capability"),
            "adapter_action": "converted stop packet into reviewable bounded proposal candidate" if gate == "PASS" else "blocked before proposal emission",
            "implementation_authorized": False,
            "proposal_accepted": False,
        },
    }

    transition_trace = {
        "schema_version": "capability_proposal_adapter_transition_trace_v0",
        "adapter_run_id": adapter_run_id,
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "STOP_CAPABILITY_LAYER_REQUIRED",
                "edge": "consume fixed structured capability-stop packet",
                "to": "CAPABILITY_STOP_PACKET_VALIDATED" if gate == "PASS" else "CAPABILITY_PROPOSAL_ADAPTER_TYPED_STOP",
            },
            {
                "from": "CAPABILITY_STOP_PACKET_VALIDATED" if gate == "PASS" else "CAPABILITY_PROPOSAL_ADAPTER_TYPED_STOP",
                "edge": "map missing objects and required capability to proposal candidate",
                "to": "BOUNDED_CAPABILITY_PROPOSAL_CANDIDATE_EMITTED" if gate == "PASS" else "STOP_TYPED",
            },
            {
                "from": "BOUNDED_CAPABILITY_PROPOSAL_CANDIDATE_EMITTED" if gate == "PASS" else "STOP_TYPED",
                "edge": "emit human decision packet without acceptance",
                "to": "STOP_REVIEW_READY" if gate == "PASS" else "STOP_TYPED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop_code,
            "next_command_goal": None,
        },
    }

    for path, obj in [
        (INTAKE_REVIEW_PATH, intake_review),
        (NORMALIZED_STOP_PACKET_PATH, normalized_packet),
        (PROPOSAL_PATH, proposal),
        (HUMAN_DECISION_PACKET_PATH, human_decision_packet),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)
    write_jsonl(TRACE_PATH, trace_rows)

    # Trace reconstruction guard.
    trace_text = TRACE_PATH.read_text()
    if gate == "PASS":
        required_trace_terms = [
            "LOAD_SOURCE_STOP_PACKET",
            "VALIDATE_STOP_PACKET_SHAPE",
            "VERIFY_CAPABILITY_BOUNDARY_STOP",
            "EXTRACT_MISSING_OBJECTS",
            "EXTRACT_REQUIRED_CAPABILITY",
            "FORM_BOUNDED_PROPOSAL_CANDIDATE",
            "EMIT_HUMAN_DECISION_PACKET",
            "EMIT_ADAPTER_RECEIPT",
        ]
        missing_trace_terms = [t for t in required_trace_terms if t not in trace_text]
        if missing_trace_terms:
            gate = "FAIL"
            pressure_class = "CAPABILITY_PROPOSAL_TRACE_MISMATCH"
            outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_BLOCKED_TRACE_MISMATCH"
            terminal_stop_code = "STOP_CAPABILITY_PROPOSAL_TRACE_MISMATCH"
            failures.extend([f"trace_term_missing:{t}" for t in missing_trace_terms])

    source_hashes_after = {rel(p): file_sha256(p) for p in required_files}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        pressure_class = "CAPABILITY_PROPOSAL_AUTHORITY_VIOLATION"
        outcome_class = "CAPABILITY_PROPOSAL_ADAPTER_AUTHORITY_VIOLATION"
        terminal_stop_code = "STOP_CAPABILITY_PROPOSAL_AUTHORITY_VIOLATION"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "SOURCE_STOP_PACKET_CONSUMED",
        "SOURCE_STOP_PACKET_FIXED_REF",
        "STOP_CODE_CAPABILITY_BOUNDARY",
        "REQUIRED_FIELDS_PRESENT",
        "MISSING_OBJECTS_PRESERVED",
        "REQUIRED_CAPABILITY_PRESERVED",
        "BOUNDARY_FLAGS_PRESERVED",
        "PROPOSAL_KIND_SELECTED_FROM_ENUM",
        "PROPOSED_SURFACE_NAMED_DETERMINISTICALLY",
        "SCOPE_DECLARED",
        "NON_GOALS_DECLARED",
        "REQUIRED_RECEIPTS_DECLARED",
        "ACCEPTANCE_CONDITIONS_DECLARED",
        "HUMAN_DECISION_OPTIONS_DECLARED",
        "PROPOSAL_CANDIDATE_ONLY",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "TRACE_EMITTED",
        "RECEIPT_EMITTED",
        "READOUT_EMITTED",
        "NEGATIVE_CONTROLS_ZERO",
        "NO_HIDDEN_NEXT_COMMAND",
        "NO_LATEST_OR_MTIME_SELECTION",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "capability_proposal_adapter_receipt_v0",
        "receipt_type": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_RECEIPT",
        "created_at": now_iso(),
        "receipt_id": None,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "adapter_run_id": adapter_run_id,
        "layer": "PROPOSAL / CAPABILITY_BOUNDARY",
        "mode": "CONVERT_STOP_PACKET_TO_PROPOSAL_CANDIDATE",
        "build_mode": "CAPABILITY_PROPOSAL_ADAPTER_ONLY",
        "gate": gate,
        "status": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_PASS_CANDIDATE_EMITTED" if gate == "PASS" else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_BLOCKED",
        "failures": failures,
        "warnings": [],
        "source_stop_packet_ref": rel(NORMALIZED_STOP_PACKET_PATH),
        "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
        "source_unit_id": normalized_packet.get("source_unit_id"),
        "source_receipt_ref": normalized_packet.get("source_receipt_ref"),
        "proposal_ref": rel(PROPOSAL_PATH) if gate == "PASS" else None,
        "proposal_id": proposal_id if gate == "PASS" else None,
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH) if gate == "PASS" else None,
        "trace_ref": rel(TRACE_PATH),
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop_code,
            "next_command_goal": None,
        },
        "proposal_status": "PROPOSAL_CANDIDATE_ONLY" if gate == "PASS" else "NOT_EMITTED",
        "validation_status": "NOT_VALIDATED_BY_ADAPTER",
        "pressure_class": pressure_class,
        "outcome_class": outcome_class,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "c8_authorized": False,
        "acceptance_gate_results": {
            "CAPABILITY_ADAPTER_0_SOURCE_STOP_PACKET_CONSUMED": gate == "PASS",
            "CAPABILITY_ADAPTER_1_SOURCE_STOP_PACKET_FIXED_REF": gate == "PASS",
            "CAPABILITY_ADAPTER_2_STOP_CODE_CAPABILITY_BOUNDARY": normalized_packet.get("stop_code") in ALLOWED_STOP_CODES,
            "CAPABILITY_ADAPTER_3_REQUIRED_FIELDS_PRESENT": gate == "PASS",
            "CAPABILITY_ADAPTER_4_MISSING_OBJECTS_PRESERVED": gate == "PASS",
            "CAPABILITY_ADAPTER_5_REQUIRED_CAPABILITY_PRESERVED": gate == "PASS",
            "CAPABILITY_ADAPTER_6_BOUNDARY_FLAGS_PRESERVED": gate == "PASS",
            "CAPABILITY_ADAPTER_7_PROPOSAL_KIND_SELECTED_FROM_ENUM": gate == "PASS",
            "CAPABILITY_ADAPTER_8_PROPOSED_SURFACE_NAMED_DETERMINISTICALLY": gate == "PASS",
            "CAPABILITY_ADAPTER_9_SCOPE_DECLARED": gate == "PASS",
            "CAPABILITY_ADAPTER_10_NON_GOALS_DECLARED": gate == "PASS",
            "CAPABILITY_ADAPTER_11_REQUIRED_RECEIPTS_DECLARED": gate == "PASS",
            "CAPABILITY_ADAPTER_12_ACCEPTANCE_CONDITIONS_DECLARED": gate == "PASS",
            "CAPABILITY_ADAPTER_13_HUMAN_DECISION_OPTIONS_DECLARED": gate == "PASS",
            "CAPABILITY_ADAPTER_14_PROPOSAL_CANDIDATE_ONLY": gate == "PASS",
            "CAPABILITY_ADAPTER_15_NO_IMPLEMENTATION": gate == "PASS",
            "CAPABILITY_ADAPTER_16_NO_RUNTIME_REPAIR": gate == "PASS",
            "CAPABILITY_ADAPTER_17_NO_SCHEMA_MUTATION": gate == "PASS",
            "CAPABILITY_ADAPTER_18_NO_MOVE_ADDITION": gate == "PASS",
            "CAPABILITY_ADAPTER_19_NO_FIXTURE_EXPANSION_BY_DEFAULT": gate == "PASS",
            "CAPABILITY_ADAPTER_20_NO_RUNTIME_PATCH": gate == "PASS",
            "CAPABILITY_ADAPTER_21_NO_LIVE_HOOK_INSTALL": gate == "PASS",
            "CAPABILITY_ADAPTER_22_NO_RUNTIME_ADOPTION_AUTHORITY": gate == "PASS",
            "CAPABILITY_ADAPTER_23_NO_C8_AUTHORIZATION": gate == "PASS",
            "CAPABILITY_ADAPTER_24_TRACE_EMITTED": TRACE_PATH.exists(),
            "CAPABILITY_ADAPTER_25_RECEIPT_EMITTED": True,
            "CAPABILITY_ADAPTER_26_READOUT_EMITTED": READOUT_PATH.exists(),
            "CAPABILITY_ADAPTER_27_NEGATIVE_CONTROLS_ZERO": gate == "PASS",
            "CAPABILITY_ADAPTER_28_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
            "CAPABILITY_ADAPTER_29_NO_LATEST_OR_MTIME_SELECTION": gate == "PASS",
        },
        "machine_readable_capability_proposal_adapter_summary": {
            "status": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_PASS_CANDIDATE_EMITTED" if gate == "PASS" else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_BLOCKED",
            "adapter_run_id": adapter_run_id,
            "source_stop_packet_id": normalized_packet.get("stop_packet_id"),
            "source_receipt_ref": normalized_packet.get("source_receipt_ref"),
            "stop_code": normalized_packet.get("stop_code"),
            "audit_result_kind": normalized_packet.get("audit_result_kind"),
            "required_capability": normalized_packet.get("required_capability"),
            "missing_objects": normalized_packet.get("missing_objects", []),
            "shared_missing_boundary": normalized_packet.get("shared_missing_boundary"),
            "proposal_emitted": gate == "PASS",
            "proposal_id": proposal_id if gate == "PASS" else None,
            "proposal_kind": proposal_kind if gate == "PASS" else None,
            "proposed_surface": proposed_surface if gate == "PASS" else None,
            "human_decision_packet_emitted": gate == "PASS",
            "human_decision_required": gate == "PASS",
            "default_human_decision": "DEFER" if gate == "PASS" else None,
            "proposal_status": "PROPOSAL_CANDIDATE_ONLY" if gate == "PASS" else "NOT_EMITTED",
            "validation_status": "NOT_VALIDATED_BY_ADAPTER",
            "pressure_class": pressure_class,
            "outcome_class": outcome_class,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "live_hook_installed": False,
            "proposal_accepted": False,
            "hidden_next_command": False,
            "latest_file_selection_used": False,
            "mtime_selection_used": False,
            "ambient_workspace_inference_used": False,
            "prior_receipt_mutation": False,
            "c8_authorized": False,
            "next_command_goal": None,
            "reason_codes": reason_codes,
        },
        "negative_controls": RECEIPT_NEGATIVE_CONTROLS_ZERO,
        "output_artifacts": {
            "intake_review": rel(INTAKE_REVIEW_PATH),
            "normalized_stop_packet": rel(NORMALIZED_STOP_PACKET_PATH),
            "bounded_capability_proposal": rel(PROPOSAL_PATH) if gate == "PASS" else None,
            "human_capability_decision_packet": rel(HUMAN_DECISION_PACKET_PATH) if gate == "PASS" else None,
            "trace": rel(TRACE_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
    }

    receipt_id = "capability_adapter_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"capability_proposal_adapter_receipt_id={receipt_id}")
    print(f"capability_proposal_adapter_receipt_path={rel(receipt_path)}")
    print(f"capability_proposal_adapter_proposal_id={proposal_id if gate == 'PASS' else 'NONE'}")
    print(f"capability_proposal_adapter_next_command_goal=NONE")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
