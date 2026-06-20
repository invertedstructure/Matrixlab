#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "runs" / "registry.sqlite"

ROWS_DIR = ROOT / "data" / "stable_delta_signature_probe_rows"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_probe_receipts"

COMPRESSION_VERSION = "stable_delta_signature_v0.2"
PROBE_NAME = "stable_delta_signature_probe_v0"
MODE = "OUTER_OBSERVER_ONLY"

NOISE_FIELD_NAMES = {
    "created_at",
    "created_utc",
    "updated_at",
    "timestamp",
    "receipt_file",
    "path",
    "file_path",
    "csv_path",
    "profile_path",
    "receipt_path",
    "run_path",
    "raw_full_receipt_hash",
    "full_receipt_hash",
    "receipt_hash",
    "receipt_sig8",
    "sig8",
}

OCCURRENCE_KEY_CANDIDATES = {
    "case_id": ["case_id", "fixture_id", "case_key", "case", "fixture", "slot_id"],
    "occurrence_id": ["occurrence_id", "event_id", "step_id", "step", "step_index", "receipt_index", "ordinal", "idx"],
    "state_hash_before": ["state_hash_before", "before_state_hash", "state_before", "start_state_sig8", "state_before_sig8"],
    "state_hash_after": ["state_hash_after", "after_state_hash", "state_after", "final_state_sig8", "state_after_sig8"],
    "move_id": ["move_id", "selected_move", "move", "action_id", "action"],
    "halt_reason": ["halt_reason", "halt_code", "stop_code"],
    "status": ["status", "gate", "checkpoint_code", "law_status"],
    "family": ["family", "family_compact", "family_name"],
    "depth": ["depth", "depth_max", "depth_min"],
    "cycle": ["cycle", "cycle_n", "cycles_per_case"],
    "probe_id": ["probe_id"],
    "slot_id": ["slot_id"],
    "burden_class": ["burden_class"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha8_obj(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def safe_json_loads(value: Any) -> Any | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except Exception:
            return None
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if not (stripped.startswith("{") or stripped.startswith("[")):
        return None
    try:
        return json.loads(stripped)
    except Exception:
        return None


def flatten(obj: Any, prefix: str = "", out: dict[str, Any] | None = None) -> dict[str, Any]:
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            k = str(key)
            name = f"{prefix}.{k}" if prefix else k
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    elif isinstance(obj, list):
        for i, value in enumerate(obj[:50]):
            name = f"{prefix}.{i}" if prefix else str(i)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    return out


def last_path_token(path: str) -> str:
    return path.rsplit(".", 1)[-1]


def value_from_sources(name_options: list[str], row: dict[str, Any], flat: dict[str, Any]) -> Any | None:
    lower_row = {str(k).lower(): v for k, v in row.items()}
    lower_flat_exact = {str(k).lower(): v for k, v in flat.items()}

    for name in name_options:
        if name.lower() in lower_row and lower_row[name.lower()] not in (None, ""):
            return lower_row[name.lower()]

    for name in name_options:
        if name.lower() in lower_flat_exact and lower_flat_exact[name.lower()] not in (None, ""):
            return lower_flat_exact[name.lower()]

    for name in name_options:
        needle = name.lower()
        for key, value in lower_flat_exact.items():
            if last_path_token(key) == needle and value not in (None, ""):
                return value

    return None


def bucket_int(value: int | float | None) -> str | None:
    if value is None:
        return None
    try:
        x = float(value)
    except Exception:
        return None
    if x < 0:
        return "neg"
    if x == 0:
        return "0"
    if x <= 1:
        return "1"
    if x <= 2:
        return "2"
    if x <= 4:
        return "3-4"
    if x <= 8:
        return "5-8"
    if x <= 16:
        return "9-16"
    if x <= 32:
        return "17-32"
    if x <= 64:
        return "33-64"
    if x <= 128:
        return "65-128"
    if x <= 256:
        return "129-256"
    if x <= 512:
        return "257-512"
    if x <= 1024:
        return "513-1024"
    return "1025+"


def payload_shape_metrics(payload: Any) -> dict[str, Any]:
    flat = flatten(payload)
    keys = sorted(flat.keys())
    scalar_items = {
        k: v for k, v in flat.items()
        if not isinstance(v, (dict, list))
    }

    numeric_values: list[float] = []
    bool_true = 0
    bool_false = 0
    none_count = 0
    string_count = 0

    for value in scalar_items.values():
        if value is None:
            none_count += 1
        elif isinstance(value, bool):
            if value:
                bool_true += 1
            else:
                bool_false += 1
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            numeric_values.append(float(value))
        elif isinstance(value, str):
            string_count += 1

    key_tail_counts: dict[str, int] = defaultdict(int)
    for key in keys:
        key_tail_counts[last_path_token(key)] += 1

    field_presence_focus = [
        "run_id",
        "case_id",
        "fixture_id",
        "step",
        "step_index",
        "selected_move",
        "move_id",
        "state_hash_before",
        "state_hash_after",
        "halt_reason",
        "gate",
        "status",
        "burden_class",
        "probe_id",
        "slot_id",
        "receipt_count",
        "total_receipts",
        "depth",
        "radius",
        "cycle",
    ]

    presence = {
        name: any(last_path_token(k).lower() == name for k in keys)
        for name in field_presence_focus
    }

    return {
        "field_count_bucket": bucket_int(len(keys)),
        "scalar_count_bucket": bucket_int(len(scalar_items)),
        "numeric_count_bucket": bucket_int(len(numeric_values)),
        "string_count_bucket": bucket_int(string_count),
        "bool_true_bucket": bucket_int(bool_true),
        "bool_false_bucket": bucket_int(bool_false),
        "none_count_bucket": bucket_int(none_count),
        "numeric_sum_bucket": bucket_int(sum(numeric_values)) if numeric_values else None,
        "field_presence_focus": presence,
        "top_key_tails": sorted(key_tail_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:20],
    }


def extract_payload(row: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    parsed_payloads: dict[str, Any] = {}
    for key, value in row.items():
        parsed = safe_json_loads(value)
        if parsed is not None:
            parsed_payloads[key] = parsed

    if len(parsed_payloads) == 1:
        key, payload = next(iter(parsed_payloads.items()))
        return payload, {"payload_source_column": key, "payload_candidates": list(parsed_payloads.keys())}

    if parsed_payloads:
        return parsed_payloads, {
            "payload_source_column": "multiple_json_columns",
            "payload_candidates": list(parsed_payloads.keys()),
        }

    scalar_payload = {
        key: value for key, value in row.items()
        if key.lower() not in NOISE_FIELD_NAMES
    }
    return scalar_payload, {"payload_source_column": "scalar_receipt_row", "payload_candidates": []}


def canonical_occurrence_key(row: dict[str, Any], payload: Any) -> tuple[str, dict[str, Any]]:
    flat = flatten(payload)

    extracted: dict[str, Any] = {}
    for canonical, names in OCCURRENCE_KEY_CANDIDATES.items():
        extracted[canonical] = value_from_sources(names, row, flat)

    run_id = row.get("run_id") or extracted.get("source_run_id")
    rowid = row.get("rowid")

    fallback_ordinal = (
        extracted.get("occurrence_id")
        if extracted.get("occurrence_id") not in (None, "")
        else rowid
    )

    case_id = extracted.get("case_id")
    if case_id in (None, ""):
        family = extracted.get("family")
        depth = extracted.get("depth")
        probe = extracted.get("probe_id")
        slot = extracted.get("slot_id")
        case_id = "|".join(str(x) for x in [family, depth, probe, slot] if x not in (None, ""))
        if not case_id:
            case_id = f"run:{run_id}:row:{rowid}"

    occurrence = {
        "source_run_id": run_id,
        "case_id": case_id,
        "occurrence_id": fallback_ordinal,
        "state_hash_before": extracted.get("state_hash_before"),
        "state_hash_after": extracted.get("state_hash_after"),
        "move_id": extracted.get("move_id"),
        "halt_reason": extracted.get("halt_reason"),
        "status": extracted.get("status"),
        "family": extracted.get("family"),
        "depth": extracted.get("depth"),
        "cycle": extracted.get("cycle"),
        "probe_id": extracted.get("probe_id"),
        "slot_id": extracted.get("slot_id"),
        "burden_class": extracted.get("burden_class"),
        "fallback_rowid_used": extracted.get("occurrence_id") in (None, ""),
        "canonical_key_version": "full_occurrence_key_v0",
    }

    key = sha8_obj(occurrence)
    return key, occurrence


def compressed_delta_signature(row: dict[str, Any], payload: Any, occurrence: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    flat = flatten(payload)
    metrics = payload_shape_metrics(payload)

    before = occurrence.get("state_hash_before")
    after = occurrence.get("state_hash_after")

    payload_bytes = len(canonical_json_bytes(payload))
    row_scalar_bytes = len(canonical_json_bytes({
        k: v for k, v in row.items()
        if k.lower() not in {"rowid"}
    }))

    # Deliberately does not include full_occurrence_key, raw receipt hash, audit pointer, path, timestamp, or rowid.
    # It is allowed to include transition/shape/halt/probe deltas and coarse burden buckets.
    delta_payload = {
        "compression_version": COMPRESSION_VERSION,
        "transition": {
            "state_hash_before": before,
            "state_hash_after": after,
            "state_changed": None if before is None or after is None else before != after,
            "move_id": occurrence.get("move_id"),
            "halt_reason": occurrence.get("halt_reason"),
            "status": occurrence.get("status"),
        },
        "case_surface": {
            "family": occurrence.get("family"),
            "depth_bucket": bucket_int(occurrence.get("depth")),
            "cycle_bucket": bucket_int(occurrence.get("cycle")),
            "probe_id": occurrence.get("probe_id"),
            "slot_id": occurrence.get("slot_id"),
            "burden_class": occurrence.get("burden_class"),
        },
        "payload_shape_delta": metrics,
        "burden_delta": {
            "payload_bytes_bucket": bucket_int(payload_bytes),
            "row_scalar_bytes_bucket": bucket_int(row_scalar_bytes),
        },
    }

    sig = sha8_obj(delta_payload)
    return sig, delta_payload


def connect_registry() -> sqlite3.Connection:
    if not REGISTRY.exists():
        raise SystemExit(f"registry sqlite not found: {REGISTRY}")
    con = sqlite3.connect(REGISTRY)
    con.row_factory = sqlite3.Row
    return con


def table_columns(con: sqlite3.Connection, table: str) -> list[str]:
    rows = con.execute(f"pragma table_info({table})").fetchall()
    return [str(row["name"]) for row in rows]


def select_run_ids(con: sqlite3.Connection, run_id: str | None, max_runs: int) -> list[str]:
    run_cols = set(table_columns(con, "runs"))
    receipt_cols = set(table_columns(con, "receipts"))

    if "run_id" not in receipt_cols:
        raise SystemExit("receipts table has no run_id column; cannot build audit-linked observer probe")

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


def load_receipt_rows(con: sqlite3.Connection, run_ids: list[str], max_receipts: int | None) -> list[dict[str, Any]]:
    if not run_ids:
        return []

    placeholders = ",".join(["?"] * len(run_ids))
    limit_sql = "" if max_receipts is None else f" limit {int(max_receipts)}"
    query = f"select rowid as rowid, * from receipts where run_id in ({placeholders}) order by run_id, rowid{limit_sql}"
    rows = con.execute(query, run_ids).fetchall()
    return [dict(row) for row in rows]


def build_probe(run_id: str | None, max_runs: int, max_receipts: int | None) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()

    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    con = connect_registry()
    try:
        run_ids = select_run_ids(con, run_id, max_runs)
        receipt_rows = load_receipt_rows(con, run_ids, max_receipts)
        receipt_columns = table_columns(con, "receipts")
        runs_columns = table_columns(con, "runs")
    finally:
        con.close()

    compressed_rows: list[dict[str, Any]] = []
    occurrence_to_sig: dict[str, str] = {}
    sig_to_occurrences: dict[str, set[str]] = defaultdict(set)

    full_receipt_bytes = 0
    compressed_signature_bytes = 0
    audit_recoverability_failures: list[str] = []
    raw_hash_truth_surface_used = False

    for index, row in enumerate(receipt_rows):
        payload, payload_meta = extract_payload(row)

        full_receipt_bytes += len(canonical_json_bytes({
            "registry_row": row,
            "parsed_payload": payload,
        }))

        full_key, occurrence_obj = canonical_occurrence_key(row, payload)
        delta_sig, delta_payload = compressed_delta_signature(row, payload, occurrence_obj)

        audit_pointer = {
            "kind": "registry.sqlite.receipts",
            "registry_path": "data/runs/registry.sqlite",
            "source_run_id": row.get("run_id"),
            "receipt_rowid": row.get("rowid"),
            "payload_source_column": payload_meta["payload_source_column"],
        }

        if not audit_pointer["source_run_id"] or audit_pointer["receipt_rowid"] is None:
            audit_recoverability_failures.append(f"missing_audit_pointer:{index}")

        occurrence_id = occurrence_obj.get("occurrence_id")
        case_id = occurrence_obj.get("case_id")

        signature_row = {
            "signature_id": sha8_obj({
                "source_run_id": row.get("run_id"),
                "receipt_rowid": row.get("rowid"),
                "delta_signature": delta_sig,
                "compression_version": COMPRESSION_VERSION,
            }),
            "source_run_id": row.get("run_id"),
            "case_id": case_id,
            "occurrence_id": occurrence_id,
            "full_occurrence_key": full_key,
            "state_hash_before": occurrence_obj.get("state_hash_before"),
            "state_hash_after": occurrence_obj.get("state_hash_after"),
            "move_id": occurrence_obj.get("move_id"),
            "delta_signature": delta_sig,
            "delta_payload": delta_payload,
            "compression_version": COMPRESSION_VERSION,
            "audit_pointer_or_full_receipt_ref": audit_pointer,
            "observer_notes": {
                "full_occurrence_key_is_not_raw_receipt_hash": True,
                "delta_signature_excludes_full_occurrence_key": True,
                "delta_signature_excludes_audit_pointer": True,
                "delta_signature_excludes_rowid": True,
                "payload_source_column": payload_meta["payload_source_column"],
                "payload_candidates": payload_meta["payload_candidates"],
            },
        }

        compressed_signature_bytes += len(canonical_json_bytes(signature_row))
        compressed_rows.append(signature_row)
        occurrence_to_sig[full_key] = delta_sig
        sig_to_occurrences[delta_sig].add(full_key)

    distinct_full_occurrence_keys = len(set(occurrence_to_sig.keys()))
    distinct_compressed_signatures = len(sig_to_occurrences)

    collision_groups = {
        sig: sorted(keys)
        for sig, keys in sig_to_occurrences.items()
        if len(keys) > 1
    }
    collision_count = len(collision_groups)
    collision_rate = (
        collision_count / distinct_compressed_signatures
        if distinct_compressed_signatures else 0.0
    )

    # No accepted merge relation exists in v0, so all collisions are false merges.
    false_merge_count = collision_count
    false_split_count: int | str = "N/A"

    distinguishability_retention_ratio = (
        distinct_compressed_signatures / distinct_full_occurrence_keys
        if distinct_full_occurrence_keys else 0.0
    )

    burden_ratio_bytes = (
        compressed_signature_bytes / full_receipt_bytes
        if full_receipt_bytes else 0.0
    )

    burden_ratio_count = (
        len(compressed_rows) / len(receipt_rows)
        if receipt_rows else 0.0
    )

    scale_value = (
        distinguishability_retention_ratio / burden_ratio_bytes
        if burden_ratio_bytes > 0 else 0.0
    )

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    pass_gates = {
        "no_silent_collapse": false_merge_count == 0,
        "burden_reduction_real": compressed_signature_bytes < full_receipt_bytes,
        "stability_across_scale": False,
        "audit_recoverability": len(audit_recoverability_failures) == 0 and len(compressed_rows) == len(receipt_rows),
        "observer_only_containment": True,
        "raw_receipt_hash_not_used_as_truth_surface": raw_hash_truth_surface_used is False,
    }

    if not pass_gates["audit_recoverability"] or not pass_gates["observer_only_containment"] or raw_hash_truth_surface_used:
        terminal_decision = "FAIL"
    elif false_merge_count > 0:
        terminal_decision = "FAIL"
    elif not pass_gates["burden_reduction_real"]:
        terminal_decision = "FAIL"
    elif not pass_gates["stability_across_scale"]:
        terminal_decision = "NEEDS_MORE_SCALE"
    else:
        terminal_decision = "PASS_OBSERVER_ONLY"

    probe = {
        "schema_version": "stable_delta_signature_probe_receipt_v0",
        "probe_name": PROBE_NAME,
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "status_law": {
            "object": "stable_delta_signature_probe.v0",
            "layer": "OUTER",
            "mode": "OBSERVE/VERIFY",
            "status": "CODE_AHEAD_EXPERIMENTAL",
            "authority": "NON_BINDING_UNLESS_LATER_FROZEN_BY_GATE",
        },
        "source": {
            "registry_path": "data/runs/registry.sqlite",
            "selected_run_ids": run_ids,
            "receipt_columns": receipt_columns,
            "runs_columns": runs_columns,
            "max_runs": max_runs,
            "max_receipts": max_receipts,
        },
        "truth_surface": {
            "primary_comparison": "full_occurrence_key_to_compressed_delta_signature",
            "raw_full_receipt_hash_used_as_truth_surface": False,
            "full_receipt_hash_compared_to_delta_signature": False,
            "canonical_occurrence_key_version": "full_occurrence_key_v0",
        },
        "authority_guards": {
            "observer_only": True,
            "runtime_receipt_emission_changed": False,
            "full_receipts_suppressed": False,
            "scale_mode_authorized": False,
            "compressed_signature_promoted_to_theorem_content": False,
            "receipt_replacement_authorized": False,
            "receipt_deletion_authorized": False,
            "receipt_compression_authorized": False,
        },
        "burden_measurements": {
            "full_receipt_count": len(receipt_rows),
            "compressed_signature_count": len(compressed_rows),
            "full_receipt_bytes": full_receipt_bytes,
            "compressed_signature_bytes": compressed_signature_bytes,
            "elapsed_ms_probe_observer": elapsed_ms,
            "actual_observer_overhead_ms": elapsed_ms,
            "projected_compressed_burden_bytes": compressed_signature_bytes,
            "projected_full_burden_bytes": full_receipt_bytes,
            "burden_ratio_bytes": burden_ratio_bytes,
            "burden_ratio_count": burden_ratio_count,
            "bytes_per_occurrence_full": (
                full_receipt_bytes / len(receipt_rows)
                if receipt_rows else 0.0
            ),
            "bytes_per_occurrence_compressed": (
                compressed_signature_bytes / len(compressed_rows)
                if compressed_rows else 0.0
            ),
        },
        "distinguishability_measurements": {
            "occurrences_total": len(receipt_rows),
            "distinct_full_occurrence_keys": distinct_full_occurrence_keys,
            "distinct_compressed_signatures": distinct_compressed_signatures,
            "collision_count": collision_count,
            "collision_rate": collision_rate,
            "false_merge_count": false_merge_count,
            "false_split_count": false_split_count,
            "distinguishability_retention_ratio": distinguishability_retention_ratio,
            "scale_value": scale_value,
        },
        "collision_gallery": [
            {
                "delta_signature": sig,
                "full_occurrence_keys": keys[:10],
                "full_occurrence_key_count": len(keys),
            }
            for sig, keys in list(collision_groups.items())[:20]
        ],
        "pass_gates": pass_gates,
        "audit_recoverability_failures": audit_recoverability_failures,
        "terminal_decision": terminal_decision,
        "terminal": {
            "type": "ADVANCE" if terminal_decision in {"PASS_OBSERVER_ONLY", "NEEDS_MORE_SCALE"} else "STOP",
            "next_command_goal": (
                "DESIGN_STABLE_DELTA_SIGNATURE_SCALE_BANDS_V0"
                if terminal_decision == "NEEDS_MORE_SCALE"
                else None
            ),
            "stop_code": None if terminal_decision in {"PASS_OBSERVER_ONLY", "NEEDS_MORE_SCALE"} else "STOP_STABLE_DELTA_SIGNATURE_PROBE_FAILED",
        },
        "honesty_box": {
            "does_not_prove_delta_signatures_work": True,
            "does_not_authorize_receipt_discarding": True,
            "does_not_authorize_scale_mode": True,
            "does_not_define_final_metric_set": True,
            "does_not_claim_all_occurrence_identity_is_transition_delta": True,
            "does_not_change_authority_boundary": True,
        },
        "gate": "STABLE_DELTA_SIGNATURE_PROBE_EXECUTION_PASS",
        "failures": [],
        "warnings": [],
        "created_at": now_iso(),
    }

    if len(receipt_rows) == 0:
        probe["failures"].append("no_receipts_loaded")
    if raw_hash_truth_surface_used:
        probe["failures"].append("raw_receipt_hash_truth_surface_used")
    if not pass_gates["observer_only_containment"]:
        probe["failures"].append("observer_only_containment_failed")
    if probe["failures"]:
        probe["gate"] = "FAIL"
        probe["terminal_decision"] = "FAIL"
        probe["terminal"] = {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_STABLE_DELTA_SIGNATURE_PROBE_EXECUTION_INVALID",
        }

    probe_id = sha8_obj({
        "probe_name": probe["probe_name"],
        "compression_version": COMPRESSION_VERSION,
        "source": probe["source"],
        "burden": probe["burden_measurements"],
        "distinguishability": probe["distinguishability_measurements"],
        "terminal_decision": probe["terminal_decision"],
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in compressed_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")

    probe["rows_path"] = f"data/stable_delta_signature_probe_rows/{probe_id}.jsonl"

    receipt_id = sha8_obj(probe)
    receipt = {
        "schema_version": "stable_delta_signature_probe_minimal_receipt_v0",
        "probe_id": probe_id,
        "probe_sig8": probe_id,
        "receipt_id": receipt_id,
        "receipt_sig8": receipt_id,
        "rows_path": probe["rows_path"],
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "full_receipt_count": probe["burden_measurements"]["full_receipt_count"],
        "compressed_signature_count": probe["burden_measurements"]["compressed_signature_count"],
        "full_receipt_bytes": probe["burden_measurements"]["full_receipt_bytes"],
        "compressed_signature_bytes": probe["burden_measurements"]["compressed_signature_bytes"],
        "actual_observer_overhead_ms": probe["burden_measurements"]["actual_observer_overhead_ms"],
        "projected_compressed_burden_bytes": probe["burden_measurements"]["projected_compressed_burden_bytes"],
        "distinct_full_occurrence_keys": distinct_full_occurrence_keys,
        "distinct_compressed_signatures": distinct_compressed_signatures,
        "collision_count": collision_count,
        "collision_rate": collision_rate,
        "false_merge_count": false_merge_count,
        "false_split_count": false_split_count,
        "distinguishability_retention_ratio": distinguishability_retention_ratio,
        "burden_ratio_bytes": burden_ratio_bytes,
        "burden_ratio_count": burden_ratio_count,
        "scale_value": scale_value,
        "pass_gates": pass_gates,
        "truth_surface": probe["truth_surface"],
        "authority_guards": probe["authority_guards"],
        "terminal_decision": probe["terminal_decision"],
        "terminal": probe["terminal"],
        "gate": probe["gate"],
        "failures": probe["failures"],
        "warnings": probe["warnings"],
        "created_at": now_iso(),
    }

    receipt_path = RECEIPT_DIR / f"{probe_id}.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return probe, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="latest")
    parser.add_argument("--max-runs", type=int, default=1)
    parser.add_argument("--max-receipts", type=int, default=None)
    args = parser.parse_args()

    probe, receipt = build_probe(args.run_id, args.max_runs, args.max_receipts)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"probe_id={probe['probe_id']}")
    print(f"probe_rows_path={probe['rows_path']}")
    print(f"probe_receipt_path=data/stable_delta_signature_probe_receipts/{probe['probe_id']}.json")

    # Return success when observer execution is valid, even if the experimental terminal_decision is FAIL.
    # FAIL here means the signature candidate failed, not that the command failed.
    return 0 if probe["gate"] == "STABLE_DELTA_SIGNATURE_PROBE_EXECUTION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
