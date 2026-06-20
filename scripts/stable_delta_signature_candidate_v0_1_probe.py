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

POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_policy_receipts"
DIAG_DIR = ROOT / "data" / "stable_delta_signature_diagnostics"
DIAG_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_diagnostic_receipts"
SOURCE_PROBE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_probe_receipts"

ROWS_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_rows"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_receipts"

EXPECTED_POLICY_ID = "c3dcd5d1"
EXPECTED_POLICY_RECEIPT_ID = "3a908ae7"
EXPECTED_DIAGNOSTIC_ID = "21878f3c"
EXPECTED_DIAGNOSTIC_RECEIPT_ID = "7467309f"
EXPECTED_SOURCE_PROBE_ID = "a729e00e"
EXPECTED_SOURCE_PROBE_RECEIPT_ID = "0ce90f3f"

COMPRESSION_VERSION = "stable_delta_signature_v0.1_candidate"
MODE = "OUTER_OBSERVER_ONLY"

ALLOWED_TERMINALS = [
    "PASS_OBSERVER_ONLY_LOCAL",
    "FAIL_FALSE_MERGE",
    "FAIL_NO_BURDEN_REDUCTION",
    "FAIL_SOURCE_SURFACE_INSUFFICIENT",
    "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS",
]

NOISE_NAMES = {
    "created_at",
    "created_utc",
    "updated_at",
    "timestamp",
    "path",
    "file_path",
    "receipt_file",
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

FIELD_CANDIDATES = {
    "case_id": ["case_id", "fixture_id", "case_key", "case", "fixture", "slot_id"],
    "canonical_occurrence_id": ["occurrence_id", "event_id", "step_id", "step", "step_index", "ordinal", "idx"],
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
    "shape_count": ["shape_count", "shapes_count", "shape_total", "n_shapes"],
    "raw_event_count": ["raw_event_count", "raw_events", "event_count", "total_events"],
    "receipt_count": ["receipt_count", "total_receipts", "receipts"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def canonical_bytes(obj: Any) -> int:
    return len(canonical_blob(obj))


def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def safe_json(value: Any) -> Any | None:
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
    text = value.strip()
    if not text:
        return None
    if not (text.startswith("{") or text.startswith("[")):
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def flatten(obj: Any, prefix: str = "", out: dict[str, Any] | None = None) -> dict[str, Any]:
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    elif isinstance(obj, list):
        for i, value in enumerate(obj[:100]):
            name = f"{prefix}.{i}" if prefix else str(i)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    return out


def last_token(path: str) -> str:
    return path.rsplit(".", 1)[-1]


def find_value(options: list[str], registry_row: dict[str, Any], flat: dict[str, Any]) -> Any | None:
    lower_row = {str(k).lower(): v for k, v in registry_row.items()}
    lower_flat = {str(k).lower(): v for k, v in flat.items()}

    for option in options:
        key = option.lower()
        if key in lower_row and lower_row[key] not in (None, ""):
            return lower_row[key]

    for option in options:
        key = option.lower()
        if key in lower_flat and lower_flat[key] not in (None, ""):
            return lower_flat[key]

    for option in options:
        needle = option.lower()
        for key, value in lower_flat.items():
            if last_token(key) == needle and value not in (None, ""):
                return value

    return None


def bool_bucket(value: Any) -> str | None:
    if value is None:
        return None
    return "T" if bool(value) else "F"


def int_bucket(value: Any) -> str | None:
    if value in (None, ""):
        return None
    try:
        x = int(float(value))
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


def extract_payload(registry_row: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    parsed: dict[str, Any] = {}
    for key, value in registry_row.items():
        j = safe_json(value)
        if j is not None:
            parsed[key] = j

    if len(parsed) == 1:
        key, payload = next(iter(parsed.items()))
        return payload, {"payload_source_column": key, "payload_candidate_columns": list(parsed.keys())}

    if parsed:
        return parsed, {"payload_source_column": "multiple_json_columns", "payload_candidate_columns": list(parsed.keys())}

    scalar_payload = {
        k: v for k, v in registry_row.items()
        if str(k).lower() not in NOISE_NAMES and str(k).lower() != "rowid"
    }
    return scalar_payload, {"payload_source_column": "scalar_receipt_row", "payload_candidate_columns": []}


def extract_fields(registry_row: dict[str, Any], payload: Any) -> dict[str, Any]:
    flat = flatten(payload)
    extracted = {}
    for canonical, candidates in FIELD_CANDIDATES.items():
        extracted[canonical] = find_value(candidates, registry_row, flat)
    return extracted


def occurrence_key_from_full_layer(registry_row: dict[str, Any], extracted: dict[str, Any], payload_meta: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    # Baseline occurrence key is audit-layer identity, not compressed signature identity.
    # It may use registry rowid as the audit occurrence locator when richer occurrence id is absent.
    # The candidate signature payload must not use rowid as its discriminator.
    occurrence_id = extracted.get("canonical_occurrence_id")
    rowid_used = False
    if occurrence_id in (None, ""):
        occurrence_id = registry_row.get("rowid")
        rowid_used = True

    case_id = extracted.get("case_id")
    if case_id in (None, ""):
        case_parts = [
            extracted.get("family"),
            extracted.get("depth"),
            extracted.get("probe_id"),
            extracted.get("slot_id"),
            extracted.get("burden_class"),
        ]
        case_id = "|".join(str(x) for x in case_parts if x not in (None, ""))
        if not case_id:
            case_id = f"run:{registry_row.get('run_id')}"

    occurrence = {
        "canonical_occurrence_key_version": "full_occurrence_key_v0_1",
        "source_run_id": registry_row.get("run_id"),
        "case_id": case_id,
        "occurrence_id": occurrence_id,
        "audit_locator_rowid_used": rowid_used,
        "payload_source_column": payload_meta.get("payload_source_column"),
        "transition_basis": {
            "state_hash_before": extracted.get("state_hash_before"),
            "state_hash_after": extracted.get("state_hash_after"),
            "move_id": extracted.get("move_id"),
            "halt_reason": extracted.get("halt_reason"),
            "status": extracted.get("status"),
        },
    }
    return sha8(occurrence), occurrence


def field_stats(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    values = [row.get("extracted", {}).get(field) for row in rows]
    present_values = [v for v in values if v not in (None, "")]
    return {
        "field": field,
        "present": len(present_values),
        "missing": len(rows) - len(present_values),
        "missing_rate": round((len(rows) - len(present_values)) / len(rows), 6) if rows else 0.0,
        "distinct_present_values": len({repr(v) for v in present_values}),
    }


def source_surface(rows: list[dict[str, Any]]) -> dict[str, Any]:
    stats = {
        field: field_stats(rows, field)
        for field in [
            "state_hash_before",
            "state_hash_after",
            "move_id",
            "halt_reason",
            "status",
            "case_id",
            "canonical_occurrence_id",
            "probe_id",
            "slot_id",
            "burden_class",
            "shape_count",
            "raw_event_count",
            "receipt_count",
        ]
    }

    total = len(rows)
    all_state_before = stats["state_hash_before"]["present"] == total and total > 0
    all_state_after = stats["state_hash_after"]["present"] == total and total > 0
    move_discriminative = stats["move_id"]["distinct_present_values"] > 1
    halt_discriminative = stats["halt_reason"]["distinct_present_values"] > 1 or stats["status"]["distinct_present_values"] > 1
    occurrence_discriminator_present = stats["canonical_occurrence_id"]["present"] == total and stats["canonical_occurrence_id"]["distinct_present_values"] > 1
    case_discriminator_present = stats["case_id"]["present"] == total and stats["case_id"]["distinct_present_values"] > 1
    shape_or_event_discriminative = any(
        stats[field]["distinct_present_values"] > 1
        for field in ["shape_count", "raw_event_count", "receipt_count"]
    )

    transition_sufficient = all_state_before and all_state_after and (move_discriminative or halt_discriminative)
    canonical_discriminator_sufficient = occurrence_discriminator_present or case_discriminator_present
    weak_metric_discriminator_available = shape_or_event_discriminative

    sufficient_for_local_pass = transition_sufficient or canonical_discriminator_sufficient or weak_metric_discriminator_available

    return {
        "stats": stats,
        "transition_sufficient": transition_sufficient,
        "canonical_discriminator_sufficient": canonical_discriminator_sufficient,
        "weak_metric_discriminator_available": weak_metric_discriminator_available,
        "sufficient_for_local_pass": sufficient_for_local_pass,
        "honesty_status": "SUFFICIENT_FOR_LOCAL_COLLISION_TEST" if sufficient_for_local_pass else "SOURCE_SURFACE_INSUFFICIENT",
        "reason": (
            "Canonical transition/discriminator surface has enough non-packaging variation for local collision testing."
            if sufficient_for_local_pass
            else "Canonical transition fields are missing or non-discriminative; candidate must not report a local pass."
        ),
    }


def candidate_signature_payload(extracted: dict[str, Any], surface: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "cv": "v0.1",
    }

    # Include only canonical, non-packaging, compact signal fields.
    # Do not include full_occurrence_key, audit pointer, rowid, paths, timestamps, raw receipt hashes, or debug payload.
    if extracted.get("state_hash_before") not in (None, ""):
        payload["s0"] = extracted.get("state_hash_before")
    if extracted.get("move_id") not in (None, "") and surface["stats"]["move_id"]["distinct_present_values"] > 1:
        payload["m"] = extracted.get("move_id")
    elif extracted.get("move_id") not in (None, ""):
        # allowed as transition context only, not expected to separate by itself
        payload["m_const"] = extracted.get("move_id")
    if extracted.get("state_hash_after") not in (None, ""):
        payload["s1"] = extracted.get("state_hash_after")
    if extracted.get("halt_reason") not in (None, ""):
        payload["h"] = extracted.get("halt_reason")
    elif extracted.get("status") not in (None, ""):
        payload["st"] = extracted.get("status")

    if extracted.get("case_id") not in (None, "") and surface["stats"]["case_id"]["distinct_present_values"] > 1:
        payload["case"] = extracted.get("case_id")
    if extracted.get("canonical_occurrence_id") not in (None, "") and surface["stats"]["canonical_occurrence_id"]["distinct_present_values"] > 1:
        payload["occ"] = extracted.get("canonical_occurrence_id")

    # Compact metric buckets only. These are candidates, not authority.
    metric_buckets = {}
    for short, field in [
        ("shape", "shape_count"),
        ("raw", "raw_event_count"),
        ("receipt", "receipt_count"),
        ("depth", "depth"),
        ("cycle", "cycle"),
    ]:
        value = int_bucket(extracted.get(field))
        if value is not None and surface["stats"].get(field, {"distinct_present_values": 0})["distinct_present_values"] > 1:
            metric_buckets[short] = value
    if metric_buckets:
        payload["b"] = metric_buckets

    return payload


def projected_scale_row(signature_id: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "source_run_id": row.get("source_run_id"),
        "case_id": row.get("case_id"),
        "candidate_delta_signature": row.get("candidate_delta_signature"),
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer_or_full_receipt_ref": row.get("audit_pointer_or_full_receipt_ref"),
    }


def minimal_required_row(signature_id: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": signature_id,
        "source_run_id": row.get("source_run_id"),
        "case_id": row.get("case_id"),
        "occurrence_id": row.get("occurrence_id"),
        "full_occurrence_key": row.get("full_occurrence_key"),
        "candidate_delta_signature": row.get("candidate_delta_signature"),
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer_or_full_receipt_ref": row.get("audit_pointer_or_full_receipt_ref"),
    }


def connect_registry() -> sqlite3.Connection:
    if not REGISTRY.exists():
        raise SystemExit(f"registry sqlite missing: {REGISTRY}")
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


def verify_policy(policy: dict[str, Any], receipt: dict[str, Any], diag: dict[str, Any], diag_receipt: dict[str, Any], source_probe: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_mismatch:{receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("candidate_design_id") != "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1":
        failures.append(f"candidate_design_id_wrong:{policy.get('candidate_design_id')}")
    if policy.get("source_diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"policy_source_diagnostic_wrong:{policy.get('source_diagnostic_id')}")
    if diag.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"diagnostic_id_wrong:{diag.get('diagnostic_id')}")
    if diag_receipt.get("receipt_id") != EXPECTED_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"diagnostic_receipt_wrong:{diag_receipt.get('receipt_id')}")
    if diag.get("gate") != "PASS":
        failures.append(f"diagnostic_gate_not_PASS:{diag.get('gate')}")
    if source_probe.get("probe_id") != EXPECTED_SOURCE_PROBE_ID:
        failures.append(f"source_probe_id_wrong:{source_probe.get('probe_id')}")
    if source_probe.get("receipt_id") != EXPECTED_SOURCE_PROBE_RECEIPT_ID:
        failures.append(f"source_probe_receipt_wrong:{source_probe.get('receipt_id')}")
    if source_probe.get("terminal_decision") != "FAIL":
        failures.append(f"source_probe_terminal_not_FAIL:{source_probe.get('terminal_decision')}")

    auth = policy.get("authority") or {}
    if auth.get("authorizes_next_candidate_probe_implementation") is not True:
        failures.append("policy_does_not_authorize_candidate_probe")
    if auth.get("authorized_next_command_goal") != "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_PROBE":
        failures.append(f"policy_next_goal_wrong:{auth.get('authorized_next_command_goal')}")
    for key in [
        "authorizes_runtime_receipt_emission_change",
        "authorizes_full_receipt_suppression",
        "authorizes_scale_mode",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_theorem_content",
        "authorizes_scale_band_run_now",
        "authorizes_acceptance_now",
        "authorizes_current_v0_signature_scaling",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authorization:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/stable_delta_signature_candidate_v0_1_probe.py"]:
        failures.append(f"policy_touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    if constraints.get("must_read_existing_receipts_only") is not True:
        failures.append("policy_read_existing_receipts_only_missing")
    if constraints.get("must_not_change_registry_sqlite") is not True:
        failures.append("policy_no_registry_change_missing")

    design = policy.get("required_v0_1_design") or {}
    if design.get("signature_payload_must_be_tiny") is not True:
        failures.append("policy_tiny_payload_missing")
    if design.get("signature_payload_measured_separately_from_debug_sidecar") is not True:
        failures.append("policy_separate_payload_bytes_missing")
    if design.get("raw_receipt_hash_truth_surface_forbidden") is not True:
        failures.append("policy_raw_hash_forbidden_missing")
    if design.get("scale_bands_forbidden_until_no_silent_collapse") is not True:
        failures.append("policy_scale_band_guard_missing")
    if "FAIL_SOURCE_SURFACE_INSUFFICIENT" not in (design.get("allowed_terminal_decisions") or []):
        failures.append("policy_source_insufficient_terminal_missing")

    return failures


def build_candidate_probe(policy_id: str, run_id: str | None, max_runs: int, max_receipts: int | None) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()

    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    diag = load_json(DIAG_DIR / f"{EXPECTED_DIAGNOSTIC_ID}.json")
    diag_receipt = load_json(DIAG_RECEIPT_DIR / f"{EXPECTED_DIAGNOSTIC_ID}.json")
    source_probe = load_json(SOURCE_PROBE_RECEIPT_DIR / f"{EXPECTED_SOURCE_PROBE_ID}.json")

    failures = verify_policy(policy, policy_receipt, diag, diag_receipt, source_probe)

    con = connect_registry()
    try:
        run_ids = select_run_ids(con, run_id, max_runs)
        receipt_rows = load_receipts(con, run_ids, max_receipts)
        receipt_columns = table_columns(con, "receipts")
        runs_columns = table_columns(con, "runs")
    finally:
        con.close()

    prepared: list[dict[str, Any]] = []
    full_receipt_bytes = 0

    for registry_row in receipt_rows:
        payload, payload_meta = extract_payload(registry_row)
        extracted = extract_fields(registry_row, payload)
        full_key, occurrence = occurrence_key_from_full_layer(registry_row, extracted, payload_meta)

        full_receipt_bytes += canonical_bytes({
            "registry_row": registry_row,
            "parsed_payload": payload,
        })

        prepared.append({
            "registry_row": registry_row,
            "payload": payload,
            "payload_meta": payload_meta,
            "extracted": extracted,
            "full_occurrence_key": full_key,
            "occurrence": occurrence,
        })

    surface = source_surface(prepared)

    output_rows: list[dict[str, Any]] = []
    sig_to_full_keys: dict[str, set[str]] = defaultdict(set)

    signature_payload_bytes = 0
    audit_sidecar_bytes = 0
    debug_sidecar_bytes = 0
    projected_scale_row_bytes = 0
    minimal_required_row_bytes = 0

    rowid_identity_leak = False
    raw_hash_truth_surface_used = False
    debug_payload_counted_as_signature = False
    audit_failures: list[str] = []

    for item in prepared:
        registry_row = item["registry_row"]
        extracted = item["extracted"]
        occurrence = item["occurrence"]
        full_key = item["full_occurrence_key"]
        payload_meta = item["payload_meta"]

        sig_payload = candidate_signature_payload(extracted, surface)
        candidate_delta_signature = sha8(sig_payload)

        audit_pointer = {
            "kind": "registry.sqlite.receipts",
            "registry_path": "data/runs/registry.sqlite",
            "source_run_id": registry_row.get("run_id"),
            "receipt_rowid": registry_row.get("rowid"),
            "payload_source_column": payload_meta.get("payload_source_column"),
        }
        if not audit_pointer["source_run_id"] or audit_pointer["receipt_rowid"] is None:
            audit_failures.append(f"missing_audit_pointer:{len(output_rows)}")

        signature_id = sha8({
            "source_run_id": registry_row.get("run_id"),
            "candidate_delta_signature": candidate_delta_signature,
            "compression_version": COMPRESSION_VERSION,
            "audit_pointer": audit_pointer,
        })

        debug_sidecar = {
            "extracted_field_presence": {
                field: extracted.get(field) not in (None, "")
                for field in sorted(extracted.keys())
            },
            "source_surface_honesty_status": surface["honesty_status"],
            "payload_source_column": payload_meta.get("payload_source_column"),
            "candidate_payload_field_count": len(sig_payload),
            "candidate_payload_keys": sorted(sig_payload.keys()),
            "rowid_excluded_from_signature_payload": "rowid" not in json.dumps(sig_payload, sort_keys=True).lower(),
            "raw_receipt_hash_excluded_from_signature_payload": "receipt_hash" not in json.dumps(sig_payload, sort_keys=True).lower(),
        }

        row = {
            "signature_id": signature_id,
            "source_run_id": registry_row.get("run_id"),
            "case_id": occurrence.get("case_id"),
            "occurrence_id": occurrence.get("occurrence_id"),
            "full_occurrence_key": full_key,
            "candidate_delta_signature": candidate_delta_signature,
            "signature_payload": sig_payload,
            "signature_payload_bytes": canonical_bytes(sig_payload),
            "audit_pointer_or_full_receipt_ref": audit_pointer,
            "audit_sidecar_bytes": canonical_bytes(audit_pointer),
            "debug_sidecar": debug_sidecar,
            "debug_sidecar_bytes": canonical_bytes(debug_sidecar),
            "compression_version": COMPRESSION_VERSION,
            "truth_surface": {
                "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
                "raw_full_receipt_hash_used_as_truth_surface": False,
                "full_receipt_hash_compared_to_delta_signature": False,
            },
            "authority_guards": {
                "observer_only": True,
                "runtime_receipt_emission_changed": False,
                "full_receipts_suppressed": False,
                "scale_mode_authorized": False,
                "receipt_replacement_authorized": False,
                "receipt_deletion_authorized": False,
                "receipt_compression_authorized": False,
            },
        }

        # Explicit rowid leak guard: rowid may appear only in audit pointer, never in signature payload.
        sig_payload_blob = json.dumps(sig_payload, sort_keys=True, default=str).lower()
        if "rowid" in sig_payload_blob or "receipt_rowid" in sig_payload_blob:
            rowid_identity_leak = True
        if "receipt_hash" in sig_payload_blob or "full_receipt_hash" in sig_payload_blob or "raw_full_receipt_hash" in sig_payload_blob:
            raw_hash_truth_surface_used = True

        proj = projected_scale_row(signature_id, row)
        minimal = minimal_required_row(signature_id, row)

        signature_payload_bytes += canonical_bytes(sig_payload)
        audit_sidecar_bytes += canonical_bytes(audit_pointer)
        debug_sidecar_bytes += canonical_bytes(debug_sidecar)
        projected_scale_row_bytes += canonical_bytes(proj)
        minimal_required_row_bytes += canonical_bytes(minimal)

        output_rows.append(row)
        sig_to_full_keys[candidate_delta_signature].add(full_key)

    distinct_full_occurrence_keys = len({row["full_occurrence_key"] for row in output_rows})
    distinct_candidate_signatures = len(sig_to_full_keys)
    collision_groups = {
        sig: sorted(keys)
        for sig, keys in sig_to_full_keys.items()
        if len(keys) > 1
    }
    collision_count = len(collision_groups)
    false_merge_count = collision_count

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

    source_insufficient = not surface["sufficient_for_local_pass"]

    terminal_decision: str
    if source_insufficient:
        terminal_decision = "FAIL_SOURCE_SURFACE_INSUFFICIENT"
    elif false_merge_count > 0:
        terminal_decision = "FAIL_FALSE_MERGE"
    elif projected_scale_row_bytes >= full_receipt_bytes:
        terminal_decision = "FAIL_NO_BURDEN_REDUCTION"
    else:
        terminal_decision = "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS"

    pass_gates = {
        "raw_hash_truth_surface_forbidden": raw_hash_truth_surface_used is False,
        "observer_only_containment": True,
        "audit_recoverability": len(audit_failures) == 0 and len(output_rows) == len(receipt_rows),
        "no_rowid_identity_leak": rowid_identity_leak is False,
        "debug_payload_not_counted_as_signature": debug_payload_counted_as_signature is False,
        "signature_payload_measured_separately": True,
        "source_surface_honesty": (not source_insufficient) or terminal_decision == "FAIL_SOURCE_SURFACE_INSUFFICIENT",
        "no_silent_collapse_local": false_merge_count == 0,
        "real_projected_burden_reduction": projected_scale_row_bytes < full_receipt_bytes if full_receipt_bytes else False,
        "scale_bands_forbidden_until_no_silent_collapse": terminal_decision != "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS" or false_merge_count == 0,
    }

    if raw_hash_truth_surface_used:
        failures.append("raw_hash_truth_surface_used")
    if rowid_identity_leak:
        failures.append("rowid_identity_leak_in_signature_payload")
    if debug_payload_counted_as_signature:
        failures.append("debug_payload_counted_as_signature_payload")
    if audit_failures:
        failures.append(f"audit_recoverability_failures:{audit_failures[:5]}")
    if terminal_decision == "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS" and false_merge_count > 0:
        failures.append("scale_band_advance_with_false_merges")

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    probe = {
        "schema_version": "stable_delta_signature_candidate_v0_1_probe_receipt_v0",
        "probe_kind": "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_PROBE",
        "candidate_design_id": "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1",
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_probe_id": EXPECTED_SOURCE_PROBE_ID,
        "selected_run_ids": run_ids,
        "registry_surface": {
            "registry_path": "data/runs/registry.sqlite",
            "receipt_columns": receipt_columns,
            "runs_columns": runs_columns,
            "max_runs": max_runs,
            "max_receipts": max_receipts,
            "registry_sqlite_changed": False,
        },
        "authority_guards": {
            "observer_only": True,
            "runtime_receipt_emission_changed": False,
            "full_receipts_suppressed": False,
            "scale_mode_authorized": False,
            "receipt_replacement_authorized": False,
            "receipt_deletion_authorized": False,
            "receipt_compression_authorized": False,
            "raw_receipt_hash_truth_surface_authorized": False,
            "theorem_content_authorized": False,
            "scale_band_run_authorized": False,
        },
        "truth_surface": {
            "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
            "raw_full_receipt_hash_used_as_truth_surface": False,
            "full_receipt_hash_compared_to_delta_signature": False,
            "canonical_occurrence_key_version": "full_occurrence_key_v0_1",
        },
        "source_surface": surface,
        "burden_measurements": {
            "full_receipt_count": len(receipt_rows),
            "candidate_signature_count": len(output_rows),
            "full_receipt_bytes": full_receipt_bytes,
            "signature_payload_bytes": signature_payload_bytes,
            "audit_sidecar_bytes": audit_sidecar_bytes,
            "debug_sidecar_bytes": debug_sidecar_bytes,
            "minimal_required_row_bytes": minimal_required_row_bytes,
            "projected_scale_row_bytes": projected_scale_row_bytes,
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
            "false_split_count": "N/A",
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
        "pass_gates": pass_gates,
        "audit_recoverability_failures": audit_failures,
        "negative_claims": {
            "does_not_authorize_scale_mode": True,
            "does_not_authorize_receipt_replacement": True,
            "does_not_authorize_receipt_deletion": True,
            "does_not_authorize_receipt_compression": True,
            "does_not_modify_runtime_receipt_emission": True,
            "does_not_use_raw_receipt_hash_as_truth_surface": True,
            "does_not_use_rowid_as_signature_identity": True,
            "does_not_count_debug_sidecar_as_signature_payload": True,
        },
        "terminal_decision": terminal_decision,
        "terminal": {
            "type": "ADVANCE" if terminal_decision == "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS" else "STOP",
            "next_command_goal": "DESIGN_STABLE_DELTA_SIGNATURE_SCALE_BANDS_V0" if terminal_decision == "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS" else None,
            "stop_code": None if terminal_decision == "NEEDS_MORE_SCALE_AFTER_LOCAL_PASS" else terminal_decision,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    probe_id = sha8({
        "candidate_design_id": probe["candidate_design_id"],
        "compression_version": probe["compression_version"],
        "source_policy_id": probe["source_policy_id"],
        "selected_run_ids": run_ids,
        "source_surface": surface,
        "burden_measurements": probe["burden_measurements"],
        "distinguishability_measurements": probe["distinguishability_measurements"],
        "terminal_decision": terminal_decision,
    })
    probe["candidate_probe_id"] = probe_id
    probe["candidate_probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in output_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["rows_path"] = f"data/stable_delta_signature_candidate_v0_1_rows/{probe_id}.jsonl"

    receipt_id = sha8(probe)
    receipt = dict(probe)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    receipt["schema_version"] = "stable_delta_signature_candidate_v0_1_probe_receipt_v0"

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

    probe, receipt = build_candidate_probe(
        policy_id=args.policy_id,
        run_id=args.run_id,
        max_runs=args.max_runs,
        max_receipts=args.max_receipts,
    )

    print(json.dumps({
        "candidate_probe_id": receipt["candidate_probe_id"],
        "receipt_id": receipt["receipt_id"],
        "gate": receipt["gate"],
        "mode": receipt["mode"],
        "source_policy_id": receipt["source_policy_id"],
        "source_diagnostic_id": receipt["source_diagnostic_id"],
        "compression_version": receipt["compression_version"],
        "selected_run_ids": receipt["selected_run_ids"],
        "source_surface": receipt["source_surface"],
        "burden_measurements": receipt["burden_measurements"],
        "distinguishability_measurements": receipt["distinguishability_measurements"],
        "pass_gates": receipt["pass_gates"],
        "truth_surface": receipt["truth_surface"],
        "authority_guards": receipt["authority_guards"],
        "negative_claims": receipt["negative_claims"],
        "terminal_decision": receipt["terminal_decision"],
        "terminal": receipt["terminal"],
        "failures": receipt["failures"],
        "warnings": receipt["warnings"],
    }, indent=2, sort_keys=True))
    print(f"candidate_probe_id={receipt['candidate_probe_id']}")
    print(f"candidate_rows_path={receipt['rows_path']}")
    print(f"candidate_receipt_path=data/stable_delta_signature_candidate_v0_1_receipts/{receipt['candidate_probe_id']}.json")

    # A terminal FAIL_* is a valid candidate result. Exit nonzero only if harness gate failed.
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
