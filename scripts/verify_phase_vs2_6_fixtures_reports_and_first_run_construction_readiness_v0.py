#!/usr/bin/env python3
"""Static verifier for VS2.6 fixture/report/readiness construction outputs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_phase_vs2_6_fixtures_reports_and_first_run_construction_readiness_v0 as b


ARTIFACT_PATHS = {
    "D0": b.D0_JSON,
    "F0X": b.F0X_JSON,
    "S0X": b.S0X_JSON,
    "FS0": b.FS0_JSON,
    "RP0": b.RP0_JSON,
    "E0": b.E0_JSON,
    "G0": b.G0_JSON,
    "GR0": b.GR0_JSON,
    "RS0": b.RS0_JSON,
    "U0": b.U0_JSON,
}

READY_STATUS = "READY"


def run_git(root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def load_json(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    if not path.exists():
        raise AssertionError(f"missing:{rel}")
    return json.loads(path.read_text(encoding="utf-8"))


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def canonical_binding_hash(artifact: dict[str, Any], rel: str) -> str:
    binding_key, payload_key, hash_key = b.binding_tuple(rel)
    binding = artifact.get(binding_key)
    if not isinstance(binding, dict):
        raise AssertionError(f"missing_binding:{rel}:{binding_key}")
    payload = binding.get(payload_key)
    got = binding.get(hash_key)
    actual = b.canonical_hash(payload)
    if got != actual:
        raise AssertionError(f"binding_hash_mismatch:{rel}:{got}!={actual}")
    return got


def assert_ref_matches(
    failures: list[str],
    label: str,
    got: dict[str, Any] | None,
    artifact: dict[str, Any],
    rel: str,
    role: str,
) -> None:
    want = b.local_ref(artifact, rel, role)
    if got != want:
        failures.append(f"reference_mismatch:{label}")


def check_no_unresolved(root: Path, failures: list[str]) -> None:
    for rel in b.GENERATED_DOCS:
        text = (root / rel).read_text(encoding="utf-8")
        for token in ["<derived>", "<placeholder>", "<hash>", "TBD", "TODO"]:
            if token in text:
                failures.append(f"unresolved_value:{rel}:{token}")


def main() -> int:
    root = Path.cwd().resolve()
    failures: list[str] = []

    if str(root) != b.ROOT:
        failures.append(f"repo_root_mismatch:{root}!={b.ROOT}")

    head = run_git(root, ["rev-parse", "HEAD"])
    branch = run_git(root, ["branch", "--show-current"])
    if head != b.HEAD:
        failures.append(f"head_mismatch:{head}!={b.HEAD}")
    if branch != "master":
        failures.append(f"branch_mismatch:{branch}!=master")

    status = run_git(root, ["status", "--short", "--untracked-files=all"])
    dirty_paths = status_paths(status)
    dirty_set = set(dirty_paths)
    if dirty_set != b.ALLOWED_DIRTY:
        failures.append(
            "dirty_scope_mismatch:"
            + json.dumps(
                {
                    "expected_count": len(b.ALLOWED_DIRTY),
                    "observed_count": len(dirty_set),
                    "missing": sorted(b.ALLOWED_DIRTY - dirty_set),
                    "unexpected": sorted(dirty_set - b.ALLOWED_DIRTY),
                },
                sort_keys=True,
            )
        )
    if any(path.startswith("discussion_packets/") for path in dirty_paths):
        failures.append("discussion_packets_dirty")

    try:
        check_no_unresolved(root, failures)
    except Exception as exc:  # noqa: BLE001 - verifier should surface exact artifact failure.
        failures.append(str(exc))

    artifacts: dict[str, dict[str, Any]] = {}
    artifact_hashes: dict[str, str] = {}
    for key, rel in ARTIFACT_PATHS.items():
        try:
            artifacts[key] = load_json(root, rel)
            artifact_hashes[key] = canonical_binding_hash(artifacts[key], rel)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{key}:{exc}")

    candidates: dict[str, dict[str, Any]] = {}
    candidate_hashes: dict[str, str] = {}
    for fixture_id, rel in b.CANDIDATE_PATHS.items():
        try:
            candidate = load_json(root, rel)
            candidates[fixture_id] = candidate
            candidate_hashes[fixture_id] = canonical_binding_hash(candidate, rel)
            if candidate.get("fixture_id") != fixture_id:
                failures.append(f"candidate_fixture_id_mismatch:{fixture_id}")
            for runtime_field in [
                "runtime_candidate_instance",
                "runtime_candidate_successor",
                "runtime_move_applied",
                "runtime_receipt_emitted",
                "runtime_state_published",
            ]:
                value = candidate.get(runtime_field)
                if value not in (None, False):
                    failures.append(f"candidate_runtime_field_nonempty:{fixture_id}:{runtime_field}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"candidate:{fixture_id}:{exc}")

    definitions: dict[str, dict[str, Any]] = {}
    definition_hashes: dict[str, str] = {}
    for fixture_id, rel in b.DEFINITION_PATHS.items():
        try:
            definition = load_json(root, rel)
            definitions[fixture_id] = definition
            definition_hashes[fixture_id] = canonical_binding_hash(definition, rel)
            if definition.get("fixture_id") != fixture_id:
                failures.append(f"definition_fixture_id_mismatch:{fixture_id}")
            if definition.get("expectation_match") != "NOT_EVALUATED":
                failures.append(f"definition_expectation_match_not_pre_execution:{fixture_id}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"definition:{fixture_id}:{exc}")

    report_hashes: dict[str, str] = {}
    for key, (_artifact_id, _contract_id, rel) in b.REPORT_CONTRACTS.items():
        try:
            report = load_json(root, rel)
            report_hashes[key] = canonical_binding_hash(report, rel)
            runtime_fields = report.get("runtime_fields_pre_execution", {})
            if runtime_fields.get("runtime_report_emitted") is not False:
                failures.append(f"report_runtime_emitted:{key}")
            if runtime_fields.get("runtime_case_count") != 0:
                failures.append(f"report_runtime_case_count:{key}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"report:{key}:{exc}")

    for rel, want in b.EXPECTED_RAW.items():
        actual = b.sha256_file(root / rel)
        if actual != want:
            failures.append(f"raw_upstream_hash_mismatch:{rel}:{actual}!={want}")
    for rel, want in b.EXPECTED_CANONICAL.items():
        upstream = load_json(root, rel)
        actual = canonical_binding_hash(upstream, rel)
        if actual != want:
            failures.append(f"canonical_upstream_hash_mismatch:{rel}:{actual}!={want}")

    if artifacts:
        d0 = artifacts.get("D0", {})
        f0x = artifacts.get("F0X", {})
        s0x = artifacts.get("S0X", {})
        fs0 = artifacts.get("FS0", {})
        rp0 = artifacts.get("RP0", {})
        e0 = artifacts.get("E0", {})
        g0 = artifacts.get("G0", {})
        gr0 = artifacts.get("GR0", {})
        rs0 = artifacts.get("RS0", {})
        u0 = artifacts.get("U0", {})

        if d0.get("remaining_construction_grant_records") and len(d0["remaining_construction_grant_records"]) != 3:
            failures.append("d0_remaining_grant_count_not_3")
        if f0x.get("fixture_ids") != b.FIXTURE_IDS or f0x.get("fixture_count") != 10:
            failures.append("f0x_fixture_order_or_count_wrong")
        if s0x.get("source_snapshot_status") != "FROZEN_FOR_CONSTRUCTION_READINESS_AUDIT":
            failures.append("s0x_snapshot_status_wrong")
        if fs0.get("fixture_order") != b.FIXTURE_IDS:
            failures.append("fs0_fixture_order_wrong")
        if fs0.get("candidate_specimen_count") != 10 or fs0.get("static_witness_count") != 10:
            failures.append("fs0_counts_wrong")
        if rp0.get("report_contract_count") != 5 or len(rp0.get("individual_report_contract_references", {})) != 5:
            failures.append("rp0_report_contract_count_wrong")
        if e0.get("exact_package_only") is not True:
            failures.append("e0_exact_package_only_not_true")
        if any(key in e0.get("package_references", {}) for key in ["G0", "GR0", "RS0"]):
            failures.append("e0_contains_post_core_reference")

        records = g0.get("readiness_component_records", [])
        statuses = {row.get("readiness_component_id"): row.get("readiness_status") for row in records}
        expected_component_ids = b.READINESS_COMPONENT_IDS
        if [row.get("readiness_component_id") for row in records] != expected_component_ids:
            failures.append("g0_r01_r21_order_wrong")
        if any(status != READY_STATUS for status in statuses.values()):
            failures.append("g0_r_status_not_ready")
        if g0.get("readiness_verdict") != b.READY_GATE:
            failures.append("g0_readiness_verdict_wrong")
        if g0.get("eligible_for_execution_decision") is not True:
            failures.append("g0_execution_decision_eligibility_wrong")

        if gr0.get("readiness_verdict") != b.READY_GATE:
            failures.append("gr0_readiness_verdict_wrong")
        if gr0.get("runtime_execution_performed") is not False:
            failures.append("gr0_runtime_execution_performed")
        if rs0.get("authority_status", {}).get("execution_authority_granted") is not False:
            failures.append("rs0_execution_authority_granted")
        if rs0.get("authority_status", {}).get("runner_authority_created") is not False:
            failures.append("rs0_runner_authority_created")

        if u0.get("readiness_verdict") != b.READY_GATE:
            failures.append("u0_readiness_verdict_wrong")
        if u0.get("remaining_effective_grant_count_before") != 3:
            failures.append("u0_remaining_before_wrong")
        if u0.get("remaining_effective_grant_count_after") != 0:
            failures.append("u0_remaining_after_wrong")
        for field in [
            "execution_authority_consumed_by_vs2_6",
            "execution_authority_created_by_vs2_6",
            "sweep_authority_consumed_by_vs2_6",
            "runner_authority_created_by_vs2_6",
            "execution_authority_present",
            "sweep_authority_present",
            "execution_started",
            "live_move_selected",
            "runtime_candidate_transformed",
            "runner_created",
        ]:
            if u0.get(field) is not False:
                failures.append(f"u0_forbidden_runtime_or_authority_field:{field}")
        for field in ["runtime_candidate_instance_count", "runtime_reports_emitted", "runtime_receipts_emitted", "runtime_commit_manifests_emitted", "fixture_executed_count"]:
            if u0.get(field) != 0:
                failures.append(f"u0_runtime_count_not_zero:{field}")
        if u0.get("logical_transition") != "ADVANCE(VS2_7_PHASE_CLOSURE_PENDING)":
            failures.append("u0_logical_transition_wrong")
        if u0.get("bookkeeping_transition") != "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_6_FIXTURES_REPORTS_AND_FIRST_RUN_CONSTRUCTION_READINESS_V0_PENDING)":
            failures.append("u0_bookkeeping_transition_wrong")

        assert_ref_matches(failures, "U0.D0", u0.get("artifact_bindings", {}).get("D0"), d0, b.D0_JSON, "UPSTREAM_PACKAGE_DEPENDENCY_INVENTORY")
        assert_ref_matches(failures, "U0.F0X", u0.get("artifact_bindings", {}).get("F0X"), f0x, b.F0X_JSON, "FIXTURE_CONTRACT")
        assert_ref_matches(failures, "U0.S0X", u0.get("artifact_bindings", {}).get("S0X"), s0x, b.S0X_JSON, "RUNTIME_SOURCE_SNAPSHOT")
        assert_ref_matches(failures, "U0.FS0", u0.get("artifact_bindings", {}).get("FS0"), fs0, b.FS0_JSON, "FIXTURE_SET")
        assert_ref_matches(failures, "U0.RP0", u0.get("artifact_bindings", {}).get("RP0"), rp0, b.RP0_JSON, "REPORT_CONTRACT_PACKAGE")
        assert_ref_matches(failures, "U0.E0", u0.get("artifact_bindings", {}).get("E0"), e0, b.E0_JSON, "EXECUTION_PACKAGE_CORE")
        assert_ref_matches(failures, "U0.G0", u0.get("artifact_bindings", {}).get("G0"), g0, b.G0_JSON, "READINESS_GATE")
        assert_ref_matches(failures, "U0.GR0", u0.get("artifact_bindings", {}).get("GR0"), gr0, b.GR0_JSON, "READINESS_GATE_RECEIPT")
        assert_ref_matches(failures, "U0.RS0", u0.get("artifact_bindings", {}).get("RS0"), rs0, b.RS0_JSON, "READINESS_SEAL")

    manifest_path = root / "baseline_share/MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_files = set(manifest.get("source_files", []))
        for required in [*b.GENERATED_DOCS, b.SCRIPT, b.VERIFY_SCRIPT]:
            if required not in source_files:
                failures.append(f"baseline_source_file_missing:{required}")
        if manifest.get("phase_vs2_current_unit") != b.UNIT_ID:
            failures.append("baseline_phase_vs2_current_unit_wrong")
        if manifest.get("current_unit") != b.UNIT_ID:
            failures.append("baseline_current_unit_wrong")
        if manifest.get("readiness_verdict") != b.READY_GATE:
            failures.append("baseline_readiness_verdict_wrong")
        if manifest.get("remaining_effective_grant_count") != 0:
            failures.append("baseline_remaining_grant_count_wrong")
        if manifest.get("execution_authority_present") is not False:
            failures.append("baseline_execution_authority_present_wrong")
    else:
        failures.append("baseline_manifest_missing")

    result = {
        "standalone_verifier_gate": "PASS" if not failures else "FAIL",
        "aggregate_gate": b.READY_GATE if not failures else "VS2_6_STATIC_VERIFICATION_FAIL",
        "repo_root": str(root),
        "branch": branch,
        "head": head,
        "dirty_count": len(dirty_set),
        "expected_dirty_count": len(b.ALLOWED_DIRTY),
        "readiness_verdict": artifacts.get("U0", {}).get("readiness_verdict"),
        "seal_status": artifacts.get("U0", {}).get("seal_status"),
        "execution_decision_eligibility": artifacts.get("U0", {}).get("eligible_for_execution_decision"),
        "artifact_hashes": artifact_hashes,
        "candidate_hashes": candidate_hashes,
        "fixture_definition_hashes": definition_hashes,
        "report_contract_hashes": report_hashes,
        "r01_through_r21_statuses": statuses if "statuses" in locals() else {},
        "fixture_count": artifacts.get("U0", {}).get("fixture_count"),
        "static_candidate_specimen_count": artifacts.get("U0", {}).get("static_candidate_specimen_count"),
        "runtime_candidate_instance_count": artifacts.get("U0", {}).get("runtime_candidate_instance_count"),
        "runtime_reports_emitted": artifacts.get("U0", {}).get("runtime_reports_emitted"),
        "runtime_receipts_emitted": artifacts.get("U0", {}).get("runtime_receipts_emitted"),
        "remaining_effective_grant_count_after": artifacts.get("U0", {}).get("remaining_effective_grant_count_after"),
        "execution_authority_present": artifacts.get("U0", {}).get("execution_authority_present"),
        "logical_transition": artifacts.get("U0", {}).get("logical_transition"),
        "bookkeeping_transition": artifacts.get("U0", {}).get("bookkeeping_transition"),
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
