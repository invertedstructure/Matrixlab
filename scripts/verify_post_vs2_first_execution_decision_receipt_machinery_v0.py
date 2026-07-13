#!/usr/bin/env python3
"""Verify Post-VS2 first execution decision receipt machinery v0."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "a6252de12e71ad9eb558a9a5a539e21002678dc3"
GATE = "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PASS_READY_FOR_EXPLICIT_HUMAN_DECISION_INPUT"
SURFACE_HASH = "d7150101acbfe46342c95506c526e2b49b6ca295881c2e390d78fdb4c5001d35"
SURFACE_RECEIPT_HASH = "658fcc2331fd3fc3c9c2865778d9163ddcb05724db1dc2d3343189859c4100cd"
TERMINAL = "STOP_POST_VS2_DECISION_RECEIPT_MACHINERY_READY_SURFACE_UNCONSUMED"

INPUT_CONTRACT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.json"
INPUT_CONTRACT_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_human_decision_input_contract_v0.md"
RECEIPT_CONTRACT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.json"
RECEIPT_CONTRACT_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.md"
MACHINERY_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_machinery_receipt_v0.json"
AUTH_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.json"
AUTH_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_v0.md"
SURFACE_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.json"
SURFACE_MD = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_v0.md"
SURFACE_RECEIPT_JSON = "docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json"
RECEIPT_BUILDER = "scripts/build_post_vs2_first_execution_decision_receipt_v0.py"
RECEIPT_VERIFIER = "scripts/verify_post_vs2_first_execution_decision_receipt_v0.py"
SCRIPT = "scripts/build_post_vs2_first_execution_decision_receipt_machinery_v0.py"
VERIFY_SCRIPT = "scripts/verify_post_vs2_first_execution_decision_receipt_machinery_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
EXPECTED_NEW = {SCRIPT, VERIFY_SCRIPT, RECEIPT_BUILDER, RECEIPT_VERIFIER, INPUT_CONTRACT_JSON, INPUT_CONTRACT_MD, RECEIPT_CONTRACT_JSON, RECEIPT_CONTRACT_MD, MACHINERY_RECEIPT_JSON}
EXPECTED_MODIFIED = {BASELINE_SCRIPT, *BASELINE_OUTPUTS}
EXPECTED_DIRTY = EXPECTED_NEW | EXPECTED_MODIFIED
OPTIONS = [
    "AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE",
    "REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
    "RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION",
    "DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION",
    "REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST",
    "ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION",
]
BRANCHES = ["D01", "D02", "D03", "D04", "D05", "D06"]


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(root: Path, args: list[str], binary: bool = False) -> Any:
    return subprocess.check_output(["git", *args], cwd=root, text=not binary)


def status_paths(status: str) -> set[str]:
    paths: set[str] = set()
    for line in status.splitlines():
        if line.startswith("?? "):
            paths.add(line[3:])
        elif len(line) >= 4:
            paths.add(line[3:])
    return paths


def base_input(option: str, branch: str) -> dict[str, Any]:
    payloads = {
        "D01": {"branch_id": "D01", "requested_absolute_expiry_timestamp": "2026-12-31T00:00:00Z", "earliest_expiry_rule_acknowledged": True},
        "D02": {"branch_id": "D02", "requested_fixture_ids": ["F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION"], "requested_fixture_order": ["F01_POSITIVE_REQUIRED_FIELD_AND_NORMALIZATION"], "requested_fixture_count": 1, "requested_maximum_controlled_steps_per_case": 1, "requested_maximum_attempted_moves_per_case": 1, "requested_maximum_applied_moves_per_case": 1, "requested_maximum_total_controlled_steps": 1, "requested_maximum_total_attempted_moves": 1, "requested_maximum_total_applied_moves": 1, "reduction_rationale": "Verifier test.", "desired_evidence_objective": "Verifier test."},
        "D03": {"branch_id": "D03", "affected_artifact_id": "phase_vs2_execution_package_core_manifest_v0", "affected_package_surface": {"artifact_id": "phase_vs2_execution_package_core_manifest_v0"}, "requested_change": "Verifier test.", "reason": "Verifier test.", "expected_evidence_improvement": "Verifier test.", "required_new_evidence": ["new chain"]},
        "D04": {"branch_id": "D04", "defer_reason": "Verifier test.", "reconsideration_condition": "later input", "new_decision_surface_required": True, "identity_revalidation_required": True, "execution_eligibility_revalidation_required": True, "readiness_rerun_condition": "if changed"},
        "D05": {"branch_id": "D05", "rejection_reason": "Verifier test.", "rejection_scope": "CURRENT_EXECUTION_REQUEST_ONLY", "package_may_be_reconsidered": True, "revision_recommended": False, "new_decision_surface_required_for_reconsideration": True},
        "D06": {"branch_id": "D06", "abandonment_reason": "Verifier test.", "abandonment_scope": "EXACT_EXECUTION_PACKAGE_CORE_AND_READINESS_SEAL_TUPLE", "supersession_expected": True},
    }
    return {
        "schema_version": "matrixlabs_post_vs2_first_execution_human_decision_input_v0",
        "input_id": "post_vs2_first_execution_human_decision_input_v0",
        "input_version": "v0",
        "decision_timestamp": "2026-07-13T00:00:00Z",
        "decision_actor_class": "HUMAN_AUTHORITY",
        "decision_actor_reference": "verifier_test_only",
        "decision_actor_authentication_reference": "evidence://verifier/test",
        "decision_interface_contract_reference": "POST_VS2_FIRST_EXECUTION_HUMAN_DECISION_INPUT_CONTRACT_V0",
        "decision_surface_id": "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE",
        "decision_surface_version": "v0",
        "decision_surface_canonical_hash": SURFACE_HASH,
        "selected_surface_option_code": option,
        "decision_payload": payloads[branch],
        "decision_rationale": "Verifier test-only validation.",
        "authoritative": False,
        "test_only": True,
    }


def run_builder(root: Path, payload: dict[str, Any]) -> bool:
    with tempfile.TemporaryDirectory(prefix="post_vs2_machinery_verify_") as tmp:
        path = Path(tmp) / "input.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        proc = subprocess.run([sys.executable, RECEIPT_BUILDER, "--decision-input", str(path), "--validate-only"], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return proc.returncode == 0 and "POST_VS2_FIRST_EXECUTION_DECISION_INPUT_VALIDATION_ONLY_PASS" in proc.stdout


def main() -> int:
    root = Path.cwd().resolve()
    failures: list[str] = []
    if str(root) != ROOT:
        failures.append(f"repo_root_wrong:{root}")
    if git(root, ["branch", "--show-current"]).strip() != BRANCH:
        failures.append("branch_wrong")
    if git(root, ["rev-parse", "HEAD"]).strip() != HEAD:
        failures.append("head_wrong")
    staged = git(root, ["diff", "--cached", "--name-only"]).splitlines()
    if staged:
        failures.append(f"staged_present:{staged}")

    for rel in [INPUT_CONTRACT_JSON, INPUT_CONTRACT_MD, RECEIPT_CONTRACT_JSON, RECEIPT_CONTRACT_MD, MACHINERY_RECEIPT_JSON, RECEIPT_BUILDER, RECEIPT_VERIFIER]:
        if not (root / rel).exists():
            failures.append(f"missing:{rel}")
    if (root / AUTH_JSON).exists() or (root / AUTH_MD).exists():
        failures.append("authoritative_receipt_present")

    surface = json.loads((root / SURFACE_JSON).read_text(encoding="utf-8"))
    surface_receipt = json.loads((root / SURFACE_RECEIPT_JSON).read_text(encoding="utf-8"))
    machinery = json.loads((root / MACHINERY_RECEIPT_JSON).read_text(encoding="utf-8"))
    payload = machinery.get("receipt_binding", {}).get("receipt_payload", {})
    if sha256_bytes(canonical_bytes(payload)) != machinery.get("receipt_binding", {}).get("receipt_sha256"):
        failures.append("machinery_receipt_hash_wrong")
    if surface.get("surface_payload_sha256") != SURFACE_HASH:
        failures.append("surface_hash_wrong")
    if surface_receipt.get("receipt_payload_sha256") != SURFACE_RECEIPT_HASH:
        failures.append("surface_receipt_hash_wrong")
    if payload.get("machinery_gate") != GATE or payload.get("terminal_transition") != TERMINAL:
        failures.append("machinery_gate_or_terminal_wrong")
    if payload.get("source_identity_count") != 44 or payload.get("source_linkage_count") != 11:
        failures.append("source_counts_wrong")
    if payload.get("machinery_check_count") != 24 or payload.get("machinery_check_pass_count") != 24:
        failures.append("machinery_checks_wrong")
    if payload.get("negative_probe_count") != 18 or payload.get("negative_probe_pass_count") != 18:
        failures.append("negative_probes_wrong")
    if payload.get("test_branch_count") != 6 or payload.get("test_branch_validation_pass_count") != 6:
        failures.append("branch_validation_wrong")
    posture = payload.get("normalized_blocker_posture", {})
    if posture.get("blocker_source_count") != 4 or posture.get("normalized_typed_readiness_blocker_count") != 0 or posture.get("RS0_blocker_field_required") is not False:
        failures.append("blocker_posture_wrong")
    for option, branch in zip(OPTIONS, BRANCHES):
        if not run_builder(root, base_input(option, branch)):
            failures.append(f"branch_validate_failed:{branch}")
    manifest = json.loads((root / "baseline_share/MANIFEST.json").read_text(encoding="utf-8"))
    expected_baseline = {
        "current_unit": "POST_VS2_FIRST_EXECUTION_DECISION_RECEIPT_MACHINERY_PREPARATION",
        "current_surface": "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE",
        "surface_instance_state": "UNCONSUMED",
        "human_decision_required": True,
        "human_decision_input_present": False,
        "human_decision_recorded": False,
        "decision_receipt_created": False,
        "decision_receipt_machinery_ready": True,
        "decision_option_count": 6,
        "authority_update_applied": False,
        "execution_authority_present": False,
        "run_id_created": False,
        "execution_source_intake_created": False,
        "execution_started": False,
        "runtime_receipts_emitted": 0,
        "runtime_reports_emitted": 0,
        "runner_created": False,
        "next_lawful_action": "SUPPLY_ONE_EXPLICIT_AUTHENTICATED_POST_VS2_HUMAN_DECISION_INPUT",
        "terminal_transition": TERMINAL,
    }
    for key, expected in expected_baseline.items():
        if manifest.get(key) != expected:
            failures.append(f"baseline_{key}_wrong:{manifest.get(key)}")
    source_files = set(manifest.get("source_files", []))
    for rel in [INPUT_CONTRACT_JSON, INPUT_CONTRACT_MD, RECEIPT_CONTRACT_JSON, RECEIPT_CONTRACT_MD, MACHINERY_RECEIPT_JSON, SCRIPT, VERIFY_SCRIPT, RECEIPT_BUILDER, RECEIPT_VERIFIER]:
        if rel not in source_files:
            failures.append(f"baseline_source_missing:{rel}")
    dirty = status_paths(git(root, ["status", "--short", "--untracked-files=all"]))
    if dirty != EXPECTED_DIRTY:
        failures.append(f"dirty_scope_wrong:{sorted(dirty)}")
    protected_phase_vs2 = subprocess.run(["git", "diff", "--quiet", "--", "docs/matrixlabs/phase_vs2"], cwd=root).returncode == 0
    protected_surface = subprocess.run(["git", "diff", "--quiet", "--", SURFACE_JSON, SURFACE_MD, SURFACE_RECEIPT_JSON], cwd=root).returncode == 0
    if not protected_phase_vs2:
        failures.append("phase_vs2_changed")
    if not protected_surface:
        failures.append("post_vs2_surface_changed")

    result = {
        "machinery_verifier_gate": GATE if not failures else "FAIL",
        "repo_root": str(root),
        "branch": BRANCH,
        "HEAD": HEAD,
        "source_anchor_commit": HEAD,
        "surface_canonical_hash": SURFACE_HASH,
        "surface_preparation_receipt_canonical_hash": SURFACE_RECEIPT_HASH,
        "input_contract_canonical_hash": json.loads((root / INPUT_CONTRACT_JSON).read_text(encoding="utf-8"))["contract_binding"]["contract_sha256"],
        "input_contract_markdown_raw_hash": sha256_file(root / INPUT_CONTRACT_MD),
        "receipt_contract_canonical_hash": json.loads((root / RECEIPT_CONTRACT_JSON).read_text(encoding="utf-8"))["contract_binding"]["contract_sha256"],
        "receipt_contract_markdown_raw_hash": sha256_file(root / RECEIPT_CONTRACT_MD),
        "machinery_receipt_canonical_hash": machinery.get("receipt_binding", {}).get("receipt_sha256"),
        "machinery_receipt_raw_hash": sha256_file(root / MACHINERY_RECEIPT_JSON),
        "machinery_check_count": payload.get("machinery_check_count"),
        "machinery_check_pass_count": payload.get("machinery_check_pass_count"),
        "negative_probe_count": payload.get("negative_probe_count"),
        "negative_probe_pass_count": payload.get("negative_probe_pass_count"),
        "test_branch_count": payload.get("test_branch_count"),
        "test_branch_validation_pass_count": payload.get("test_branch_validation_pass_count"),
        "generic_proceed_maps_to_option": payload.get("generic_proceed_maps_to_option"),
        "authoritative_input_created": payload.get("authoritative_human_decision_input_created"),
        "authoritative_decision_receipt_created": payload.get("authoritative_decision_receipt_created"),
        "surface_state": payload.get("surface_state"),
        "surface_consumed": payload.get("surface_consumed"),
        "human_decision_recorded": payload.get("human_decision_recorded"),
        "selected_option": payload.get("selected_option"),
        "authority_update_applied": payload.get("authority_update_applied"),
        "package_state_updated": payload.get("package_state_updated"),
        "execution_authority_present": payload.get("execution_authority_present"),
        "run_id_created": payload.get("run_id_created"),
        "execution_source_intake_created": payload.get("execution_source_intake_created"),
        "fixtures_executed": payload.get("fixtures_executed"),
        "runtime_receipts_emitted": payload.get("runtime_receipts_emitted"),
        "runtime_reports_emitted": payload.get("runtime_reports_emitted"),
        "protected_Phase_VS2_sources_unchanged": protected_phase_vs2,
        "committed_Post_VS2_surface_unchanged": protected_surface,
        "dirty_path_count": len(dirty),
        "staged_path_count": len(staged),
        "commit_created": False,
        "push_executed": False,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
