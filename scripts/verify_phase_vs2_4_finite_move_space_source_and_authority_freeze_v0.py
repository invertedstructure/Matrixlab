#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path("/home/asd/projects/matrixlab")
HEAD = "99ed9ab2244c95d781ee709088839a79236f173b"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
HASH_ALG = "SHA-256"

F0_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.json"
F0_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_scope_regime_contract_v0.md"
O1_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.json"
O1_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_runtime_control_state_contract_v0.md"
O2_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.json"
O2_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_candidate_typed_state_contract_schema_v0.md"
O3_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.json"
O3_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_frozen_target_contract_v0.md"
M0_JSON = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.json"
M0_MD = "docs/matrixlabs/phase_vs2/object_model/phase_vs2_object_model_binding_manifest_v0.md"
VS2_3_RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json"

S0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.json"
S0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_source_and_version_binding_contract_v0.md"
V0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.json"
V0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_vocabulary_partition_v0.md"
A0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.json"
A0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_authority_matrix_v0.md"
MS0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.json"
MS0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_finite_move_space_v0.md"
P0_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.json"
P0_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_prospective_controlled_step_authority_envelope_v0.md"
M1_JSON = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.json"
M1_MD = "docs/matrixlabs/phase_vs2/move_space/phase_vs2_move_space_binding_manifest_v0.md"
RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_4_finite_move_space_source_and_authority_freeze_receipt_v0.json"

EXPECTED_RAW = {
    F0_JSON: "afda05e34228cc40a2bcd476105c1f6c0f747717db3a3d7e657fcec84c53ffb1",
    F0_MD: "bd787bdbaaf87da3b804659a99d5334f4603cce0a6e6cc75787eccf629fb76ae",
    O1_JSON: "944eead2d69a2690b9ad61cb93b288abb9a4f05d98e1f76d7012113bed7c975e",
    O1_MD: "bab3c65157cfbe22f9ae82b5005e6689abe49ca66dcff986ce4dcd6e47792d29",
    O2_JSON: "d2b0beb329b4caf56ef9569a4100fd6aff6b2f7df1fa67b1dff5087234f5d32a",
    O2_MD: "edac672e791e19e98cf9d762331f9cdca203b87feeb45138c53ab432834d94ee",
    O3_JSON: "6cc4952517fbb1718e3247c5465c60ba1281e390fc12c38485163b6e0d6b91eb",
    O3_MD: "483bd540ce9861ce5f8cb014a07d45c243ce1344a8f6e8d333f695e44f712401",
    M0_JSON: "2586a52032d91fb4addb4ae12facb421423fef0979083174f97f51cc1cabdf71",
    M0_MD: "98d8bf95cc335d441b6e4c6915e34c7930e6c7f59932d3d3a073dbfa92112def",
    VS2_3_RECEIPT_JSON: "04ec78427d317b127d4c7d0f1ec50e159f8b7385ff56d8470132eec22fb51ef0",
}
EXPECTED_CANONICAL = {
    F0_JSON: "a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179",
    O1_JSON: "25fbdfb007372e346d61a3f5de8b0a4f5004c6dff1857e5fc31df38e17c087ad",
    O2_JSON: "0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070",
    O3_JSON: "378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546",
    M0_JSON: "0af5f635aaca5c37428cc94ca1a8ee6f3885d6e56543198bbdd33a5d4062db3c",
    VS2_3_RECEIPT_JSON: "61a2298c0d04fa3acf47c391cc593df70be1d8e239e26de891d88b05ac879d0c",
}

MOVE_IDS = [
    "M01_ADD_AUTHORIZED_REQUIRED_FIELD",
    "M02_NORMALIZE_TYPED_VALUE",
    "M03_BIND_DECLARED_SOURCE_IDENTITY",
    "M04_BIND_DECLARED_SOURCE_FRESHNESS",
    "M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION",
    "M06_TIGHTEN_AMBIGUOUS_BOUNDARY",
    "M07_SPLIT_CONFLATED_DECLARATION",
    "M08_REJECT_UNSUPPORTED_CLAIM",
]
PARTITIONS = [
    "V1_TRANSFORMATION_MOVES",
    "V2_OBSERVATIONS",
    "V3_CONDITION_CLASSIFICATIONS",
    "V4_VALIDATION_RESULTS",
    "V5_CANDIDATE_ADMISSIBILITY_RESULTS",
    "V6_CONVERGENCE_RESULTS",
    "V7_TERMINAL_OUTCOMES",
]
TERMINAL_OUTCOMES = [
    "TARGET_REACHED",
    "STOP_REPAIR_NOT_LAWFUL",
    "STOP_MISSING_SOURCE",
    "STOP_MISSING_SCHEMA",
    "STOP_MISSING_AUTHORITY",
    "STOP_MISSING_CAPABILITY",
    "STOP_RADIUS_EXHAUSTED",
    "STOP_NO_ADMISSIBLE_MOVE",
    "STOP_VALIDATION_FAILED",
    "STOP_ADMISSIBILITY_FAILED",
    "STOP_FORBIDDEN_EFFECT_DETECTED",
    "STOP_SOURCE_IDENTITY_UNVERIFIED",
    "STOP_SCOPE_REGIME_VIOLATION",
    "STOP_NON_PROGRESS",
    "STOP_REPEATED_STATE",
    "STOP_CONVERGENCE_CRITERION_UNMET",
    "STOP_UNCLASSIFIED_RESULT_REQUIRES_TAXONOMY_REFINEMENT",
]
SEMANTIC_DOMAINS = {
    "contract_identity_declarations",
    "state_identity_declarations",
    "source_binding_declarations",
    "authority_declarations",
    "typed_field_declarations",
    "runtime_boundary_declarations",
    "halt_and_terminal_declarations",
    "receipt_declarations",
    "forbidden_effect_declarations",
    "claim_declarations",
}
FORBIDDEN_WRITE_TERMS = [
    "candidate_contract_id",
    "candidate_family",
    "candidate_version",
    "candidate_hash",
    "created_from_candidate_reference",
    "candidate_schema_reference",
    "profile_reference",
    "scope_regime_reference",
    "instance_origin_reference",
    "instance_source_snapshot_reference",
    "runtime authority package",
    "runtime budget",
    "move-space binding",
    "target-contract binding",
    "current validation status",
    "current admissibility status",
    "current convergence status",
    "pressure classification",
    "diagnostic state",
]
CORE_JSON = [S0_JSON, V0_JSON, A0_JSON, MS0_JSON, P0_JSON, M1_JSON, RECEIPT_JSON]
CORE_MD = [S0_MD, V0_MD, A0_MD, MS0_MD, P0_MD, M1_MD]
CORE = [S0_JSON, S0_MD, V0_JSON, V0_MD, A0_JSON, A0_MD, MS0_JSON, MS0_MD, P0_JSON, P0_MD, M1_JSON, M1_MD, RECEIPT_JSON]
FORBIDDEN_OUTPUT_FRAGMENTS = [
    "selector_priority",
    "applicator",
    "runtime_instance",
    "candidate_instance",
    "fixture_set",
    "exact_source_snapshot",
    "active_authority",
    "runtime_move_receipt",
    "runtime_terminal_receipt",
    "runner",
]


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_4_VERIFIER_INVARIANT") -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def stop(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_4_VERIFIER_INVARIANT") -> None:
    raise StopFailure(code, artifact, field, expected, observed, invariant)


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path: str) -> dict[str, Any]:
    if not (ROOT / path).exists():
        stop("STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", path, "path", "present", "missing")
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(observed: Any, expected: Any, code: str, artifact: str, field: str, invariant: str = "VALUE_MATCH") -> None:
    if observed != expected:
        stop(code, artifact, field, expected, observed, invariant)


def verify_upstream() -> None:
    require(git("rev-parse", "HEAD"), HEAD, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", "repo", "HEAD")
    for path, expected in EXPECTED_RAW.items():
        committed = git("show", f"{HEAD}:{path}", binary=True)
        current = (ROOT / path).read_bytes()
        require(current, committed, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, "committed_bytes")
        require(sha256_file(path), expected, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, "raw_sha256")
    artifacts = {
        F0_JSON: (load(F0_JSON), "contract_binding", "contract_payload", "contract_sha256"),
        O1_JSON: (load(O1_JSON), "contract_binding", "contract_payload", "contract_sha256"),
        O2_JSON: (load(O2_JSON), "schema_binding", "schema_payload", "schema_sha256"),
        O3_JSON: (load(O3_JSON), "target_contract_binding", "target_contract_payload", "target_contract_sha256"),
        M0_JSON: (load(M0_JSON), "manifest_binding", "manifest_payload", "manifest_sha256"),
        VS2_3_RECEIPT_JSON: (load(VS2_3_RECEIPT_JSON), "receipt_binding", "receipt_payload", "receipt_sha256"),
    }
    for path, (artifact, binding, payload_key, hash_key) in artifacts.items():
        digest = canonical_hash(artifact[binding][payload_key])
        require(digest, EXPECTED_CANONICAL[path], "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, hash_key)
        require(artifact[binding][hash_key], digest, "STOP_VS2_4_SCOPE_AND_OBJECT_MODEL_NOT_PASS", path, hash_key)
    m0_committed = git("show", f"{HEAD}:{M0_JSON}", binary=True)
    require((ROOT / M0_JSON).read_bytes(), m0_committed, "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M0_JSON, "committed_bytes")


def verify_binding(artifact: dict[str, Any], path: str, binding: str, payload_key: str, hash_key: str) -> str:
    payload = artifact[binding][payload_key]
    digest = canonical_hash(payload)
    require(artifact[binding]["canonicalization"], CANON, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "canonicalization")
    require(artifact[binding][hash_key], digest, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, hash_key)
    return digest


def verify_reference(row: dict[str, Any], path: str) -> None:
    required = [
        "reference_id",
        "reference_role",
        "binding_status",
        "expected_artifact_kind",
        "required_by_unit",
        "artifact_id",
        "artifact_kind",
        "artifact_version",
        "declared_path",
        "content_sha256",
        "hash_algorithm",
        "canonicalization_rule",
        "binding_reason",
    ]
    for key in required:
        if key not in row:
            stop("STOP_VS2_4_FAKE_OR_PREBOUND_AUTHORITY_REFERENCE", path, f"reference.{key}", "present", "missing")
    if row["binding_status"] == "BOUND":
        for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256"]:
            if row[key] is None:
                stop("STOP_VS2_4_FAKE_OR_PREBOUND_AUTHORITY_REFERENCE", path, key, "non-null", None)
        require(row["hash_algorithm"], HASH_ALG, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "hash_algorithm")
        require(row["canonicalization_rule"], CANON, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", path, "canonicalization_rule")
    else:
        for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256", "hash_algorithm", "canonicalization_rule"]:
            require(row[key], None, "STOP_VS2_4_FAKE_OR_PREBOUND_AUTHORITY_REFERENCE", path, f"{row['reference_id']}.{key}")


def verify_move(move: dict[str, Any]) -> None:
    payload = move["move_contract_payload"]
    move_id = move["move_id"]
    require(payload["move_id"], move_id, "STOP_VS2_4_MOVE_CONTRACT_INCOMPLETE", MS0_JSON, f"{move_id}.move_id")
    require(canonical_hash(payload), move["move_contract_sha256"], "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", MS0_JSON, f"{move_id}.move_contract_sha256")
    require(payload["move_version"], "v0", "STOP_VS2_4_MOVE_CONTRACT_INCOMPLETE", MS0_JSON, f"{move_id}.move_version")
    require(payload["move_class"], "TRANSFORMATION_MOVE", "STOP_VS2_4_MOVE_CONTRACT_INCOMPLETE", MS0_JSON, f"{move_id}.move_class")
    require(payload["move_status"], "FROZEN_NOT_ACTIVE", "STOP_VS2_4_ACTIVE_EXECUTION_AUTHORITY_PRESENT", MS0_JSON, f"{move_id}.move_status")
    require(payload["runtime_authority_status"], "PROSPECTIVE_AUTHORITY_REQUIRED_NOT_ACTIVE", "STOP_VS2_4_ACTIVE_EXECUTION_AUTHORITY_PRESENT", MS0_JSON, f"{move_id}.runtime_authority_status")
    for key in [
        "operand_contract",
        "structural_applicability_preconditions",
        "target_rule_requirements",
        "capability_requirements",
        "prospective_authority_requirements",
        "runtime_authorization_requirements",
        "budget_cost",
        "delta_contract",
        "receipt_obligations",
        "forbidden_effects",
        "possible_terminal_outcomes",
    ]:
        if key not in payload:
            stop("STOP_VS2_4_MOVE_CONTRACT_INCOMPLETE", MS0_JSON, f"{move_id}.{key}", "present", "missing")
    require(payload["budget_cost"], 1, "STOP_VS2_4_MOVE_BUDGET_COST_MISSING", MS0_JSON, f"{move_id}.budget_cost")
    require(payload["possible_terminal_outcomes"], TERMINAL_OUTCOMES, "STOP_VS2_4_TERMINAL_OUTCOME_FAMILY_DRIFT", MS0_JSON, f"{move_id}.possible_terminal_outcomes")
    for template in payload["candidate_write_path_templates"]:
        domain = template.split(".", 1)[0]
        if domain not in SEMANTIC_DOMAINS:
            stop("STOP_VS2_4_MOVE_CAN_MUTATE_FORBIDDEN_OBJECT_OR_PATH", MS0_JSON, f"{move_id}.candidate_write_path_templates", "O2 semantic domain", template)
        lowered = template.lower()
        for term in FORBIDDEN_WRITE_TERMS:
            if term in lowered:
                stop("STOP_VS2_4_MOVE_CAN_WRITE_EVALUATOR_STATE", MS0_JSON, f"{move_id}.candidate_write_path_templates", "no forbidden term", template)
    forbidden_text = json.dumps(payload["forbidden_effects"], sort_keys=True)
    for expected in ["mutate F0", "mutate O3", "mutate M0", "mutate MS0", "grant authority", "acquire source", "write evaluator state"]:
        if expected not in forbidden_text:
            stop("STOP_VS2_4_MOVE_FORBIDDEN_EFFECTS_MISSING", MS0_JSON, f"{move_id}.forbidden_effects", expected, "missing")
    if payload["capability_requirements"][0].get("capability_id") is None:
        stop("STOP_VS2_4_MOVE_CAPABILITY_REQUIREMENT_MISSING", MS0_JSON, f"{move_id}.capability_requirements", "explicit capability or NONE_REQUIRED", payload["capability_requirements"])


def verify_pending_counts(rows: list[dict[str, Any]], count: int, pending: int, absent: int, path: str) -> None:
    require(len(rows), count, "STOP_VS2_4_CONTROLLED_STEP_COMPONENT_PRECONSUMED", path, "binding_count")
    require(sum(1 for row in rows if row["binding_status"] == "PENDING"), pending, "STOP_VS2_4_CONTROLLED_STEP_COMPONENT_PRECONSUMED", path, "pending_count")
    require(sum(1 for row in rows if row["binding_status"] == "ABSENT_BY_POLICY"), absent, "STOP_VS2_4_ACTIVE_EXECUTION_AUTHORITY_PRESENT", path, "absent_count")
    for row in rows:
        verify_reference(row, path)


def verify_forbidden_outputs() -> None:
    allowed = {Path(path) for path in CORE}
    for path in (ROOT / "docs/matrixlabs/phase_vs2").rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        rel_s = str(rel)
        if Path(rel_s) in allowed:
            continue
        if rel_s in EXPECTED_RAW or "phase_vs2_first_sweep_capable_kernel_profile" in rel_s or "phase_vs2_typed_state_contract_convergence_target_freeze" in rel_s:
            continue
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in path.name:
                stop("STOP_VS2_4_EXECUTION_OR_FIXTURE_DRIFT", rel_s, "forbidden_output", "absent", "present")
    if (ROOT / "discussion_packets").exists():
        stop("STOP_VS2_4_EXECUTION_OR_FIXTURE_DRIFT", "discussion_packets", "forbidden_output", "absent", "present")


def main() -> int:
    try:
        verify_upstream()
        s0 = load(S0_JSON)
        v0 = load(V0_JSON)
        a0 = load(A0_JSON)
        ms0 = load(MS0_JSON)
        p0 = load(P0_JSON)
        m1 = load(M1_JSON)
        receipt = load(RECEIPT_JSON)

        s0_sha = verify_binding(s0, S0_JSON, "contract_binding", "contract_payload", "contract_sha256")
        v0_sha = verify_binding(v0, V0_JSON, "partition_binding", "partition_payload", "partition_sha256")
        a0_sha = verify_binding(a0, A0_JSON, "matrix_binding", "matrix_payload", "matrix_sha256")
        ms0_sha = verify_binding(ms0, MS0_JSON, "move_space_binding", "move_space_payload", "move_space_sha256")
        p0_sha = verify_binding(p0, P0_JSON, "envelope_binding", "envelope_payload", "envelope_sha256")
        m1_sha = verify_binding(m1, M1_JSON, "manifest_binding", "manifest_payload", "manifest_sha256")
        receipt_sha = verify_binding(receipt, RECEIPT_JSON, "receipt_binding", "receipt_payload", "receipt_sha256")

        require(s0["contract_status"], "FROZEN_EXACT_SOURCE_SNAPSHOT_PENDING", "STOP_VS2_4_SOURCE_AND_VERSION_BINDING_CONTRACT_INCOMPLETE", S0_JSON, "contract_status")
        require(s0["exact_source_snapshot_frozen"], False, "STOP_VS2_4_SOURCE_SNAPSHOT_PREMATURELY_FROZEN", S0_JSON, "exact_source_snapshot_frozen")
        if "latest-file resolution" not in s0["forbidden_resolution_methods"]:
            stop("STOP_VS2_4_SOURCE_RESOLUTION_METHOD_UNAUTHORIZED", S0_JSON, "forbidden_resolution_methods", "latest-file resolution", "missing")
        verify_reference(s0["pending_exact_source_snapshot_reference"], S0_JSON)

        require(v0["partition_count"], 7, "STOP_VS2_4_VOCABULARY_PARTITION_COLLISION", V0_JSON, "partition_count")
        require(list(v0["partitions"].keys()), PARTITIONS, "STOP_VS2_4_VOCABULARY_PARTITION_COLLISION", V0_JSON, "partitions")
        require(v0["move_catalog"]["ordered_move_ids"], MOVE_IDS, "STOP_VS2_4_MOVE_CATALOG_MISMATCH", V0_JSON, "ordered_move_ids")
        require(v0["move_catalog"]["dynamic_move_creation_allowed"], False, "STOP_VS2_4_DYNAMIC_MOVE_CREATION_ALLOWED", V0_JSON, "dynamic_move_creation_allowed")
        ids = [row["identifier"] for rows in v0["partitions"].values() for row in rows]
        require(len(ids), len(set(ids)), "STOP_VS2_4_MOVE_ID_DUPLICATED", V0_JSON, "global_identifier_uniqueness")
        require([row["identifier"] for row in v0["partitions"]["V7_TERMINAL_OUTCOMES"]], TERMINAL_OUTCOMES, "STOP_VS2_4_TERMINAL_OUTCOME_FAMILY_DRIFT", V0_JSON, "terminal_outcomes")
        if "STOP_BUDGET_EXHAUSTED" in ids:
            stop("STOP_VS2_4_TERMINAL_OUTCOME_FAMILY_DRIFT", V0_JSON, "STOP_BUDGET_EXHAUSTED", "absent", "present")

        require(len(a0["move_authority_rows"]), 8, "STOP_VS2_4_MOVE_CONTRACT_INCOMPLETE", A0_JSON, "row_count")
        for row in a0["move_authority_rows"]:
            require(row["structural_applicability_requires_active_authority"], False, "STOP_VS2_4_APPLICABILITY_AND_AUTHORITY_CONFLATED", A0_JSON, row["move_id"])
            require(row["authority_status"], "FROZEN_NOT_ACTIVE", "STOP_VS2_4_ACTIVE_EXECUTION_AUTHORITY_PRESENT", A0_JSON, row["move_id"])

        require(ms0["move_count"], 8, "STOP_VS2_4_MOVE_SPACE_NOT_FINITE", MS0_JSON, "move_count")
        require(ms0["ordered_move_ids"], MOVE_IDS, "STOP_VS2_4_MOVE_CATALOG_MISMATCH", MS0_JSON, "ordered_move_ids")
        require(ms0["closure_law"]["dynamic_move_creation_allowed"], False, "STOP_VS2_4_DYNAMIC_MOVE_CREATION_ALLOWED", MS0_JSON, "dynamic_move_creation_allowed")
        require(ms0["closure_law"]["move_space_active"], False, "STOP_VS2_4_ACTIVE_EXECUTION_AUTHORITY_PRESENT", MS0_JSON, "move_space_active")
        require("content_sha256" in json.dumps(ms0["prospective_authority_envelope_identity"], sort_keys=True), False, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", MS0_JSON, "P0_hash_bound")
        moves = ms0["move_contracts"]
        require([move["move_id"] for move in moves], MOVE_IDS, "STOP_VS2_4_MOVE_CATALOG_MISMATCH", MS0_JSON, "move_contract_order")
        for move in moves:
            verify_move(move)
        require(ms0["move_contract_hashes"], {move["move_id"]: move["move_contract_sha256"] for move in moves}, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", MS0_JSON, "move_contract_hashes")
        m05 = next(move["move_contract_payload"] for move in moves if move["move_id"] == "M05_REMOVE_PROHIBITED_CANDIDATE_DECLARATION")
        m08 = next(move["move_contract_payload"] for move in moves if move["move_id"] == "M08_REJECT_UNSUPPORTED_CLAIM")
        if "claim_declarations" not in m05.get("excluded_domains", []):
            stop("STOP_VS2_4_PROHIBITED_DECLARATION_AND_CLAIM_REJECTION_CONFLATED", MS0_JSON, "M05.excluded_domains", "claim_declarations", m05.get("excluded_domains"))
        if "claim_declarations.declared_supported_claims" not in m08["candidate_write_path_templates"]:
            stop("STOP_VS2_4_PROHIBITED_DECLARATION_AND_CLAIM_REJECTION_CONFLATED", MS0_JSON, "M08.claim_paths", "present", m08["candidate_write_path_templates"])

        require(p0["envelope_active"], False, "STOP_VS2_4_AUTHORITY_ENVELOPE_MARKED_ACTIVE", P0_JSON, "envelope_active")
        require(p0["prospective_authority_envelope_active"], False, "STOP_VS2_4_AUTHORITY_ENVELOPE_MARKED_ACTIVE", P0_JSON, "prospective_authority_envelope_active")
        verify_pending_counts(p0["authority_bindings"], 7, 5, 2, P0_JSON)
        require(p0["finite_move_space_reference"]["content_sha256"], ms0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", P0_JSON, "MS0_hash")
        scope = p0["maximum_prospective_scope"]
        if scope["applied_moves_per_case_maximum"] > scope["attempted_moves_per_case_maximum"]:
            stop("STOP_VS2_4_AUTHORITY_ENVELOPE_UNBOUNDED", P0_JSON, "applied_moves_per_case_maximum", "<= attempted", scope)
        if scope["total_applied_moves_maximum"] > scope["total_attempted_moves_maximum"]:
            stop("STOP_VS2_4_AUTHORITY_ENVELOPE_UNBOUNDED", P0_JSON, "total_applied_moves_maximum", "<= attempted", scope)

        require(m1["manifest_mutable"], False, "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M1_JSON, "manifest_mutable")
        require(m1["predecessor_object_model_manifest_reference"]["content_sha256"], EXPECTED_CANONICAL[M0_JSON], "STOP_VS2_4_M0_REWRITTEN_OR_SUCCESSOR_MANIFEST_MISSING", M1_JSON, "M0_hash")
        require(m1["source_and_version_binding_contract_reference"]["content_sha256"], s0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M1_JSON, "S0_hash")
        require(m1["vocabulary_partition_reference"]["content_sha256"], v0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M1_JSON, "V0_hash")
        require(m1["move_authority_matrix_reference"]["content_sha256"], a0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M1_JSON, "A0_hash")
        require(m1["finite_move_space_reference"]["content_sha256"], ms0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M1_JSON, "MS0_hash")
        require(m1["prospective_authority_envelope_reference"]["content_sha256"], p0_sha, "STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", M1_JSON, "P0_hash")
        verify_pending_counts(m1["pending_downstream_bindings"], 17, 15, 2, M1_JSON)
        require(m1["downstream_binding_summary"]["fabricated_future_reference_count"], 0, "STOP_VS2_4_FAKE_OR_PREBOUND_AUTHORITY_REFERENCE", M1_JSON, "fabricated_future_reference_count")

        payload = receipt["receipt_binding"]["receipt_payload"]
        require(payload["receipt_gate"], "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS", "STOP_VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_PASS", RECEIPT_JSON, "receipt_gate")
        require(payload["construction_authority"]["bounded_construction_consumption_count_before"], 1, "STOP_VS2_4_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", RECEIPT_JSON, "count_before")
        require(payload["construction_authority"]["bounded_construction_consumption_count_after"], 1, "STOP_VS2_4_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", RECEIPT_JSON, "count_after")
        require(payload["construction_authority"]["additional_bounded_construction_grant_consumption_by_vs2_4"], False, "STOP_VS2_4_CONSTRUCTION_GRANT_RECONSUMPTION_ATTEMPT", RECEIPT_JSON, "additional_consumption")
        require(payload["post_state"]["move_selected"], False, "STOP_VS2_4_MOVE_SELECTED", RECEIPT_JSON, "move_selected")
        require(payload["post_state"]["move_applied"], False, "STOP_VS2_4_MOVE_APPLIED", RECEIPT_JSON, "move_applied")
        require(payload["post_state"]["runtime_instance_created"], False, "STOP_VS2_4_RUNTIME_INSTANCE_PREMATURELY_CREATED", RECEIPT_JSON, "runtime_instance_created")
        require(payload["post_state"]["candidate_instance_created"], False, "STOP_VS2_4_CANDIDATE_INSTANCE_PREMATURELY_CREATED", RECEIPT_JSON, "candidate_instance_created")
        require(payload["post_state"]["fixture_instance_created"], False, "STOP_VS2_4_CANDIDATE_FIXTURE_PREMATURELY_CREATED", RECEIPT_JSON, "fixture_instance_created")
        require(payload["logical_terminal_transition"], "ADVANCE(VS2_5_CONTROLLED_STEP_AND_CONVERGENCE_CONTRACT_CONSTRUCTION_PENDING)", "STOP_VS2_4_NEXT_UNIT_AUTO_EXECUTED", RECEIPT_JSON, "logical_terminal_transition")

        for md, digest in [(S0_MD, s0_sha), (V0_MD, v0_sha), (A0_MD, a0_sha), (MS0_MD, ms0_sha), (P0_MD, p0_sha), (M1_MD, m1_sha)]:
            text = (ROOT / md).read_text(encoding="utf-8")
            if digest not in text:
                stop("STOP_VS2_4_HASH_GRAPH_OR_CANONICALIZATION_INVALID", md, "markdown_canonical_hash", digest, "missing")

        verify_forbidden_outputs()
        raw_hashes = {path: sha256_file(path) for path in CORE}
        print(json.dumps({
            "vs2_4_verifier_gate": "PASS",
            "source_and_version_binding_contract_sha256": s0_sha,
            "move_vocabulary_partition_sha256": v0_sha,
            "move_authority_matrix_sha256": a0_sha,
            "finite_move_space_sha256": ms0_sha,
            "prospective_authority_envelope_sha256": p0_sha,
            "move_space_binding_manifest_sha256": m1_sha,
            "receipt_sha256": receipt_sha,
            "move_hashes": {move["move_id"]: move["move_contract_sha256"] for move in moves},
            "raw_hashes_calculated": raw_hashes,
        }, indent=2, sort_keys=True))
        return 0
    except StopFailure as exc:
        print(json.dumps({
            "vs2_4_verifier_gate": "STOP",
            "failure_code": exc.code,
            "failed_artifact": exc.artifact,
            "failed_move_or_field": exc.field,
            "expected_value": exc.expected,
            "observed_value": exc.observed,
            "violated_invariant": exc.invariant,
            "violated_authority_boundary": "VS2_4_FINITE_MOVE_SPACE_SOURCE_AND_AUTHORITY_FREEZE_ONLY",
            "blocked_downstream_unit": "VS2.4",
            "exact_bounded_correction_surface": "VS2_4_REPAIR_OR_BOOKKEEPING_SURFACE",
            "capability_proposal_candidate_required": False,
            "human_decision_required": False,
            "self_repair_performed": False,
        }, indent=2, sort_keys=True, default=str))
        return 1


if __name__ == "__main__":
    sys.exit(main())
