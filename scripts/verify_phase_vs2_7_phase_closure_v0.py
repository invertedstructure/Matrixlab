#!/usr/bin/env python3
"""Verify Phase VS2.7 static closure artifacts."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_phase_vs2_7_phase_closure_v0 as helper


ROOT = "/home/asd/projects/matrixlab"
BRANCH = "master"
HEAD = "2369f1786d8ddcb905bc3609f983cb60af0fb70a"
READY_BRANCH = "READY"
CLOSURE_GATE = "VS2_7_PHASE_CLOSURE_PASS_READY_FOR_ONE_EXECUTION_DECISION"
FAIL_GATE = "VS2_7_PHASE_CLOSURE_FAIL"
PHASE_STATUS = "PHASE_VS2_PASS_FIRST_SWEEP_CAPABLE_KERNEL_SEALED_READY_FOR_ONE_BOUNDED_EXECUTION_DECISION"
READY_GATE = "VS2_6_FIRST_RUN_CONSTRUCTION_READINESS_PASS_READY_FOR_ONE_EXECUTION_DECISION"
TERMINAL_TRANSITION = "STOP_PHASE_VS2_CLOSED_PENDING_FIRST_EXECUTION_DECISION"
POST_PHASE_SURFACE = "POST_VS2_FIRST_EXECUTION_DECISION_SURFACE"
BOOKKEEPING_TRANSITION = "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS2_7_PHASE_CLOSURE_V0_PENDING)"

C0_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.json"
C0_MD = "docs/matrixlabs/phase_vs2/phase_vs2_closure_v0.md"
H0_MD = "docs/matrixlabs/phase_vs2/phase_vs2_closure_readout_v0.md"
R0_JSON = "docs/matrixlabs/phase_vs2/phase_vs2_7_phase_closure_receipt_v0.json"
SCRIPT = "scripts/build_phase_vs2_7_phase_closure_v0.py"
VERIFY_SCRIPT = "scripts/verify_phase_vs2_7_phase_closure_v0.py"
BASELINE_SCRIPT = "scripts/build_baseline_share_v0.py"
BASELINE_OUTPUTS = [
    "baseline_share/COMMIT_CONTEXT.md",
    "baseline_share/CURRENT_STATE.md",
    "baseline_share/MANIFEST.json",
    "baseline_share/RECEIPT_POINTERS.md",
]
ALLOWED_DIRTY = {C0_JSON, C0_MD, H0_MD, R0_JSON, SCRIPT, VERIFY_SCRIPT, BASELINE_SCRIPT, *BASELINE_OUTPUTS}
EXPECTED_SOURCE_HASHES = {
    "VS2_1_SOURCE_INTAKE": "830c62352e6eab4445b8cac9bbb7851da49a39633fc5cb673b71283bba1eaaeb",
    "VS2_1_SOURCE_MANIFEST": "9aaceb1758920971d8f5d7f305b837b7021ebc0a84714dea08755efce1c0a6ef",
    "VS2_1_RECEIPT": "b8b440b920993d38f77b0359ea928a255d780e5e682572fcc9144c35e63609cd",
    "PROFILE": "844fe441ecda5ec84076e9f665d09868373c9b24ea89d5d7056c485823db3142",
    "TARGET_FREEZE": "518bf3238994cfc88ea542289eb622c90f9eb7f3d6575398c95dd57203669eb8",
    "VS2_2_RECEIPT": "9e17272877e96f9db6885334e2531df8be8fdd7bb2d501d853c393b8f16ce425",
    "F0": "a6b4819aee35e5f09686a5a69d471b31f3a5cfdcab2078a29323ba1d31211179",
    "O1": "25fbdfb007372e346d61a3f5de8b0a4f5004c6dff1857e5fc31df38e17c087ad",
    "O2": "0216eb5944f87e760844d018d253f5e808a7a5b7ebd208d8d717e6709b979070",
    "O3": "378acf4fb02ad20bfd5213bde4b267fe605dc528812e29a985909fef251d7546",
    "M0": "0af5f635aaca5c37428cc94ca1a8ee6f3885d6e56543198bbdd33a5d4062db3c",
    "VS2_3_RECEIPT": "61a2298c0d04fa3acf47c391cc593df70be1d8e239e26de891d88b05ac879d0c",
    "S0": "9b9d6133965beec3b51600ec2d0ab9f002abbd48685cd82f1cf24e0d5d16d6ef",
    "V0": "a193dbbee21db8d5577445789d5971ffc29c8c5c37088d4bf88b14434c518c1d",
    "A0": "4fbd5ae95a00444201f0da70c52515e630b07972f9a3202944f007547d0db0ad",
    "MS0": "68b094ad5f7a283e591b7b23c66650db9921357e13b0e5c7ca7992723303cbe9",
    "P0": "7f2878149b30ca59e46ffa7e12580d4b2c96784e1b7964698d56eca5853c484c",
    "M1": "9cb7f9a66de7a0afc7109a07d789e56cb3629266d9f45821c0c971826afad389",
    "VS2_4_RECEIPT": "c78a48e892c0554327a2b1c27570453db48ce7368b27e4b58c6830defd7ff998",
    "K0": "3448ee02a854abdd5de28e2feb1ce866854473d9f18435083d5634e82b7a98a0",
    "C20": "a9c512025963df2a07ba93e3071683f392264013824f82ddbcfd923ab8321fd4",
    "R13": "a5375ec82dd148d05d7199296b58f186747b27cf3f4922555bec6ed1ed29cbf4",
    "M2": "ffb10d40f6dbf641879a3385ba312f80b9a1f9d667b230e49452ad48abce1e43",
    "VS2_5_RECEIPT": "31f88a51de957cca434747b02b3bbcbb1e0471f92323f5796a9607f2356e4c68",
    "D0": "fbc1e55d9e1c773244e72e0ed4fb14f901cb364566d0cc413c3cdcb21ec1943e",
    "F0X": "d34e71cd9d75d5c6c36bde3d17092050f5f1b1f2ede0e5fb985c57931551dec4",
    "S0X": "5638c07f1ffa559e1b12e5effaa08e21426267ac4e98906782fb0bf42b29bc7b",
    "FS0": "ce374e242bd0c9a910b8adf2002d8c037151d0dd7c5c093d5c073d6cc875eca8",
    "RP0": "830b56386b5bb189d008d2bbc904000cfb07e0f25d3be27092b4467a11c7b2b6",
    "E0": "cd3f9deed2278d8ab7292a7aa64cf1a68446312d26493f07e508f1d5360211c6",
    "G0": "94f1a98bbfb246226ef7f29887ea0a3ade2a4f71666b5852bbdf93815836cc99",
    "GR0": "705eb58f43460b289ac40a6e24557bce0be4accd04f372edd79df9ca38c12332",
    "RS0": "5c36c71da7bd70889c16a4722d882b0fe8dcfc5ce6cd8a72b80da4dbafbe2d79",
    "U0": "a651e622335001af85a79409b7074c7b1e5b1b46b9aaeb5e2b40beee4701ade5",
}


def run_git(root: Path, args: list[str]) -> str:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def status_paths(status: str) -> list[str]:
    paths: list[str] = []
    for line in status.splitlines():
        raw = line[2:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw)
    return paths


def main() -> int:
    root = Path.cwd().resolve()
    failures: list[str] = []
    if str(root) != ROOT:
        failures.append(f"repo_root_mismatch:{root}")
    branch = run_git(root, ["branch", "--show-current"])
    head = run_git(root, ["rev-parse", "HEAD"])
    if branch != BRANCH:
        failures.append(f"branch_mismatch:{branch}")
    if head != HEAD:
        failures.append(f"head_mismatch:{head}")
    dirty = set(status_paths(run_git(root, ["status", "--short", "--untracked-files=all"])))
    if dirty != ALLOWED_DIRTY:
        failures.append("dirty_scope_mismatch:" + json.dumps({"missing": sorted(ALLOWED_DIRTY - dirty), "unexpected": sorted(dirty - ALLOWED_DIRTY)}, sort_keys=True))
    if subprocess.run(["git", "diff", "--quiet", "--", *helper.PROTECTED_UPSTREAM_PATHS], cwd=root).returncode != 0:
        failures.append("protected_upstream_changed")
    if (root / "discussion_packets").exists():
        failures.append("discussion_packets_present")

    try:
        data, ledger = helper.load_sources(root)
        expected_payload = helper.build_payload(root)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"source_recompute_failed:{exc}")
        data, ledger, expected_payload = {}, [], {}

    ledger_hashes = {row["source_key"]: row["canonical_content_sha256"] for row in ledger}
    for key, expected in EXPECTED_SOURCE_HASHES.items():
        if ledger_hashes.get(key) != expected:
            failures.append(f"source_hash_mismatch:{key}:{ledger_hashes.get(key)}!={expected}")

    c0 = json.loads((root / C0_JSON).read_text(encoding="utf-8"))
    r0 = json.loads((root / R0_JSON).read_text(encoding="utf-8"))
    c0_payload = c0.get("closure_payload", {})
    if c0_payload != expected_payload:
        failures.append("c0_payload_mismatch_expected_recompute")
    if c0.get("closure_payload_sha256") != canonical_hash(c0_payload):
        failures.append("c0_canonical_hash_mismatch")
    if r0.get("receipt_payload_sha256") != canonical_hash(r0.get("receipt_payload", {})):
        failures.append("r0_canonical_hash_mismatch")
    receipt_payload = r0.get("receipt_payload", {})
    if receipt_payload.get("closure_artifact_sha256") != c0.get("closure_payload_sha256"):
        failures.append("r0_c0_hash_binding_mismatch")
    if receipt_payload.get("closure_json_raw_sha256") != sha256_file(root / C0_JSON):
        failures.append("r0_c0_raw_hash_mismatch")
    if receipt_payload.get("closure_markdown_raw_sha256") != sha256_file(root / C0_MD):
        failures.append("r0_c0_md_raw_hash_mismatch")
    if receipt_payload.get("closure_readout_raw_sha256") != sha256_file(root / H0_MD):
        failures.append("r0_h0_raw_hash_mismatch")

    cl_statuses = {row.get("closure_check_id"): row.get("closure_check_status") for row in c0_payload.get("closure_check_table_CL01_CL21", [])}
    if len(cl_statuses) != 21 or any(value != "PASS" for value in cl_statuses.values()):
        failures.append("cl01_cl21_not_all_pass")
    for key, value in {
        "readiness_branch": READY_BRANCH,
        "phase_status": PHASE_STATUS,
        "closure_gate": CLOSURE_GATE,
        "evidence_yield": "CONFIRMATION_YIELD",
    }.items():
        if c0_payload.get(key) != value:
            failures.append(f"c0_{key}_wrong:{c0_payload.get(key)}")
    if c0_payload.get("terminal_transition", {}).get("transition") != TERMINAL_TRANSITION:
        failures.append("terminal_transition_wrong")
    if c0_payload.get("post_phase_decision_surface", {}).get("surface_id") != POST_PHASE_SURFACE:
        failures.append("post_phase_surface_wrong")
    if c0_payload.get("post_phase_decision_surface", {}).get("created_by_vs2_7") is not False:
        failures.append("post_phase_surface_created")
    if c0_payload.get("authority_summary", {}).get("consumed_authority_count_by_vs2_7") != 0:
        failures.append("authority_consumed_by_vs2_7_nonzero")
    for field in ["execution_authority_present", "sweep_authority_present", "prospective_authority_active", "runner_created"]:
        if c0_payload.get("authority_summary", {}).get(field) is not False:
            failures.append(f"authority_field_wrong:{field}")
    if c0_payload.get("execution_state", {}).get("runtime_receipts_emitted") != 0:
        failures.append("runtime_receipts_emitted_nonzero")
    if c0_payload.get("execution_state", {}).get("runtime_reports_emitted") != 0:
        failures.append("runtime_reports_emitted_nonzero")

    c0_md = (root / C0_MD).read_text(encoding="utf-8")
    h0_md = (root / H0_MD).read_text(encoding="utf-8")
    for token in [PHASE_STATUS, CLOSURE_GATE, POST_PHASE_SURFACE, TERMINAL_TRANSITION, "CL01_SOURCE_SPINE_COMPLETE", "CL21_NO_EXECUTION_OR_FORBIDDEN_CLAIMS"]:
        if token not in c0_md:
            failures.append(f"c0_md_missing:{token}")
    for token in ["# Phase VS2 Closure v0", PHASE_STATUS, CLOSURE_GATE, "SEALED_READY_FOR_HUMAN_EXECUTION_DECISION", POST_PHASE_SURFACE, "It is not authorized to run."]:
        if token not in h0_md:
            failures.append(f"h0_md_missing:{token}")

    manifest = json.loads((root / "baseline_share/MANIFEST.json").read_text(encoding="utf-8"))
    for key, expected in {
        "current_unit": "VS2_7_PHASE_CLOSURE",
        "phase_status": PHASE_STATUS,
        "closure_gate": CLOSURE_GATE,
        "readiness_branch": READY_BRANCH,
        "execution_package_core_artifact_id": "phase_vs2_execution_package_core_manifest_v0",
        "execution_package_core_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_CORE_V0",
        "execution_package_core_sha256": EXPECTED_SOURCE_HASHES["E0"],
        "readiness_seal_artifact_id": "phase_vs2_execution_package_readiness_seal_v0",
        "readiness_seal_id": "FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_READINESS_SEAL_V0",
        "readiness_seal_sha256": EXPECTED_SOURCE_HASHES["RS0"],
        "next_lawful_surface": POST_PHASE_SURFACE,
        "next_surface_created": False,
        "execution_authority_present": False,
        "execution_started": False,
        "runner_created": False,
        "terminal_transition": TERMINAL_TRANSITION,
    }.items():
        if manifest.get(key) != expected:
            failures.append(f"baseline_manifest_{key}_wrong:{manifest.get(key)}!={expected}")
    source_files = set(manifest.get("source_files", []))
    for rel in [C0_JSON, C0_MD, H0_MD, R0_JSON, SCRIPT, VERIFY_SCRIPT]:
        if rel not in source_files:
            failures.append(f"baseline_source_missing:{rel}")

    receipt_pointer = (root / "baseline_share/RECEIPT_POINTERS.md").read_text(encoding="utf-8")
    if "file count: `7`" not in receipt_pointer:
        failures.append("phase_vs2_receipt_count_not_7")

    result = {
        "standalone_verifier_gate": "PASS" if not failures else FAIL_GATE,
        "closure_gate": CLOSURE_GATE if not failures else FAIL_GATE,
        "repo_root": str(root),
        "branch": branch,
        "HEAD": head,
        "dirty_count": len(dirty),
        "C0_canonical_hash": c0.get("closure_payload_sha256"),
        "C0_raw_hash": sha256_file(root / C0_JSON),
        "C0_markdown_raw_hash": sha256_file(root / C0_MD),
        "H0_readout_raw_hash": sha256_file(root / H0_MD),
        "R0_canonical_hash": r0.get("receipt_payload_sha256"),
        "R0_raw_hash": sha256_file(root / R0_JSON),
        "CL01_CL21_statuses": cl_statuses,
        "source_identity_count": len(ledger),
        "source_linkage_count": len(c0_payload.get("source_linkage_table", [])),
        "unit_gates": c0_payload.get("unit_gate_table", []),
        "logical_transitions": c0_payload.get("logical_transition_table", []),
        "readiness_branch": c0_payload.get("readiness_branch"),
        "readiness_component_count": c0_payload.get("readiness_summary", {}).get("readiness_component_count"),
        "readiness_ready_count": c0_payload.get("readiness_summary", {}).get("readiness_ready_count"),
        "fixture_count": c0_payload.get("fixture_summary", {}).get("fixture_count"),
        "static_candidate_specimen_count": c0_payload.get("fixture_summary", {}).get("static_candidate_specimen_count"),
        "runtime_candidate_instance_count": c0_payload.get("fixture_summary", {}).get("runtime_candidate_instance_count"),
        "remaining_grant_count": c0_payload.get("construction_authority_consumption_history", {}).get("vs2_6", {}).get("remaining_effective_grant_count_after"),
        "execution_authority_present": c0_payload.get("authority_summary", {}).get("execution_authority_present"),
        "sweep_authority_present": c0_payload.get("authority_summary", {}).get("sweep_authority_present"),
        "prospective_authority_active": c0_payload.get("authority_summary", {}).get("prospective_authority_active"),
        "runtime_receipts_emitted": c0_payload.get("execution_state", {}).get("runtime_receipts_emitted"),
        "runtime_reports_emitted": c0_payload.get("execution_state", {}).get("runtime_reports_emitted"),
        "runner_created": c0_payload.get("authority_summary", {}).get("runner_created"),
        "protected_upstream_unchanged": "protected_upstream_changed" not in failures,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
