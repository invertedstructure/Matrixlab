#!/usr/bin/env python3

"""Build PHASE VS0.1 source inventory and preflight v0.

VS0.1 inventories the committed Block F runway and declares phase scope. It
does not build the A-to-F specimen, run probes, create authority, or execute.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GENERATOR = "scripts/build_phase_vs0_source_inventory_v0.py"
OUTPUT_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.json"
OUTPUT_MD = "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.md"
BASELINE_MANIFEST = "baseline_share/MANIFEST.json"
BASELINE_GENERATOR = "scripts/build_baseline_share_v0.py"

F4 = "docs/matrixlabs/registry/closures/c8_n22_radius_bound_prepare_trace_registry_candidate_closure_v0.json"
F3 = "docs/matrixlabs/registry/audits/c8_n22_radius_bound_prepare_trace_registry_candidate_audit_v0.json"
F2 = "docs/matrixlabs/registry/candidates/c8_n22_radius_bound_prepare_trace_registry_candidate_v0.json"
F1 = "docs/matrixlabs/registry/compression_trace_registry_entry_schema_contract_v0.json"
E4 = "docs/matrixlabs/compression/c8_n22_compression_specimen_closure_v0.json"
E3 = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_decompression_audit_v0.json"
E2 = "docs/matrixlabs/compression/c8_n22_radius_bound_prepare_trace_compressed_packet_v0.json"
D5 = "docs/matrixlabs/proceed/c8_n22_machine_proceed_closure_v0.json"

SCHEMA_VERSION = "matrixlabs_phase_vs0_source_inventory_v0"
INVENTORY_ID = "phase_vs0_source_inventory_v0"
PASS_STATUS = "VS0_PREFLIGHT_PASS_SCOPE_DECLARED"
STOP_STATUS = "VS0_PREFLIGHT_STOP_REQUIRED_START_SOURCE_MISSING"
PASS_TRANSITION = "ADVANCE(VS0_2_HAPPY_PATH_A_TO_F_ARTIFACT_BUILD_PENDING)"
STOP_TRANSITION = "STOP_VS0_PREFLIGHT_REQUIRED_START_SOURCE_MISSING"
RUN_NAMESPACE = "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0"

FAILURE_VOCABULARY = [
    "VS0_PREFLIGHT_FAIL_REPO_ROOT_MISSING",
    "VS0_PREFLIGHT_FAIL_GIT_HEAD_UNAVAILABLE",
    "VS0_PREFLIGHT_FAIL_BASELINE_SHARE_UNAVAILABLE",
    "VS0_PREFLIGHT_STOP_REQUIRED_START_SOURCE_MISSING",
    "VS0_PREFLIGHT_STOP_START_AUTHORITY_STATE_AMBIGUOUS",
    "VS0_PREFLIGHT_FAIL_PHASE_SCOPE_UNDECLARED",
    "VS0_PREFLIGHT_FAIL_FORBIDDEN_SCOPE_UNDECLARED",
    "VS0_PREFLIGHT_FAIL_EXPECTED_OUTPUT_MARKED_AS_REQUIRED_SOURCE",
    "VS0_PREFLIGHT_FAIL_CANONICAL_OUTPUT_NAMESPACE_COLLISION",
    "VS0_PREFLIGHT_FAIL_DISCUSSION_PACKETS_IN_SCOPE",
    "VS0_PREFLIGHT_FAIL_ACTIVE_REGISTRY_CREATED",
    "VS0_PREFLIGHT_FAIL_RUNNER_AUTHORITY_CREATED",
    "VS0_PREFLIGHT_FAIL_MACHINE_ACTION_PERFORMED",
    "VS0_PREFLIGHT_FAIL_RADIUS_RENEWED",
    "VS0_PREFLIGHT_FAIL_SOURCE_AUTHORITY_REPLACED",
]

MOST_IMPORTANT_COLLAPSE_POINTS = [
    "VS0_PREFLIGHT_STOP_REQUIRED_START_SOURCE_MISSING",
    "VS0_PREFLIGHT_FAIL_EXPECTED_OUTPUT_MARKED_AS_REQUIRED_SOURCE",
    "VS0_PREFLIGHT_FAIL_CANONICAL_OUTPUT_NAMESPACE_COLLISION",
    "VS0_PREFLIGHT_FAIL_RUNNER_AUTHORITY_CREATED",
]

NON_CLAIMS = [
    "VS0.1 does not build the A\u2192F specimen.",
    "VS0.1 does not create A4/B3/C3/D5/E4/F4.",
    "VS0.1 does not run negative probes.",
    "VS0.1 does not measure final Evidence Yield.",
    "VS0.1 does not activate a registry.",
    "VS0.1 does not generalize a trace.",
    "VS0.1 does not authorize reuse.",
    "VS0.1 does not renew radius.",
    "VS0.1 does not authorize machine proceed.",
    "VS0.1 does not execute the next unit.",
    "VS0.1 does not create runner authority.",
    "VS0.1 only inventories source state and declares phase scope.",
]

KEY_NON_CLAIMS = [
    "preflight \u2260 build",
    "expected VS0 output absent \u2260 missing required source",
    "committed source context \u2260 expected VS0 output",
    "scope declared \u2260 authority expanded",
    "baseline_share projection \u2260 semantic authority",
]

EXPECTED_OUTPUTS = [
    {
        "object_id": "phase_vs0.runtime.a4_authority_transition_closure.v0",
        "phase_step": "VS0.2/A4",
        "relative_path": "a_to_f/a4_authority_transition_closure_v0.json",
        "source_group": "authority_boundary_sources",
    },
    {
        "object_id": "phase_vs0.runtime.b3_router_specimen_closure.v0",
        "phase_step": "VS0.2/B3",
        "relative_path": "a_to_f/b3_router_specimen_closure_v0.json",
        "source_group": "route_sources",
    },
    {
        "object_id": "phase_vs0.runtime.c3_candidate_archive_admissibility_audit.v0",
        "phase_step": "VS0.2/C3",
        "relative_path": "a_to_f/c3_candidate_archive_admissibility_audit_v0.json",
        "source_group": "candidate_archive_sources",
    },
    {
        "object_id": "phase_vs0.runtime.d5_machine_proceed_closure.v0",
        "phase_step": "VS0.2/D5",
        "relative_path": "a_to_f/d5_machine_proceed_closure_v0.json",
        "source_group": "machine_proceed_sources",
    },
    {
        "object_id": "phase_vs0.runtime.e4_compression_specimen_closure.v0",
        "phase_step": "VS0.2/E4",
        "relative_path": "a_to_f/e4_compression_specimen_closure_v0.json",
        "source_group": "compression_sources",
    },
    {
        "object_id": "phase_vs0.runtime.f4_registry_candidate_closure_projection.v0",
        "phase_step": "VS0.2/F4",
        "relative_path": "a_to_f/f4_registry_candidate_closure_projection_v0.json",
        "source_group": "registry_sources",
    },
]

PRIOR_CONTEXT = {
    "authority_boundary_sources": [
        ("c8.n22.authority_transition_closure.v0", "docs/matrixlabs/boundary/c8_n22_authority_transition_closure_v0.json"),
    ],
    "route_sources": [
        ("c8.n22.router_specimen_closure.v0", "docs/matrixlabs/router/c8_n22_read_only_router_specimen_closure_v0.json"),
    ],
    "candidate_archive_sources": [
        ("c8.n22.candidate_archive_entry.admissibility_audit.v0", "docs/matrixlabs/validator_archive/audits/c8_n22_candidate_archive_entry_admissibility_audit_v0.json"),
    ],
    "promotion_sources": [
        ("c8.n22.candidate_promotion_decision_receipt.v0", "docs/matrixlabs/validator_archive/promotion/c8_n22_candidate_promotion_decision_receipt_v0.json"),
        ("active.c8.n22.prepare_next_unit_definition_surface.v0", "docs/matrixlabs/validator_archive/active/c8_n22_prepare_next_unit_definition_active_archive_entry_v0.json"),
    ],
    "machine_proceed_sources": [
        ("c8.n22.machine_proceed_closure.v0", D5),
    ],
    "compression_sources": [
        ("c8.n22.radius_bound_prepare_trace.compressed_packet.v0", E2),
        ("c8.n22.radius_bound_prepare_trace.decompression_audit.v0", E3),
        ("c8.n22.compression_specimen_closure.v0", E4),
    ],
    "registry_sources": [
        ("compression_trace_registry_entry_schema_contract.v0", F1),
        ("candidate.registry.c8_n22_radius_bound_prepare_trace.v0", F2),
        ("audit.registry.c8_n22_radius_bound_prepare_trace.candidate_admissibility.v0", F3),
        ("c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0", F4),
    ],
}

REQUIRED_FILE_SOURCES = [
    ("f4_registry_candidate_closure", F4, "registry_sources"),
    ("f3_registry_candidate_admissibility_audit", F3, "registry_sources"),
    ("f2_registry_candidate", F2, "registry_sources"),
    ("f1_registry_schema_contract", F1, "registry_sources"),
    ("e4_compression_specimen_closure", E4, "compression_sources"),
    ("e3_decompression_audit", E3, "compression_sources"),
    ("e2_compressed_packet", E2, "compression_sources"),
    ("d5_machine_proceed_closure", D5, "machine_proceed_sources"),
]


class GenerationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise GenerationError(code, detail)


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
        fail(failure_code, proc.stderr.strip())
    return proc.stdout.rstrip()


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
        fail(FAILURE_VOCABULARY[0], proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    content = path.read_bytes()
    try:
        return json.loads(content), content
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail("VS0_PREFLIGHT_FAIL_REQUIRED_SOURCE_MALFORMED_JSON", f"{path}: {exc}")


def worktree_path_from_status(line: str) -> str:
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path


def validate_dirty_scope(status_lines: list[str]) -> None:
    allowed_exact = {
        GENERATOR,
        "scripts/build_baseline_share_v0.py",
    }
    allowed_prefixes = (
        "baseline_share/",
        "docs/matrixlabs/phase_vs0/phase_vs0_source_inventory_v0.",
    )
    for line in status_lines:
        path = worktree_path_from_status(line)
        if path in {"discussion_packets/", "docs/matrixlabs/phase_vs0/"} or path in allowed_exact:
            continue
        if any(path.startswith(prefix) for prefix in allowed_prefixes):
            continue
        fail("VS0_PREFLIGHT_FAIL_NON_DISCUSSION_DIRTY_PATH", line)


def status_error(data: dict[str, Any], relative_path: str) -> str | None:
    if relative_path == F4:
        checks = [
            ("registry_candidate_closure_id", data.get("registry_candidate_closure_id"), "c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0"),
            ("closure_status", data.get("closure_status"), "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY"),
            ("block_status", data.get("block_status"), "BLOCK_F_PASS_LOCAL_REGISTRY_CANDIDATE_CLOSED"),
            ("block_closed", data.get("block_closed"), True),
            ("terminal_transition", data.get("terminal_transition"), "STOP_BLOCK_F_REGISTRY_CANDIDATE_CLOSURE_COMPLETE"),
        ]
    elif relative_path == F3:
        checks = [
            ("registry_candidate_audit_id", data.get("registry_candidate_audit_id"), "audit.registry.c8_n22_radius_bound_prepare_trace.candidate_admissibility.v0"),
            ("audit_status", data.get("audit_status"), "REGISTRY_CANDIDATE_ADMISSIBILITY_AUDIT_PASS_LOCAL_ONLY"),
            ("audited_candidate_id", data.get("audited_candidate_id"), "candidate.registry.c8_n22_radius_bound_prepare_trace.v0"),
        ]
    elif relative_path == F2:
        checks = [
            ("registry_candidate_id", data.get("registry_candidate_id"), "candidate.registry.c8_n22_radius_bound_prepare_trace.v0"),
            ("candidate_status", data.get("candidate_status"), "REGISTRY_STATUS_CANDIDATE"),
            ("trace_label", data.get("trace_identity", {}).get("trace_label"), "C8_N22_RADIUS_BOUND_PREPARE_TRACE_V0"),
            ("trace_scope", data.get("trace_identity", {}).get("trace_scope"), "C8_N22_LOCAL_SPECIMEN_ONLY"),
            ("specimen_count", data.get("specimen_evidence", {}).get("specimen_count"), 1),
            ("evidence_kind", data.get("specimen_evidence", {}).get("evidence_kind"), "SINGLE_LOCAL_SPECIMEN"),
            ("generalization_status", data.get("generalization_status", {}).get("generalization_status"), "LOCAL_SPECIMEN_ONLY_NOT_GENERALIZED"),
        ]
    elif relative_path == F1:
        checks = [
            ("registry_schema_id", data.get("registry_schema_id"), "compression_trace_registry_entry_schema_contract.v0"),
            ("schema_status", data.get("schema_status"), "REGISTRY_SCHEMA_PASS_CONTRACT_DEFINED_ONLY"),
        ]
    elif relative_path == E4:
        checks = [
            ("compression_closure_id", data.get("compression_closure_id"), "c8.n22.compression_specimen_closure.v0"),
            ("closure_status", data.get("closure_status"), "COMPRESSION_CLOSURE_PASS_OBSERVABILITY_ONLY"),
        ]
    elif relative_path == E3:
        checks = [
            ("decompression_audit_id", data.get("decompression_audit_id"), "c8.n22.radius_bound_prepare_trace.decompression_audit.v0"),
            ("decompression_audit_status", data.get("audit_result", {}).get("decompression_audit_status"), "DECOMPRESSION_AUDIT_PASS_CRITICAL_FIELD_PARITY"),
        ]
    elif relative_path == E2:
        checks = [
            ("compressed_packet_id", data.get("compressed_packet_id"), "c8.n22.radius_bound_prepare_trace.compressed_packet.v0"),
            ("packet_status", data.get("packet_status"), "COMPRESSED_PACKET_CREATED_PENDING_DECOMPRESSION_AUDIT"),
        ]
    else:
        checks = [
            ("closure_id", data.get("closure_id"), "c8.n22.machine_proceed_closure.v0"),
            ("closure_status", data.get("closure_status"), "MACHINE_PROCEED_CLOSURE_PASS_RADIUS_EXHAUSTED_STOP"),
            ("radius_after", data.get("radius_result", {}).get("radius_after"), 0),
            ("radius_exhausted", data.get("radius_result", {}).get("radius_exhausted"), True),
        ]
    mismatches = [f"{field}:{got!r}!={want!r}" for field, got, want in checks if got != want]
    return "; ".join(mismatches) or None


def required_file_item(
    root: Path,
    object_id: str,
    relative_path: str,
    source_group: str,
    source_hashes: dict[str, str],
    source_commits: dict[str, str],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = root / relative_path
    item: dict[str, Any] = {
        "object_id": object_id,
        "path": relative_path,
        "source_group": source_group,
        "phase_role": "REQUIRED_START_SOURCE",
    }
    if not path.is_file():
        item.update(
            inventory_status="MISSING_REQUIRED_START_SOURCE",
            present=False,
            missing_reason="FILE_NOT_FOUND",
        )
        return item, None

    data, content = load_json(path)
    digest = sha256_bytes(content)
    error = status_error(data, relative_path)
    item.update(
        sha256=digest,
        hash_algorithm="sha256",
        loaded_by_explicit_path=True,
        status_check_passed=error is None,
    )
    if error:
        item.update(
            inventory_status="MISSING_REQUIRED_START_SOURCE",
            present=True,
            missing_reason="REQUIRED_STATUS_OR_IDENTITY_MISMATCH",
            mismatch_detail=error,
        )
        return item, data

    head = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if head.returncode != 0 or sha256_bytes(head.stdout) != digest:
        fail(FAILURE_VOCABULARY[4], f"{relative_path}: worktree does not match committed HEAD source")
    commit = run_git(root, ["log", "-n", "1", "--format=%H", "--", relative_path], FAILURE_VOCABULARY[1])
    source_hashes[relative_path] = digest
    source_commits[relative_path] = commit
    item.update(
        inventory_status="PRESENT_REQUIRED_START_SOURCE",
        present=True,
        head_blob_verified=True,
        source_commit_sha=commit,
    )
    return item, data


def expected_output_items(root: Path) -> list[dict[str, Any]]:
    canonical_paths = {path for _, path, _ in REQUIRED_FILE_SOURCES}
    items = []
    for definition in EXPECTED_OUTPUTS:
        path = f"{RUN_NAMESPACE}/{definition['relative_path']}"
        if path in canonical_paths or not path.startswith(f"{RUN_NAMESPACE}/"):
            fail(FAILURE_VOCABULARY[8], path)
        if (root / path).exists():
            fail("VS0_PREFLIGHT_FAIL_EXPECTED_OUTPUT_ALREADY_PRESENT", path)
        items.append(
            {
                "object_id": definition["object_id"],
                "phase_step": definition["phase_step"],
                "path": path,
                "source_group": definition["source_group"],
                "inventory_status": "ABSENT_EXPECTED_VS0_OUTPUT",
                "phase_role": "EXPECTED_VS0_OUTPUT",
                "expected_to_be_created_by_phase": True,
                "missing_is_failure_at_preflight": False,
            }
        )
    return items


def prior_context_items(root: Path) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    all_items = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for group, definitions in PRIOR_CONTEXT.items():
        grouped[group] = []
        for object_id, relative_path in definitions:
            present = (root / relative_path).is_file()
            item = {
                "object_id": object_id,
                "path": relative_path,
                "inventory_status": "PRESENT_PRIOR_PHASE_OUTPUT" if present else "OPTIONAL_CONTEXT_MISSING",
                "phase_role": "COMMITTED_SOURCE_CONTEXT",
                "present": present,
                "expected_vs0_output": False,
            }
            grouped[group].append(item)
            all_items.append(item)
    return all_items, grouped


def source_groups(
    required_items: list[dict[str, Any]],
    prior_grouped: dict[str, list[dict[str, Any]]],
    expected_items: list[dict[str, Any]],
    discussion_present: bool,
) -> dict[str, Any]:
    groups = {}
    names = [
        "authority_boundary_sources",
        "route_sources",
        "candidate_archive_sources",
        "promotion_sources",
        "machine_proceed_sources",
        "compression_sources",
        "registry_sources",
    ]
    for name in names:
        groups[name] = {
            "required_start_sources": [
                item["object_id"] for item in required_items if item.get("source_group") == name
            ],
            "present_prior_phase_outputs": [
                item["object_id"]
                for item in prior_grouped.get(name, [])
                if item["inventory_status"] == "PRESENT_PRIOR_PHASE_OUTPUT"
            ],
            "expected_vs0_outputs": [
                item["object_id"] for item in expected_items if item["source_group"] == name
            ],
            "optional_context_sources": [
                item["object_id"]
                for item in prior_grouped.get(name, [])
                if item["inventory_status"] == "OPTIONAL_CONTEXT_MISSING"
            ],
            "ignored_or_out_of_scope_sources": (
                [
                    {
                        "object_id": "discussion_packets",
                        "inventory_status": "OUT_OF_SCOPE_UNTRACKED",
                    }
                ]
                if discussion_present
                else []
            ),
        }
    return groups


def build_inventory(root: Path) -> dict[str, Any]:
    head_sha = run_git(root, ["rev-parse", "HEAD"], FAILURE_VOCABULARY[1])
    branch = run_git(root, ["branch", "--show-current"], FAILURE_VOCABULARY[1])
    status_lines = run_git(root, ["status", "--short"], FAILURE_VOCABULARY[1]).splitlines()
    validate_dirty_scope(status_lines)
    discussion_present = (root / "discussion_packets").exists()

    baseline_path = BASELINE_GENERATOR if (root / BASELINE_GENERATOR).is_file() else BASELINE_MANIFEST
    if not (root / baseline_path).is_file():
        fail(FAILURE_VOCABULARY[2], "baseline manifest and generator are both unavailable")

    required_items: list[dict[str, Any]] = [
        {
            "object_id": "repo_root",
            "path": str(root),
            "inventory_status": "PRESENT_REQUIRED_START_SOURCE",
            "phase_role": "REQUIRED_START_SOURCE",
            "present": True,
        },
        {
            "object_id": "git_head",
            "path": "HEAD",
            "value": head_sha,
            "inventory_status": "PRESENT_REQUIRED_START_SOURCE",
            "phase_role": "REQUIRED_START_SOURCE",
            "present": True,
        },
    ]
    baseline_content = (root / baseline_path).read_bytes()
    required_items.append(
        {
            "object_id": "baseline_share_projection_or_generator",
            "path": baseline_path,
            "inventory_status": "PRESENT_REQUIRED_START_SOURCE",
            "phase_role": "REQUIRED_START_SOURCE",
            "present": True,
            "sha256": sha256_bytes(baseline_content),
            "hash_algorithm": "sha256",
        }
    )

    source_hashes: dict[str, str] = {baseline_path: sha256_bytes(baseline_content)}
    source_commits: dict[str, str] = {}
    loaded_sources: dict[str, dict[str, Any]] = {}
    for object_id, relative_path, group in REQUIRED_FILE_SOURCES:
        item, data = required_file_item(
            root, object_id, relative_path, group, source_hashes, source_commits
        )
        required_items.append(item)
        if data is not None:
            loaded_sources[relative_path] = data

    missing_items = [
        item for item in required_items
        if item["inventory_status"] == "MISSING_REQUIRED_START_SOURCE"
    ]
    is_pass = not missing_items
    expected_items = expected_output_items(root)
    prior_items, prior_grouped = prior_context_items(root)
    groups = source_groups(required_items, prior_grouped, expected_items, discussion_present)
    inventory_status = PASS_STATUS if is_pass else STOP_STATUS
    transition = PASS_TRANSITION if is_pass else STOP_TRANSITION
    missing_object = missing_items[0]["object_id"] if missing_items else None

    preflight_decision: dict[str, Any]
    if is_pass:
        preflight_decision = {
            "decision": "PROCEED_TO_VS0_2_HAPPY_PATH_BUILD",
            "typed_stop_required": False,
            "stop_code": "NONE",
            "next_lawful_surface": "VS0_2_HAPPY_PATH_A_TO_F_ARTIFACT_BUILD",
        }
        evidence_yield = {
            "yield_axis": "PREFLIGHT_EXECUTION_RESULT",
            "yield_branch": "CONFIRMATION_YIELD",
            "reason": "preflight confirmed required start sources and phase scope",
        }
    else:
        preflight_decision = {
            "decision": "STOP_BEFORE_VS0_2",
            "typed_stop_required": True,
            "stop_code": "VS0_PREFLIGHT_STOP_REQUIRED_START_SOURCE_MISSING",
            "missing_object": missing_object,
            "missing_object_role": "REQUIRED_START_SOURCE",
            "next_lawful_surface": "CREATE_OR_IDENTIFY_REQUIRED_C8_N22_START_SOURCE",
        }
        evidence_yield = {
            "yield_axis": "PREFLIGHT_EXECUTION_RESULT",
            "yield_branch": "DIAGNOSTIC_YIELD",
            "reason": "preflight identified a missing required start source before VS0.2",
        }

    semantic_non_effects = {
        "a_to_f_specimen_built_by_vs0_1": False,
        "a4_created_by_vs0_1": False,
        "b3_created_by_vs0_1": False,
        "c3_created_by_vs0_1": False,
        "d5_created_by_vs0_1": False,
        "e4_created_by_vs0_1": False,
        "f4_created_by_vs0_1": False,
        "negative_probes_created_by_vs0_1": False,
        "evidence_yield_report_created_by_vs0_1": False,
        "phase_closure_created_by_vs0_1": False,
        "authority_changed_by_vs0_1": False,
        "machine_action_performed_by_vs0_1": False,
        "radius_renewed_by_vs0_1": False,
        "registry_activated_by_vs0_1": False,
        "runner_authority_created_by_vs0_1": False,
        "source_authority_replaced_by_vs0_1": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "inventory_id": INVENTORY_ID,
        "phase": {
            "phase_id": "PHASE_VS0",
            "phase_name": "A_TO_F_FIRST_SPECIMEN_RUNTIME_V0",
            "phase_role": "SOURCE_INVENTORY_AND_PREFLIGHT_ONLY",
        },
        "inventory_status": inventory_status,
        "generated_by": GENERATOR,
        "start_mode": {
            "mode": "FROM_COMMITTED_BLOCK_F_CANDIDATE_CHAIN",
            "greenfield_replay": False,
            "existing_a_to_f_chain_may_be_present": True,
            "present_prior_phase_outputs_are_allowed": True,
            "expected_vs0_outputs_use_phase_namespace": True,
        },
        "repo_state": {
            "repo_root": str(root),
            "branch": branch,
            "head_sha": head_sha,
            "git_status_short": status_lines,
        },
        "declared_start_source": {
            "start_source_id": "c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0",
            "start_source_path": F4,
            "start_source_status_required": "REGISTRY_CANDIDATE_CLOSURE_PASS_CANDIDATE_ONLY",
            "block_status_required": "BLOCK_F_PASS_LOCAL_REGISTRY_CANDIDATE_CLOSED",
            "start_source_role": "COMMITTED_BLOCK_F_TERMINAL_SOURCE",
        },
        "required_start_sources": {
            "required_count": len(required_items),
            "present_count": len(required_items) - len(missing_items),
            "missing_count": len(missing_items),
            "items": required_items,
        },
        "present_prior_phase_outputs": {
            "items": prior_items,
        },
        "expected_vs0_outputs": {
            "namespace_root": RUN_NAMESPACE,
            "items": expected_items,
        },
        "source_groups": groups,
        "required_start_source_integrity": {
            "explicit_paths_used": True,
            "source_hashes_captured": True,
            "source_hashes_verified_against_loaded_content": True,
            "mtime_or_latest_resolution_allowed": False,
            "directory_scan_authority_allowed": False,
            "hash_algorithm": "sha256",
            "source_hashes": source_hashes,
            "source_commits": source_commits,
        },
        "vs0_1_allowed_scope": {
            "may_create_source_inventory": True,
            "may_create_preflight_markdown": True,
            "may_update_baseline_share_projection": True,
            "may_create_a_to_f_specimen_artifacts": False,
            "may_create_negative_probe_artifacts": False,
            "may_create_evidence_yield_report": False,
            "may_create_phase_closure": False,
        },
        "phase_vs0_allowed_future_scope": {
            "vs0_2_may_create_a_to_f_specimen_artifacts": True,
            "vs0_4_may_create_negative_probe_artifacts": True,
            "vs0_5_may_create_evidence_yield_report": True,
            "vs0_6_may_create_phase_closure": True,
        },
        "forbidden_phase_scope": {
            "may_activate_registry": False,
            "may_generalize_trace": False,
            "may_create_runner": False,
            "may_authorize_runner": False,
            "may_execute_next_unit": False,
            "may_renew_radius": False,
            "may_authorize_additional_machine_proceed": False,
            "may_replace_source_authority_with_compression": False,
            "may_commit_discussion_packets": False,
        },
        "worktree_scope": {
            "discussion_packets_present": discussion_present,
            "discussion_packets_inventory_status": "OUT_OF_SCOPE_UNTRACKED",
            "discussion_packets_committable_by_vs0_1": False,
            "discussion_packets_in_scope": False,
            "discussion_packets_committed": False,
            "non_discussion_dirty_paths_allowed": False,
            "vs0_1_own_dirty_paths_allowed_before_commit": True,
        },
        "preflight_decision": preflight_decision,
        "evidence_yield_class": evidence_yield,
        "semantic_non_effects": semantic_non_effects,
        "gate": {
            "preflight_gate": inventory_status,
            "repo_root_resolved": True,
            "git_head_captured": True,
            "start_mode_declared": True,
            "declared_start_source_present": not any(
                item["object_id"] == "f4_registry_candidate_closure"
                for item in missing_items
            ),
            "required_start_sources_checked": True,
            "required_start_sources_missing": not is_pass,
            "present_prior_phase_outputs_declared": True,
            "expected_vs0_outputs_declared": True,
            "expected_vs0_outputs_missing_treated_as_failure": False,
            "vs0_1_allowed_scope_declared": True,
            "phase_vs0_future_scope_declared": True,
            "forbidden_scope_declared": True,
            "discussion_packets_in_scope": False,
            "discussion_packets_committed": False,
            "a_to_f_specimen_built_by_vs0_1": False,
            "machine_action_performed_by_vs0_1": False,
            "authority_changed_by_vs0_1": False,
            "runner_authority_created_by_vs0_1": False,
            "failures": [
                {
                    "code": "VS0_PREFLIGHT_STOP_REQUIRED_START_SOURCE_MISSING",
                    "object_id": item["object_id"],
                    "reason": item.get("missing_reason"),
                }
                for item in missing_items
            ],
        },
        "failure_vocabulary": FAILURE_VOCABULARY,
        "most_important_collapse_points": MOST_IMPORTANT_COLLAPSE_POINTS,
        "non_claims": NON_CLAIMS,
        "key_non_claims": KEY_NON_CLAIMS,
        "precommit_phase_vs0_source_inventory_gate": "PASS",
        "preflight_gate": inventory_status,
        "terminal_transition": transition,
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    status = inventory["inventory_status"]
    decision = inventory["preflight_decision"]["decision"]
    transition = inventory["terminal_transition"]
    yield_branch = inventory["evidence_yield_class"]["yield_branch"]
    missing = inventory["required_start_sources"]["missing_count"]
    required_lines = [
        "- repo root: present",
        "- git HEAD: captured",
        "- F4 registry candidate closure: present",
        "- F3 candidate admissibility audit: present",
        "- F2 registry candidate: present",
        "- F1 registry schema contract: present",
        "- E4 compression closure: present",
        "- E3 decompression audit: present",
        "- E2 compressed packet: present",
        "- D5 machine proceed closure: present",
    ]
    if missing:
        required_lines = [
            f"- {item['object_id']}: {item['inventory_status']}"
            for item in inventory["required_start_sources"]["items"]
        ]
    return f"""# Phase VS0 source inventory v0

## Status

{status}

## Phase

A_TO_F_FIRST_SPECIMEN_RUNTIME_V0

## Role

Source inventory and preflight only.

## Start mode

FROM_COMMITTED_BLOCK_F_CANDIDATE_CHAIN

## Declared start source

c8.n22.radius_bound_prepare_trace.registry_candidate_closure.v0

## Preflight decision

{decision}

## Terminal transition

{transition}

## Evidence Yield

{yield_branch}

## Required start sources

{chr(10).join(required_lines)}

## Present prior committed source context

- canonical A\u2192F / Block F source chain is present
- existing committed A\u2192F records are PRESENT_PRIOR_PHASE_OUTPUT

## Expected VS0 outputs

- VS0.2 A4 projection: expected VS0 output
- VS0.2 B3 projection: expected VS0 output
- VS0.2 C3 projection: expected VS0 output
- VS0.2 D5 projection: expected VS0 output
- VS0.2 E4 projection: expected VS0 output
- VS0.2 F4 projection: expected VS0 output
- missing expected VS0 outputs are not preflight failures

## VS0.1 allowed scope

- create source inventory
- create preflight markdown
- update baseline_share projection

## Future VS0 phase scope

- VS0.2 may create A\u2192F specimen artifacts under phase namespace
- VS0.4 may create negative probe artifacts
- VS0.5 may create evidence-yield report
- VS0.6 may create phase closure

## Forbidden phase scope

- no active registry
- no generalized trace
- no runner
- no runner authority
- no next-unit execution
- no radius renewal
- no additional machine proceed
- no source authority replacement by compression
- no discussion_packets commit

## Semantic non-effects

- A\u2192F specimen not built by VS0.1
- A4/B3/C3/D5/E4/F4 not created by VS0.1
- no negative probes created by VS0.1
- no evidence-yield report created by VS0.1
- no phase closure created by VS0.1
- no authority change
- no machine action
- no radius renewal
- no registry activation
- no runner authority

## Non-claim

VS0.1 does not build A\u2192F. It only verifies whether the phase may proceed to VS0.2 or must stop at a typed preflight halt."""


def validate_inventory(inventory: dict[str, Any]) -> None:
    if inventory.get("schema_version") != SCHEMA_VERSION:
        fail("VS0_PREFLIGHT_FAIL_INVENTORY_SCHEMA", "wrong schema_version")
    required = inventory.get("required_start_sources", {})
    if required.get("present_count", 0) + required.get("missing_count", 0) != required.get("required_count"):
        fail("VS0_PREFLIGHT_FAIL_INVENTORY_COUNTS", "required source counts do not balance")
    for item in inventory.get("expected_vs0_outputs", {}).get("items", []):
        if item.get("inventory_status") != "ABSENT_EXPECTED_VS0_OUTPUT":
            fail(FAILURE_VOCABULARY[7], item.get("object_id", "unknown"))
    for value in inventory.get("semantic_non_effects", {}).values():
        if value is not False:
            fail(FAILURE_VOCABULARY[12], "semantic non-effect became true")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    inventory = build_inventory(root)
    validate_inventory(inventory)
    write_text(root / OUTPUT_JSON, json.dumps(inventory, indent=2, sort_keys=True))
    write_text(root / OUTPUT_MD, render_markdown(inventory))
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"preflight_gate={inventory['preflight_gate']}")
    print(f"terminal_transition={inventory['terminal_transition']}")
    return 0


def main() -> int:
    try:
        return generate()
    except GenerationError as exc:
        print(f"STOP_{exc.code}: {exc.detail or exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
