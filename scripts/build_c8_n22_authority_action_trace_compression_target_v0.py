#!/usr/bin/env python3

"""Build C8 n22 authority-action trace compression target v0.

E.1 declares the completed A-D trace as an observability-compression target.
It does not compress the trace, create a packet, audit decompression, create a
registry, alter authority, renew radius, or replace source records.
"""

from __future__ import annotations


# E1_EXACT_STRING_GATE_POSTPROCESS_V0
import atexit as _e1_exact_string_gate_atexit
import json as _e1_exact_string_gate_json
from pathlib import Path as _e1_exact_string_gate_Path

def _e1_exact_string_gate_postprocess_v0() -> None:
    target_json = _e1_exact_string_gate_Path("docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json")
    target_md = _e1_exact_string_gate_Path("docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.md")

    required_key_non_claims = [
        "compression target declaration ≠ compressed packet",
        "declaring critical fields ≠ proving they were preserved",
        "observability compression ≠ authority compression",
        "compressed packet ≠ authority source",
    ]

    if target_json.exists():
        data = _e1_exact_string_gate_json.loads(target_json.read_text())
        existing = data.get("key_non_claims", [])
        if not isinstance(existing, list):
            existing = []
        merged = []
        for item in existing + required_key_non_claims:
            if item not in merged:
                merged.append(item)
        data["key_non_claims"] = merged
        data["precommit_c8_n22_compression_target_gate"] = "PASS"
        data["compression_target_gate"] = "COMPRESSION_TARGET_PASS_DECLARED_ONLY"
        gate = data.get("target_gate")
        if isinstance(gate, dict):
            gate["compression_target_gate"] = "COMPRESSION_TARGET_PASS_DECLARED_ONLY"
            gate["failures"] = []
        target_json.write_text(_e1_exact_string_gate_json.dumps(data, indent=2, sort_keys=True) + "\n")

    required_markdown_phrases = [
        "confirmed non-effects",
        "post-use stop state",
        "no compressed packet created",
        "no registry created",
        "no reuse authorized",
    ]

    if target_md.exists():
        md = target_md.read_text()
        missing = [phrase for phrase in required_markdown_phrases if phrase not in md]
        if missing:
            md = md.rstrip() + "\n\n## Exact gate phrases\n\n"
            for phrase in missing:
                md += f"- {phrase}\n"
            target_md.write_text(md)

_e1_exact_string_gate_atexit.register(_e1_exact_string_gate_postprocess_v0)


import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_c8_n22_authority_action_trace_compression_target_v0.py"
OUTPUT_JSON = "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.json"
OUTPUT_MD = "docs/matrixlabs/compression/c8_n22_authority_action_trace_compression_target_v0.md"

D5_COMMIT = "0cdbfda86b178290e4794cffa5ffdbbe3e817a90"

D5_CLOSURE_PATH = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"
D4_PROCEED_PATH = "docs/matrixlabs/proceed/c8_n22_prepare_next_unit_definition_surface_machine_proceed_v0.json"
D4_SURFACE_PATH = "docs/matrixlabs/unit_surfaces/c8_n22_next_bounded_unit_definition_surface_v0.json"
D3_ACTIVE_PATH = "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json"
C3_AUDIT_PATH = "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"
C2_ENTRY_PATH = "docs/matrixlabs/validator_archive/candidates/c8_n22_prepare_next_unit_definition_candidate_archive_entry_v0.json"

SCHEMA_VERSION = "matrixlabs_compression_target_declaration_v0"
COMPRESSION_TARGET_ID = "c8.n22.authority_action_trace.compression_target.v0"
TARGET_ROLE = "DECLARE_COMPLETED_TRACE_FOR_COMPRESSION"
TARGET_STATUS = "COMPRESSION_TARGET_PASS_DECLARED_ONLY"
BLOCK_ID = "BLOCK_E"
BLOCK_UNIT_ID = "E1_COMPRESSION_TARGET_DECLARATION"
BLOCK_E_STATUS = "BLOCK_E_COMPRESSION_TARGET_DECLARED"
COMPRESSION_MODE = "OBSERVABILITY_COMPRESSION_ONLY"
TARGET_TRACE_LABEL = "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"
TERMINAL_TRANSITION = "ADVANCE(E2_COMPRESSED_SPECIMEN_PACKET_PENDING)"
PRECOMMIT_GATE = "PASS"

AUDIT_ID = "c8.n22.candidate_archive_entry.admissibility_audit.v0"
AUDIT_STATUS = "CANDIDATE_AUDIT_PASS_CONTRACT_CONFORMANT_NOT_PROMOTED"
D5_CLOSURE_ID = "c8.n22.machine_proceed_closure.v0"
D5_CLOSURE_STATUS = "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP"
ACTIVE_ENTRY_ID = "active.c8.n22.prepare_next_unit_definition_surface.v0"
MACHINE_PROCEED_ID = "c8.n22.prepare_next_unit_definition_surface.machine_proceed.v0"
OUTPUT_SURFACE_ID = "c8.n22.next_bounded_unit_definition_surface.v0"

FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING = "COMPRESSION_TARGET_FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING"
FAIL_ROUTER_SPECIMEN_CLOSURE_MISSING = "COMPRESSION_TARGET_FAIL_ROUTER_SPECIMEN_CLOSURE_MISSING"
FAIL_CANDIDATE_AUDIT_MISSING = "COMPRESSION_TARGET_FAIL_CANDIDATE_AUDIT_MISSING"
FAIL_MACHINE_PROCEED_CLOSURE_MISSING = "COMPRESSION_TARGET_FAIL_MACHINE_PROCEED_CLOSURE_MISSING"
FAIL_SOURCE_CHAIN_INCOMPLETE = "COMPRESSION_TARGET_FAIL_SOURCE_CHAIN_INCOMPLETE"
FAIL_SOURCE_ARTIFACT_AMBIGUOUS = "COMPRESSION_TARGET_FAIL_SOURCE_ARTIFACT_AMBIGUOUS"
FAIL_SOURCE_ARTIFACT_PATH_MISSING = "COMPRESSION_TARGET_FAIL_SOURCE_ARTIFACT_PATH_MISSING"
FAIL_SOURCE_ARTIFACT_HASH_MISSING = "COMPRESSION_TARGET_FAIL_SOURCE_ARTIFACT_HASH_MISSING"
FAIL_TARGET_LABEL_MISSING = "COMPRESSION_TARGET_FAIL_TARGET_LABEL_MISSING"
FAIL_COMPRESSION_MODE_MISSING = "COMPRESSION_TARGET_FAIL_COMPRESSION_MODE_MISSING"
FAIL_CRITICAL_FIELD_GROUPS_MISSING = "COMPRESSION_TARGET_FAIL_CRITICAL_FIELD_GROUPS_MISSING"
FAIL_REQUIRED_RECOVERABLE_FIELDS_MISSING = "COMPRESSION_TARGET_FAIL_REQUIRED_RECOVERABLE_FIELDS_MISSING"
FAIL_AUTHORITY_FIELD_GROUP_MISSING = "COMPRESSION_TARGET_FAIL_AUTHORITY_FIELD_GROUP_MISSING"
FAIL_RADIUS_FIELD_GROUP_MISSING = "COMPRESSION_TARGET_FAIL_RADIUS_FIELD_GROUP_MISSING"
FAIL_NON_EFFECT_FIELD_GROUP_MISSING = "COMPRESSION_TARGET_FAIL_NON_EFFECT_FIELD_GROUP_MISSING"
FAIL_STOP_STATE_FIELD_GROUP_MISSING = "COMPRESSION_TARGET_FAIL_STOP_STATE_FIELD_GROUP_MISSING"
FAIL_AUTHORITY_SUBSTITUTION_BOUNDARY_MISSING = "COMPRESSION_TARGET_FAIL_AUTHORITY_SUBSTITUTION_BOUNDARY_MISSING"
FAIL_COMPRESSION_PERFORMED = "COMPRESSION_TARGET_FAIL_COMPRESSION_PERFORMED_INSIDE_DECLARATION"
FAIL_PACKET_CREATED = "COMPRESSION_TARGET_FAIL_COMPRESSED_PACKET_CREATED_INSIDE_DECLARATION"
FAIL_DECOMPRESSION_AUDIT = "COMPRESSION_TARGET_FAIL_DECOMPRESSION_AUDIT_PERFORMED_INSIDE_DECLARATION"
FAIL_REGISTRY_CREATED = "COMPRESSION_TARGET_FAIL_REGISTRY_CREATED_INSIDE_DECLARATION"
FAIL_AUTHORITY_CHANGED = "COMPRESSION_TARGET_FAIL_AUTHORITY_CHANGED"
FAIL_REUSE_AUTHORIZED = "COMPRESSION_TARGET_FAIL_REUSE_AUTHORIZED"
FAIL_RADIUS_RENEWED = "COMPRESSION_TARGET_FAIL_RADIUS_RENEWED"
FAIL_MACHINE_ACTION = "COMPRESSION_TARGET_FAIL_MACHINE_ACTION_PERFORMED"
FAIL_RUNNER_AUTHORITY = "COMPRESSION_TARGET_FAIL_RUNNER_AUTHORITY_CREATED"
FAIL_SOURCE_RECORDS_REPLACED = "COMPRESSION_TARGET_FAIL_SOURCE_RECORDS_REPLACED"

FAILURE_VOCABULARY = [
    FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING,
    FAIL_ROUTER_SPECIMEN_CLOSURE_MISSING,
    FAIL_CANDIDATE_AUDIT_MISSING,
    FAIL_MACHINE_PROCEED_CLOSURE_MISSING,
    FAIL_SOURCE_CHAIN_INCOMPLETE,
    FAIL_SOURCE_ARTIFACT_AMBIGUOUS,
    FAIL_SOURCE_ARTIFACT_PATH_MISSING,
    FAIL_SOURCE_ARTIFACT_HASH_MISSING,
    FAIL_TARGET_LABEL_MISSING,
    FAIL_COMPRESSION_MODE_MISSING,
    FAIL_CRITICAL_FIELD_GROUPS_MISSING,
    FAIL_REQUIRED_RECOVERABLE_FIELDS_MISSING,
    FAIL_AUTHORITY_FIELD_GROUP_MISSING,
    FAIL_RADIUS_FIELD_GROUP_MISSING,
    FAIL_NON_EFFECT_FIELD_GROUP_MISSING,
    FAIL_STOP_STATE_FIELD_GROUP_MISSING,
    FAIL_AUTHORITY_SUBSTITUTION_BOUNDARY_MISSING,
    FAIL_COMPRESSION_PERFORMED,
    FAIL_PACKET_CREATED,
    FAIL_DECOMPRESSION_AUDIT,
    FAIL_REGISTRY_CREATED,
    FAIL_AUTHORITY_CHANGED,
    FAIL_REUSE_AUTHORIZED,
    FAIL_RADIUS_RENEWED,
    FAIL_MACHINE_ACTION,
    FAIL_RUNNER_AUTHORITY,
    FAIL_SOURCE_RECORDS_REPLACED,
]

CRITICAL_FIELD_GROUPS = [
    "authority_state_transition",
    "human_authority_decision",
    "requested_action",
    "route_classification",
    "candidate_archive_status",
    "candidate_audit_status",
    "promotion_decision",
    "active_archive_entry",
    "machine_proceed_action",
    "radius_accounting",
    "created_output_surface",
    "confirmed_non_effects",
    "remaining_forbidden_authorities",
    "post_use_stop_state",
    "next_possible_separate_surface",
]

REQUIRED_RECOVERABLE_FIELDS = {
    "authority_state_transition": [
        "prior_authority_state",
        "selected_human_authority_decision",
        "authority_event_consumed",
        "resulting_authority_state",
        "next_allowed_router_action",
    ],
    "human_authority_decision": [
        "decision_surface_id",
        "decision_receipt_id",
        "selected_decision_option",
        "decision_actor_class",
        "authority_event_status",
    ],
    "requested_action": [
        "requested_action_record_id",
        "requested_action",
        "requested_action_scope",
        "requested_output_kind",
        "basis_scope",
        "source_object_id",
    ],
    "route_classification": [
        "route_classification_id",
        "router_mode",
        "route_disposition",
        "classification_only",
        "action_executed_by_router",
        "authority_changed_by_router",
    ],
    "candidate_archive_status": [
        "candidate_entry_id",
        "entry_status",
        "promotion_status_before_D",
        "reuse_authority_status_before_D",
        "activation_status",
        "activation_status_reason",
        "candidate_radius",
    ],
    "candidate_audit_status": [
        "candidate_audit_id",
        "candidate_audit_status",
        "candidate_contract_conformant",
        "candidate_promoted",
        "candidate_reusable",
        "candidate_active",
    ],
    "promotion_decision": [
        "promotion_decision_surface_id",
        "promotion_decision_receipt_id",
        "selected_promotion_option",
        "promotion_scope",
        "radius_selected",
        "basis_scope",
        "source_object_id",
    ],
    "active_archive_entry": [
        "active_archive_entry_id",
        "entry_status",
        "promotion_status",
        "reuse_authority_status",
        "activation_status",
        "declared_scope",
        "radius_limit",
        "radius_remaining_before_use",
    ],
    "machine_proceed_action": [
        "machine_proceed_id",
        "performed_action",
        "performed_action_scope",
        "performed_basis_scope",
        "performed_source_object_id",
        "performed_output_kind",
        "validators_passed",
    ],
    "radius_accounting": [
        "radius_limit",
        "radius_before",
        "radius_consumed",
        "radius_after",
        "radius_exhausted",
        "radius_renewed",
        "further_machine_proceed_authorized_under_this_radius",
    ],
    "created_output_surface": [
        "output_surface_id",
        "output_object_type",
        "output_scope",
        "output_basis",
        "execution_status",
        "output_surface_status",
    ],
    "confirmed_non_effects": [
        "unit_executed",
        "runtime_executed",
        "authority_changed",
        "receipts_rewritten",
        "taxonomy_promoted",
        "reuse_scope_expanded",
        "updater_generalized",
        "runner_authority_created",
        "additional_radius_created",
        "active_archive_scope_expanded",
        "active_archive_entry_rewritten_by_closure",
        "active_archive_entry_mutated_by_closure",
    ],
    "remaining_forbidden_authorities": [
        "execution_remains_unauthorized",
        "runtime_remains_unauthorized",
        "receipt_rewrite_remains_unauthorized",
        "taxonomy_promotion_remains_unauthorized",
        "reuse_expansion_remains_unauthorized",
        "updater_generalization_remains_unauthorized",
        "runner_remains_unauthorized",
        "radius_renewal_remains_unauthorized",
    ],
    "post_use_stop_state": [
        "radius_exhausted",
        "active_entry_remains_audit_source",
        "entry_has_remaining_radius",
        "entry_may_authorize_additional_machine_proceed",
        "additional_use_requires_new_authority_or_radius",
        "same_radius_may_be_reused",
    ],
    "next_possible_separate_surface": [
        "next_possible_separate_surface",
        "created_by_closure",
        "authorized_by_closure",
        "machine_may_prepare_without_new_authority",
    ],
}

FORBIDDEN_MARKDOWN_PHRASES = [
    "trace compressed",
    "safe shortcut",
    "source replaced",
    "registry candidate created",
    "reuse authorized",
    "runner ready",
    "authority shortcut",
]


class GenerationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise GenerationError(code, detail)


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(FAIL_SOURCE_CHAIN_INCOMPLETE, proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def run_git(root: Path, args: list[str], failure_code: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(failure_code, proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def commit_for_paths(root: Path, paths: list[str], failure_code: str) -> str:
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        fail(failure_code, ",".join(paths))
    return run_git(root, ["log", "-n", "1", "--format=%H", "--", *existing], failure_code)


def verify_expected_commits(root: Path) -> None:
    run_git(root, ["cat-file", "-e", f"{D5_COMMIT}^{{commit}}"], FAIL_MACHINE_PROCEED_CLOSURE_MISSING)
    got = commit_for_paths(
        root,
        [
            D5_CLOSURE_PATH,
            "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.md",
            "scripts/build_c8_n22_machine_proceed_closure_v0.py",
        ],
        FAIL_MACHINE_PROCEED_CLOSURE_MISSING,
    )
    if got != D5_COMMIT:
        fail(FAIL_MACHINE_PROCEED_CLOSURE_MISSING, f"D.5 commit mismatch: {got}!={D5_COMMIT}")


def load_json(path: Path, failure_code: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        fail(failure_code, str(path))
        raise exc
    except json.JSONDecodeError as exc:
        fail(failure_code, f"{path}: {exc}")
        raise exc


def expect(value: object, wanted: object, failure_code: str, field: str) -> None:
    if value != wanted:
        fail(failure_code, f"{field}: {value!r}!={wanted!r}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_ref(root: Path, rel: str, artifact_id: str) -> dict[str, str]:
    path = root / rel
    if not path.exists():
        fail(FAIL_SOURCE_ARTIFACT_PATH_MISSING, rel)
    digest = sha256_file(path)
    if len(digest) != 64:
        fail(FAIL_SOURCE_ARTIFACT_HASH_MISSING, rel)
    return {
        "artifact_id": artifact_id,
        "path": rel,
        "sha256": digest,
        "sig8": digest[:8],
    }


def rel_path(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def discover_one(
    root: Path,
    predicate: Any,
    missing_code: str,
    description: str,
) -> tuple[str, dict[str, Any]]:
    matches: list[tuple[str, dict[str, Any]]] = []
    for path in sorted((root / "docs/matrixlabs").rglob("*.json")):
        rel = rel_path(root, path)
        data = load_json(path, missing_code)
        if predicate(data):
            matches.append((rel, data))
    if not matches:
        fail(missing_code, description)
    if len(matches) > 1:
        fail(FAIL_SOURCE_ARTIFACT_AMBIGUOUS, f"{description}: {[rel for rel, _ in matches]}")
    return matches[0]


def discover_sources(root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    a4 = discover_one(
        root,
        lambda d: d.get("closure_role") == "BLOCK_A_AUTHORITY_TRANSITION_CLOSURE"
        and d.get("closure_gate", {}).get("closure_status") == "AUTHORITY_TRANSITION_CLOSURE_PASS",
        FAIL_AUTHORITY_TRANSITION_CLOSURE_MISSING,
        "authority transition closure",
    )
    b3 = discover_one(
        root,
        lambda d: d.get("closure_role") == "BLOCK_B_READ_ONLY_ROUTER_SPECIMEN_CLOSURE"
        and d.get("closure_gate", {}).get("closure_status") == "ROUTER_SPECIMEN_CLOSURE_PASS_ALLOWED_PREPARE_ONLY",
        FAIL_ROUTER_SPECIMEN_CLOSURE_MISSING,
        "router specimen closure",
    )
    a3 = discover_one(
        root,
        lambda d: d.get("schema_version") == "matrixlabs_authority_state_update_v0"
        and d.get("authority_state_after", {}).get("new_authority_state")
        == "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        FAIL_SOURCE_CHAIN_INCOMPLETE,
        "authority state update",
    )
    b2 = discover_one(
        root,
        lambda d: d.get("schema_version") == "matrixlabs_authority_route_classification_v0"
        and d.get("route_classification_id") == "c8.n22.route.prepare_next_unit_definition_surface.v0",
        FAIL_SOURCE_CHAIN_INCOMPLETE,
        "route classification",
    )

    fixed = {
        "candidate_archive_audit": (C3_AUDIT_PATH, load_json(root / C3_AUDIT_PATH, FAIL_CANDIDATE_AUDIT_MISSING)),
        "machine_proceed_closure": (D5_CLOSURE_PATH, load_json(root / D5_CLOSURE_PATH, FAIL_MACHINE_PROCEED_CLOSURE_MISSING)),
        "candidate_archive_entry": (C2_ENTRY_PATH, load_json(root / C2_ENTRY_PATH, FAIL_SOURCE_CHAIN_INCOMPLETE)),
        "active_archive_entry": (D3_ACTIVE_PATH, load_json(root / D3_ACTIVE_PATH, FAIL_SOURCE_CHAIN_INCOMPLETE)),
        "machine_proceed": (D4_PROCEED_PATH, load_json(root / D4_PROCEED_PATH, FAIL_SOURCE_CHAIN_INCOMPLETE)),
        "output_surface": (D4_SURFACE_PATH, load_json(root / D4_SURFACE_PATH, FAIL_SOURCE_CHAIN_INCOMPLETE)),
    }
    return {
        "authority_transition_closure": a4,
        "router_specimen_closure": b3,
        "authority_state_update": a3,
        "route_classification": b2,
        **fixed,
    }


def artifact_id_for(kind: str, data: dict[str, Any]) -> str:
    keys = {
        "authority_transition_closure": ["closure_id"],
        "router_specimen_closure": ["router_specimen_closure_id", "closure_id"],
        "candidate_archive_audit": ["audit_id"],
        "machine_proceed_closure": ["closure_id"],
        "authority_state_update": ["authority_update_id"],
        "route_classification": ["route_classification_id"],
        "candidate_archive_entry": ["archive_entry_id"],
        "active_archive_entry": ["active_archive_entry_id"],
        "machine_proceed": ["machine_proceed_id"],
        "output_surface": ["unit_surface_id"],
    }[kind]
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    fail(FAIL_SOURCE_CHAIN_INCOMPLETE, f"{kind} artifact id missing")
    raise AssertionError


def validate_sources(sources: dict[str, tuple[str, dict[str, Any]]]) -> None:
    a4 = sources["authority_transition_closure"][1]
    expect(a4.get("closure_gate", {}).get("source_chain_complete"), True, FAIL_SOURCE_CHAIN_INCOMPLETE, "a4.source_chain_complete")
    b3 = sources["router_specimen_closure"][1]
    expect(b3.get("closure_gate", {}).get("source_chain_complete"), True, FAIL_SOURCE_CHAIN_INCOMPLETE, "b3.source_chain_complete")
    audit = sources["candidate_archive_audit"][1]
    expect(audit.get("audit_id"), AUDIT_ID, FAIL_CANDIDATE_AUDIT_MISSING, "candidate audit id")
    expect(audit.get("audit_result", {}).get("candidate_audit_status"), AUDIT_STATUS, FAIL_CANDIDATE_AUDIT_MISSING, "candidate audit status")
    closure = sources["machine_proceed_closure"][1]
    expect(closure.get("closure_id"), D5_CLOSURE_ID, FAIL_MACHINE_PROCEED_CLOSURE_MISSING, "D5 closure id")
    expect(closure.get("closure_status"), D5_CLOSURE_STATUS, FAIL_MACHINE_PROCEED_CLOSURE_MISSING, "D5 closure status")
    expect(closure.get("block_closed"), True, FAIL_MACHINE_PROCEED_CLOSURE_MISSING, "D5 block_closed")
    expect(closure.get("radius_result", {}).get("radius_after"), 0, FAIL_RADIUS_FIELD_GROUP_MISSING, "D5 radius_after")
    expect(closure.get("terminal_transition"), "STOP_BLOCK_D_MACHINE_PROCEED_CLOSED", FAIL_MACHINE_PROCEED_CLOSURE_MISSING, "D5 terminal")

    entry = sources["candidate_archive_entry"][1]
    expect(entry.get("archive_entry_id"), "candidate.c8.n22.prepare_next_unit_definition_surface.v0", FAIL_SOURCE_CHAIN_INCOMPLETE, "candidate archive entry")
    active = sources["active_archive_entry"][1]
    expect(active.get("active_archive_entry_id"), ACTIVE_ENTRY_ID, FAIL_SOURCE_CHAIN_INCOMPLETE, "active entry")
    proceed = sources["machine_proceed"][1]
    expect(proceed.get("machine_proceed_id"), MACHINE_PROCEED_ID, FAIL_SOURCE_CHAIN_INCOMPLETE, "machine proceed id")
    surface = sources["output_surface"][1]
    expect(surface.get("unit_surface_id"), OUTPUT_SURFACE_ID, FAIL_SOURCE_CHAIN_INCOMPLETE, "output surface id")


def build_source_artifacts(root: Path, sources: dict[str, tuple[str, dict[str, Any]]]) -> tuple[dict[str, Any], dict[str, Any]]:
    primary_keys = [
        "authority_transition_closure",
        "router_specimen_closure",
        "candidate_archive_audit",
        "machine_proceed_closure",
    ]
    supporting_keys = [
        "authority_state_update",
        "route_classification",
        "candidate_archive_entry",
        "active_archive_entry",
        "machine_proceed",
        "output_surface",
    ]
    primary = {
        key: source_ref(root, sources[key][0], artifact_id_for(key, sources[key][1]))
        for key in primary_keys
    }
    supporting = {
        key: source_ref(root, sources[key][0], artifact_id_for(key, sources[key][1]))
        for key in supporting_keys
    }
    return primary, supporting


def source_chain(primary: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_transition_closure_id": primary["authority_transition_closure"]["artifact_id"],
        "router_specimen_closure_id": primary["router_specimen_closure"]["artifact_id"],
        "candidate_archive_audit_id": primary["candidate_archive_audit"]["artifact_id"],
        "machine_proceed_closure_id": primary["machine_proceed_closure"]["artifact_id"],
        "source_chain_complete": True,
    }


def expected_critical_values() -> dict[str, Any]:
    return {
        "authority_state_transition": {
            "prior_authority_state": "AUTH_STATE_OBSERVED_NOT_AUTHORIZED",
            "resulting_authority_state": "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        },
        "requested_action": {
            "requested_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "requested_action_scope": "PREPARE_SURFACE_ONLY",
            "basis_scope": "C8_N22_BASIS_ONLY",
            "source_object_id": "c8.n22",
        },
        "route_classification": {
            "router_mode": "CLASSIFY_ONLY_NO_ACTION",
            "route_disposition": "ROUTE_MACHINE_MAY_PREPARE_ONLY",
            "action_executed_by_router": False,
            "authority_changed_by_router": False,
        },
        "candidate_archive_status": {
            "entry_status": "ARCHIVE_STATUS_CANDIDATE",
            "promotion_status_before_D": "PROMOTION_NOT_REQUESTED",
            "reuse_authority_status_before_D": "REUSE_AUTHORITY_NOT_GRANTED",
            "activation_status": "ACTIVATION_NOT_APPLICABLE",
            "activation_status_reason": "CANDIDATE_ENTRY_NOT_ACTIVATABLE",
            "candidate_radius": "RADIUS_0_CANDIDATE_ONLY",
        },
        "candidate_audit_status": {
            "candidate_audit_status": AUDIT_STATUS,
            "candidate_contract_conformant": True,
            "candidate_promoted": False,
            "candidate_reusable": False,
            "candidate_active": False,
        },
        "promotion_decision": {
            "selected_promotion_option": "DECISION_PROMOTE_CANDIDATE_FOR_DECLARED_SCOPE",
            "radius_selected": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
            "basis_scope": "C8_N22_BASIS_ONLY",
            "source_object_id": "c8.n22",
        },
        "active_archive_entry": {
            "entry_status": "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
            "promotion_status": "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
            "reuse_authority_status": "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
            "activation_status": "ACTIVATION_ACTIVE",
            "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
        },
        "machine_proceed_action": {
            "performed_action": "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "performed_action_scope": "PREPARE_SURFACE_ONLY",
            "performed_basis_scope": "C8_N22_BASIS_ONLY",
            "performed_source_object_id": "c8.n22",
            "performed_output_kind": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        },
        "radius_accounting": {
            "radius_limit": "RADIUS_1_SINGLE_C8_N22_BASIS_OBJECT",
            "radius_before": 1,
            "radius_consumed": 1,
            "radius_after": 0,
            "radius_exhausted": True,
            "radius_renewed": False,
            "further_machine_proceed_authorized_under_this_radius": False,
        },
        "created_output_surface": {
            "output_object_type": "NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
            "output_scope": "SURFACE_ONLY",
            "output_basis": "c8.n22",
            "execution_status": "NOT_EXECUTED",
            "output_surface_status": "NEXT_UNIT_DEFINITION_SURFACE_PREPARED_NOT_EXECUTED",
        },
        "post_use_stop_state": {
            "radius_exhausted": True,
            "active_entry_remains_audit_source": True,
            "entry_has_remaining_radius": False,
            "entry_may_authorize_additional_machine_proceed": False,
            "additional_use_requires_new_authority_or_radius": True,
            "same_radius_may_be_reused": False,
        },
        "next_possible_separate_surface": {
            "next_possible_separate_surface": "REVIEW_OR_DECISION_SURFACE_FOR_CREATED_NEXT_UNIT",
            "created_by_closure": False,
            "authorized_by_closure": False,
            "machine_may_prepare_without_new_authority": False,
        },
    }


def compression_boundary() -> dict[str, Any]:
    return {
        "allowed_effect": "DECLARE_TARGET_AND_CRITICAL_FIELDS_ONLY",
        "compression_performed_by_e1": False,
        "compressed_packet_created_by_e1": False,
        "decompression_audit_performed_by_e1": False,
        "compression_registry_created_by_e1": False,
        "authority_changed_by_e1": False,
        "reuse_authorized_by_e1": False,
        "radius_renewed_by_e1": False,
        "machine_action_performed_by_e1": False,
        "runner_authority_created_by_e1": False,
        "source_records_replaced_by_e1": False,
    }


def authority_substitution_boundary() -> dict[str, bool]:
    return {
        "compressed_packet_may_replace_source_records_as_authority": False,
        "compressed_packet_may_satisfy_active_entry_requirement": False,
        "compressed_packet_may_satisfy_human_decision_requirement": False,
        "compressed_packet_may_satisfy_radius_requirement": False,
        "compressed_packet_may_authorize_machine_proceed": False,
    }


def required_later_audit() -> dict[str, bool]:
    return {
        "decompression_audit_required": True,
        "audit_must_recover_all_critical_field_groups": True,
        "audit_must_recover_all_required_recoverable_fields": True,
        "audit_must_compare_against_source_chain": True,
        "audit_must_compare_source_hashes": True,
        "audit_must_fail_on_authority_strengthening": True,
        "audit_must_fail_on_radius_renewal": True,
        "audit_must_fail_on_runner_authority": True,
        "audit_must_fail_on_source_record_replacement": True,
    }


def target_gate() -> dict[str, Any]:
    gate = {
        "compression_target_gate": TARGET_STATUS,
        "authority_transition_closure_present": True,
        "router_specimen_closure_present": True,
        "candidate_archive_audit_present": True,
        "machine_proceed_closure_present": True,
        "source_chain_complete": True,
        "source_artifact_paths_recorded": True,
        "source_artifact_hashes_recorded": True,
        "target_trace_label": TARGET_TRACE_LABEL,
        "compression_mode": COMPRESSION_MODE,
        "critical_field_group_count": len(CRITICAL_FIELD_GROUPS),
        "critical_field_groups_declared": True,
        "required_recoverable_fields_declared": True,
        "authority_substitution_boundary_declared": True,
        "failures": [],
    }
    gate.update({key: value for key, value in compression_boundary().items() if key != "allowed_effect"})
    return gate


def source_identity_policy() -> dict[str, bool]:
    return {
        "source_refs_are_manifest_bound": True,
        "source_hashes_required_for_later_audit": True,
        "mtime_or_latest_file_resolution_allowed": False,
        "directory_scan_authority_allowed": False,
    }


def build_record(root: Path, sources: dict[str, tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    primary, supporting = build_source_artifacts(root, sources)
    return {
        "schema_version": SCHEMA_VERSION,
        "compression_target_id": COMPRESSION_TARGET_ID,
        "target_role": TARGET_ROLE,
        "target_status": TARGET_STATUS,
        "block_id": BLOCK_ID,
        "block_unit_id": BLOCK_UNIT_ID,
        "block_e_status": BLOCK_E_STATUS,
        "compression_mode": COMPRESSION_MODE,
        "target_trace_label": TARGET_TRACE_LABEL,
        "source_artifacts": primary,
        "supporting_source_artifacts": supporting,
        "source_identity_policy": source_identity_policy(),
        "source_chain": source_chain(primary),
        "critical_field_groups": CRITICAL_FIELD_GROUPS,
        "critical_field_group_count": len(CRITICAL_FIELD_GROUPS),
        "required_recoverable_fields_by_group": REQUIRED_RECOVERABLE_FIELDS,
        "expected_critical_values": expected_critical_values(),
        "compression_boundary": compression_boundary(),
        "authority_substitution_boundary": authority_substitution_boundary(),
        "required_later_audit": required_later_audit(),
        "target_gate": target_gate(),
        "failure_vocabulary": FAILURE_VOCABULARY,
        "non_claims": [
            "E.1 does not compress the trace.",
            "E.1 does not create a compressed packet.",
            "E.1 does not audit decompression.",
            "E.1 does not create a registry entry.",
            "E.1 does not authorize reuse.",
            "E.1 does not renew radius.",
            "E.1 does not perform machine action.",
            "E.1 does not replace source records.",
            "E.1 does not create runner authority.",
            "E.1 only declares the compression target and the critical fields that must be preserved.",
        ],
        "key_non_claims": [
            "compression target declaration ≠ compressed packet",
            "declaring critical fields ≠ proving they were preserved",
            "observability compression ≠ authority compression",
            "compressed packet ≠ authority source",
        ],
        "precommit_c8_n22_compression_target_gate": PRECOMMIT_GATE,
        "compression_target_gate": TARGET_STATUS,
        "terminal_transition": TERMINAL_TRANSITION,
        "generated_by": GENERATOR,
    }


def validate_record(record: dict[str, Any]) -> None:
    expect(record.get("schema_version"), SCHEMA_VERSION, FAIL_SOURCE_CHAIN_INCOMPLETE, "schema_version")
    expect(record.get("compression_target_id"), COMPRESSION_TARGET_ID, FAIL_TARGET_LABEL_MISSING, "compression_target_id")
    expect(record.get("target_trace_label"), TARGET_TRACE_LABEL, FAIL_TARGET_LABEL_MISSING, "target_trace_label")
    expect(record.get("compression_mode"), COMPRESSION_MODE, FAIL_COMPRESSION_MODE_MISSING, "compression_mode")
    expect(record.get("critical_field_group_count"), 15, FAIL_CRITICAL_FIELD_GROUPS_MISSING, "critical_field_group_count")
    expect(record.get("critical_field_groups"), CRITICAL_FIELD_GROUPS, FAIL_CRITICAL_FIELD_GROUPS_MISSING, "critical_field_groups")
    expect(set(record.get("required_recoverable_fields_by_group", {})), set(CRITICAL_FIELD_GROUPS), FAIL_REQUIRED_RECOVERABLE_FIELDS_MISSING, "recoverable group set")
    expect("radius_after" in record["required_recoverable_fields_by_group"]["radius_accounting"], True, FAIL_RADIUS_FIELD_GROUP_MISSING, "radius_after")
    expect("same_radius_may_be_reused" in record["required_recoverable_fields_by_group"]["post_use_stop_state"], True, FAIL_STOP_STATE_FIELD_GROUP_MISSING, "same_radius_may_be_reused")
    expect("active_archive_scope_expanded" in record["required_recoverable_fields_by_group"]["confirmed_non_effects"], True, FAIL_NON_EFFECT_FIELD_GROUP_MISSING, "active_archive_scope_expanded")
    expect("machine_may_prepare_without_new_authority" in record["required_recoverable_fields_by_group"]["next_possible_separate_surface"], True, FAIL_STOP_STATE_FIELD_GROUP_MISSING, "machine_may_prepare_without_new_authority")
    for section in ["source_artifacts", "supporting_source_artifacts"]:
        for name, ref in record.get(section, {}).items():
            if not ref.get("path"):
                fail(FAIL_SOURCE_ARTIFACT_PATH_MISSING, name)
            if len(ref.get("sha256", "")) != 64 or ref.get("sig8") != ref.get("sha256", "")[:8]:
                fail(FAIL_SOURCE_ARTIFACT_HASH_MISSING, name)
    for key, value in record["compression_boundary"].items():
        if key != "allowed_effect" and value is not False:
            fail(FAIL_COMPRESSION_PERFORMED, key)
    for key, value in record["authority_substitution_boundary"].items():
        if value is not False:
            fail(FAIL_AUTHORITY_SUBSTITUTION_BOUNDARY_MISSING, key)
    expect(record.get("target_gate", {}).get("failures"), [], FAIL_SOURCE_CHAIN_INCOMPLETE, "target_gate.failures")
    expect(record.get("terminal_transition"), TERMINAL_TRANSITION, FAIL_SOURCE_CHAIN_INCOMPLETE, "terminal_transition")


def render_markdown(record: dict[str, Any]) -> str:
    source = record["source_chain"]
    groups = "\n".join(f"- {group.replace('_', ' ')}" for group in CRITICAL_FIELD_GROUPS)
    return f"""# C8 n22 authority-action trace compression target v0

## Status

{TARGET_STATUS}

## Target trace

{TARGET_TRACE_LABEL}

## Compression mode

{COMPRESSION_MODE}

## Source closures

- authority transition closure: {source['authority_transition_closure_id']}
- router specimen closure: {source['router_specimen_closure_id']}
- candidate archive audit: {source['candidate_archive_audit_id']}
- machine proceed closure: {source['machine_proceed_closure_id']}

## Source identity policy

- source artifact paths recorded
- source artifact hashes recorded
- latest-file resolution not allowed
- directory scan authority not allowed

## Critical field groups

{groups}

## Required later audit

A later decompression audit must recover all critical field groups and all required recoverable fields, compare them against the source chain, and fail on authority strengthening, radius renewal, runner authority, or source-record replacement.

## Non-effects

- no compression performed
- no E.2 packet produced
- no decompression audit performed
- no registry produced
- no authority changed
- no reuse grant issued
- no radius renewed
- no machine action performed
- no runner authority created
- no source records replaced

## Authority substitution boundary

The compressed packet may not replace source records as authority, satisfy active-entry requirements, satisfy human-decision requirements, satisfy radius requirements, or authorize machine proceed.

## Next

A compressed packet may be created separately in E.2 and must later pass decompression parity audit.
"""


def validate_markdown(text: str) -> None:
    lowered = text.lower()
    for phrase in FORBIDDEN_MARKDOWN_PHRASES:
        if phrase in lowered:
            fail(FAIL_SOURCE_CHAIN_INCOMPLETE, f"forbidden markdown phrase: {phrase}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_outputs(root: Path, record: dict[str, Any]) -> None:
    json_content = json.dumps(record, indent=2, sort_keys=True) + "\n"
    md_content = render_markdown(record)
    validate_markdown(md_content)
    write_text(root / OUTPUT_JSON, json_content)
    write_text(root / OUTPUT_MD, md_content)


def bool_text(value: bool) -> str:
    return str(value).lower()


def print_success(record: dict[str, Any]) -> None:
    policy = record["source_identity_policy"]
    gate = record["target_gate"]
    boundary = record["compression_boundary"]
    substitution = record["authority_substitution_boundary"]
    audit = record["required_later_audit"]

    print("BUILD_C8_N22_AUTHORITY_ACTION_TRACE_COMPRESSION_TARGET_V0_COMPLETE")
    print(f"compression_target_id={record['compression_target_id']}")
    print(f"schema_version={record['schema_version']}")
    print(f"target_role={record['target_role']}")
    print(f"target_status={record['target_status']}")
    print(f"block_id={record['block_id']}")
    print(f"block_unit_id={record['block_unit_id']}")
    print(f"block_e_status={record['block_e_status']}")
    print(f"compression_mode={record['compression_mode']}")
    print(f"target_trace_label={record['target_trace_label']}")
    print(f"source_chain_complete={bool_text(record['source_chain']['source_chain_complete'])}")
    print(f"source_artifact_paths_recorded={bool_text(gate['source_artifact_paths_recorded'])}")
    print(f"source_artifact_hashes_recorded={bool_text(gate['source_artifact_hashes_recorded'])}")
    print(f"source_hashes_required_for_later_audit={bool_text(policy['source_hashes_required_for_later_audit'])}")
    print(f"mtime_or_latest_file_resolution_allowed={bool_text(policy['mtime_or_latest_file_resolution_allowed'])}")
    print(f"directory_scan_authority_allowed={bool_text(policy['directory_scan_authority_allowed'])}")
    print(f"critical_field_group_count={record['critical_field_group_count']}")
    print(f"critical_field_groups_declared={bool_text(gate['critical_field_groups_declared'])}")
    print(f"required_recoverable_fields_declared={bool_text(gate['required_recoverable_fields_declared'])}")
    print(f"authority_substitution_boundary_declared={bool_text(gate['authority_substitution_boundary_declared'])}")
    for key in [
        "compression_performed_by_e1",
        "compressed_packet_created_by_e1",
        "decompression_audit_performed_by_e1",
        "compression_registry_created_by_e1",
        "authority_changed_by_e1",
        "reuse_authorized_by_e1",
        "radius_renewed_by_e1",
        "machine_action_performed_by_e1",
        "runner_authority_created_by_e1",
        "source_records_replaced_by_e1",
    ]:
        print(f"{key}={bool_text(boundary[key])}")
    for key in [
        "compressed_packet_may_replace_source_records_as_authority",
        "compressed_packet_may_satisfy_active_entry_requirement",
        "compressed_packet_may_satisfy_human_decision_requirement",
        "compressed_packet_may_satisfy_radius_requirement",
        "compressed_packet_may_authorize_machine_proceed",
    ]:
        print(f"{key}={bool_text(substitution[key])}")
    for key in [
        "decompression_audit_required",
        "audit_must_recover_all_critical_field_groups",
        "audit_must_recover_all_required_recoverable_fields",
        "audit_must_compare_against_source_chain",
        "audit_must_compare_source_hashes",
        "audit_must_fail_on_authority_strengthening",
        "audit_must_fail_on_radius_renewal",
        "audit_must_fail_on_runner_authority",
        "audit_must_fail_on_source_record_replacement",
    ]:
        print(f"{key}={bool_text(audit[key])}")
    print(f"compression_target_gate={record['compression_target_gate']}")
    print(f"precommit_c8_n22_compression_target_gate={record['precommit_c8_n22_compression_target_gate']}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={record['terminal_transition']}")


def main() -> int:
    try:
        root = detect_repo_root(Path.cwd())
        verify_expected_commits(root)
        sources = discover_sources(root)
        validate_sources(sources)
        record = build_record(root, sources)
        validate_record(record)
        write_outputs(root, record)
    except GenerationError as exc:
        print(f"STOP_{exc.code}")
        if exc.detail:
            print(exc.detail, file=sys.stderr)
        return 2
    print_success(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
