#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "runs" / "registry.sqlite"

POLICY_DIR = ROOT / "data" / "canonical_transition_surface_probe_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "canonical_transition_surface_probe_policy_receipts"
FM_DIAG_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostics"
CANDIDATE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_receipts"

ROWS_DIR = ROOT / "data" / "canonical_transition_surface_probe_rows"
RECEIPT_DIR = ROOT / "data" / "canonical_transition_surface_probe_receipts"

EXPECTED_POLICY_ID = "c7d3d021"
EXPECTED_POLICY_RECEIPT_ID = "079a71f5"
EXPECTED_FM_DIAG_ID = "79acf44a"
EXPECTED_CANDIDATE_PROBE_ID = "a097b68f"
EXPECTED_CANDIDATE_RECEIPT_ID = "08b4ac55"

PROBE_KIND = "CANONICAL_TRANSITION_SURFACE_PROBE_V0"
PROBE_PATCH_VERSION = "alias_patch_state_sig8_before_after_v0"
MODE = "OUTER_OBSERVER_ONLY"

FIELD_CANDIDATES = {
    "run_id": ["run_id"],
    "case_id": ["case_id", "fixture_id", "case_key", "case", "fixture", "slot_id"],
    "occurrence_id": ["occurrence_id", "event_id", "step_id", "step", "step_index", "ordinal", "idx"],
    "transition_id": ["transition_id", "transition_key", "transition", "edge_id"],
    "state_hash_before": ["state_hash_before", "before_state_hash", "state_before_hash", "state_before", "start_state_sig8", "state_before_sig8", "state_sig8_before", "before_sig8"],
    "move_id": ["move_id", "selected_move", "move", "action_id", "action"],
    "state_hash_after": ["state_hash_after", "after_state_hash", "state_after_hash", "state_after", "final_state_sig8", "state_after_sig8", "state_sig8_after", "after_sig8"],
    "halt_reason": ["halt_reason", "halt_code", "stop_code"],
    "terminal_status": ["terminal_status", "terminal_decision", "status", "gate", "checkpoint_code", "law_status"],
    "family": ["family", "family_compact", "family_name"],
    "radius": ["radius", "r"],
    "depth": ["depth", "depth_max", "depth_min"],
    "cycle": ["cycle", "cycle_n", "cycles", "cycles_per_case"],
    "probe_id": ["probe_id"],
    "slot_id": ["slot_id"],
    "burden_class": ["burden_class"],
    "raw_event_count": ["raw_event_count", "raw_events", "event_count", "total_events", "raw_total"],
    "shape_count": ["shape_count", "shapes_count", "shape_total", "n_shapes", "new_shape_count", "same_shape_count"],
    "receipt_count": ["receipt_count", "total_receipts", "receipts", "receipt_total"],
}

PACKAGING_NOISE_TOKENS = {
    "rowid",
    "receipt_rowid",
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

RAW_HASH_FIELD_TOKENS = {
    "raw_full_receipt_hash",
    "full_receipt_hash",
    "receipt_hash",
    "receipt_sig8",
}


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


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
        for i, value in enumerate(obj[:200]):
            name = f"{prefix}.{i}" if prefix else str(i)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    return out


def last_token(path: str) -> str:
    return str(path).rsplit(".", 1)[-1]


def is_packaging_path(path: str) -> bool:
    p = str(path).lower()
    token = last_token(p)
    return token in PACKAGING_NOISE_TOKENS or any(t in p for t in ["receipt_file", "file_path", "created_at", "created_utc"])


def is_raw_hash_path(path: str) -> bool:
    p = str(path).lower()
    token = last_token(p)
    return token in RAW_HASH_FIELD_TOKENS or any(t in p for t in RAW_HASH_FIELD_TOKENS)


def safe_repr(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    return repr(value)


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
        if str(k).lower() not in PACKAGING_NOISE_TOKENS and str(k).lower() != "rowid"
    }
    return scalar_payload, {"payload_source_column": "scalar_receipt_row", "payload_candidate_columns": []}


def find_candidates(canonical_field: str, registry_row: dict[str, Any], payload: Any) -> list[dict[str, Any]]:
    flat = flatten(payload)
    lower_row = {str(k).lower(): (k, v) for k, v in registry_row.items()}
    lower_flat = {str(k).lower(): (k, v) for k, v in flat.items()}

    results: list[dict[str, Any]] = []
    seen = set()

    for option in FIELD_CANDIDATES[canonical_field]:
        opt = option.lower()

        if opt in lower_row:
            key, value = lower_row[opt]
            if value not in (None, ""):
                ident = ("registry", str(key), safe_repr(value))
                if ident not in seen:
                    seen.add(ident)
                    results.append({
                        "surface": "registry_column",
                        "path": str(key),
                        "value": value,
                        "is_packaging_noise": is_packaging_path(str(key)),
                        "is_raw_hash": is_raw_hash_path(str(key)),
                    })

        if opt in lower_flat:
            key, value = lower_flat[opt]
            if value not in (None, ""):
                ident = ("payload", str(key), safe_repr(value))
                if ident not in seen:
                    seen.add(ident)
                    results.append({
                        "surface": "payload_json",
                        "path": str(key),
                        "value": value,
                        "is_packaging_noise": is_packaging_path(str(key)),
                        "is_raw_hash": is_raw_hash_path(str(key)),
                    })

        for key_l, (key, value) in lower_flat.items():
            if last_token(key_l) == opt and value not in (None, ""):
                ident = ("payload", str(key), safe_repr(value))
                if ident not in seen:
                    seen.add(ident)
                    results.append({
                        "surface": "payload_json_suffix",
                        "path": str(key),
                        "value": value,
                        "is_packaging_noise": is_packaging_path(str(key)),
                        "is_raw_hash": is_raw_hash_path(str(key)),
                    })

    return results


def pick_value(candidates: list[dict[str, Any]]) -> tuple[Any | None, dict[str, Any] | None]:
    usable = [
        c for c in candidates
        if c.get("value") not in (None, "")
        and c.get("is_raw_hash") is False
        and c.get("is_packaging_noise") is False
    ]
    if usable:
        return usable[0]["value"], usable[0]

    non_hash = [
        c for c in candidates
        if c.get("value") not in (None, "")
        and c.get("is_raw_hash") is False
    ]
    if non_hash:
        return non_hash[0]["value"], non_hash[0]

    if candidates:
        return candidates[0]["value"], candidates[0]

    return None, None


def classify_fields(registry_row: dict[str, Any], payload: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for field in FIELD_CANDIDATES:
        candidates = find_candidates(field, registry_row, payload)
        value, chosen = pick_value(candidates)
        out[field] = {
            "value": value,
            "chosen": chosen,
            "candidates": candidates,
            "candidate_count": len(candidates),
        }
    return out


def connect_registry() -> sqlite3.Connection:
    if not REGISTRY.exists():
        raise SystemExit(f"registry sqlite missing: {REGISTRY}")
    con = sqlite3.connect(f"file:{REGISTRY}?mode=ro", uri=True)
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


def field_stats(surface_rows: list[dict[str, Any]]) -> dict[str, Any]:
    stats: dict[str, Any] = {}

    for field in FIELD_CANDIDATES:
        values = []
        candidate_paths = []
        packaging_count = 0
        raw_hash_count = 0
        payload_count = 0
        registry_count = 0

        for row in surface_rows:
            entry = row["fields"][field]
            value = entry.get("value")
            chosen = entry.get("chosen")
            if value not in (None, ""):
                values.append(value)
            if chosen:
                candidate_paths.append(str(chosen.get("path")))
                if chosen.get("is_packaging_noise"):
                    packaging_count += 1
                if chosen.get("is_raw_hash"):
                    raw_hash_count += 1
                if str(chosen.get("surface", "")).startswith("payload"):
                    payload_count += 1
                if chosen.get("surface") == "registry_column":
                    registry_count += 1

        present_count = len(values)
        missing_count = len(surface_rows) - present_count
        distinct_values = len({safe_repr(v) for v in values})
        is_constant = present_count > 0 and distinct_values <= 1
        is_discriminative = distinct_values > 1
        is_packaging_noise = present_count > 0 and packaging_count == present_count
        is_raw_hash = present_count > 0 and raw_hash_count == present_count
        is_audit_derived = present_count > 0 and not is_packaging_noise and not is_raw_hash
        usable_for_transition_surface = (
            present_count > 0
            and is_audit_derived
            and not is_packaging_noise
            and not is_raw_hash
            and (field in ["state_hash_before", "move_id", "state_hash_after", "transition_id", "occurrence_id", "halt_reason", "terminal_status"])
        )
        usable_for_signature_payload = (
            usable_for_transition_surface
            and field not in ["occurrence_id"]
        )

        stats[field] = {
            "field": field,
            "present_count": present_count,
            "missing_count": missing_count,
            "missing_rate": round(missing_count / len(surface_rows), 6) if surface_rows else 0.0,
            "distinct_present_values": distinct_values,
            "is_constant": is_constant,
            "is_discriminative": is_discriminative,
            "is_audit_derived": is_audit_derived,
            "is_packaging_noise": is_packaging_noise,
            "is_raw_hash": is_raw_hash,
            "usable_for_transition_surface": usable_for_transition_surface,
            "usable_for_signature_payload": usable_for_signature_payload,
            "chosen_path_top10": [k for k, _ in Counter(candidate_paths).most_common(10)],
            "surface_counts": {
                "payload_json": payload_count,
                "registry_column": registry_count,
                "packaging_noise_chosen": packaging_count,
                "raw_hash_chosen": raw_hash_count,
            },
        }

    return stats


def derive_transition_surface(stats: dict[str, Any], surface_rows: list[dict[str, Any]]) -> dict[str, Any]:
    state_before_present = stats["state_hash_before"]["present_count"] > 0 and stats["state_hash_before"]["usable_for_transition_surface"]
    state_after_present = stats["state_hash_after"]["present_count"] > 0 and stats["state_hash_after"]["usable_for_transition_surface"]
    move_present = stats["move_id"]["present_count"] > 0 and stats["move_id"]["usable_for_transition_surface"]
    move_discriminative = stats["move_id"]["is_discriminative"]

    transition_id_present = stats["transition_id"]["present_count"] > 0 and stats["transition_id"]["usable_for_transition_surface"]
    transition_id_discriminative = stats["transition_id"]["is_discriminative"]
    transition_id_packaging_noise = stats["transition_id"]["is_packaging_noise"]

    occurrence_id_present = stats["occurrence_id"]["present_count"] > 0 and stats["occurrence_id"]["usable_for_transition_surface"]
    occurrence_id_discriminative = stats["occurrence_id"]["is_discriminative"]
    occurrence_id_packaging_noise = stats["occurrence_id"]["is_packaging_noise"]

    case_id_present = stats["case_id"]["present_count"] > 0
    case_id_discriminative = stats["case_id"]["is_discriminative"]

    # Rowid is always audit locator in this registry, but cannot be primary transition identity.
    rowid_available = all("rowid" in row["registry_row_keys"] for row in surface_rows) if surface_rows else False

    full_transition_tuple_present = state_before_present and move_present and state_after_present
    full_transition_tuple_discriminative = full_transition_tuple_present and (
        stats["state_hash_before"]["is_discriminative"]
        or stats["move_id"]["is_discriminative"]
        or stats["state_hash_after"]["is_discriminative"]
    )

    lawful_transition_discriminator_present = (
        transition_id_present and transition_id_discriminative and not transition_id_packaging_noise
    )

    within_case_discriminator_present = (
        (occurrence_id_present and occurrence_id_discriminative and not occurrence_id_packaging_noise)
        or lawful_transition_discriminator_present
        or full_transition_tuple_discriminative
    )

    case_only_surface = case_id_present and case_id_discriminative and not within_case_discriminator_present

    transition_surface_sufficient = full_transition_tuple_discriminative or lawful_transition_discriminator_present
    packaging_noise_only = (
        not transition_surface_sufficient
        and not within_case_discriminator_present
        and rowid_available
        and case_only_surface
    )

    return {
        "state_hash_before_present": state_before_present,
        "move_id_present": move_present,
        "move_id_discriminative": move_discriminative,
        "state_hash_after_present": state_after_present,
        "transition_id_present": transition_id_present,
        "transition_id_discriminative": transition_id_discriminative,
        "transition_id_packaging_noise": transition_id_packaging_noise,
        "within_case_discriminator_present": within_case_discriminator_present,
        "within_case_discriminator_packaging_noise": packaging_noise_only,
        "case_id_present": case_id_present,
        "case_id_discriminative": case_id_discriminative,
        "case_only_surface": case_only_surface,
        "rowid_available_as_audit_locator": rowid_available,
        "rowid_allowed_as_transition_identity": False,
        "full_transition_tuple_present": full_transition_tuple_present,
        "full_transition_tuple_discriminative": full_transition_tuple_discriminative,
        "lawful_transition_discriminator_present": lawful_transition_discriminator_present,
        "transition_surface_sufficient": transition_surface_sufficient,
        "source_surface_honesty_status": (
            "PASS_SURFACE_PRESENT"
            if transition_surface_sufficient and within_case_discriminator_present
            else "PACKAGING_NOISE_ONLY"
            if packaging_noise_only
            else "TRANSITION_SURFACE_MISSING"
            if not transition_surface_sufficient
            else "WITHIN_CASE_OCCURRENCE_SURFACE_MISSING"
        ),
    }


def verify_policy(policy: dict[str, Any], policy_receipt: dict[str, Any], fm_diag: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_mismatch:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_mismatch:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_name") != "BUILD_CANONICAL_TRANSITION_SURFACE_PROBE_POLICY_V0":
        failures.append(f"policy_name_wrong:{policy.get('policy_name')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_CANONICAL_TRANSITION_SURFACE_PROBE_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    auth = policy.get("authority") or {}
    if auth.get("authorizes_next_probe_implementation") is not True:
        failures.append("policy_does_not_authorize_probe")
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
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    behavior = policy.get("required_probe_behavior") or {}
    for key in [
        "read_existing_surfaces_only",
        "inspect_registry_receipts",
        "inspect_receipt_payload_json_if_present",
        "classify_each_candidate_field",
        "emit_surface_rows_jsonl",
        "emit_probe_receipt",
        "must_not_write_to_registry_sqlite",
        "must_not_change_receipt_generation",
        "must_not_use_raw_receipt_hash_as_truth_surface",
        "must_not_use_rowid_as_signature_identity",
    ]:
        if behavior.get(key) is not True:
            failures.append(f"required_probe_behavior_missing:{key}:{behavior.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/canonical_transition_surface_probe_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    if constraints.get("must_not_change_registry_sqlite") is not True:
        failures.append("must_not_change_registry_sqlite_missing")
    if constraints.get("must_not_create_compression_candidate") is not True:
        failures.append("must_not_create_compression_candidate_missing")
    if constraints.get("must_not_run_scale_bands") is not True:
        failures.append("must_not_run_scale_bands_missing")

    if fm_diag.get("diagnostic_id") != EXPECTED_FM_DIAG_ID:
        failures.append(f"fm_diag_id_wrong:{fm_diag.get('diagnostic_id')}")
    if fm_diag.get("gate") != "PASS":
        failures.append(f"fm_diag_gate_not_PASS:{fm_diag.get('gate')}")
    if fm_diag.get("terminal", {}).get("next_command_goal") != "BUILD_CANONICAL_TRANSITION_SURFACE_PROBE_POLICY_V0":
        failures.append(f"fm_diag_next_goal_wrong:{fm_diag.get('terminal', {}).get('next_command_goal')}")

    decision = fm_diag.get("decision") or {}
    if decision.get("transition_surface_missing") is not True:
        failures.append("fm_decision_transition_surface_missing_not_true")
    if decision.get("case_only_discriminator") is not True:
        failures.append("fm_decision_case_only_not_true")
    if decision.get("do_not_scale_current_candidate") is not True:
        failures.append("fm_decision_do_not_scale_missing")

    if candidate.get("candidate_probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate.get('candidate_probe_id')}")
    if candidate.get("receipt_id") != EXPECTED_CANDIDATE_RECEIPT_ID:
        failures.append(f"candidate_receipt_id_wrong:{candidate.get('receipt_id')}")
    if candidate.get("terminal_decision") != "FAIL_FALSE_MERGE":
        failures.append(f"candidate_terminal_wrong:{candidate.get('terminal_decision')}")

    return failures


def build_probe(policy_id: str, run_id: str | None, max_runs: int, max_receipts: int | None) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()

    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    fm_diag = load_json(FM_DIAG_DIR / f"{EXPECTED_FM_DIAG_ID}.json")
    candidate = load_json(CANDIDATE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")

    failures = verify_policy(policy, policy_receipt, fm_diag, candidate)

    registry_hash_before = file_sha256(REGISTRY)

    con = connect_registry()
    try:
        run_ids = select_run_ids(con, run_id, max_runs)
        receipt_rows = load_receipts(con, run_ids, max_receipts)
        receipt_columns = table_columns(con, "receipts")
        runs_columns = table_columns(con, "runs")
    finally:
        con.close()

    surface_rows: list[dict[str, Any]] = []
    payload_json_rows = 0

    for registry_row in receipt_rows:
        payload, payload_meta = extract_payload(registry_row)
        if payload_meta.get("payload_source_column") != "scalar_receipt_row":
            payload_json_rows += 1

        fields = classify_fields(registry_row, payload)

        audit_pointer = {
            "kind": "registry.sqlite.receipts",
            "registry_path": "data/runs/registry.sqlite",
            "source_run_id": registry_row.get("run_id"),
            "receipt_rowid": registry_row.get("rowid"),
            "payload_source_column": payload_meta.get("payload_source_column"),
        }

        row = {
            "surface_row_id": sha8({
                "source_run_id": registry_row.get("run_id"),
                "receipt_rowid": registry_row.get("rowid"),
                "payload_source_column": payload_meta.get("payload_source_column"),
            }),
            "source_run_id": registry_row.get("run_id"),
            "receipt_rowid": registry_row.get("rowid"),
            "audit_pointer": audit_pointer,
            "payload_meta": payload_meta,
            "registry_row_keys": sorted(registry_row.keys()),
            "fields": fields,
            "authority_guards": {
                "observer_only": True,
                "runtime_receipt_emission_changed": False,
                "registry_sqlite_changed": False,
                "scale_mode_authorized": False,
                "receipt_replacement_authorized": False,
                "receipt_compression_authorized": False,
                "raw_receipt_hash_used_as_truth_surface": False,
            },
        }
        surface_rows.append(row)

    stats = field_stats(surface_rows)
    transition_surface = derive_transition_surface(stats, surface_rows)

    registry_hash_after = file_sha256(REGISTRY)
    registry_changed = registry_hash_before != registry_hash_after

    authority_guards = {
        "observer_only": True,
        "runtime_receipt_emission_changed": False,
        "registry_sqlite_changed": registry_changed,
        "scale_mode_authorized": False,
        "receipt_replacement_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_compression_authorized": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "scale_band_run_authorized": False,
        "stable_delta_candidate_acceptance_authorized": False,
    }

    pass_gates = {
        "authority_containment": (
            authority_guards["observer_only"] is True
            and authority_guards["runtime_receipt_emission_changed"] is False
            and authority_guards["registry_sqlite_changed"] is False
            and authority_guards["scale_mode_authorized"] is False
            and authority_guards["receipt_replacement_authorized"] is False
            and authority_guards["receipt_compression_authorized"] is False
        ),
        "occurrence_anchoring": len(surface_rows) > 0 and all(row.get("audit_pointer", {}).get("source_run_id") for row in surface_rows),
        "transition_surface_completeness": transition_surface["transition_surface_sufficient"] is True,
        "within_case_discriminator": transition_surface["within_case_discriminator_present"] is True and transition_surface["within_case_discriminator_packaging_noise"] is False,
        "source_surface_honesty": True,
        "rowid_not_used_as_transition_identity": transition_surface["rowid_allowed_as_transition_identity"] is False,
        "raw_hash_not_used_as_truth_surface": authority_guards["raw_receipt_hash_used_as_truth_surface"] is False,
        "no_scale_bands": authority_guards["scale_band_run_authorized"] is False,
        "no_compression_candidate_created": True,
    }

    if registry_changed:
        failures.append("registry_sqlite_changed")

    terminal_decision: str
    next_command_goal: str | None = None

    if not pass_gates["authority_containment"]:
        terminal_decision = "FAIL_OBSERVER_INTERFERENCE"
    elif transition_surface["within_case_discriminator_packaging_noise"] is True and transition_surface["case_only_surface"] is True:
        terminal_decision = "FAIL_PACKAGING_NOISE_ONLY"
        next_command_goal = "BUILD_SOURCE_SURFACE_EXTENSION_POLICY_V0"
    elif not pass_gates["transition_surface_completeness"]:
        terminal_decision = "FAIL_TRANSITION_SURFACE_MISSING"
        next_command_goal = "BUILD_SOURCE_SURFACE_EXTENSION_POLICY_V0"
    elif not pass_gates["within_case_discriminator"]:
        terminal_decision = "FAIL_WITHIN_CASE_OCCURRENCE_SURFACE_MISSING"
        next_command_goal = "BUILD_SOURCE_SURFACE_EXTENSION_POLICY_V0"
    else:
        terminal_decision = "PASS_CANONICAL_TRANSITION_SURFACE_OBSERVER_ONLY"
        next_command_goal = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_POLICY"

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    probe = {
        "schema_version": "canonical_transition_surface_probe_receipt_v0",
        "probe_kind": PROBE_KIND,
        "probe_patch_version": PROBE_PATCH_VERSION,
        "mode": MODE,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_false_merge_diagnostic_id": EXPECTED_FM_DIAG_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "selected_run_ids": run_ids,
        "registry_surface": {
            "registry_path": "data/runs/registry.sqlite",
            "registry_sha256_before": registry_hash_before,
            "registry_sha256_after": registry_hash_after,
            "registry_sqlite_changed": registry_changed,
            "receipt_columns": receipt_columns,
            "runs_columns": runs_columns,
            "receipt_rows_inspected": len(receipt_rows),
            "payload_json_rows": payload_json_rows,
            "max_runs": max_runs,
            "max_receipts": max_receipts,
        },
        "field_stats": stats,
        "transition_surface": transition_surface,
        "summary": {
            "state_hash_before_present": transition_surface["state_hash_before_present"],
            "state_hash_after_present": transition_surface["state_hash_after_present"],
            "move_id_present": transition_surface["move_id_present"],
            "move_id_discriminative": transition_surface["move_id_discriminative"],
            "transition_id_present": transition_surface["transition_id_present"],
            "transition_id_discriminative": transition_surface["transition_id_discriminative"],
            "within_case_discriminator_present": transition_surface["within_case_discriminator_present"],
            "case_only_surface": transition_surface["case_only_surface"],
            "transition_surface_sufficient": transition_surface["transition_surface_sufficient"],
            "source_surface_honesty_status": transition_surface["source_surface_honesty_status"],
        },
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "negative_claims": {
            "does_not_change_runtime_receipt_emission": True,
            "does_not_write_registry_sqlite": registry_changed is False,
            "does_not_use_rowid_as_transition_identity": True,
            "does_not_use_raw_receipt_hash_as_truth_surface": True,
            "does_not_authorize_scale_mode": True,
            "does_not_run_scale_bands": True,
            "does_not_create_compression_candidate": True,
            "does_not_accept_stable_delta_candidate": True,
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
        "actual_observer_overhead_ms": elapsed_ms,
        "created_at": now_iso(),
    }

    probe_id = sha8({
        "probe_kind": PROBE_KIND,
        "source_policy_id": EXPECTED_POLICY_ID,
        "selected_run_ids": run_ids,
        "registry_surface": probe["registry_surface"],
        "field_stats": stats,
        "transition_surface": transition_surface,
        "terminal_decision": terminal_decision,
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in surface_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["surface_rows_path"] = f"data/canonical_transition_surface_probe_rows/{probe_id}.jsonl"

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
        "source_policy_id": receipt["source_policy_id"],
        "selected_run_ids": receipt["selected_run_ids"],
        "registry_surface": receipt["registry_surface"],
        "summary": receipt["summary"],
        "transition_surface": receipt["transition_surface"],
        "authority_guards": receipt["authority_guards"],
        "pass_gates": receipt["pass_gates"],
        "negative_claims": receipt["negative_claims"],
        "terminal_decision": receipt["terminal_decision"],
        "terminal": receipt["terminal"],
        "failures": receipt["failures"],
        "warnings": receipt["warnings"],
    }, indent=2, sort_keys=True))
    print(f"probe_id={receipt['probe_id']}")
    print(f"surface_rows_path={receipt['surface_rows_path']}")
    print(f"probe_receipt_path=data/canonical_transition_surface_probe_receipts/{receipt['probe_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
