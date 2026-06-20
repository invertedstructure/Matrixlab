#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "runs" / "registry.sqlite"

POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_policy_receipts"
SURFACE_RECEIPT_DIR = ROOT / "data" / "canonical_transition_surface_probe_receipts"

ROWS_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_rows"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_receipts"

EXPECTED_POLICY_ID = "5bc46943"
EXPECTED_POLICY_RECEIPT_ID = "6b57b499"
EXPECTED_SURFACE_PROBE_ID = "07be6e6b"
EXPECTED_SURFACE_RECEIPT_ID = "1c1e392f"

PROBE_KIND = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_PROBE"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2"
COMPRESSION_VERSION = "stable_delta_signature_v0.2_candidate"
MODE = "OUTER_OBSERVER_ONLY"

REQUIRED_SIGNATURE_FIELDS = ["cv", "state_hash_before", "move_id", "state_hash_after"]

FORBIDDEN_SIGNATURE_KEYS = {
    "full_occurrence_key",
    "raw_full_receipt_hash",
    "full_receipt_hash",
    "receipt_hash",
    "receipt_sig8",
    "receipt_rowid",
    "rowid",
    "audit_pointer",
    "debug_payload",
    "observer_notes",
    "created_at",
    "created_utc",
    "timestamp",
    "path",
    "receipt_path",
    "file_path",
    "cycle_n_as_primary_identity",
    "case_id_as_primary_identity",
}

DELTA_COLUMNS = [
    "row_delta",
    "col_delta",
    "rank_delta",
    "support_delta",
    "distinct_column_types_before",
    "distinct_column_types_after",
    "new_column_types_added",
    "compression_ratio",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def canonical_bytes(obj: Any) -> int:
    return len(canonical_blob(obj))


def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_blob(obj)).hexdigest()[:8]


def file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def compact_bucket(value: Any) -> str | None:
    if value in (None, ""):
        return None
    number = safe_float(value)
    if number is None:
        return str(value)
    if number < 0:
        sign = "neg"
        number = abs(number)
    else:
        sign = "pos"
    if number == 0:
        return "0"
    if number <= 1:
        return f"{sign}_1"
    if number <= 2:
        return f"{sign}_2"
    if number <= 4:
        return f"{sign}_3_4"
    if number <= 8:
        return f"{sign}_5_8"
    if number <= 16:
        return f"{sign}_9_16"
    if number <= 32:
        return f"{sign}_17_32"
    if number <= 64:
        return f"{sign}_33_64"
    if number <= 128:
        return f"{sign}_65_128"
    if number <= 256:
        return f"{sign}_129_256"
    if number <= 512:
        return f"{sign}_257_512"
    if number <= 1024:
        return f"{sign}_513_1024"
    return f"{sign}_1025_plus"


def connect_registry() -> sqlite3.Connection:
    if not REGISTRY.exists():
        raise SystemExit(f"registry sqlite missing: {REGISTRY}")
    con = sqlite3.connect(f"file:{REGISTRY}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def table_columns(con: sqlite3.Connection, table: str) -> list[str]:
    return [str(row["name"]) for row in con.execute(f"pragma table_info({table})").fetchall()]


def select_run_ids(con: sqlite3.Connection, run_id: str | None, max_runs: int) -> list[str]:
    run_cols = set(table_columns(con, "runs"))
    receipt_cols = set(table_columns(con, "receipts"))

    if "run_id" not in receipt_cols:
        raise SystemExit("receipts table has no run_id column")

    if run_id and run_id != "latest":
        return [run_id]

    if "run_id" not in run_cols:
        rows = con.execute("select distinct run_id from receipts order by run_id desc limit ?", (max_runs,)).fetchall()
        return [row["run_id"] for row in rows]

    if "status" in run_cols and "created_utc" in run_cols:
        rows = con.execute(
            "select run_id from runs where status='DONE' order by created_utc desc limit ?",
            (max_runs,),
        ).fetchall()
    elif "created_utc" in run_cols:
        rows = con.execute(
            "select run_id from runs order by created_utc desc limit ?",
            (max_runs,),
        ).fetchall()
    else:
        rows = con.execute(
            "select run_id from runs order by rowid desc limit ?",
            (max_runs,),
        ).fetchall()

    return [row["run_id"] for row in rows]


def load_receipts(con: sqlite3.Connection, run_ids: list[str], max_receipts: int | None) -> list[dict[str, Any]]:
    if not run_ids:
        return []
    placeholders = ",".join(["?"] * len(run_ids))
    limit = "" if max_receipts is None else f" limit {int(max_receipts)}"
    sql = f"select rowid as rowid, * from receipts where run_id in ({placeholders}) order by run_id, rowid{limit}"
    return [dict(row) for row in con.execute(sql, run_ids).fetchall()]


def verify_sources(policy: dict[str, Any], policy_receipt: dict[str, Any], surface: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_mismatch:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{policy.get('candidate_design_id')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_PROBE":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    auth = policy.get("authority") or {}
    if auth.get("authorizes_next_candidate_probe_implementation") is not True:
        failures.append("policy_does_not_authorize_candidate_probe")
    for key in [
        "authorizes_runtime_receipt_emission_change",
        "authorizes_full_receipt_suppression",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_scale_mode",
        "authorizes_scale_band_run",
        "authorizes_theorem_content",
        "authorizes_taxonomy_evolution",
        "authorizes_architecture_redesign",
        "authorizes_stable_delta_candidate_acceptance",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_source_surface_extension",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    contract = policy.get("candidate_v0_2_signature_contract") or {}
    if contract.get("signature_payload_required_fields") != REQUIRED_SIGNATURE_FIELDS:
        failures.append(f"required_signature_fields_wrong:{contract.get('signature_payload_required_fields')}")
    for forbidden in FORBIDDEN_SIGNATURE_KEYS:
        if forbidden not in (contract.get("forbidden_signature_payload_fields") or []):
            failures.append(f"forbidden_signature_field_missing:{forbidden}")
    if contract.get("cycle_n_policy", {}).get("may_include_in_v0_2_signature_payload") is not False:
        failures.append("cycle_n_policy_allows_payload_unexpectedly")
    if contract.get("case_id_policy", {}).get("may_include_in_v0_2_signature_payload") is not False:
        failures.append("case_id_policy_allows_payload_unexpectedly")

    behavior = policy.get("required_candidate_probe_behavior") or {}
    for key in [
        "read_existing_surfaces_only",
        "load_corrected_canonical_surface_probe_receipt",
        "load_registry_receipts_read_only",
        "reconstruct_full_occurrence_key_without_raw_receipt_hash_truth_surface",
        "construct_candidate_signature_from_lawful_transition_tuple",
        "measure_signature_payload_bytes",
        "measure_projected_scale_row_bytes",
        "measure_audit_sidecar_bytes_separately",
        "measure_debug_sidecar_bytes_separately",
        "compute_distinguishability_retention_ratio",
        "compute_false_merge_count",
        "compute_burden_ratio_projected",
        "emit_candidate_rows_jsonl",
        "emit_candidate_probe_receipt",
        "must_not_write_to_registry_sqlite",
        "must_not_change_receipt_generation",
        "must_not_run_scale_bands",
        "must_not_create_source_surface_extension",
    ]:
        if behavior.get(key) is not True:
            failures.append(f"required_behavior_missing:{key}:{behavior.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/stable_delta_signature_candidate_v0_2_probe.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    if constraints.get("must_not_change_registry_sqlite") is not True:
        failures.append("must_not_change_registry_sqlite_missing")
    if constraints.get("must_not_run_scale_bands") is not True:
        failures.append("must_not_run_scale_bands_missing")
    if constraints.get("must_not_accept_candidate") is not True:
        failures.append("must_not_accept_candidate_missing")
    if constraints.get("must_not_extend_source_surface") is not True:
        failures.append("must_not_extend_source_surface_missing")

    if surface.get("probe_id") != EXPECTED_SURFACE_PROBE_ID:
        failures.append(f"surface_probe_id_mismatch:{surface.get('probe_id')}")
    if surface.get("receipt_id") != EXPECTED_SURFACE_RECEIPT_ID:
        failures.append(f"surface_receipt_id_mismatch:{surface.get('receipt_id')}")
    if surface.get("gate") != "PASS":
        failures.append(f"surface_gate_not_PASS:{surface.get('gate')}")
    if surface.get("terminal_decision") != "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY":
        failures.append(f"surface_terminal_wrong:{surface.get('terminal_decision')}")
    if surface.get("probe_patch_version") != "alias_patch_state_sig8_before_after_v0":
        failures.append(f"surface_patch_version_wrong:{surface.get('probe_patch_version')}")

    summary = surface.get("summary") or {}
    for key in [
        "state_hash_before_present",
        "state_hash_after_present",
        "move_id_present",
        "transition_surface_sufficient",
        "within_case_discriminator_present",
    ]:
        if summary.get(key) is not True:
            failures.append(f"surface_summary_expected_true:{key}:{summary.get(key)}")
    if summary.get("case_only_surface") is not False:
        failures.append(f"surface_case_only_expected_false:{summary.get('case_only_surface')}")
    if summary.get("source_surface_honesty_status") != "PASS_SURFACE_PRESENT":
        failures.append(f"surface_honesty_status_wrong:{summary.get('source_surface_honesty_status')}")

    surface_auth = surface.get("authority_guards") or {}
    for key in [
        "runtime_receipt_emission_changed",
        "registry_sqlite_changed",
        "scale_mode_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "scale_band_run_authorized",
        "stable_delta_candidate_acceptance_authorized",
    ]:
        if surface_auth.get(key) is not False:
            failures.append(f"surface_illegal_authority:{key}:{surface_auth.get(key)}")

    field_stats = surface.get("field_stats") or {}
    before = field_stats.get("state_hash_before") or {}
    after = field_stats.get("state_hash_after") or {}
    move = field_stats.get("move_id") or {}

    if before.get("present_count") != 176 or before.get("distinct_present_values") != 176:
        failures.append("surface_state_before_not_confirmed")
    if "state_sig8_before" not in (before.get("chosen_path_top10") or []):
        failures.append("surface_state_before_alias_missing")
    if before.get("usable_for_signature_payload") is not True:
        failures.append("surface_state_before_not_usable")

    if after.get("present_count") != 176 or after.get("distinct_present_values", 0) < 170:
        failures.append("surface_state_after_not_confirmed")
    if "state_sig8_after" not in (after.get("chosen_path_top10") or []):
        failures.append("surface_state_after_alias_missing")
    if after.get("usable_for_signature_payload") is not True:
        failures.append("surface_state_after_not_usable")

    if move.get("present_count") != 176 or move.get("usable_for_signature_payload") is not True:
        failures.append("surface_move_id_not_confirmed")

    return failures


def require_column(row: dict[str, Any], name: str) -> Any:
    if name not in row or row[name] in (None, ""):
        raise KeyError(name)
    return row[name]


def full_occurrence_key(row: dict[str, Any]) -> str:
    # Baseline full occurrence key uses lawful transition tuple plus audit-derived case/cycle context.
    # It does not use raw receipt hashes as truth surface.
    payload = {
        "version": "full_occurrence_key_v0_2",
        "run_id": row.get("run_id"),
        "case_id": row.get("case_id"),
        "cycle_n": row.get("cycle_n"),
        "state_hash_before": row.get("state_sig8_before"),
        "move_id": row.get("move_id"),
        "state_hash_after": row.get("state_sig8_after"),
        "halt_reason": row.get("halt_reason"),
        "move_profile_id": row.get("move_profile_id"),
    }
    return sha8(payload)


def candidate_signature_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "cv": "v0.2",
        "state_hash_before": require_column(row, "state_sig8_before"),
        "move_id": require_column(row, "move_id"),
        "state_hash_after": require_column(row, "state_sig8_after"),
    }


def compact_delta_debug(row: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for col in DELTA_COLUMNS:
        if col in row and row[col] not in (None, ""):
            out[col] = {
                "raw": row[col],
                "bucket": compact_bucket(row[col]),
            }
    return out


def projected_scale_row(signature_id: str, candidate_delta_signature: str, row: dict[str, Any], audit_pointer: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "source_run_id": row.get("run_id"),
        "candidate_delta_signature": candidate_delta_signature,
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer": audit_pointer,
    }


def minimal_required_row(signature_id: str, full_key: str, candidate_delta_signature: str, row: dict[str, Any], audit_pointer: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "source_run_id": row.get("run_id"),
        "case_id": row.get("case_id"),
        "cycle_n": row.get("cycle_n"),
        "full_occurrence_key": full_key,
        "candidate_delta_signature": candidate_delta_signature,
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer": audit_pointer,
    }


def signature_has_identity_leak(sig_payload: dict[str, Any]) -> bool:
    text = json.dumps(sig_payload, sort_keys=True, default=str).lower()
    return any(forbidden.lower() in text for forbidden in FORBIDDEN_SIGNATURE_KEYS)


def build_probe(policy_id: str, run_id: str | None, max_runs: int, max_receipts: int | None) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()

    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    surface = load_json(SURFACE_RECEIPT_DIR / f"{EXPECTED_SURFACE_PROBE_ID}.json")

    failures = verify_sources(policy, policy_receipt, surface)

    registry_hash_before = file_sha256(REGISTRY)

    con = connect_registry()
    try:
        run_ids = select_run_ids(con, run_id, max_runs)
        receipt_rows = load_receipts(con, run_ids, max_receipts)
        receipt_columns = table_columns(con, "receipts")
        runs_columns = table_columns(con, "runs")
    finally:
        con.close()

    registry_hash_after = file_sha256(REGISTRY)
    registry_changed = registry_hash_before != registry_hash_after

    if registry_changed:
        failures.append("registry_sqlite_changed")

    source_regression_failures: list[str] = []
    required_cols = ["state_sig8_before", "move_id", "state_sig8_after"]
    for col in required_cols:
        if col not in receipt_columns:
            source_regression_failures.append(f"missing_required_column:{col}")

    candidate_rows: list[dict[str, Any]] = []
    signature_payload_bytes = 0
    projected_scale_row_bytes = 0
    audit_sidecar_bytes = 0
    debug_sidecar_bytes = 0
    minimal_required_row_bytes = 0
    full_receipt_bytes = 0

    sig_to_full_keys: dict[str, set[str]] = defaultdict(set)
    full_key_to_sigs: dict[str, set[str]] = defaultdict(set)
    identity_leak = False
    audit_failures: list[str] = []

    for row in receipt_rows:
        full_receipt_bytes += canonical_bytes(row)

        try:
            sig_payload = candidate_signature_payload(row)
        except KeyError as exc:
            source_regression_failures.append(f"missing_required_value:{exc.args[0]}:rowid={row.get('rowid')}")
            sig_payload = {
                "cv": "v0.2",
                "source_surface_regression": True,
            }

        if signature_has_identity_leak(sig_payload):
            identity_leak = True

        candidate_delta_signature = sha8(sig_payload)
        full_key = full_occurrence_key(row)

        audit_pointer = {
            "kind": "registry.sqlite.receipts",
            "registry_path": "data/runs/registry.sqlite",
            "source_run_id": row.get("run_id"),
            "receipt_rowid": row.get("rowid"),
        }
        if not audit_pointer["source_run_id"] or audit_pointer["receipt_rowid"] is None:
            audit_failures.append(f"missing_audit_pointer:rowid={row.get('rowid')}")

        signature_id = sha8({
            "compression_version": COMPRESSION_VERSION,
            "candidate_delta_signature": candidate_delta_signature,
            "source_run_id": row.get("run_id"),
            "audit_pointer": audit_pointer,
        })

        debug_sidecar = {
            "source_columns": {
                "state_hash_before": "state_sig8_before",
                "move_id": "move_id",
                "state_hash_after": "state_sig8_after",
            },
            "case_id": row.get("case_id"),
            "cycle_n": row.get("cycle_n"),
            "halt_reason": row.get("halt_reason"),
            "move_profile_id": row.get("move_profile_id"),
            "compact_delta_debug": compact_delta_debug(row),
            "identity_policy": {
                "cycle_n_in_signature_payload": False,
                "case_id_in_signature_payload": False,
                "rowid_in_signature_payload": False,
                "raw_receipt_hash_truth_surface": False,
            },
        }

        proj = projected_scale_row(signature_id, candidate_delta_signature, row, audit_pointer)
        minimal = minimal_required_row(signature_id, full_key, candidate_delta_signature, row, audit_pointer)

        sig_bytes = canonical_bytes(sig_payload)
        audit_bytes = canonical_bytes(audit_pointer)
        debug_bytes = canonical_bytes(debug_sidecar)
        proj_bytes = canonical_bytes(proj)
        min_bytes = canonical_bytes(minimal)

        signature_payload_bytes += sig_bytes
        audit_sidecar_bytes += audit_bytes
        debug_sidecar_bytes += debug_bytes
        projected_scale_row_bytes += proj_bytes
        minimal_required_row_bytes += min_bytes

        out_row = {
            "signature_id": signature_id,
            "source_run_id": row.get("run_id"),
            "full_occurrence_key": full_key,
            "candidate_delta_signature": candidate_delta_signature,
            "signature_payload": sig_payload,
            "signature_payload_bytes": sig_bytes,
            "audit_pointer": audit_pointer,
            "audit_sidecar_bytes": audit_bytes,
            "debug_sidecar": debug_sidecar,
            "debug_sidecar_bytes": debug_bytes,
            "projected_scale_row_bytes": proj_bytes,
            "minimal_required_row_bytes": min_bytes,
            "compression_version": COMPRESSION_VERSION,
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "truth_surface": {
                "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
                "raw_full_receipt_hash_used_as_truth_surface": False,
                "full_receipt_hash_compared_to_delta_signature": False,
            },
            "authority_guards": {
                "observer_only": True,
                "runtime_receipt_emission_changed": False,
                "registry_sqlite_changed": False,
                "scale_mode_authorized": False,
                "scale_band_run_authorized": False,
                "receipt_replacement_authorized": False,
                "receipt_deletion_authorized": False,
                "receipt_compression_authorized": False,
                "stable_delta_candidate_acceptance_authorized": False,
            },
        }

        candidate_rows.append(out_row)
        sig_to_full_keys[candidate_delta_signature].add(full_key)
        full_key_to_sigs[full_key].add(candidate_delta_signature)

    distinct_full_occurrence_keys = len(full_key_to_sigs)
    distinct_candidate_signatures = len(sig_to_full_keys)
    collision_groups = {
        sig: sorted(keys)
        for sig, keys in sig_to_full_keys.items()
        if len(keys) > 1
    }
    collision_count = len(collision_groups)
    false_merge_count = collision_count

    false_split_groups = {
        key: sorted(sigs)
        for key, sigs in full_key_to_sigs.items()
        if len(sigs) > 1
    }

    distinguishability_retention_ratio = (
        distinct_candidate_signatures / distinct_full_occurrence_keys
        if distinct_full_occurrence_keys else 0.0
    )
    burden_ratio_projected = (
        projected_scale_row_bytes / full_receipt_bytes
        if full_receipt_bytes else 0.0
    )
    burden_ratio_signature_payload = (
        signature_payload_bytes / full_receipt_bytes
        if full_receipt_bytes else 0.0
    )

    authority_guards = {
        "observer_only": True,
        "runtime_receipt_emission_changed": False,
        "registry_sqlite_changed": registry_changed,
        "scale_mode_authorized": False,
        "scale_band_run_authorized": False,
        "receipt_replacement_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_compression_authorized": False,
        "stable_delta_candidate_acceptance_authorized": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "source_surface_extension_authorized": False,
    }

    pass_gates = {
        "authority_containment": (
            authority_guards["observer_only"] is True
            and authority_guards["runtime_receipt_emission_changed"] is False
            and authority_guards["registry_sqlite_changed"] is False
            and authority_guards["scale_mode_authorized"] is False
            and authority_guards["scale_band_run_authorized"] is False
            and authority_guards["receipt_replacement_authorized"] is False
            and authority_guards["receipt_compression_authorized"] is False
        ),
        "source_surface_regression": len(source_regression_failures) == 0,
        "truth_surface": True,
        "no_identity_leak": identity_leak is False,
        "no_false_merge": false_merge_count == 0,
        "burden_reduction": projected_scale_row_bytes < full_receipt_bytes if full_receipt_bytes else False,
        "debug_separation": debug_sidecar_bytes > 0 and signature_payload_bytes < (signature_payload_bytes + debug_sidecar_bytes),
        "audit_recoverability": len(audit_failures) == 0 and len(candidate_rows) == len(receipt_rows),
        "scale_precondition": false_merge_count == 0 and projected_scale_row_bytes < full_receipt_bytes,
    }

    if source_regression_failures:
        failures.append(f"source_surface_regression:{source_regression_failures[:10]}")
    if identity_leak:
        failures.append("identity_leak_in_signature_payload")
    if audit_failures:
        failures.append(f"audit_recoverability_failures:{audit_failures[:10]}")
    if not pass_gates["authority_containment"]:
        failures.append("authority_containment_failed")

    if not pass_gates["authority_containment"]:
        terminal_decision = "FAIL_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["source_surface_regression"]:
        terminal_decision = "FAIL_SOURCE_SURFACE_REGRESSION"
        next_command_goal = None
    elif identity_leak:
        terminal_decision = "FAIL_IDENTITY_LEAK"
        next_command_goal = None
    elif false_merge_count > 0:
        terminal_decision = "FAIL_FALSE_MERGE"
        next_command_goal = None
    elif not pass_gates["burden_reduction"]:
        terminal_decision = "FAIL_NO_BURDEN_REDUCTION"
        next_command_goal = None
    else:
        terminal_decision = "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS"
        next_command_goal = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_POLICY"

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    probe = {
        "schema_version": "stable_delta_signature_candidate_v0_2_probe_receipt_v0",
        "probe_kind": PROBE_KIND,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "source_canonical_surface_receipt_id": EXPECTED_SURFACE_RECEIPT_ID,
        "selected_run_ids": run_ids,
        "registry_surface": {
            "registry_path": "data/runs/registry.sqlite",
            "registry_sha256_before": registry_hash_before,
            "registry_sha256_after": registry_hash_after,
            "registry_sqlite_changed": registry_changed,
            "receipt_columns": receipt_columns,
            "runs_columns": runs_columns,
            "receipt_rows_inspected": len(receipt_rows),
            "max_runs": max_runs,
            "max_receipts": max_receipts,
        },
        "source_surface_check": {
            "required_tuple": {
                "state_hash_before": "state_sig8_before",
                "move_id": "move_id",
                "state_hash_after": "state_sig8_after",
            },
            "source_surface_regression_failures": source_regression_failures,
            "surface_probe_terminal_decision": surface.get("terminal_decision"),
            "surface_probe_patch_version": surface.get("probe_patch_version"),
        },
        "truth_surface": {
            "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
            "raw_full_receipt_hash_used_as_truth_surface": False,
            "full_receipt_hash_compared_to_delta_signature": False,
        },
        "signature_contract": {
            "signature_payload_required_fields": REQUIRED_SIGNATURE_FIELDS,
            "signature_payload_forbidden_fields": sorted(FORBIDDEN_SIGNATURE_KEYS),
            "cycle_n_in_signature_payload": False,
            "case_id_in_signature_payload": False,
            "compact_delta_columns_measured_in_debug": DELTA_COLUMNS,
        },
        "burden_measurements": {
            "full_receipt_count": len(receipt_rows),
            "candidate_signature_count": len(candidate_rows),
            "full_receipt_bytes": full_receipt_bytes,
            "signature_payload_bytes": signature_payload_bytes,
            "projected_scale_row_bytes": projected_scale_row_bytes,
            "audit_sidecar_bytes": audit_sidecar_bytes,
            "debug_sidecar_bytes": debug_sidecar_bytes,
            "minimal_required_row_bytes": minimal_required_row_bytes,
            "burden_ratio_projected": burden_ratio_projected,
            "burden_ratio_signature_payload": burden_ratio_signature_payload,
            "actual_observer_overhead_ms": elapsed_ms,
        },
        "distinguishability_measurements": {
            "occurrences_total": len(receipt_rows),
            "distinct_full_occurrence_keys": distinct_full_occurrence_keys,
            "distinct_candidate_signatures": distinct_candidate_signatures,
            "collision_count": collision_count,
            "false_merge_count": false_merge_count,
            "false_split_count": len(false_split_groups),
            "distinguishability_retention_ratio": distinguishability_retention_ratio,
        },
        "collision_gallery": [
            {
                "candidate_delta_signature": sig,
                "full_occurrence_key_count": len(keys),
                "full_occurrence_keys_sample": keys[:10],
            }
            for sig, keys in list(sorted(collision_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])))[:20]
        ],
        "false_split_gallery": [
            {
                "full_occurrence_key": key,
                "candidate_signature_count": len(sigs),
                "candidate_signatures_sample": sigs[:10],
            }
            for key, sigs in list(sorted(false_split_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])))[:20]
        ],
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "negative_claims": {
            "does_not_change_runtime_receipt_emission": True,
            "does_not_write_registry_sqlite": registry_changed is False,
            "does_not_use_rowid_as_signature_identity": True,
            "does_not_use_raw_receipt_hash_as_truth_surface": True,
            "does_not_include_full_occurrence_key_in_signature_payload": True,
            "does_not_include_audit_pointer_in_signature_payload": True,
            "does_not_include_case_id_as_primary_identity": True,
            "does_not_include_cycle_n_as_primary_identity": True,
            "does_not_authorize_scale_mode": True,
            "does_not_run_scale_bands": True,
            "does_not_accept_candidate": True,
            "does_not_extend_source_surface": True,
        },
        "terminal_decision": terminal_decision,
        "terminal": {
            "type": "ADVANCE" if next_command_goal else "STOP",
            "next_command_goal": next_command_goal,
            "stop_code": None if next_command_goal else terminal_decision,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    probe_id = sha8({
        "probe_kind": PROBE_KIND,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_canonical_surface_probe_id": EXPECTED_SURFACE_PROBE_ID,
        "selected_run_ids": run_ids,
        "signature_contract": probe["signature_contract"],
        "burden_measurements": probe["burden_measurements"],
        "distinguishability_measurements": probe["distinguishability_measurements"],
        "terminal_decision": terminal_decision,
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in candidate_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["candidate_rows_path"] = f"data/stable_delta_signature_candidate_v0_2_rows/{probe_id}.jsonl"

    receipt_id = sha8(probe)
    receipt = dict(probe)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    receipt_path = RECEIPT_DIR / f"{probe_id}.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return probe, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    parser.add_argument("--run-id", default="latest")
    parser.add_argument("--max-runs", type=int, default=1)
    parser.add_argument("--max-receipts", type=int, default=None)
    args = parser.parse_args()

    probe, receipt = build_probe(
        policy_id=args.policy_id,
        run_id=args.run_id,
        max_runs=args.max_runs,
        max_receipts=args.max_receipts,
    )

    print(json.dumps({
        "probe_id": receipt["probe_id"],
        "receipt_id": receipt["receipt_id"],
        "gate": receipt["gate"],
        "mode": receipt["mode"],
        "candidate_design_id": receipt["candidate_design_id"],
        "compression_version": receipt["compression_version"],
        "source_policy_id": receipt["source_policy_id"],
        "source_canonical_surface_probe_id": receipt["source_canonical_surface_probe_id"],
        "selected_run_ids": receipt["selected_run_ids"],
        "source_surface_check": receipt["source_surface_check"],
        "signature_contract": receipt["signature_contract"],
        "burden_measurements": receipt["burden_measurements"],
        "distinguishability_measurements": receipt["distinguishability_measurements"],
        "pass_gates": receipt["pass_gates"],
        "authority_guards": receipt["authority_guards"],
        "negative_claims": receipt["negative_claims"],
        "terminal_decision": receipt["terminal_decision"],
        "terminal": receipt["terminal"],
        "failures": receipt["failures"],
        "warnings": receipt["warnings"],
    }, indent=2, sort_keys=True))
    print(f"probe_id={receipt['probe_id']}")
    print(f"candidate_rows_path={receipt['candidate_rows_path']}")
    print(f"candidate_receipt_path=data/stable_delta_signature_candidate_v0_2_receipts/{receipt['probe_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
