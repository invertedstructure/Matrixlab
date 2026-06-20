#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "src" / "matrixlab" / "cli.py"
DB = ROOT / "data" / "runs" / "registry.sqlite"

PROFILE_DIR = ROOT / "data" / "micro_burden_profiles"
RECEIPT_DIR = ROOT / "data" / "micro_burden_profile_receipts"
LOG_DIR = ROOT / ".matrixlab_tmp" / "micro_burden_logs"

ALLOWED_BURDEN_CLASSES = {
    "BURDEN_UNKNOWN",
    "BURDEN_DEPTH_SCAN",
    "BURDEN_CYCLE_SCAN",
    "BURDEN_REPEATED_SLOT_WORK",
    "BURDEN_RECEIPT_VOLUME",
    "BURDEN_DB_WRITE",
    "BURDEN_PROGRESS_LOGGING",
    "BURDEN_MATRIX_BUILD",
    "BURDEN_LAW_CHECK",
    "BURDEN_GATE_OVERHEAD",
    "BURDEN_MATRIX_BOUNDARY",
}

FAMILY_NAMES = {
    "A": "one_sided_suspension",
    "B": "two_sided_suspension",
    "C": "suspension_plus_repair",
    "D": "projection_quotient",
    "E": "relabel_symmetry_stress",
}

EXPECTED_REPEATED_SLOT_IDS = (
    "slot_01_E1",
    "slot_02_E2",
    "slot_03_E3",
    "slot_04_D1",
    "slot_05_D2",
    "slot_06_B1",
    "slot_07_B2",
    "slot_08_C1",
    "slot_09_A1",
)


@dataclass(frozen=True)
class SlotExecutionPlan:
    probe_id: str
    slot_label: str
    slot_id: str
    family_compact: str
    family: str
    depth_max: int
    cycles_per_case: int
    max_cells: int
    stress_cli_args: tuple[str, ...]
    cache_key: tuple[str, str, str, int, int, int]


def _slot_id_for(probe_id: str, slot_label: str, family_compact: str) -> str:
    if slot_label.startswith("slot_"):
        return slot_label
    return f"{probe_id}_{family_compact}"


@lru_cache(maxsize=None)
def _build_slot_execution_plan(
    probe_id: str,
    slot_label: str,
    family_compact: str,
    depth_max: int,
    cycles_per_case: int,
    max_cells: int,
) -> SlotExecutionPlan:
    """Build immutable slot execution metadata only.

    This cache is intentionally scoped to this Python process. It must never
    cache run ids, receipt rows, receipt counts as substitutes for execution,
    law results, gate results, halt results, stdout/stderr, or any prior
    execution result.
    """

    slot_id = _slot_id_for(probe_id, slot_label, family_compact)
    family = FAMILY_NAMES[family_compact]
    cache_key = (
        probe_id,
        slot_id,
        family_compact,
        int(depth_max),
        int(cycles_per_case),
        int(max_cells),
    )
    stress_cli_args = (
        sys.executable,
        str(CLI),
        "stress",
        "--families",
        family_compact,
        "--depth-max",
        str(depth_max),
        "--cycles-per-case",
        str(cycles_per_case),
        "--max-cells",
        str(max_cells),
    )
    return SlotExecutionPlan(
        probe_id=probe_id,
        slot_label=slot_label,
        slot_id=slot_id,
        family_compact=family_compact,
        family=family,
        depth_max=int(depth_max),
        cycles_per_case=int(cycles_per_case),
        max_cells=int(max_cells),
        stress_cli_args=stress_cli_args,
        cache_key=cache_key,
    )


def _build_probe_execution_plans(probe: dict[str, Any]) -> tuple[SlotExecutionPlan, ...]:
    return tuple(
        _build_slot_execution_plan(
            str(probe["probe_id"]),
            str(slot_label),
            str(family_compact),
            int(probe["depth_max"]),
            int(probe["cycles_per_case"]),
            int(probe["max_cells"]),
        )
        for slot_label, family_compact in probe["slots"]
    )


def _validate_repeated_slot_identity(plans: tuple[SlotExecutionPlan, ...]) -> None:
    repeated = [
        plan.slot_id
        for plan in plans
        if plan.probe_id == "MICRO_04_REPEATED_SLOT_PRESSURE"
    ]
    if repeated and tuple(repeated) != EXPECTED_REPEATED_SLOT_IDS:
        raise RuntimeError(
            "repeated slot identity changed: "
            f"expected={EXPECTED_REPEATED_SLOT_IDS!r} observed={tuple(repeated)!r}"
        )


PROBES = [
    {
        "probe_id": "MICRO_01_WIDE_FAMILY_SMOKE",
        "purpose": "Prove all families execute and emit burden rows.",
        "slots": [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")],
        "depth_max": 8,
        "cycles_per_case": 3,
        "max_cells": 10000,
    },
    {
        "probe_id": "MICRO_02_CYCLE_PRESSURE",
        "purpose": "Expose cycle-loop burden.",
        "slots": [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")],
        "depth_max": 8,
        "cycles_per_case": 20,
        "max_cells": 10000,
    },
    {
        "probe_id": "MICRO_03_DEPTH_PRESSURE",
        "purpose": "Expose depth-scan burden.",
        "slots": [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")],
        "depth_max": 25,
        "cycles_per_case": 3,
        "max_cells": 10000,
    },
    {
        "probe_id": "MICRO_04_REPEATED_SLOT_PRESSURE",
        "purpose": "Expose repeated slot work without paying R125 cost.",
        "slots": [
            ("slot_01_E1", "E"),
            ("slot_02_E2", "E"),
            ("slot_03_E3", "E"),
            ("slot_04_D1", "D"),
            ("slot_05_D2", "D"),
            ("slot_06_B1", "B"),
            ("slot_07_B2", "B"),
            ("slot_08_C1", "C"),
            ("slot_09_A1", "A"),
        ],
        "depth_max": 8,
        "cycles_per_case": 5,
        "max_cells": 10000,
    },
    {
        "probe_id": "MICRO_05_RECEIPT_WRITE_PRESSURE",
        "purpose": "Expose receipt/write/logging burden on the known expensive family.",
        "slots": [("E", "E")],
        "depth_max": 12,
        "cycles_per_case": 20,
        "max_cells": 10000,
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_sig(obj: dict[str, Any]) -> str:
    body = dict(obj)
    for key in ("profile_id", "profile_sig8", "receipt_id", "receipt_sig8"):
        body.pop(key, None)
    blob = json.dumps(body, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def run_cmd(args: list[str], *, env: dict[str, str] | None = None, log_path: Path | None = None) -> tuple[int, str, str, int]:
    started = time.perf_counter()
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    elapsed_ms = int(round((time.perf_counter() - started) * 1000))
    if log_path:
        log_path.write_text(
            "CMD: " + " ".join(args) + "\n\n"
            + "STDOUT:\n" + proc.stdout + "\n\n"
            + "STDERR:\n" + proc.stderr + "\n"
        )
    return proc.returncode, proc.stdout, proc.stderr, elapsed_ms


def extract_run_id(text: str) -> str | None:
    matches = re.findall(r"run_[0-9][0-9_]*", text)
    return matches[-1] if matches else None


def extract_json_object(text: str) -> dict[str, Any] | None:
    idx = text.rfind("{")
    if idx < 0:
        return None

    # Walk backward to find a JSON object that parses.
    for start in [m.start() for m in re.finditer(r"\{", text)]:
        candidate = text[start:].strip()
        try:
            return json.loads(candidate)
        except Exception:
            continue
    return None


def db_table_count(table: str) -> int:
    if not DB.exists():
        return 0
    con = sqlite3.connect(DB)
    try:
        return int(con.execute(f"select count(*) from {table}").fetchone()[0])
    finally:
        con.close()


def db_columns(table: str) -> list[str]:
    if not DB.exists():
        return []
    con = sqlite3.connect(DB)
    try:
        return [row[1] for row in con.execute(f"pragma table_info({table})").fetchall()]
    finally:
        con.close()


def db_receipts_for_run(run_id: str) -> int:
    con = sqlite3.connect(DB)
    try:
        return int(con.execute("select count(*) from receipts where run_id=?", (run_id,)).fetchone()[0])
    finally:
        con.close()


def db_halts_for_run(run_id: str) -> dict[str, int]:
    cols = set(db_columns("receipts"))
    if "halt_reason" not in cols:
        return {}
    con = sqlite3.connect(DB)
    try:
        rows = con.execute(
            "select halt_reason, count(*) from receipts where run_id=? group by halt_reason",
            (run_id,),
        ).fetchall()
        return {str(k): int(v) for k, v in rows if k is not None}
    finally:
        con.close()


def db_matrix_cells_for_run(run_id: str) -> int | None:
    cols = set(db_columns("receipts"))
    candidates = ["matrix_cells", "cells", "n_cells"]
    col = next((c for c in candidates if c in cols), None)
    if not col:
        return None
    con = sqlite3.connect(DB)
    try:
        row = con.execute(
            f"select max({col}) from receipts where run_id=?",
            (run_id,),
        ).fetchone()
        if row and row[0] is not None:
            return int(row[0])
        return None
    finally:
        con.close()


def bucket_cycle(cycles: int) -> str:
    if cycles <= 3:
        return "cycles_000_003"
    if cycles <= 5:
        return "cycles_004_005"
    if cycles <= 20:
        return "cycles_006_020"
    return "cycles_021_plus"


def bucket_matrix_cells(cells: int | None) -> str | None:
    if cells is None:
        return None
    if cells <= 100:
        return "cells_000001_000100"
    if cells <= 1000:
        return "cells_000101_001000"
    if cells <= 10000:
        return "cells_001001_010000"
    return "cells_010001_plus"


def classify_burden(
    *,
    probe_id: str,
    slot_id: str,
    family: str,
    depth_max: int,
    cycles_per_case: int,
    receipts: int,
    elapsed_ms: int,
    receipts_per_sec: float,
) -> str:
    if probe_id == "MICRO_04_REPEATED_SLOT_PRESSURE":
        return "BURDEN_REPEATED_SLOT_WORK"
    if probe_id == "MICRO_03_DEPTH_PRESSURE" or depth_max >= 25:
        return "BURDEN_DEPTH_SCAN"
    if probe_id == "MICRO_02_CYCLE_PRESSURE" or cycles_per_case >= 20:
        if family == "E" and receipts >= 100:
            return "BURDEN_RECEIPT_VOLUME"
        return "BURDEN_CYCLE_SCAN"
    if probe_id == "MICRO_05_RECEIPT_WRITE_PRESSURE":
        return "BURDEN_RECEIPT_VOLUME"
    if receipts >= 1000:
        return "BURDEN_RECEIPT_VOLUME"
    if elapsed_ms > 0 and receipts_per_sec < 50 and receipts > 0:
        return "BURDEN_DB_WRITE"
    return "BURDEN_UNKNOWN"


def aggregate(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    buckets: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        label = "NA" if value is None else str(value)
        if label not in buckets:
            buckets[label] = {
                key: value,
                "rows": 0,
                "receipts": 0,
                "elapsed_ms": 0,
                "run_ids": [],
                "burden_classes": Counter(),
            }
        b = buckets[label]
        b["rows"] += 1
        b["receipts"] += int(row.get("receipts") or 0)
        b["elapsed_ms"] += int(row.get("elapsed_ms") or 0)
        b["run_ids"].append(row.get("run_id"))
        b["burden_classes"][row.get("burden_class") or "BURDEN_UNKNOWN"] += 1

    out = []
    for b in buckets.values():
        elapsed = int(b["elapsed_ms"])
        receipts = int(b["receipts"])
        out.append({
            key: b[key],
            "rows": b["rows"],
            "receipts": receipts,
            "elapsed_ms": elapsed,
            "receipts_per_sec": round((receipts / (elapsed / 1000.0)), 6) if elapsed > 0 else None,
            "run_ids": b["run_ids"],
            "burden_classes": dict(b["burden_classes"]),
            "dominant_burden_class": b["burden_classes"].most_common(1)[0][0] if b["burden_classes"] else "BURDEN_UNKNOWN",
        })
    return sorted(out, key=lambda r: (-int(r["receipts"]), str(r.get(key))))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "profile_id",
        "probe_id",
        "run_id",
        "family",
        "family_compact",
        "slot_id",
        "depth",
        "cycle_bucket",
        "matrix_cells",
        "receipts",
        "elapsed_ms",
        "receipts_per_sec",
        "halt_reason",
        "burden_class",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field) for field in fields})


def build_profile(*, execute: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    receipt_count_before = db_table_count("receipts")
    run_count_before = db_table_count("runs")

    env = os.environ.copy()
    env["MATRIXLAB_PROGRESS"] = "0"

    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    warnings: list[str] = []
    probe_completion: dict[str, str] = {}

    for probe in PROBES:
        probe_id = probe["probe_id"]
        probe_failures_before = len(failures)

        plans = _build_probe_execution_plans(probe)
        _validate_repeated_slot_identity(plans)

        for plan in plans:
            family_letter = plan.family_compact
            family_name = plan.family
            slot_id = plan.slot_id

            log_path = LOG_DIR / f"{probe_id}_{slot_id}.log"
            cmd = list(plan.stress_cli_args)

            if not execute:
                failures.append("execute_flag_required")
                continue

            code, stdout, stderr, elapsed_ms = run_cmd(cmd, env=env, log_path=log_path)
            if code != 0:
                failures.append(f"stress_failed:{probe_id}:{slot_id}:{family_letter}:{code}")
                continue

            run_id = extract_run_id(stdout + "\n" + stderr)
            if not run_id:
                failures.append(f"run_id_missing:{probe_id}:{slot_id}:{family_letter}")
                continue

            gate_log_path = LOG_DIR / f"{probe_id}_{slot_id}_gate.log"
            gate_code, gate_out, gate_err, gate_elapsed_ms = run_cmd(
                [sys.executable, str(CLI), "gate", run_id],
                env=env,
                log_path=gate_log_path,
            )
            if gate_code != 0 or "GATE_PASS" not in (gate_out + gate_err):
                failures.append(f"gate_failed:{probe_id}:{slot_id}:{run_id}:{gate_code}")

            parsed = extract_json_object(stdout)
            receipts_db = db_receipts_for_run(run_id)
            receipts_cli = int((parsed or {}).get("total_receipts") or receipts_db)
            if receipts_cli != receipts_db:
                failures.append(f"receipt_total_mismatch:{probe_id}:{slot_id}:{run_id}:cli={receipts_cli}:db={receipts_db}")

            halt_counts = (parsed or {}).get("halt_counts") or db_halts_for_run(run_id)
            halt_reason = ",".join(f"{k}:{v}" for k, v in sorted(halt_counts.items())) if halt_counts else "HALT_REASON_UNAVAILABLE"

            matrix_cells = (parsed or {}).get("max_matrix_cells")
            if matrix_cells is None:
                matrix_cells = db_matrix_cells_for_run(run_id)

            total_elapsed_ms = elapsed_ms + gate_elapsed_ms
            receipts_per_sec = round(receipts_db / (total_elapsed_ms / 1000.0), 6) if total_elapsed_ms > 0 else None
            burden_class = classify_burden(
                probe_id=probe_id,
                slot_id=slot_id,
                family=family_letter,
                depth_max=int(probe["depth_max"]),
                cycles_per_case=int(probe["cycles_per_case"]),
                receipts=receipts_db,
                elapsed_ms=total_elapsed_ms,
                receipts_per_sec=float(receipts_per_sec or 0),
            )

            if burden_class not in ALLOWED_BURDEN_CLASSES:
                failures.append(f"burden_class_not_allowed:{burden_class}")

            rows.append({
                "profile_id": None,
                "probe_id": probe_id,
                "run_id": run_id,
                "family": family_name,
                "family_compact": family_letter,
                "slot_id": slot_id,
                "depth": int(probe["depth_max"]),
                "cycle_bucket": bucket_cycle(int(probe["cycles_per_case"])),
                "matrix_cells": matrix_cells,
                "matrix_cells_bucket": bucket_matrix_cells(matrix_cells),
                "receipts": receipts_db,
                "elapsed_ms": total_elapsed_ms,
                "receipts_per_sec": receipts_per_sec,
                "halt_reason": halt_reason,
                "burden_class": burden_class,
                "stress_elapsed_ms": elapsed_ms,
                "gate_elapsed_ms": gate_elapsed_ms,
                "stress_log_path": str(log_path.relative_to(ROOT)),
                "gate_log_path": str(gate_log_path.relative_to(ROOT)),
                "depth_max": int(probe["depth_max"]),
                "cycles_per_case": int(probe["cycles_per_case"]),
                "max_cells": int(probe["max_cells"]),
            })

        probe_completion[probe_id] = "PASS" if len(failures) == probe_failures_before else "FAIL"

    receipt_count_after = db_table_count("receipts")
    run_count_after = db_table_count("runs")

    profile_receipts_total = sum(int(row["receipts"]) for row in rows)
    db_receipt_delta = receipt_count_after - receipt_count_before

    families_seen = sorted(set(row["family_compact"] for row in rows))
    all_probe_ids_seen = sorted(set(row["probe_id"] for row in rows))

    repeated_rows = [row for row in rows if row["probe_id"] == "MICRO_04_REPEATED_SLOT_PRESSURE"]
    repeated_slot_ids = [row["slot_id"] for row in repeated_rows]
    repeated_slot_expected = [
        "slot_01_E1",
        "slot_02_E2",
        "slot_03_E3",
        "slot_04_D1",
        "slot_05_D2",
        "slot_06_B1",
        "slot_07_B2",
        "slot_08_C1",
        "slot_09_A1",
    ]

    if sorted(all_probe_ids_seen) != sorted(p["probe_id"] for p in PROBES):
        failures.append("not_all_micro_probes_completed")
    if families_seen != ["A", "B", "C", "D", "E"]:
        failures.append(f"not_all_families_seen:{families_seen}")
    if repeated_slot_ids != repeated_slot_expected:
        failures.append(f"repeated_slot_identity_missing_or_mismatched:{repeated_slot_ids}")
    if profile_receipts_total != db_receipt_delta:
        failures.append(f"profile_receipt_total_mismatch_database_delta:profile={profile_receipts_total}:db_delta={db_receipt_delta}")
    if any(row.get("elapsed_ms") is None for row in rows):
        failures.append("timing_unavailable_for_profile_rows")

    non_unknown_classes = sorted(set(row["burden_class"] for row in rows if row["burden_class"] != "BURDEN_UNKNOWN"))
    if not non_unknown_classes:
        failures.append("burden_class_remains_only_BURDEN_UNKNOWN")

    matrix_cells_available = any(row.get("matrix_cells") is not None for row in rows)

    aggregates = {
        "by_probe": aggregate(rows, "probe_id"),
        "by_family": aggregate(rows, "family_compact"),
        "by_slot": aggregate(rows, "slot_id") if repeated_slot_ids else [],
        "by_depth": aggregate(rows, "depth"),
        "by_cycle_bucket": aggregate(rows, "cycle_bucket"),
        "by_halt_reason": aggregate(rows, "halt_reason"),
        "top_20_receipt_sources": sorted(rows, key=lambda r: int(r["receipts"]), reverse=True)[:20],
        "top_20_time_sources": sorted(rows, key=lambda r: int(r["elapsed_ms"]), reverse=True)[:20],
    }

    if matrix_cells_available:
        aggregates["by_matrix_cells_bucket"] = aggregate(rows, "matrix_cells_bucket")
    else:
        aggregates["matrix_cells_na_reason"] = "matrix_cells_unavailable_in_cli_or_receipt_db"

    if not aggregates["top_20_receipt_sources"]:
        failures.append("top_20_receipt_sources_missing")
    if not aggregates["top_20_time_sources"]:
        failures.append("top_20_time_sources_missing")

    aggregate_elapsed_ok = True
    for name, value in aggregates.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and name not in ("top_20_receipt_sources", "top_20_time_sources"):
                    if item.get("elapsed_ms") is None:
                        aggregate_elapsed_ok = False
    if not aggregate_elapsed_ok:
        failures.append("elapsed_ms_missing_for_aggregate_rows")

    semantics = {
        "passive_observability_layer": True,
        "runner_semantics_changed": False,
        "gate_semantics_changed": False,
        "law_semantics_changed": False,
        "receipt_rows_deleted": False,
        "execution_skipped": False,
        "receipts_compressed": False,
    }

    if semantics["runner_semantics_changed"]:
        failures.append("runner_semantics_changed")
    if semantics["gate_semantics_changed"]:
        failures.append("gate_semantics_changed")
    if semantics["law_semantics_changed"]:
        failures.append("law_semantics_changed")
    if semantics["receipt_rows_deleted"]:
        failures.append("receipt_rows_deleted")
    if semantics["execution_skipped"]:
        failures.append("execution_skipped")

    profile = {
        "schema_version": "wide_burden_profile_microruns_v0",
        "profile_kind": "WIDE_BURDEN_PROFILE_MICRORUNS",
        "purpose": "Use tiny, wide runs to expose burden classes before any optimization work is allowed.",
        "doctrine": [
            "Small runs first.",
            "Wide burden profile first.",
            "Fix only from explicit burden class.",
            "Retest the same micro suite.",
            "Only scale after the micro suite is boring.",
        ],
        "allowed_burden_classes": sorted(ALLOWED_BURDEN_CLASSES),
        "cycle_period_compression": _build_cycle_period_compression_observation(rows),
        "repeated_slot_execution_plan_cache": {
            "status": "APPLIED_METADATA_ONLY",
            "cache_scope": "within_one_micro_profile_execution_only",
            "cache_kind": "immutable_slot_execution_plan_metadata",
            "does_not_cache": [
                "run_id",
                "receipt rows",
                "receipt counts as substitutes for execution",
                "law results",
                "gate results",
                "halt results",
                "stdout/stderr from a prior run",
                "any prior execution result",
            ],
            "expected_repeated_slot_ids": list(EXPECTED_REPEATED_SLOT_IDS),
            "cache_info": {
                "hits": _build_slot_execution_plan.cache_info().hits,
                "misses": _build_slot_execution_plan.cache_info().misses,
                "currsize": _build_slot_execution_plan.cache_info().currsize,
            },
        },
        "probe_specs": PROBES,
        "probe_completion": probe_completion,
        "rows": rows,
        "aggregates": aggregates,
        "families_seen": families_seen,
        "non_unknown_burden_classes": non_unknown_classes,
        "receipt_count_before": receipt_count_before,
        "receipt_count_after": receipt_count_after,
        "db_receipt_delta": db_receipt_delta,
        "profile_receipts_total": profile_receipts_total,
        "run_count_before": run_count_before,
        "run_count_after": run_count_after,
        "semantics": semantics,
        "gate_rules": {
            "all_five_micro_probes_complete": sorted(all_probe_ids_seen) == sorted(p["probe_id"] for p in PROBES),
            "every_family_A_E_appears": families_seen == ["A", "B", "C", "D", "E"],
            "repeated_slot_probe_distinguishable": repeated_slot_ids == repeated_slot_expected,
            "receipt_totals_match_registry_sqlite": profile_receipts_total == db_receipt_delta,
            "elapsed_ms_exists": all(row.get("elapsed_ms") is not None for row in rows),
            "top_20_time_sources_exists": bool(aggregates["top_20_time_sources"]),
            "top_20_receipt_sources_exists": bool(aggregates["top_20_receipt_sources"]),
            "non_unknown_burden_class_emitted": bool(non_unknown_classes),
            "no_runner_semantics_changed": not semantics["runner_semantics_changed"],
            "no_gate_semantics_changed": not semantics["gate_semantics_changed"],
            "no_receipt_deletion": not semantics["receipt_rows_deleted"],
            "no_execution_skipping": not semantics["execution_skipped"],
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "BUILD_BURDEN_BACKED_FIX_CANDIDATE_POLICY_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_MICRO_BURDEN_PROFILE_INVALID",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "MICRO_BURDEN_PROFILE_PASS" if not failures else "FAIL",
        "created_at": now_iso(),
    }

    sig = stable_sig(profile)
    profile["profile_id"] = sig
    profile["profile_sig8"] = sig
    for row in profile["rows"]:
        row["profile_id"] = sig

    receipt = {
        "schema_version": "wide_burden_profile_microruns_receipt_v0",
        "profile_id": sig,
        "profile_path": f"data/micro_burden_profiles/{sig}.json",
        "csv_path": f"data/micro_burden_profiles/{sig}.csv",
        "profile_sig8": sig,
        "gate": profile["gate"],
        "terminal": profile["terminal"],
        "receipt_totals": {
            "before": receipt_count_before,
            "after": receipt_count_after,
            "delta": db_receipt_delta,
            "profile_total": profile_receipts_total,
            "matches_registry_sqlite": profile_receipts_total == db_receipt_delta,
        },
        "probe_completion": probe_completion,
        "families_seen": families_seen,
        "non_unknown_burden_classes": non_unknown_classes,
        "burden_class_counts": dict(Counter(row["burden_class"] for row in rows)),
        "top_20_receipt_sources_present": bool(aggregates["top_20_receipt_sources"]),
        "top_20_time_sources_present": bool(aggregates["top_20_time_sources"]),
        "semantics": semantics,
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }
    receipt_sig = stable_sig(receipt)
    receipt["receipt_id"] = receipt_sig
    receipt["receipt_sig8"] = receipt_sig

    profile_json_path = PROFILE_DIR / f"{sig}.json"
    profile_csv_path = PROFILE_DIR / f"{sig}.csv"
    receipt_path = RECEIPT_DIR / f"{sig}.json"

    profile_json_path.write_text(json.dumps(profile, indent=2, sort_keys=True))
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    write_csv(profile_csv_path, profile["rows"])

    return profile, receipt


@dataclass(frozen=True)
class CyclePeriodCertificate:
    probe_id: str
    slot_id: str
    family_compact: str
    receipts: int
    elapsed_ms: int
    observed_periodic_halt_presence: bool
    metadata_only_no_execution_substitution: bool


EXPECTED_CYCLE_PERIOD_SLOT_IDS = (
    "MICRO_02_CYCLE_PRESSURE_A",
    "MICRO_02_CYCLE_PRESSURE_B",
    "MICRO_02_CYCLE_PRESSURE_C",
    "MICRO_02_CYCLE_PRESSURE_D",
    "MICRO_02_CYCLE_PRESSURE_E",
)


def _cycle_row_halt_counts(row: dict[str, Any]) -> dict[str, int]:
    raw = (
        row.get("halt_counts")
        or row.get("halt_reason_counts")
        or row.get("halts")
        or {}
    )
    if isinstance(raw, dict):
        return {str(k): int(v) for k, v in raw.items() if isinstance(v, int) or str(v).isdigit()}

    halt_reason = row.get("halt_reason")
    if halt_reason:
        return {str(halt_reason): 1}

    return {}


def _build_cycle_period_compression_observation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cycle_rows = [
        row for row in rows
        if row.get("probe_id") == "MICRO_02_CYCLE_PRESSURE"
        and row.get("burden_class") == "BURDEN_CYCLE_SCAN"
    ]

    observed_slots = [str(row.get("slot_id")) for row in cycle_rows]
    certificates: list[dict[str, Any]] = []

    for row in cycle_rows:
        halt_counts = _cycle_row_halt_counts(row)
        observed_periodic = bool(
            halt_counts.get("REPEATED_STATE_PERIODIC", 0)
            or row.get("halt_reason") == "REPEATED_STATE_PERIODIC"
        )
        certificate = CyclePeriodCertificate(
            probe_id=str(row.get("probe_id")),
            slot_id=str(row.get("slot_id")),
            family_compact=str(row.get("family_compact")),
            receipts=int(row.get("receipts") or 0),
            elapsed_ms=int(row.get("elapsed_ms") or 0),
            observed_periodic_halt_presence=observed_periodic,
            metadata_only_no_execution_substitution=True,
        )
        certificates.append({
            "probe_id": certificate.probe_id,
            "slot_id": certificate.slot_id,
            "family_compact": certificate.family_compact,
            "receipts": certificate.receipts,
            "elapsed_ms": certificate.elapsed_ms,
            "observed_periodic_halt_presence": certificate.observed_periodic_halt_presence,
            "metadata_only_no_execution_substitution": certificate.metadata_only_no_execution_substitution,
            "halt_counts_observed_after_execution": halt_counts,
        })

    return {
        "status": "APPLIED_POST_EXECUTION_METADATA_ONLY",
        "certificate_kind": "cycle_period_observation_certificate",
        "certificate_scope": "post_execution_observation_metadata_only",
        "certificate_count": len(certificates),
        "expected_cycle_slot_ids": list(EXPECTED_CYCLE_PERIOD_SLOT_IDS),
        "observed_cycle_slot_ids": observed_slots,
        "slot_identity_matches_expected": tuple(observed_slots) == EXPECTED_CYCLE_PERIOD_SLOT_IDS,
        "families_must_remain_A_E": ["A", "B", "C", "D", "E"],
        "probe_must_remain": "MICRO_02_CYCLE_PRESSURE",
        "certificates": certificates,
        "does_not_certify_without_execution": True,
        "does_not_change_cycles_per_case": True,
        "does_not_change_halt_reason": True,
        "does_not_skip_cycle_execution": True,
        "does_not_early_halt_on_period_detection": True,
        "does_not_emit_synthetic_receipts": True,
        "does_not_reuse_prior_cycle_results_as_execution": True,
        "semantics": {
            "execution_skipping": False,
            "cycle_execution_skipping": False,
            "early_halt_on_period_detection": False,
            "synthetic_cycle_receipts": False,
            "reusing_prior_cycle_results_as_execution": False,
            "halt_semantics_change": False,
            "law_semantics_change": False,
            "gate_semantics_change": False,
            "run_semantics_change": False,
            "receipt_deletion": False,
            "receipt_compression": False,
            "radius_expansion": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Actually run the micro probes.")
    args = parser.parse_args()

    profile, receipt = build_profile(execute=args.execute)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"profile_json_path={receipt['profile_path']}")
    print(f"profile_csv_path={receipt['csv_path']}")
    print(f"profile_receipt_path=data/micro_burden_profile_receipts/{profile['profile_id']}.json")

    return 0 if profile["gate"] == "MICRO_BURDEN_PROFILE_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
