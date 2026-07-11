#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path("/home/asd/projects/matrixlab")
HEAD = "007244b3483464f76b91141ca47c85457e7f0bf1"
CANON = "MATRIXLAB_CANONICAL_JSON_V0"
PROFILE_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.json"
PROFILE_MD_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_first_sweep_capable_kernel_profile_v0.md"
TARGET_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.json"
TARGET_MD_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_typed_state_contract_convergence_target_freeze_v0.md"
UPSTREAM_RECEIPT_PATH = "docs/matrixlabs/phase_vs2/phase_vs2_2_kernel_profile_and_target_freeze_receipt_v0.json"
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
RECEIPT_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_3_scope_regime_and_three_object_model_definition_receipt_v0.json"

EXPECTED_RAW = {
    PROFILE_PATH: "2d61b8f7aaa11c10416ffbf2097f4ff95069d5131a99b63b8d1728485e7cf96b",
    PROFILE_MD_PATH: "42bbfeb1a77df4ed6f1c624dbd88e4a319b85c1aedf1325a66b7f6187d32c592",
    TARGET_PATH: "5e31db512163961034c98790a762036afa1730d57c7cf7346f5e9f7260ec985a",
    TARGET_MD_PATH: "ad0a852e157c1b75043cdaa4ab1e58def1bb17289f88386b0046c3764f8d181b",
    UPSTREAM_RECEIPT_PATH: "a6a57810854215f912cb2251dbda277eb6bf8f110cd79371af615908497cc833",
}
PROFILE_SHA = "844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142"
TARGET_SHA = "518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8"
UPSTREAM_RECEIPT_SHA = "9e17272877e96f9db6885334e2531df8be8fdd7bb2d501d853c393b8f16ce425"
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
CORE_JSON = [F0_JSON, O1_JSON, O2_JSON, O3_JSON, M0_JSON, RECEIPT_JSON]
CORE_MD = [F0_MD, O1_MD, O2_MD, O3_MD, M0_MD]


class StopFailure(RuntimeError):
    def __init__(self, code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str) -> None:
        super().__init__(code)
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        self.invariant = invariant


def stop(code: str, artifact: str, field: str, expected: Any, observed: Any, invariant: str = "VS2_3_VERIFIER_INVARIANT") -> None:
    raise StopFailure(code, artifact, field, expected, observed, invariant)


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=not binary)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, ["git", *args], result.stdout, result.stderr)
    return result.stdout if binary else result.stdout.strip()


def load(path: str) -> dict[str, Any]:
    if not (ROOT / path).exists():
        stop("STOP_VS2_3_BINDING_MANIFEST_MISSING", path, "path", "present", "missing")
    return json.loads((ROOT / path).read_text())


def require(observed: Any, expected: Any, code: str, artifact: str, field: str, invariant: str = "VALUE_MATCH") -> None:
    if observed != expected:
        stop(code, artifact, field, expected, observed, invariant)


def require_false(observed: Any, code: str, artifact: str, field: str, invariant: str = "FALSE_REQUIRED") -> None:
    if observed is not False:
        stop(code, artifact, field, False, observed, invariant)


def verify_upstream() -> None:
    require(git("rev-parse", "HEAD"), HEAD, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", "repo", "HEAD")
    for path, expected in EXPECTED_RAW.items():
        committed = git("show", f"{HEAD}:{path}", binary=True)
        current = (ROOT / path).read_bytes()
        require(current, committed, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", path, "committed_bytes")
        require(sha256_file(path), expected, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", path, "raw_sha256")
    profile = load(PROFILE_PATH)
    target = load(TARGET_PATH)
    receipt = load(UPSTREAM_RECEIPT_PATH)
    require(canonical_hash(profile["profile_binding"]["profile_payload"]), PROFILE_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", PROFILE_PATH, "profile_sha256")
    require(canonical_hash(target["target_freeze_binding"]["target_freeze_payload"]), TARGET_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", TARGET_PATH, "target_sha256")
    require(canonical_hash(receipt["receipt_binding"]["receipt_payload"]), UPSTREAM_RECEIPT_SHA, "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "receipt_sha256")
    require(receipt["logical_downstream_transition"], "ADVANCE(VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_DEFINITION_PENDING)", "STOP_VS2_3_KERNEL_PROFILE_AND_TARGET_FREEZE_NOT_PASS", UPSTREAM_RECEIPT_PATH, "logical_downstream_transition")


def binding_hash(artifact: dict[str, Any], binding: str, payload_key: str, hash_key: str, code: str, path: str) -> str:
    payload = artifact[binding][payload_key]
    digest = canonical_hash(payload)
    require(digest, artifact[binding][hash_key], code, path, hash_key, "HASH_AND_CANONICALIZATION_INVARIANT")
    return digest


def verify_reference_shape(row: dict[str, Any], path: str) -> None:
    if row["binding_status"] == "BOUND":
        for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256", "canonicalization_rule"]:
            if row.get(key) is None:
                stop("STOP_VS2_3_FAKE_PENDING_REFERENCE_EMITTED", path, f"BOUND.{key}", "non-null", None, "REFERENCE_CONTRACT")
        require(row["hash_algorithm"], "SHA-256", "STOP_VS2_3_HASH_CANONICALIZATION_RULE_MISSING", path, "hash_algorithm")
    else:
        for key in ["artifact_id", "artifact_kind", "artifact_version", "declared_path", "content_sha256"]:
            if row.get(key) is not None:
                stop("STOP_VS2_3_FAKE_PENDING_REFERENCE_EMITTED", path, f"{row['binding_status']}.{key}", None, row.get(key), "REFERENCE_CONTRACT")


def verify_markdown(path: str, digest: str) -> None:
    text = (ROOT / path).read_text()
    if digest not in text:
        stop("STOP_VS2_3_HASH_CANONICALIZATION_RULE_MISSING", path, "markdown canonical hash", digest, "missing")


def main() -> int:
    try:
        verify_upstream()
        f0 = load(F0_JSON)
        o1 = load(O1_JSON)
        o2 = load(O2_JSON)
        o3 = load(O3_JSON)
        m0 = load(M0_JSON)
        receipt = load(RECEIPT_JSON)

        f0_sha = binding_hash(f0, "contract_binding", "contract_payload", "contract_sha256", "STOP_VS2_3_SCOPE_REGIME_FRAME_INCOMPLETE", F0_JSON)
        o1_sha = binding_hash(o1, "contract_binding", "contract_payload", "contract_sha256", "STOP_VS2_3_RUNTIME_STATE_CONTRACT_MISSING", O1_JSON)
        o2_sha = binding_hash(o2, "schema_binding", "schema_payload", "schema_sha256", "STOP_VS2_3_CANDIDATE_CONTRACT_SCHEMA_MISSING", O2_JSON)
        o3_sha = binding_hash(o3, "target_contract_binding", "target_contract_payload", "target_contract_sha256", "STOP_VS2_3_FROZEN_TARGET_CONTRACT_MISSING", O3_JSON)
        m0_sha = binding_hash(m0, "manifest_binding", "manifest_payload", "manifest_sha256", "STOP_VS2_3_BINDING_MANIFEST_MISSING", M0_JSON)
        receipt_sha = canonical_hash(receipt["receipt_binding"]["receipt_payload"])
        require(receipt_sha, receipt["receipt_binding"]["receipt_sha256"], "STOP_VS2_3_HASH_CANONICALIZATION_RULE_MISSING", RECEIPT_JSON, "receipt_sha256")

        require(f0["immutability_contract"]["frame_mutable"], False, "STOP_VS2_3_SCOPE_REGIME_MUTABILITY_PRESENT", F0_JSON, "frame_mutable")
        require(f0["allowed_execution_domain_object_roles"], ["RUNTIME_CONTROL_STATE", "CANDIDATE_TYPED_STATE_CONTRACT", "FROZEN_TARGET_CONTRACT"], "STOP_VS2_3_OBJECT_ROLE_COUNT_INVALID", F0_JSON, "allowed_roles")
        require(f0["object_identity_rules"]["execution_domain_object_role_count"], 3, "STOP_VS2_3_OBJECT_ROLE_COUNT_INVALID", F0_JSON, "role_count")
        require(f0["object_identity_rules"]["additional_mutable_execution_domain_object_count"], 0, "STOP_VS2_3_OBJECT_ROLE_COUNT_INVALID", F0_JSON, "additional_mutable")

        require(o2["candidate_instance_created"], False, "STOP_VS2_3_CANDIDATE_INSTANCE_PREMATURELY_CREATED", O2_JSON, "candidate_instance_created")
        require(o2["fixture_instance_created"], False, "STOP_VS2_3_FIXTURE_INSTANCE_PREMATURELY_CREATED", O2_JSON, "fixture_instance_created")
        require(set(o2["potentially_mutable_domains"]), set([
            "contract_identity_declarations", "state_identity_declarations", "source_binding_declarations", "authority_declarations", "typed_field_declarations", "runtime_boundary_declarations", "halt_and_terminal_declarations", "receipt_declarations", "forbidden_effect_declarations", "claim_declarations"
        ]), "STOP_VS2_3_UNBOUNDED_CANDIDATE_MUTATION_DOMAIN", O2_JSON, "potentially_mutable_domains")
        for forbidden in ["define executable moves", "alter O3", "alter the move-space"]:
            if forbidden not in o2["forbidden_content"]:
                stop("STOP_VS2_3_MUTATION_BOUNDARY_INCOMPLETE", O2_JSON, "forbidden_content", forbidden, "missing")

        require(o3["target_mutable"], False, "STOP_VS2_3_TARGET_MUTABILITY_PRESENT", O3_JSON, "target_mutable")
        require(o3["terminal_outcome_family"]["terminal_outcomes"], TERMINAL_OUTCOMES, "STOP_VS2_3_TERMINAL_OUTCOME_FAMILY_DRIFT", O3_JSON, "terminal_outcomes")
        require(o3["terminal_outcome_family"]["terminal_outcome_count"], 17, "STOP_VS2_3_TERMINAL_OUTCOME_FAMILY_DRIFT", O3_JSON, "terminal_outcome_count")
        require(o3["semantic_target_satisfaction_conditions"]["runtime_terminal_result_emitted"], False, "STOP_VS2_3_TARGET_CONFORMANCE_TERMINALIZATION_CONFLATED", O3_JSON, "runtime_terminal_result_emitted")
        require(o3["candidate_mutation_requirements"]["candidate_can_modify_target"], False, "STOP_VS2_3_CANDIDATE_CAN_MODIFY_TARGET", O3_JSON, "candidate_can_modify_target")
        require(o3["candidate_mutation_requirements"]["candidate_can_modify_move_space"], False, "STOP_VS2_3_CANDIDATE_CAN_MODIFY_MOVE_SPACE", O3_JSON, "candidate_can_modify_move_space")
        require(o3["candidate_mutation_requirements"]["candidate_can_modify_scope_regime"], False, "STOP_VS2_3_CANDIDATE_CAN_MODIFY_SCOPE_REGIME", O3_JSON, "candidate_can_modify_scope_regime")

        require(o1["runtime_instance_created"], False, "STOP_VS2_3_RUNTIME_INSTANCE_PREMATURELY_CREATED", O1_JSON, "runtime_instance_created")
        if "TARGET_REACHED" in o1["allowed_loop_positions"]:
            stop("STOP_VS2_3_TARGET_CONFORMANCE_TERMINALIZATION_CONFLATED", O1_JSON, "loop_positions", "TARGET_REACHED absent", o1["allowed_loop_positions"])
        for forbidden in ["self-generated moves", "fixture content", "runner authority"]:
            if forbidden not in o1["forbidden_content"]:
                stop("STOP_VS2_3_MOVE_OR_EXECUTION_DRIFT", O1_JSON, "forbidden_content", forbidden, "missing")

        require(m0["manifest_mutable"], False, "STOP_VS2_3_BINDING_MANIFEST_MUTABILITY_PRESENT", M0_JSON, "manifest_mutable")
        downstream = m0["pending_downstream_bindings"]
        require(len(downstream), 19, "STOP_VS2_3_DOWNSTREAM_COMPONENT_PRECONSUMED", M0_JSON, "downstream_binding_count")
        require(sum(1 for row in downstream if row["binding_status"] == "PENDING"), 18, "STOP_VS2_3_DOWNSTREAM_COMPONENT_PRECONSUMED", M0_JSON, "pending_binding_count")
        require(sum(1 for row in downstream if row["binding_status"] == "ABSENT_BY_POLICY"), 1, "STOP_VS2_3_EXECUTION_AUTHORITY_PRESENT", M0_JSON, "absent_by_policy_count")
        for row in downstream:
            verify_reference_shape(row, M0_JSON)
        require(m0["downstream_binding_summary"]["fabricated_future_reference_count"], 0, "STOP_VS2_3_FAKE_PENDING_REFERENCE_EMITTED", M0_JSON, "fabricated_future_reference_count")
        require(len(m0["cross_object_invariants"]), 18, "STOP_VS2_3_CROSS_OBJECT_IDENTITY_INVARIANT_INCOMPLETE", M0_JSON, "cross_object_invariant_count")
        for row in m0["cross_object_invariants"]:
            require(row["verification_status"], "VERIFIED_AT_VS2_3_CONSTRUCTION", "STOP_VS2_3_CROSS_OBJECT_IDENTITY_INVARIANT_INCOMPLETE", M0_JSON, row["invariant_id"])

        for path, digest in [(F0_MD, f0_sha), (O1_MD, o1_sha), (O2_MD, o2_sha), (O3_MD, o3_sha), (M0_MD, m0_sha)]:
            verify_markdown(path, digest)
        for path in CORE_JSON + CORE_MD:
            sha256_file(path)

        auth = receipt["receipt_binding"]["receipt_payload"]["construction_authority"]
        require(auth["bounded_construction_grant_consumed"], True, "STOP_VS2_3_CONSTRUCTION_AUTHORITY_ABSENT", RECEIPT_JSON, "bounded_construction_grant_consumed")
        require(auth["bounded_construction_consumption_count_before"], 0, "STOP_VS2_3_CONSTRUCTION_AUTHORITY_ALREADY_CONSUMED", RECEIPT_JSON, "count_before")
        require(auth["bounded_construction_consumption_count_after"], 1, "STOP_VS2_3_CONSTRUCTION_AUTHORITY_SCOPE_DRIFT", RECEIPT_JSON, "count_after")
        require(auth["bounded_construction_frame_open"], True, "STOP_VS2_3_CONSTRUCTION_AUTHORITY_SCOPE_DRIFT", RECEIPT_JSON, "frame_open")
        require(auth["unconsumed_effective_grant_count"], 3, "STOP_VS2_3_CONSTRUCTION_AUTHORITY_SCOPE_DRIFT", RECEIPT_JSON, "unconsumed_effective_grant_count")
        post = receipt["receipt_binding"]["receipt_payload"]["post_state"]
        for key in ["runtime_instance_created", "candidate_instance_created", "fixture_instance_created", "move_space_constructed", "selector_constructed", "applicator_constructed", "convergence_criterion_constructed", "execution_authorized", "execution_performed", "sweep_authorized", "sweep_executed", "runner_created"]:
            require(post[key], False, "STOP_VS2_3_MOVE_OR_EXECUTION_DRIFT", RECEIPT_JSON, key)
        require(post["vs2_4_may_begin"], True, "STOP_VS2_3_NEXT_UNIT_AUTO_EXECUTED", RECEIPT_JSON, "vs2_4_may_begin")

        print(json.dumps({
            "vs2_3_verifier_gate": "PASS",
            "scope_regime_contract_sha256": f0_sha,
            "runtime_state_contract_sha256": o1_sha,
            "candidate_schema_sha256": o2_sha,
            "frozen_target_contract_sha256": o3_sha,
            "object_model_manifest_sha256": m0_sha,
            "receipt_sha256": receipt_sha,
            "raw_hashes_calculated": {path: sha256_file(path) for path in CORE_JSON + CORE_MD},
        }, indent=2, sort_keys=True))
        return 0
    except StopFailure as exc:
        print(json.dumps({
            "vs2_3_verifier_gate": "STOP",
            "failure_code": exc.code,
            "failed_artifact": exc.artifact,
            "failed_field_or_relationship": exc.field,
            "expected_value": exc.expected,
            "observed_value": exc.observed,
            "violated_invariant": exc.invariant,
            "violated_authority_boundary": "VS2_3_SCOPE_REGIME_AND_THREE_OBJECT_MODEL_ONLY",
            "blocked_downstream_unit": "VS2.3",
            "exact_bounded_correction_surface": "VS2_3_REPAIR_OR_BOOKKEEPING_SURFACE",
            "capability_proposal_candidate_required": False,
            "human_decision_required": False,
            "self_repair_performed": False,
        }, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
