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

POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_policy_receipts"
V02_PROBE_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_receipts"

ROWS_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_rows"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

EXPECTED_POLICY_ID = "b79955ce"
EXPECTED_POLICY_RECEIPT_ID = "faf978c6"
EXPECTED_V02_PROBE_ID = "bcdb3d93"

PROBE_KIND = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_BOUNDED_SCALE_BAND_PROBE"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2"
COMPRESSION_VERSION = "stable_delta_signature_v0.2_candidate"
MODE = "OUTER_OBSERVER_ONLY"

REQUIRED_SIGNATURE_FIELDS = ["cv", "state_hash_before", "move_id", "state_hash_after"]
REQUIRED_SOURCE_COLUMNS = ["state_sig8_before", "move_id", "state_sig8_after"]

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


def safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def compact_bucket(value: Any) -> str | None:
    if value in (None, ""):
        return None
    n = safe_float(value)
    if n is None:
        return str(value)
    sign = "neg" if n < 0 else "pos"
    n = abs(n)
    if n == 0:
        return "0"
    if n <= 1:
        return f"{sign}_1"
    if n <= 2:
        return f"{sign}_2"
    if n <= 4:
        return f"{sign}_3_4"
    if n <= 8:
        return f"{sign}_5_8"
    if n <= 16:
        return f"{sign}_9_16"
    if n <= 32:
        return f"{sign}_17_32"
    if n <= 64:
        return f"{sign}_33_64"
    if n <= 128:
        return f"{sign}_65_128"
    if n <= 256:
        return f"{sign}_129_256"
    if n <= 512:
        return f"{sign}_257_512"
    if n <= 1024:
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


def runs_order_query(con: sqlite3.Connection, *, limit: int | None, descending: bool) -> list[str]:
    run_cols = set(table_columns(con, "runs"))
    direction = "desc" if descending else "asc"

    if "run_id" in run_cols:
        if "created_utc" in run_cols:
            sql = f"select run_id from runs order by created_utc {direction}"
        else:
            sql = f"select run_id from runs order by rowid {direction}"
        if limit is not None:
            rows = con.execute(sql + " limit ?", (limit,)).fetchall()
        else:
            rows = con.execute(sql).fetchall()
        return [row["run_id"] for row in rows]

    sql = f"select distinct run_id from receipts order by run_id {direction}"
    if limit is not None:
        rows = con.execute(sql + " limit ?", (limit,)).fetchall()
    else:
        rows = con.execute(sql).fetchall()
    return [row["run_id"] for row in rows]


def total_run_count_estimate(con: sqlite3.Connection) -> int | None:
    try:
        run_cols = set(table_columns(con, "runs"))
        if "run_id" in run_cols:
            return int(con.execute("select count(*) as n from runs").fetchone()["n"])
        return int(con.execute("select count(distinct run_id) as n from receipts").fetchone()["n"])
    except Exception:
        return None


def selected_bounded_run_ids(
    con: sqlite3.Connection,
    *,
    source_run_id: str,
    latest_compatible_runs: int,
    full_registry: bool,
) -> tuple[list[str], dict[str, Any]]:
    if latest_compatible_runs < 1:
        raise SystemExit("--latest-compatible-runs must be >= 1")
    if latest_compatible_runs > 25 and not full_registry:
        raise SystemExit("--latest-compatible-runs > 25 requires --full-registry or an explicit policy revision")

    if full_registry:
        base = runs_order_query(con, limit=None, descending=True)
    else:
        base = runs_order_query(con, limit=latest_compatible_runs, descending=True)

    selected: list[str] = []
    for run_id in [source_run_id] + base:
        if run_id and run_id not in selected:
            selected.append(run_id)

    estimate = total_run_count_estimate(con)
    skipped = None if estimate is None else max(0, estimate - len(selected))

    return selected, {
        "selection_mode": "FULL_REGISTRY_EXPLICIT" if full_registry else "BOUNDED_BY_DEFAULT",
        "source_run_id": source_run_id,
        "source_run_included": source_run_id in selected,
        "latest_compatible_runs_requested": latest_compatible_runs,
        "full_registry_used": full_registry,
        "full_registry_requires_explicit_flag": True,
        "selected_run_ids": selected,
        "selected_run_count": len(selected),
        "default_full_registry_scan": False,
        "total_compatible_run_count_estimate_if_known": estimate,
        "skipped_compatible_run_count": skipped,
        "bounded_default_max_registry_runs_touched": latest_compatible_runs + 1,
    }


def load_receipts_for_runs(con: sqlite3.Connection, run_ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    if not run_ids:
        return {}

    placeholders = ",".join(["?"] * len(run_ids))
    rows = con.execute(
        f"select rowid as rowid, * from receipts where run_id in ({placeholders}) order by run_id, rowid",
        run_ids,
    ).fetchall()

    by_run: dict[str, list[dict[str, Any]]] = {run_id: [] for run_id in run_ids}
    for row in rows:
        d = dict(row)
        by_run.setdefault(str(d.get("run_id")), []).append(d)
    return by_run


def required_values_present(row: dict[str, Any]) -> bool:
    return all(col in row and row[col] not in (None, "") for col in REQUIRED_SOURCE_COLUMNS)


def compatible_selected_rows(
    con: sqlite3.Connection,
    run_ids: list[str],
) -> tuple[list[str], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    receipt_cols = table_columns(con, "receipts")
    missing_cols = [col for col in REQUIRED_SOURCE_COLUMNS if col not in receipt_cols]
    rows_by_run_raw = load_receipts_for_runs(con, run_ids)

    compatible: list[str] = []
    rows_by_run: dict[str, list[dict[str, Any]]] = {}
    rejected: dict[str, Any] = {}

    for run_id in run_ids:
        rows = rows_by_run_raw.get(run_id) or []
        if not rows:
            rejected[run_id] = {"reason": "no_receipts"}
            continue
        if missing_cols:
            rejected[run_id] = {"reason": "missing_required_columns", "missing_columns": missing_cols, "rows": len(rows)}
            continue

        missing_values = sum(1 for row in rows if not required_values_present(row))
        if missing_values:
            rejected[run_id] = {"reason": "missing_required_values", "missing_value_rows": missing_values, "rows": len(rows)}
            continue

        compatible.append(run_id)
        rows_by_run[run_id] = rows

    return compatible, rows_by_run, {
        "receipt_columns": receipt_cols,
        "missing_required_columns": missing_cols,
        "rejected_selected_runs": rejected,
        "selected_run_ids_pre_compatibility": run_ids,
    }


def full_occurrence_key(row: dict[str, Any]) -> str:
    return sha8({
        "version": "full_occurrence_key_v0_2_bounded_scale_band",
        "run_id": row.get("run_id"),
        "case_id": row.get("case_id"),
        "cycle_n": row.get("cycle_n"),
        "state_hash_before": row.get("state_sig8_before"),
        "move_id": row.get("move_id"),
        "state_hash_after": row.get("state_sig8_after"),
        "halt_reason": row.get("halt_reason"),
        "move_profile_id": row.get("move_profile_id"),
    })


def candidate_signature_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "cv": "v0.2",
        "state_hash_before": row["state_sig8_before"],
        "move_id": row["move_id"],
        "state_hash_after": row["state_sig8_after"],
    }


def signature_has_identity_leak(sig_payload: dict[str, Any]) -> bool:
    text = json.dumps(sig_payload, sort_keys=True, default=str).lower()
    return any(key.lower() in text for key in FORBIDDEN_SIGNATURE_KEYS)


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


def make_bands(rows_by_run: dict[str, list[dict[str, Any]]], source_run_id: str | None) -> list[dict[str, Any]]:
    bands: list[dict[str, Any]] = []

    for run_id, rows in rows_by_run.items():
        if source_run_id and run_id == source_run_id:
            bands.append({
                "band_id": sha8({"axis": "local_run_replay", "run_id": run_id}),
                "axis": "local_run_replay",
                "axis_value": run_id,
                "run_id": run_id,
                "rows": rows,
            })

        bands.append({
            "band_id": sha8({"axis": "available_run_ids", "run_id": run_id}),
            "axis": "available_run_ids",
            "axis_value": run_id,
            "run_id": run_id,
            "rows": rows,
        })

        for axis, col in [
            ("depth", "depth"),
            ("cycle_n", "cycle_n"),
            ("family", "family"),
            ("case_id", "case_id"),
        ]:
            groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for row in rows:
                if col in row and row[col] not in (None, ""):
                    groups[str(row[col])].append(row)
            for value, group_rows in sorted(groups.items(), key=lambda kv: kv[0]):
                bands.append({
                    "band_id": sha8({"axis": axis, "run_id": run_id, "value": value}),
                    "axis": axis,
                    "axis_value": value,
                    "run_id": run_id,
                    "rows": group_rows,
                })

        bands.append({
            "band_id": sha8({"axis": "receipt_count", "run_id": run_id, "value": len(rows)}),
            "axis": "receipt_count",
            "axis_value": str(len(rows)),
            "run_id": run_id,
            "rows": rows,
        })

        if any("cells" in row for row in rows):
            groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for row in rows:
                bucket = compact_bucket(row.get("cells"))
                if bucket is not None:
                    groups[bucket].append(row)
            for value, group_rows in sorted(groups.items(), key=lambda kv: kv[0]):
                bands.append({
                    "band_id": sha8({"axis": "raw/cell size fields if present", "run_id": run_id, "value": value}),
                    "axis": "raw/cell size fields if present",
                    "axis_value": value,
                    "run_id": run_id,
                    "rows": group_rows,
                })

    seen = set()
    unique = []
    for band in bands:
        if band["band_id"] in seen:
            continue
        seen.add(band["band_id"])
        unique.append(band)
    return unique


def measure_band(band: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = band["rows"]

    full_receipt_bytes = 0
    signature_payload_bytes = 0
    projected_scale_row_bytes = 0
    audit_sidecar_bytes = 0
    debug_sidecar_bytes = 0

    source_surface_regression_count = 0
    identity_leak_count = 0
    audit_recoverability_failures = 0

    sig_to_full: dict[str, set[str]] = defaultdict(set)
    full_to_sig: dict[str, set[str]] = defaultdict(set)
    out_rows: list[dict[str, Any]] = []

    for row in rows:
        full_receipt_bytes += canonical_bytes(row)

        if not required_values_present(row):
            source_surface_regression_count += 1
            continue

        sig_payload = candidate_signature_payload(row)
        if signature_has_identity_leak(sig_payload):
            identity_leak_count += 1

        candidate_delta_signature = sha8(sig_payload)
        full_key = full_occurrence_key(row)

        audit_pointer = {
            "kind": "registry.sqlite.receipts",
            "registry_path": "data/runs/registry.sqlite",
            "source_run_id": row.get("run_id"),
            "receipt_rowid": row.get("rowid"),
        }
        if not audit_pointer["source_run_id"] or audit_pointer["receipt_rowid"] is None:
            audit_recoverability_failures += 1

        signature_id = sha8({
            "compression_version": COMPRESSION_VERSION,
            "candidate_delta_signature": candidate_delta_signature,
            "source_run_id": row.get("run_id"),
            "audit_pointer": audit_pointer,
        })

        debug_sidecar = {
            "band_id": band["band_id"],
            "axis": band["axis"],
            "axis_value": band["axis_value"],
            "case_id_debug_only": row.get("case_id"),
            "cycle_n_debug_only": row.get("cycle_n"),
            "depth_debug_only": row.get("depth"),
            "family_debug_only": row.get("family"),
            "halt_reason": row.get("halt_reason"),
            "move_profile_id": row.get("move_profile_id"),
            "compact_delta_debug": compact_delta_debug(row),
            "identity_policy": {
                "case_id_in_signature_payload": False,
                "cycle_n_in_signature_payload": False,
                "rowid_in_signature_payload": False,
                "raw_receipt_hash_truth_surface": False,
            },
        }

        proj = projected_scale_row(signature_id, candidate_delta_signature, row, audit_pointer)

        sig_bytes = canonical_bytes(sig_payload)
        proj_bytes = canonical_bytes(proj)
        audit_bytes = canonical_bytes(audit_pointer)
        debug_bytes = canonical_bytes(debug_sidecar)

        signature_payload_bytes += sig_bytes
        projected_scale_row_bytes += proj_bytes
        audit_sidecar_bytes += audit_bytes
        debug_sidecar_bytes += debug_bytes

        sig_to_full[candidate_delta_signature].add(full_key)
        full_to_sig[full_key].add(candidate_delta_signature)

        out_rows.append({
            "scale_band_row_id": sha8({
                "band_id": band["band_id"],
                "source_run_id": row.get("run_id"),
                "receipt_rowid": row.get("rowid"),
                "candidate_delta_signature": candidate_delta_signature,
            }),
            "band_id": band["band_id"],
            "axis": band["axis"],
            "axis_value": band["axis_value"],
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
                "candidate_acceptance_authorized": False,
                "receipt_replacement_authorized": False,
                "receipt_compression_authorized": False,
            },
        })

    collision_groups = {sig: keys for sig, keys in sig_to_full.items() if len(keys) > 1}
    false_split_groups = {key: sigs for key, sigs in full_to_sig.items() if len(sigs) > 1}

    distinct_full = len(full_to_sig)
    distinct_sig = len(sig_to_full)
    burden_ratio_projected = projected_scale_row_bytes / full_receipt_bytes if full_receipt_bytes else 0.0
    burden_ratio_signature_payload = signature_payload_bytes / full_receipt_bytes if full_receipt_bytes else 0.0
    retention = distinct_sig / distinct_full if distinct_full else 0.0

    passed = (
        source_surface_regression_count == 0
        and identity_leak_count == 0
        and audit_recoverability_failures == 0
        and len(collision_groups) == 0
        and len(false_split_groups) == 0
        and projected_scale_row_bytes < full_receipt_bytes
        and full_receipt_bytes > 0
    )

    return {
        "band_id": band["band_id"],
        "run_id": band["run_id"],
        "axis": band["axis"],
        "axis_value": band["axis_value"],
        "occurrences_total": len(rows),
        "distinct_full_occurrence_keys": distinct_full,
        "distinct_candidate_signatures": distinct_sig,
        "collision_count": len(collision_groups),
        "false_merge_count": len(collision_groups),
        "false_split_count": len(false_split_groups),
        "distinguishability_retention_ratio": retention,
        "full_receipt_bytes": full_receipt_bytes,
        "signature_payload_bytes": signature_payload_bytes,
        "projected_scale_row_bytes": projected_scale_row_bytes,
        "audit_sidecar_bytes": audit_sidecar_bytes,
        "debug_sidecar_bytes": debug_sidecar_bytes,
        "burden_ratio_projected": burden_ratio_projected,
        "burden_ratio_signature_payload": burden_ratio_signature_payload,
        "source_surface_regression_count": source_surface_regression_count,
        "identity_leak_count": identity_leak_count,
        "audit_recoverability_failures": audit_recoverability_failures,
        "observer_overhead_ms": 0,
        "band_passed": passed,
        "failure_reasons": [
            reason
            for reason, condition in [
                ("source_surface_regression", source_surface_regression_count > 0),
                ("identity_leak", identity_leak_count > 0),
                ("audit_recoverability", audit_recoverability_failures > 0),
                ("false_merge", len(collision_groups) > 0),
                ("false_split", len(false_split_groups) > 0),
                ("burden_regression", not (projected_scale_row_bytes < full_receipt_bytes and full_receipt_bytes > 0)),
            ]
            if condition
        ],
    }, out_rows


def verify_policy(policy: dict[str, Any], policy_receipt: dict[str, Any], v02_probe: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_mismatch:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_SCALE_BAND_PROBE":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    selection = policy.get("bounded_scale_band_selection") or {}
    if selection.get("selection_mode") != "BOUNDED_BY_DEFAULT":
        failures.append(f"selection_mode_wrong:{selection.get('selection_mode')}")
    if selection.get("default_full_registry_scan") is not False:
        failures.append("default_full_registry_scan_not_false")
    if selection.get("full_registry_scan_forbidden_without_flag") is not True:
        failures.append("full_registry_scan_forbidden_without_flag_not_true")
    if selection.get("full_registry_requires_explicit_flag") != "--full-registry":
        failures.append(f"full_registry_flag_wrong:{selection.get('full_registry_requires_explicit_flag')}")
    default_n = selection.get("default_latest_compatible_runs")
    if not isinstance(default_n, int) or default_n < 1 or default_n > 25:
        failures.append(f"default_latest_compatible_runs_out_of_bounds:{default_n}")
    if selection.get("source_run_must_always_be_included") is not True:
        failures.append("source_run_must_always_be_included_not_true")

    auth = policy.get("authority") or {}
    if auth.get("authorizes_next_scale_band_probe_implementation") is not True:
        failures.append("policy_does_not_authorize_scale_band_probe_implementation")
    if auth.get("authorizes_scale_band_probe_execution") is not True:
        failures.append("policy_does_not_authorize_scale_band_probe_execution")
    if auth.get("authorizes_full_registry_scan_by_default") is not False:
        failures.append("policy_authorizes_full_registry_by_default")
    if auth.get("authorizes_full_registry_scan_with_explicit_flag") is not True:
        failures.append("policy_does_not_authorize_explicit_full_registry_flag")
    for key in [
        "authorizes_scale_band_run",
        "authorizes_scale_mode",
        "authorizes_candidate_acceptance",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_registry_write",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_source_surface_extension",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    behavior = policy.get("required_probe_behavior") or {}
    for key in [
        "read_existing_registry_only",
        "load_v02_local_probe_receipt",
        "replay_v02_signature_logic_across_compatible_runs",
        "emit_scale_band_rows_jsonl",
        "emit_scale_band_probe_receipt",
        "measure_per_band_burden_and_distinguishability",
        "measure_aggregate_worst_case",
        "classify_insufficient_scale_coverage_honestly",
        "must_not_write_registry_sqlite",
        "must_not_change_runtime_receipt_generation",
        "must_not_authorize_scale_mode",
        "must_not_accept_candidate",
        "must_not_replace_or_suppress_receipts",
        "must_not_use_raw_receipt_hash_truth_surface",
        "must_not_use_rowid_as_signature_identity",
        "must_not_use_cycle_n_or_case_id_as_primary_signature_identity",
        "include_v02_selected_source_run",
        "include_latest_n_compatible_runs_by_default",
        "do_not_scan_all_registry_runs_by_default",
        "require_full_registry_flag_for_all_runs",
        "record_bounded_selection_receipt_fields",
    ]:
        if behavior.get(key) is not True:
            failures.append(f"required_behavior_missing:{key}:{behavior.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    if constraints.get("must_not_scan_all_registry_runs_by_default") is not True:
        failures.append("must_not_scan_all_registry_runs_by_default_missing")
    if constraints.get("full_registry_requires_explicit_flag") is not True:
        failures.append("full_registry_requires_explicit_flag_missing")
    if constraints.get("default_latest_compatible_runs") != default_n:
        failures.append("default_latest_compatible_runs_mismatch_between_selection_and_constraints")

    if v02_probe.get("probe_id") != EXPECTED_V02_PROBE_ID:
        failures.append(f"v02_probe_id_mismatch:{v02_probe.get('probe_id')}")
    if v02_probe.get("gate") != "PASS":
        failures.append(f"v02_probe_gate_not_PASS:{v02_probe.get('gate')}")
    if v02_probe.get("terminal_decision") != "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS":
        failures.append(f"v02_probe_terminal_wrong:{v02_probe.get('terminal_decision')}")

    local = v02_probe.get("distinguishability_measurements") or {}
    if local.get("false_merge_count") != 0:
        failures.append(f"v02_local_false_merge_not_zero:{local.get('false_merge_count')}")
    if local.get("false_split_count") != 0:
        failures.append(f"v02_local_false_split_not_zero:{local.get('false_split_count')}")
    if local.get("distinguishability_retention_ratio") != 1.0:
        failures.append(f"v02_local_retention_not_one:{local.get('distinguishability_retention_ratio')}")

    burden = v02_probe.get("burden_measurements") or {}
    if burden.get("burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"v02_local_burden_not_reduced:{burden.get('burden_ratio_projected')}")

    return failures


def build_probe(policy_id: str, latest_compatible_runs: int | None, full_registry: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    v02_probe = load_json(V02_PROBE_DIR / f"{EXPECTED_V02_PROBE_ID}.json")

    failures = verify_policy(policy, policy_receipt, v02_probe)

    selection_policy = policy.get("bounded_scale_band_selection") or {}
    default_n = int(selection_policy.get("default_latest_compatible_runs", 10))
    latest_n = latest_compatible_runs if latest_compatible_runs is not None else default_n

    source_run_ids = v02_probe.get("selected_run_ids") or []
    source_run_id = source_run_ids[0] if source_run_ids else None
    if not source_run_id:
        failures.append("missing_source_run_id_from_v02_probe")
        source_run_id = ""

    if latest_n < 1:
        failures.append(f"latest_compatible_runs_must_be_positive:{latest_n}")
    if latest_n > 25 and not full_registry:
        failures.append(f"latest_compatible_runs_above_25_requires_full_registry:{latest_n}")

    registry_hash_before = file_sha256(REGISTRY)

    con = connect_registry()
    try:
        if failures:
            selected_run_ids, selection = [], {
                "selection_mode": "INVALID_PRECONDITION",
                "source_run_id": source_run_id,
                "source_run_included": False,
                "latest_compatible_runs_requested": latest_n,
                "full_registry_used": full_registry,
                "selected_run_ids": [],
                "selected_run_count": 0,
                "total_compatible_run_count_estimate_if_known": None,
                "skipped_compatible_run_count": None,
            }
            compatible_run_ids, rows_by_run, compatibility = [], {}, {
                "receipt_columns": table_columns(con, "receipts"),
                "rejected_selected_runs": {},
                "selected_run_ids_pre_compatibility": [],
            }
        else:
            selected_run_ids, selection = selected_bounded_run_ids(
                con,
                source_run_id=source_run_id,
                latest_compatible_runs=latest_n,
                full_registry=full_registry,
            )
            compatible_run_ids, rows_by_run, compatibility = compatible_selected_rows(con, selected_run_ids)

        runs_columns = table_columns(con, "runs")
    finally:
        con.close()

    if source_run_id and source_run_id not in compatible_run_ids:
        failures.append(f"source_run_not_compatible_or_not_selected:{source_run_id}")

    registry_hash_after = file_sha256(REGISTRY)
    registry_changed = registry_hash_before != registry_hash_after
    if registry_changed:
        failures.append("registry_sqlite_changed")

    bands = make_bands(rows_by_run, source_run_id=source_run_id)

    band_measurements: list[dict[str, Any]] = []
    scale_rows: list[dict[str, Any]] = []

    for band in bands:
        band_start = time.perf_counter()
        measurement, rows = measure_band(band)
        measurement["observer_overhead_ms"] = int(round((time.perf_counter() - band_start) * 1000))
        band_measurements.append(measurement)
        scale_rows.extend(rows)

    bands_total = len(band_measurements)
    bands_passed = sum(1 for b in band_measurements if b["band_passed"])
    bands_failed = bands_total - bands_passed

    worst_false_merge_count = max((b["false_merge_count"] for b in band_measurements), default=0)
    worst_collision_count = max((b["collision_count"] for b in band_measurements), default=0)
    worst_retention = min((b["distinguishability_retention_ratio"] for b in band_measurements), default=0.0)
    worst_burden_ratio = max((b["burden_ratio_projected"] for b in band_measurements), default=0.0)
    worst_source_surface_regression = max((b["source_surface_regression_count"] for b in band_measurements), default=0)
    worst_identity_leak = max((b["identity_leak_count"] for b in band_measurements), default=0)
    worst_audit_failures = max((b["audit_recoverability_failures"] for b in band_measurements), default=0)

    compatible_run_count = len(compatible_run_ids)

    if full_registry:
        scale_coverage_status = "FULL_REGISTRY_EXPLICIT_MULTI_RUN" if compatible_run_count >= 2 else "FULL_REGISTRY_EXPLICIT_INSUFFICIENT_COMPATIBLE_RUNS"
    elif compatible_run_count >= 2:
        scale_coverage_status = "BOUNDED_MULTI_RUN_COMPATIBLE"
    else:
        scale_coverage_status = "LOCAL_REPLAY_ONLY_INSUFFICIENT_SCALE_COVERAGE"

    authority_guards = {
        "observer_only": True,
        "runtime_receipt_emission_changed": False,
        "registry_sqlite_changed": registry_changed,
        "scale_mode_authorized": False,
        "scale_band_run_authorized": False,
        "candidate_acceptance_authorized": False,
        "registry_write_authorized": False,
        "receipt_replacement_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_compression_authorized": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "full_registry_scan_used": full_registry,
        "full_registry_scan_authorized_by_explicit_flag": full_registry,
    }

    pass_gates = {
        "authority_containment": (
            authority_guards["observer_only"] is True
            and authority_guards["runtime_receipt_emission_changed"] is False
            and authority_guards["registry_sqlite_changed"] is False
            and authority_guards["scale_mode_authorized"] is False
            and authority_guards["candidate_acceptance_authorized"] is False
            and authority_guards["registry_write_authorized"] is False
        ),
        "bounded_selection": (
            full_registry is True
            or (
                selection.get("full_registry_used") is False
                and selection.get("source_run_included") is True
                and selection.get("selected_run_count", 10**9) <= latest_n + 1
            )
        ),
        "local_precondition_preserved": True,
        "source_surface_regression": worst_source_surface_regression == 0,
        "truth_surface": True,
        "no_identity_leak": worst_identity_leak == 0,
        "audit_recoverability": worst_audit_failures == 0,
        "no_false_merge_all_bands": worst_false_merge_count == 0,
        "burden_reduction_all_bands": worst_burden_ratio < 1.0 and bands_total > 0,
        "scale_coverage_honesty": True,
    }

    if not pass_gates["authority_containment"]:
        terminal_decision = "FAIL_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["bounded_selection"]:
        terminal_decision = "FAIL_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["source_surface_regression"]:
        terminal_decision = "FAIL_SOURCE_SURFACE_REGRESSION"
        next_command_goal = None
    elif not pass_gates["no_identity_leak"]:
        terminal_decision = "FAIL_IDENTITY_LEAK"
        next_command_goal = None
    elif not pass_gates["audit_recoverability"]:
        terminal_decision = "FAIL_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["no_false_merge_all_bands"]:
        terminal_decision = "FAIL_SCALE_FALSE_MERGE"
        next_command_goal = None
    elif not pass_gates["burden_reduction_all_bands"]:
        terminal_decision = "FAIL_SCALE_BURDEN_REGRESSION"
        next_command_goal = None
    elif compatible_run_count < 2:
        terminal_decision = "PASS_LOCAL_REPLAY_ONLY_INSUFFICIENT_SCALE_COVERAGE"
        next_command_goal = "BUILD_COMPATIBLE_SCALE_COVERAGE_EXPANSION_POLICY_V0"
    elif full_registry:
        terminal_decision = "PASS_SCALE_BANDS_OBSERVER_ONLY"
        next_command_goal = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_FULL_REGISTRY_REVIEW_POLICY"
    else:
        terminal_decision = "PASS_SCALE_BANDS_OBSERVER_ONLY"
        next_command_goal = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_BOUNDED_SCALE_REVIEW_POLICY"

    pass_gates["scale_coverage_honesty"] = (
        (compatible_run_count < 2 and terminal_decision == "PASS_LOCAL_REPLAY_ONLY_INSUFFICIENT_SCALE_COVERAGE")
        or (compatible_run_count >= 2 and terminal_decision in {
            "PASS_SCALE_BANDS_OBSERVER_ONLY",
            "FAIL_SCALE_FALSE_MERGE",
            "FAIL_SCALE_BURDEN_REGRESSION",
            "FAIL_SOURCE_SURFACE_REGRESSION",
            "FAIL_IDENTITY_LEAK",
            "FAIL_OBSERVER_INTERFERENCE",
        })
    )

    if not pass_gates["scale_coverage_honesty"]:
        failures.append("scale_coverage_honesty_failed")

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    probe = {
        "schema_version": "stable_delta_signature_candidate_v0_2_bounded_scale_band_probe_receipt_v0",
        "probe_kind": PROBE_KIND,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_v02_probe_id": EXPECTED_V02_PROBE_ID,
        "bounded_scale_band_selection": selection,
        "registry_surface": {
            "registry_path": "data/runs/registry.sqlite",
            "registry_sha256_before": registry_hash_before,
            "registry_sha256_after": registry_hash_after,
            "registry_sqlite_changed": registry_changed,
            "receipt_columns": compatibility.get("receipt_columns"),
            "runs_columns": runs_columns,
            "selected_run_ids_pre_compatibility": compatibility.get("selected_run_ids_pre_compatibility"),
            "compatible_run_ids": compatible_run_ids,
            "compatible_run_count": compatible_run_count,
            "rejected_selected_runs": compatibility.get("rejected_selected_runs"),
        },
        "signature_contract": {
            "candidate_signature_payload_required_fields": REQUIRED_SIGNATURE_FIELDS,
            "candidate_signature_payload_forbidden_fields": sorted(FORBIDDEN_SIGNATURE_KEYS),
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "cycle_n_in_signature_payload": False,
            "case_id_in_signature_payload": False,
            "compact_delta_columns_measured_in_debug": DELTA_COLUMNS,
        },
        "scale_coverage": {
            "scale_coverage_status": scale_coverage_status,
            "compatible_run_count": compatible_run_count,
            "compatible_run_ids": compatible_run_ids,
            "bands_total": bands_total,
            "band_axes": sorted({b["axis"] for b in band_measurements}),
            "local_replay_included": any(b["axis"] == "local_run_replay" for b in band_measurements),
            "full_registry_used": full_registry,
            "bounded_default_used": not full_registry,
        },
        "aggregate_measurements": {
            "bands_total": bands_total,
            "bands_passed": bands_passed,
            "bands_failed": bands_failed,
            "worst_false_merge_count": worst_false_merge_count,
            "worst_collision_count": worst_collision_count,
            "worst_distinguishability_retention_ratio": worst_retention,
            "worst_burden_ratio_projected": worst_burden_ratio,
            "worst_source_surface_regression_count": worst_source_surface_regression,
            "worst_identity_leak_count": worst_identity_leak,
            "worst_audit_recoverability_failures": worst_audit_failures,
            "scale_coverage_status": scale_coverage_status,
            "compatible_run_count": compatible_run_count,
            "actual_observer_overhead_ms": elapsed_ms,
        },
        "band_measurements": band_measurements,
        "failed_band_gallery": [b for b in band_measurements if not b["band_passed"]][:20],
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "negative_claims": {
            "does_not_change_runtime_receipt_emission": True,
            "does_not_write_registry_sqlite": registry_changed is False,
            "does_not_scan_all_registry_by_default": full_registry is False,
            "does_not_use_rowid_as_signature_identity": True,
            "does_not_use_raw_receipt_hash_as_truth_surface": True,
            "does_not_include_full_occurrence_key_in_signature_payload": True,
            "does_not_include_audit_pointer_in_signature_payload": True,
            "does_not_include_case_id_as_primary_identity": True,
            "does_not_include_cycle_n_as_primary_identity": True,
            "does_not_authorize_scale_mode": True,
            "does_not_authorize_candidate_acceptance": True,
            "does_not_replace_or_suppress_receipts": True,
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
        "source_v02_probe_id": EXPECTED_V02_PROBE_ID,
        "bounded_scale_band_selection": selection,
        "scale_coverage": probe["scale_coverage"],
        "aggregate_measurements": probe["aggregate_measurements"],
        "terminal_decision": terminal_decision,
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in scale_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["scale_band_rows_path"] = f"data/stable_delta_signature_candidate_v0_2_scale_band_rows/{probe_id}.jsonl"

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
    parser.add_argument("--latest-compatible-runs", type=int, default=None)
    parser.add_argument("--full-registry", action="store_true")
    args = parser.parse_args()

    probe, receipt = build_probe(
        policy_id=args.policy_id,
        latest_compatible_runs=args.latest_compatible_runs,
        full_registry=args.full_registry,
    )

    print(json.dumps({
        "probe_id": receipt["probe_id"],
        "receipt_id": receipt["receipt_id"],
        "gate": receipt["gate"],
        "mode": receipt["mode"],
        "candidate_design_id": receipt["candidate_design_id"],
        "compression_version": receipt["compression_version"],
        "source_policy_id": receipt["source_policy_id"],
        "source_v02_probe_id": receipt["source_v02_probe_id"],
        "bounded_scale_band_selection": receipt["bounded_scale_band_selection"],
        "registry_surface": receipt["registry_surface"],
        "scale_coverage": receipt["scale_coverage"],
        "aggregate_measurements": receipt["aggregate_measurements"],
        "signature_contract": receipt["signature_contract"],
        "pass_gates": receipt["pass_gates"],
        "authority_guards": receipt["authority_guards"],
        "negative_claims": receipt["negative_claims"],
        "terminal_decision": receipt["terminal_decision"],
        "terminal": receipt["terminal"],
        "failures": receipt["failures"],
        "warnings": receipt["warnings"],
    }, indent=2, sort_keys=True))
    print(f"probe_id={receipt['probe_id']}")
    print(f"scale_band_rows_path={receipt['scale_band_rows_path']}")
    print(f"scale_band_receipt_path=data/stable_delta_signature_candidate_v0_2_scale_band_receipts/{receipt['probe_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
