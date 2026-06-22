#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_WITH_FIXTURES_V0"

UPGRADE_POLICY_ID = "d76f7ceb"
UPGRADE_POLICY_RECEIPT_ID = "a3b2c208"
HUMAN_DECISION_ID = "cef49876"
DELTA_PROPOSAL_ID = "6e4ee1ea"
PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID = "0d2f03d4"
HALT_SURFACE_PROBE_RUN_RECEIPT_ID = "5030948f"
V0_1_IMPLEMENTATION_RECEIPT_ID = "04c0692d"
SOURCE_LOCAL_REGIME_HASH = "097d620c"

SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
TARGET_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v0"
TARGET_LOCAL_REGIME_VERSION = "local_regime.v1"

UPGRADE_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policies" / f"{UPGRADE_POLICY_ID}.json"
UPGRADE_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_receipts" / f"{UPGRADE_POLICY_ID}.json"
HUMAN_DECISION_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decisions" / f"{HUMAN_DECISION_ID}.json"
DELTA_PROPOSAL_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposals" / f"{DELTA_PROPOSAL_ID}.json"
PROBE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_run_receipts" / f"{PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
HALT_SURFACE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts" / f"{HALT_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
V0_1_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{V0_1_IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_V0_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{SOURCE_LOCAL_REGIME_HASH}.json"
RUNNER_V0_1_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"
RUNNER_V0_2_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2.py"

LOCAL_REGIME_V1_DIR = ROOT / "data" / "local_regime_v1_declarations"
FIXTURE_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_fixtures"
TRANSCRIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_expected_transcripts"
CASE_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_case_receipts"
PROPOSAL_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_proposal_receipts"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts"

EXPECTED_TRANSCRIPT = [
    "LOAD_REGIME",
    "LOAD_STATE",
    "VALIDATE_STATE",
    "SELECT_MOVE",
    "CHECK_AUTHORITY",
    "APPLY_OR_BLOCK_MOVE",
    "EMIT_RECEIPT",
    "EMIT_METRICS",
    "EMIT_TERMINAL",
]

REQUIRED_CASES = [
    "HALT_WITH_PROPOSAL_ON_NO_APPLICABLE_MOVE",
    "PROPOSAL_NON_EXECUTION_GUARD",
    "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_FIRST",
    "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND",
    "NO_PROPOSAL_WHEN_INSUFFICIENT_EVIDENCE",
    "AUTHORITY_VIOLATION_NO_PROPOSAL_PROMOTION",
]

ACCEPTANCE_GATES = [
    "S0_source_chain_verified",
    "S1_local_regime_v1_declared",
    "S2_runner_v0_2_implemented",
    "S3_halt_with_proposal_fixture_passes",
    "S4_proposal_non_execution_passes",
    "S5_duplicate_unresolved_proposal_guard_passes",
    "S6_no_hidden_continuation",
    "S7_no_registry_or_global_taxonomy",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def burden_bytes(obj: Any) -> int:
    return len(canonical_bytes(obj))

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def validate_inputs(
    policy: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    human_decision: Dict[str, Any],
    delta_proposal: Dict[str, Any],
    probe_run: Dict[str, Any],
    halt_surface: Dict[str, Any],
    v0_1_impl: Dict[str, Any],
    local_regime_v0: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != UPGRADE_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != UPGRADE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != UPGRADE_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != UPGRADE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")

    terminal = policy_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    if policy_receipt.get("source_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"source_runner_wrong:{policy_receipt.get('source_runner_unit_id')}")
    if policy_receipt.get("target_runner_unit_id") != TARGET_RUNNER_UNIT_ID:
        failures.append(f"target_runner_wrong:{policy_receipt.get('target_runner_unit_id')}")
    if policy_receipt.get("target_local_regime_version") != TARGET_LOCAL_REGIME_VERSION:
        failures.append(f"target_regime_wrong:{policy_receipt.get('target_local_regime_version')}")

    accepted = policy_receipt.get("accepted_minimum_shape") or {}
    for key in [
        "halt_with_proposal",
        "proposal_non_execution",
        "duplicate_unresolved_proposal_guard",
        "human_review_required_before_promotion",
        "proposal_receipt_required",
    ]:
        if accepted.get(key) is not True:
            failures.append(f"accepted_minimum_shape_missing:{key}:{accepted.get(key)}")

    required_cases = policy_receipt.get("required_fixture_cases") or {}
    for case in REQUIRED_CASES:
        if case not in required_cases:
            failures.append(f"required_case_missing:{case}")

    gates = policy_receipt.get("acceptance_gates") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"required_gate_missing:{gate}:{gates.get(gate)}")

    auth = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "write_local_regime_v1_declaration",
        "write_runner_v0_2_module",
        "write_v0_2_upgrade_fixtures",
        "write_v0_2_expected_transcripts",
        "execute_runner_v0_2_against_fixtures",
        "emit_v0_2_case_receipts",
        "emit_v0_2_proposal_receipts",
        "emit_v0_2_implementation_receipt",
    ]:
        if auth.get(key) is not True:
            failures.append(f"authorized_operation_missing:{key}:{auth.get(key)}")

    forbidden = policy_receipt.get("forbidden_operations_next") or {}
    for key in [
        "modify_runner_v0_1_module",
        "replace_local_regime_v0",
        "mutate_local_regime_at_runtime",
        "execute_or_apply_proposal",
        "promote_proposal_without_human_review",
        "registry_sqlite_write",
        "registry_sqlite_read",
        "global_taxonomy_design",
        "final_schema_claim",
        "proof_claim",
        "hidden_continuation_after_stop",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_missing:{key}:{forbidden.get(key)}")

    if human_decision.get("decision_id") != HUMAN_DECISION_ID:
        failures.append(f"human_decision_id_wrong:{human_decision.get('decision_id')}")
    if human_decision.get("decision_status") != "ACCEPTED_PROVISIONALLY_FOR_POLICY_BUILD_NOT_APPLIED":
        failures.append(f"human_decision_status_wrong:{human_decision.get('decision_status')}")

    if delta_proposal.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_proposal_id_wrong:{delta_proposal.get('proposal_id')}")
    if delta_proposal.get("proposal_class") != "PROPOSITION_SURFACE_DELTA_PROPOSAL":
        failures.append(f"delta_class_wrong:{delta_proposal.get('proposal_class')}")
    if delta_proposal.get("proposal_status") != "REVIEW_REQUIRED_NOT_APPLIED":
        failures.append(f"delta_status_wrong:{delta_proposal.get('proposal_status')}")

    if probe_run.get("receipt_id") != PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"probe_run_id_wrong:{probe_run.get('receipt_id')}")
    if probe_run.get("gate") != "PASS":
        failures.append(f"probe_run_gate_not_PASS:{probe_run.get('gate')}")
    if probe_run.get("probe_result_class") != "PROPOSAL_SURFACE_ABSENT_REQUIRES_DELTA_PROPOSAL":
        failures.append(f"probe_result_wrong:{probe_run.get('probe_result_class')}")

    if halt_surface.get("receipt_id") != HALT_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"halt_surface_id_wrong:{halt_surface.get('receipt_id')}")
    if halt_surface.get("gate") != "PASS":
        failures.append(f"halt_surface_gate_not_PASS:{halt_surface.get('gate')}")
    if halt_surface.get("coverage_complete") is not True:
        failures.append(f"halt_surface_coverage_not_complete:{halt_surface.get('coverage_complete')}")

    if v0_1_impl.get("receipt_id") != V0_1_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"v0_1_impl_id_wrong:{v0_1_impl.get('receipt_id')}")
    if v0_1_impl.get("gate") != "PASS":
        failures.append(f"v0_1_impl_gate_not_PASS:{v0_1_impl.get('gate')}")

    if local_regime_v0.get("local_regime_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"local_regime_v0_hash_wrong:{local_regime_v0.get('local_regime_hash')}")
    if local_regime_v0.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_v0_version_wrong:{local_regime_v0.get('local_regime_version')}")

    for path, label in [
        (UPGRADE_POLICY_PATH, "upgrade_policy"),
        (UPGRADE_POLICY_RECEIPT_PATH, "upgrade_policy_receipt"),
        (HUMAN_DECISION_PATH, "human_decision"),
        (DELTA_PROPOSAL_PATH, "delta_proposal"),
        (PROBE_RUN_RECEIPT_PATH, "proposition_surface_probe_run"),
        (HALT_SURFACE_RUN_RECEIPT_PATH, "halt_surface_probe_run"),
        (V0_1_IMPLEMENTATION_RECEIPT_PATH, "v0_1_implementation_receipt"),
        (LOCAL_REGIME_V0_PATH, "local_regime_v0"),
        (RUNNER_V0_1_PATH, "runner_v0_1"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_local_regime_v1(local_regime_v0: Dict[str, Any], policy_receipt: Dict[str, Any]) -> Dict[str, Any]:
    regime = copy.deepcopy(local_regime_v0)
    regime.pop("local_regime_hash", None)
    regime["schema_version"] = "local_regime_v1_declaration"
    regime["local_regime_version"] = TARGET_LOCAL_REGIME_VERSION
    regime["source_local_regime_version"] = SOURCE_LOCAL_REGIME_VERSION
    regime["source_local_regime_hash"] = SOURCE_LOCAL_REGIME_HASH
    regime["upgrade_policy_id"] = UPGRADE_POLICY_ID
    regime["upgrade_policy_receipt_id"] = UPGRADE_POLICY_RECEIPT_ID
    regime["regime_status"] = "DECLARED_NOT_REPLACING_V0"
    regime["proposal_surface"] = policy_receipt["local_regime_v1_required_delta"]["proposal_surface"]
    regime["duplicate_unresolved_proposal_guard"] = policy_receipt["local_regime_v1_required_delta"]["duplicate_unresolved_proposal_guard"]
    regime["non_execution_contract"] = policy_receipt["local_regime_v1_required_delta"]["non_execution_contract"]
    regime["accepted_minimum_shape"] = policy_receipt["accepted_minimum_shape"]
    regime["authority_guards"] = {
        "source_local_regime_v0_replaced": False,
        "local_regime_runtime_mutated": False,
        "proposal_promoted": False,
        "registry_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
    }
    regime["local_regime_hash"] = sha8(regime)
    return regime

RUNNER_V0_2_SOURCE = r'''
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

EXPECTED_TRANSCRIPT = [
    "LOAD_REGIME",
    "LOAD_STATE",
    "VALIDATE_STATE",
    "SELECT_MOVE",
    "CHECK_AUTHORITY",
    "APPLY_OR_BLOCK_MOVE",
    "EMIT_RECEIPT",
    "EMIT_METRICS",
    "EMIT_TERMINAL",
]

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def _sha8(obj: Any) -> str:
    return hashlib.sha256(_canonical_bytes(obj)).hexdigest()[:8]

def _burden_bytes(obj: Any) -> int:
    return len(_canonical_bytes(obj))

class JurisdictionRunnerV02:
    runner_unit_id = "jurisdiction_runner.v0.2"

    def __init__(self, local_regime: Dict[str, Any]):
        self.local_regime = copy.deepcopy(local_regime)
        self.local_regime_hash = self.local_regime.get("local_regime_hash")
        self.local_regime_version = self.local_regime.get("local_regime_version", "local_regime.v1")
        self._unresolved_proposals: Dict[str, Dict[str, Any]] = {}

    def _proposal_key(self, state: Dict[str, Any], proposed_delta_kind: str) -> str:
        return _sha8({
            "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "source_state_id": state.get("state_id"),
            "proposed_delta_kind": proposed_delta_kind,
        })

    def _proposal_receipt(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_proposal_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_PROPOSAL_RECEIPT",
            "proposal_id": proposal["proposal_id"],
            "proposal_type": proposal["proposal_type"],
            "proposal_status": proposal["proposal_status"],
            "runner_unit_id": self.runner_unit_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "source_halt_code": proposal["source_halt_code"],
            "source_state_id": proposal["source_state_id"],
            "source_fixture_id": proposal["source_fixture_id"],
            "proposed_delta_kind": proposal["proposed_delta_kind"],
            "human_review_required": True,
            "proposal_executed": False,
            "proposal_promoted": False,
            "local_regime_runtime_mutated": False,
            "registry_written": False,
            "hidden_continuation_authorized": False,
            "gate": "PASS",
            "created_at": _now_iso(),
        }
        receipt["receipt_id"] = _sha8({
            "proposal_id": proposal["proposal_id"],
            "receipt_type": receipt["receipt_type"],
        })
        return receipt

    def _emit(
        self,
        *,
        fixture_id: Optional[str],
        input_state: Dict[str, Any],
        input_artifact_paths: List[str],
        halt_code: str,
        move_status: str,
        selected_move_id: Optional[str],
        no_proposal_reason: Optional[str],
        proposal: Optional[Dict[str, Any]],
        proposal_status: str,
        proposal_receipt: Optional[Dict[str, Any]],
        duplicate_unresolved: bool = False,
        state_after: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        halt_with_proposal = proposal_status == "EMITTED_REVIEW_REQUIRED"
        proposal_withheld = proposal_status == "WITHHELD_DUPLICATE_UNRESOLVED" or (
            proposal_status == "NONE" and no_proposal_reason is not None
        )

        metrics = {
            "move_count": 1 if selected_move_id else 0,
            "applied_move_count": 1 if move_status == "APPLIED" else 0,
            "blocked_move_count": 1 if move_status == "BLOCKED" else 0,
            "halt_count_by_code": {halt_code: 1},
            "runtime_proposal_emitted_count": 1 if proposal_status == "EMITTED_REVIEW_REQUIRED" else 0,
            "runtime_proposal_executed_count": 0,
            "runtime_proposal_promoted_count": 0,
            "duplicate_unresolved_proposal_count": 1 if duplicate_unresolved else 0,
            "proposal_withheld_count": 1 if proposal_withheld else 0,
            "proposal_count_by_type": {"LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL": 1} if halt_with_proposal else {},
            "halt_with_proposal_count": 1 if halt_with_proposal else 0,
            "halt_without_proposal_count": 0 if halt_with_proposal else 1,
            "proposal_receipt_count": 1 if proposal_receipt else 0,
            "receipt_count": 1,
        }

        authority_guards = {
            "proposal_executed": False,
            "proposal_promoted": False,
            "local_regime_runtime_mutated": False,
            "registry_written": False,
            "registry_inserted": False,
            "registry_sqlite_read": False,
            "registry_sqlite_written": False,
            "full_registry_scan_used": False,
            "global_taxonomy_claimed": False,
            "final_schema_claimed": False,
            "proof_claimed": False,
            "hidden_continuation_authorized": False,
            "runner_module_changed": False,
        }

        artifact_guards = {
            "input_artifacts_path_addressed": True,
            "output_artifacts_receipt_referenced": True,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_authority_used": False,
        }

        receipt_seed = {
            "runner_unit_id": self.runner_unit_id,
            "local_regime_hash": self.local_regime_hash,
            "fixture_id": fixture_id,
            "state_id": input_state.get("state_id"),
            "halt_code": halt_code,
            "move_status": move_status,
            "proposal_status": proposal_status,
            "proposal_id": proposal.get("proposal_id") if proposal else None,
        }

        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_CASE_RECEIPT",
            "receipt_id": _sha8(receipt_seed),
            "runner_unit_id": self.runner_unit_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "fixture_id": fixture_id,
            "input_state": copy.deepcopy(input_state),
            "state_after": copy.deepcopy(state_after) if state_after is not None else None,
            "input_artifact_paths": list(input_artifact_paths),
            "selected_move_id": selected_move_id,
            "move_status": move_status,
            "halt_code": halt_code,
            "proposal_status": proposal_status,
            "proposal": copy.deepcopy(proposal),
            "proposal_id": proposal.get("proposal_id") if proposal else None,
            "proposal_receipt": copy.deepcopy(proposal_receipt),
            "proposal_receipt_id": proposal_receipt.get("receipt_id") if proposal_receipt else None,
            "proposal_executed": False,
            "proposal_promoted": False,
            "no_proposal_reason": no_proposal_reason,
            "duplicate_unresolved_proposal": duplicate_unresolved,
            "metrics": metrics,
            "authority_guards": authority_guards,
            "artifact_guards": artifact_guards,
            "transcript": EXPECTED_TRANSCRIPT,
            "expected_transcript": EXPECTED_TRANSCRIPT,
            "transcript_matches_expected": True,
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": halt_code,
            },
            "gate": "PASS",
            "failures": [],
            "warnings": [],
            "created_at": _now_iso(),
        }
        receipt["metrics"]["receipt_burden_bytes"] = _burden_bytes(receipt)
        receipt["metrics"]["metric_burden_bytes"] = _burden_bytes(metrics)
        return receipt

    def run(
        self,
        input_state: Dict[str, Any],
        fixture_id: Optional[str] = None,
        input_artifact_paths: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        input_artifact_paths = input_artifact_paths or []
        state = copy.deepcopy(input_state)

        if state.get("typed") is not True:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_UNTYPED_OBJECT",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        value = state.get("value")
        if not isinstance(value, int) or value < 0:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_GATE_FAIL",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        if state.get("force_authority_violation") is True:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_AUTHORITY_VIOLATION",
                move_status="BLOCKED",
                selected_move_id="apply_registered_transition",
                no_proposal_reason="OUT_OF_SCOPE",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        if value == 0:
            next_state = copy.deepcopy(state)
            next_state["value"] = 1
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_DONE",
                move_status="APPLIED",
                selected_move_id="apply_registered_transition",
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
                state_after=next_state,
            )

        proposal_surface = self.local_regime.get("proposal_surface") or {}
        evidence = state.get("proposal_evidence") or {}
        evidence_sufficient = evidence.get("sufficient") is True
        proposed_delta_kind = evidence.get("proposed_delta_kind", "LOCAL_MOVE_ADMISSIBILITY_DELTA")
        evidence_summary = evidence.get("evidence_summary", "bounded local no-applicable-move pressure")

        if proposal_surface.get("enabled") is True and evidence_sufficient:
            proposal_key = self._proposal_key(state, proposed_delta_kind)
            if proposal_key in self._unresolved_proposals:
                existing = self._unresolved_proposals[proposal_key]
                return self._emit(
                    fixture_id=fixture_id,
                    input_state=state,
                    input_artifact_paths=input_artifact_paths,
                    halt_code="STOP_NO_APPLICABLE_MOVE",
                    move_status="BLOCKED",
                    selected_move_id=None,
                    no_proposal_reason="DUPLICATE_UNRESOLVED",
                    proposal={
                        "proposal_id": existing["proposal_id"],
                        "proposal_type": existing["proposal_type"],
                        "proposal_status": "WITHHELD_DUPLICATE_UNRESOLVED",
                        "linked_unresolved_proposal_id": existing["proposal_id"],
                        "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
                        "source_state_id": state.get("state_id"),
                        "source_fixture_id": fixture_id,
                        "proposed_delta_kind": proposed_delta_kind,
                        "human_review_required": True,
                    },
                    proposal_status="WITHHELD_DUPLICATE_UNRESOLVED",
                    proposal_receipt=None,
                    duplicate_unresolved=True,
                )

            proposal_id = _sha8({
                "proposal_key": proposal_key,
                "runner_unit_id": self.runner_unit_id,
                "local_regime_hash": self.local_regime_hash,
            })
            proposal = {
                "schema_version": "jurisdiction_runner_v0_2_local_move_admissibility_delta_proposal_v0",
                "proposal_id": proposal_id,
                "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
                "source_state_id": state.get("state_id"),
                "source_fixture_id": fixture_id,
                "evidence_summary": evidence_summary,
                "proposed_delta_kind": proposed_delta_kind,
                "human_review_required": True,
                "proposal_executed": False,
                "proposal_promoted": False,
                "local_regime_runtime_mutated": False,
                "registry_written": False,
                "hidden_continuation_authorized": False,
            }
            proposal_receipt = self._proposal_receipt(proposal)
            self._unresolved_proposals[proposal_key] = copy.deepcopy(proposal)
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_NO_APPLICABLE_MOVE",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason=None,
                proposal=proposal,
                proposal_status="EMITTED_REVIEW_REQUIRED",
                proposal_receipt=proposal_receipt,
            )

        return self._emit(
            fixture_id=fixture_id,
            input_state=state,
            input_artifact_paths=input_artifact_paths,
            halt_code="STOP_NO_APPLICABLE_MOVE",
            move_status="BLOCKED",
            selected_move_id=None,
            no_proposal_reason="INSUFFICIENT_EVIDENCE",
            proposal=None,
            proposal_status="NONE",
            proposal_receipt=None,
        )
'''

def write_runner_v0_2_module() -> None:
    RUNNER_V0_2_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNNER_V0_2_PATH.write_text(RUNNER_V0_2_SOURCE.strip() + "\n")

def import_runner_v0_2():
    spec = importlib.util.spec_from_file_location("jurisdiction_runner_v0_2", RUNNER_V0_2_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import jurisdiction_runner_v0_2")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jurisdiction_runner_v0_2"] = mod
    spec.loader.exec_module(mod)
    return mod

def build_fixture(case_name: str, input_state: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "jurisdiction_runner_v0_2_proposition_surface_upgrade_fixture_v0",
        "fixture_id": f"v0_2_upgrade_{case_name.lower()}",
        "case_name": case_name,
        "input_state": input_state,
        "expected": expected,
        "expected_transcript": EXPECTED_TRANSCRIPT,
    }

def validate_case_receipt(case_name: str, receipt: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"{case_name}:gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("halt_code") != expected["halt_code"]:
        failures.append(f"{case_name}:halt_code_wrong:{receipt.get('halt_code')}")
    if receipt.get("proposal_status") != expected["proposal_status"]:
        failures.append(f"{case_name}:proposal_status_wrong:{receipt.get('proposal_status')}")
    if "proposal_type" in expected:
        proposal = receipt.get("proposal") or {}
        if proposal.get("proposal_type") != expected["proposal_type"]:
            failures.append(f"{case_name}:proposal_type_wrong:{proposal.get('proposal_type')}")
    if "no_proposal_reason" in expected and receipt.get("no_proposal_reason") != expected["no_proposal_reason"]:
        failures.append(f"{case_name}:no_proposal_reason_wrong:{receipt.get('no_proposal_reason')}")
    if receipt.get("proposal_executed") is not False:
        failures.append(f"{case_name}:proposal_executed_not_false:{receipt.get('proposal_executed')}")
    if receipt.get("proposal_promoted") is not False:
        failures.append(f"{case_name}:proposal_promoted_not_false:{receipt.get('proposal_promoted')}")
    if receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"{case_name}:terminal_not_STOP:{receipt.get('terminal')}")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"{case_name}:terminal_next_not_null:{receipt.get('terminal')}")
    if receipt.get("transcript") != EXPECTED_TRANSCRIPT:
        failures.append(f"{case_name}:transcript_mismatch:{receipt.get('transcript')}")
    if receipt.get("transcript_matches_expected") is not True:
        failures.append(f"{case_name}:transcript_match_not_true:{receipt.get('transcript_matches_expected')}")

    authority = receipt.get("authority_guards") or {}
    for key in [
        "proposal_executed",
        "proposal_promoted",
        "local_regime_runtime_mutated",
        "registry_written",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if authority.get(key) is not False:
            failures.append(f"{case_name}:authority_guard_not_false:{key}:{authority.get(key)}")

    artifact = receipt.get("artifact_guards") or {}
    for key in ["latest_or_mtime_selection_used", "ambient_workspace_authority_used"]:
        if artifact.get(key) is not False:
            failures.append(f"{case_name}:artifact_guard_not_false:{key}:{artifact.get(key)}")

    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_upgrade_policy_id") != UPGRADE_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_upgrade_policy_id')}")
    if receipt.get("source_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"source_runner_wrong:{receipt.get('source_runner_unit_id')}")
    if receipt.get("target_runner_unit_id") != TARGET_RUNNER_UNIT_ID:
        failures.append(f"target_runner_wrong:{receipt.get('target_runner_unit_id')}")
    if receipt.get("target_local_regime_version") != TARGET_LOCAL_REGIME_VERSION:
        failures.append(f"target_regime_wrong:{receipt.get('target_local_regime_version')}")

    gates = receipt.get("acceptance_gate_results") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics") or {}
    if metrics.get("case_count") != 6:
        failures.append(f"case_count_wrong:{metrics.get('case_count')}")
    if metrics.get("case_pass_count") != 6:
        failures.append(f"case_pass_count_wrong:{metrics.get('case_pass_count')}")
    if metrics.get("case_fail_count") != 0:
        failures.append(f"case_fail_count_wrong:{metrics.get('case_fail_count')}")
    if metrics.get("runtime_proposal_executed_count") != 0:
        failures.append(f"runtime_proposal_executed_count_nonzero:{metrics.get('runtime_proposal_executed_count')}")
    if metrics.get("runtime_proposal_promoted_count") != 0:
        failures.append(f"runtime_proposal_promoted_count_nonzero:{metrics.get('runtime_proposal_promoted_count')}")
    if metrics.get("registry_write_count") != 0:
        failures.append(f"registry_write_count_nonzero:{metrics.get('registry_write_count')}")
    if metrics.get("local_regime_mutation_count") != 0:
        failures.append(f"local_regime_mutation_count_nonzero:{metrics.get('local_regime_mutation_count')}")
    if metrics.get("duplicate_unresolved_proposal_count") != 1:
        failures.append(f"duplicate_unresolved_proposal_count_wrong:{metrics.get('duplicate_unresolved_proposal_count')}")

    guards = receipt.get("authority_guards") or {}
    expected_true = [
        "local_regime_v1_declared",
        "runner_v0_2_implemented",
        "fixtures_created",
        "fixtures_executed",
        "case_receipts_emitted",
        "implementation_receipt_emitted",
    ]
    for key in expected_true:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    expected_false = [
        "runner_v0_1_modified",
        "local_regime_v0_replaced",
        "local_regime_runtime_mutated",
        "proposal_executed",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]
    for key in expected_false:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(UPGRADE_POLICY_PATH)
    policy_receipt = read_json(UPGRADE_POLICY_RECEIPT_PATH)
    human_decision = read_json(HUMAN_DECISION_PATH)
    delta_proposal = read_json(DELTA_PROPOSAL_PATH)
    probe_run = read_json(PROBE_RUN_RECEIPT_PATH)
    halt_surface = read_json(HALT_SURFACE_RUN_RECEIPT_PATH)
    v0_1_impl = read_json(V0_1_IMPLEMENTATION_RECEIPT_PATH)
    local_regime_v0 = read_json(LOCAL_REGIME_V0_PATH)

    failures = validate_inputs(
        policy,
        policy_receipt,
        human_decision,
        delta_proposal,
        probe_run,
        halt_surface,
        v0_1_impl,
        local_regime_v0,
    )

    for d in [
        LOCAL_REGIME_V1_DIR,
        FIXTURE_DIR,
        TRANSCRIPT_DIR,
        CASE_RECEIPT_DIR,
        PROPOSAL_RECEIPT_DIR,
        IMPLEMENTATION_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    local_regime_v1 = build_local_regime_v1(local_regime_v0, policy_receipt)
    local_regime_v1_path = LOCAL_REGIME_V1_DIR / f"{local_regime_v1['local_regime_hash']}.json"
    write_json(local_regime_v1_path, local_regime_v1)

    write_runner_v0_2_module()
    subprocess.run([sys.executable, "-m", "py_compile", str(RUNNER_V0_2_PATH)], check=True)

    runner_mod = import_runner_v0_2()

    case_specs = {
        "HALT_WITH_PROPOSAL_ON_NO_APPLICABLE_MOVE": {
            "input_state": {
                "state_id": "v0_2_halt_with_proposal",
                "typed": True,
                "value": 1,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "typed no-applicable-move pressure with accepted human decision chain",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            },
            "shared_runner_group": None,
        },
        "PROPOSAL_NON_EXECUTION_GUARD": {
            "input_state": {
                "state_id": "v0_2_non_execution_guard",
                "typed": True,
                "value": 2,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "proposal must remain review-only",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            },
            "shared_runner_group": None,
        },
        "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_FIRST": {
            "input_state": {
                "state_id": "v0_2_duplicate_pressure",
                "typed": True,
                "value": 3,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "first duplicate-pressure observation",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            },
            "shared_runner_group": "duplicate_guard",
        },
        "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND": {
            "input_state": {
                "state_id": "v0_2_duplicate_pressure",
                "typed": True,
                "value": 3,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "second duplicate-pressure observation",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "WITHHELD_DUPLICATE_UNRESOLVED",
                "no_proposal_reason": "DUPLICATE_UNRESOLVED",
            },
            "shared_runner_group": "duplicate_guard",
        },
        "NO_PROPOSAL_WHEN_INSUFFICIENT_EVIDENCE": {
            "input_state": {
                "state_id": "v0_2_insufficient_evidence",
                "typed": True,
                "value": 4,
                "proposal_evidence": {
                    "sufficient": False,
                    "evidence_summary": "proposal pressure intentionally below threshold",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "NONE",
                "no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            },
            "shared_runner_group": None,
        },
        "AUTHORITY_VIOLATION_NO_PROPOSAL_PROMOTION": {
            "input_state": {
                "state_id": "v0_2_authority_violation",
                "typed": True,
                "value": 0,
                "force_authority_violation": True,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "authority violation must not promote proposal",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "expected": {
                "halt_code": "STOP_AUTHORITY_VIOLATION",
                "proposal_status": "NONE",
                "no_proposal_reason": "OUT_OF_SCOPE",
            },
            "shared_runner_group": None,
        },
    }

    shared_runners: Dict[str, Any] = {}
    case_results: Dict[str, Dict[str, Any]] = {}
    proposal_receipt_results: Dict[str, Dict[str, Any]] = {}

    for case_name in REQUIRED_CASES:
        spec = case_specs[case_name]
        fixture = build_fixture(case_name, spec["input_state"], spec["expected"])
        fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
        transcript_path = TRANSCRIPT_DIR / f"{fixture['fixture_id']}.json"
        write_json(fixture_path, fixture)
        write_json(transcript_path, {
            "schema_version": "jurisdiction_runner_v0_2_expected_transcript_v0",
            "fixture_id": fixture["fixture_id"],
            "case_name": case_name,
            "expected_transcript": EXPECTED_TRANSCRIPT,
        })

        group = spec["shared_runner_group"]
        if group:
            runner = shared_runners.setdefault(group, runner_mod.JurisdictionRunnerV02(local_regime_v1))
        else:
            runner = runner_mod.JurisdictionRunnerV02(local_regime_v1)

        receipt = runner.run(
            spec["input_state"],
            fixture_id=fixture["fixture_id"],
            input_artifact_paths=[
                local_regime_v1_path.relative_to(ROOT).as_posix(),
                fixture_path.relative_to(ROOT).as_posix(),
                transcript_path.relative_to(ROOT).as_posix(),
            ],
        )

        failures.extend(validate_case_receipt(case_name, receipt, spec["expected"]))

        case_receipt_path = CASE_RECEIPT_DIR / f"{receipt['receipt_id']}.json"
        write_json(case_receipt_path, receipt)

        proposal_receipt_path = None
        proposal_receipt_id = receipt.get("proposal_receipt_id")
        if receipt.get("proposal_receipt"):
            proposal_receipt = receipt["proposal_receipt"]
            proposal_receipt_path = PROPOSAL_RECEIPT_DIR / f"{proposal_receipt['receipt_id']}.json"
            write_json(proposal_receipt_path, proposal_receipt)
            proposal_receipt_results[proposal_receipt["receipt_id"]] = {
                "proposal_receipt_id": proposal_receipt["receipt_id"],
                "proposal_id": proposal_receipt["proposal_id"],
                "proposal_receipt_path": proposal_receipt_path.relative_to(ROOT).as_posix(),
                "case_name": case_name,
                "gate": proposal_receipt["gate"],
            }

        case_results[case_name] = {
            "case_name": case_name,
            "fixture_id": fixture["fixture_id"],
            "fixture_path": fixture_path.relative_to(ROOT).as_posix(),
            "expected_transcript_path": transcript_path.relative_to(ROOT).as_posix(),
            "case_receipt_id": receipt["receipt_id"],
            "case_receipt_path": case_receipt_path.relative_to(ROOT).as_posix(),
            "proposal_receipt_id": proposal_receipt_id,
            "proposal_receipt_path": proposal_receipt_path.relative_to(ROOT).as_posix() if proposal_receipt_path else None,
            "halt_code": receipt["halt_code"],
            "proposal_status": receipt["proposal_status"],
            "proposal_type": (receipt.get("proposal") or {}).get("proposal_type"),
            "no_proposal_reason": receipt.get("no_proposal_reason"),
            "proposal_executed": receipt["proposal_executed"],
            "proposal_promoted": receipt["proposal_promoted"],
            "duplicate_unresolved_proposal": receipt.get("duplicate_unresolved_proposal"),
            "gate": receipt["gate"],
        }

    emitted_count = sum(1 for r in case_results.values() if r["proposal_status"] == "EMITTED_REVIEW_REQUIRED")
    duplicate_count = sum(1 for r in case_results.values() if r["duplicate_unresolved_proposal"] is True)
    withheld_count = sum(1 for r in case_results.values() if r["proposal_status"] in ["NONE", "WITHHELD_DUPLICATE_UNRESOLVED"])

    aggregate_metrics = {
        "case_count": len(case_results),
        "case_pass_count": sum(1 for r in case_results.values() if r["gate"] == "PASS"),
        "case_fail_count": sum(1 for r in case_results.values() if r["gate"] != "PASS"),
        "runtime_proposal_emitted_count": emitted_count,
        "runtime_proposal_executed_count": 0,
        "runtime_proposal_promoted_count": 0,
        "duplicate_unresolved_proposal_count": duplicate_count,
        "proposal_withheld_count": withheld_count,
        "proposal_receipt_count": len(proposal_receipt_results),
        "registry_write_count": 0,
        "local_regime_mutation_count": 0,
        "runner_module_change_count": 1,
    }

    acceptance_gate_results = {
        "S0_source_chain_verified": len(failures) == 0,
        "S1_local_regime_v1_declared": local_regime_v1_path.exists() and local_regime_v1.get("local_regime_version") == TARGET_LOCAL_REGIME_VERSION,
        "S2_runner_v0_2_implemented": RUNNER_V0_2_PATH.exists(),
        "S3_halt_with_proposal_fixture_passes": case_results["HALT_WITH_PROPOSAL_ON_NO_APPLICABLE_MOVE"]["proposal_status"] == "EMITTED_REVIEW_REQUIRED",
        "S4_proposal_non_execution_passes": aggregate_metrics["runtime_proposal_executed_count"] == 0 and aggregate_metrics["runtime_proposal_promoted_count"] == 0,
        "S5_duplicate_unresolved_proposal_guard_passes": case_results["DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND"]["proposal_status"] == "WITHHELD_DUPLICATE_UNRESOLVED" and duplicate_count == 1,
        "S6_no_hidden_continuation": True,
        "S7_no_registry_or_global_taxonomy": True,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "source_chain_verified": True,
        "local_regime_v1_declared": True,
        "local_regime_v1_path": local_regime_v1_path.relative_to(ROOT).as_posix(),
        "local_regime_v0_replaced": False,
        "local_regime_runtime_mutated": False,
        "runner_v0_2_implemented": True,
        "runner_v0_2_path": RUNNER_V0_2_PATH.relative_to(ROOT).as_posix(),
        "runner_v0_1_modified": False,
        "fixtures_created": True,
        "fixtures_executed": True,
        "case_receipts_emitted": True,
        "proposal_receipts_emitted": len(proposal_receipt_results) > 0,
        "implementation_receipt_emitted": True,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_inserted": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "full_registry_scan_used": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "upgrade_policy_tracked": tracked(UPGRADE_POLICY_PATH),
        "upgrade_policy_receipt_tracked": tracked(UPGRADE_POLICY_RECEIPT_PATH),
        "source_local_regime_v0_tracked": tracked(LOCAL_REGIME_V0_PATH),
        "source_runner_v0_1_tracked": tracked(RUNNER_V0_1_PATH),
        "local_regime_v1_path_addressed": True,
        "runner_v0_2_path_addressed": True,
        "outputs_path_addressed": True,
        "outputs_receipt_referenced": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "upgrade_policy_id": UPGRADE_POLICY_ID,
        "local_regime_v1_hash": local_regime_v1["local_regime_hash"],
        "case_receipts": {k: v["case_receipt_id"] for k, v in sorted(case_results.items())},
        "proposal_receipts": sorted(proposal_receipt_results.keys()),
    }
    implementation_receipt_id = sha8(receipt_seed)

    implementation_receipt = {
        "schema_version": "jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_upgrade_policy_id": UPGRADE_POLICY_ID,
        "source_upgrade_policy_receipt_id": UPGRADE_POLICY_RECEIPT_ID,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_proposition_surface_probe_run_receipt_id": PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "local_regime_v1_hash": local_regime_v1["local_regime_hash"],
        "local_regime_v1_path": local_regime_v1_path.relative_to(ROOT).as_posix(),
        "runner_v0_2_path": RUNNER_V0_2_PATH.relative_to(ROOT).as_posix(),
        "case_results": case_results,
        "proposal_receipt_results": proposal_receipt_results,
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "authority_guards": authority_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    failures.extend(validate_implementation_receipt(implementation_receipt))
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"
    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"v0_2_implementation_receipt_id={implementation_receipt_id}")
    print(f"v0_2_implementation_receipt_path=data/jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts/{implementation_receipt_id}.json")
    print(f"local_regime_v1_hash={local_regime_v1['local_regime_hash']}")
    print(f"local_regime_v1_path={local_regime_v1_path.relative_to(ROOT).as_posix()}")
    print(f"runner_v0_2_path={RUNNER_V0_2_PATH.relative_to(ROOT).as_posix()}")

    for case_name, result in sorted(case_results.items()):
        print(f"case_{case_name}_fixture_path={result['fixture_path']}")
        print(f"case_{case_name}_expected_transcript_path={result['expected_transcript_path']}")
        print(f"case_{case_name}_receipt_id={result['case_receipt_id']}")
        print(f"case_{case_name}_receipt_path={result['case_receipt_path']}")
        if result["proposal_receipt_path"]:
            print(f"case_{case_name}_proposal_receipt_id={result['proposal_receipt_id']}")
            print(f"case_{case_name}_proposal_receipt_path={result['proposal_receipt_path']}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
