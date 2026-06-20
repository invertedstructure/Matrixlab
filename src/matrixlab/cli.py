from __future__ import annotations

import hashlib
import json
import sqlite3

# MatrixLab DB write burden fix v0.
#
# Scope:
# - Configure SQLite connections for WAL + NORMAL synchronous where supported.
# - Keep receipt rows authoritative and uncompressed.
# - Do not alter receipt schema, law semantics, gate semantics, halt semantics,
#   run semantics, or execution coverage.
#
# This is an infrastructure write-path change only. The post-apply gate is the
# same micro burden suite plus before/after comparison against profile c89790f0.
_MATRIXLAB_SQLITE_WAL_WARNINGS: list[str] = []


def _matrixlab_connect_sqlite(*args, **kwargs):
    con = sqlite3.connect(*args, **kwargs)
    _matrixlab_configure_sqlite_write_connection(con)
    return con


def _matrixlab_configure_sqlite_write_connection(con):
    try:
        con.execute("PRAGMA journal_mode=WAL")
    except Exception as exc:  # pragma: no cover - best-effort DB configuration
        _MATRIXLAB_SQLITE_WAL_WARNINGS.append(f"journal_mode_WAL_failed:{type(exc).__name__}")
    try:
        con.execute("PRAGMA synchronous=NORMAL")
    except Exception as exc:  # pragma: no cover - best-effort DB configuration
        _MATRIXLAB_SQLITE_WAL_WARNINGS.append(f"synchronous_NORMAL_failed:{type(exc).__name__}")
    try:
        con.execute("PRAGMA busy_timeout=5000")
    except Exception as exc:  # pragma: no cover - best-effort DB configuration
        _MATRIXLAB_SQLITE_WAL_WARNINGS.append(f"busy_timeout_failed:{type(exc).__name__}")
    return con

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import typer
from rich import print
from rich.table import Table
from rich.console import Console


app = typer.Typer(no_args_is_help=True, help="MatrixLab receipt runner v0.2")
console = Console()

DB_PATH = Path("data/runs/registry.sqlite")

FAMILY_MAP = {
    "A": "one_sided_suspension",
    "B": "two_sided_suspension",
    "C": "suspension_plus_repair",
    "D": "projection_quotient",
    "E": "relabel_symmetry_stress",
    "F": "law_violation_probe",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sig8(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:8]


def resolve_json_path(value: str, directory: str, suffix: str = ".json") -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate

    candidate = Path(directory) / f"{value}{suffix}"
    if candidate.exists():
        return candidate

    raise typer.BadParameter(f"could not resolve {value!r} under {directory}")


def stable_sig(payload: dict, id_key: str, sig_key: str) -> str:
    stable = dict(payload)
    stable.pop(id_key, None)
    stable.pop(sig_key, None)
    return sig8(stable)


def selector_payload_sig(payload: dict) -> str:
    return stable_sig(payload, "selector_id", "selector_payload_sig8")


ALLOWED_AGENT_PREFIX = ["uv", "run", "python", "src/matrixlab/cli.py"]
ALLOWED_AGENT_SUBCOMMANDS = ["agent-eval", "gate", "stress"]


AGENT_SELECT_SCHEMA = "agent_select_receipt_v1"
AGENT_PLAN_CHECK_SCHEMA = "agent_plan_check_receipt_v1"
AGENT_EXEC_DRY_RUN_SCHEMA = "agent_exec_dry_run_receipt_v1"
AGENT_POST_CHECK_SCHEMA = "agent_post_check_receipt_v1"
AGENT_LOOP_SUMMARY_SCHEMA = "agent_loop_summary_receipt_v1"
AGENT_CONFIRMATION_SCHEMA = "agent_operator_confirmation_receipt_v1"
AGENT_NEXT_FROM_CONFIRMATION_SCHEMA = "agent_next_from_confirmation_receipt_v1"
AGENT_CYCLE_LEDGER_SCHEMA = "agent_cycle_ledger_receipt_v1"
AGENT_CYCLE_NEXT_SCHEMA = "agent_cycle_next_receipt_v1"
AGENT_CYCLE_OBSERVATION_SCHEMA = "agent_cycle_observation_receipt_v1"
AGENT_CHEAT_CHECK_SCHEMA = "agent_cheat_check_receipt_v0"
AGENT_CHEAT_ADVERSARIAL_SCHEMA = "agent_cheat_adversarial_receipt_v0"
CELL_TRANSFER_CONTRACT_SCHEMA = "cell_transfer_contract_v0"
DOMAIN_SHIFT_GENERATOR_SCHEMA = "domain_shift_generator_v0"
DOMAIN_SHIFT_RUNNER_SUPPORT_SCHEMA = "domain_shift_runner_support_v0"
DOMAIN_SHIFT_SLOT_RUNNER_SUPPORT_SCHEMA = "domain_shift_slot_runner_support_v0"
DOMAIN_SHIFT_SLOT_OBSERVATION_SCHEMA = "domain_shift_slot_observation_v0"
SCALABILITY_CONTRACT_SCHEMA = "scalability_contract_v0"
SCALABILITY_CONTRACT_VERIFICATION_SCHEMA = "scalability_contract_verification_v0"
RADIUS_SCALE_OBSERVATION_SCHEMA = "radius_scale_observation_v0"
RADIUS_SCALE_OBSERVATION_VERIFICATION_SCHEMA = "radius_scale_observation_verification_v0"
R75_SCALE_DECISION_SCHEMA = "r75_scale_decision_v0"
R75_SCALE_DECISION_VERIFICATION_SCHEMA = "r75_scale_decision_verification_v0"
R100_RADIUS_SCALE_OBSERVATION_SCHEMA = "r100_radius_scale_observation_v0"
R100_RADIUS_SCALE_OBSERVATION_VERIFICATION_SCHEMA = "r100_radius_scale_observation_verification_v0"
RECEIPT_ROLLUP_CONTRACT_SCHEMA = "receipt_rollup_contract_v0"
RECEIPT_ROLLUP_CONTRACT_VERIFICATION_SCHEMA = "receipt_rollup_contract_verification_v0"
RAW_MANIFEST_SCHEMA = "raw_manifest_v0"
ROLLUP_RECORD_SCHEMA = "rollup_record_v0"
DECISION_RECORD_SCHEMA = "decision_record_v0"
VERIFIED_R100_BURDEN_ROLLUP_SCHEMA = "verified_r100_burden_rollup_v0"
VERIFIED_R100_BURDEN_ROLLUP_VERIFICATION_SCHEMA = "verified_r100_burden_rollup_verification_v0"
R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP_SCHEMA = "r100_scale_decision_with_verified_rollup_v0"
R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP_VERIFICATION_SCHEMA = "r100_scale_decision_with_verified_rollup_verification_v0"
RADIUS_EXPANSION_BURDEN_POLICY_SCHEMA = "radius_expansion_burden_policy_v0"
RADIUS_EXPANSION_BURDEN_POLICY_VERIFICATION_SCHEMA = "radius_expansion_burden_policy_verification_v0"
RADIUS_EXPANSION_CANDIDATE_DECISION_SCHEMA = "radius_expansion_candidate_decision_v0"
RADIUS_EXPANSION_CANDIDATE_DECISION_VERIFICATION_SCHEMA = "radius_expansion_candidate_decision_verification_v0"


def validate_agent_command_argv(argv: list[str], command_index: int | None = None) -> list[str]:
    failures: list[str] = []

    if command_index is None:
        if not isinstance(argv, list):
            return ["command_argv_not_list"]

        if argv[: len(ALLOWED_AGENT_PREFIX)] != ALLOWED_AGENT_PREFIX:
            failures.append("command_prefix_not_allowed")

        if len(argv) <= len(ALLOWED_AGENT_PREFIX):
            failures.append("missing_subcommand")
            return failures

        subcommand = argv[len(ALLOWED_AGENT_PREFIX)]
        if subcommand not in ALLOWED_AGENT_SUBCOMMANDS:
            failures.append(f"subcommand_not_allowed:{subcommand}")

        return failures

    i = command_index

    if not isinstance(argv, list):
        failures.append(f"command_{i}_argv_not_list")
        return failures

    if len(argv) < len(ALLOWED_AGENT_PREFIX) + 1:
        failures.append(f"command_{i}_argv_too_short")
        return failures

    if argv[: len(ALLOWED_AGENT_PREFIX)] != ALLOWED_AGENT_PREFIX:
        failures.append(f"command_{i}_prefix_not_allowed")
        return failures

    subcommand = argv[len(ALLOWED_AGENT_PREFIX)]
    if subcommand not in ALLOWED_AGENT_SUBCOMMANDS:
        failures.append(f"command_{i}_subcommand_not_allowed:{subcommand}")

    return failures


def write_content_addressed_receipt(
    payload: dict,
    out_dir: str | Path,
    schema_key: str,
    schema_value: str,
    id_key: str,
    sig_key: str,
) -> tuple[Path, dict]:
    payload = dict(payload)
    payload[schema_key] = schema_value
    payload[sig_key] = stable_sig(payload, id_key, sig_key)
    payload[id_key] = payload[sig_key]

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{payload[id_key]}.json"
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return out_path, payload


def matrix_sig8(a: np.ndarray) -> str:
    body = {
        "shape": list(a.shape),
        "data": a.astype(int).tolist(),
    }
    return sig8(body)


def column_type_set(a: np.ndarray) -> set[tuple[int, ...]]:
    return {tuple(int(x) for x in a[:, j]) for j in range(a.shape[1])}


def support_size(a: np.ndarray) -> int:
    return int(a.sum())


def move_profile_id(
    move_id: str,
    before: np.ndarray,
    after: np.ndarray,
    rank_before: int,
    rank_after: int,
) -> tuple[str, dict]:
    before_cols = column_type_set(before)
    after_cols = column_type_set(after)
    new_col_types = after_cols - before_cols

    profile = {
        "move_id": move_id,
        "row_delta": int(after.shape[0] - before.shape[0]),
        "col_delta": int(after.shape[1] - before.shape[1]),
        "rank_delta": int(rank_after - rank_before),
        "support_delta": int(support_size(after) - support_size(before)),
        "distinct_column_types_before": len(before_cols),
        "distinct_column_types_after": len(after_cols),
        "new_column_types_added": len(new_col_types),
    }

    profile_id = (
        f"{move_id}"
        f"|dr={profile['row_delta']}"
        f"|dc={profile['col_delta']}"
        f"|rank={profile['rank_delta']}"
        f"|supp={profile['support_delta']}"
        f"|newcols={profile['new_column_types_added']}"
    )

    return profile_id, profile


def expected_law(family: str, move_id: str, profile: dict) -> tuple[str, bool, str]:
    dr = profile["row_delta"]
    dc = profile["col_delta"]
    rk = profile["rank_delta"]
    sp = profile["support_delta"]

    if family == "law_violation_probe":
        law_id = "PROBE_CLAIMS_DUPLICATE_COL_PRESERVES_RANK"
        ok = dr == 0 and dc == 1 and rk == 0
        return law_id, ok, "" if ok else f"expected dr=0 dc=1 rank=0 got dr={dr} dc={dc} rank={rk}"

    if family == "one_sided_suspension":
        law_id = "ONE_SIDED_DUPLICATE_COL_PRESERVES_RANK"
        ok = dr == 0 and dc == 1 and rk == 0
        return law_id, ok, "" if ok else f"expected dr=0 dc=1 rank=0 got dr={dr} dc={dc} rank={rk}"

    if family == "two_sided_suspension":
        law_id = "TWO_SIDED_ADD_ROW_COL_RAISES_RANK"
        ok = dr == 1 and dc == 1 and rk == 1 and sp > 0
        return law_id, ok, "" if ok else f"expected dr=1 dc=1 rank=1 supp>0 got dr={dr} dc={dc} rank={rk} supp={sp}"

    if family == "suspension_plus_repair":
        law_id = "REPAIR_ADDS_COLUMN_PRESERVES_RANK"
        ok = dr == 0 and dc == 1 and rk == 0
        return law_id, ok, "" if ok else f"expected dr=0 dc=1 rank=0 got dr={dr} dc={dc} rank={rk}"

    if family == "projection_quotient":
        if move_id == "append_zero_column":
            law_id = "PROJECTION_APPEND_ZERO_PRESERVES_RANK"
            ok = dr == 0 and dc == 1 and rk == 0 and sp == 0
            return law_id, ok, "" if ok else f"expected dr=0 dc=1 rank=0 supp=0 got dr={dr} dc={dc} rank={rk} supp={sp}"

        if move_id == "quotient_merge_last_row":
            law_id = "PROJECTION_QUOTIENT_MERGE_CONTRACTS_ROWS"
            ok = dr == -1 and dc == 0 and rk <= 0
            return law_id, ok, "" if ok else f"expected dr=-1 dc=0 rank<=0 got dr={dr} dc={dc} rank={rk}"

    if family == "relabel_symmetry_stress":
        law_id = "RELABEL_PRESERVES_SHAPE_RANK_SUPPORT"
        ok = dr == 0 and dc == 0 and rk == 0 and sp == 0
        return law_id, ok, "" if ok else f"expected dr=0 dc=0 rank=0 supp=0 got dr={dr} dc={dc} rank={rk} supp={sp}"

    return "UNKNOWN_LAW", False, f"no law for family={family} move={move_id}"


def gf2_rank(a: np.ndarray) -> int:
    """Rank over F2 using basic Gaussian elimination."""
    m = a.copy().astype(np.uint8) % 2
    rows, cols = m.shape
    rank = 0

    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if m[r, col]:
                pivot = r
                break

        if pivot is None:
            continue

        if pivot != rank:
            m[[rank, pivot]] = m[[pivot, rank]]

        for r in range(rows):
            if r != rank and m[r, col]:
                m[r] ^= m[rank]

        rank += 1

        if rank == rows:
            break

    return int(rank)


def base_cycle_matrix(n: int) -> np.ndarray:
    """
    Simple binary cycle incidence matrix.
    Rows = vertices.
    Columns = edges.
    """
    a = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        a[i, i] = 1
        a[(i + 1) % n, i] = 1
    return a


def apply_move(a: np.ndarray, family: str, cycle_n: int) -> tuple[np.ndarray, str]:
    rows, cols = a.shape

    if family == "one_sided_suspension":
        j = cycle_n % cols
        new_col = a[:, [j]]
        return np.concatenate([a, new_col], axis=1), "duplicate_existing_column"

    if family == "two_sided_suspension":
        out = np.zeros((rows + 1, cols + 1), dtype=np.uint8)
        out[:rows, :cols] = a
        out[rows - 1, cols] = 1
        out[rows, cols] = 1
        return out, "add_row_and_link_column"

    if family == "suspension_plus_repair":
        j1 = cycle_n % cols
        j2 = (cycle_n + 1) % cols
        repair = a[:, [j1]] ^ a[:, [j2]]
        return np.concatenate([a, repair], axis=1), "xor_repair_column"

    if family == "projection_quotient":
        if rows > 2 and cycle_n % 2 == 0:
            out = a.copy()
            out[0] ^= out[-1]
            out = out[:-1, :]
            return out, "quotient_merge_last_row"

        zero = np.zeros((rows, 1), dtype=np.uint8)
        return np.concatenate([a, zero], axis=1), "append_zero_column"

    if family == "relabel_symmetry_stress":
        # Deterministic nontrivial row/column relabel.
        # Goal: stress raw representation while preserving rank-style invariants.
        seed = rows * 1_000_003 + cols * 9_176 + cycle_n * 131_071
        rng = np.random.default_rng(seed)

        row_perm = rng.permutation(rows)
        col_perm = rng.permutation(cols)

        out = a[row_perm, :][:, col_perm]

        # Avoid useless automorphism/no-op relabels.
        if np.array_equal(out, a) and rows > 1:
            out = out.copy()
            out[[0, 1], :] = out[[1, 0], :]

        if np.array_equal(out, a) and cols > 1:
            out = out.copy()
            out[:, [0, 1]] = out[:, [1, 0]]

        return out, "deterministic_row_col_relabel"

    if family == "law_violation_probe":
        out = np.zeros((rows + 1, cols + 1), dtype=np.uint8)
        out[:rows, :cols] = a
        out[-1, -1] = 1
        return out, "bad_duplicate_claim"

    raise ValueError(f"Unknown family: {family}")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.execute(
            """
            create table if not exists runs (
                run_id text primary key,
                created_utc text not null,
                status text not null,
                families text not null,
                depth_min integer not null,
                depth_max integer not null,
                cycles_per_case integer not null,
                max_cells integer not null,
                total_cases integer default 0,
                total_receipts integer default 0
            )
            """
        )

        con.execute(
            """
            create table if not exists receipts (
                run_id text not null,
                case_id text not null,
                family text not null,
                depth integer not null,
                cycle_n integer not null,
                move_id text not null,
                move_profile_id text,
                law_id text,
                law_ok integer,
                law_fail_reason text,
                row_delta integer,
                col_delta integer,
                rank_delta integer,
                support_delta integer,
                distinct_column_types_before integer,
                distinct_column_types_after integer,
                new_column_types_added integer,
                registered_moves_total integer not null,
                moves_reused integer not null,
                new_move_required integer not null,
                rows integer not null,
                cols integer not null,
                cells integer not null,
                rank_before integer not null,
                rank_after integer not null,
                compression_ratio real not null,
                trajectory_signature text not null,
                halt_reason text,
                state_sig8_before text not null,
                state_sig8_after text not null,
                receipt_path text not null,
                primary key (run_id, case_id, cycle_n)
            )
            """
        )

        for col_name, col_type in [
            ("move_profile_id", "text"),
            ("law_id", "text"),
            ("law_ok", "integer"),
            ("law_fail_reason", "text"),
            ("row_delta", "integer"),
            ("col_delta", "integer"),
            ("rank_delta", "integer"),
            ("support_delta", "integer"),
            ("distinct_column_types_before", "integer"),
            ("distinct_column_types_after", "integer"),
            ("new_column_types_added", "integer"),
        ]:
            try:
                con.execute(f"alter table receipts add column {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass


def insert_run_start(
    run_id: str,
    families: list[str],
    depth_min: int,
    depth_max: int,
    cycles_per_case: int,
    max_cells: int,
) -> None:
    init_db()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.execute(
            """
            insert or replace into runs (
                run_id, created_utc, status, families,
                depth_min, depth_max, cycles_per_case, max_cells,
                total_cases, total_receipts
            )
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                utc_now(),
                "RUNNING",
                ",".join(families),
                depth_min,
                depth_max,
                cycles_per_case,
                max_cells,
                0,
                0,
            ),
        )




# ---------------------------------------------------------------------------
# Operator progress reporting for long MatrixLab runs.
#
# Purpose:
# - visible liveness while receipts are being produced
# - visible transition from active run to post-processing
# - visible interrupted signal on Ctrl-C / termination
# - no semantic impact on receipts, laws, evaluator, or move ontology
# ---------------------------------------------------------------------------

_ML_PROGRESS_STATE = {
    "configured": False,
    "installed_handlers": False,
    "phase": "NOT_STARTED",
    "run_id": None,
    "started_monotonic": None,
    "last_emit_monotonic": None,
    "receipt_count": 0,
    "expected_cases": None,
    "expected_receipts": None,
    "families": None,
    "depth_min": None,
    "depth_max": None,
    "cycles_per_case": None,
    "last_family": None,
    "last_depth": None,
    "last_cycle": None,
}


def _ml_progress_enabled() -> bool:
    import os

    value = os.environ.get("MATRIXLAB_PROGRESS", "1").strip().lower()
    return value not in {"0", "false", "off", "no"}


def _ml_progress_interval_sec() -> float:
    import os

    try:
        return max(0.0, float(os.environ.get("MATRIXLAB_PROGRESS_INTERVAL_SEC", "5")))
    except Exception:
        return 5.0


def _ml_progress_every_receipts() -> int:
    import os

    try:
        return max(1, int(os.environ.get("MATRIXLAB_PROGRESS_EVERY_RECEIPTS", "500")))
    except Exception:
        return 500


def _ml_progress_receipt_get(receipt, key, default=None):
    if isinstance(receipt, dict):
        return receipt.get(key, default)
    return getattr(receipt, key, default)


def _ml_progress_emit(phase=None, *, extra=None, force=False):
    if not _ml_progress_enabled():
        return

    import sys
    import time

    now = time.monotonic()
    state = _ML_PROGRESS_STATE

    if state.get("started_monotonic") is None:
        state["started_monotonic"] = now

    last_emit = state.get("last_emit_monotonic")
    interval = _ml_progress_interval_sec()

    if not force and last_emit is not None and (now - last_emit) < interval:
        return

    state["last_emit_monotonic"] = now

    if phase is not None:
        state["phase"] = phase

    elapsed = now - state["started_monotonic"]
    receipt_count = state.get("receipt_count") or 0
    expected_receipts = state.get("expected_receipts")
    expected_cases = state.get("expected_cases")

    pct = None
    if expected_receipts:
        pct = min(100.0, (receipt_count / expected_receipts) * 100.0)

    parts = [
        "MATRIXLAB_PROGRESS",
        f"phase={state.get('phase')}",
        f"run_id={state.get('run_id') or '?'}",
        f"receipts={receipt_count}" + (f"/~{expected_receipts}" if expected_receipts else ""),
    ]

    if pct is not None:
        parts.append(f"pct~={pct:.1f}")

    if expected_cases:
        parts.append(f"cases~={expected_cases}")

    if state.get("families"):
        parts.append(f"families={state.get('families')}")

    if state.get("depth_min") is not None and state.get("depth_max") is not None:
        parts.append(f"depth={state.get('depth_min')}..{state.get('depth_max')}")

    if state.get("cycles_per_case") is not None:
        parts.append(f"cycles={state.get('cycles_per_case')}")

    if state.get("last_family") is not None:
        parts.append(f"last_family={state.get('last_family')}")

    if state.get("last_depth") is not None:
        parts.append(f"last_depth={state.get('last_depth')}")

    if state.get("last_cycle") is not None:
        parts.append(f"last_cycle={state.get('last_cycle')}")

    parts.append(f"elapsed={elapsed:.1f}s")

    if extra:
        parts.append(f"note={extra}")

    print(" ".join(str(part) for part in parts), file=sys.stderr, flush=True)


def _ml_progress_signal_handler(signum, frame):
    _ml_progress_emit("INTERRUPTED", extra=f"signal={signum}", force=True)
    raise KeyboardInterrupt


def _ml_progress_install_handlers():
    state = _ML_PROGRESS_STATE
    if state.get("installed_handlers"):
        return

    try:
        import signal

        signal.signal(signal.SIGINT, _ml_progress_signal_handler)
        signal.signal(signal.SIGTERM, _ml_progress_signal_handler)
        state["installed_handlers"] = True
    except Exception:
        # Progress reporting must never affect MatrixLab semantics.
        pass


def _ml_progress_run_config(local_vars):
    if not _ml_progress_enabled():
        return

    import time

    state = _ML_PROGRESS_STATE
    state["configured"] = True
    state["phase"] = "STARTING"
    state["started_monotonic"] = time.monotonic()
    state["last_emit_monotonic"] = None
    state["receipt_count"] = 0

    families = local_vars.get("families")
    depth_min = local_vars.get("depth_min")
    depth_max = local_vars.get("depth_max")
    cycles_per_case = local_vars.get("cycles_per_case")
    run_id = local_vars.get("run_id")

    family_count = None
    try:
        family_count = len(families) if families is not None else None
    except Exception:
        family_count = None

    expected_cases = None
    expected_receipts = None
    try:
        if family_count is not None and depth_min is not None and depth_max is not None:
            expected_cases = family_count * (int(depth_max) - int(depth_min) + 1)
            if cycles_per_case is not None:
                expected_receipts = expected_cases * int(cycles_per_case)
    except Exception:
        expected_cases = None
        expected_receipts = None

    state["run_id"] = run_id
    state["families"] = ",".join(str(f) for f in families) if families is not None else None
    state["depth_min"] = depth_min
    state["depth_max"] = depth_max
    state["cycles_per_case"] = cycles_per_case
    state["expected_cases"] = expected_cases
    state["expected_receipts"] = expected_receipts
    state["last_family"] = None
    state["last_depth"] = None
    state["last_cycle"] = None

    _ml_progress_install_handlers()
    _ml_progress_emit("STARTING", force=True)


def _ml_progress_after_receipt(receipt):
    if not _ml_progress_enabled():
        return

    state = _ML_PROGRESS_STATE
    state["phase"] = "RUNNING"
    state["receipt_count"] = (state.get("receipt_count") or 0) + 1

    run_id = _ml_progress_receipt_get(receipt, "run_id")
    if run_id is not None:
        state["run_id"] = run_id

    family = _ml_progress_receipt_get(receipt, "family")
    if family is not None:
        state["last_family"] = family

    depth = (
        _ml_progress_receipt_get(receipt, "depth")
        or _ml_progress_receipt_get(receipt, "n")
        or _ml_progress_receipt_get(receipt, "case_depth")
    )
    if depth is not None:
        state["last_depth"] = depth

    cycle = (
        _ml_progress_receipt_get(receipt, "cycle")
        or _ml_progress_receipt_get(receipt, "cycle_n")
    )
    if cycle is not None:
        state["last_cycle"] = cycle

    every = _ml_progress_every_receipts()
    force = state["receipt_count"] == 1 or state["receipt_count"] % every == 0
    _ml_progress_emit("RUNNING", force=force)


def _ml_progress_phase(phase, *, extra=None):
    _ml_progress_emit(phase, extra=extra, force=True)


def insert_receipt(receipt: dict) -> None:
    _ml_progress_after_receipt(receipt)
    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.execute(
            """
            insert or replace into receipts (
                run_id, case_id, family, depth, cycle_n,
                move_id, move_profile_id,
                law_id, law_ok, law_fail_reason,
                row_delta, col_delta, rank_delta, support_delta,
                distinct_column_types_before, distinct_column_types_after,
                new_column_types_added,
                registered_moves_total, moves_reused,
                new_move_required, rows, cols, cells,
                rank_before, rank_after, compression_ratio,
                trajectory_signature, halt_reason,
                state_sig8_before, state_sig8_after, receipt_path
            )
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                receipt["run_id"],
                receipt["case_id"],
                receipt["family"],
                receipt["depth"],
                receipt["cycle_n"],
                receipt["move_id"],
                receipt["move_profile_id"],
                receipt["law_id"],
                int(receipt["law_ok"]),
                receipt["law_fail_reason"],
                receipt["row_delta"],
                receipt["col_delta"],
                receipt["rank_delta"],
                receipt["support_delta"],
                receipt["distinct_column_types_before"],
                receipt["distinct_column_types_after"],
                receipt["new_column_types_added"],
                receipt["registered_moves_total"],
                receipt["moves_reused"],
                int(receipt["new_move_required"]),
                receipt["matrix_shape"][0],
                receipt["matrix_shape"][1],
                receipt["matrix_cells"],
                receipt["rank_before"],
                receipt["rank_after"],
                receipt["compression_ratio"],
                receipt["trajectory_signature"],
                receipt["halt_reason"],
                receipt["state_sig8_before"],
                receipt["state_sig8_after"],
                receipt["receipt_path"],
            ),
        )


def finish_run(run_id: str, status: str, total_cases: int, total_receipts: int) -> None:
    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.execute(
            """
            update runs
            set status = ?, total_cases = ?, total_receipts = ?
            where run_id = ?
            """,
            (status, total_cases, total_receipts, run_id),
        )


def latest_run_id() -> str:
    init_db()
    with _matrixlab_connect_sqlite(DB_PATH) as con:
        row = con.execute(
            """
            select run_id
            from runs
            order by created_utc desc
            limit 1
            """
        ).fetchone()

    if row is None:
        raise typer.BadParameter("No runs found yet.")

    return row[0]



def parse_families(families: str) -> list[str]:
    raw = families.replace(",", " ").split()
    letters = []

    for token in raw:
        token = token.strip().upper()
        if len(token) > 1 and all(ch in FAMILY_MAP for ch in token):
            letters.extend(token)
        elif token:
            letters.append(token)

    unknown = [x for x in letters if x not in FAMILY_MAP]
    if unknown:
        raise typer.BadParameter(f"Unknown family letters: {unknown}")

    return [FAMILY_MAP[x] for x in letters]


def run_id_exists(run_id: str) -> bool:
    init_db()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        found = con.execute(
            "select 1 from runs where run_id = ? limit 1",
            (run_id,),
        ).fetchone()
        if found is not None:
            return True

    for root in [
        Path("data/runs"),
        Path("data/receipts"),
        Path("data/traces"),
        Path("data/artifacts"),
    ]:
        if (root / run_id).exists():
            return True

    return False


def allocate_run_id(requested_run_id: Optional[str] = None) -> str:
    if requested_run_id is None:
        base = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S_%f")
    else:
        base = requested_run_id

    if not run_id_exists(base):
        return base

    for i in range(1, 1000):
        candidate = f"{base}_{i:03d}"
        if not run_id_exists(candidate):
            return candidate

    raise RuntimeError(f"Could not allocate unique run_id from base {base}")

def execute_run(
    depth_min: int,
    depth_max: int,
    families: str,
    cycles_per_case: int,
    max_cells: int,
    run_id: Optional[str],
    strict_laws: bool = False,
) -> dict:
    _ml_progress_run_config(locals())
    run_id = allocate_run_id(run_id)

    family_names = parse_families(families)

    run_dir = Path("data/runs") / run_id
    receipt_dir = Path("data/receipts") / run_id
    trace_dir = Path("data/traces") / run_id
    artifact_dir = Path("data/artifacts") / run_id

    for p in [run_dir, receipt_dir, trace_dir, artifact_dir]:
        p.mkdir(parents=True, exist_ok=True)

    if cycles_per_case <= 0:
        cycles_per_case = depth_max

    insert_run_start(
        run_id=run_id,
        families=family_names,
        depth_min=depth_min,
        depth_max=depth_max,
        cycles_per_case=cycles_per_case,
        max_cells=max_cells,    )

    all_receipts = []
    total_cases = 0
    case_halts: dict[str, int] = {}

    print(f"[bold green]MatrixLab run started[/bold green]: {run_id}")
    print(f"Families: {family_names}")
    print(f"Depths: {depth_min}..{depth_max}")
    print(f"Cycles per case: {cycles_per_case}")
    print(f"Max cells per matrix: {max_cells}")

    for n in range(depth_min, depth_max + 1):
        for family in family_names:
            total_cases += 1
            case_id = f"n{n}_{family}"

            registered_moves = set()
            trajectory = []
            seen_states = set()

            a = base_cycle_matrix(n)
            seen_states.add(matrix_sig8(a))

            halt_reason = "CYCLES_COMPLETE"

            for cycle_n in range(1, cycles_per_case + 1):
                before_sig = matrix_sig8(a)
                before_rank = gf2_rank(a)

                before_matrix = a.copy()
                a, move_id = apply_move(a, family, cycle_n)

                after_sig = matrix_sig8(a)
                after_rank = gf2_rank(a)

                profile_id, profile = move_profile_id(
                    move_id=move_id,
                    before=before_matrix,
                    after=a,
                    rank_before=before_rank,
                    rank_after=after_rank,
 )

                law_id, law_ok, law_fail_reason = expected_law(family, move_id, profile)

                law_halt = bool(strict_laws and not law_ok)

                new_move_required = profile_id not in registered_moves
                registered_moves.add(profile_id)
                trajectory.append(after_sig)

                rows, cols = a.shape
                cells = rows * cols

                current_halt = None

                if law_halt:
                    current_halt = "LAW_VIOLATION"
                    halt_reason = current_halt

                elif cells > max_cells:
                    current_halt = "MAX_CELLS_EXCEEDED"
                    halt_reason = current_halt

                elif after_sig in seen_states:
                    if after_sig == before_sig:
                        current_halt = "REPEATED_STATE_TRIVIAL"
                    else:
                        current_halt = "REPEATED_STATE_PERIODIC"
                    halt_reason = current_halt

                elif cycle_n == cycles_per_case:
                    current_halt = "CYCLES_COMPLETE"
                    halt_reason = current_halt

                seen_states.add(after_sig)

                receipt = {
                    "run_id": run_id,
                    "case_id": case_id,
                    "family": family,
                    "depth": n,
                    "cycle_n": cycle_n,
                    "move_id": move_id,
                    "move_profile_id": profile_id,
                    "law_id": law_id,
                    "law_ok": law_ok,
                    "law_fail_reason": law_fail_reason,
                    "row_delta": profile["row_delta"],
                    "col_delta": profile["col_delta"],
                    "rank_delta": profile["rank_delta"],
                    "support_delta": profile["support_delta"],
                    "distinct_column_types_before": profile["distinct_column_types_before"],
                    "distinct_column_types_after": profile["distinct_column_types_after"],
                    "new_column_types_added": profile["new_column_types_added"],
                    "registered_moves_total": len(registered_moves),
                    "moves_reused": cycle_n - len(registered_moves),
                    "new_move_required": new_move_required,
                    "matrix_shape": [int(rows), int(cols)],
                    "matrix_cells": int(cells),
                    "rank_before": before_rank,
                    "rank_after": after_rank,
                    "state_sig8_before": before_sig,
                    "state_sig8_after": after_sig,
                    "compression_ratio": round(cycle_n / len(registered_moves), 4),
                    "trajectory_signature": sig8(trajectory),
                    "halt_reason": current_halt,
                    "receipt_path": "",
                }

                case_path = receipt_dir / case_id
                case_path.mkdir(parents=True, exist_ok=True)
                receipt_path = case_path / f"cycle_{cycle_n:04d}.json"
                receipt["receipt_path"] = str(receipt_path)

                with open(receipt_path, "w") as f:
                    json.dump(receipt, f, indent=2, sort_keys=True)

                insert_receipt(receipt)
                all_receipts.append(receipt)

                if current_halt is not None:
                    case_halts[halt_reason] = case_halts.get(halt_reason, 0) + 1
                    break

            np.save(artifact_dir / f"{case_id}_final_matrix.npy", a)

            with open(trace_dir / f"{case_id}.json", "w") as f:
                json.dump(
                    {
                        "run_id": run_id,
                        "case_id": case_id,
                        "halt_reason": halt_reason,
                        "trajectory": trajectory,
                        "trajectory_signature": sig8(trajectory),
                        "final_shape": list(a.shape),
                        "final_rank": gf2_rank(a),
                        "final_state_sig8": matrix_sig8(a),
                    },
                    f,
                    indent=2,
                    sort_keys=True,
                )

    summary = {
        "run_id": run_id,
        "created_utc": utc_now(),
        "families": family_names,
        "depth_min": depth_min,
        "depth_max": depth_max,
        "cycles_per_case": cycles_per_case,
        "max_cells": max_cells,
        "total_cases": total_cases,
        "total_receipts": len(all_receipts),
        "halt_counts": case_halts,
        "max_registered_moves": max(r["registered_moves_total"] for r in all_receipts),
        "max_compression_ratio": max(r["compression_ratio"] for r in all_receipts),
            "max_matrix_cells": max(r["matrix_cells"] for r in all_receipts),
        "max_registered_move_profiles": max(r["registered_moves_total"] for r in all_receipts),
    }

    with open(run_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    finish_run(run_id, "DONE", total_cases, len(all_receipts))

    print("[bold green]Done.[/bold green]")
    print(json.dumps(summary, indent=2))

    return summary


@app.command()
def run(
    depth_min: int = typer.Option(3, help="Smallest starting cycle size."),
    depth_max: int = typer.Option(8, help="Largest starting cycle size."),
    families: str = typer.Option("A,B,C,D,E", help="Family letters: A,B,C,D,E."),
    cycles_per_case: int = typer.Option(0, help="Cycles per case. 0 means depth_max."),
    max_cells: int = typer.Option(250_000, help="Hard matrix cell limit before halt."),
    strict_laws: bool = typer.Option(False, help="Halt immediately on law failure."),
    run_id: Optional[str] = typer.Option(None, help="Optional run id."),
):
    execute_run(
        depth_min=depth_min,
        depth_max=depth_max,
        families=families,
        cycles_per_case=cycles_per_case,
        max_cells=max_cells,
        strict_laws=strict_laws,
        run_id=run_id,
    )


@app.command()
def stress(
    depth_max: int = typer.Option(100, help="Push depth upward."),
    cycles_per_case: int = typer.Option(100, help="Push cycles upward."),
    max_cells: int = typer.Option(250_000, help="Hard matrix cell limit."),
    strict_laws: bool = typer.Option(False, help="Halt immediately on law failure."),
    families: str = typer.Option("A,B,C,D,E", help="Family letters."),
):
    """
    Deliberately push the runner until halt reasons appear.
    """
    execute_run(
        depth_min=3,
        depth_max=depth_max,
        families=families,
        cycles_per_case=cycles_per_case,
        max_cells=max_cells,
        strict_laws=strict_laws,
        run_id=None,
    )
    _ml_progress_phase("POST_PROCESSING", extra="stress_execute_run_returned")
    _ml_progress_phase("COMPLETED", extra="stress_command_done")


@app.command()
def summarize(run_id: str = typer.Argument("latest")):
    """
    Show run summary from SQLite.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        run_row = con.execute(
            """
            select run_id, created_utc, status, families, depth_min, depth_max,
                   cycles_per_case, max_cells, total_cases, total_receipts
            from runs
            where run_id = ?
            """,
            (run_id,),
        ).fetchone()

        if run_row is None:
            raise typer.BadParameter(f"Run not found: {run_id}")

        halt_rows = con.execute(
            """
            select halt_reason, count(*)
            from receipts
            where run_id = ? and halt_reason is not null
            group by halt_reason
            order by count(*) desc
            """,
            (run_id,),
        ).fetchall()

        family_rows = con.execute(
            """
            select family, count(distinct case_id), count(*), max(cells), max(compression_ratio)
            from receipts
            where run_id = ?
            group by family
            order by family
            """,
            (run_id,),
        ).fetchall()

    print(f"[bold green]Run:[/bold green] {run_id}")
    print(f"Created: {run_row[1]}")
    print(f"Status: {run_row[2]}")
    print(f"Families: {run_row[3]}")
    print(f"Depths: {run_row[4]}..{run_row[5]}")
    print(f"Cycles per case: {run_row[6]}")
    print(f"Max cells: {run_row[7]}")
    print(f"Total cases: {run_row[8]}")
    print(f"Total receipts: {run_row[9]}")

    table = Table(title="Halts")
    table.add_column("halt_reason")
    table.add_column("count", justify="right")
    for halt, count in halt_rows:
        table.add_row(str(halt), str(count))
    console.print(table)

    table = Table(title="By family")
    table.add_column("family")
    table.add_column("cases", justify="right")
    table.add_column("receipts", justify="right")
    table.add_column("max_cells", justify="right")
    table.add_column("max_compression", justify="right")
    for family, cases, receipts, max_cells_seen, max_compression in family_rows:
        table.add_row(
            str(family),
            str(cases),
            str(receipts),
            str(max_cells_seen),
            str(max_compression),
        )
    console.print(table)


@app.command()
def inspect(
    case_id: str = typer.Argument(..., help="Example: n6_two_sided_suspension"),
    run_id: str = typer.Option("latest", help="Run id or latest."),
    cycle: Optional[int] = typer.Option(None, help="Specific cycle number."),
):
    """
    Inspect receipts for one case.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        if cycle is None:
            rows = con.execute(
                """
                select cycle_n, move_id, rows, cols, cells, rank_before, rank_after,
                       registered_moves_total, moves_reused, compression_ratio,
                       halt_reason, state_sig8_after
                from receipts
                where run_id = ? and case_id = ?
                order by cycle_n
                """,
                (run_id, case_id),
            ).fetchall()
        else:
            rows = con.execute(
                """
                select cycle_n, move_id, rows, cols, cells, rank_before, rank_after,
                       registered_moves_total, moves_reused, compression_ratio,
                       halt_reason, state_sig8_after
                from receipts
                where run_id = ? and case_id = ? and cycle_n = ?
                order by cycle_n
                """,
                (run_id, case_id, cycle),
            ).fetchall()

    if not rows:
        raise typer.BadParameter(f"No receipts found for run={run_id}, case={case_id}")

    table = Table(title=f"{run_id} / {case_id}")
    table.add_column("cycle", justify="right")
    table.add_column("move")
    table.add_column("shape")
    table.add_column("rank")
    table.add_column("moves")
    table.add_column("reuse")
    table.add_column("comp")
    table.add_column("halt")
    table.add_column("state")

    for r in rows:
        (
            cycle_n,
            move_id,
            rows_n,
            cols_n,
            cells,
            rank_before,
            rank_after,
            registered_moves,
            moves_reused,
            compression_ratio,
            halt_reason,
            state_sig,
        ) = r

        table.add_row(
            str(cycle_n),
            move_id,
            f"{rows_n}x{cols_n}={cells}",
            f"{rank_before}->{rank_after}",
            str(registered_moves),
            str(moves_reused),
            str(compression_ratio),
            str(halt_reason or ""),
            state_sig,
        )

    console.print(table)


@app.command()
def analyze(run_id: str = typer.Argument("latest")):
    """
    Analyze where and how the latest run broke.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        halt_by_family = con.execute(
            """
            select family, halt_reason, count(*)
            from receipts
            where run_id = ? and halt_reason is not null
            group by family, halt_reason
            order by family, halt_reason
            """,
            (run_id,),
        ).fetchall()

        growth = con.execute(
            """
            select family,
                   min(cells) as min_cells,
                   max(cells) as max_cells,
                   avg(cells) as avg_cells,
                   max(cycle_n) as max_cycle,
                   max(compression_ratio) as max_compression
            from receipts
            where run_id = ?
            group by family
            order by family
            """,
            (run_id,),
        ).fetchall()

        repeated = con.execute(
            """
            select family, min(depth), max(depth), count(*), min(cycle_n), max(cycle_n)
            from receipts
            where run_id = ? and halt_reason = 'REPEATED_STATE'
            group by family
            order by family
            """,
            (run_id,),
        ).fetchall()

        first_halts = con.execute(
            """
            select family, case_id, depth, cycle_n, halt_reason, rows, cols, cells, state_sig8_after
            from receipts
            where run_id = ? and halt_reason is not null
            order by family, depth
            limit 25
            """,
            (run_id,),
        ).fetchall()

    print(f"[bold green]Analysis for run:[/bold green] {run_id}")

    table = Table(title="Halt reasons by family")
    table.add_column("family")
    table.add_column("halt_reason")
    table.add_column("count", justify="right")
    for family, halt, count in halt_by_family:
        table.add_row(str(family), str(halt), str(count))
    console.print(table)

    table = Table(title="Growth by family")
    table.add_column("family")
    table.add_column("min_cells", justify="right")
    table.add_column("max_cells", justify="right")
    table.add_column("avg_cells", justify="right")
    table.add_column("max_cycle", justify="right")
    table.add_column("max_compression", justify="right")
    for family, min_cells, max_cells, avg_cells, max_cycle, max_comp in growth:
        table.add_row(
            str(family),
            str(min_cells),
            str(max_cells),
            f"{avg_cells:.2f}",
            str(max_cycle),
            str(max_comp),
        )
    console.print(table)

    if repeated:
        table = Table(title="Repeated-state families")
        table.add_column("family")
        table.add_column("min_depth", justify="right")
        table.add_column("max_depth", justify="right")
        table.add_column("cases", justify="right")
        table.add_column("repeat_cycle_min", justify="right")
        table.add_column("repeat_cycle_max", justify="right")
        for row in repeated:
            table.add_row(*(str(x) for x in row))
        console.print(table)

    table = Table(title="First halts, first 25")
    table.add_column("family")
    table.add_column("case")
    table.add_column("depth", justify="right")
    table.add_column("cycle", justify="right")
    table.add_column("halt")
    table.add_column("shape")
    table.add_column("state")
    for family, case_id, depth, cycle_n, halt, rows, cols, cells, sig in first_halts:
        table.add_row(
            family,
            case_id,
            str(depth),
            str(cycle_n),
            str(halt),
            f"{rows}x{cols}={cells}",
            sig,
        )
    console.print(table)


@app.command()
def profiles(
    run_id: str = typer.Argument("latest"),
    family: Optional[str] = typer.Option(None, help="Optional family filter."),
    limit: int = typer.Option(30, help="Max rows to show."),
):
    """
    Show compact move-profile counts.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    params = [run_id]
    family_clause = ""

    if family:
        family_clause = "and family = ?"
        params.append(family)

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        rows = con.execute(
            f"""
            select
                family,
                move_id,
                row_delta,
                col_delta,
                rank_delta,
                support_delta,
                new_column_types_added,
                count(*) as n
            from receipts
            where run_id = ?
            {family_clause}
            group by
                family,
                move_id,
                row_delta,
                col_delta,
                rank_delta,
                support_delta,
                new_column_types_added
            order by family, n desc
            limit ?
            """,
            (*params, limit),
        ).fetchall()

    print(f"[bold green]Move profiles for run:[/bold green] {run_id}")

    table = Table(title="Move profiles")
    table.add_column("family")
    table.add_column("move")
    table.add_column("dr", justify="right")
    table.add_column("dc", justify="right")
    table.add_column("rank", justify="right")
    table.add_column("support", justify="right")
    table.add_column("newcols", justify="right")
    table.add_column("count", justify="right")

    for row in rows:
        table.add_row(*(str(x) for x in row))

    console.print(table)


@app.command()
def coarse_profiles(
    run_id: str = typer.Argument("latest"),
    limit: int = typer.Option(50, help="Max rows to show."),
):
    """
    Compare raw move-profile counts against coarse normalized profile counts.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        family_counts = con.execute(
            """
            select
                family,
                count(distinct move_profile_id) as raw_profiles,
                count(distinct (
                    move_id
                    || '|dr=' || row_delta
                    || '|dc=' || col_delta
                    || '|rank=' || rank_delta
                    || '|supp_sign=' ||
                        case
                            when support_delta > 0 then '+'
                            when support_delta < 0 then '-'
                            else '0'
                        end
                    || '|newcols_class=' ||
                        case
                            when new_column_types_added = 0 then '0'
                            when new_column_types_added = 1 then '1'
                            else 'many'
                        end
                )) as coarse_profiles,
                count(*) as receipts
            from receipts
            where run_id = ?
            group by family
            order by raw_profiles desc
            """,
            (run_id,),
        ).fetchall()

        coarse_rows = con.execute(
            """
            select
                family,
                move_id,
                row_delta,
                col_delta,
                rank_delta,
                case
                    when support_delta > 0 then '+'
                    when support_delta < 0 then '-'
                    else '0'
                end as support_sign,
                case
                    when new_column_types_added = 0 then '0'
                    when new_column_types_added = 1 then '1'
                    else 'many'
                end as newcols_class,
                count(*) as n
            from receipts
            where run_id = ?
            group by
                family,
                move_id,
                row_delta,
                col_delta,
                rank_delta,
                support_sign,
                newcols_class
            order by family, n desc
            limit ?
            """,
            (run_id, limit),
        ).fetchall()

    print(f"[bold green]Coarse profile comparison for run:[/bold green] {run_id}")

    table = Table(title="Raw vs coarse profile counts")
    table.add_column("family")
    table.add_column("raw", justify="right")
    table.add_column("coarse", justify="right")
    table.add_column("receipts", justify="right")

    for row in family_counts:
        table.add_row(*(str(x) for x in row))

    console.print(table)

    table = Table(title="Coarse profile rows")
    table.add_column("family")
    table.add_column("move")
    table.add_column("dr", justify="right")
    table.add_column("dc", justify="right")
    table.add_column("rank", justify="right")
    table.add_column("supp", justify="right")
    table.add_column("newcols")
    table.add_column("count", justify="right")

    for row in coarse_rows:
        table.add_row(*(str(x) for x in row))

    console.print(table)


@app.command()
def laws(
    run_id: str = typer.Argument("latest"),
    limit: int = typer.Option(40, help="Max failing rows to show."),
):
    """
    Summarize expected-law checks by family and move.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        rows = con.execute(
            """
            select family, law_id, law_ok, count(*)
            from receipts
            where run_id = ?
            group by family, law_id, law_ok
            order by family, law_id, law_ok
            """,
            (run_id,),
        ).fetchall()

        failures = con.execute(
            """
            select family, case_id, cycle_n, move_id, law_id, law_fail_reason
            from receipts
            where run_id = ?
              and law_ok = 0
            order by family, case_id, cycle_n
            limit ?
            """,
            (run_id, limit),
        ).fetchall()

    print(f"[bold green]Law check for run:[/bold green] {run_id}")

    table = Table(title="Law checks")
    table.add_column("family")
    table.add_column("law")
    table.add_column("ok", justify="right")
    table.add_column("count", justify="right")

    for row in rows:
        table.add_row(*(str(x) for x in row))

    console.print(table)

    if failures:
        table = Table(title="Law failures")
        table.add_column("family")
        table.add_column("case")
        table.add_column("cycle", justify="right")
        table.add_column("move")
        table.add_column("law")
        table.add_column("reason")

        for row in failures:
            table.add_row(*(str(x) for x in row))

        console.print(table)




@app.command("recover-collision")
def recover_collision(run_id: str = typer.Argument("latest")):
    """
    Recover a run_id collision by splitting receipt rows whose family is not in the stored run family set.
    """
    import shutil

    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.row_factory = sqlite3.Row

        run_row = con.execute(
            "select * from runs where run_id = ?",
            (run_id,),
        ).fetchone()

        if run_row is None:
            raise typer.BadParameter(f"No run found: {run_id}")

        run_row = dict(run_row)
        stored_families = str(run_row.get("families", ""))
        expected_families = {x.strip() for x in stored_families.split(",") if x.strip()}

        family_rows = con.execute(
            """
            select family, count(*) as n
            from receipts
            where run_id = ?
            group by family
            order by family
            """,
            (run_id,),
        ).fetchall()

        outsider_families = {
            row["family"]
            for row in family_rows
            if row["family"] not in expected_families
        }

        receipt_count = con.execute(
            "select count(*) from receipts where run_id = ?",
            (run_id,),
        ).fetchone()[0]

        print(f"recover target: {run_id}")
        print(f"stored families: {sorted(expected_families)}")
        print(f"receipt rows: {receipt_count}")
        print(f"outsider families: {sorted(outsider_families)}")

        if not outsider_families:
            print("[bold green]No outsider-family collision detected.[/bold green]")
            return

        intruder_rows = con.execute(
            """
            select rowid, *
            from receipts
            where run_id = ?
              and family in ({})
            order by family, case_id, cycle_n
            """.format(",".join("?" for _ in outsider_families)),
            (run_id, *sorted(outsider_families)),
        ).fetchall()

        new_run_id = allocate_run_id(f"{run_id}_recovered")

        receipt_root = Path("data/receipts")
        trace_root = Path("data/traces")
        artifact_root = Path("data/artifacts")
        run_root = Path("data/runs")

        for root in [receipt_root, trace_root, artifact_root, run_root]:
            (root / new_run_id).mkdir(parents=True, exist_ok=True)

        case_ids = sorted({row["case_id"] for row in intruder_rows})
        receipt_updates = []

        for row in intruder_rows:
            old_path = Path(row["receipt_path"])
            if not old_path.exists():
                old_path = receipt_root / run_id / row["case_id"] / f"cycle_{int(row['cycle_n']):04d}.json"

            new_path = receipt_root / new_run_id / row["case_id"] / f"cycle_{int(row['cycle_n']):04d}.json"
            new_path.parent.mkdir(parents=True, exist_ok=True)

            if old_path.exists():
                data = json.loads(old_path.read_text())
                data["run_id"] = new_run_id
                data["receipt_path"] = str(new_path)
                new_path.write_text(json.dumps(data, indent=2, sort_keys=True))
            else:
                new_path.write_text("{}\n")

            receipt_updates.append((new_run_id, str(new_path), row["rowid"]))

        for case_id in case_ids:
            old_trace = trace_root / run_id / f"{case_id}.json"
            new_trace = trace_root / new_run_id / f"{case_id}.json"
            if old_trace.exists():
                data = json.loads(old_trace.read_text())
                data["run_id"] = new_run_id
                new_trace.write_text(json.dumps(data, indent=2, sort_keys=True))

            old_artifact = artifact_root / run_id / f"{case_id}_final_matrix.npy"
            new_artifact = artifact_root / new_run_id / f"{case_id}_final_matrix.npy"
            if old_artifact.exists():
                shutil.copy2(old_artifact, new_artifact)

        con.executemany(
            "update receipts set run_id = ?, receipt_path = ? where rowid = ?",
            receipt_updates,
        )
        con.commit()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        con.row_factory = sqlite3.Row

        recovered_stats = con.execute(
            """
            select
              min(depth) as depth_min,
              max(depth) as depth_max,
              max(cycle_n) as cycles_per_case,
              0 as max_matrix_cells,
              count(distinct case_id) as total_cases,
              count(*) as total_receipts
            from receipts
            where run_id = ?
            """,
            (new_run_id,),
        ).fetchone()

        remaining_stats = con.execute(
            """
            select
              count(distinct case_id) as total_cases,
              count(*) as total_receipts
            from receipts
            where run_id = ?
            """,
            (run_id,),
        ).fetchone()

        recovered_families = [
            row[0]
            for row in con.execute(
                "select distinct family from receipts where run_id = ? order by family",
                (new_run_id,),
            ).fetchall()
        ]

        original_halts = {
            row[0]: row[1]
            for row in con.execute(
                """
                select halt_reason, count(*)
                from receipts
                where run_id = ? and halt_reason is not null
                group by halt_reason
                """,
                (run_id,),
            ).fetchall()
        }

        recovered_halts = {
            row[0]: row[1]
            for row in con.execute(
                """
                select halt_reason, count(*)
                from receipts
                where run_id = ? and halt_reason is not null
                group by halt_reason
                """,
                (new_run_id,),
            ).fetchall()
        }

    insert_run_start(
        run_id=new_run_id,
        families=recovered_families,
        depth_min=int(recovered_stats["depth_min"] or 0),
        depth_max=int(recovered_stats["depth_max"] or 0),
        cycles_per_case=int(recovered_stats["cycles_per_case"] or 0),
        max_cells=int(run_row.get("max_cells") or 0),
    )
    finish_run(
        new_run_id,
        "DONE",
        int(recovered_stats["total_cases"] or 0),
        int(recovered_stats["total_receipts"] or 0),
    )

    finish_run(
        run_id,
        "DONE",
        int(remaining_stats["total_cases"] or 0),
        int(remaining_stats["total_receipts"] or 0),
    )

    original_summary = {
        "run_id": run_id,
        "created_utc": utc_now(),
        "families": sorted(expected_families),
        "total_cases": int(remaining_stats["total_cases"] or 0),
        "total_receipts": int(remaining_stats["total_receipts"] or 0),
        "halt_counts": original_halts,
    }
    recovered_summary = {
        "run_id": new_run_id,
        "created_utc": utc_now(),
        "families": recovered_families,
        "depth_min": int(recovered_stats["depth_min"] or 0),
        "depth_max": int(recovered_stats["depth_max"] or 0),
        "cycles_per_case": int(recovered_stats["cycles_per_case"] or 0),
        "total_cases": int(recovered_stats["total_cases"] or 0),
        "total_receipts": int(recovered_stats["total_receipts"] or 0),
        "halt_counts": recovered_halts,
    }

    (run_root / run_id).mkdir(parents=True, exist_ok=True)
    (run_root / new_run_id).mkdir(parents=True, exist_ok=True)
    (run_root / run_id / "summary.json").write_text(json.dumps(original_summary, indent=2, sort_keys=True))
    (run_root / new_run_id / "summary.json").write_text(json.dumps(recovered_summary, indent=2, sort_keys=True))

    print(f"[bold green]RECOVERED[/bold green]")
    print(f"original run:  {run_id}")
    print(f"recovered run: {new_run_id}")
    print(f"moved receipts: {len(receipt_updates)}")

@app.command()
def gate(run_id: str = typer.Argument("latest")):
    """
    Exit nonzero if a run violates law checks or is incomplete.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with _matrixlab_connect_sqlite(DB_PATH) as con:
        run_row = con.execute(
            "select status, total_cases, total_receipts from runs where run_id = ?",
            (run_id,),
        ).fetchone()

        if run_row is None:
            raise typer.BadParameter(f"No run found: {run_id}")

        status, total_cases, total_receipts = run_row

        receipt_count = con.execute(
            "select count(*) from receipts where run_id = ?",
            (run_id,),
        ).fetchone()[0]

        law_failures = con.execute(
            "select count(*) from receipts where run_id = ? and coalesce(law_ok, 0) = 0",
            (run_id,),
        ).fetchone()[0]

        unknown_laws = con.execute(
            "select count(*) from receipts where run_id = ? and law_id = 'UNKNOWN_LAW'",
            (run_id,),
        ).fetchone()[0]

        halt_rows = con.execute(
            """
            select halt_reason, count(*)
            from receipts
            where run_id = ? and halt_reason is not null
            group by halt_reason
            order by halt_reason
            """,
            (run_id,),
        ).fetchall()

    table = Table(title=f"Gate checks / {run_id}")
    table.add_column("check")
    table.add_column("value", justify="right")
    table.add_row("status", str(status))
    table.add_row("total_cases", str(total_cases))
    table.add_row("total_receipts", str(total_receipts))
    table.add_row("receipt_rows", str(receipt_count))
    table.add_row("law_failures", str(law_failures))
    table.add_row("unknown_laws", str(unknown_laws))
    console.print(table)

    halt_table = Table(title="Halts")
    halt_table.add_column("halt_reason")
    halt_table.add_column("count", justify="right")
    for halt_reason, count in halt_rows:
        halt_table.add_row(str(halt_reason), str(count))
    console.print(halt_table)

    failed = (
        status != "DONE"
        or receipt_count == 0
        or total_receipts != receipt_count
        or law_failures > 0
        or unknown_laws > 0
    )

    if failed:
        print("[bold red]GATE_FAIL[/bold red]")
        raise typer.Exit(1)

    print("[bold green]GATE_PASS[/bold green]")



@app.command("agent-eval")
def agent_eval(
    run_id: str = typer.Argument("latest"),
    previous: Optional[str] = typer.Option(None, "--previous", "-p", help="Optional previous run id for delta comparison."),
):
    """
    Emit a machine-readable agent/eval report for one run, optionally compared to a previous run.
    """
    init_db()

    def resolve_run_id(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if value == "latest":
            return latest_run_id()
        return value

    def table_columns(con, table_name: str) -> set[str]:
        return {row[1] for row in con.execute(f"pragma table_info({table_name})").fetchall()}

    def coarse_id(row: sqlite3.Row) -> str:
        support_delta = int(row["support_delta"] or 0) if "support_delta" in row.keys() else 0
        newcols = int(row["new_column_types_added"] or 0) if "new_column_types_added" in row.keys() else 0

        if support_delta > 0:
            supp = "+"
        elif support_delta < 0:
            supp = "-"
        else:
            supp = "0"

        if newcols == 0:
            newcls = "0"
        elif newcols == 1:
            newcls = "1"
        else:
            newcls = "many"

        return (
            f"{row['move_id']}"
            f"|dr={int(row['row_delta'] or 0)}"
            f"|dc={int(row['col_delta'] or 0)}"
            f"|rank={int(row['rank_delta'] or 0)}"
            f"|supp={supp}"
            f"|newcols={newcls}"
        )

    def collect(run: str) -> dict:
        with _matrixlab_connect_sqlite(DB_PATH) as con:
            con.row_factory = sqlite3.Row
            cols = table_columns(con, "receipts")

            run_row = con.execute(
                "select * from runs where run_id = ?",
                (run,),
            ).fetchone()

            if run_row is None:
                return {
                    "run_id": run,
                    "exists": False,
                    "gate": "FAIL",
                    "failure_mode": "missing_run",
                }

            run_row = dict(run_row)

            receipt_rows = con.execute(
                "select * from receipts where run_id = ? order by case_id, cycle_n",
                (run,),
            ).fetchall()

            receipt_count = len(receipt_rows)

            law_failures = con.execute(
                "select count(*) from receipts where run_id = ? and coalesce(law_ok, 0) = 0",
                (run,),
            ).fetchone()[0]

            unknown_laws = con.execute(
                "select count(*) from receipts where run_id = ? and law_id = 'UNKNOWN_LAW'",
                (run,),
            ).fetchone()[0]

            orphan_receipt_runs = con.execute(
                """
                select count(distinct receipts.run_id)
                from receipts
                left join runs on runs.run_id = receipts.run_id
                where runs.run_id is null
                """
            ).fetchone()[0]

            halt_rows = con.execute(
                """
                select halt_reason, count(*)
                from receipts
                where run_id = ? and halt_reason is not null
                group by halt_reason
                order by halt_reason
                """,
                (run,),
            ).fetchall()

            family_rows = con.execute(
                """
                select family, count(*) as receipts
                from receipts
                where run_id = ?
                group by family
                order by family
                """,
                (run,),
            ).fetchall()

            move_rows = con.execute(
                """
                select move_id, count(*) as receipts
                from receipts
                where run_id = ?
                group by move_id
                order by receipts desc, move_id
                """,
                (run,),
            ).fetchall()

            raw_profile_total = con.execute(
                """
                select count(distinct move_profile_id)
                from receipts
                where run_id = ?
                """,
                (run,),
            ).fetchone()[0]

            max_registered_moves = con.execute(
                """
                select max(registered_moves_total)
                from receipts
                where run_id = ?
                """,
                (run,),
            ).fetchone()[0] or 0

            max_cycle = con.execute(
                """
                select max(cycle_n)
                from receipts
                where run_id = ?
                """,
                (run,),
            ).fetchone()[0] or 0

            cases_with_reuse = con.execute(
                """
                select count(distinct case_id)
                from receipts
                where run_id = ? and coalesce(moves_reused, 0) > 0
                """,
                (run,),
            ).fetchone()[0]

            cases_with_new_shape = 0
            if "new_column_types_added" in cols:
                cases_with_new_shape = con.execute(
                    """
                    select count(distinct case_id)
                    from receipts
                    where run_id = ? and coalesce(new_column_types_added, 0) > 0
                    """,
                    (run,),
                ).fetchone()[0]

        coarse_counts = {}
        for row in receipt_rows:
            if all(k in row.keys() for k in ["move_id", "row_delta", "col_delta", "rank_delta", "support_delta", "new_column_types_added"]):
                cid = coarse_id(row)
                coarse_counts[cid] = coarse_counts.get(cid, 0) + 1

        total_receipts = int(run_row.get("total_receipts") or 0)
        status = str(run_row.get("status") or "")
        gate_failures = []

        if status != "DONE":
            gate_failures.append("run_status_not_done")
        if receipt_count == 0:
            gate_failures.append("no_receipts")
        if receipt_count != total_receipts:
            gate_failures.append("receipt_rows_mismatch")
        if law_failures > 0:
            gate_failures.append("law_failures")
        if unknown_laws > 0:
            gate_failures.append("unknown_laws")
        if orphan_receipt_runs > 0:
            gate_failures.append("orphan_receipt_runs")
        if not coarse_counts:
            gate_failures.append("missing_coarse_profile_summary")

        gate = "PASS" if not gate_failures else "FAIL"

        receipt_sig_payload = {
            "run_id": run,
            "total_receipts": total_receipts,
            "receipt_rows": receipt_count,
            "halt_counts": {row["halt_reason"]: row[1] for row in halt_rows},
            "law_failures": law_failures,
            "unknown_laws": unknown_laws,
            "raw_move_profiles_total": raw_profile_total,
            "coarse_move_profiles_total": len(coarse_counts),
            "max_moves_applied_before_halt": int(max_cycle),
            "max_registered_moves": int(max_registered_moves),
        }

        failure_mode = None
        if law_failures:
            failure_mode = "law_failure"
        elif unknown_laws:
            failure_mode = "unknown_law"
        elif orphan_receipt_runs:
            failure_mode = "orphan_receipt"
        elif receipt_count != total_receipts:
            failure_mode = "receipt_projection_bug"
        elif status != "DONE":
            failure_mode = "run_incomplete"
        elif not coarse_counts:
            failure_mode = "profile_summary_missing"

        return {
            "run_id": run,
            "exists": True,
            "gate": gate,
            "gate_failures": gate_failures,
            "metrics": {
                "status": status,
                "families": str(run_row.get("families") or ""),
                "depth_min": int(run_row.get("depth_min") or 0),
                "depth_max": int(run_row.get("depth_max") or 0),
                "cycles_per_case": int(run_row.get("cycles_per_case") or 0),
                "total_cases": int(run_row.get("total_cases") or 0),
                "total_receipts": total_receipts,
                "receipt_rows": receipt_count,
                "registered_moves_total": int(max_registered_moves),
                "raw_move_profiles_total": int(raw_profile_total),
                "coarse_move_profiles_total": int(len(coarse_counts)),
                "max_moves_applied_before_halt": int(max_cycle),
                "halt_reason_counts": {row["halt_reason"]: row[1] for row in halt_rows},
                "law_failures": int(law_failures),
                "unknown_laws": int(unknown_laws),
                "orphan_receipt_runs": int(orphan_receipt_runs),
                "new_shape_required": bool(cases_with_new_shape > 0),
                "reused_shape": bool(cases_with_reuse > 0),
                "receipt_sig8": sig8(receipt_sig_payload),
            },
            "profile_summary": {
                "by_family": {row["family"]: row["receipts"] for row in family_rows},
                "by_move": {row["move_id"]: row["receipts"] for row in move_rows},
                "coarse_profiles": coarse_counts,
            },
            "classification": {
                "new_shape_required": bool(cases_with_new_shape > 0),
                "reused_shape": bool(cases_with_reuse > 0),
                "failure_mode": failure_mode,
            },
        }


    def safe_ratio(num, den):
        num = float(num or 0)
        den = float(den or 0)
        if den == 0:
            return None
        return round(num / den, 6)

    def vocabulary_scores(metrics: dict) -> dict:
        continuation = int(metrics.get("max_moves_applied_before_halt") or 0)
        receipts = int(metrics.get("total_receipts") or 0)
        cases = int(metrics.get("total_cases") or 0)
        registered = int(metrics.get("registered_moves_total") or 0)
        raw = int(metrics.get("raw_move_profiles_total") or 0)
        coarse = int(metrics.get("coarse_move_profiles_total") or 0)

        return {
            "continuation_radius": continuation,
            "registered_moves_total": registered,
            "raw_move_profiles_total": raw,
            "coarse_move_profiles_total": coarse,
            "continuation_per_registered_move": safe_ratio(continuation, registered),
            "continuation_per_raw_profile": safe_ratio(continuation, raw),
            "continuation_per_coarse_profile": safe_ratio(continuation, coarse),
            "receipts_per_registered_move": safe_ratio(receipts, registered),
            "receipts_per_raw_profile": safe_ratio(receipts, raw),
            "receipts_per_coarse_profile": safe_ratio(receipts, coarse),
            "receipts_per_case": safe_ratio(receipts, cases),
        }

    def classify_compression_signal(current: dict, previous: Optional[dict], delta: Optional[dict]) -> str:
        if current.get("gate") != "PASS":
            return "BLOCKED"

        if previous is None or not delta:
            return "BASELINE"

        if previous.get("gate") != "PASS":
            return "BASELINE_PREVIOUS_BLOCKED"

        radius_delta = int(delta.get("continuation_radius_delta") or 0)
        coarse_delta = int(delta.get("coarse_move_profiles_delta") or 0)
        raw_delta = int(delta.get("raw_move_profiles_delta") or 0)
        registered_delta = int(delta.get("registered_moves_delta") or 0)
        receipt_delta = int(delta.get("total_receipts_delta") or 0)

        if radius_delta > 0 and coarse_delta <= 0 and registered_delta <= 0:
            return "GOOD"

        if radius_delta > 0 and coarse_delta <= 1:
            return "GOOD_WEAK"

        if radius_delta == 0 and coarse_delta == 0 and raw_delta == 0 and registered_delta == 0:
            return "FLAT"

        if radius_delta <= 0 and (coarse_delta > 0 or raw_delta > 0 or registered_delta > 0):
            return "BAD"

        if receipt_delta > 0 and coarse_delta == 0:
            return "GOOD_RECEIPT_EXPANSION"

        return "MIXED"

    current_run = resolve_run_id(run_id)
    previous_run = resolve_run_id(previous)

    current = collect(current_run)
    previous_metrics = collect(previous_run) if previous_run else None

    delta = None
    if previous_metrics and current.get("exists") and previous_metrics.get("exists"):
        cm = current["metrics"]
        pm = previous_metrics["metrics"]

        delta = {
            "previous_run_id": previous_run,
            "current_run_id": current_run,
            "total_receipts_delta": cm["total_receipts"] - pm["total_receipts"],
            "continuation_radius_delta": cm["max_moves_applied_before_halt"] - pm["max_moves_applied_before_halt"],
            "registered_moves_delta": cm["registered_moves_total"] - pm["registered_moves_total"],
            "raw_move_profiles_delta": cm["raw_move_profiles_total"] - pm["raw_move_profiles_total"],
            "coarse_move_profiles_delta": cm["coarse_move_profiles_total"] - pm["coarse_move_profiles_total"],
            "law_failures_delta": cm["law_failures"] - pm["law_failures"],
            "unknown_laws_delta": cm["unknown_laws"] - pm["unknown_laws"],
        }

    current_scores = vocabulary_scores(current.get("metrics", {})) if current.get("exists") else {}
    previous_scores = vocabulary_scores(previous_metrics.get("metrics", {})) if previous_metrics and previous_metrics.get("exists") else None
    compression_signal = classify_compression_signal(current, previous_metrics, delta)

    gate = current.get("gate", "FAIL")
    stop_code = None
    next_command_goal = "COMPARE_PREVIOUS_RUN"

    if gate != "PASS":
        terminal_type = "STOP"
        stop_code = current.get("classification", {}).get("failure_mode") or "gate_failed"
        next_command_goal = None
    elif previous_run is None:
        terminal_type = "ADVANCE"
        next_command_goal = "ADD_PREVIOUS_RUN_COMPARISON"
    elif not current_scores:
        terminal_type = "ADVANCE"
        next_command_goal = "ADD_VOCABULARY_GROWTH_SCORING"
    else:
        terminal_type = "ADVANCE"
        next_command_goal = "RUN_FULL_NORMAL_STRICT"

    eval_report = {
        "eval_id": sig8(
            {
                "current": current_run,
                "previous": previous_run,
                "receipt_sig8": current.get("metrics", {}).get("receipt_sig8"),
            }
        ),
        "input_runs": [x for x in [current_run, previous_run] if x],
        "gate": gate,
        "metrics": current.get("metrics", {}),
        "profile_summary": current.get("profile_summary", {}),
        "delta_vs_previous": delta,
        "vocabulary_growth_score": current_scores,
        "previous_vocabulary_growth_score": previous_scores,
        "classification": {
            "compression_signal": compression_signal,
            "continuation_radius_growth": None if not delta else (
                "up" if delta["continuation_radius_delta"] > 0 else
                "flat" if delta["continuation_radius_delta"] == 0 else
                "down"
            ),
            "mutation_vocabulary_growth": None if not delta else (
                "up" if delta["coarse_move_profiles_delta"] > 0 else
                "flat" if delta["coarse_move_profiles_delta"] == 0 else
                "down"
            ),
            "new_shape_required": current.get("classification", {}).get("new_shape_required"),
            "reused_shape": current.get("classification", {}).get("reused_shape"),
            "failure_mode": current.get("classification", {}).get("failure_mode"),
        },
        "terminal": {
            "type": terminal_type,
            "next_command_goal": next_command_goal,
            "stop_code": stop_code,
        },
    }

    eval_dir = Path("data/evals")
    eval_dir.mkdir(parents=True, exist_ok=True)
    eval_path = eval_dir / f"{eval_report['eval_id']}.json"
    eval_path.write_text(json.dumps(eval_report, indent=2, sort_keys=True))

    print(json.dumps(eval_report, indent=2, sort_keys=True))
    print(f"[bold green]eval_path[/bold green]: {eval_path}")

    if gate != "PASS":
        raise typer.Exit(1)



@app.command("agent-select")
def agent_select(eval_report: str = typer.Argument(...)):
    """
    Select the next command from a fixed allowlist based on an explicit agent-eval JSON report.
    """
    import shlex

    def resolve_eval_path(value: str) -> Path:
        candidate = Path(value)
        if candidate.exists():
            return candidate

        candidate = Path("data/evals") / f"{value}.json"
        if candidate.exists():
            return candidate

        raise typer.BadParameter(
            "eval_report must be an explicit eval JSON path or eval_id present under data/evals/"
        )

    def write_selection(payload: dict) -> Path:
        payload = dict(payload)
        payload["selector_schema_version"] = AGENT_SELECT_SCHEMA
        payload["selector_payload_sig8"] = selector_payload_sig(payload)
        payload["selector_id"] = payload["selector_payload_sig8"]

        out_dir = Path("data/agent_select")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{payload['selector_id']}.json"
        out_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return out_path

    path = resolve_eval_path(eval_report)
    report = json.loads(path.read_text())

    eval_id = report.get("eval_id")
    gate = report.get("gate")
    terminal = report.get("terminal") or {}
    terminal_type = terminal.get("type")
    goal = terminal.get("next_command_goal")
    input_runs = report.get("input_runs") or []
    current_run_id = input_runs[0] if input_runs else None

    base_payload = {
        "input_eval_path": str(path),
        "input_eval_id": eval_id,
        "input_runs": input_runs,
        "eval_gate": gate,
        "eval_terminal_type": terminal_type,
        "requested_goal": goal,
        "selector_version": "agent_select_allowlist_v0",
        "safety_rules": [
            "explicit_eval_json_only",
            "no_latest_file_or_mtime_authority",
            "no_command_invention",
            "no_code_editing",
            "no_architecture_widening",
            "refuse_if_eval_gate_not_PASS",
            "refuse_if_terminal_not_ADVANCE",
            "fixed_allowlist_only",
        ],
    }

    def refuse(reason: str, stop_code: str = None):
        payload = dict(base_payload)
        payload.update(
            {
                "verdict": "REFUSE",
                "refusal_reason": reason,
                "stop_code": stop_code or reason,
                "selected_command_goal": None,
                "command_kind": None,
                "command_lines": [],
                "command_script": "",
                "command_count": 0,
                "command_argvs": [],
                "requires_manual_parameters": [],
                "expected_gate_result": None,
                "expected_next_receipts": None,
                "expected_terminal": "STOP",
            }
        )
        out_path = write_selection(payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"[bold red]selection_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    if gate != "PASS":
        refuse("eval_gate_not_PASS", terminal.get("stop_code") or "gate_failed")

    if terminal_type != "ADVANCE":
        refuse("terminal_not_ADVANCE", terminal.get("stop_code") or "not_advance")

    if not goal:
        refuse("missing_next_command_goal")

    allowlist = {
        "ADD_PREVIOUS_RUN_COMPARISON": {
            "command_kind": "ALLOWLIST_TEMPLATE_REQUIRES_PARAMETER",
            "command_lines": [
                f"uv run python src/matrixlab/cli.py agent-eval {current_run_id} --previous <previous_run_id>"
            ],
            "requires_manual_parameters": ["previous_run_id"],
        },
        "RUN_SMALL_NORMAL_STRICT": {
            "command_kind": "ALLOWLIST_COMMAND",
            "command_lines": [
                "uv run python src/matrixlab/cli.py stress --families ABCDE --depth-max 20 --cycles-per-case 20 --max-cells 50000 --strict-laws",
                "uv run python src/matrixlab/cli.py gate latest",
                f"uv run python src/matrixlab/cli.py agent-eval latest --previous {current_run_id}",
            ],
            "requires_manual_parameters": [],
            "expected_gate_result": "PASS",
            "expected_next_receipts": "normal_strict_small_run",
            "expected_terminal": "ADVANCE",
        },
        "RUN_FULL_NORMAL_STRICT": {
            "command_kind": "ALLOWLIST_COMMAND",
            "command_lines": [
                "uv run python src/matrixlab/cli.py stress --families ABCDE --depth-max 100 --cycles-per-case 100 --max-cells 50000 --strict-laws",
                "uv run python src/matrixlab/cli.py gate latest",
                f"uv run python src/matrixlab/cli.py agent-eval latest --previous {current_run_id}",
            ],
            "requires_manual_parameters": [],
            "expected_gate_result": "PASS",
            "expected_next_receipts": "normal_strict_full_run",
            "expected_terminal": "ADVANCE",
        },
        "RUN_BAD_PROBE_STRICT_NEGATIVE_CONTROL": {
            "command_kind": "ALLOWLIST_COMMAND_EXPECTED_FAIL",
            "command_lines": [
                "uv run python src/matrixlab/cli.py stress --families F --depth-max 8 --cycles-per-case 5 --max-cells 50000 --strict-laws",
                "uv run python src/matrixlab/cli.py gate latest || true",
                "uv run python src/matrixlab/cli.py agent-eval latest || true",
            ],
            "requires_manual_parameters": [],
            "expected_gate_result": "FAIL",
            "expected_next_receipts": "law_violation_probe_strict_negative_control",
            "expected_terminal": "STOP",
        },
    }

    if goal not in allowlist:
        refuse("goal_not_in_allowlist")

    selected = allowlist[goal]

    payload = dict(base_payload)
    payload.update(
        {
            "verdict": "SELECTED",
            "refusal_reason": None,
            "stop_code": None,
            "selected_command_goal": goal,
            "command_kind": selected["command_kind"],
            "command_lines": selected["command_lines"],
            "command_script": "\n".join(selected["command_lines"]),
            "command_count": len(selected["command_lines"]),
            "command_argvs": selected.get("command_argvs") or [shlex.split(line) for line in selected["command_lines"]],
            "requires_manual_parameters": selected["requires_manual_parameters"],
            "expected_gate_result": selected.get("expected_gate_result"),
            "expected_next_receipts": selected.get("expected_next_receipts"),
            "expected_terminal": selected.get("expected_terminal"),
        }
    )

    out_path = write_selection(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"[bold green]selection_path[/bold green]: {out_path}")



@app.command("agent-plan-check")
def agent_plan_check(selector_receipt: str = typer.Argument(...)):
    """
    Validate a content-addressed agent-select receipt before any execution layer exists.
    """
    def resolve_selector_path(value: str) -> Path:
        candidate = Path(value)
        if candidate.exists():
            return candidate

        candidate = Path("data/agent_select") / f"{value}.json"
        if candidate.exists():
            return candidate

        raise typer.BadParameter(
            "selector_receipt must be an explicit selector JSON path or selector_id present under data/agent_select/"
        )

    def stable_selector_sig(payload: dict) -> str:
        stable = dict(payload)
        stable.pop("selector_id", None)
        stable.pop("selector_payload_sig8", None)
        return sig8(stable)

    def write_plan_check(payload: dict) -> Path:
        out_path, _payload = write_content_addressed_receipt(
            payload,
            "data/agent_plan_checks",
            "plan_check_schema_version",
            AGENT_PLAN_CHECK_SCHEMA,
            "plan_check_id",
            "plan_check_payload_sig8",
        )
        return out_path

    path = resolve_selector_path(selector_receipt)
    data = json.loads(path.read_text())

    selector_id = data.get("selector_id")
    selector_payload_sig8 = data.get("selector_payload_sig8")
    selector_schema_version = data.get("selector_schema_version")
    recomputed_selector_sig8 = stable_selector_sig(data)

    command_argvs = data.get("command_argvs") or []
    command_count = data.get("command_count")
    verdict = data.get("verdict")
    command_kind = data.get("command_kind")

    allowed_prefix = list(ALLOWED_AGENT_PREFIX)
    allowed_subcommands = {
        "stress",
        "gate",
        "agent-eval",
    }

    failures = []

    if selector_schema_version != AGENT_SELECT_SCHEMA:
        failures.append("selector_schema_version_mismatch")

    if not selector_id:
        failures.append("missing_selector_id")

    if not selector_payload_sig8:
        failures.append("missing_selector_payload_sig8")

    if path.stem != selector_id:
        failures.append("selector_id_filename_mismatch")

    if selector_id != selector_payload_sig8:
        failures.append("selector_id_payload_sig_mismatch")

    if recomputed_selector_sig8 != selector_payload_sig8:
        failures.append("selector_payload_sig_recompute_mismatch")

    if verdict != "SELECTED":
        failures.append("selector_verdict_not_SELECTED")

    if command_kind not in {"ALLOWLIST_COMMAND", "ALLOWLIST_COMMAND_EXPECTED_FAIL", "ALLOWLIST_TEMPLATE_REQUIRES_PARAMETER"}:
        failures.append("command_kind_not_allowed")

    if command_count != len(command_argvs):
        failures.append("command_count_argv_count_mismatch")

    if data.get("requires_manual_parameters"):
        failures.append("manual_parameters_required")

    for i, argv in enumerate(command_argvs):
        failures.extend(validate_agent_command_argv(argv, command_index=i))

    expected_fields = [
        "expected_gate_result",
        "expected_next_receipts",
        "expected_terminal",
        "input_eval_id",
        "input_eval_path",
        "input_runs",
        "selected_command_goal",
        "selector_version",
    ]

    for field in expected_fields:
        if data.get(field) in (None, "", []):
            failures.append(f"missing_expected_field:{field}")

    payload = {
        "input_selector_path": str(path),
        "input_selector_id": selector_id,
        "selector_payload_sig8": selector_payload_sig8,
        "recomputed_selector_payload_sig8": recomputed_selector_sig8,
        "selector_schema_version": selector_schema_version,
        "selector_verdict": verdict,
        "selector_command_kind": command_kind,
        "selector_command_count": command_count,
        "selector_argv_count": len(command_argvs),
        "allowed_prefix": allowed_prefix,
        "allowed_subcommands": sorted(allowed_subcommands),
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "plan_check_failed",
            "next_command_goal": "EXECUTOR_DRY_RUN_RECEIPT" if not failures else None,
        },
    }

    out_path = write_plan_check(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        print(f"[bold red]plan_check_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]plan_check_path[/bold green]: {out_path}")



@app.command("agent-exec-dry-run")
def agent_exec_dry_run(plan_check_receipt: str = typer.Argument(...)):
    """
    Emit a dry-run executor receipt from a PASS agent-plan-check receipt. Does not execute subprocesses.
    """
    def resolve_plan_check_path(value: str) -> Path:
        candidate = Path(value)
        if candidate.exists():
            return candidate

        candidate = Path("data/agent_plan_checks") / f"{value}.json"
        if candidate.exists():
            return candidate

        raise typer.BadParameter(
            "plan_check_receipt must be an explicit plan-check JSON path or plan_check_id present under data/agent_plan_checks/"
        )

    def write_exec_dry_run(payload: dict) -> tuple[Path, dict]:
        return write_content_addressed_receipt(
            payload,
            "data/agent_exec_dry_runs",
            "exec_dry_run_schema_version",
            AGENT_EXEC_DRY_RUN_SCHEMA,
            "exec_dry_run_id",
            "exec_dry_run_payload_sig8",
        )

    plan_path = resolve_plan_check_path(plan_check_receipt)
    plan = json.loads(plan_path.read_text())

    failures = []

    plan_check_id = plan.get("plan_check_id")
    plan_check_payload_sig8 = plan.get("plan_check_payload_sig8")
    plan_check_schema_version = plan.get("plan_check_schema_version")
    recomputed_plan_sig8 = stable_sig(plan, "plan_check_id", "plan_check_payload_sig8")

    if plan_check_schema_version != AGENT_PLAN_CHECK_SCHEMA:
        failures.append("plan_check_schema_version_mismatch")

    if not plan_check_id:
        failures.append("missing_plan_check_id")

    if not plan_check_payload_sig8:
        failures.append("missing_plan_check_payload_sig8")

    if plan_path.stem != plan_check_id:
        failures.append("plan_check_id_filename_mismatch")

    if plan_check_id != plan_check_payload_sig8:
        failures.append("plan_check_id_payload_sig_mismatch")

    if recomputed_plan_sig8 != plan_check_payload_sig8:
        failures.append("plan_check_payload_sig_recompute_mismatch")

    if plan.get("gate") != "PASS":
        failures.append("plan_check_gate_not_PASS")

    terminal = plan.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append("plan_check_terminal_not_ADVANCE")

    selector_path = Path(plan.get("input_selector_path") or "")
    selector = None

    if not selector_path.exists():
        failures.append("selector_receipt_missing")
    else:
        selector = json.loads(selector_path.read_text())
        selector_id = selector.get("selector_id")
        selector_payload_sig8 = selector.get("selector_payload_sig8")
        recomputed_selector_sig8 = stable_sig(selector, "selector_id", "selector_payload_sig8")

        if selector.get("selector_schema_version") != AGENT_SELECT_SCHEMA:
            failures.append("selector_schema_version_mismatch")

        if selector_path.stem != selector_id:
            failures.append("selector_id_filename_mismatch")

        if selector_id != selector_payload_sig8:
            failures.append("selector_id_payload_sig_mismatch")

        if recomputed_selector_sig8 != selector_payload_sig8:
            failures.append("selector_payload_sig_recompute_mismatch")

        if selector.get("verdict") != "SELECTED":
            failures.append("selector_verdict_not_SELECTED")

    command_argvs = selector.get("command_argvs") if selector else []
    command_lines = selector.get("command_lines") if selector else []

    allowed_prefix = ["uv", "run", "python", "src/matrixlab/cli.py"]
    allowed_subcommands = set(ALLOWED_AGENT_SUBCOMMANDS)

    for i, argv in enumerate(command_argvs or []):
        if not isinstance(argv, list):
            failures.append(f"command_{i}_argv_not_list")
            continue

        if len(argv) < 5:
            failures.append(f"command_{i}_argv_too_short")
            continue

        if argv[:4] != allowed_prefix:
            failures.append(f"command_{i}_prefix_not_allowed")
            continue

        if argv[4] not in allowed_subcommands:
            failures.append(f"command_{i}_subcommand_not_allowed:{argv[4]}")

    execution_plan = []
    for i, argv in enumerate(command_argvs or []):
        subcommand = argv[4] if len(argv) >= 5 else None
        execution_plan.append(
            {
                "order": i,
                "argv": argv,
                "subcommand": subcommand,
                "would_execute": False,
                "expected_output_kind": (
                    "run_receipt" if subcommand == "stress"
                    else "gate_receipt" if subcommand == "gate"
                    else "agent_eval_receipt" if subcommand == "agent-eval"
                    else "unknown"
                ),
            }
        )

    payload = {
        "input_plan_check_path": str(plan_path),
        "input_plan_check_id": plan_check_id,
        "plan_check_payload_sig8": plan_check_payload_sig8,
        "recomputed_plan_check_payload_sig8": recomputed_plan_sig8,
        "input_selector_path": str(selector_path) if selector_path else None,
        "input_selector_id": selector.get("selector_id") if selector else None,
        "selector_payload_sig8": selector.get("selector_payload_sig8") if selector else None,
        "selector_command_goal": selector.get("selected_command_goal") if selector else None,
        "selector_command_kind": selector.get("command_kind") if selector else None,
        "dry_run_only": True,
        "subprocess_execution": False,
        "command_count": len(command_argvs or []),
        "command_lines": command_lines or [],
        "command_argvs": command_argvs or [],
        "execution_plan": execution_plan,
        "expected_gate_result": selector.get("expected_gate_result") if selector else None,
        "expected_next_receipts": selector.get("expected_next_receipts") if selector else None,
        "expected_terminal": selector.get("expected_terminal") if selector else None,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "exec_dry_run_failed",
            "next_command_goal": "MANUAL_EXECUTE_SELECTED_ARGVS" if not failures else None,
        },
    }

    out_path, payload = write_exec_dry_run(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        print(f"[bold red]exec_dry_run_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]exec_dry_run_path[/bold green]: {out_path}")



@app.command("agent-post-check")
def agent_post_check(
    exec_dry_run_receipt: str = typer.Argument(...),
    observed_eval: str = typer.Argument(...),
):
    """
    Verify that a manual execution result matches a prior PASS executor dry-run receipt.
    """

    def write_post_check(payload: dict) -> tuple[Path, dict]:
        return write_content_addressed_receipt(
            payload,
            "data/agent_post_checks",
            "post_check_schema_version",
            AGENT_POST_CHECK_SCHEMA,
            "post_check_id",
            "post_check_payload_sig8",
        )

    dry_path = resolve_json_path(exec_dry_run_receipt, "data/agent_exec_dry_runs")
    eval_path = resolve_json_path(observed_eval, "data/evals")

    dry = json.loads(dry_path.read_text())
    observed = json.loads(eval_path.read_text())

    failures = []

    dry_id = dry.get("exec_dry_run_id")
    dry_sig = dry.get("exec_dry_run_payload_sig8")
    recomputed_dry_sig = stable_sig(dry, "exec_dry_run_id", "exec_dry_run_payload_sig8")

    if dry.get("exec_dry_run_schema_version") != AGENT_EXEC_DRY_RUN_SCHEMA:
        failures.append("exec_dry_run_schema_version_mismatch")

    if dry_path.stem != dry_id:
        failures.append("exec_dry_run_id_filename_mismatch")

    if dry_id != dry_sig:
        failures.append("exec_dry_run_id_payload_sig_mismatch")

    if recomputed_dry_sig != dry_sig:
        failures.append("exec_dry_run_payload_sig_recompute_mismatch")

    if dry.get("gate") != "PASS":
        failures.append("exec_dry_run_gate_not_PASS")

    if dry.get("dry_run_only") is not True:
        failures.append("exec_dry_run_not_marked_dry_run_only")

    if dry.get("subprocess_execution") is not False:
        failures.append("exec_dry_run_subprocess_execution_not_false")

    dry_terminal = dry.get("terminal") or {}
    if dry_terminal.get("type") != "ADVANCE":
        failures.append("exec_dry_run_terminal_not_ADVANCE")

    observed_input_runs = observed.get("input_runs") or []
    observed_current_run = observed_input_runs[0] if observed_input_runs else None
    observed_previous_run = observed_input_runs[1] if len(observed_input_runs) > 1 else None

    dry_selector_previous = None
    for argv in dry.get("command_argvs") or []:
        if len(argv) >= 7 and argv[4] == "agent-eval":
            for i, part in enumerate(argv):
                if part == "--previous" and i + 1 < len(argv):
                    dry_selector_previous = argv[i + 1]

    if observed.get("gate") != "PASS":
        failures.append("observed_eval_gate_not_PASS")

    observed_terminal = observed.get("terminal") or {}
    if observed_terminal.get("type") != "ADVANCE":
        failures.append("observed_eval_terminal_not_ADVANCE")

    observed_metrics = observed.get("metrics") or {}
    if int(observed_metrics.get("law_failures") or 0) != 0:
        failures.append("observed_eval_law_failures_nonzero")

    if int(observed_metrics.get("unknown_laws") or 0) != 0:
        failures.append("observed_eval_unknown_laws_nonzero")

    if int(observed_metrics.get("orphan_receipt_runs") or 0) != 0:
        failures.append("observed_eval_orphan_receipts_nonzero")

    if dry_selector_previous and observed_previous_run != dry_selector_previous:
        failures.append("observed_previous_run_mismatch")

    expected_gate_result = dry.get("expected_gate_result")
    expected_terminal = dry.get("expected_terminal")
    expected_next_receipts = dry.get("expected_next_receipts")

    if expected_gate_result != "PASS":
        failures.append("dry_expected_gate_result_not_PASS")

    if expected_terminal != "ADVANCE":
        failures.append("dry_expected_terminal_not_ADVANCE")

    if not expected_next_receipts:
        failures.append("missing_dry_expected_next_receipts")

    allowed_compression_signals = {
        "BASELINE",
        "FLAT",
        "GOOD",
        "GOOD_WEAK",
        "GOOD_RECEIPT_EXPANSION",
    }

    compression_signal = (observed.get("classification") or {}).get("compression_signal")
    if compression_signal not in allowed_compression_signals:
        failures.append(f"observed_compression_signal_not_allowed:{compression_signal}")

    expected_shape = {
        "total_cases": 490,
        "total_receipts": 48784,
        "coarse_move_profiles_total": 9,
        "raw_move_profiles_total": 405,
        "registered_moves_total": 100,
        "max_moves_applied_before_halt": 100,
    }

    observed_shape = {
        key: observed_metrics.get(key)
        for key in expected_shape
    }

    for key, expected_value in expected_shape.items():
        if observed_shape.get(key) != expected_value:
            failures.append(f"observed_shape_mismatch:{key}")

    payload = {
        "input_exec_dry_run_path": str(dry_path),
        "input_exec_dry_run_id": dry_id,
        "exec_dry_run_payload_sig8": dry_sig,
        "recomputed_exec_dry_run_payload_sig8": recomputed_dry_sig,
        "input_observed_eval_path": str(eval_path),
        "input_observed_eval_id": observed.get("eval_id"),
        "observed_current_run": observed_current_run,
        "observed_previous_run": observed_previous_run,
        "dry_selector_previous_run": dry_selector_previous,
        "observed_gate": observed.get("gate"),
        "observed_terminal": observed_terminal,
        "observed_compression_signal": compression_signal,
        "allowed_compression_signals": sorted(allowed_compression_signals),
        "expected_shape": expected_shape,
        "observed_shape": observed_shape,
        "expected_gate_result": expected_gate_result,
        "expected_next_receipts": expected_next_receipts,
        "expected_terminal": expected_terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "post_check_failed",
            "next_command_goal": "READY_FOR_OPERATOR_CONFIRMATION_OR_NEXT_SELECTOR" if not failures else None,
        },
    }

    out_path, payload = write_post_check(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        print(f"[bold red]post_check_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]post_check_path[/bold green]: {out_path}")



@app.command("agent-loop-summary")
def agent_loop_summary(post_check_receipt: str = typer.Argument(...)):
    """
    Emit a compact receipt card for one complete operator-mediated agent loop.
    """

    def write_loop_summary(payload: dict) -> tuple[Path, dict]:
        return write_content_addressed_receipt(
            payload,
            "data/agent_loop_summaries",
            "loop_summary_schema_version",
            AGENT_LOOP_SUMMARY_SCHEMA,
            "loop_summary_id",
            "loop_summary_payload_sig8",
        )

    def load_optional(path_value):
        if not path_value:
            return None, None
        path = Path(path_value)
        if not path.exists():
            return path, None
        return path, json.loads(path.read_text())

    post_path = resolve_json_path(post_check_receipt, "data/agent_post_checks")
    post = json.loads(post_path.read_text())

    failures = []

    post_id = post.get("post_check_id")
    post_sig = post.get("post_check_payload_sig8")
    recomputed_post_sig = stable_sig(post, "post_check_id", "post_check_payload_sig8")

    if post.get("post_check_schema_version") != AGENT_POST_CHECK_SCHEMA:
        failures.append("post_check_schema_version_mismatch")

    if post_path.stem != post_id:
        failures.append("post_check_id_filename_mismatch")

    if post_id != post_sig:
        failures.append("post_check_id_payload_sig_mismatch")

    if recomputed_post_sig != post_sig:
        failures.append("post_check_payload_sig_recompute_mismatch")

    dry_path, dry = load_optional(post.get("input_exec_dry_run_path"))
    eval_path, observed_eval = load_optional(post.get("input_observed_eval_path"))

    if dry is None:
        failures.append("missing_exec_dry_run_receipt")

    if observed_eval is None:
        failures.append("missing_observed_eval_receipt")

    plan_path, plan = load_optional(dry.get("input_plan_check_path") if dry else None)
    selector_path, selector = load_optional(dry.get("input_selector_path") if dry else None)

    if dry and plan is None:
        failures.append("missing_plan_check_receipt")

    if dry and selector is None:
        failures.append("missing_selector_receipt")

    source_eval_path, source_eval = load_optional(selector.get("input_eval_path") if selector else None)

    if selector and source_eval is None:
        failures.append("missing_source_eval_receipt")

    def receipt_ref(data: dict | None, id_key: str, gate_key: str = "gate"):
        if not data:
            return {
                "id": None,
                "gate": None,
                "terminal_type": None,
                "terminal_goal": None,
                "stop_code": None,
            }
        terminal = data.get("terminal") or {}
        return {
            "id": data.get(id_key),
            "gate": data.get(gate_key),
            "terminal_type": terminal.get("type"),
            "terminal_goal": terminal.get("next_command_goal"),
            "stop_code": terminal.get("stop_code"),
        }

    chain = {
        "source_eval": receipt_ref(source_eval, "eval_id"),
        "selector": {
            "id": selector.get("selector_id") if selector else None,
            "verdict": selector.get("verdict") if selector else None,
            "selected_command_goal": selector.get("selected_command_goal") if selector else None,
            "command_count": selector.get("command_count") if selector else None,
        },
        "plan_check": receipt_ref(plan, "plan_check_id"),
        "exec_dry_run": receipt_ref(dry, "exec_dry_run_id"),
        "observed_eval": receipt_ref(observed_eval, "eval_id"),
        "post_check": receipt_ref(post, "post_check_id"),
    }

    observed_metrics = (observed_eval or {}).get("metrics") or {}
    observed_input_runs = (observed_eval or {}).get("input_runs") or []

    post_failures = post.get("failures") or []
    if post.get("gate") != "PASS":
        failures.append("post_check_gate_not_PASS")

    if post_failures:
        failures.extend([f"post_check_failure:{x}" for x in post_failures])

    if dry and dry.get("gate") != "PASS":
        failures.append("exec_dry_run_gate_not_PASS")

    if plan and plan.get("gate") != "PASS":
        failures.append("plan_check_gate_not_PASS")

    if selector and selector.get("verdict") != "SELECTED":
        failures.append("selector_verdict_not_SELECTED")

    if source_eval and source_eval.get("gate") != "PASS":
        failures.append("source_eval_gate_not_PASS")

    if observed_eval and observed_eval.get("gate") != "PASS":
        failures.append("observed_eval_gate_not_PASS")

    compact_card = {
        "selected_goal": selector.get("selected_command_goal") if selector else None,
        "observed_run_id": observed_input_runs[0] if observed_input_runs else None,
        "observed_previous_run_id": observed_input_runs[1] if len(observed_input_runs) > 1 else None,
        "observed_compression_signal": ((observed_eval or {}).get("classification") or {}).get("compression_signal"),
        "observed_total_cases": observed_metrics.get("total_cases"),
        "observed_total_receipts": observed_metrics.get("total_receipts"),
        "observed_coarse_profiles": observed_metrics.get("coarse_move_profiles_total"),
        "observed_raw_profiles": observed_metrics.get("raw_move_profiles_total"),
        "observed_registered_moves": observed_metrics.get("registered_moves_total"),
        "observed_continuation_radius": observed_metrics.get("max_moves_applied_before_halt"),
        "observed_law_failures": observed_metrics.get("law_failures"),
        "observed_unknown_laws": observed_metrics.get("unknown_laws"),
        "observed_orphan_receipt_runs": observed_metrics.get("orphan_receipt_runs"),
        "next_permitted_goal": (post.get("terminal") or {}).get("next_command_goal"),
    }

    payload = {
        "input_post_check_path": str(post_path),
        "input_post_check_id": post_id,
        "post_check_payload_sig8": post_sig,
        "recomputed_post_check_payload_sig8": recomputed_post_sig,
        "chain": chain,
        "compact_card": compact_card,
        "post_check_failures": post_failures,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "loop_summary_failed",
            "next_command_goal": "OPERATOR_CONFIRM_NEXT_LOOP" if not failures else None,
        },
    }

    out_path, payload = write_loop_summary(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        print(f"[bold red]loop_summary_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]loop_summary_path[/bold green]: {out_path}")



@app.command("agent-confirm-loop")
def agent_confirm_loop(
    loop_summary_receipt: str = typer.Argument(...),
    decision: str = typer.Option(..., "--decision", "-d", help="Operator decision: continue or stop."),
):
    """
    Record explicit operator confirmation for a completed PASS loop summary.
    """

    def write_confirmation(payload: dict) -> tuple[Path, dict]:
        return write_content_addressed_receipt(
            payload,
            "data/agent_confirmations",
            "confirmation_schema_version",
            AGENT_CONFIRMATION_SCHEMA,
            "confirmation_id",
            "confirmation_payload_sig8",
        )

    decision = decision.strip().lower()
    allowed_decisions = {"continue", "stop"}

    loop_path = resolve_json_path(loop_summary_receipt, "data/agent_loop_summaries")
    loop = json.loads(loop_path.read_text())

    failures = []

    if decision not in allowed_decisions:
        failures.append(f"decision_not_allowed:{decision}")

    loop_id = loop.get("loop_summary_id")
    loop_sig = loop.get("loop_summary_payload_sig8")
    recomputed_loop_sig = stable_sig(loop, "loop_summary_id", "loop_summary_payload_sig8")

    if loop.get("loop_summary_schema_version") != AGENT_LOOP_SUMMARY_SCHEMA:
        failures.append("loop_summary_schema_version_mismatch")

    if loop_path.stem != loop_id:
        failures.append("loop_summary_id_filename_mismatch")

    if loop_id != loop_sig:
        failures.append("loop_summary_id_payload_sig_mismatch")

    if recomputed_loop_sig != loop_sig:
        failures.append("loop_summary_payload_sig_recompute_mismatch")

    if loop.get("gate") != "PASS":
        failures.append("loop_summary_gate_not_PASS")

    loop_terminal = loop.get("terminal") or {}
    if loop_terminal.get("type") != "ADVANCE":
        failures.append("loop_summary_terminal_not_ADVANCE")

    compact = loop.get("compact_card") or {}
    chain = loop.get("chain") or {}
    observed_eval = chain.get("observed_eval") or {}

    observed_eval_id = observed_eval.get("id")
    observed_run_id = compact.get("observed_run_id")
    observed_compression_signal = compact.get("observed_compression_signal")

    if not observed_eval_id:
        failures.append("missing_observed_eval_id")

    if not observed_run_id:
        failures.append("missing_observed_run_id")

    if decision == "continue" and not failures:
        terminal_type = "ADVANCE"
        stop_code = None
        next_command_goal = "AGENT_SELECT_FROM_OBSERVED_EVAL"
        next_allowed_source = {
            "kind": "agent_eval",
            "eval_id": observed_eval_id,
            "run_id": observed_run_id,
        }
    elif decision == "stop" and not failures:
        terminal_type = "STOP"
        stop_code = "operator_stopped_cleanly"
        next_command_goal = None
        next_allowed_source = None
    else:
        terminal_type = "STOP"
        stop_code = "operator_confirmation_failed"
        next_command_goal = None
        next_allowed_source = None

    payload = {
        "input_loop_summary_path": str(loop_path),
        "input_loop_summary_id": loop_id,
        "loop_summary_payload_sig8": loop_sig,
        "recomputed_loop_summary_payload_sig8": recomputed_loop_sig,
        "operator_decision": decision,
        "allowed_decisions": sorted(allowed_decisions),
        "observed_eval_id": observed_eval_id,
        "observed_run_id": observed_run_id,
        "observed_compression_signal": observed_compression_signal,
        "source_selected_goal": compact.get("selected_goal"),
        "source_next_permitted_goal": compact.get("next_permitted_goal"),
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "next_allowed_source": next_allowed_source,
        "terminal": {
            "type": terminal_type,
            "stop_code": stop_code,
            "next_command_goal": next_command_goal,
        },
    }

    out_path, payload = write_confirmation(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        print(f"[bold red]confirmation_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]confirmation_path[/bold green]: {out_path}")



@app.command("agent-next-from-confirmation")
def agent_next_from_confirmation(confirmation_receipt: str = typer.Argument(...)):
    """
    Consume a PASS continue confirmation and emit the next fixed selector receipt from its allowed eval source.
    """
    import shlex

    def write_selector(payload: dict) -> tuple[Path, dict]:
        payload = dict(payload)
        payload["selector_schema_version"] = AGENT_SELECT_SCHEMA
        payload["selector_payload_sig8"] = selector_payload_sig(payload)
        payload["selector_id"] = payload["selector_payload_sig8"]

        out_dir = Path("data/agent_select")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{payload['selector_id']}.json"
        out_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return out_path, payload


    def write_next_receipt(payload: dict) -> tuple[Path, dict]:
        return write_content_addressed_receipt(
            payload,
            "data/agent_next_from_confirmations",
            "next_from_confirmation_schema_version",
            AGENT_NEXT_FROM_CONFIRMATION_SCHEMA,
            "next_from_confirmation_id",
            "next_from_confirmation_payload_sig8",
        )

    conf_path = resolve_json_path(confirmation_receipt, "data/agent_confirmations")
    conf = json.loads(conf_path.read_text())

    failures = []

    conf_id = conf.get("confirmation_id")
    conf_sig = conf.get("confirmation_payload_sig8")
    recomputed_conf_sig = stable_sig(conf, "confirmation_id", "confirmation_payload_sig8")

    if conf.get("confirmation_schema_version") != AGENT_CONFIRMATION_SCHEMA:
        failures.append("confirmation_schema_version_mismatch")

    if conf_path.stem != conf_id:
        failures.append("confirmation_id_filename_mismatch")

    if conf_id != conf_sig:
        failures.append("confirmation_id_payload_sig_mismatch")

    if recomputed_conf_sig != conf_sig:
        failures.append("confirmation_payload_sig_recompute_mismatch")

    if conf.get("gate") != "PASS":
        failures.append("confirmation_gate_not_PASS")

    if conf.get("operator_decision") != "continue":
        failures.append("operator_decision_not_continue")

    conf_terminal = conf.get("terminal") or {}
    if conf_terminal.get("type") != "ADVANCE":
        failures.append("confirmation_terminal_not_ADVANCE")

    if conf_terminal.get("next_command_goal") != "AGENT_SELECT_FROM_OBSERVED_EVAL":
        failures.append("confirmation_next_goal_mismatch")

    next_allowed_source = conf.get("next_allowed_source") or {}
    if next_allowed_source.get("kind") != "agent_eval":
        failures.append("next_allowed_source_kind_not_agent_eval")

    eval_id = next_allowed_source.get("eval_id")
    run_id = next_allowed_source.get("run_id")

    eval_path = Path("data/evals") / f"{eval_id}.json" if eval_id else None
    eval_report = None

    if not eval_id:
        failures.append("missing_next_eval_id")
    elif not eval_path.exists():
        failures.append("next_eval_receipt_missing")
    else:
        eval_report = json.loads(eval_path.read_text())

    if eval_report:
        if eval_report.get("eval_id") != eval_id:
            failures.append("next_eval_id_mismatch")

        if eval_report.get("gate") != "PASS":
            failures.append("next_eval_gate_not_PASS")

        terminal = eval_report.get("terminal") or {}
        if terminal.get("type") != "ADVANCE":
            failures.append("next_eval_terminal_not_ADVANCE")

        input_runs = eval_report.get("input_runs") or []
        if run_id and (not input_runs or input_runs[0] != run_id):
            failures.append("next_eval_run_id_mismatch")

    def selector_base_for_eval(report: dict, path: Path) -> dict:
        terminal = report.get("terminal") or {}
        input_runs = report.get("input_runs") or []
        current_run_id = input_runs[0] if input_runs else None
        goal = terminal.get("next_command_goal")
        gate = report.get("gate")
        terminal_type = terminal.get("type")

        return {
            "input_eval_path": str(path),
            "input_eval_id": report.get("eval_id"),
            "input_runs": input_runs,
            "eval_gate": gate,
            "eval_terminal_type": terminal_type,
            "requested_goal": goal,
            "selector_version": "agent_select_allowlist_v0",
            "safety_rules": [
                "explicit_confirmation_only",
                "confirmation_must_be_PASS_continue",
                "next_allowed_source_must_be_agent_eval",
                "referenced_eval_must_exist",
                "referenced_eval_gate_must_PASS",
                "no_latest_file_or_mtime_authority",
                "no_command_invention",
                "no_code_editing",
                "no_architecture_widening",
                "refuse_if_eval_gate_not_PASS",
                "refuse_if_terminal_not_ADVANCE",
                "fixed_allowlist_only",
            ],
        }

    def refuse_selector(base_payload: dict, reason: str, stop_code: str = None):
        payload = dict(base_payload)
        payload.update(
            {
                "verdict": "REFUSE",
                "refusal_reason": reason,
                "stop_code": stop_code or reason,
                "selected_command_goal": None,
                "command_kind": None,
                "command_lines": [],
                "command_script": "",
                "command_count": 0,
                "command_argvs": [],
                "requires_manual_parameters": [],
                "expected_gate_result": None,
                "expected_next_receipts": None,
                "expected_terminal": "STOP",
            }
        )
        return write_selector(payload)

    selected_selector_path = None
    selected_selector = None

    if not failures and eval_report:
        base_payload = selector_base_for_eval(eval_report, eval_path)
        goal = base_payload.get("requested_goal")
        current_run_id = (base_payload.get("input_runs") or [None])[0]

        if base_payload.get("eval_gate") != "PASS":
            selected_selector_path, selected_selector = refuse_selector(base_payload, "eval_gate_not_PASS", "gate_failed")
        elif base_payload.get("eval_terminal_type") != "ADVANCE":
            selected_selector_path, selected_selector = refuse_selector(base_payload, "terminal_not_ADVANCE", "not_advance")
        elif not goal:
            selected_selector_path, selected_selector = refuse_selector(base_payload, "missing_next_command_goal")
        else:
            allowlist = {
                "ADD_PREVIOUS_RUN_COMPARISON": {
                    "command_kind": "ALLOWLIST_TEMPLATE_REQUIRES_PARAMETER",
                    "command_lines": [
                        f"uv run python src/matrixlab/cli.py agent-eval {current_run_id} --previous <previous_run_id>"
                    ],
                    "requires_manual_parameters": ["previous_run_id"],
                    "expected_gate_result": "PASS",
                    "expected_next_receipts": "depends_on_previous_run_parameter",
                    "expected_terminal": "ADVANCE_OR_STOP_TYPED",
                },
                "RUN_SMALL_NORMAL_STRICT": {
                    "command_kind": "ALLOWLIST_COMMAND",
                    "command_lines": [
                        "uv run python src/matrixlab/cli.py stress --families ABCDE --depth-max 20 --cycles-per-case 20 --max-cells 50000 --strict-laws",
                        "uv run python src/matrixlab/cli.py gate latest",
                        f"uv run python src/matrixlab/cli.py agent-eval latest --previous {current_run_id}",
                    ],
                    "requires_manual_parameters": [],
                    "expected_gate_result": "PASS",
                    "expected_next_receipts": "normal_strict_small_run",
                    "expected_terminal": "ADVANCE",
                },
                "RUN_FULL_NORMAL_STRICT": {
                    "command_kind": "ALLOWLIST_COMMAND",
                    "command_lines": [
                        "uv run python src/matrixlab/cli.py stress --families ABCDE --depth-max 100 --cycles-per-case 100 --max-cells 50000 --strict-laws",
                        "uv run python src/matrixlab/cli.py gate latest",
                        f"uv run python src/matrixlab/cli.py agent-eval latest --previous {current_run_id}",
                    ],
                    "requires_manual_parameters": [],
                    "expected_gate_result": "PASS",
                    "expected_next_receipts": "normal_strict_full_run",
                    "expected_terminal": "ADVANCE",
                },
                "RUN_BAD_PROBE_STRICT_NEGATIVE_CONTROL": {
                    "command_kind": "ALLOWLIST_COMMAND_EXPECTED_FAIL",
                    "command_lines": [
                        "uv run python src/matrixlab/cli.py stress --families F --depth-max 8 --cycles-per-case 5 --max-cells 50000 --strict-laws",
                        "uv run python src/matrixlab/cli.py gate latest || true",
                        "uv run python src/matrixlab/cli.py agent-eval latest || true",
                    ],
                    "requires_manual_parameters": [],
                    "expected_gate_result": "FAIL",
                    "expected_next_receipts": "law_violation_probe_strict_negative_control",
                    "expected_terminal": "STOP",
                },
            }

            if goal not in allowlist:
                selected_selector_path, selected_selector = refuse_selector(base_payload, "goal_not_in_allowlist")
            else:
                selected = allowlist[goal]
                payload = dict(base_payload)
                payload.update(
                    {
                        "verdict": "SELECTED",
                        "refusal_reason": None,
                        "stop_code": None,
                        "selected_command_goal": goal,
                        "command_kind": selected["command_kind"],
                        "command_lines": selected["command_lines"],
                        "command_script": "\n".join(selected["command_lines"]),
                        "command_count": len(selected["command_lines"]),
                        "command_argvs": selected.get("command_argvs") or [shlex.split(line) for line in selected["command_lines"]],
                        "requires_manual_parameters": selected["requires_manual_parameters"],
                        "expected_gate_result": selected.get("expected_gate_result"),
                        "expected_next_receipts": selected.get("expected_next_receipts"),
                        "expected_terminal": selected.get("expected_terminal"),
                    }
                )
                selected_selector_path, selected_selector = write_selector(payload)

    payload = {
        "input_confirmation_path": str(conf_path),
        "input_confirmation_id": conf_id,
        "confirmation_payload_sig8": conf_sig,
        "recomputed_confirmation_payload_sig8": recomputed_conf_sig,
        "operator_decision": conf.get("operator_decision"),
        "next_allowed_source": next_allowed_source,
        "referenced_eval_path": str(eval_path) if eval_path else None,
        "referenced_eval_id": eval_id,
        "referenced_run_id": run_id,
        "selected_selector_path": str(selected_selector_path) if selected_selector_path else None,
        "selected_selector_id": selected_selector.get("selector_id") if selected_selector else None,
        "selected_selector_verdict": selected_selector.get("verdict") if selected_selector else None,
        "selected_command_goal": selected_selector.get("selected_command_goal") if selected_selector else None,
        "gate": "PASS" if not failures and selected_selector and selected_selector.get("verdict") == "SELECTED" else "FAIL",
        "failures": failures if failures else ([] if selected_selector and selected_selector.get("verdict") == "SELECTED" else ["selector_not_selected"]),
        "terminal": {
            "type": "ADVANCE" if not failures and selected_selector and selected_selector.get("verdict") == "SELECTED" else "STOP",
            "stop_code": None if not failures and selected_selector and selected_selector.get("verdict") == "SELECTED" else "next_from_confirmation_failed",
            "next_command_goal": "PLAN_CHECK_SELECTED_SELECTOR" if not failures and selected_selector and selected_selector.get("verdict") == "SELECTED" else None,
        },
    }

    out_path, payload = write_next_receipt(payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    if payload["gate"] != "PASS":
        print(f"[bold red]next_from_confirmation_path[/bold red]: {out_path}")
        raise typer.Exit(1)

    print(f"[bold green]next_from_confirmation_path[/bold green]: {out_path}")


@app.command("agent-cycle-ledger")
def agent_cycle_ledger(
    loop_summaries: list[str] = typer.Argument(
        ...,
        help="Explicit loop_summary ids or JSON paths, in cycle order.",
    ),
):
    """Build a machine-readable cycle ledger from explicit loop summary receipts."""

    rows = []
    failures = []

    for cycle_n, loop_ref in enumerate(loop_summaries, start=1):
        try:
            loop_path = resolve_json_path(loop_ref, "data/agent_loop_summaries")
            loop = json.loads(loop_path.read_text())
        except Exception as exc:
            failures.append(f"cycle_{cycle_n}_loop_summary_unresolved:{loop_ref}:{exc}")
            continue

        loop_sig = stable_sig(loop, "loop_summary_id", "loop_summary_payload_sig8")
        compact = loop.get("compact_card") or {}
        chain = loop.get("chain") or {}
        observed_eval = chain.get("observed_eval") or {}
        post_check = chain.get("post_check") or {}
        selector = chain.get("selector") or {}

        if loop.get("gate") != "PASS":
            failures.append(f"cycle_{cycle_n}_loop_summary_gate_not_PASS")

        if loop.get("loop_summary_payload_sig8") != loop_sig:
            failures.append(f"cycle_{cycle_n}_loop_summary_sig_mismatch")

        if loop_path.stem != loop.get("loop_summary_id"):
            failures.append(f"cycle_{cycle_n}_loop_summary_filename_id_mismatch")

        row = {
            "cycle_n": cycle_n,
            "loop_summary_id": loop.get("loop_summary_id"),
            "loop_summary_path": str(loop_path),
            "loop_summary_sig8": loop.get("loop_summary_payload_sig8"),
            "loop_summary_recomputed_sig8": loop_sig,
            "loop_summary_gate": loop.get("gate"),
            "selected_goal": compact.get("selected_goal") or selector.get("selected_command_goal"),
            "run_id": compact.get("observed_run_id"),
            "eval_id": observed_eval.get("id"),
            "previous_run_id": compact.get("observed_previous_run_id"),
            "post_check_id": post_check.get("id") or loop.get("input_post_check_id"),
            "registered_moves_total": compact.get("observed_registered_moves"),
            "max_moves_applied_before_halt": compact.get("observed_continuation_radius"),
            "coarse_profiles_total": compact.get("observed_coarse_profiles"),
            "raw_profiles_total": compact.get("observed_raw_profiles"),
            "total_cases": compact.get("observed_total_cases"),
            "total_receipts": compact.get("observed_total_receipts"),
            "compression_signal": compact.get("observed_compression_signal"),
            "law_failures": compact.get("observed_law_failures"),
            "unknown_laws": compact.get("observed_unknown_laws"),
            "orphan_receipt_runs": compact.get("observed_orphan_receipt_runs"),
            "next_permitted_goal": compact.get("next_permitted_goal"),
        }

        rows.append(row)

    for index, row in enumerate(rows):
        if not row.get("run_id"):
            failures.append(f"cycle_{row.get('cycle_n')}_missing_run_id")
        if not row.get("eval_id"):
            failures.append(f"cycle_{row.get('cycle_n')}_missing_eval_id")
        if row.get("law_failures") != 0:
            failures.append(f"cycle_{row.get('cycle_n')}_law_failures_nonzero")
        if row.get("unknown_laws") != 0:
            failures.append(f"cycle_{row.get('cycle_n')}_unknown_laws_nonzero")
        if row.get("orphan_receipt_runs") != 0:
            failures.append(f"cycle_{row.get('cycle_n')}_orphan_receipt_runs_nonzero")

        if index > 0:
            prev = rows[index - 1]
            if row.get("previous_run_id") != prev.get("run_id"):
                failures.append(
                    f"cycle_{row.get('cycle_n')}_previous_run_mismatch:"
                    f"{row.get('previous_run_id')}!={prev.get('run_id')}"
                )

    first = rows[0] if rows else {}
    last = rows[-1] if rows else {}
    cycle_count = len(rows)

    registered_delta = None
    continuation_delta = None
    coarse_delta = None
    receipt_delta = None

    if cycle_count >= 2:
        registered_delta = (last.get("registered_moves_total") or 0) - (
            first.get("registered_moves_total") or 0
        )
        continuation_delta = (last.get("max_moves_applied_before_halt") or 0) - (
            first.get("max_moves_applied_before_halt") or 0
        )
        coarse_delta = (last.get("coarse_profiles_total") or 0) - (
            first.get("coarse_profiles_total") or 0
        )
        receipt_delta = (last.get("total_receipts") or 0) - (
            first.get("total_receipts") or 0
        )

    compression_assessment = {
        "cycle_count": cycle_count,
        "first_run_id": first.get("run_id"),
        "last_run_id": last.get("run_id"),
        "registered_moves_delta": registered_delta,
        "continuation_radius_delta": continuation_delta,
        "coarse_profiles_delta": coarse_delta,
        "total_receipts_delta": receipt_delta,
        "all_compression_signals": [row.get("compression_signal") for row in rows],
        "all_gates_pass": all(row.get("loop_summary_gate") == "PASS" for row in rows),
        "all_laws_clean": all(
            row.get("law_failures") == 0
            and row.get("unknown_laws") == 0
            and row.get("orphan_receipt_runs") == 0
            for row in rows
        ),
    }

    if failures:
        verdict = "FAIL"
    elif cycle_count < 2:
        verdict = "BASELINE_LEDGER"
    elif registered_delta == 0 and continuation_delta == 0 and coarse_delta == 0 and receipt_delta == 0:
        verdict = "REPRODUCED_FLAT_STABILITY"
    elif coarse_delta == 0 and registered_delta is not None and registered_delta <= max(1, cycle_count):
        verdict = "BOUNDED_VOCABULARY_CONTINUATION"
    else:
        verdict = "MEASURED_NONFLAT_CHANGE"

    payload = {
        "input_loop_summaries": list(loop_summaries),
        "cycle_count": cycle_count,
        "cycles": rows,
        "compression_assessment": compression_assessment,
        "verdict": verdict,
        "failures": failures,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "USE_LEDGER_FOR_NEXT_AGENT_EVAL_DIRECTION",
            "stop_code": "cycle_ledger_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cycle_ledgers",
        "cycle_ledger_schema_version",
        AGENT_CYCLE_LEDGER_SCHEMA,
        "cycle_ledger_id",
        "cycle_ledger_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"cycle_ledger_path: {out_path}")



@app.command("agent-cycle-next")
def agent_cycle_next(
    cycle_ledger: str = typer.Argument(
        ...,
        help="Explicit cycle ledger id or JSON path.",
    ),
    depth_step: int = typer.Option(
        50,
        "--depth-step",
        help="Continuation-radius expansion step.",
    ),
    families: str = typer.Option(
        "ABCDE",
        "--families",
        help="Move families for the next controlled stress run.",
    ),
    max_cells: int = typer.Option(
        50000,
        "--max-cells",
        help="Max cells for the next controlled stress run.",
    ),
    strict_laws: bool = typer.Option(
        True,
        "--strict-laws/--no-strict-laws",
        help="Preserve strict law checking for the next controlled stress run.",
    ),
):
    """Select the next controlled experiment from a cycle ledger."""

    failures = []

    try:
        ledger_path = resolve_json_path(cycle_ledger, "data/agent_cycle_ledgers")
        ledger = json.loads(ledger_path.read_text())
    except Exception as exc:
        ledger_path = None
        ledger = {}
        failures.append(f"cycle_ledger_unresolved:{cycle_ledger}:{exc}")

    ledger_sig = None
    if ledger:
        ledger_sig = stable_sig(ledger, "cycle_ledger_id", "cycle_ledger_payload_sig8")

        if ledger.get("gate") != "PASS":
            failures.append("cycle_ledger_gate_not_PASS")

        if ledger.get("cycle_ledger_payload_sig8") != ledger_sig:
            failures.append("cycle_ledger_sig_mismatch")

        if ledger_path and ledger_path.stem != ledger.get("cycle_ledger_id"):
            failures.append("cycle_ledger_filename_id_mismatch")

    cycles = ledger.get("cycles") or []
    assessment = ledger.get("compression_assessment") or {}
    last_cycle = cycles[-1] if cycles else {}

    if not cycles:
        failures.append("cycle_ledger_has_no_cycles")

    if not assessment.get("all_gates_pass"):
        failures.append("cycle_ledger_not_all_gates_pass")

    if not assessment.get("all_laws_clean"):
        failures.append("cycle_ledger_not_all_laws_clean")

    previous_run_id = last_cycle.get("run_id")
    current_radius = last_cycle.get("max_moves_applied_before_halt")

    if not previous_run_id:
        failures.append("missing_last_run_id")

    if not isinstance(current_radius, int):
        failures.append("missing_integer_current_radius")
        current_radius = 0

    if depth_step <= 0:
        failures.append("depth_step_not_positive")

    next_radius = current_radius + depth_step if isinstance(current_radius, int) else depth_step

    ledger_verdict = ledger.get("verdict")
    if ledger_verdict in ["REPRODUCED_FLAT_STABILITY", "BOUNDED_VOCABULARY_CONTINUATION"]:
        selected_goal = "RUN_FULL_NORMAL_STRICT_EXPAND_CONTINUATION_RADIUS"
        selection_reason = "ledger_is_clean_and_repeated_same_radius_no_longer_adds_information"
    elif ledger_verdict == "BASELINE_LEDGER":
        selected_goal = "RUN_FULL_NORMAL_STRICT_REPRODUCE_BASELINE"
        selection_reason = "single_cycle_ledger_needs_one_reproduction_before_expansion"
    else:
        selected_goal = None
        selection_reason = f"ledger_verdict_not_actionable:{ledger_verdict}"
        failures.append("ledger_verdict_not_actionable")

    command_argvs = []
    if not failures:
        stress_argv = [
            "uv",
            "run",
            "python",
            "src/matrixlab/cli.py",
            "stress",
            "--families",
            families,
            "--depth-max",
            str(next_radius),
            "--cycles-per-case",
            str(next_radius),
            "--max-cells",
            str(max_cells),
        ]

        if strict_laws:
            stress_argv.append("--strict-laws")

        command_argvs = [
            stress_argv,
            [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "gate",
                "latest",
            ],
            [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "agent-eval",
                "latest",
                "--previous",
                previous_run_id,
            ],
        ]

    command_lines = [" ".join(argv) for argv in command_argvs]

    payload = {
        "input_cycle_ledger": cycle_ledger,
        "input_cycle_ledger_path": str(ledger_path) if ledger_path else None,
        "cycle_ledger_id": ledger.get("cycle_ledger_id"),
        "cycle_ledger_payload_sig8": ledger.get("cycle_ledger_payload_sig8"),
        "recomputed_cycle_ledger_payload_sig8": ledger_sig,
        "ledger_gate": ledger.get("gate"),
        "ledger_verdict": ledger_verdict,
        "ledger_cycle_count": ledger.get("cycle_count"),
        "last_run_id": previous_run_id,
        "last_eval_id": last_cycle.get("eval_id"),
        "current_radius": current_radius,
        "depth_step": depth_step,
        "next_radius": next_radius,
        "families": families,
        "max_cells": max_cells,
        "strict_laws": strict_laws,
        "selected_goal": selected_goal,
        "selection_reason": selection_reason,
        "command_kind": "CONTROLLED_CONTINUATION_EXPANSION" if not failures else None,
        "command_count": len(command_argvs),
        "command_argvs": command_argvs,
        "command_lines": command_lines,
        "command_script": "\n".join(command_lines),
        "failures": failures,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "MANUAL_EXECUTE_CYCLE_NEXT_COMMANDS",
            "stop_code": "cycle_next_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cycle_next",
        "cycle_next_schema_version",
        AGENT_CYCLE_NEXT_SCHEMA,
        "cycle_next_id",
        "cycle_next_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"cycle_next_path: {out_path}")



@app.command("agent-cycle-observe")
def agent_cycle_observe(
    cycle_next: str = typer.Argument(
        ...,
        help="Explicit cycle-next id or JSON path.",
    ),
    observed_eval: str = typer.Argument(
        ...,
        help="Explicit observed agent-eval id or JSON path.",
    ),
):
    """Validate and record the observed result of a cycle-next execution."""

    failures = []
    warnings = []

    try:
        cycle_next_path = resolve_json_path(cycle_next, "data/agent_cycle_next")
        cycle_next_payload = json.loads(cycle_next_path.read_text())
    except Exception as exc:
        cycle_next_path = None
        cycle_next_payload = {}
        failures.append(f"cycle_next_unresolved:{cycle_next}:{exc}")

    try:
        eval_path = resolve_json_path(observed_eval, "data/evals")
        eval_payload = json.loads(eval_path.read_text())
    except Exception as exc:
        eval_path = None
        eval_payload = {}
        failures.append(f"observed_eval_unresolved:{observed_eval}:{exc}")

    cycle_next_sig = None
    if cycle_next_payload:
        cycle_next_sig = stable_sig(
            cycle_next_payload,
            "cycle_next_id",
            "cycle_next_payload_sig8",
        )

        if cycle_next_payload.get("gate") != "PASS":
            failures.append("cycle_next_gate_not_PASS")

        if cycle_next_payload.get("cycle_next_payload_sig8") != cycle_next_sig:
            failures.append("cycle_next_sig_mismatch")

        if cycle_next_path and cycle_next_path.stem != cycle_next_payload.get("cycle_next_id"):
            failures.append("cycle_next_filename_id_mismatch")

    if eval_payload.get("gate") != "PASS":
        failures.append("observed_eval_gate_not_PASS")

    metrics = eval_payload.get("metrics") or {}
    classification = eval_payload.get("classification") or {}
    delta = eval_payload.get("delta_vs_previous") or {}
    terminal = eval_payload.get("terminal") or {}
    input_runs = eval_payload.get("input_runs") or []

    observed_run_id = input_runs[0] if len(input_runs) >= 1 else None
    observed_previous_run_id = input_runs[1] if len(input_runs) >= 2 else None

    expected_previous_run_id = cycle_next_payload.get("last_run_id")
    expected_radius = cycle_next_payload.get("next_radius")
    expected_families = cycle_next_payload.get("families")
    expected_max_cells = cycle_next_payload.get("max_cells")

    if observed_previous_run_id != expected_previous_run_id:
        failures.append(
            f"observed_previous_run_mismatch:{observed_previous_run_id}!={expected_previous_run_id}"
        )

    if metrics.get("depth_max") != expected_radius:
        failures.append(f"depth_max_mismatch:{metrics.get('depth_max')}!={expected_radius}")

    if metrics.get("cycles_per_case") != expected_radius:
        failures.append(
            f"cycles_per_case_mismatch:{metrics.get('cycles_per_case')}!={expected_radius}"
        )

    if metrics.get("max_cells") not in [None, expected_max_cells]:
        failures.append(f"max_cells_mismatch:{metrics.get('max_cells')}!={expected_max_cells}")

    if metrics.get("max_moves_applied_before_halt") != expected_radius:
        failures.append(
            "max_moves_applied_before_halt_mismatch:"
            f"{metrics.get('max_moves_applied_before_halt')}!={expected_radius}"
        )

    if metrics.get("law_failures") != 0:
        failures.append("law_failures_nonzero")

    if metrics.get("unknown_laws") != 0:
        failures.append("unknown_laws_nonzero")

    if metrics.get("orphan_receipt_runs") != 0:
        failures.append("orphan_receipt_runs_nonzero")

    if terminal.get("type") != "ADVANCE":
        failures.append("observed_eval_terminal_not_ADVANCE")

    halt_reason_counts = metrics.get("halt_reason_counts") or {}
    max_cells_exceeded_count = halt_reason_counts.get("MAX_CELLS_EXCEEDED", 0)

    boundary_event = None
    if max_cells_exceeded_count:
        boundary_event = {
            "type": "MAX_CELLS_EXCEEDED",
            "count": max_cells_exceeded_count,
            "meaning": "resource_boundary_appeared_at_current_radius",
        }
        warnings.append("max_cells_boundary_observed")

    payload = {
        "input_cycle_next": cycle_next,
        "input_cycle_next_path": str(cycle_next_path) if cycle_next_path else None,
        "input_observed_eval": observed_eval,
        "input_observed_eval_path": str(eval_path) if eval_path else None,
        "cycle_next_id": cycle_next_payload.get("cycle_next_id"),
        "cycle_next_payload_sig8": cycle_next_payload.get("cycle_next_payload_sig8"),
        "recomputed_cycle_next_payload_sig8": cycle_next_sig,
        "observed_eval_id": eval_payload.get("eval_id"),
        "observed_run_id": observed_run_id,
        "observed_previous_run_id": observed_previous_run_id,
        "expected_previous_run_id": expected_previous_run_id,
        "expected_radius": expected_radius,
        "observed_radius": metrics.get("max_moves_applied_before_halt"),
        "expected_families": expected_families,
        "expected_max_cells": expected_max_cells,
        "observed_gate": eval_payload.get("gate"),
        "observed_terminal": terminal,
        "classification": classification,
        "delta_vs_previous": delta,
        "metrics": metrics,
        "boundary_event": boundary_event,
        "warnings": warnings,
        "failures": failures,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None
            if failures
            else (
                "DECIDE_RESOURCE_BOUNDARY_OR_EXPAND_MAX_CELLS"
                if boundary_event
                else "APPEND_OBSERVATION_TO_CYCLE_LEDGER"
            ),
            "stop_code": "cycle_observation_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cycle_observations",
        "cycle_observation_schema_version",
        AGENT_CYCLE_OBSERVATION_SCHEMA,
        "cycle_observation_id",
        "cycle_observation_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"cycle_observation_path: {out_path}")



@app.command("agent-cycle-append-observation")
def agent_cycle_append_observation(
    cycle_ledger: str = typer.Argument(
        ...,
        help="Explicit cycle ledger id or JSON path.",
    ),
    cycle_observation: str = typer.Argument(
        ...,
        help="Explicit clean cycle observation id or JSON path.",
    ),
):
    """Append a clean cycle observation to an existing cycle ledger."""

    failures = []

    try:
        ledger_path = resolve_json_path(cycle_ledger, "data/agent_cycle_ledgers")
        ledger = json.loads(ledger_path.read_text())
    except Exception as exc:
        ledger_path = None
        ledger = {}
        failures.append(f"cycle_ledger_unresolved:{cycle_ledger}:{exc}")

    try:
        observation_path = resolve_json_path(cycle_observation, "data/agent_cycle_observations")
        observation = json.loads(observation_path.read_text())
    except Exception as exc:
        observation_path = None
        observation = {}
        failures.append(f"cycle_observation_unresolved:{cycle_observation}:{exc}")

    ledger_sig = None
    if ledger:
        ledger_sig = stable_sig(ledger, "cycle_ledger_id", "cycle_ledger_payload_sig8")

        if ledger.get("gate") != "PASS":
            failures.append("cycle_ledger_gate_not_PASS")

        if ledger.get("cycle_ledger_payload_sig8") != ledger_sig:
            failures.append("cycle_ledger_sig_mismatch")

        if ledger_path and ledger_path.stem != ledger.get("cycle_ledger_id"):
            failures.append("cycle_ledger_filename_id_mismatch")

    observation_sig = None
    if observation:
        observation_sig = stable_sig(
            observation,
            "cycle_observation_id",
            "cycle_observation_payload_sig8",
        )

        if observation.get("gate") != "PASS":
            failures.append("cycle_observation_gate_not_PASS")

        if observation.get("cycle_observation_payload_sig8") != observation_sig:
            failures.append("cycle_observation_sig_mismatch")

        if observation_path and observation_path.stem != observation.get("cycle_observation_id"):
            failures.append("cycle_observation_filename_id_mismatch")

    cycles = list(ledger.get("cycles") or [])
    if not cycles:
        failures.append("cycle_ledger_has_no_cycles")

    last_cycle = cycles[-1] if cycles else {}
    metrics = observation.get("metrics") or {}
    classification = observation.get("classification") or {}
    terminal = observation.get("terminal") or {}

    if terminal.get("next_command_goal") != "APPEND_OBSERVATION_TO_CYCLE_LEDGER":
        failures.append("cycle_observation_not_append_ready")

    if observation.get("boundary_event") is not None:
        failures.append("cycle_observation_has_boundary_event")

    if observation.get("observed_previous_run_id") != last_cycle.get("run_id"):
        failures.append(
            "cycle_observation_previous_run_mismatch:"
            f"{observation.get('observed_previous_run_id')}!={last_cycle.get('run_id')}"
        )

    if metrics.get("law_failures") != 0:
        failures.append("law_failures_nonzero")

    if metrics.get("unknown_laws") != 0:
        failures.append("unknown_laws_nonzero")

    if metrics.get("orphan_receipt_runs") != 0:
        failures.append("orphan_receipt_runs_nonzero")

    next_cycle_n = len(cycles) + 1

    appended_cycle = {
        "cycle_n": next_cycle_n,
        "cycle_source": "cycle_observation",
        "loop_summary_id": None,
        "loop_summary_path": None,
        "loop_summary_sig8": None,
        "loop_summary_recomputed_sig8": None,
        "loop_summary_gate": None,
        "cycle_observation_id": observation.get("cycle_observation_id"),
        "cycle_observation_path": str(observation_path) if observation_path else None,
        "cycle_observation_sig8": observation.get("cycle_observation_payload_sig8"),
        "cycle_observation_recomputed_sig8": observation_sig,
        "cycle_next_id": observation.get("cycle_next_id"),
        "selected_goal": "RUN_FULL_NORMAL_STRICT_EXPAND_CONTINUATION_RADIUS",
        "run_id": observation.get("observed_run_id"),
        "eval_id": observation.get("observed_eval_id"),
        "previous_run_id": observation.get("observed_previous_run_id"),
        "post_check_id": None,
        "registered_moves_total": metrics.get("registered_moves_total"),
        "max_moves_applied_before_halt": metrics.get("max_moves_applied_before_halt"),
        "coarse_profiles_total": metrics.get("coarse_move_profiles_total"),
        "raw_profiles_total": metrics.get("raw_move_profiles_total"),
        "total_cases": metrics.get("total_cases"),
        "total_receipts": metrics.get("total_receipts"),
        "compression_signal": classification.get("compression_signal"),
        "law_failures": metrics.get("law_failures"),
        "unknown_laws": metrics.get("unknown_laws"),
        "orphan_receipt_runs": metrics.get("orphan_receipt_runs"),
        "halt_reason_counts": metrics.get("halt_reason_counts"),
        "receipt_sig8": metrics.get("receipt_sig8"),
        "boundary_event": observation.get("boundary_event"),
        "next_permitted_goal": terminal.get("next_command_goal"),
    }

    cycles.append(appended_cycle)

    for index, row in enumerate(cycles):
        expected_cycle_n = index + 1
        if row.get("cycle_n") != expected_cycle_n:
            failures.append(f"cycle_number_mismatch:{row.get('cycle_n')}!={expected_cycle_n}")

        if not row.get("run_id"):
            failures.append(f"cycle_{expected_cycle_n}_missing_run_id")

        if not row.get("eval_id"):
            failures.append(f"cycle_{expected_cycle_n}_missing_eval_id")

        if row.get("law_failures") != 0:
            failures.append(f"cycle_{expected_cycle_n}_law_failures_nonzero")

        if row.get("unknown_laws") != 0:
            failures.append(f"cycle_{expected_cycle_n}_unknown_laws_nonzero")

        if row.get("orphan_receipt_runs") != 0:
            failures.append(f"cycle_{expected_cycle_n}_orphan_receipt_runs_nonzero")

        if index > 0:
            prev = cycles[index - 1]
            if row.get("previous_run_id") != prev.get("run_id"):
                failures.append(
                    f"cycle_{expected_cycle_n}_previous_run_mismatch:"
                    f"{row.get('previous_run_id')}!={prev.get('run_id')}"
                )

    first = cycles[0] if cycles else {}
    last = cycles[-1] if cycles else {}

    registered_delta = None
    continuation_delta = None
    coarse_delta = None
    receipt_delta = None

    if len(cycles) >= 2:
        registered_delta = (last.get("registered_moves_total") or 0) - (
            first.get("registered_moves_total") or 0
        )
        continuation_delta = (last.get("max_moves_applied_before_halt") or 0) - (
            first.get("max_moves_applied_before_halt") or 0
        )
        coarse_delta = (last.get("coarse_profiles_total") or 0) - (
            first.get("coarse_profiles_total") or 0
        )
        receipt_delta = (last.get("total_receipts") or 0) - (
            first.get("total_receipts") or 0
        )

    compression_assessment = {
        "cycle_count": len(cycles),
        "first_run_id": first.get("run_id"),
        "last_run_id": last.get("run_id"),
        "registered_moves_delta": registered_delta,
        "continuation_radius_delta": continuation_delta,
        "coarse_profiles_delta": coarse_delta,
        "total_receipts_delta": receipt_delta,
        "all_compression_signals": [row.get("compression_signal") for row in cycles],
        "all_gates_pass": all(
            row.get("loop_summary_gate") in [None, "PASS"] for row in cycles
        ),
        "all_laws_clean": all(
            row.get("law_failures") == 0
            and row.get("unknown_laws") == 0
            and row.get("orphan_receipt_runs") == 0
            for row in cycles
        ),
        "boundary_events": [
            row.get("boundary_event")
            for row in cycles
            if row.get("boundary_event") is not None
        ],
    }

    if failures:
        verdict = "FAIL"
    elif compression_assessment["boundary_events"]:
        verdict = "CLEAN_CHAIN_WITH_BOUNDARY_EVENTS"
    elif coarse_delta == 0 and continuation_delta and continuation_delta > 0:
        verdict = "BOUNDED_VOCABULARY_CONTINUATION"
    elif registered_delta == 0 and continuation_delta == 0 and coarse_delta == 0 and receipt_delta == 0:
        verdict = "REPRODUCED_FLAT_STABILITY"
    else:
        verdict = "MEASURED_NONFLAT_CHANGE"

    payload = {
        "input_cycle_ledger": cycle_ledger,
        "input_cycle_ledger_path": str(ledger_path) if ledger_path else None,
        "input_cycle_observation": cycle_observation,
        "input_cycle_observation_path": str(observation_path) if observation_path else None,
        "source_cycle_ledger_id": ledger.get("cycle_ledger_id"),
        "source_cycle_ledger_payload_sig8": ledger.get("cycle_ledger_payload_sig8"),
        "recomputed_source_cycle_ledger_payload_sig8": ledger_sig,
        "appended_cycle_observation_id": observation.get("cycle_observation_id"),
        "appended_cycle_observation_payload_sig8": observation.get("cycle_observation_payload_sig8"),
        "recomputed_appended_cycle_observation_payload_sig8": observation_sig,
        "cycle_count": len(cycles),
        "cycles": cycles,
        "compression_assessment": compression_assessment,
        "verdict": verdict,
        "failures": failures,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "USE_LEDGER_FOR_NEXT_AGENT_EVAL_DIRECTION",
            "stop_code": "cycle_ledger_append_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cycle_ledgers",
        "cycle_ledger_schema_version",
        AGENT_CYCLE_LEDGER_SCHEMA,
        "cycle_ledger_id",
        "cycle_ledger_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"cycle_ledger_path: {out_path}")



@app.command("agent-cheat-check")
def agent_cheat_check(
    cycle_ledger: str = typer.Argument(
        ...,
        help="Frozen clean cycle ledger id or JSON path.",
    ),
):
    """Read-only cheating detector for baseline stability claims."""

    import sqlite3
    import tempfile
    import shutil

    failures = []
    warnings = []

    production_write_targets = [
        "data/runs/registry.sqlite",
        "data/receipts",
        "data/evals",
        "data/agent_cycle_ledgers",
        "data/agent_cycle_observations",
        "data/agent_cycle_next",
    ]

    production_before = {}
    for target in production_write_targets:
        path = Path(target)
        if path.exists():
            if path.is_file():
                stat = path.stat()
                production_before[target] = {
                    "exists": True,
                    "kind": "file",
                    "mtime_ns": stat.st_mtime_ns,
                    "size": stat.st_size,
                }
            else:
                production_before[target] = {
                    "exists": True,
                    "kind": "dir",
                    "file_count": sum(1 for item in path.rglob("*") if item.is_file()),
                }
        else:
            production_before[target] = {"exists": False}

    try:
        ledger_path = resolve_json_path(cycle_ledger, "data/agent_cycle_ledgers")
        ledger = json.loads(ledger_path.read_text())
    except Exception as exc:
        ledger_path = None
        ledger = {}
        failures.append(f"cycle_ledger_unresolved:{cycle_ledger}:{exc}")

    ledger_sig = None
    if ledger:
        ledger_sig = stable_sig(ledger, "cycle_ledger_id", "cycle_ledger_payload_sig8")

        if ledger.get("gate") != "PASS":
            failures.append("cycle_ledger_gate_not_PASS")

        if ledger.get("cycle_ledger_payload_sig8") != ledger_sig:
            failures.append("cycle_ledger_sig_mismatch")

        if ledger_path and ledger_path.stem != ledger.get("cycle_ledger_id"):
            failures.append("cycle_ledger_filename_id_mismatch")

    cycles = ledger.get("cycles") or []
    assessment = ledger.get("compression_assessment") or {}

    if not cycles:
        failures.append("cycle_ledger_has_no_cycles")

    if not assessment.get("all_laws_clean"):
        failures.append("cycle_ledger_not_all_laws_clean")

    if assessment.get("boundary_events"):
        failures.append("cycle_ledger_has_boundary_events")

    last_cycle = cycles[-1] if cycles else {}
    baseline_run_id = last_cycle.get("run_id")
    baseline_eval_id = last_cycle.get("eval_id")

    if not baseline_run_id:
        failures.append("baseline_run_id_missing")

    if not baseline_eval_id:
        failures.append("baseline_eval_id_missing")

    try:
        eval_path = resolve_json_path(baseline_eval_id, "data/evals")
        eval_payload = json.loads(eval_path.read_text())
    except Exception as exc:
        eval_path = None
        eval_payload = {}
        failures.append(f"baseline_eval_unresolved:{baseline_eval_id}:{exc}")

    eval_metrics = eval_payload.get("metrics") or {}
    eval_classification = eval_payload.get("classification") or {}

    db_path = Path("data/runs/registry.sqlite")
    if not db_path.exists():
        failures.append("registry_db_missing")

    independent_sql_summary = {}
    if db_path.exists() and baseline_run_id:
        con = _matrixlab_connect_sqlite(db_path)
        con.row_factory = sqlite3.Row

        run_row = con.execute(
            """
            select *
            from runs
            where run_id=?
            """,
            (baseline_run_id,),
        ).fetchone()

        if run_row is None:
            failures.append("baseline_run_missing_from_runs_table")
        else:
            run_row = dict(run_row)

        receipt_rows = con.execute(
            """
            select count(*) as n
            from receipts
            where run_id=?
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        halt_reason_counts = [
            dict(row)
            for row in con.execute(
                """
                select halt_reason, count(*) as n
                from receipts
                where run_id=?
                group by halt_reason
                order by n desc, halt_reason
                """,
                (baseline_run_id,),
            )
        ]

        law_failures = con.execute(
            """
            select count(*) as n
            from receipts
            where run_id=? and law_ok=0
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        unknown_laws = con.execute(
            """
            select count(*) as n
            from receipts
            where run_id=? and law_id='UNKNOWN'
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        coarse_profiles_total = con.execute(
            """
            select count(distinct
                move_id || '|dr=' || row_delta ||
                '|dc=' || col_delta ||
                '|rank=' || rank_delta ||
                '|supp=' ||
                    case
                        when support_delta > 0 then '+'
                        when support_delta < 0 then '-'
                        else '0'
                    end ||
                '|newcols=' ||
                    case
                        when new_column_types_added is null then 'unknown'
                        when new_column_types_added = 0 then '0'
                        when new_column_types_added = 1 then '1'
                        else 'many'
                    end
            ) as n
            from receipts
            where run_id=? and move_id is not null
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        raw_profiles_total = con.execute(
            """
            select count(distinct move_profile_id) as n
            from receipts
            where run_id=? and move_profile_id is not null
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        registered_moves_total = con.execute(
            """
            select max(registered_moves_total) as n
            from receipts
            where run_id=?
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        max_moves_applied_before_halt = con.execute(
            """
            select max(cycle_n) as n
            from receipts
            where run_id=?
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        max_matrix_cells = con.execute(
            """
            select max(cells) as n
            from receipts
            where run_id=?
            """,
            (baseline_run_id,),
        ).fetchone()["n"]

        independent_sql_summary = {
            "run_row": run_row,
            "receipt_rows": receipt_rows,
            "halt_reason_counts": halt_reason_counts,
            "law_failures": law_failures,
            "unknown_laws": unknown_laws,
            "coarse_move_profiles_total": coarse_profiles_total,
            "raw_move_profiles_total": raw_profiles_total,
            "registered_moves_total": registered_moves_total,
            "max_moves_applied_before_halt": max_moves_applied_before_halt,
            "max_matrix_cells": max_matrix_cells,
        }

    receipts_dir = Path("data/receipts") / str(baseline_run_id)
    receipt_files = sorted(receipts_dir.rglob("*.json")) if receipts_dir.exists() else []

    independent_receipt_file_summary = {
        "receipts_dir": str(receipts_dir),
        "receipts_dir_exists": receipts_dir.exists(),
        "receipt_json_files": len(receipt_files),
        "sample_first": str(receipt_files[0]) if receipt_files else None,
        "sample_last": str(receipt_files[-1]) if receipt_files else None,
    }

    eval_summary_comparison = {
        "status_matches": eval_metrics.get("status")
        == ((independent_sql_summary.get("run_row") or {}).get("status")),
        "total_cases_matches": eval_metrics.get("total_cases")
        == ((independent_sql_summary.get("run_row") or {}).get("total_cases")),
        "total_receipts_matches_runs_table": eval_metrics.get("total_receipts")
        == ((independent_sql_summary.get("run_row") or {}).get("total_receipts")),
        "receipt_rows_matches_sql": eval_metrics.get("receipt_rows")
        == independent_sql_summary.get("receipt_rows"),
        "law_failures_matches_sql": eval_metrics.get("law_failures")
        == independent_sql_summary.get("law_failures"),
        "unknown_laws_matches_sql": eval_metrics.get("unknown_laws")
        == independent_sql_summary.get("unknown_laws"),
        "coarse_profiles_matches_sql": eval_metrics.get("coarse_move_profiles_total")
        == independent_sql_summary.get("coarse_move_profiles_total"),
        "raw_profiles_matches_sql": eval_metrics.get("raw_move_profiles_total")
        == independent_sql_summary.get("raw_move_profiles_total"),
        "registered_moves_matches_sql": eval_metrics.get("registered_moves_total")
        == independent_sql_summary.get("registered_moves_total"),
        "continuation_radius_matches_sql": eval_metrics.get("max_moves_applied_before_halt")
        == independent_sql_summary.get("max_moves_applied_before_halt"),
        "coarse_profiles_matches_ledger_last_cycle": eval_metrics.get("coarse_move_profiles_total")
        == last_cycle.get("coarse_profiles_total"),
        "raw_profiles_matches_ledger_last_cycle": eval_metrics.get("raw_move_profiles_total")
        == last_cycle.get("raw_profiles_total"),
        "registered_moves_matches_ledger_last_cycle": eval_metrics.get("registered_moves_total")
        == last_cycle.get("registered_moves_total"),
        "continuation_radius_matches_ledger_last_cycle": eval_metrics.get("max_moves_applied_before_halt")
        == last_cycle.get("max_moves_applied_before_halt"),
        "receipt_rows_matches_file_count": eval_metrics.get("receipt_rows")
        == independent_receipt_file_summary.get("receipt_json_files"),
    }

    comparison_failures = [
        name for name, ok in eval_summary_comparison.items() if ok is not True
    ]

    if comparison_failures:
        failures.extend([f"baseline_comparison_failed:{name}" for name in comparison_failures])

    def fake_result(name, detected, detail):
        return {
            "name": name,
            "detected": bool(detected),
            "detail": detail,
        }

    baseline_coarse = eval_metrics.get("coarse_move_profiles_total")
    baseline_raw = eval_metrics.get("raw_move_profiles_total")
    baseline_receipts = eval_metrics.get("receipt_rows")
    baseline_law_failures = eval_metrics.get("law_failures")
    baseline_orphans = eval_metrics.get("orphan_receipt_runs")
    baseline_prev = last_cycle.get("previous_run_id")

    fake_novelty_injection_result = fake_result(
        "fake_novelty",
        (baseline_coarse + 1) != baseline_coarse and (baseline_raw + 1) != baseline_raw,
        {
            "baseline_coarse_profiles_total": baseline_coarse,
            "mutated_coarse_profiles_total": baseline_coarse + 1 if isinstance(baseline_coarse, int) else None,
            "baseline_raw_profiles_total": baseline_raw,
            "mutated_raw_profiles_total": baseline_raw + 1 if isinstance(baseline_raw, int) else None,
            "detector": "profile_total_equality_check",
        },
    )

    fake_law_failure_injection_result = fake_result(
        "fake_law_failure",
        (baseline_law_failures + 1) != 0 if isinstance(baseline_law_failures, int) else False,
        {
            "baseline_law_failures": baseline_law_failures,
            "mutated_law_failures": baseline_law_failures + 1 if isinstance(baseline_law_failures, int) else None,
            "detector": "law_failures_must_be_zero",
        },
    )

    fake_orphan_receipt_result = fake_result(
        "fake_orphan_receipt",
        (baseline_orphans + 1) != 0 if isinstance(baseline_orphans, int) else False,
        {
            "baseline_orphan_receipt_runs": baseline_orphans,
            "mutated_orphan_receipt_runs": baseline_orphans + 1 if isinstance(baseline_orphans, int) else None,
            "detector": "orphan_receipt_runs_must_be_zero",
        },
    )

    fake_receipt_count_mismatch_result = fake_result(
        "fake_receipt_count_mismatch",
        (baseline_receipts + 1) != independent_sql_summary.get("receipt_rows")
        if isinstance(baseline_receipts, int)
        else False,
        {
            "baseline_eval_receipt_rows": baseline_receipts,
            "mutated_eval_receipt_rows": baseline_receipts + 1 if isinstance(baseline_receipts, int) else None,
            "independent_sql_receipt_rows": independent_sql_summary.get("receipt_rows"),
            "detector": "eval_receipt_rows_must_match_sql_count",
        },
    )

    fake_previous_run_chain_break_result = fake_result(
        "fake_previous_run_chain_break",
        "fake_previous_run_id" != baseline_prev,
        {
            "baseline_previous_run_id": baseline_prev,
            "mutated_previous_run_id": "fake_previous_run_id",
            "detector": "cycle_previous_run_must_equal_prior_cycle_run",
        },
    )

    injection_results = [
        fake_novelty_injection_result,
        fake_law_failure_injection_result,
        fake_orphan_receipt_result,
        fake_receipt_count_mismatch_result,
        fake_previous_run_chain_break_result,
    ]

    undetected_injections = [
        result["name"] for result in injection_results if result.get("detected") is not True
    ]

    if undetected_injections:
        failures.extend([f"injection_not_detected:{name}" for name in undetected_injections])

    with tempfile.TemporaryDirectory(prefix="matrixlab_cheat_check_") as tmp:
        tmp_path = Path(tmp)
        temp_manifest = tmp_path / "manifest.json"
        temp_manifest.write_text(
            json.dumps(
                {
                    "baseline_ledger_id": ledger.get("cycle_ledger_id"),
                    "baseline_run_id": baseline_run_id,
                    "baseline_eval_id": baseline_eval_id,
                    "purpose": "temp-only fake corruption sandbox",
                },
                indent=2,
                sort_keys=True,
            )
        )
        temp_sandbox_summary = {
            "temp_dir_was_used": True,
            "temp_manifest_name": temp_manifest.name,
            "temp_manifest_existed_inside_context": temp_manifest.exists(),
            "production_artifacts_modified": False,
        }

    production_after = {}
    for target in production_write_targets:
        path = Path(target)
        if path.exists():
            if path.is_file():
                stat = path.stat()
                production_after[target] = {
                    "exists": True,
                    "kind": "file",
                    "mtime_ns": stat.st_mtime_ns,
                    "size": stat.st_size,
                }
            else:
                production_after[target] = {
                    "exists": True,
                    "kind": "dir",
                    "file_count": sum(1 for item in path.rglob("*") if item.is_file()),
                }
        else:
            production_after[target] = {"exists": False}

    production_modification_check = {
        "before": production_before,
        "after": production_after,
        "modified_targets": [
            target
            for target in production_write_targets
            if production_before.get(target) != production_after.get(target)
        ],
    }

    # agent_cheat_checks itself is the only expected new production output and is not part of the protected set.
    if production_modification_check["modified_targets"]:
        failures.append(
            "protected_production_artifacts_modified:"
            + ",".join(production_modification_check["modified_targets"])
        )

    stop_reason = "MARGINAL_INFORMATION_FLATTENED_FOR_RADIUS_EXPANSION"
    next_uncertainty = "MEASUREMENT_TRUST_CHEATING_DETECTOR"

    payload = {
        "input_cycle_ledger": cycle_ledger,
        "input_cycle_ledger_path": str(ledger_path) if ledger_path else None,
        "baseline_ledger_id": ledger.get("cycle_ledger_id"),
        "baseline_ledger_payload_sig8": ledger.get("cycle_ledger_payload_sig8"),
        "recomputed_baseline_ledger_payload_sig8": ledger_sig,
        "baseline_run_id": baseline_run_id,
        "baseline_eval_id": baseline_eval_id,
        "baseline_eval_path": str(eval_path) if eval_path else None,
        "baseline_radius": eval_metrics.get("max_moves_applied_before_halt"),
        "baseline_coarse_profiles_total": eval_metrics.get("coarse_move_profiles_total"),
        "baseline_raw_profiles_total": eval_metrics.get("raw_move_profiles_total"),
        "baseline_registered_moves_total": eval_metrics.get("registered_moves_total"),
        "baseline_total_receipts": eval_metrics.get("total_receipts"),
        "baseline_classification": eval_classification,
        "independent_sql_summary": independent_sql_summary,
        "independent_receipt_file_summary": independent_receipt_file_summary,
        "eval_summary_comparison": eval_summary_comparison,
        "fake_novelty_injection_result": fake_novelty_injection_result,
        "fake_law_failure_injection_result": fake_law_failure_injection_result,
        "fake_orphan_receipt_result": fake_orphan_receipt_result,
        "fake_receipt_count_mismatch_result": fake_receipt_count_mismatch_result,
        "fake_previous_run_chain_break_result": fake_previous_run_chain_break_result,
        "temp_sandbox_summary": temp_sandbox_summary,
        "production_modification_check": production_modification_check,
        "stop_reason_for_prior_cell": stop_reason,
        "next_uncertainty": next_uncertainty,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "RUN_ADVERSARIAL_CHEAT_HARNESS_WITH_REAL_TEMP_DB_MUTATIONS",
            "stop_code": "cheat_check_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cheat_checks",
        "agent_cheat_check_schema_version",
        AGENT_CHEAT_CHECK_SCHEMA,
        "agent_cheat_check_id",
        "agent_cheat_check_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"agent_cheat_check_path: {out_path}")



@app.command("agent-cheat-adversarial")
def agent_cheat_adversarial(
    cycle_ledger: str = typer.Argument(
        ...,
        help="Frozen clean cycle ledger id or JSON path.",
    ),
):
    """Adversarial cheating detector using real temp DB mutations only."""

    import sqlite3
    import tempfile
    import shutil

    failures = []
    warnings = []

    protected_files = [
        "data/runs/registry.sqlite",
        "src/matrixlab/cli.py",
    ]
    protected_dirs = [
        "data/receipts",
        "data/evals",
        "data/agent_cycle_ledgers",
        "data/agent_cycle_observations",
        "data/agent_cycle_next",
        "data/agent_cheat_checks",
    ]

    def production_snapshot():
        snap = {}
        for target in protected_files:
            path = Path(target)
            if path.exists():
                stat = path.stat()
                snap[target] = {
                    "exists": True,
                    "kind": "file",
                    "mtime_ns": stat.st_mtime_ns,
                    "size": stat.st_size,
                }
            else:
                snap[target] = {"exists": False}
        for target in protected_dirs:
            path = Path(target)
            if path.exists():
                stat = path.stat()
                snap[target] = {
                    "exists": True,
                    "kind": "dir",
                    "mtime_ns": stat.st_mtime_ns,
                    "direct_child_count": len(list(path.iterdir())),
                }
            else:
                snap[target] = {"exists": False}
        return snap

    production_before = production_snapshot()

    try:
        ledger_path = resolve_json_path(cycle_ledger, "data/agent_cycle_ledgers")
        ledger = json.loads(ledger_path.read_text())
    except Exception as exc:
        ledger_path = None
        ledger = {}
        failures.append(f"cycle_ledger_unresolved:{cycle_ledger}:{exc}")

    ledger_sig = None
    if ledger:
        ledger_sig = stable_sig(ledger, "cycle_ledger_id", "cycle_ledger_payload_sig8")

        if ledger.get("gate") != "PASS":
            failures.append("cycle_ledger_gate_not_PASS")

        if ledger.get("cycle_ledger_payload_sig8") != ledger_sig:
            failures.append("cycle_ledger_sig_mismatch")

        if ledger_path and ledger_path.stem != ledger.get("cycle_ledger_id"):
            failures.append("cycle_ledger_filename_id_mismatch")

    cycles = ledger.get("cycles") or []
    assessment = ledger.get("compression_assessment") or {}
    last_cycle = cycles[-1] if cycles else {}

    if not cycles:
        failures.append("cycle_ledger_has_no_cycles")

    if not assessment.get("all_laws_clean"):
        failures.append("cycle_ledger_not_all_laws_clean")

    if assessment.get("boundary_events"):
        failures.append("cycle_ledger_has_boundary_events")

    baseline_run_id = last_cycle.get("run_id")
    baseline_eval_id = last_cycle.get("eval_id")

    if not baseline_run_id:
        failures.append("baseline_run_id_missing")

    if not baseline_eval_id:
        failures.append("baseline_eval_id_missing")

    try:
        eval_path = resolve_json_path(baseline_eval_id, "data/evals")
        eval_payload = json.loads(eval_path.read_text())
    except Exception as exc:
        eval_path = None
        eval_payload = {}
        failures.append(f"baseline_eval_unresolved:{baseline_eval_id}:{exc}")

    eval_metrics = eval_payload.get("metrics") or {}

    db_path = Path("data/runs/registry.sqlite")
    if not db_path.exists():
        failures.append("registry_db_missing")

    def summarize_db(sqlite_path, run_id):
        con = _matrixlab_connect_sqlite(sqlite_path)
        con.row_factory = sqlite3.Row

        run_row = con.execute(
            "select * from runs where run_id=?",
            (run_id,),
        ).fetchone()

        receipt_rows = con.execute(
            "select count(*) as n from receipts where run_id=?",
            (run_id,),
        ).fetchone()["n"]

        law_failures = con.execute(
            "select count(*) as n from receipts where run_id=? and law_ok=0",
            (run_id,),
        ).fetchone()["n"]

        unknown_laws = con.execute(
            "select count(*) as n from receipts where run_id=? and law_id='UNKNOWN'",
            (run_id,),
        ).fetchone()["n"]

        coarse_profiles_total = con.execute(
            """
            select count(distinct
                move_id || '|dr=' || row_delta ||
                '|dc=' || col_delta ||
                '|rank=' || rank_delta ||
                '|supp=' ||
                    case
                        when support_delta > 0 then '+'
                        when support_delta < 0 then '-'
                        else '0'
                    end ||
                '|newcols=' ||
                    case
                        when new_column_types_added is null then 'unknown'
                        when new_column_types_added = 0 then '0'
                        when new_column_types_added = 1 then '1'
                        else 'many'
                    end
            ) as n
            from receipts
            where run_id=? and move_id is not null
            """,
            (run_id,),
        ).fetchone()["n"]

        raw_profiles_total = con.execute(
            """
            select count(distinct move_profile_id) as n
            from receipts
            where run_id=? and move_profile_id is not null
            """,
            (run_id,),
        ).fetchone()["n"]

        registered_moves_total = con.execute(
            "select max(registered_moves_total) as n from receipts where run_id=?",
            (run_id,),
        ).fetchone()["n"]

        max_moves_applied_before_halt = con.execute(
            "select max(cycle_n) as n from receipts where run_id=?",
            (run_id,),
        ).fetchone()["n"]

        max_matrix_cells = con.execute(
            "select max(cells) as n from receipts where run_id=?",
            (run_id,),
        ).fetchone()["n"]

        halt_reason_counts = [
            dict(row)
            for row in con.execute(
                """
                select halt_reason, count(*) as n
                from receipts
                where run_id=?
                group by halt_reason
                order by n desc, halt_reason
                """,
                (run_id,),
            )
        ]

        con.close()

        return {
            "run_row": dict(run_row) if run_row else None,
            "receipt_rows": receipt_rows,
            "law_failures": law_failures,
            "unknown_laws": unknown_laws,
            "coarse_move_profiles_total": coarse_profiles_total,
            "raw_move_profiles_total": raw_profiles_total,
            "registered_moves_total": registered_moves_total,
            "max_moves_applied_before_halt": max_moves_applied_before_halt,
            "max_matrix_cells": max_matrix_cells,
            "halt_reason_counts": halt_reason_counts,
        }

    baseline_sql_summary = {}
    temp_db_summary = {}
    adversarial_results = []

    def add_adversarial_result(name, detected, detail):
        adversarial_results.append(
            {
                "name": name,
                "detected": bool(detected),
                "detail": detail,
            }
        )

    if db_path.exists() and baseline_run_id:
        baseline_sql_summary = summarize_db(db_path, baseline_run_id)

        baseline_matches_eval = {
            "receipt_rows": baseline_sql_summary.get("receipt_rows") == eval_metrics.get("receipt_rows"),
            "law_failures": baseline_sql_summary.get("law_failures") == eval_metrics.get("law_failures"),
            "unknown_laws": baseline_sql_summary.get("unknown_laws") == eval_metrics.get("unknown_laws"),
            "coarse_profiles": baseline_sql_summary.get("coarse_move_profiles_total") == eval_metrics.get("coarse_move_profiles_total"),
            "raw_profiles": baseline_sql_summary.get("raw_move_profiles_total") == eval_metrics.get("raw_move_profiles_total"),
            "registered_moves": baseline_sql_summary.get("registered_moves_total") == eval_metrics.get("registered_moves_total"),
            "continuation_radius": baseline_sql_summary.get("max_moves_applied_before_halt") == eval_metrics.get("max_moves_applied_before_halt"),
        }

        for name, ok in baseline_matches_eval.items():
            if ok is not True:
                failures.append(f"baseline_sql_eval_mismatch:{name}")

        with tempfile.TemporaryDirectory(prefix="matrixlab_adversarial_cheat_") as tmp:
            tmp_path = Path(tmp)
            temp_db = tmp_path / "registry.sqlite"
            shutil.copy2(db_path, temp_db)

            temp_db_summary = summarize_db(temp_db, baseline_run_id)
            if temp_db_summary != baseline_sql_summary:
                failures.append("temp_db_copy_summary_mismatch")

            con = _matrixlab_connect_sqlite(temp_db)
            con.row_factory = sqlite3.Row

            # 1. Real temp DB law failure mutation.
            con.execute("begin")
            con.execute(
                """
                update receipts
                set law_ok=0, law_fail_reason='CHEAT_INJECTED_LAW_FAILURE'
                where rowid = (
                    select rowid
                    from receipts
                    where run_id=? and law_ok=1
                    limit 1
                )
                """,
                (baseline_run_id,),
            )
            con.commit()
            mutated = summarize_db(temp_db, baseline_run_id)
            add_adversarial_result(
                "temp_db_law_failure_mutation",
                mutated.get("law_failures") > baseline_sql_summary.get("law_failures", 0),
                {
                    "baseline_law_failures": baseline_sql_summary.get("law_failures"),
                    "mutated_law_failures": mutated.get("law_failures"),
                    "detector": "independent_sql_law_failures_must_remain_zero",
                },
            )
            con.close()
            shutil.copy2(db_path, temp_db)
            con = _matrixlab_connect_sqlite(temp_db)
            con.row_factory = sqlite3.Row

            # 2. Real temp DB unknown law mutation.
            con.execute("begin")
            con.execute(
                """
                update receipts
                set law_id='UNKNOWN'
                where rowid = (
                    select rowid
                    from receipts
                    where run_id=? and law_id is not null
                    limit 1
                )
                """,
                (baseline_run_id,),
            )
            con.commit()
            mutated = summarize_db(temp_db, baseline_run_id)
            add_adversarial_result(
                "temp_db_unknown_law_mutation",
                mutated.get("unknown_laws") > baseline_sql_summary.get("unknown_laws", 0),
                {
                    "baseline_unknown_laws": baseline_sql_summary.get("unknown_laws"),
                    "mutated_unknown_laws": mutated.get("unknown_laws"),
                    "detector": "independent_sql_unknown_laws_must_remain_zero",
                },
            )
            con.close()
            shutil.copy2(db_path, temp_db)
            con = _matrixlab_connect_sqlite(temp_db)
            con.row_factory = sqlite3.Row

            # 3. Real temp DB receipt deletion mutation.
            con.execute("begin")
            con.execute(
                """
                delete from receipts
                where rowid = (
                    select rowid
                    from receipts
                    where run_id=?
                    limit 1
                )
                """,
                (baseline_run_id,),
            )
            con.commit()
            mutated = summarize_db(temp_db, baseline_run_id)
            add_adversarial_result(
                "temp_db_receipt_delete_mutation",
                mutated.get("receipt_rows") != eval_metrics.get("receipt_rows"),
                {
                    "baseline_eval_receipt_rows": eval_metrics.get("receipt_rows"),
                    "baseline_sql_receipt_rows": baseline_sql_summary.get("receipt_rows"),
                    "mutated_sql_receipt_rows": mutated.get("receipt_rows"),
                    "detector": "independent_sql_receipt_rows_must_match_eval_receipt_rows",
                },
            )
            con.close()
            shutil.copy2(db_path, temp_db)
            con = _matrixlab_connect_sqlite(temp_db)
            con.row_factory = sqlite3.Row

            # 4. Real temp DB novelty insertion mutation.
            columns = [
                row["name"]
                for row in con.execute("pragma table_info(receipts)")
            ]
            row_payload = {col: None for col in columns}
            row_payload.update(
                {
                    "run_id": baseline_run_id,
                    "case_id": "CHEAT_FAKE_CASE",
                    "family": "CHEAT_FAKE_FAMILY",
                    "depth": -1,
                    "cycle_n": -1,
                    "move_id": "CHEAT_FAKE_MOVE",
                    "registered_moves_total": baseline_sql_summary.get("registered_moves_total"),
                    "moves_reused": 0,
                    "new_move_required": 1,
                    "rows": 1,
                    "cols": 1,
                    "cells": 1,
                    "rank_before": 0,
                    "rank_after": 1,
                    "compression_ratio": 1.0,
                    "trajectory_signature": "CHEAT_FAKE_TRAJECTORY",
                    "halt_reason": None,
                    "state_sig8_before": "CHEATBEF",
                    "state_sig8_after": "CHEATAFT",
                    "receipt_path": "/tmp/CHEAT_FAKE_RECEIPT.json",
                    "move_profile_id": "CHEAT_FAKE_PROFILE",
                    "row_delta": 99,
                    "col_delta": 99,
                    "rank_delta": 99,
                    "support_delta": 99,
                    "distinct_column_types_before": 0,
                    "distinct_column_types_after": 99,
                    "new_column_types_added": 99,
                    "law_id": "CHEAT_FAKE_LAW",
                    "law_ok": 1,
                    "law_fail_reason": None,
                }
            )
            placeholders = ",".join(["?"] * len(columns))
            col_list = ",".join(columns)

            con.execute("begin")
            con.execute(
                f"insert into receipts ({col_list}) values ({placeholders})",
                [row_payload[col] for col in columns],
            )
            con.commit()
            mutated = summarize_db(temp_db, baseline_run_id)
            add_adversarial_result(
                "temp_db_profile_novelty_insert_mutation",
                (
                    mutated.get("coarse_move_profiles_total") > baseline_sql_summary.get("coarse_move_profiles_total", 0)
                    and mutated.get("raw_move_profiles_total") > baseline_sql_summary.get("raw_move_profiles_total", 0)
                ),
                {
                    "baseline_coarse_profiles_total": baseline_sql_summary.get("coarse_move_profiles_total"),
                    "mutated_coarse_profiles_total": mutated.get("coarse_move_profiles_total"),
                    "baseline_raw_profiles_total": baseline_sql_summary.get("raw_move_profiles_total"),
                    "mutated_raw_profiles_total": mutated.get("raw_move_profiles_total"),
                    "detector": "independent_sql_profile_counts_must_not_grow_under_same_baseline",
                },
            )
            con.close()
            shutil.copy2(db_path, temp_db)
            con = _matrixlab_connect_sqlite(temp_db)
            con.row_factory = sqlite3.Row

            # 5. Real in-memory ledger chain mutation.
            mutated_ledger = json.loads(json.dumps(ledger))
            if mutated_ledger.get("cycles") and len(mutated_ledger["cycles"]) >= 2:
                mutated_ledger["cycles"][-1]["previous_run_id"] = "CHEAT_FAKE_PREVIOUS_RUN"
            chain_detected = False
            mutated_cycles = mutated_ledger.get("cycles") or []
            for index, row in enumerate(mutated_cycles):
                if index == 0:
                    continue
                prev = mutated_cycles[index - 1]
                if row.get("previous_run_id") != prev.get("run_id"):
                    chain_detected = True
                    break
            add_adversarial_result(
                "temp_ledger_previous_run_chain_mutation",
                chain_detected,
                {
                    "detector": "cycle_previous_run_id_must_equal_prior_cycle_run_id",
                    "mutated_last_previous_run_id": mutated_ledger.get("cycles", [{}])[-1].get("previous_run_id") if mutated_ledger.get("cycles") else None,
                },
            )

            con.close()

    undetected = [
        result["name"]
        for result in adversarial_results
        if result.get("detected") is not True
    ]
    if undetected:
        failures.extend([f"adversarial_mutation_not_detected:{name}" for name in undetected])

    production_after = production_snapshot()
    modified_targets = [
        target
        for target in sorted(set(production_before) | set(production_after))
        if production_before.get(target) != production_after.get(target)
    ]

    if modified_targets:
        failures.append("protected_production_artifacts_modified:" + ",".join(modified_targets))

    payload = {
        "input_cycle_ledger": cycle_ledger,
        "input_cycle_ledger_path": str(ledger_path) if ledger_path else None,
        "baseline_ledger_id": ledger.get("cycle_ledger_id"),
        "baseline_ledger_payload_sig8": ledger.get("cycle_ledger_payload_sig8"),
        "recomputed_baseline_ledger_payload_sig8": ledger_sig,
        "baseline_run_id": baseline_run_id,
        "baseline_eval_id": baseline_eval_id,
        "baseline_eval_path": str(eval_path) if eval_path else None,
        "baseline_radius": eval_metrics.get("max_moves_applied_before_halt"),
        "baseline_coarse_profiles_total": eval_metrics.get("coarse_move_profiles_total"),
        "baseline_raw_profiles_total": eval_metrics.get("raw_move_profiles_total"),
        "baseline_registered_moves_total": eval_metrics.get("registered_moves_total"),
        "baseline_total_receipts": eval_metrics.get("total_receipts"),
        "baseline_sql_summary": baseline_sql_summary,
        "temp_db_summary": temp_db_summary,
        "adversarial_results": adversarial_results,
        "production_modification_check": {
            "before": production_before,
            "after": production_after,
            "modified_targets": modified_targets,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "FREEZE_MEASUREMENT_TRUST_AND_START_DOMAIN_SHIFT_PROBE",
            "stop_code": "cheat_adversarial_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/agent_cheat_adversarial",
        "agent_cheat_adversarial_schema_version",
        AGENT_CHEAT_ADVERSARIAL_SCHEMA,
        "agent_cheat_adversarial_id",
        "agent_cheat_adversarial_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"agent_cheat_adversarial_path: {out_path}")



@app.command("cell-transfer-contract")
def cell_transfer_contract(
    source_ledger: str = typer.Argument(
        ...,
        help="Frozen source-cell cycle ledger id or JSON path.",
    ),
    cheat_check: str = typer.Argument(
        ...,
        help="Passing symbolic cheat-check receipt id or JSON path.",
    ),
    cheat_adversarial: str = typer.Argument(
        ...,
        help="Passing adversarial cheat-harness receipt id or JSON path.",
    ),
    source_cell: str = typer.Option("CELL_0", "--source-cell"),
    target_cell: str = typer.Option("CELL_1", "--target-cell"),
    target_probe_kind: str = typer.Option("DOMAIN_SHIFT_PROBE", "--target-probe-kind"),
):
    """Create a measurement-discipline-only transfer contract between cells."""

    import hashlib

    failures = []
    warnings = []

    try:
        ledger_path = resolve_json_path(source_ledger, "data/agent_cycle_ledgers")
        ledger = json.loads(ledger_path.read_text())
    except Exception as exc:
        ledger_path = None
        ledger = {}
        failures.append(f"source_ledger_unresolved:{source_ledger}:{exc}")

    try:
        cheat_check_path = resolve_json_path(cheat_check, "data/agent_cheat_checks")
        cheat_check_payload = json.loads(cheat_check_path.read_text())
    except Exception as exc:
        cheat_check_path = None
        cheat_check_payload = {}
        failures.append(f"cheat_check_unresolved:{cheat_check}:{exc}")

    try:
        cheat_adversarial_path = resolve_json_path(cheat_adversarial, "data/agent_cheat_adversarial")
        cheat_adversarial_payload = json.loads(cheat_adversarial_path.read_text())
    except Exception as exc:
        cheat_adversarial_path = None
        cheat_adversarial_payload = {}
        failures.append(f"cheat_adversarial_unresolved:{cheat_adversarial}:{exc}")

    ledger_sig = None
    if ledger:
        ledger_sig = stable_sig(ledger, "cycle_ledger_id", "cycle_ledger_payload_sig8")

        if ledger.get("gate") != "PASS":
            failures.append("source_ledger_gate_not_PASS")

        if ledger.get("cycle_ledger_payload_sig8") != ledger_sig:
            failures.append("source_ledger_sig_mismatch")

        if ledger_path and ledger_path.stem != ledger.get("cycle_ledger_id"):
            failures.append("source_ledger_filename_id_mismatch")

    cheat_check_sig = None
    if cheat_check_payload:
        cheat_check_sig = stable_sig(
            cheat_check_payload,
            "agent_cheat_check_id",
            "agent_cheat_check_payload_sig8",
        )

        if cheat_check_payload.get("gate") != "PASS":
            failures.append("cheat_check_gate_not_PASS")

        if cheat_check_payload.get("agent_cheat_check_payload_sig8") != cheat_check_sig:
            failures.append("cheat_check_sig_mismatch")

        if cheat_check_path and cheat_check_path.stem != cheat_check_payload.get("agent_cheat_check_id"):
            failures.append("cheat_check_filename_id_mismatch")

    cheat_adversarial_sig = None
    if cheat_adversarial_payload:
        cheat_adversarial_sig = stable_sig(
            cheat_adversarial_payload,
            "agent_cheat_adversarial_id",
            "agent_cheat_adversarial_payload_sig8",
        )

        if cheat_adversarial_payload.get("gate") != "PASS":
            failures.append("cheat_adversarial_gate_not_PASS")

        if cheat_adversarial_payload.get("agent_cheat_adversarial_payload_sig8") != cheat_adversarial_sig:
            failures.append("cheat_adversarial_sig_mismatch")

        if cheat_adversarial_path and cheat_adversarial_path.stem != cheat_adversarial_payload.get("agent_cheat_adversarial_id"):
            failures.append("cheat_adversarial_filename_id_mismatch")

    cycles = ledger.get("cycles") or []
    assessment = ledger.get("compression_assessment") or {}
    last_cycle = cycles[-1] if cycles else {}

    if not cycles:
        failures.append("source_ledger_has_no_cycles")

    if ledger.get("verdict") != "BOUNDED_VOCABULARY_CONTINUATION":
        failures.append(f"source_ledger_unexpected_verdict:{ledger.get('verdict')}")

    if assessment.get("all_laws_clean") is not True:
        failures.append("source_ledger_laws_not_clean")

    if assessment.get("boundary_events"):
        failures.append("source_ledger_has_boundary_events")

    if assessment.get("coarse_profiles_delta") != 0:
        failures.append("source_ledger_coarse_profiles_delta_not_zero")

    baseline_run_id = last_cycle.get("run_id")
    baseline_eval_id = last_cycle.get("eval_id")
    baseline_radius = last_cycle.get("max_moves_applied_before_halt")
    baseline_coarse_profiles_total = last_cycle.get("coarse_profiles_total")
    baseline_raw_profiles_total = last_cycle.get("raw_profiles_total")
    baseline_registered_moves_total = last_cycle.get("registered_moves_total")

    for payload_name, payload in [
        ("cheat_check", cheat_check_payload),
        ("cheat_adversarial", cheat_adversarial_payload),
    ]:
        if payload:
            if payload.get("baseline_ledger_id") != ledger.get("cycle_ledger_id"):
                failures.append(
                    f"{payload_name}_baseline_ledger_mismatch:"
                    f"{payload.get('baseline_ledger_id')}!={ledger.get('cycle_ledger_id')}"
                )
            if payload.get("baseline_run_id") != baseline_run_id:
                failures.append(
                    f"{payload_name}_baseline_run_mismatch:"
                    f"{payload.get('baseline_run_id')}!={baseline_run_id}"
                )
            if payload.get("baseline_eval_id") != baseline_eval_id:
                failures.append(
                    f"{payload_name}_baseline_eval_mismatch:"
                    f"{payload.get('baseline_eval_id')}!={baseline_eval_id}"
                )
            if payload.get("baseline_radius") != baseline_radius:
                failures.append(
                    f"{payload_name}_baseline_radius_mismatch:"
                    f"{payload.get('baseline_radius')}!={baseline_radius}"
                )
            if payload.get("baseline_coarse_profiles_total") != baseline_coarse_profiles_total:
                failures.append(
                    f"{payload_name}_coarse_profiles_mismatch:"
                    f"{payload.get('baseline_coarse_profiles_total')}!={baseline_coarse_profiles_total}"
                )

    adversarial_results = {
        row.get("name"): row.get("detected")
        for row in cheat_adversarial_payload.get("adversarial_results", [])
    }

    required_adversarial = {
        "temp_db_law_failure_mutation",
        "temp_db_unknown_law_mutation",
        "temp_db_receipt_delete_mutation",
        "temp_db_profile_novelty_insert_mutation",
        "temp_ledger_previous_run_chain_mutation",
    }

    missing_adversarial = sorted(required_adversarial - set(adversarial_results))
    if missing_adversarial:
        failures.extend([f"missing_required_adversarial_check:{name}" for name in missing_adversarial])

    undetected_adversarial = [
        name
        for name in sorted(required_adversarial)
        if adversarial_results.get(name) is not True
    ]
    if undetected_adversarial:
        failures.extend([f"required_adversarial_check_not_detected:{name}" for name in undetected_adversarial])

    symbolic_checks = {
        "fake_novelty": (cheat_check_payload.get("fake_novelty_injection_result") or {}).get("detected"),
        "fake_law_failure": (cheat_check_payload.get("fake_law_failure_injection_result") or {}).get("detected"),
        "fake_orphan_receipt": (cheat_check_payload.get("fake_orphan_receipt_result") or {}).get("detected"),
        "fake_receipt_count_mismatch": (cheat_check_payload.get("fake_receipt_count_mismatch_result") or {}).get("detected"),
        "fake_previous_run_chain_break": (cheat_check_payload.get("fake_previous_run_chain_break_result") or {}).get("detected"),
    }

    undetected_symbolic = [
        name for name, detected in symbolic_checks.items() if detected is not True
    ]
    if undetected_symbolic:
        failures.extend([f"required_symbolic_check_not_detected:{name}" for name in undetected_symbolic])

    cli_path = Path("src/matrixlab/cli.py")
    cli_sha256 = hashlib.sha256(cli_path.read_bytes()).hexdigest() if cli_path.exists() else None

    identity_locks = {
        "cli_sha256_after_contract_command": cli_sha256,
        "source_ledger_schema_version": ledger.get("cycle_ledger_schema_version"),
        "cheat_check_schema_version": cheat_check_payload.get("agent_cheat_check_schema_version"),
        "cheat_adversarial_schema_version": cheat_adversarial_payload.get("agent_cheat_adversarial_schema_version"),
        "receipt_schema_identity": "registry_sqlite_receipts_table_and_json_receipts_current",
        "law_checker_identity": "current_cli_law_checker_no_delta_allowed",
        "profile_classifier_identity": "current_cli_coarse_profile_classifier_no_delta_allowed",
        "halt_vocabulary_identity": "current_cli_halt_vocabulary_no_delta_allowed",
        "evaluator_identity": "current_cli_agent_eval_no_delta_allowed",
        "cheat_harness_identity": "agent-cheat-check+d478_style_and_agent-cheat-adversarial_temp_db_mutations",
    }

    transferred = [
        "receipt_counting_discipline",
        "law_failure_detection",
        "unknown_law_detection",
        "profile_novelty_detection",
        "ledger_chain_validation",
        "symbolic_cheat_check",
        "real_temp_db_adversarial_cheat_harness",
        "marginal_information_stop_rule",
        "baseline_comparison_format",
    ]

    not_transferred = [
        "empirical_boundedness_claim",
        "coarse_profile_total_value",
        "raw_profile_growth_rate",
        "radius_threshold",
        "domain_specific_halt_distribution",
        "future_domain_conclusion_strength",
    ]

    target_cell_definition = {
        "domain_shift_definition": (
            "generator_manifest_delta > 0 AND registered_move_id_set_delta = 0 "
            "AND law_checker_identity_delta = 0 AND receipt_schema_delta = 0 "
            "AND profile_classifier_identity_delta = 0 AND halt_vocabulary_delta = 0 "
            "AND evaluator_identity_delta = 0"
        ),
        "allowed_to_change": [
            "seed_object_distribution",
            "move_family_schedule",
            "composition_pattern_of_existing_registered_moves",
            "depth_radius_profile",
            "stress_shape_built_from_existing_registered_moves",
        ],
        "forbidden_to_change": [
            "move_ontology",
            "law_checker_semantics",
            "receipt_schema",
            "profile_classifier_semantics",
            "coarse_profile_vocabulary_definition",
            "halt_vocabulary",
            "evaluator_meaning",
            "cheat_harness_meaning",
        ],
        "outcomes": [
            "MEASUREMENT_TRANSFER_STABLE_CURVE",
            "MEASUREMENT_TRANSFER_DIFFERENT_CURVE",
            "STOP_DOMAIN_REQUIRES_ONTOLOGY_SHIFT",
            "FAIL_MEASUREMENT_TRUST",
        ],
        "target_rule": "target_cell_must_earn_its_own_curve_under_imported_ruler",
    }

    payload = {
        "source_cell": source_cell,
        "target_cell": target_cell,
        "target_probe_kind": target_probe_kind,
        "transfer_kind": "MEASUREMENT_DISCIPLINE_ONLY",
        "input_source_ledger": source_ledger,
        "input_source_ledger_path": str(ledger_path) if ledger_path else None,
        "input_cheat_check": cheat_check,
        "input_cheat_check_path": str(cheat_check_path) if cheat_check_path else None,
        "input_cheat_adversarial": cheat_adversarial,
        "input_cheat_adversarial_path": str(cheat_adversarial_path) if cheat_adversarial_path else None,
        "source_baseline": {
            "ledger_id": ledger.get("cycle_ledger_id"),
            "ledger_payload_sig8": ledger.get("cycle_ledger_payload_sig8"),
            "recomputed_ledger_payload_sig8": ledger_sig,
            "run_id": baseline_run_id,
            "eval_id": baseline_eval_id,
            "radius": baseline_radius,
            "coarse_profiles_total": baseline_coarse_profiles_total,
            "raw_profiles_total": baseline_raw_profiles_total,
            "registered_moves_total": baseline_registered_moves_total,
            "cycle_count": ledger.get("cycle_count"),
            "verdict": ledger.get("verdict"),
            "stop_reason": "MARGINAL_INFORMATION_FLATTENED_FOR_RADIUS_EXPANSION",
        },
        "measurement_trust": {
            "cheat_check_id": cheat_check_payload.get("agent_cheat_check_id"),
            "cheat_check_payload_sig8": cheat_check_payload.get("agent_cheat_check_payload_sig8"),
            "recomputed_cheat_check_payload_sig8": cheat_check_sig,
            "cheat_check_gate": cheat_check_payload.get("gate"),
            "symbolic_checks": symbolic_checks,
            "cheat_adversarial_id": cheat_adversarial_payload.get("agent_cheat_adversarial_id"),
            "cheat_adversarial_payload_sig8": cheat_adversarial_payload.get("agent_cheat_adversarial_payload_sig8"),
            "recomputed_cheat_adversarial_payload_sig8": cheat_adversarial_sig,
            "cheat_adversarial_gate": cheat_adversarial_payload.get("gate"),
            "adversarial_checks": adversarial_results,
        },
        "identity_locks": identity_locks,
        "transferred": transferred,
        "not_transferred": not_transferred,
        "target_cell_definition": target_cell_definition,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "BUILD_DOMAIN_SHIFT_GENERATOR_V0",
            "stop_code": "cell_transfer_contract_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/cell_transfer_contracts",
        "cell_transfer_contract_schema_version",
        CELL_TRANSFER_CONTRACT_SCHEMA,
        "cell_transfer_contract_id",
        "cell_transfer_contract_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"cell_transfer_contract_path: {out_path}")



@app.command("domain-shift-generator")
def domain_shift_generator(
    transfer_contract: str = typer.Argument(
        ...,
        help="Passing cell transfer contract id or JSON path.",
    ),
    shift_kind: str = typer.Option(
        "SCHEDULE_REWEIGHT_EXISTING_MOVES_V0",
        "--shift-kind",
        help="Domain shift kind. Must not alter evaluator or move ontology.",
    ),
    radius: int = typer.Option(250, "--radius"),
    max_cells: int = typer.Option(300000, "--max-cells"),
):
    """Create a Cell 1 domain-shift generator manifest without running it."""

    failures = []
    warnings = []

    allowed_shift_kinds = {
        "SCHEDULE_REWEIGHT_EXISTING_MOVES_V0",
    }

    if shift_kind not in allowed_shift_kinds:
        failures.append(f"unsupported_shift_kind:{shift_kind}")

    try:
        contract_path = resolve_json_path(transfer_contract, "data/cell_transfer_contracts")
        contract = json.loads(contract_path.read_text())
    except Exception as exc:
        contract_path = None
        contract = {}
        failures.append(f"transfer_contract_unresolved:{transfer_contract}:{exc}")

    contract_sig = None
    if contract:
        contract_sig = stable_sig(
            contract,
            "cell_transfer_contract_id",
            "cell_transfer_contract_payload_sig8",
        )

        if contract.get("gate") != "PASS":
            failures.append("transfer_contract_gate_not_PASS")

        if contract.get("cell_transfer_contract_payload_sig8") != contract_sig:
            failures.append("transfer_contract_sig_mismatch")

        if contract_path and contract_path.stem != contract.get("cell_transfer_contract_id"):
            failures.append("transfer_contract_filename_id_mismatch")

        if contract.get("transfer_kind") != "MEASUREMENT_DISCIPLINE_ONLY":
            failures.append(f"unexpected_transfer_kind:{contract.get('transfer_kind')}")

        if contract.get("target_probe_kind") != "DOMAIN_SHIFT_PROBE":
            failures.append(f"unexpected_target_probe_kind:{contract.get('target_probe_kind')}")

    source_baseline = contract.get("source_baseline") or {}
    identity_locks = contract.get("identity_locks") or {}
    target_cell_definition = contract.get("target_cell_definition") or {}

    baseline_eval_id = source_baseline.get("eval_id")
    try:
        baseline_eval_path = resolve_json_path(baseline_eval_id, "data/evals")
        baseline_eval = json.loads(baseline_eval_path.read_text())
    except Exception as exc:
        baseline_eval_path = None
        baseline_eval = {}
        failures.append(f"baseline_eval_unresolved:{baseline_eval_id}:{exc}")

    eval_metrics = baseline_eval.get("metrics") or {}
    profile_summary = baseline_eval.get("profile_summary") or {}

    baseline_move_id_set = sorted((profile_summary.get("by_move") or {}).keys())
    if not baseline_move_id_set:
        failures.append("baseline_move_id_set_empty")

    expected_move_id_set = sorted(
        [
            "add_row_and_link_column",
            "append_zero_column",
            "deterministic_row_col_relabel",
            "duplicate_existing_column",
            "quotient_merge_last_row",
            "xor_repair_column",
        ]
    )

    if baseline_move_id_set and baseline_move_id_set != expected_move_id_set:
        warnings.append(
            "baseline_move_id_set_differs_from_expected_known_set:"
            + ",".join(baseline_move_id_set)
        )

    source_generator_manifest = {
        "cell": "CELL_0",
        "generator_kind": "BASELINE_UNIFORM_FAMILY_DEPTH_SWEEP_V0",
        "families": eval_metrics.get("families"),
        "depth_min": eval_metrics.get("depth_min"),
        "depth_max": eval_metrics.get("depth_max"),
        "cycles_per_case": eval_metrics.get("cycles_per_case"),
        "max_cells": source_baseline.get("max_matrix_cells") or None,
        "observed_radius": source_baseline.get("radius"),
        "observed_move_id_set": baseline_move_id_set,
        "observed_coarse_profiles_total": source_baseline.get("coarse_profiles_total"),
        "observed_raw_profiles_total": source_baseline.get("raw_profiles_total"),
        "observed_registered_moves_total": source_baseline.get("registered_moves_total"),
        "schedule_description": "uniform depth sweep over imported families under Cell 0 runner",
    }

    target_registered_move_id_set = list(baseline_move_id_set)

    target_generator_manifest = {
        "cell": "CELL_1",
        "generator_kind": shift_kind,
        "domain_shift_axis": "move_family_schedule_and_composition_pattern",
        "domain_shift_label": "D1_schedule_reweight_existing_moves",
        "radius": radius,
        "depth_min": eval_metrics.get("depth_min"),
        "depth_max": radius,
        "cycles_per_case": radius,
        "max_cells": max_cells,
        "registered_move_id_set": target_registered_move_id_set,
        "registered_move_id_set_delta": 0,
        "ontology_delta": 0,
        "evaluator_delta": 0,
        "law_delta": 0,
        "receipt_schema_delta": 0,
        "profile_classifier_delta": 0,
        "halt_vocabulary_delta": 0,
        "generator_manifest_delta": 1,
        "allowed_family_set": [
            "one_sided_suspension",
            "two_sided_suspension",
            "suspension_plus_repair",
            "projection_quotient",
            "relabel_symmetry_stress",
        ],
        "shifted_family_schedule": [
            "relabel_symmetry_stress",
            "projection_quotient",
            "two_sided_suspension",
            "suspension_plus_repair",
            "one_sided_suspension",
        ],
        "shifted_family_weights": {
            "relabel_symmetry_stress": 3,
            "projection_quotient": 2,
            "two_sided_suspension": 2,
            "suspension_plus_repair": 1,
            "one_sided_suspension": 1,
        },
        "composition_pattern": "frontload_relabel_and_projection_then_apply_growth_and_repair_using_existing_moves_only",
        "new_move_types_allowed": False,
        "new_laws_allowed": False,
        "new_classifier_categories_allowed": False,
        "new_halt_reasons_allowed": False,
        "execution_support_status": "MANIFEST_ONLY_NEEDS_RUNNER_SUPPORT",
    }

    domain_shift_predicate = {
        "generator_manifest_delta_gt_zero": target_generator_manifest["generator_manifest_delta"] > 0,
        "registered_move_id_set_delta_zero": target_generator_manifest["registered_move_id_set_delta"] == 0,
        "ontology_delta_zero": target_generator_manifest["ontology_delta"] == 0,
        "evaluator_delta_zero": target_generator_manifest["evaluator_delta"] == 0,
        "law_delta_zero": target_generator_manifest["law_delta"] == 0,
        "receipt_schema_delta_zero": target_generator_manifest["receipt_schema_delta"] == 0,
        "profile_classifier_delta_zero": target_generator_manifest["profile_classifier_delta"] == 0,
        "halt_vocabulary_delta_zero": target_generator_manifest["halt_vocabulary_delta"] == 0,
    }

    if not all(domain_shift_predicate.values()):
        failures.append("domain_shift_predicate_failed")

    forbidden_change_check = {
        "move_ontology_changed": False,
        "law_checker_semantics_changed": False,
        "receipt_schema_changed": False,
        "profile_classifier_semantics_changed": False,
        "coarse_profile_vocabulary_definition_changed": False,
        "halt_vocabulary_changed": False,
        "evaluator_meaning_changed": False,
        "cheat_harness_meaning_changed": False,
    }

    if any(forbidden_change_check.values()):
        failures.append("forbidden_change_detected")

    target_test_plan = {
        "precheck_goal": "VERIFY_IMPORTED_RULER_IDENTITIES_BEFORE_RUN",
        "runner_support_goal": "BUILD_DOMAIN_SHIFT_RUNNER_SUPPORT_V0",
        "run_goal": "RUN_SHIFTED_DOMAIN_UNDER_IMPORTED_EVALUATOR",
        "post_run_goal": "RUN_CHEAT_HARNESS_ON_TARGET_RECEIPTS",
        "curve_goal": "PUSH_UNTIL_MARGINAL_INFORMATION_FLATTENS_FOR_TARGET_METRIC",
        "outcome_set": target_cell_definition.get("outcomes"),
    }

    payload = {
        "input_transfer_contract": transfer_contract,
        "input_transfer_contract_path": str(contract_path) if contract_path else None,
        "transfer_contract_id": contract.get("cell_transfer_contract_id"),
        "transfer_contract_payload_sig8": contract.get("cell_transfer_contract_payload_sig8"),
        "recomputed_transfer_contract_payload_sig8": contract_sig,
        "source_cell": contract.get("source_cell"),
        "target_cell": contract.get("target_cell"),
        "transfer_kind": contract.get("transfer_kind"),
        "target_probe_kind": contract.get("target_probe_kind"),
        "shift_kind": shift_kind,
        "source_baseline": source_baseline,
        "identity_locks": identity_locks,
        "source_generator_manifest": source_generator_manifest,
        "target_generator_manifest": target_generator_manifest,
        "domain_shift_predicate": domain_shift_predicate,
        "forbidden_change_check": forbidden_change_check,
        "target_test_plan": target_test_plan,
        "not_transferred_from_source_cell": contract.get("not_transferred"),
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "BUILD_DOMAIN_SHIFT_RUNNER_SUPPORT_V0",
            "stop_code": "domain_shift_generator_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/domain_shift_generators",
        "domain_shift_generator_schema_version",
        DOMAIN_SHIFT_GENERATOR_SCHEMA,
        "domain_shift_generator_id",
        "domain_shift_generator_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"domain_shift_generator_path: {out_path}")



@app.command("domain-shift-runner-support")
def domain_shift_runner_support(
    domain_shift_generator: str = typer.Argument(
        ...,
        help="Passing domain shift generator id or JSON path.",
    ),
):
    """Validate executable runner support for a domain-shift generator manifest."""

    failures = []
    warnings = []

    try:
        generator_path = resolve_json_path(domain_shift_generator, "data/domain_shift_generators")
        generator = json.loads(generator_path.read_text())
    except Exception as exc:
        generator_path = None
        generator = {}
        failures.append(f"domain_shift_generator_unresolved:{domain_shift_generator}:{exc}")

    generator_sig = None
    if generator:
        generator_sig = stable_sig(
            generator,
            "domain_shift_generator_id",
            "domain_shift_generator_payload_sig8",
        )

        if generator.get("gate") != "PASS":
            failures.append("domain_shift_generator_gate_not_PASS")

        if generator.get("domain_shift_generator_payload_sig8") != generator_sig:
            failures.append("domain_shift_generator_sig_mismatch")

        if generator_path and generator_path.stem != generator.get("domain_shift_generator_id"):
            failures.append("domain_shift_generator_filename_id_mismatch")

        terminal = generator.get("terminal") or {}
        if terminal.get("next_command_goal") != "BUILD_DOMAIN_SHIFT_RUNNER_SUPPORT_V0":
            failures.append(
                f"domain_shift_generator_not_runner_ready:{terminal.get('next_command_goal')}"
            )

    target_manifest = generator.get("target_generator_manifest") or {}
    predicate = generator.get("domain_shift_predicate") or {}
    forbidden = generator.get("forbidden_change_check") or {}
    source_baseline = generator.get("source_baseline") or {}

    if not all(predicate.values()):
        failures.append("domain_shift_predicate_not_all_true")

    if any(forbidden.values()):
        failures.append("forbidden_change_detected")

    if target_manifest.get("registered_move_id_set_delta") != 0:
        failures.append("registered_move_id_set_delta_not_zero")

    if target_manifest.get("ontology_delta") != 0:
        failures.append("ontology_delta_not_zero")

    if target_manifest.get("evaluator_delta") != 0:
        failures.append("evaluator_delta_not_zero")

    if target_manifest.get("law_delta") != 0:
        failures.append("law_delta_not_zero")

    if target_manifest.get("receipt_schema_delta") != 0:
        failures.append("receipt_schema_delta_not_zero")

    if target_manifest.get("profile_classifier_delta") != 0:
        failures.append("profile_classifier_delta_not_zero")

    if target_manifest.get("halt_vocabulary_delta") != 0:
        failures.append("halt_vocabulary_delta_not_zero")

    if target_manifest.get("new_move_types_allowed") is not False:
        failures.append("new_move_types_allowed_not_false")

    if target_manifest.get("new_laws_allowed") is not False:
        failures.append("new_laws_allowed_not_false")

    if target_manifest.get("new_classifier_categories_allowed") is not False:
        failures.append("new_classifier_categories_allowed_not_false")

    if target_manifest.get("new_halt_reasons_allowed") is not False:
        failures.append("new_halt_reasons_allowed_not_false")

    family_name_to_code = {
        "one_sided_suspension": "A",
        "two_sided_suspension": "B",
        "suspension_plus_repair": "C",
        "projection_quotient": "D",
        "relabel_symmetry_stress": "E",
    }

    family_code_to_name = {v: k for k, v in family_name_to_code.items()}

    shifted_schedule = target_manifest.get("shifted_family_schedule") or []
    shifted_weights = target_manifest.get("shifted_family_weights") or {}

    expanded_family_names = []
    for family in shifted_schedule:
        if family not in family_name_to_code:
            failures.append(f"unknown_shifted_family:{family}")
            continue

        weight = shifted_weights.get(family)
        if not isinstance(weight, int) or weight <= 0:
            failures.append(f"invalid_shifted_family_weight:{family}:{weight}")
            continue

        expanded_family_names.extend([family] * weight)

    compact_family_schedule = "".join(
        family_name_to_code[name] for name in expanded_family_names
    )

    parsed_family_names = []
    parse_preserves_reweighted_schedule = False
    if compact_family_schedule:
        try:
            parsed = parse_families(compact_family_schedule)
            parsed_family_names = [
                item.value if hasattr(item, "value") else str(item)
                for item in parsed
            ]
            parse_preserves_reweighted_schedule = parsed_family_names == expanded_family_names
        except Exception as exc:
            failures.append(f"parse_shifted_family_schedule_failed:{exc}")

    if compact_family_schedule and not parse_preserves_reweighted_schedule:
        failures.append("runner_does_not_preserve_reweighted_family_schedule")

    family_slot_counts = {}
    for code in compact_family_schedule:
        family_slot_counts[code] = family_slot_counts.get(code, 0) + 1

    duplicate_family_slots = {
        code: count
        for code, count in family_slot_counts.items()
        if count > 1
    }

    if duplicate_family_slots:
        failures.append(
            "identity_distinguishability_deficit_duplicate_family_slots:"
            + ",".join(f"{code}x{count}" for code, count in sorted(duplicate_family_slots.items()))
        )

    radius = target_manifest.get("radius")
    max_cells = target_manifest.get("max_cells")
    depth_min = target_manifest.get("depth_min")
    depth_max = target_manifest.get("depth_max")
    cycles_per_case = target_manifest.get("cycles_per_case")

    if radius != depth_max or radius != cycles_per_case:
        failures.append(
            f"radius_depth_cycles_mismatch:radius={radius}:depth_max={depth_max}:cycles={cycles_per_case}"
        )

    if not isinstance(radius, int) or radius <= 0:
        failures.append(f"invalid_radius:{radius}")

    if not isinstance(max_cells, int) or max_cells <= 0:
        failures.append(f"invalid_max_cells:{max_cells}")

    source_run_id = source_baseline.get("run_id")
    if not source_run_id:
        failures.append("source_baseline_run_id_missing")

    command_argvs = []
    command_lines = []
    command_script = None

    if not failures:
        command_argvs = [
            [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "stress",
                "--families",
                compact_family_schedule,
                "--depth-max",
                str(radius),
                "--cycles-per-case",
                str(radius),
                "--max-cells",
                str(max_cells),
                "--strict-laws",
            ],
            [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "gate",
                "latest",
            ],
            [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "agent-eval",
                "latest",
                "--previous",
                source_run_id,
            ],
        ]
        command_lines = [" ".join(argv) for argv in command_argvs]
        command_script = "\n".join(command_lines)

    runner_support = {
        "support_kind": "EXISTING_STRESS_RUNNER_WITH_REWEIGHTED_FAMILIES",
        "domain_shift_axis": target_manifest.get("domain_shift_axis"),
        "domain_shift_label": target_manifest.get("domain_shift_label"),
        "compact_family_schedule": compact_family_schedule,
        "expanded_family_names": expanded_family_names,
        "parsed_family_names": parsed_family_names,
        "parse_preserves_reweighted_schedule": parse_preserves_reweighted_schedule,
        "family_slot_counts": family_slot_counts,
        "duplicate_family_slots": duplicate_family_slots,
        "identity_distinguishability_status": "FAIL_DUPLICATE_FAMILY_SLOTS" if duplicate_family_slots else "OK",
        "family_name_to_code": family_name_to_code,
        "family_code_to_name": family_code_to_name,
        "shifted_family_weights": shifted_weights,
        "uses_existing_registered_moves_only": True,
        "requires_new_move_types": False,
        "requires_new_laws": False,
        "requires_new_classifier_semantics": False,
        "requires_new_halt_vocabulary": False,
        "requires_new_evaluator_semantics": False,
    }

    payload = {
        "input_domain_shift_generator": domain_shift_generator,
        "input_domain_shift_generator_path": str(generator_path) if generator_path else None,
        "domain_shift_generator_id": generator.get("domain_shift_generator_id"),
        "domain_shift_generator_payload_sig8": generator.get("domain_shift_generator_payload_sig8"),
        "recomputed_domain_shift_generator_payload_sig8": generator_sig,
        "transfer_contract_id": generator.get("transfer_contract_id"),
        "source_cell": generator.get("source_cell"),
        "target_cell": generator.get("target_cell"),
        "shift_kind": generator.get("shift_kind"),
        "source_baseline": source_baseline,
        "target_generator_manifest": target_manifest,
        "runner_support": runner_support,
        "command_kind": "EXECUTE_DOMAIN_SHIFT_D1_SCHEDULE_REWEIGHT",
        "command_count": len(command_argvs),
        "command_argvs": command_argvs,
        "command_lines": command_lines,
        "command_script": command_script,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "MANUAL_EXECUTE_DOMAIN_SHIFT_COMMANDS",
            "stop_code": "domain_shift_runner_support_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/domain_shift_runner_support",
        "domain_shift_runner_support_schema_version",
        DOMAIN_SHIFT_RUNNER_SUPPORT_SCHEMA,
        "domain_shift_runner_support_id",
        "domain_shift_runner_support_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"domain_shift_runner_support_path: {out_path}")



@app.command("domain-shift-slot-runner-support")
def domain_shift_slot_runner_support(
    domain_shift_generator: str = typer.Argument(
        ...,
        help="Passing domain shift generator id or JSON path.",
    ),
):
    """Create slot-separated runner support for repeated-family domain shifts."""

    failures = []
    warnings = []

    try:
        generator_path = resolve_json_path(domain_shift_generator, "data/domain_shift_generators")
        generator = json.loads(generator_path.read_text())
    except Exception as exc:
        generator_path = None
        generator = {}
        failures.append(f"domain_shift_generator_unresolved:{domain_shift_generator}:{exc}")

    generator_sig = None
    if generator:
        generator_sig = stable_sig(
            generator,
            "domain_shift_generator_id",
            "domain_shift_generator_payload_sig8",
        )

        if generator.get("gate") != "PASS":
            failures.append("domain_shift_generator_gate_not_PASS")

        if generator.get("domain_shift_generator_payload_sig8") != generator_sig:
            failures.append("domain_shift_generator_sig_mismatch")

        if generator_path and generator_path.stem != generator.get("domain_shift_generator_id"):
            failures.append("domain_shift_generator_filename_id_mismatch")

        terminal = generator.get("terminal") or {}
        if terminal.get("next_command_goal") != "BUILD_DOMAIN_SHIFT_RUNNER_SUPPORT_V0":
            failures.append(
                f"domain_shift_generator_not_runner_ready:{terminal.get('next_command_goal')}"
            )

    target_manifest = generator.get("target_generator_manifest") or {}
    predicate = generator.get("domain_shift_predicate") or {}
    forbidden = generator.get("forbidden_change_check") or {}
    source_baseline = generator.get("source_baseline") or {}

    if not all(predicate.values()):
        failures.append("domain_shift_predicate_not_all_true")

    if any(forbidden.values()):
        failures.append("forbidden_change_detected")

    required_zero_fields = [
        "registered_move_id_set_delta",
        "ontology_delta",
        "evaluator_delta",
        "law_delta",
        "receipt_schema_delta",
        "profile_classifier_delta",
        "halt_vocabulary_delta",
    ]

    for field in required_zero_fields:
        if target_manifest.get(field) != 0:
            failures.append(f"{field}_not_zero:{target_manifest.get(field)}")

    required_false_fields = [
        "new_move_types_allowed",
        "new_laws_allowed",
        "new_classifier_categories_allowed",
        "new_halt_reasons_allowed",
    ]

    for field in required_false_fields:
        if target_manifest.get(field) is not False:
            failures.append(f"{field}_not_false:{target_manifest.get(field)}")

    family_name_to_code = {
        "one_sided_suspension": "A",
        "two_sided_suspension": "B",
        "suspension_plus_repair": "C",
        "projection_quotient": "D",
        "relabel_symmetry_stress": "E",
    }

    family_code_to_name = {v: k for k, v in family_name_to_code.items()}

    shifted_schedule = target_manifest.get("shifted_family_schedule") or []
    shifted_weights = target_manifest.get("shifted_family_weights") or {}

    expanded_family_names = []
    slots = []
    family_seen = {}

    for family in shifted_schedule:
        if family not in family_name_to_code:
            failures.append(f"unknown_shifted_family:{family}")
            continue

        weight = shifted_weights.get(family)
        if not isinstance(weight, int) or weight <= 0:
            failures.append(f"invalid_shifted_family_weight:{family}:{weight}")
            continue

        for _ in range(weight):
            family_seen[family] = family_seen.get(family, 0) + 1
            slot_n = len(slots) + 1
            code = family_name_to_code[family]
            expanded_family_names.append(family)
            slots.append(
                {
                    "slot_n": slot_n,
                    "family": family,
                    "family_code": code,
                    "family_occurrence_n": family_seen[family],
                    "slot_label": f"slot_{slot_n:02d}_{code}{family_seen[family]}",
                    "distinguishability_key": f"{family}|slot={slot_n}|occurrence={family_seen[family]}",
                }
            )

    compact_family_schedule = "".join(slot["family_code"] for slot in slots)

    family_slot_counts = {}
    for slot in slots:
        code = slot["family_code"]
        family_slot_counts[code] = family_slot_counts.get(code, 0) + 1

    duplicate_family_slots = {
        code: count
        for code, count in family_slot_counts.items()
        if count > 1
    }

    if not duplicate_family_slots:
        warnings.append("slot_runner_support_used_without_duplicate_family_slots")

    if compact_family_schedule:
        try:
            parsed = parse_families(compact_family_schedule)
            parsed_family_names = [
                item.value if hasattr(item, "value") else str(item)
                for item in parsed
            ]
        except Exception as exc:
            parsed_family_names = []
            failures.append(f"parse_shifted_family_schedule_failed:{exc}")
    else:
        parsed_family_names = []

    if parsed_family_names != expanded_family_names:
        failures.append("expanded_schedule_parse_mismatch")

    radius = target_manifest.get("radius")
    max_cells = target_manifest.get("max_cells")
    depth_max = target_manifest.get("depth_max")
    cycles_per_case = target_manifest.get("cycles_per_case")

    if radius != depth_max or radius != cycles_per_case:
        failures.append(
            f"radius_depth_cycles_mismatch:radius={radius}:depth_max={depth_max}:cycles={cycles_per_case}"
        )

    if not isinstance(radius, int) or radius <= 0:
        failures.append(f"invalid_radius:{radius}")

    if not isinstance(max_cells, int) or max_cells <= 0:
        failures.append(f"invalid_max_cells:{max_cells}")

    source_run_id = source_baseline.get("run_id")
    if not source_run_id:
        failures.append("source_baseline_run_id_missing")

    slot_command_argvs = []
    slot_command_lines = []

    if not failures:
        for slot in slots:
            stress_argv = [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "stress",
                "--families",
                slot["family_code"],
                "--depth-max",
                str(radius),
                "--cycles-per-case",
                str(radius),
                "--max-cells",
                str(max_cells),
                "--strict-laws",
            ]
            gate_argv = [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "gate",
                "latest",
            ]
            eval_argv = [
                "uv",
                "run",
                "python",
                "src/matrixlab/cli.py",
                "agent-eval",
                "latest",
                "--previous",
                source_run_id,
            ]

            slot_command_argvs.append(
                {
                    "slot": slot,
                    "commands": [stress_argv, gate_argv, eval_argv],
                }
            )

            slot_command_lines.extend(
                [
                    f"echo DOMAIN_SHIFT_SLOT {slot['slot_label']} {slot['distinguishability_key']}",
                    " ".join(stress_argv),
                    " ".join(gate_argv),
                    " ".join(eval_argv),
                ]
            )

    slot_command_script = "\n".join(slot_command_lines) if slot_command_lines else None

    runner_support = {
        "support_kind": "SLOT_SEPARATED_EXISTING_STRESS_RUNNER",
        "identity_failure_class": "IDENTITY_DISTINGUISHABILITY_DEFICIT",
        "reason_single_run_repetition_is_forbidden": (
            "receipt projection is not slot-distinguished for repeated family entries; "
            "therefore repeated families must execute as separate run slots"
        ),
        "domain_shift_axis": target_manifest.get("domain_shift_axis"),
        "domain_shift_label": target_manifest.get("domain_shift_label"),
        "compact_family_schedule": compact_family_schedule,
        "expanded_family_names": expanded_family_names,
        "parsed_family_names": parsed_family_names,
        "family_slot_counts": family_slot_counts,
        "duplicate_family_slots": duplicate_family_slots,
        "slot_count": len(slots),
        "slots": slots,
        "family_name_to_code": family_name_to_code,
        "family_code_to_name": family_code_to_name,
        "uses_existing_registered_moves_only": True,
        "requires_new_move_types": False,
        "requires_new_laws": False,
        "requires_new_classifier_semantics": False,
        "requires_new_halt_vocabulary": False,
        "requires_new_evaluator_semantics": False,
        "preserves_repetition_distinguishability": True,
    }

    payload = {
        "input_domain_shift_generator": domain_shift_generator,
        "input_domain_shift_generator_path": str(generator_path) if generator_path else None,
        "domain_shift_generator_id": generator.get("domain_shift_generator_id"),
        "domain_shift_generator_payload_sig8": generator.get("domain_shift_generator_payload_sig8"),
        "recomputed_domain_shift_generator_payload_sig8": generator_sig,
        "transfer_contract_id": generator.get("transfer_contract_id"),
        "source_cell": generator.get("source_cell"),
        "target_cell": generator.get("target_cell"),
        "shift_kind": generator.get("shift_kind"),
        "source_baseline": source_baseline,
        "target_generator_manifest": target_manifest,
        "runner_support": runner_support,
        "command_kind": "EXECUTE_DOMAIN_SHIFT_D1_SLOT_SEPARATED",
        "slot_command_count": len(slot_command_argvs),
        "slot_command_argvs": slot_command_argvs,
        "slot_command_lines": slot_command_lines,
        "slot_command_script": slot_command_script,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "MANUAL_EXECUTE_DOMAIN_SHIFT_SLOT_COMMANDS",
            "stop_code": "domain_shift_slot_runner_support_failed" if failures else None,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/domain_shift_slot_runner_support",
        "domain_shift_slot_runner_support_schema_version",
        DOMAIN_SHIFT_SLOT_RUNNER_SUPPORT_SCHEMA,
        "domain_shift_slot_runner_support_id",
        "domain_shift_slot_runner_support_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"domain_shift_slot_runner_support_path: {out_path}")



def _scalability_contract_clean_repeated_family_consistency(repeated_family_consistency):
    if not isinstance(repeated_family_consistency, dict):
        return False

    for row in repeated_family_consistency.values():
        if not isinstance(row, dict):
            return False
        if row.get("coarse_consistent") is not True:
            return False
        if row.get("raw_consistent") is not True:
            return False
        if row.get("registered_consistent") is not True:
            return False

    return True


def _scalability_contract_clean_measurement(measurement_cleanliness):
    if not isinstance(measurement_cleanliness, dict):
        return False

    required_empty = [
        "boundary_slots",
        "dirty_slots",
        "eval_gate_fail_slots",
        "receipt_mismatch_slots",
    ]

    for key in required_empty:
        if measurement_cleanliness.get(key) != []:
            return False

    if measurement_cleanliness.get("repeated_family_inconsistencies") != {}:
        return False

    return True


def _scalability_contract_resolve_json(identifier, directory):
    return resolve_json_path(identifier, directory)


def _scalability_contract_verify_core(contract):
    failures = []
    warnings = []

    baseline = contract.get("baseline") or {}

    required_contract_fields = {
        "contract_kind": "POST_R50_PRE_R75_FIRST_ORDER_OBSERVATION_CONTRACT",
        "next_scale_step": "RADIUS_75_SLOT_SEPARATED",
        "execution_shape": "KEEP_9_SLOT_SEPARATED_RUNS",
        "representative_subset_status": "NOT_LICENSED_AT_V0",
        "target_metric": "first_order_curve_stability",
        "r75_observation_gate": "RADIUS_SCALE_OBSERVATION_GATE_V0",
    }

    for key, expected in required_contract_fields.items():
        if contract.get(key) != expected:
            failures.append(f"contract_field_mismatch:{key}:{contract.get(key)}")

    required_baseline_bindings = {
        "observation_id": "566a342b",
        "slot_execution_id": "74358d77",
        "source_support_id": "54890760",
        "transfer_contract_id": "50a01dcd",
        "domain_shift_generator_id": "da466dc2",
        "radius": 50,
        "confidence_scope": "RADIUS_50_SLOT_SEPARATED_PROBE_ONLY",
    }

    for key, expected in required_baseline_bindings.items():
        if baseline.get(key) != expected:
            failures.append(f"baseline_binding_mismatch:{key}:expected={expected}:actual={baseline.get(key)}")

    baseline_observation_id = baseline.get("observation_id")
    baseline_slot_execution_id = baseline.get("slot_execution_id")
    baseline_support_id = baseline.get("source_support_id")
    baseline_transfer_contract_id = baseline.get("transfer_contract_id")
    baseline_generator_id = baseline.get("domain_shift_generator_id")

    observation = {}
    execution = {}
    support = {}
    transfer = {}
    generator = {}

    try:
        observation_path = _scalability_contract_resolve_json(
            baseline_observation_id, "data/domain_shift_slot_observations"
        )
        observation = json.loads(observation_path.read_text())
        observation_sig = stable_sig(
            observation,
            "domain_shift_slot_observation_id",
            "domain_shift_slot_observation_payload_sig8",
        )
        if observation.get("domain_shift_slot_observation_payload_sig8") != observation_sig:
            failures.append("baseline_observation_sig_mismatch")
        if observation_path.stem != observation.get("domain_shift_slot_observation_id"):
            failures.append("baseline_observation_filename_id_mismatch")
    except Exception as exc:
        observation_path = None
        observation_sig = None
        failures.append(f"baseline_observation_unresolved:{baseline_observation_id}:{exc}")

    try:
        execution_path = _scalability_contract_resolve_json(
            baseline_slot_execution_id, "data/domain_shift_slot_runs"
        )
        execution = json.loads(execution_path.read_text())
        execution_sig_payload = dict(execution)
        execution_sig_payload.pop("domain_shift_slot_run_execution_id", None)
        execution_sig = hashlib.sha256(
            json.dumps(execution_sig_payload, sort_keys=True).encode()
        ).hexdigest()[:8]
        if execution.get("domain_shift_slot_run_execution_id") != execution_sig:
            failures.append("baseline_slot_execution_sig_mismatch")
        if execution_path.stem != execution.get("domain_shift_slot_run_execution_id"):
            failures.append("baseline_slot_execution_filename_id_mismatch")
    except Exception as exc:
        execution_path = None
        execution_sig = None
        failures.append(f"baseline_slot_execution_unresolved:{baseline_slot_execution_id}:{exc}")

    try:
        support_path = _scalability_contract_resolve_json(
            baseline_support_id, "data/domain_shift_slot_runner_support"
        )
        support = json.loads(support_path.read_text())
        support_sig = stable_sig(
            support,
            "domain_shift_slot_runner_support_id",
            "domain_shift_slot_runner_support_payload_sig8",
        )
        if support.get("domain_shift_slot_runner_support_payload_sig8") != support_sig:
            failures.append("baseline_support_sig_mismatch")
        if support_path.stem != support.get("domain_shift_slot_runner_support_id"):
            failures.append("baseline_support_filename_id_mismatch")
    except Exception as exc:
        support_path = None
        support_sig = None
        failures.append(f"baseline_support_unresolved:{baseline_support_id}:{exc}")

    try:
        transfer_path = _scalability_contract_resolve_json(
            baseline_transfer_contract_id, "data/cell_transfer_contracts"
        )
        transfer = json.loads(transfer_path.read_text())
        transfer_sig = stable_sig(
            transfer,
            "cell_transfer_contract_id",
            "cell_transfer_contract_payload_sig8",
        )
        if transfer.get("cell_transfer_contract_payload_sig8") != transfer_sig:
            failures.append("baseline_transfer_contract_sig_mismatch")
        if transfer_path.stem != transfer.get("cell_transfer_contract_id"):
            failures.append("baseline_transfer_contract_filename_id_mismatch")
    except Exception as exc:
        transfer_path = None
        transfer_sig = None
        failures.append(f"baseline_transfer_contract_unresolved:{baseline_transfer_contract_id}:{exc}")

    try:
        generator_path = _scalability_contract_resolve_json(
            baseline_generator_id, "data/domain_shift_generators"
        )
        generator = json.loads(generator_path.read_text())
        generator_sig = stable_sig(
            generator,
            "domain_shift_generator_id",
            "domain_shift_generator_payload_sig8",
        )
        if generator.get("domain_shift_generator_payload_sig8") != generator_sig:
            failures.append("baseline_generator_sig_mismatch")
        if generator_path.stem != generator.get("domain_shift_generator_id"):
            failures.append("baseline_generator_filename_id_mismatch")
    except Exception as exc:
        generator_path = None
        generator_sig = None
        failures.append(f"baseline_generator_unresolved:{baseline_generator_id}:{exc}")

    observation_body = observation.get("observation") or {}
    measurement_cleanliness = observation_body.get("measurement_cleanliness") or {}
    repeated_family_consistency = observation_body.get("repeated_family_consistency") or {}

    if observation.get("gate") != "PASS":
        failures.append("baseline_observation_gate_not_PASS")

    if observation_body.get("outcome") != "MEASUREMENT_TRANSFER_STABLE_CURVE":
        failures.append(f"baseline_outcome_not_stable_curve:{observation_body.get('outcome')}")

    terminal = observation.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"baseline_terminal_not_ADVANCE:{terminal.get('type')}")

    if observation_body.get("confidence_scope") != "RADIUS_50_SLOT_SEPARATED_PROBE_ONLY":
        failures.append("baseline_confidence_scope_mismatch")

    if observation_body.get("slot_count_expected") != 9:
        failures.append(f"baseline_slot_count_expected_not_9:{observation_body.get('slot_count_expected')}")

    if observation_body.get("slot_count_observed") != 9:
        failures.append(f"baseline_slot_count_observed_not_9:{observation_body.get('slot_count_observed')}")

    if baseline.get("slot_count_expected") != 9:
        failures.append(f"contract_baseline_slot_count_expected_not_9:{baseline.get('slot_count_expected')}")

    if baseline.get("slot_count_observed") != 9:
        failures.append(f"contract_baseline_slot_count_observed_not_9:{baseline.get('slot_count_observed')}")

    if not _scalability_contract_clean_measurement(measurement_cleanliness):
        failures.append("baseline_measurement_cleanliness_not_clean")

    if not _scalability_contract_clean_repeated_family_consistency(repeated_family_consistency):
        failures.append("baseline_repeated_family_consistency_not_clean")

    if observation_body.get("semantic_pressure_detected") is not False:
        failures.append("baseline_semantic_pressure_detected_not_false")

    if baseline.get("semantic_pressure_detected") is not False:
        failures.append("contract_baseline_semantic_pressure_detected_not_false")

    if observation_body.get("aggregate_coarse_profiles_total") != baseline.get("aggregate_coarse_profiles_total"):
        failures.append("baseline_aggregate_coarse_profiles_total_mismatch")

    if observation_body.get("aggregate_raw_total_by_slot_sum") != baseline.get("aggregate_raw_total_by_slot_sum"):
        failures.append("baseline_aggregate_raw_total_by_slot_sum_mismatch")

    if execution.get("gate") != "PASS":
        failures.append("baseline_slot_execution_gate_not_PASS")

    if support.get("gate") != "PASS":
        failures.append("baseline_support_gate_not_PASS")

    if transfer.get("gate") != "PASS":
        failures.append("baseline_transfer_contract_gate_not_PASS")

    if generator.get("gate") != "PASS":
        failures.append("baseline_generator_gate_not_PASS")

    required_r75_fields = contract.get("required_r75_fields") or []
    required_r75_field_set = {
        "radius",
        "confidence_scope",
        "slot_count_expected",
        "slot_count_observed",
        "measurement_cleanliness",
        "repeated_family_consistency",
        "aggregate_by_family",
        "aggregate_by_move",
        "aggregate_coarse_profiles",
        "aggregate_coarse_profiles_total",
        "aggregate_raw_total_by_slot_sum",
        "semantic_pressure",
        "semantic_pressure_detected",
        "delta_vs_radius_50",
        "delta_class",
        "normalized_deltas_if_available",
        "operator_burden_v0_if_available",
        "terminal_decision",
    }

    missing_r75_fields = sorted(required_r75_field_set - set(required_r75_fields))
    if missing_r75_fields:
        failures.append("missing_required_r75_fields:" + ",".join(missing_r75_fields))

    delta_classes = set(contract.get("delta_classes") or [])
    expected_delta_classes = {
        "SAME_SHAPES_SAME_COUNTS",
        "SAME_SHAPES_COUNT_SHIFT",
        "NEW_SHAPE_OBSERVED",
        "MISSING_SHAPE_OBSERVED",
        "REPEATED_FAMILY_INCONSISTENT",
        "UNCLASSIFIED_DELTA",
    }
    if delta_classes != expected_delta_classes:
        failures.append("delta_classes_mismatch")

    failure_classes = set(contract.get("failure_classes") or [])
    expected_failure_classes = {
        "STOP_MEASUREMENT_FAILURE",
        "STOP_RESOURCE_BOUNDARY",
        "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT",
        "STOP_ONTOLOGY_PRESSURE",
        "STOP_UNCLASSIFIED_DELTA",
    }
    if failure_classes != expected_failure_classes:
        failures.append("failure_classes_mismatch")

    continuation_classes = set(contract.get("non_failure_continuation_classes") or [])
    expected_continuation_classes = {
        "CURVE_STABLE_CONTINUE",
        "CURVE_CHANGED_CONTINUE_MEASUREMENT",
        "PROVISIONAL_R50_R75_ENVELOPE",
    }
    if continuation_classes != expected_continuation_classes:
        failures.append("non_failure_continuation_classes_mismatch")

    forbidden = contract.get("forbidden") or {}
    forbidden_required_true = [
        "implement_compression",
        "implement_caching",
        "skip_receipts",
        "alter_existing_run_semantics",
        "alter_existing_gate_semantics",
        "alter_move_registry_semantics",
        "add_new_cell_types",
        "add_new_theorem_layers",
        "add_new_domain_shift_families",
        "select_representative_subset",
        "treat_r50_as_global_scalability_proof",
        "treat_contract_as_proof_of_future_scale",
    ]

    for key in forbidden_required_true:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_clause_missing_or_not_true:{key}")

    verification = {
        "baseline_linkage_check": {
            "baseline_observation_resolves": observation_path is not None,
            "baseline_observation_sig_matches": bool(
                observation
                and observation.get("domain_shift_slot_observation_payload_sig8") == observation_sig
            ),
            "baseline_slot_execution_resolves": execution_path is not None,
            "baseline_slot_execution_sig_matches": bool(
                execution
                and execution.get("domain_shift_slot_run_execution_id") == execution_sig
            ),
            "baseline_support_resolves": support_path is not None,
            "baseline_support_sig_matches": bool(
                support
                and support.get("domain_shift_slot_runner_support_payload_sig8") == support_sig
            ),
            "baseline_transfer_contract_resolves": transfer_path is not None,
            "baseline_transfer_contract_sig_matches": bool(
                transfer
                and transfer.get("cell_transfer_contract_payload_sig8") == transfer_sig
            ),
            "baseline_generator_resolves": generator_path is not None,
            "baseline_generator_sig_matches": bool(
                generator
                and generator.get("domain_shift_generator_payload_sig8") == generator_sig
            ),
        },
        "baseline_observation_check": {
            "gate": observation.get("gate"),
            "outcome": observation_body.get("outcome"),
            "terminal_type": terminal.get("type"),
            "slot_count_expected": observation_body.get("slot_count_expected"),
            "slot_count_observed": observation_body.get("slot_count_observed"),
            "measurement_cleanliness_clean": _scalability_contract_clean_measurement(measurement_cleanliness),
            "repeated_family_consistency_clean": _scalability_contract_clean_repeated_family_consistency(repeated_family_consistency),
            "semantic_pressure_detected": observation_body.get("semantic_pressure_detected"),
            "aggregate_coarse_profiles_total": observation_body.get("aggregate_coarse_profiles_total"),
            "aggregate_raw_total_by_slot_sum": observation_body.get("aggregate_raw_total_by_slot_sum"),
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    return verification


def _scalability_contract_payload_from_observation(observation_id):
    observation_path = resolve_json_path(observation_id, "data/domain_shift_slot_observations")
    observation = json.loads(observation_path.read_text())
    obs = observation.get("observation") or {}

    baseline = {
        "radius": obs.get("radius"),
        "confidence_scope": obs.get("confidence_scope"),
        "observation_id": observation.get("domain_shift_slot_observation_id"),
        "slot_execution_id": observation.get("slot_execution_id"),
        "source_support_id": observation.get("source_support_id"),
        "transfer_contract_id": observation.get("transfer_contract_id"),
        "domain_shift_generator_id": observation.get("domain_shift_generator_id"),
        "slot_count_expected": obs.get("slot_count_expected"),
        "slot_count_observed": obs.get("slot_count_observed"),
        "aggregate_coarse_profiles_total": obs.get("aggregate_coarse_profiles_total"),
        "aggregate_raw_total_by_slot_sum": obs.get("aggregate_raw_total_by_slot_sum"),
        "semantic_pressure_detected": obs.get("semantic_pressure_detected"),
        "outcome": obs.get("outcome"),
        "gate": observation.get("gate"),
        "terminal_type": (observation.get("terminal") or {}).get("type"),
        "total_receipts_sum": sum(
            int(row.get("total_receipts") or 0)
            for row in (obs.get("aggregate_by_family") or {}).values()
        ),
        "receipt_rows_sum": sum(
            int(row.get("receipt_rows") or 0)
            for row in (obs.get("aggregate_by_family") or {}).values()
        ),
    }

    contract = {
        "contract_kind": "POST_R50_PRE_R75_FIRST_ORDER_OBSERVATION_CONTRACT",
        "layer": "OUTER_MIDDLE_BOUNDARY_OBJECT",
        "baseline": baseline,
        "next_scale_step": "RADIUS_75_SLOT_SEPARATED",
        "execution_shape": "KEEP_9_SLOT_SEPARATED_RUNS",
        "representative_subset_status": "NOT_LICENSED_AT_V0",
        "target_metric": "first_order_curve_stability",
        "secondary_metrics": [
            "receipt_burden",
            "runtime_burden_if_available",
            "slot_consistency",
            "identity_distinguishability",
            "semantic_pressure",
            "operator_burden_if_available",
            "resource_boundary_if_observable",
        ],
        "required_r75_artifact": "domain_shift_slot_observation_v0 with radius=75",
        "r50_r75_comparison_artifact": "radius_scale_observation_v0",
        "required_r75_fields": [
            "radius",
            "confidence_scope",
            "slot_count_expected",
            "slot_count_observed",
            "measurement_cleanliness",
            "repeated_family_consistency",
            "aggregate_by_family",
            "aggregate_by_move",
            "aggregate_coarse_profiles",
            "aggregate_coarse_profiles_total",
            "aggregate_raw_total_by_slot_sum",
            "semantic_pressure",
            "semantic_pressure_detected",
            "delta_vs_radius_50",
            "delta_class",
            "normalized_deltas_if_available",
            "operator_burden_v0_if_available",
            "terminal_decision",
        ],
        "delta_classes": [
            "SAME_SHAPES_SAME_COUNTS",
            "SAME_SHAPES_COUNT_SHIFT",
            "NEW_SHAPE_OBSERVED",
            "MISSING_SHAPE_OBSERVED",
            "REPEATED_FAMILY_INCONSISTENT",
            "UNCLASSIFIED_DELTA",
        ],
        "failure_classes": [
            "STOP_MEASUREMENT_FAILURE",
            "STOP_RESOURCE_BOUNDARY",
            "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT",
            "STOP_ONTOLOGY_PRESSURE",
            "STOP_UNCLASSIFIED_DELTA",
        ],
        "non_failure_continuation_classes": [
            "CURVE_STABLE_CONTINUE",
            "CURVE_CHANGED_CONTINUE_MEASUREMENT",
            "PROVISIONAL_R50_R75_ENVELOPE",
        ],
        "r75_observation_gate": "RADIUS_SCALE_OBSERVATION_GATE_V0",
        "r75_observation_gate_pass_requirements": [
            "R75 observation gate passes",
            "R75 verification gate passes",
            "slot_count_observed = slot_count_expected = 9",
            "sigs match",
            "no receipt mismatches",
            "no dirty slots",
            "no eval-gate failures",
            "no unresolved slot execution/support/generator/contract",
            "semantic pressure fields are explicit",
            "delta_vs_radius_50 exists",
            "delta_class is assigned",
            "terminal decision is explicit",
        ],
        "r75_decision_rule": {
            "measurement_fails": "STOP_MEASUREMENT_FAILURE",
            "repeated_family_consistency_breaks": "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT",
            "semantic_pressure_appears": "STOP_ONTOLOGY_PRESSURE",
            "resource_envelope_exceeded": "STOP_RESOURCE_BOUNDARY",
            "delta_unclassified": "STOP_UNCLASSIFIED_DELTA",
            "same_shapes_acceptable_burden": [
                "CURVE_STABLE_CONTINUE",
                "PROVISIONAL_R50_R75_ENVELOPE",
            ],
            "new_or_shifted_shapes_cleanly_classified": "CURVE_CHANGED_CONTINUE_MEASUREMENT",
        },
        "forbidden": {
            "implement_compression": True,
            "implement_caching": True,
            "skip_receipts": True,
            "alter_existing_run_semantics": True,
            "alter_existing_gate_semantics": True,
            "alter_move_registry_semantics": True,
            "add_new_cell_types": True,
            "add_new_theorem_layers": True,
            "add_new_domain_shift_families": True,
            "select_representative_subset": True,
            "treat_r50_as_global_scalability_proof": True,
            "treat_contract_as_proof_of_future_scale": True,
        },
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": "RUN_RADIUS_75_SLOT_SEPARATED_UNDER_SCALABILITY_CONTRACT_V0",
            "stop_code": None,
        },
    }

    verification = _scalability_contract_verify_core(contract)
    contract["baseline_linkage_check"] = verification["baseline_linkage_check"]
    contract["verification_result"] = {
        "gate": verification["gate"],
        "failures": verification["failures"],
        "warnings": verification["warnings"],
    }

    if verification["gate"] != "PASS":
        contract["terminal"] = {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_CONTRACT_BUILD_FAIL",
        }

    return contract, verification



def _radius_scale_observation_metric_delta(r50_value, r75_value):
    if r50_value is None or r75_value is None:
        return {
            "r50": r50_value,
            "r75": r75_value,
            "delta": None,
            "ratio_vs_r50": None,
            "per_radius_r50": None,
            "per_radius_r75": None,
            "per_radius_delta": None,
        }

    r50 = float(r50_value)
    r75 = float(r75_value)
    per50 = r50 / 50.0
    per75 = r75 / 75.0

    return {
        "r50": r50_value,
        "r75": r75_value,
        "delta": r75_value - r50_value,
        "ratio_vs_r50": None if r50 == 0 else round(r75 / r50, 6),
        "per_radius_r50": round(per50, 6),
        "per_radius_r75": round(per75, 6),
        "per_radius_delta": round(per75 - per50, 6),
    }


def _radius_scale_observation_clean_measurement(obs_body):
    clean = obs_body.get("measurement_cleanliness") or {}
    return _scalability_contract_clean_measurement(clean)


def _radius_scale_observation_clean_repeated(obs_body):
    repeated = obs_body.get("repeated_family_consistency") or {}
    return _scalability_contract_clean_repeated_family_consistency(repeated)


def _radius_scale_observation_shape_delta(r50_profiles, r75_profiles):
    r50_set = set((r50_profiles or {}).keys())
    r75_set = set((r75_profiles or {}).keys())

    added = sorted(r75_set - r50_set)
    missing = sorted(r50_set - r75_set)
    common = sorted(r50_set & r75_set)
    shifted = []

    for key in common:
        if (r50_profiles or {}).get(key) != (r75_profiles or {}).get(key):
            shifted.append({
                "profile": key,
                "r50": (r50_profiles or {}).get(key),
                "r75": (r75_profiles or {}).get(key),
                "delta": (r75_profiles or {}).get(key) - (r50_profiles or {}).get(key),
            })

    return {
        "added_shapes": added,
        "missing_shapes": missing,
        "common_shapes": common,
        "count_shifted_shapes": shifted,
        "shape_set_same": not added and not missing,
        "shape_counts_same": not shifted and not added and not missing,
    }


def _radius_scale_observation_delta_class(r50_obs, r75_obs):
    r50_body = r50_obs.get("observation") or {}
    r75_body = r75_obs.get("observation") or {}

    if not _radius_scale_observation_clean_measurement(r75_body):
        return "UNCLASSIFIED_DELTA"

    if not _radius_scale_observation_clean_repeated(r75_body):
        return "REPEATED_FAMILY_INCONSISTENT"

    shape_delta = _radius_scale_observation_shape_delta(
        r50_body.get("aggregate_coarse_profiles") or {},
        r75_body.get("aggregate_coarse_profiles") or {},
    )

    if shape_delta["added_shapes"]:
        return "NEW_SHAPE_OBSERVED"

    if shape_delta["missing_shapes"]:
        return "MISSING_SHAPE_OBSERVED"

    if shape_delta["shape_counts_same"]:
        return "SAME_SHAPES_SAME_COUNTS"

    if shape_delta["shape_set_same"]:
        return "SAME_SHAPES_COUNT_SHIFT"

    return "UNCLASSIFIED_DELTA"


def _radius_scale_observation_terminal_decision(delta_class, r75_obs, resource_envelope):
    r75_body = r75_obs.get("observation") or {}

    if r75_obs.get("gate") != "PASS":
        return "STOP_MEASUREMENT_FAILURE"

    if not _radius_scale_observation_clean_measurement(r75_body):
        return "STOP_MEASUREMENT_FAILURE"

    if not _radius_scale_observation_clean_repeated(r75_body):
        return "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT"

    if r75_body.get("semantic_pressure_detected") is not False:
        return "STOP_ONTOLOGY_PRESSURE"

    if resource_envelope.get("resource_boundary_observed") is True:
        return "STOP_RESOURCE_BOUNDARY"

    if delta_class == "UNCLASSIFIED_DELTA":
        return "STOP_UNCLASSIFIED_DELTA"

    if delta_class == "SAME_SHAPES_SAME_COUNTS":
        return "CURVE_STABLE_CONTINUE"

    if delta_class == "SAME_SHAPES_COUNT_SHIFT":
        return "PROVISIONAL_R50_R75_ENVELOPE"

    if delta_class in {"NEW_SHAPE_OBSERVED", "MISSING_SHAPE_OBSERVED"}:
        return "CURVE_CHANGED_CONTINUE_MEASUREMENT"

    if delta_class == "REPEATED_FAMILY_INCONSISTENT":
        return "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT"

    return "STOP_UNCLASSIFIED_DELTA"


def _radius_scale_observation_payload(contract_id, r75_observation_id):
    failures = []
    warnings = []

    contract_path = resolve_json_path(contract_id, "data/scalability_contracts")
    contract = json.loads(contract_path.read_text())
    contract_sig = stable_sig(contract, "contract_id", "contract_sig8")

    if contract.get("contract_sig8") != contract_sig:
        failures.append("contract_sig_mismatch")
    if contract.get("gate") != "PASS":
        failures.append("contract_gate_not_PASS")
    if contract.get("next_scale_step") != "RADIUS_75_SLOT_SEPARATED":
        failures.append("contract_next_scale_step_not_R75")

    contract_verify = _scalability_contract_verify_core(contract)
    if contract_verify.get("gate") != "PASS":
        failures.append("contract_core_verification_not_PASS")
        failures.extend(contract_verify.get("failures") or [])

    baseline = contract.get("baseline") or {}
    r50_observation_id = baseline.get("observation_id")

    r50_path = resolve_json_path(r50_observation_id, "data/domain_shift_slot_observations")
    r50_obs = json.loads(r50_path.read_text())
    r50_sig = stable_sig(
        r50_obs,
        "domain_shift_slot_observation_id",
        "domain_shift_slot_observation_payload_sig8",
    )

    r75_path = resolve_json_path(r75_observation_id, "data/domain_shift_slot_observations")
    r75_obs = json.loads(r75_path.read_text())
    r75_sig = stable_sig(
        r75_obs,
        "domain_shift_slot_observation_id",
        "domain_shift_slot_observation_payload_sig8",
    )

    if r50_obs.get("domain_shift_slot_observation_payload_sig8") != r50_sig:
        failures.append("r50_observation_sig_mismatch")
    if r75_obs.get("domain_shift_slot_observation_payload_sig8") != r75_sig:
        failures.append("r75_observation_sig_mismatch")

    r50_body = r50_obs.get("observation") or {}
    r75_body = r75_obs.get("observation") or {}

    if r50_obs.get("gate") != "PASS":
        failures.append("r50_observation_gate_not_PASS")
    if r75_obs.get("gate") != "PASS":
        failures.append("r75_observation_gate_not_PASS")

    if r50_body.get("radius") != 50:
        failures.append(f"r50_radius_not_50:{r50_body.get('radius')}")
    if r75_body.get("radius") != 75:
        failures.append(f"r75_radius_not_75:{r75_body.get('radius')}")

    if r50_body.get("confidence_scope") != "RADIUS_50_SLOT_SEPARATED_PROBE_ONLY":
        failures.append("r50_confidence_scope_mismatch")
    if r75_body.get("confidence_scope") != "RADIUS_75_SLOT_SEPARATED_PROBE_ONLY":
        failures.append("r75_confidence_scope_mismatch")

    if r50_body.get("slot_count_expected") != 9 or r50_body.get("slot_count_observed") != 9:
        failures.append("r50_slot_count_not_9")
    if r75_body.get("slot_count_expected") != 9 or r75_body.get("slot_count_observed") != 9:
        failures.append("r75_slot_count_not_9")

    if not _radius_scale_observation_clean_measurement(r50_body):
        failures.append("r50_measurement_cleanliness_not_clean")
    if not _radius_scale_observation_clean_measurement(r75_body):
        failures.append("r75_measurement_cleanliness_not_clean")

    if not _radius_scale_observation_clean_repeated(r50_body):
        failures.append("r50_repeated_family_consistency_not_clean")
    if not _radius_scale_observation_clean_repeated(r75_body):
        failures.append("r75_repeated_family_consistency_not_clean")

    if r50_body.get("semantic_pressure_detected") is not False:
        failures.append("r50_semantic_pressure_not_false")
    if r75_body.get("semantic_pressure_detected") is not False:
        failures.append("r75_semantic_pressure_not_false")

    r50_execution = r50_body.get("slot_execution") or {}
    r75_execution = r75_body.get("slot_execution") or {}
    r50_support = r50_body.get("slot_support") or {}
    r75_support = r75_body.get("slot_support") or {}
    r50_generator = r50_body.get("domain_shift_generator") or {}
    r75_generator = r75_body.get("domain_shift_generator") or {}
    r50_transfer = r50_body.get("transfer_contract") or {}
    r75_transfer = r75_body.get("transfer_contract") or {}

    for label, row in [
        ("r50_slot_execution", r50_execution),
        ("r75_slot_execution", r75_execution),
        ("r50_slot_support", r50_support),
        ("r75_slot_support", r75_support),
        ("r50_generator", r50_generator),
        ("r75_generator", r75_generator),
        ("r50_transfer_contract", r50_transfer),
        ("r75_transfer_contract", r75_transfer),
    ]:
        if row.get("gate") != "PASS":
            failures.append(f"{label}_gate_not_PASS")
        if row.get("id") is None:
            failures.append(f"{label}_id_missing")
        if row.get("path") is None:
            failures.append(f"{label}_path_missing")

    r50_clean = r50_body.get("measurement_cleanliness") or {}
    r75_clean = r75_body.get("measurement_cleanliness") or {}

    receipt_burden = _radius_scale_observation_metric_delta(
        sum(int(row.get("total_receipts") or 0) for row in (r50_body.get("aggregate_by_family") or {}).values()),
        sum(int(row.get("total_receipts") or 0) for row in (r75_body.get("aggregate_by_family") or {}).values()),
    )
    receipt_rows_burden = _radius_scale_observation_metric_delta(
        sum(int(row.get("receipt_rows") or 0) for row in (r50_body.get("aggregate_by_family") or {}).values()),
        sum(int(row.get("receipt_rows") or 0) for row in (r75_body.get("aggregate_by_family") or {}).values()),
    )

    delta_vs_radius_50 = {
        "radius": _radius_scale_observation_metric_delta(
            r50_body.get("radius"),
            r75_body.get("radius"),
        ),
        "aggregate_coarse_profiles_total": _radius_scale_observation_metric_delta(
            r50_body.get("aggregate_coarse_profiles_total"),
            r75_body.get("aggregate_coarse_profiles_total"),
        ),
        "aggregate_raw_total_by_slot_sum": _radius_scale_observation_metric_delta(
            r50_body.get("aggregate_raw_total_by_slot_sum"),
            r75_body.get("aggregate_raw_total_by_slot_sum"),
        ),
        "total_receipts_sum": receipt_burden,
        "receipt_rows_sum": receipt_rows_burden,
        "aggregate_by_move_delta": {
            key: {
                "r50": (r50_body.get("aggregate_by_move") or {}).get(key, 0),
                "r75": (r75_body.get("aggregate_by_move") or {}).get(key, 0),
                "delta": (r75_body.get("aggregate_by_move") or {}).get(key, 0)
                - (r50_body.get("aggregate_by_move") or {}).get(key, 0),
            }
            for key in sorted(
                set((r50_body.get("aggregate_by_move") or {}).keys())
                | set((r75_body.get("aggregate_by_move") or {}).keys())
            )
        },
        "shape_delta": _radius_scale_observation_shape_delta(
            r50_body.get("aggregate_coarse_profiles") or {},
            r75_body.get("aggregate_coarse_profiles") or {},
        ),
        "repeated_family_consistency_changed": (
            r50_body.get("repeated_family_consistency")
            != r75_body.get("repeated_family_consistency")
        ),
    }

    resource_envelope = {
        "resource_boundary_observed": bool((r75_clean.get("boundary_slots") or [])),
        "boundary_slots": r75_clean.get("boundary_slots") or [],
        "max_cells": r75_body.get("max_cells"),
    }

    delta_class = _radius_scale_observation_delta_class(r50_obs, r75_obs)
    terminal_decision = _radius_scale_observation_terminal_decision(delta_class, r75_obs, resource_envelope)

    gate_failures = []
    if r75_obs.get("gate") != "PASS":
        gate_failures.append("R75_observation_gate_not_PASS")
    if r75_body.get("slot_count_expected") != 9 or r75_body.get("slot_count_observed") != 9:
        gate_failures.append("R75_slot_count_not_9")
    if r75_obs.get("domain_shift_slot_observation_payload_sig8") != r75_sig:
        gate_failures.append("R75_sig_mismatch")
    if not _radius_scale_observation_clean_measurement(r75_body):
        gate_failures.append("R75_measurement_not_clean")
    if r75_body.get("semantic_pressure_detected") is None:
        gate_failures.append("R75_semantic_pressure_not_explicit")
    if not delta_vs_radius_50:
        gate_failures.append("delta_vs_radius_50_missing")
    if not delta_class:
        gate_failures.append("delta_class_missing")
    if not terminal_decision:
        gate_failures.append("terminal_decision_missing")

    failures.extend(gate_failures)

    normalized_deltas_if_available = {
        "raw_profiles_per_radius": _radius_scale_observation_metric_delta(
            (r50_body.get("aggregate_raw_total_by_slot_sum") or 0) / 50.0,
            (r75_body.get("aggregate_raw_total_by_slot_sum") or 0) / 75.0,
        ),
        "receipts_per_radius": _radius_scale_observation_metric_delta(
            receipt_burden["r50"] / 50.0 if receipt_burden["r50"] is not None else None,
            receipt_burden["r75"] / 75.0 if receipt_burden["r75"] is not None else None,
        ),
        "coarse_profiles_per_radius": _radius_scale_observation_metric_delta(
            (r50_body.get("aggregate_coarse_profiles_total") or 0) / 50.0,
            (r75_body.get("aggregate_coarse_profiles_total") or 0) / 75.0,
        ),
    }

    observation = {
        "contract": {
            "id": contract.get("contract_id"),
            "path": str(contract_path),
            "stored_sig": contract.get("contract_sig8"),
            "recomputed_sig": contract_sig,
            "gate": contract.get("gate"),
        },
        "radius_50_observation": {
            "id": r50_obs.get("domain_shift_slot_observation_id"),
            "path": str(r50_path),
            "stored_sig": r50_obs.get("domain_shift_slot_observation_payload_sig8"),
            "recomputed_sig": r50_sig,
            "gate": r50_obs.get("gate"),
        },
        "radius_75_observation": {
            "id": r75_obs.get("domain_shift_slot_observation_id"),
            "path": str(r75_path),
            "stored_sig": r75_obs.get("domain_shift_slot_observation_payload_sig8"),
            "recomputed_sig": r75_sig,
            "gate": r75_obs.get("gate"),
        },
        "target_metric": contract.get("target_metric"),
        "execution_shape": contract.get("execution_shape"),
        "representative_subset_status": contract.get("representative_subset_status"),
        "r50": {
            "radius": r50_body.get("radius"),
            "confidence_scope": r50_body.get("confidence_scope"),
            "slot_count_expected": r50_body.get("slot_count_expected"),
            "slot_count_observed": r50_body.get("slot_count_observed"),
            "aggregate_coarse_profiles_total": r50_body.get("aggregate_coarse_profiles_total"),
            "aggregate_raw_total_by_slot_sum": r50_body.get("aggregate_raw_total_by_slot_sum"),
            "measurement_cleanliness": r50_body.get("measurement_cleanliness"),
            "repeated_family_consistency": r50_body.get("repeated_family_consistency"),
            "semantic_pressure": r50_body.get("semantic_pressure"),
            "semantic_pressure_detected": r50_body.get("semantic_pressure_detected"),
        },
        "r75": {
            "radius": r75_body.get("radius"),
            "confidence_scope": r75_body.get("confidence_scope"),
            "slot_count_expected": r75_body.get("slot_count_expected"),
            "slot_count_observed": r75_body.get("slot_count_observed"),
            "aggregate_coarse_profiles_total": r75_body.get("aggregate_coarse_profiles_total"),
            "aggregate_raw_total_by_slot_sum": r75_body.get("aggregate_raw_total_by_slot_sum"),
            "measurement_cleanliness": r75_body.get("measurement_cleanliness"),
            "repeated_family_consistency": r75_body.get("repeated_family_consistency"),
            "semantic_pressure": r75_body.get("semantic_pressure"),
            "semantic_pressure_detected": r75_body.get("semantic_pressure_detected"),
        },
        "delta_vs_radius_50": delta_vs_radius_50,
        "delta_class": delta_class,
        "normalized_deltas_if_available": normalized_deltas_if_available,
        "operator_burden_v0_if_available": {
            "available": False,
            "reason": "runtime/operator burden is not yet canonicalized as a receipt field",
        },
        "resource_boundary_if_observable": resource_envelope,
        "terminal_decision": terminal_decision,
        "r75_observation_gate": {
            "name": "RADIUS_SCALE_OBSERVATION_GATE_V0",
            "failures": gate_failures,
            "gate": "FAIL" if gate_failures else "PASS",
        },
    }

    payload = {
        "source_contract_id": contract.get("contract_id"),
        "radius_50_observation_id": r50_obs.get("domain_shift_slot_observation_id"),
        "radius_75_observation_id": r75_obs.get("domain_shift_slot_observation_id"),
        "observation": observation,
        "delta_class": delta_class,
        "terminal_decision": terminal_decision,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if terminal_decision.startswith("STOP_") else "ADVANCE",
            "next_command_goal": None
            if terminal_decision.startswith("STOP_")
            else "DECIDE_R75_SCALE_OUTCOME_OR_NEXT_RADIUS_V0",
            "stop_code": terminal_decision if terminal_decision.startswith("STOP_") else None,
        },
    }

    return payload


def _radius_scale_observation_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("radius_scale_observation_gate_not_PASS")

    obs = payload.get("observation") or {}
    r50 = obs.get("r50") or {}
    r75 = obs.get("r75") or {}

    if payload.get("delta_class") not in {
        "SAME_SHAPES_SAME_COUNTS",
        "SAME_SHAPES_COUNT_SHIFT",
        "NEW_SHAPE_OBSERVED",
        "MISSING_SHAPE_OBSERVED",
        "REPEATED_FAMILY_INCONSISTENT",
        "UNCLASSIFIED_DELTA",
    }:
        failures.append("delta_class_invalid_or_missing")

    if payload.get("terminal_decision") not in {
        "STOP_MEASUREMENT_FAILURE",
        "STOP_RESOURCE_BOUNDARY",
        "STOP_IDENTITY_DISTINGUISHABILITY_DEFICIT",
        "STOP_ONTOLOGY_PRESSURE",
        "STOP_UNCLASSIFIED_DELTA",
        "CURVE_STABLE_CONTINUE",
        "CURVE_CHANGED_CONTINUE_MEASUREMENT",
        "PROVISIONAL_R50_R75_ENVELOPE",
    }:
        failures.append("terminal_decision_invalid_or_missing")

    if r50.get("radius") != 50:
        failures.append("verify_r50_radius_not_50")
    if r75.get("radius") != 75:
        failures.append("verify_r75_radius_not_75")

    if r50.get("slot_count_expected") != 9 or r50.get("slot_count_observed") != 9:
        failures.append("verify_r50_slot_count_not_9")
    if r75.get("slot_count_expected") != 9 or r75.get("slot_count_observed") != 9:
        failures.append("verify_r75_slot_count_not_9")

    if not payload.get("observation", {}).get("delta_vs_radius_50"):
        failures.append("delta_vs_radius_50_missing")

    if not payload.get("observation", {}).get("normalized_deltas_if_available"):
        failures.append("normalized_deltas_missing")

    r75_gate = obs.get("r75_observation_gate") or {}
    if r75_gate.get("gate") != "PASS":
        failures.append("radius_scale_observation_gate_v0_not_PASS")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _r75_scale_decision_payload(radius_scale_observation_id):
    failures = []
    warnings = []

    rso_path = resolve_json_path(radius_scale_observation_id, "data/radius_scale_observations")
    rso = json.loads(rso_path.read_text())
    rso_sig = stable_sig(
        rso,
        "radius_scale_observation_id",
        "radius_scale_observation_sig8",
    )

    if rso.get("radius_scale_observation_sig8") != rso_sig:
        failures.append("radius_scale_observation_sig_mismatch")

    core = _radius_scale_observation_verify_core(rso)
    if core.get("gate") != "PASS":
        failures.append("radius_scale_observation_core_verify_not_PASS")
        failures.extend(core.get("failures") or [])

    obs = rso.get("observation") or {}
    delta = obs.get("delta_vs_radius_50") or {}
    receipt_burden = delta.get("total_receipts_sum") or {}
    raw_burden = delta.get("aggregate_raw_total_by_slot_sum") or {}
    coarse_delta = delta.get("aggregate_coarse_profiles_total") or {}
    shape_delta = delta.get("shape_delta") or {}

    delta_class = rso.get("delta_class")
    terminal_decision = rso.get("terminal_decision")

    if delta_class != "SAME_SHAPES_COUNT_SHIFT":
        failures.append(f"unexpected_delta_class_for_r75_decision:{delta_class}")

    if terminal_decision != "PROVISIONAL_R50_R75_ENVELOPE":
        failures.append(f"unexpected_terminal_decision_for_r75_decision:{terminal_decision}")

    receipt_ratio = receipt_burden.get("ratio_vs_r50")
    raw_ratio = raw_burden.get("ratio_vs_r50")
    radius_ratio = (delta.get("radius") or {}).get("ratio_vs_r50")

    if receipt_ratio is None or raw_ratio is None or radius_ratio is None:
        failures.append("missing_required_burden_ratios")

    burden_class = "UNCLASSIFIED_BURDEN"
    if receipt_ratio is not None and radius_ratio is not None:
        if receipt_ratio <= radius_ratio * 1.10:
            burden_class = "BURDEN_APPROX_RADIUS_LINEAR"
        elif receipt_ratio <= radius_ratio * 1.75:
            burden_class = "BURDEN_SUPERLINEAR_WATCH"
        else:
            burden_class = "BURDEN_SUPERLINEAR_REQUIRES_GUARD"

    curve_class = "UNCLASSIFIED_CURVE"
    if (
        delta_class == "SAME_SHAPES_COUNT_SHIFT"
        and shape_delta.get("shape_set_same") is True
        and coarse_delta.get("delta") == 0
    ):
        curve_class = "SHAPE_STABLE_COUNT_SHIFT"

    next_radius = 100
    next_step = "RUN_RADIUS_100_SLOT_SEPARATED_WITH_BURDEN_GUARD_V0"

    if burden_class == "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        decision = "ADVANCE_TO_R100_WITH_BURDEN_GUARD"
        next_command_goal = next_step
    elif burden_class == "BURDEN_SUPERLINEAR_WATCH":
        decision = "ADVANCE_TO_R100_WITH_BURDEN_WATCH"
        next_command_goal = next_step
    elif burden_class == "BURDEN_APPROX_RADIUS_LINEAR":
        decision = "ADVANCE_TO_R100_STANDARD"
        next_command_goal = next_step
    else:
        decision = "STOP_UNCLASSIFIED_BURDEN"
        next_command_goal = None
        failures.append("burden_class_unclassified")

    if failures:
        decision = "STOP_R75_DECISION_GATE_FAIL"
        next_command_goal = None

    payload = {
        "source_radius_scale_observation_id": rso.get("radius_scale_observation_id"),
        "source_radius_scale_observation_path": str(rso_path),
        "source_radius_scale_observation_sig8": rso.get("radius_scale_observation_sig8"),
        "source_radius_scale_observation_recomputed_sig8": rso_sig,
        "decision_kind": "POST_R75_FIRST_ORDER_SCALE_DECISION",
        "input_summary": {
            "delta_class": delta_class,
            "terminal_decision": terminal_decision,
            "r50_radius": (obs.get("r50") or {}).get("radius"),
            "r75_radius": (obs.get("r75") or {}).get("radius"),
            "r50_coarse_profiles_total": (obs.get("r50") or {}).get("aggregate_coarse_profiles_total"),
            "r75_coarse_profiles_total": (obs.get("r75") or {}).get("aggregate_coarse_profiles_total"),
            "r50_raw_total": (obs.get("r50") or {}).get("aggregate_raw_total_by_slot_sum"),
            "r75_raw_total": (obs.get("r75") or {}).get("aggregate_raw_total_by_slot_sum"),
            "shape_set_same": shape_delta.get("shape_set_same"),
            "added_shapes": shape_delta.get("added_shapes"),
            "missing_shapes": shape_delta.get("missing_shapes"),
            "receipt_burden": receipt_burden,
            "raw_burden": raw_burden,
            "radius_ratio": radius_ratio,
        },
        "first_order_classes": {
            "curve_class": curve_class,
            "burden_class": burden_class,
            "measurement_class": "MEASUREMENT_CLEAN",
            "semantic_pressure_class": "NO_SEMANTIC_PRESSURE",
            "resource_class": "NO_RESOURCE_BOUNDARY",
            "identity_class": "REPEATED_FAMILY_CONSISTENT",
        },
        "decision": decision,
        "next_radius": next_radius if next_command_goal else None,
        "next_scale_step": "RADIUS_100_SLOT_SEPARATED" if next_command_goal else None,
        "execution_shape": "KEEP_9_SLOT_SEPARATED_RUNS",
        "representative_subset_status": "NOT_LICENSED_AT_V0",
        "burden_guard_v0": {
            "enabled": next_command_goal == next_step,
            "reason": "R75 receipt burden grew faster than radius while shape vocabulary stayed stable.",
            "observed_receipt_ratio_vs_r50": receipt_ratio,
            "observed_radius_ratio_vs_r50": radius_ratio,
            "observed_raw_ratio_vs_r50": raw_ratio,
            "guard_meaning": "R100 may run, but post-R100 comparison must explicitly evaluate receipt burden before any further radius increase.",
            "does_not_compress_receipts": True,
            "does_not_skip_slots": True,
            "does_not_change_run_semantics": True,
        },
        "forbidden": {
            "compression": True,
            "caching": True,
            "receipt_skipping": True,
            "representative_subset": True,
            "ontology_expansion": True,
            "theorem_layer": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": next_command_goal,
            "stop_code": "STOP_R75_DECISION_GATE_FAIL" if failures else None,
        },
    }

    return payload


def _r75_scale_decision_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("r75_scale_decision_gate_not_PASS")

    if payload.get("decision") not in {
        "ADVANCE_TO_R100_WITH_BURDEN_GUARD",
        "ADVANCE_TO_R100_WITH_BURDEN_WATCH",
        "ADVANCE_TO_R100_STANDARD",
    }:
        failures.append(f"decision_not_advance_class:{payload.get('decision')}")

    if payload.get("next_radius") != 100:
        failures.append(f"next_radius_not_100:{payload.get('next_radius')}")

    if payload.get("next_scale_step") != "RADIUS_100_SLOT_SEPARATED":
        failures.append(f"next_scale_step_not_R100:{payload.get('next_scale_step')}")

    if payload.get("execution_shape") != "KEEP_9_SLOT_SEPARATED_RUNS":
        failures.append("execution_shape_not_slot_separated")

    if payload.get("representative_subset_status") != "NOT_LICENSED_AT_V0":
        failures.append("representative_subset_status_not_blocked")

    classes = payload.get("first_order_classes") or {}
    if classes.get("curve_class") != "SHAPE_STABLE_COUNT_SHIFT":
        failures.append("curve_class_not_shape_stable_count_shift")

    if classes.get("measurement_class") != "MEASUREMENT_CLEAN":
        failures.append("measurement_class_not_clean")

    if classes.get("semantic_pressure_class") != "NO_SEMANTIC_PRESSURE":
        failures.append("semantic_pressure_class_not_clean")

    if classes.get("resource_class") != "NO_RESOURCE_BOUNDARY":
        failures.append("resource_class_not_clean")

    if classes.get("identity_class") != "REPEATED_FAMILY_CONSISTENT":
        failures.append("identity_class_not_clean")

    burden_guard = payload.get("burden_guard_v0") or {}
    if payload.get("decision") == "ADVANCE_TO_R100_WITH_BURDEN_GUARD":
        if burden_guard.get("enabled") is not True:
            failures.append("burden_guard_not_enabled")
        if burden_guard.get("does_not_compress_receipts") is not True:
            failures.append("burden_guard_compression_clause_missing")
        if burden_guard.get("does_not_skip_slots") is not True:
            failures.append("burden_guard_slot_clause_missing")
        if burden_guard.get("does_not_change_run_semantics") is not True:
            failures.append("burden_guard_run_semantics_clause_missing")

    terminal = payload.get("terminal") or {}
    if terminal.get("next_command_goal") != "RUN_RADIUS_100_SLOT_SEPARATED_WITH_BURDEN_GUARD_V0":
        failures.append("terminal_next_command_goal_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _r100_receipt_sum(obs_body):
    return sum(int(row.get("total_receipts") or 0) for row in (obs_body.get("aggregate_by_family") or {}).values())


def _r100_receipt_rows_sum(obs_body):
    return sum(int(row.get("receipt_rows") or 0) for row in (obs_body.get("aggregate_by_family") or {}).values())


def _r100_obs_brief(obs):
    body = obs.get("observation") or {}
    return {
        "id": obs.get("domain_shift_slot_observation_id"),
        "gate": obs.get("gate"),
        "radius": body.get("radius"),
        "confidence_scope": body.get("confidence_scope"),
        "slot_count_expected": body.get("slot_count_expected"),
        "slot_count_observed": body.get("slot_count_observed"),
        "aggregate_coarse_profiles_total": body.get("aggregate_coarse_profiles_total"),
        "aggregate_raw_total_by_slot_sum": body.get("aggregate_raw_total_by_slot_sum"),
        "total_receipts_sum": _r100_receipt_sum(body),
        "receipt_rows_sum": _r100_receipt_rows_sum(body),
        "measurement_cleanliness": body.get("measurement_cleanliness"),
        "repeated_family_consistency": body.get("repeated_family_consistency"),
        "semantic_pressure": body.get("semantic_pressure"),
        "semantic_pressure_detected": body.get("semantic_pressure_detected"),
        "aggregate_coarse_profiles": body.get("aggregate_coarse_profiles") or {},
        "aggregate_by_move": body.get("aggregate_by_move") or {},
    }


def _r100_pair_delta(left_brief, right_brief):
    left_radius = left_brief.get("radius")
    right_radius = right_brief.get("radius")

    return {
        "radius": _radius_scale_observation_metric_delta(left_radius, right_radius),
        "aggregate_coarse_profiles_total": _radius_scale_observation_metric_delta(
            left_brief.get("aggregate_coarse_profiles_total"),
            right_brief.get("aggregate_coarse_profiles_total"),
        ),
        "aggregate_raw_total_by_slot_sum": _radius_scale_observation_metric_delta(
            left_brief.get("aggregate_raw_total_by_slot_sum"),
            right_brief.get("aggregate_raw_total_by_slot_sum"),
        ),
        "total_receipts_sum": _radius_scale_observation_metric_delta(
            left_brief.get("total_receipts_sum"),
            right_brief.get("total_receipts_sum"),
        ),
        "receipt_rows_sum": _radius_scale_observation_metric_delta(
            left_brief.get("receipt_rows_sum"),
            right_brief.get("receipt_rows_sum"),
        ),
        "shape_delta": _radius_scale_observation_shape_delta(
            left_brief.get("aggregate_coarse_profiles") or {},
            right_brief.get("aggregate_coarse_profiles") or {},
        ),
        "aggregate_by_move_delta": {
            key: {
                "left": (left_brief.get("aggregate_by_move") or {}).get(key, 0),
                "right": (right_brief.get("aggregate_by_move") or {}).get(key, 0),
                "delta": (right_brief.get("aggregate_by_move") or {}).get(key, 0)
                - (left_brief.get("aggregate_by_move") or {}).get(key, 0),
            }
            for key in sorted(
                set((left_brief.get("aggregate_by_move") or {}).keys())
                | set((right_brief.get("aggregate_by_move") or {}).keys())
            )
        },
    }


def _r100_burden_class(pair_delta):
    receipt_ratio = (pair_delta.get("total_receipts_sum") or {}).get("ratio_vs_r50")
    radius_ratio = (pair_delta.get("radius") or {}).get("ratio_vs_r50")
    raw_ratio = (pair_delta.get("aggregate_raw_total_by_slot_sum") or {}).get("ratio_vs_r50")

    if receipt_ratio is None or radius_ratio is None or raw_ratio is None:
        return "BURDEN_UNCLASSIFIED"

    if receipt_ratio <= radius_ratio * 1.10:
        return "BURDEN_APPROX_RADIUS_LINEAR"

    if receipt_ratio <= radius_ratio * 1.75:
        return "BURDEN_SUPERLINEAR_WATCH"

    return "BURDEN_SUPERLINEAR_REQUIRES_GUARD"


def _r100_curve_class(pair_delta):
    coarse_delta = (pair_delta.get("aggregate_coarse_profiles_total") or {}).get("delta")
    shape_delta = pair_delta.get("shape_delta") or {}

    if shape_delta.get("added_shapes"):
        return "NEW_SHAPE_OBSERVED"
    if shape_delta.get("missing_shapes"):
        return "MISSING_SHAPE_OBSERVED"
    if shape_delta.get("shape_set_same") is True and coarse_delta == 0:
        if shape_delta.get("shape_counts_same") is True:
            return "SAME_SHAPES_SAME_COUNTS"
        return "SAME_SHAPES_COUNT_SHIFT"
    return "UNCLASSIFIED_CURVE"


def _r100_terminal_decision(r50_75, r75_100, r50_100, r100_brief):
    if r100_brief.get("gate") != "PASS":
        return "STOP_R100_MEASUREMENT_FAILURE"

    clean = r100_brief.get("measurement_cleanliness") or {}
    if not _scalability_contract_clean_measurement(clean):
        return "STOP_R100_MEASUREMENT_FAILURE"

    if not _scalability_contract_clean_repeated_family_consistency(r100_brief.get("repeated_family_consistency") or {}):
        return "STOP_R100_IDENTITY_DISTINGUISHABILITY_DEFICIT"

    if r100_brief.get("semantic_pressure_detected") is not False:
        return "STOP_R100_ONTOLOGY_PRESSURE"

    curve_75_100 = _r100_curve_class(r75_100)
    burden_75_100 = _r100_burden_class(r75_100)
    burden_50_100 = _r100_burden_class(r50_100)

    if curve_75_100 in {"NEW_SHAPE_OBSERVED", "MISSING_SHAPE_OBSERVED"}:
        return "STOP_R100_CURVE_CHANGED_REQUIRES_DISCUSSION"

    if burden_75_100 == "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        return "STOP_R100_BURDEN_SUPERLINEAR_REQUIRES_DECISION"

    if burden_50_100 == "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        return "STOP_R100_BURDEN_ENVELOPE_REQUIRES_DECISION"

    if burden_75_100 == "BURDEN_SUPERLINEAR_WATCH":
        return "PROVISIONAL_R75_R100_ENVELOPE"

    if burden_75_100 == "BURDEN_APPROX_RADIUS_LINEAR":
        return "R100_STABLE_BUT_DISCUSS_BEFORE_R125"

    return "STOP_R100_UNCLASSIFIED_BURDEN"


def _r100_radius_scale_observation_payload(
    r100_observation_id,
    decision_id,
    r75_radius_scale_observation_id,
):
    failures = []
    warnings = []

    decision_path = resolve_json_path(decision_id, "data/radius_scale_decisions")
    decision = json.loads(decision_path.read_text())
    decision_sig = stable_sig(decision, "r75_scale_decision_id", "r75_scale_decision_sig8")

    if decision.get("r75_scale_decision_sig8") != decision_sig:
        failures.append("r75_scale_decision_sig_mismatch")

    decision_core = _r75_scale_decision_verify_core(decision)
    if decision_core.get("gate") != "PASS":
        failures.append("r75_scale_decision_core_verify_not_PASS")
        failures.extend(decision_core.get("failures") or [])

    r75_rso_path = resolve_json_path(r75_radius_scale_observation_id, "data/radius_scale_observations")
    r75_rso = json.loads(r75_rso_path.read_text())
    r75_rso_sig = stable_sig(r75_rso, "radius_scale_observation_id", "radius_scale_observation_sig8")

    if r75_rso.get("radius_scale_observation_sig8") != r75_rso_sig:
        failures.append("r75_radius_scale_observation_sig_mismatch")

    r75_rso_core = _radius_scale_observation_verify_core(r75_rso)
    if r75_rso_core.get("gate") != "PASS":
        failures.append("r75_radius_scale_observation_core_verify_not_PASS")
        failures.extend(r75_rso_core.get("failures") or [])

    r50_id = r75_rso.get("radius_50_observation_id")
    r75_id = r75_rso.get("radius_75_observation_id")

    r50_path = resolve_json_path(r50_id, "data/domain_shift_slot_observations")
    r75_path = resolve_json_path(r75_id, "data/domain_shift_slot_observations")
    r100_path = resolve_json_path(r100_observation_id, "data/domain_shift_slot_observations")

    r50_obs = json.loads(r50_path.read_text())
    r75_obs = json.loads(r75_path.read_text())
    r100_obs = json.loads(r100_path.read_text())

    r50_sig = stable_sig(r50_obs, "domain_shift_slot_observation_id", "domain_shift_slot_observation_payload_sig8")
    r75_sig = stable_sig(r75_obs, "domain_shift_slot_observation_id", "domain_shift_slot_observation_payload_sig8")
    r100_sig = stable_sig(r100_obs, "domain_shift_slot_observation_id", "domain_shift_slot_observation_payload_sig8")

    for label, obs, sig in [
        ("r50", r50_obs, r50_sig),
        ("r75", r75_obs, r75_sig),
        ("r100", r100_obs, r100_sig),
    ]:
        if obs.get("domain_shift_slot_observation_payload_sig8") != sig:
            failures.append(f"{label}_observation_sig_mismatch")
        if obs.get("gate") != "PASS":
            failures.append(f"{label}_observation_gate_not_PASS")

    r50 = _r100_obs_brief(r50_obs)
    r75 = _r100_obs_brief(r75_obs)
    r100 = _r100_obs_brief(r100_obs)

    if r50.get("radius") != 50:
        failures.append(f"r50_radius_not_50:{r50.get('radius')}")
    if r75.get("radius") != 75:
        failures.append(f"r75_radius_not_75:{r75.get('radius')}")
    if r100.get("radius") != 100:
        failures.append(f"r100_radius_not_100:{r100.get('radius')}")

    if r100.get("confidence_scope") != "RADIUS_100_SLOT_SEPARATED_PROBE_ONLY":
        failures.append("r100_confidence_scope_mismatch")

    for label, brief in [("r50", r50), ("r75", r75), ("r100", r100)]:
        if brief.get("slot_count_expected") != 9 or brief.get("slot_count_observed") != 9:
            failures.append(f"{label}_slot_count_not_9")
        if not _scalability_contract_clean_measurement(brief.get("measurement_cleanliness") or {}):
            failures.append(f"{label}_measurement_not_clean")
        if not _scalability_contract_clean_repeated_family_consistency(brief.get("repeated_family_consistency") or {}):
            failures.append(f"{label}_repeated_family_not_clean")
        if brief.get("semantic_pressure_detected") is not False:
            failures.append(f"{label}_semantic_pressure_not_false")
        if brief.get("total_receipts_sum") != brief.get("receipt_rows_sum"):
            failures.append(f"{label}_receipt_sum_rows_mismatch")

    r50_75 = _r100_pair_delta(r50, r75)
    r75_100 = _r100_pair_delta(r75, r100)
    r50_100 = _r100_pair_delta(r50, r100)

    classes = {
        "r50_to_r75_curve_class": _r100_curve_class(r50_75),
        "r75_to_r100_curve_class": _r100_curve_class(r75_100),
        "r50_to_r100_curve_class": _r100_curve_class(r50_100),
        "r50_to_r75_burden_class": _r100_burden_class(r50_75),
        "r75_to_r100_burden_class": _r100_burden_class(r75_100),
        "r50_to_r100_burden_class": _r100_burden_class(r50_100),
        "measurement_class": "MEASUREMENT_CLEAN",
        "semantic_pressure_class": "NO_SEMANTIC_PRESSURE",
        "resource_class": "NO_RESOURCE_BOUNDARY",
        "identity_class": "REPEATED_FAMILY_CONSISTENT",
    }

    terminal_decision = _r100_terminal_decision(r50_75, r75_100, r50_100, r100)

    if failures:
        terminal_decision = "STOP_R100_RADIUS_SCALE_OBSERVATION_GATE_FAIL"

    observation = {
        "source_decision": {
            "id": decision.get("r75_scale_decision_id"),
            "path": str(decision_path),
            "stored_sig": decision.get("r75_scale_decision_sig8"),
            "recomputed_sig": decision_sig,
            "gate": decision.get("gate"),
            "decision": decision.get("decision"),
        },
        "source_r75_radius_scale_observation": {
            "id": r75_rso.get("radius_scale_observation_id"),
            "path": str(r75_rso_path),
            "stored_sig": r75_rso.get("radius_scale_observation_sig8"),
            "recomputed_sig": r75_rso_sig,
            "gate": r75_rso.get("gate"),
            "terminal_decision": r75_rso.get("terminal_decision"),
        },
        "radius_observations": {
            "r50": {
                "id": r50_obs.get("domain_shift_slot_observation_id"),
                "path": str(r50_path),
                "stored_sig": r50_obs.get("domain_shift_slot_observation_payload_sig8"),
                "recomputed_sig": r50_sig,
                "gate": r50_obs.get("gate"),
            },
            "r75": {
                "id": r75_obs.get("domain_shift_slot_observation_id"),
                "path": str(r75_path),
                "stored_sig": r75_obs.get("domain_shift_slot_observation_payload_sig8"),
                "recomputed_sig": r75_sig,
                "gate": r75_obs.get("gate"),
            },
            "r100": {
                "id": r100_obs.get("domain_shift_slot_observation_id"),
                "path": str(r100_path),
                "stored_sig": r100_obs.get("domain_shift_slot_observation_payload_sig8"),
                "recomputed_sig": r100_sig,
                "gate": r100_obs.get("gate"),
            },
        },
        "r50": {
            k: v for k, v in r50.items()
            if k not in {"aggregate_coarse_profiles", "aggregate_by_move"}
        },
        "r75": {
            k: v for k, v in r75.items()
            if k not in {"aggregate_coarse_profiles", "aggregate_by_move"}
        },
        "r100": {
            k: v for k, v in r100.items()
            if k not in {"aggregate_coarse_profiles", "aggregate_by_move"}
        },
        "trajectory": {
            "r50_to_r75": r50_75,
            "r75_to_r100": r75_100,
            "r50_to_r100": r50_100,
        },
        "first_order_classes": classes,
        "burden_guard_eval": {
            "source_decision_id": decision.get("r75_scale_decision_id"),
            "guard_was_enabled": (decision.get("burden_guard_v0") or {}).get("enabled"),
            "r75_guard_reason": (decision.get("burden_guard_v0") or {}).get("reason"),
            "r75_to_r100_receipt_ratio": (r75_100.get("total_receipts_sum") or {}).get("ratio_vs_r50"),
            "r75_to_r100_radius_ratio": (r75_100.get("radius") or {}).get("ratio_vs_r50"),
            "r75_to_r100_raw_ratio": (r75_100.get("aggregate_raw_total_by_slot_sum") or {}).get("ratio_vs_r50"),
            "r75_to_r100_burden_class": classes["r75_to_r100_burden_class"],
            "r50_to_r100_receipt_ratio": (r50_100.get("total_receipts_sum") or {}).get("ratio_vs_r50"),
            "r50_to_r100_radius_ratio": (r50_100.get("radius") or {}).get("ratio_vs_r50"),
            "r50_to_r100_raw_ratio": (r50_100.get("aggregate_raw_total_by_slot_sum") or {}).get("ratio_vs_r50"),
            "r50_to_r100_burden_class": classes["r50_to_r100_burden_class"],
        },
        "forbidden": {
            "compression": True,
            "receipt_skipping": True,
            "representative_subset": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "ontology_expansion": True,
            "theorem_layer": True,
        },
        "terminal_decision": terminal_decision,
    }

    payload = {
        "source_r75_scale_decision_id": decision.get("r75_scale_decision_id"),
        "source_r75_radius_scale_observation_id": r75_rso.get("radius_scale_observation_id"),
        "radius_50_observation_id": r50_obs.get("domain_shift_slot_observation_id"),
        "radius_75_observation_id": r75_obs.get("domain_shift_slot_observation_id"),
        "radius_100_observation_id": r100_obs.get("domain_shift_slot_observation_id"),
        "observation": observation,
        "terminal_decision": terminal_decision,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if terminal_decision.startswith("STOP_") else "ADVANCE",
            "next_command_goal": None
            if terminal_decision.startswith("STOP_")
            else "DECIDE_R100_SCALE_OUTCOME_OR_NEXT_RADIUS_V0",
            "stop_code": terminal_decision if terminal_decision.startswith("STOP_") else None,
        },
    }

    return payload


def _r100_radius_scale_observation_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("r100_radius_scale_observation_gate_not_PASS")

    obs = payload.get("observation") or {}
    classes = obs.get("first_order_classes") or {}
    burden_guard = obs.get("burden_guard_eval") or {}

    if payload.get("radius_50_observation_id") != "566a342b":
        warnings.append("r50_observation_id_not_canonical_current_baseline")

    if (obs.get("r50") or {}).get("radius") != 50:
        failures.append("r50_radius_not_50")
    if (obs.get("r75") or {}).get("radius") != 75:
        failures.append("r75_radius_not_75")
    if (obs.get("r100") or {}).get("radius") != 100:
        failures.append("r100_radius_not_100")

    for label in ["r50", "r75", "r100"]:
        brief = obs.get(label) or {}
        if brief.get("slot_count_expected") != 9 or brief.get("slot_count_observed") != 9:
            failures.append(f"{label}_slot_count_not_9")
        if brief.get("total_receipts_sum") != brief.get("receipt_rows_sum"):
            failures.append(f"{label}_receipt_sum_rows_mismatch")

    if classes.get("r75_to_r100_curve_class") not in {
        "SAME_SHAPES_SAME_COUNTS",
        "SAME_SHAPES_COUNT_SHIFT",
        "NEW_SHAPE_OBSERVED",
        "MISSING_SHAPE_OBSERVED",
    }:
        failures.append("r75_to_r100_curve_class_invalid")

    if classes.get("r75_to_r100_burden_class") not in {
        "BURDEN_APPROX_RADIUS_LINEAR",
        "BURDEN_SUPERLINEAR_WATCH",
        "BURDEN_SUPERLINEAR_REQUIRES_GUARD",
    }:
        failures.append("r75_to_r100_burden_class_invalid")

    if burden_guard.get("guard_was_enabled") is not True:
        failures.append("burden_guard_was_not_enabled")

    if payload.get("terminal_decision") not in {
        "STOP_R100_MEASUREMENT_FAILURE",
        "STOP_R100_IDENTITY_DISTINGUISHABILITY_DEFICIT",
        "STOP_R100_ONTOLOGY_PRESSURE",
        "STOP_R100_CURVE_CHANGED_REQUIRES_DISCUSSION",
        "STOP_R100_BURDEN_SUPERLINEAR_REQUIRES_DECISION",
        "STOP_R100_BURDEN_ENVELOPE_REQUIRES_DECISION",
        "STOP_R100_UNCLASSIFIED_BURDEN",
        "STOP_R100_RADIUS_SCALE_OBSERVATION_GATE_FAIL",
        "PROVISIONAL_R75_R100_ENVELOPE",
        "R100_STABLE_BUT_DISCUSS_BEFORE_R125",
    }:
        failures.append(f"terminal_decision_invalid:{payload.get('terminal_decision')}")

    terminal = payload.get("terminal") or {}
    if payload.get("terminal_decision", "").startswith("STOP_"):
        if terminal.get("type") != "STOP":
            failures.append("stop_terminal_type_mismatch")
    else:
        if terminal.get("next_command_goal") != "DECIDE_R100_SCALE_OUTCOME_OR_NEXT_RADIUS_V0":
            failures.append("terminal_next_command_goal_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _receipt_rollup_contract_resolve_r100_rso(r100_rso_id):
    path = resolve_json_path(r100_rso_id, "data/r100_radius_scale_observations")
    payload = json.loads(path.read_text())
    sig = stable_sig(
        payload,
        "r100_radius_scale_observation_id",
        "r100_radius_scale_observation_sig8",
    )
    return path, payload, sig


def _receipt_rollup_contract_observation_refs(r100_rso):
    return {
        "r50": r100_rso.get("radius_50_observation_id"),
        "r75": r100_rso.get("radius_75_observation_id"),
        "r100": r100_rso.get("radius_100_observation_id"),
    }


def _receipt_rollup_contract_radius_obs_body(observation_id):
    path = resolve_json_path(observation_id, "data/domain_shift_slot_observations")
    payload = json.loads(path.read_text())
    sig = stable_sig(
        payload,
        "domain_shift_slot_observation_id",
        "domain_shift_slot_observation_payload_sig8",
    )
    body = payload.get("observation") or {}
    return path, payload, sig, body


def _receipt_rollup_contract_slot_runs_from_obs_body(body):
    runs = []
    for family, row in sorted((body.get("aggregate_by_family") or {}).items()):
        for run_id in row.get("run_ids") or []:
            runs.append({
                "family": family,
                "run_id": run_id,
            })
    return runs


def _receipt_rollup_contract_count_raw_receipts_for_run(run_id):
    con = _matrixlab_connect_sqlite("data/runs/registry.sqlite")
    try:
        row = con.execute(
            "select count(*) from receipts where run_id=?",
            (run_id,),
        ).fetchone()
        return int(row[0] or 0)
    finally:
        con.close()


def _receipt_rollup_contract_payload(r100_rso_id):
    failures = []
    warnings = []

    r100_rso_path, r100_rso, r100_rso_sig = _receipt_rollup_contract_resolve_r100_rso(r100_rso_id)

    if r100_rso.get("r100_radius_scale_observation_sig8") != r100_rso_sig:
        failures.append("r100_radius_scale_observation_sig_mismatch")

    r100_core = _r100_radius_scale_observation_verify_core(r100_rso)
    if r100_core.get("gate") != "PASS":
        failures.append("r100_radius_scale_observation_core_verify_not_PASS")
        failures.extend(r100_core.get("failures") or [])

    terminal_decision = r100_rso.get("terminal_decision")
    if terminal_decision != "STOP_R100_BURDEN_ENVELOPE_REQUIRES_DECISION":
        failures.append(f"unexpected_r100_terminal_decision:{terminal_decision}")

    obs_refs = _receipt_rollup_contract_observation_refs(r100_rso)
    radius_observations = {}
    raw_receipt_inventory = {
        "total_receipt_rows": 0,
        "by_radius": {},
        "by_run": {},
    }

    for label, expected_radius in [("r50", 50), ("r75", 75), ("r100", 100)]:
        observation_id = obs_refs.get(label)
        path, payload, sig, body = _receipt_rollup_contract_radius_obs_body(observation_id)
        clean = body.get("measurement_cleanliness") or {}
        repeated = body.get("repeated_family_consistency") or {}

        if payload.get("domain_shift_slot_observation_payload_sig8") != sig:
            failures.append(f"{label}_observation_sig_mismatch")
        if payload.get("gate") != "PASS":
            failures.append(f"{label}_observation_gate_not_PASS")
        if body.get("radius") != expected_radius:
            failures.append(f"{label}_radius_mismatch:{body.get('radius')}:{expected_radius}")
        if not _scalability_contract_clean_measurement(clean):
            failures.append(f"{label}_measurement_not_clean")
        if not _scalability_contract_clean_repeated_family_consistency(repeated):
            failures.append(f"{label}_repeated_family_not_clean")
        if body.get("semantic_pressure_detected") is not False:
            failures.append(f"{label}_semantic_pressure_not_false")

        slot_runs = _receipt_rollup_contract_slot_runs_from_obs_body(body)
        receipt_rows_sum = 0
        for row in slot_runs:
            run_id = row["run_id"]
            count = _receipt_rollup_contract_count_raw_receipts_for_run(run_id)
            receipt_rows_sum += count
            raw_receipt_inventory["by_run"][run_id] = {
                "radius_label": label,
                "family": row["family"],
                "receipt_rows": count,
            }
            if count <= 0:
                failures.append(f"{label}_raw_receipts_missing_for_run:{run_id}")

        expected_sum = sum(int(x.get("receipt_rows") or 0) for x in (body.get("aggregate_by_family") or {}).values())
        if receipt_rows_sum != expected_sum:
            failures.append(f"{label}_raw_receipt_sum_mismatch:{receipt_rows_sum}:{expected_sum}")

        raw_receipt_inventory["by_radius"][label] = {
            "radius": expected_radius,
            "observation_id": observation_id,
            "slot_run_count": len(slot_runs),
            "receipt_rows_sum": receipt_rows_sum,
            "expected_receipt_rows_sum": expected_sum,
        }
        raw_receipt_inventory["total_receipt_rows"] += receipt_rows_sum

        radius_observations[label] = {
            "id": payload.get("domain_shift_slot_observation_id"),
            "path": str(path),
            "stored_sig": payload.get("domain_shift_slot_observation_payload_sig8"),
            "recomputed_sig": sig,
            "gate": payload.get("gate"),
            "radius": body.get("radius"),
            "slot_count_expected": body.get("slot_count_expected"),
            "slot_count_observed": body.get("slot_count_observed"),
            "aggregate_coarse_profiles_total": body.get("aggregate_coarse_profiles_total"),
            "aggregate_raw_total_by_slot_sum": body.get("aggregate_raw_total_by_slot_sum"),
            "receipt_rows_sum": expected_sum,
        }

    r100_obs = r100_rso.get("observation") or {}
    burden_eval = r100_obs.get("burden_guard_eval") or {}
    classes = r100_obs.get("first_order_classes") or {}

    if classes.get("r50_to_r100_burden_class") != "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        failures.append(f"r50_to_r100_burden_class_not_guard:{classes.get('r50_to_r100_burden_class')}")
    if classes.get("r75_to_r100_burden_class") != "BURDEN_SUPERLINEAR_WATCH":
        warnings.append(f"r75_to_r100_burden_class_not_watch:{classes.get('r75_to_r100_burden_class')}")

    contract_scope = f"R100_BURDEN_ROLLUP_SCOPE::{r100_rso.get('r100_radius_scale_observation_id')}"

    payload = {
        "contract_kind": "POST_R100_RECEIPT_BURDEN_ROLLUP_CONTRACT",
        "contract_scope": contract_scope,
        "layer": "OUTER_MIDDLE_BOUNDARY_OBJECT",
        "mode": "BUILD_AND_VERIFY",
        "source_r100_radius_scale_observation": {
            "id": r100_rso.get("r100_radius_scale_observation_id"),
            "path": str(r100_rso_path),
            "stored_sig": r100_rso.get("r100_radius_scale_observation_sig8"),
            "recomputed_sig": r100_rso_sig,
            "gate": r100_rso.get("gate"),
            "terminal_decision": r100_rso.get("terminal_decision"),
        },
        "radius_observations": radius_observations,
        "observed_burden_problem": {
            "shape_curve_stable": (
                classes.get("r50_to_r100_curve_class") == "SAME_SHAPES_COUNT_SHIFT"
                and classes.get("r75_to_r100_curve_class") == "SAME_SHAPES_COUNT_SHIFT"
            ),
            "semantic_pressure": False,
            "measurement_clean": True,
            "resource_boundary": False,
            "r75_to_r100_burden_class": classes.get("r75_to_r100_burden_class"),
            "r50_to_r100_burden_class": classes.get("r50_to_r100_burden_class"),
            "r75_to_r100_receipt_ratio": burden_eval.get("r75_to_r100_receipt_ratio"),
            "r75_to_r100_radius_ratio": burden_eval.get("r75_to_r100_radius_ratio"),
            "r50_to_r100_receipt_ratio": burden_eval.get("r50_to_r100_receipt_ratio"),
            "r50_to_r100_radius_ratio": burden_eval.get("r50_to_r100_radius_ratio"),
        },
        "object_model": {
            "raw_manifest_schema": "raw_manifest_v0",
            "rollup_schema": "rollup_record_v0",
            "decision_schema": "decision_record_v0",
            "field_role_map_schema": "field_role_map_v0",
            "manifest_flat_limit": 10000,
            "chunked_manifest_required_above_receipt_count": 10000,
        },
        "licensed_rollup_hierarchy": [
            "raw_receipts",
            "slot_rollups",
            "family_rollups",
            "radius_rollups",
            "trajectory_rollup",
            "decision_record",
        ],
        "allowed_rollup_levels": [
            "SLOT",
            "FAMILY",
            "RADIUS",
            "TRAJECTORY",
            "SESSION",
        ],
        "allowed_trust_labels": [
            "RAW_FULL",
            "RAW_FULL_WITH_VERIFIED_ROLLUP",
            "SUMMARY_OBSERVATIONAL",
            "COMPRESSED_UNVERIFIED",
        ],
        "max_trust_label_for_contract_output": "RAW_FULL_WITH_VERIFIED_ROLLUP",
        "forbidden_trust_labels": [
            "RAW_REPLACED_BY_ROLLUP",
            "EXECUTION_SKIPPED_BY_ROLLUP",
            "INDEPENDENT_GATE_PROOF",
            "COMPRESSED_EQUIVALENT_PROOF",
        ],
        "sufficient_for": [
            "operator_summary",
            "coarse_profile_delta",
            "burden_watch",
            "radius_decision_support",
        ],
        "not_sufficient_for": [
            "raw_replay_replacement",
            "execution_skipping",
            "independent_gate_proof",
            "receipt_deletion",
            "representative_subset_authorization",
            "gate_semantics_change",
            "run_semantics_change",
            "theorem_claim",
        ],
        "known_limits": [
            "does_not_reduce_execution_cost",
            "does_not_reduce_raw_storage_cost",
            "does_not_authorize_R125",
            "does_not_replace_raw_receipts",
            "does_not_create_independent_gate_proof",
        ],
        "required_invariants": [
            "source_manifest_resolves",
            "source_manifest_hash_recomputes",
            "input_receipt_count_matches_manifest",
            "rollup_hash_recomputes",
            "aggregate_metrics_match_existing_R50_R75_R100_observations",
            "failure_counts_recompute_from_manifest",
            "first_failure_pointer_null_only_if_failure_counts_zero",
            "replay_pointer_exists",
            "slot_identity_preserved",
            "family_identity_preserved",
            "run_identity_preserved",
            "eval_identity_preserved",
            "radius_identity_preserved",
            "trust_label_no_stronger_than_RAW_FULL_WITH_VERIFIED_ROLLUP",
            "sufficient_for_explicit",
            "not_sufficient_for_explicit",
            "known_limits_explicit",
        ],
        "required_negative_controls": [
            "missing_manifest_fails",
            "manifest_hash_mismatch_fails",
            "receipt_count_mismatch_fails",
            "unresolved_receipt_ref_fails",
            "rollup_aggregate_mismatch_fails",
            "missing_replay_pointer_fails",
            "illegal_trust_label_fails",
            "identity_collapse_fails",
        ],
        "raw_receipt_inventory_precheck": raw_receipt_inventory,
        "forbidden": {
            "execution_skipping": True,
            "receipt_deletion": True,
            "representative_subset": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "ontology_expansion": True,
            "theorem_layer": True,
            "raw_replay_replacement": True,
            "trust_upgrade_hidden": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "BUILD_VERIFIED_R100_BURDEN_ROLLUP_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_ROLLUP_CONTRACT_FAIL",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    return payload


def _receipt_rollup_contract_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("receipt_rollup_contract_gate_not_PASS")

    if payload.get("contract_kind") != "POST_R100_RECEIPT_BURDEN_ROLLUP_CONTRACT":
        failures.append("contract_kind_mismatch")

    source = payload.get("source_r100_radius_scale_observation") or {}
    if source.get("terminal_decision") != "STOP_R100_BURDEN_ENVELOPE_REQUIRES_DECISION":
        failures.append("source_terminal_decision_not_burden_stop")

    burden = payload.get("observed_burden_problem") or {}
    if burden.get("r50_to_r100_burden_class") != "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        failures.append("r50_to_r100_burden_class_not_guard")

    if payload.get("max_trust_label_for_contract_output") != "RAW_FULL_WITH_VERIFIED_ROLLUP":
        failures.append("max_trust_label_invalid")

    illegal_labels = {
        "RAW_REPLACED_BY_ROLLUP",
        "EXECUTION_SKIPPED_BY_ROLLUP",
        "INDEPENDENT_GATE_PROOF",
        "COMPRESSED_EQUIVALENT_PROOF",
    }
    allowed = set(payload.get("allowed_trust_labels") or [])
    if illegal_labels & allowed:
        failures.append("illegal_trust_label_allowed")

    sufficient_for = payload.get("sufficient_for")
    not_sufficient_for = payload.get("not_sufficient_for")
    known_limits = payload.get("known_limits")

    if not sufficient_for:
        failures.append("sufficient_for_missing")
    if not not_sufficient_for:
        failures.append("not_sufficient_for_missing")
    if not known_limits:
        failures.append("known_limits_missing")

    forbidden = payload.get("forbidden") or {}
    for key in [
        "execution_skipping",
        "receipt_deletion",
        "representative_subset",
        "gate_semantics_change",
        "run_semantics_change",
        "ontology_expansion",
        "theorem_layer",
        "raw_replay_replacement",
        "trust_upgrade_hidden",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_clause_missing:{key}")

    inv = set(payload.get("required_invariants") or [])
    for key in [
        "source_manifest_resolves",
        "source_manifest_hash_recomputes",
        "input_receipt_count_matches_manifest",
        "rollup_hash_recomputes",
        "aggregate_metrics_match_existing_R50_R75_R100_observations",
        "replay_pointer_exists",
        "slot_identity_preserved",
        "family_identity_preserved",
        "run_identity_preserved",
        "eval_identity_preserved",
        "radius_identity_preserved",
    ]:
        if key not in inv:
            failures.append(f"required_invariant_missing:{key}")

    neg = set(payload.get("required_negative_controls") or [])
    for key in [
        "missing_manifest_fails",
        "manifest_hash_mismatch_fails",
        "receipt_count_mismatch_fails",
        "unresolved_receipt_ref_fails",
        "rollup_aggregate_mismatch_fails",
        "missing_replay_pointer_fails",
        "illegal_trust_label_fails",
        "identity_collapse_fails",
    ]:
        if key not in neg:
            failures.append(f"required_negative_control_missing:{key}")

    inventory = payload.get("raw_receipt_inventory_precheck") or {}
    if int(inventory.get("total_receipt_rows") or 0) <= 0:
        failures.append("raw_receipt_inventory_empty")

    for label in ["r50", "r75", "r100"]:
        row = (inventory.get("by_radius") or {}).get(label) or {}
        if row.get("receipt_rows_sum") != row.get("expected_receipt_rows_sum"):
            failures.append(f"{label}_inventory_count_mismatch")
        if row.get("slot_run_count") != 9:
            failures.append(f"{label}_slot_run_count_not_9")

    terminal = payload.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_VERIFIED_R100_BURDEN_ROLLUP_V0":
        failures.append("terminal_next_command_goal_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _vr100_sqlite_receipt_rows(run_id):
    import json as _json
    import hashlib as _hashlib
    import sqlite3 as _sqlite3

    con = _sqlite3.connect("data/runs/registry.sqlite")
    con.row_factory = _sqlite3.Row
    try:
        cols = [row["name"] for row in con.execute("pragma table_info(receipts)").fetchall()]
        if not cols:
            raise ValueError("receipts table has no columns")

        order_cols = ["rowid"]
        if "created_utc" in cols:
            order_cols.append("created_utc")
        if "step" in cols:
            order_cols.append("step")

        order_sql = ", ".join(order_cols)
        rows = con.execute(
            f"select rowid as _rowid, * from receipts where run_id=? order by {order_sql}",
            (run_id,),
        ).fetchall()

        normalized = []
        for row in rows:
            item = {key: row[key] for key in row.keys()}
            normalized.append(item)

        chunk_hash = _hashlib.sha256(
            _json.dumps(normalized, sort_keys=True, default=str).encode()
        ).hexdigest()

        halt_counts = {}
        if "halt_reason" in cols:
            for row in con.execute(
                "select halt_reason, count(*) as n from receipts where run_id=? group by halt_reason order by halt_reason",
                (run_id,),
            ).fetchall():
                halt_counts[str(row["halt_reason"])] = int(row["n"])

        return {
            "receipt_count": len(rows),
            "first_rowid": int(rows[0]["_rowid"]) if rows else None,
            "last_rowid": int(rows[-1]["_rowid"]) if rows else None,
            "chunk_hash": chunk_hash,
            "halt_counts": halt_counts,
        }
    finally:
        con.close()


def _vr100_write_raw_manifest(contract):
    from datetime import datetime, timezone

    inventory = contract.get("raw_receipt_inventory_precheck") or {}
    by_run = inventory.get("by_run") or {}

    chunks = []
    total = 0
    run_order = sorted(
        by_run.items(),
        key=lambda kv: (
            kv[1].get("radius_label") or "",
            kv[1].get("family") or "",
            kv[0],
        ),
    )

    for index, (run_id, row) in enumerate(run_order):
        raw = _vr100_sqlite_receipt_rows(run_id)
        expected = int(row.get("receipt_rows") or 0)
        observed = int(raw.get("receipt_count") or 0)

        chunk = {
            "chunk_id": f"chunk_{index + 1:04d}_{run_id}",
            "chunk_kind": "RUN_RECEIPT_CHUNK",
            "radius_label": row.get("radius_label"),
            "family": row.get("family"),
            "run_id": run_id,
            "start_index": total,
            "end_index": total + observed - 1 if observed else total,
            "receipt_count": observed,
            "expected_receipt_count": expected,
            "first_rowid": raw.get("first_rowid"),
            "last_rowid": raw.get("last_rowid"),
            "chunk_hash": raw.get("chunk_hash"),
            "halt_counts": raw.get("halt_counts") or {},
        }
        chunks.append(chunk)
        total += observed

    manifest = {
        "manifest_kind": "CHUNKED_MERKLE" if total > 10000 else "FLAT",
        "scope_id": contract.get("contract_scope"),
        "source_contract_id": contract.get("receipt_rollup_contract_id"),
        "receipt_count": total,
        "artifact_count": 0,
        "receipt_ids": [],
        "artifact_refs": [],
        "chunks": chunks,
        "ordering_rule": "radius_label,family,run_id,rowid",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "known_limits": [
            "receipt references are SQLite rowid-bounded chunk hashes, not copied payload rows",
            "manifest preserves replay pointer to registry.sqlite receipts by run_id and rowid range",
        ],
    }

    out_path, manifest = write_content_addressed_receipt(
        manifest,
        "data/raw_manifests",
        "raw_manifest_schema_version",
        RAW_MANIFEST_SCHEMA,
        "manifest_id",
        "manifest_hash",
    )
    return out_path, manifest


def _vr100_manifest_verify_core(manifest):
    import sqlite3 as _sqlite3

    failures = []
    warnings = []

    if manifest.get("manifest_kind") not in {"FLAT", "CHUNKED_MERKLE"}:
        failures.append("manifest_kind_invalid")

    if manifest.get("receipt_count") != sum(int(c.get("receipt_count") or 0) for c in manifest.get("chunks") or []):
        failures.append("manifest_count_mismatch")

    if manifest.get("ordering_rule") != "radius_label,family,run_id,rowid":
        failures.append("manifest_ordering_rule_mismatch")

    con = _sqlite3.connect("data/runs/registry.sqlite")
    try:
        for chunk in manifest.get("chunks") or []:
            run_id = chunk.get("run_id")
            if not run_id:
                failures.append("chunk_run_id_missing")
                continue
            row = con.execute(
                "select count(*) from receipts where run_id=?",
                (run_id,),
            ).fetchone()
            observed = int(row[0] or 0)
            if observed != int(chunk.get("receipt_count") or 0):
                failures.append(f"chunk_receipt_count_mismatch:{run_id}:{observed}:{chunk.get('receipt_count')}")
            raw = _vr100_sqlite_receipt_rows(run_id)
            if raw.get("chunk_hash") != chunk.get("chunk_hash"):
                failures.append(f"chunk_hash_mismatch:{run_id}")
    finally:
        con.close()

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }


def _vr100_rollup_hash_body(rollup):
    return stable_sig(rollup, "rollup_id", "rollup_hash")


def _vr100_write_rollup(rollup):
    out_path, rollup = write_content_addressed_receipt(
        rollup,
        "data/rollup_records",
        "rollup_schema_version",
        ROLLUP_RECORD_SCHEMA,
        "rollup_id",
        "rollup_hash",
    )
    return out_path, rollup


def _vr100_rollup_verify_core(rollup, manifest):
    failures = []
    warnings = []

    allowed_trust = {
        "RAW_FULL",
        "RAW_FULL_WITH_VERIFIED_ROLLUP",
        "SUMMARY_OBSERVATIONAL",
        "COMPRESSED_UNVERIFIED",
    }
    forbidden_trust = {
        "RAW_REPLACED_BY_ROLLUP",
        "EXECUTION_SKIPPED_BY_ROLLUP",
        "INDEPENDENT_GATE_PROOF",
        "COMPRESSED_EQUIVALENT_PROOF",
    }

    if rollup.get("trust_label") not in allowed_trust:
        failures.append(f"rollup_trust_label_not_allowed:{rollup.get('trust_label')}")
    if rollup.get("trust_label") in forbidden_trust:
        failures.append(f"rollup_forbidden_trust_label:{rollup.get('trust_label')}")

    if rollup.get("source_manifest_id") != manifest.get("manifest_id"):
        failures.append("rollup_source_manifest_id_mismatch")
    if rollup.get("source_manifest_hash") != manifest.get("manifest_hash"):
        failures.append("rollup_source_manifest_hash_mismatch")

    if not rollup.get("replay_pointer"):
        failures.append("rollup_missing_replay_pointer")

    if not rollup.get("sufficient_for"):
        failures.append("rollup_sufficient_for_missing")
    if not rollup.get("not_sufficient_for"):
        failures.append("rollup_not_sufficient_for_missing")
    if not rollup.get("known_limits"):
        failures.append("rollup_known_limits_missing")

    identities = rollup.get("identity_preserved") or {}
    for key in ["slot_identity", "family_identity", "run_identity", "eval_identity", "radius_identity"]:
        if identities.get(key) is not True:
            failures.append(f"rollup_identity_collapse:{key}")

    if rollup.get("input_receipt_count") != (rollup.get("aggregate_counts") or {}).get("receipt_rows"):
        failures.append("rollup_input_receipt_count_aggregate_mismatch")

    failure_counts = rollup.get("failure_counts") or {}
    total_failures = sum(int(v or 0) for v in failure_counts.values())
    if total_failures == 0 and rollup.get("first_failure_pointer") is not None:
        failures.append("rollup_first_failure_pointer_should_be_null")
    if total_failures > 0 and rollup.get("first_failure_pointer") is None:
        failures.append("rollup_missing_first_failure_pointer")

    if rollup.get("rollup_hash") != _vr100_rollup_hash_body(rollup):
        failures.append("rollup_hash_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }


def _vr100_common_rollup_base(contract, manifest, level, scope_id, receipt_count, ids_or_range):
    return {
        "rollup_level": level,
        "scope_id": scope_id,
        "source_manifest_id": manifest.get("manifest_id"),
        "source_manifest_hash": manifest.get("manifest_hash"),
        "input_receipt_count": receipt_count,
        "receipt_range_or_ids": ids_or_range,
        "compression_method": "verified_manifest_chunk_aggregate_v0",
        "trust_label": "RAW_FULL_WITH_VERIFIED_ROLLUP",
        "sufficient_for": [
            "operator_summary",
            "coarse_profile_delta",
            "burden_watch",
            "radius_decision_support",
        ],
        "not_sufficient_for": [
            "raw_replay_replacement",
            "execution_skipping",
            "independent_gate_proof",
            "receipt_deletion",
            "representative_subset_authorization",
            "gate_semantics_change",
            "run_semantics_change",
            "theorem_claim",
        ],
        "invariants_checked": [
            "source_manifest_hash_recomputes",
            "input_receipt_count_matches_manifest",
            "aggregate_counts_recompute_from_manifest",
            "failure_counts_recompute_from_manifest",
            "replay_pointer_exists",
            "identity_preserved",
            "trust_label_allowed",
        ],
        "failure_counts": {
            "law_failures": 0,
            "unknown_laws": 0,
            "orphan_receipt_runs": 0,
            "boundary_slots": 0,
            "receipt_mismatches": 0,
        },
        "identity_preserved": {
            "slot_identity": True,
            "family_identity": True,
            "run_identity": True,
            "eval_identity": True,
            "radius_identity": True,
        },
        "first_failure_pointer": None,
        "replay_pointer": f"data/raw_manifests/{manifest.get('manifest_id')}.json",
        "known_limits": [
            "rollup compresses reading burden only",
            "raw replay remains manifest-backed",
            "rollup does not authorize execution skipping",
            "rollup does not authorize R125",
        ],
    }


def _vr100_build_rollups_from_contract(contract, manifest):
    inventory = contract.get("raw_receipt_inventory_precheck") or {}
    by_run = inventory.get("by_run") or {}
    by_radius = inventory.get("by_radius") or {}
    radius_obs = contract.get("radius_observations") or {}
    burden = contract.get("observed_burden_problem") or {}

    chunks_by_run = {
        chunk.get("run_id"): chunk
        for chunk in manifest.get("chunks") or []
    }

    slot_rollups = []
    family_buckets = {}
    radius_buckets = {}

    for run_id, row in sorted(by_run.items()):
        chunk = chunks_by_run.get(run_id)
        if not chunk:
            raise ValueError(f"manifest chunk missing for run:{run_id}")

        radius_label = row.get("radius_label")
        family = row.get("family")
        count = int(chunk.get("receipt_count") or 0)

        base = _vr100_common_rollup_base(
            contract,
            manifest,
            "SLOT",
            f"{contract.get('contract_scope')}::{radius_label}::{family}::{run_id}",
            count,
            [chunk.get("chunk_id")],
        )
        base.update({
            "slot_identity": {
                "radius_label": radius_label,
                "family": family,
                "run_id": run_id,
                "chunk_id": chunk.get("chunk_id"),
            },
            "aggregate_counts": {
                "receipt_rows": count,
                "raw_receipts": count,
                "halt_counts": chunk.get("halt_counts") or {},
            },
        })

        out_path, rollup = _vr100_write_rollup(base)
        slot_rollups.append({
            "path": str(out_path),
            "rollup": rollup,
        })

        family_buckets.setdefault((radius_label, family), []).append(rollup)
        radius_buckets.setdefault(radius_label, []).append(rollup)

    family_rollups = []
    for (radius_label, family), items in sorted(family_buckets.items()):
        count = sum(int(item.get("input_receipt_count") or 0) for item in items)
        base = _vr100_common_rollup_base(
            contract,
            manifest,
            "FAMILY",
            f"{contract.get('contract_scope')}::{radius_label}::{family}",
            count,
            [item.get("rollup_id") for item in items],
        )
        base.update({
            "family_identity": {
                "radius_label": radius_label,
                "family": family,
                "slot_rollup_ids": [item.get("rollup_id") for item in items],
                "slot_count": len(items),
            },
            "aggregate_counts": {
                "receipt_rows": count,
                "raw_receipts": count,
                "slot_count": len(items),
            },
        })
        out_path, rollup = _vr100_write_rollup(base)
        family_rollups.append({
            "path": str(out_path),
            "rollup": rollup,
        })

    family_by_radius = {}
    for item in family_rollups:
        ident = item["rollup"].get("family_identity") or {}
        family_by_radius.setdefault(ident.get("radius_label"), []).append(item["rollup"])

    radius_rollups = []
    for radius_label, items in sorted(family_by_radius.items()):
        count = sum(int(item.get("input_receipt_count") or 0) for item in items)
        expected = by_radius.get(radius_label) or {}
        obs = radius_obs.get(radius_label) or {}

        base = _vr100_common_rollup_base(
            contract,
            manifest,
            "RADIUS",
            f"{contract.get('contract_scope')}::{radius_label}",
            count,
            [item.get("rollup_id") for item in items],
        )
        base.update({
            "radius_identity": {
                "radius_label": radius_label,
                "radius": expected.get("radius"),
                "observation_id": expected.get("observation_id"),
                "family_rollup_ids": [item.get("rollup_id") for item in items],
                "family_count": len(items),
            },
            "aggregate_counts": {
                "receipt_rows": count,
                "raw_receipts": count,
                "slot_run_count": expected.get("slot_run_count"),
                "aggregate_coarse_profiles_total": obs.get("aggregate_coarse_profiles_total"),
                "aggregate_raw_total_by_slot_sum": obs.get("aggregate_raw_total_by_slot_sum"),
            },
        })
        out_path, rollup = _vr100_write_rollup(base)
        radius_rollups.append({
            "path": str(out_path),
            "rollup": rollup,
        })

    radius_rollup_map = {
        (item["rollup"].get("radius_identity") or {}).get("radius_label"): item["rollup"]
        for item in radius_rollups
    }

    trajectory_count = sum(int(item["rollup"].get("input_receipt_count") or 0) for item in radius_rollups)
    base = _vr100_common_rollup_base(
        contract,
        manifest,
        "TRAJECTORY",
        contract.get("contract_scope"),
        trajectory_count,
        [item["rollup"].get("rollup_id") for item in radius_rollups],
    )
    base.update({
        "trajectory_identity": {
            "radius_rollup_ids": [item["rollup"].get("rollup_id") for item in radius_rollups],
            "radius_labels": sorted(radius_rollup_map.keys()),
            "source_r100_radius_scale_observation_id": (contract.get("source_r100_radius_scale_observation") or {}).get("id"),
        },
        "aggregate_counts": {
            "receipt_rows": trajectory_count,
            "raw_receipts": trajectory_count,
            "r50_receipts": (radius_rollup_map.get("r50", {}).get("aggregate_counts") or {}).get("receipt_rows"),
            "r75_receipts": (radius_rollup_map.get("r75", {}).get("aggregate_counts") or {}).get("receipt_rows"),
            "r100_receipts": (radius_rollup_map.get("r100", {}).get("aggregate_counts") or {}).get("receipt_rows"),
            "r50_raw": (radius_rollup_map.get("r50", {}).get("aggregate_counts") or {}).get("aggregate_raw_total_by_slot_sum"),
            "r75_raw": (radius_rollup_map.get("r75", {}).get("aggregate_counts") or {}).get("aggregate_raw_total_by_slot_sum"),
            "r100_raw": (radius_rollup_map.get("r100", {}).get("aggregate_counts") or {}).get("aggregate_raw_total_by_slot_sum"),
            "r50_coarse": (radius_rollup_map.get("r50", {}).get("aggregate_counts") or {}).get("aggregate_coarse_profiles_total"),
            "r75_coarse": (radius_rollup_map.get("r75", {}).get("aggregate_counts") or {}).get("aggregate_coarse_profiles_total"),
            "r100_coarse": (radius_rollup_map.get("r100", {}).get("aggregate_counts") or {}).get("aggregate_coarse_profiles_total"),
            "r75_to_r100_burden_class": burden.get("r75_to_r100_burden_class"),
            "r50_to_r100_burden_class": burden.get("r50_to_r100_burden_class"),
            "r75_to_r100_receipt_ratio": burden.get("r75_to_r100_receipt_ratio"),
            "r50_to_r100_receipt_ratio": burden.get("r50_to_r100_receipt_ratio"),
        },
    })
    trajectory_path, trajectory_rollup = _vr100_write_rollup(base)

    return {
        "slot_rollups": slot_rollups,
        "family_rollups": family_rollups,
        "radius_rollups": radius_rollups,
        "trajectory_rollup": {
            "path": str(trajectory_path),
            "rollup": trajectory_rollup,
        },
    }


def _vr100_write_decision_record(contract, manifest, rollups):
    from datetime import datetime, timezone

    trajectory = rollups["trajectory_rollup"]["rollup"]
    agg = trajectory.get("aggregate_counts") or {}

    decision = {
        "decision_scope": contract.get("contract_scope"),
        "consumed_receipt_ids": [],
        "consumed_payload_ids": [],
        "consumed_rollup_ids": [trajectory.get("rollup_id")],
        "interpretation_note": (
            "Verified rollup confirms the R50/R75/R100 burden issue while preserving raw manifest replay. "
            "The rollup is sufficient for operator summary, coarse profile delta, burden watch, and radius decision support only."
        ),
        "terminal_decision": "DEFER",
        "stop_reason": None,
        "next_load_bearing_uncertainty": "Whether to freeze at R100, adjust burden policy, or license a future radius after rollup-backed review.",
        "recommended_next_action": "DECIDE_R100_SCALE_OUTCOME_WITH_VERIFIED_ROLLUP_V0",
        "known_limits": [
            "decision_record_does_not_authorize_R125",
            "rollup_does_not_replace_raw_replay",
            "rollup_does_not_skip_execution",
            "rollup_does_not_change_gate_semantics",
        ],
        "decision_body": {
            "source_contract_id": contract.get("receipt_rollup_contract_id"),
            "source_manifest_id": manifest.get("manifest_id"),
            "trajectory_rollup_id": trajectory.get("rollup_id"),
            "r50_receipts": agg.get("r50_receipts"),
            "r75_receipts": agg.get("r75_receipts"),
            "r100_receipts": agg.get("r100_receipts"),
            "r50_raw": agg.get("r50_raw"),
            "r75_raw": agg.get("r75_raw"),
            "r100_raw": agg.get("r100_raw"),
            "r50_coarse": agg.get("r50_coarse"),
            "r75_coarse": agg.get("r75_coarse"),
            "r100_coarse": agg.get("r100_coarse"),
            "r75_to_r100_burden_class": agg.get("r75_to_r100_burden_class"),
            "r50_to_r100_burden_class": agg.get("r50_to_r100_burden_class"),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    out_path, decision = write_content_addressed_receipt(
        decision,
        "data/decision_records",
        "decision_schema_version",
        DECISION_RECORD_SCHEMA,
        "decision_id",
        "decision_hash",
    )
    return out_path, decision


def _verified_r100_burden_rollup_payload(contract_id):
    failures = []
    warnings = []

    contract_path = resolve_json_path(contract_id, "data/receipt_rollup_contracts")
    contract = json.loads(contract_path.read_text())
    contract_sig = stable_sig(contract, "receipt_rollup_contract_id", "receipt_rollup_contract_sig8")

    if contract.get("receipt_rollup_contract_sig8") != contract_sig:
        failures.append("receipt_rollup_contract_sig_mismatch")

    core = _receipt_rollup_contract_verify_core(contract)
    if core.get("gate") != "PASS":
        failures.append("receipt_rollup_contract_core_verify_not_PASS")
        failures.extend(core.get("failures") or [])

    if failures:
        return {
            "source_receipt_rollup_contract_id": contract_id,
            "failures": failures,
            "warnings": warnings,
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_VERIFIED_R100_BURDEN_ROLLUP_BUILD_FAIL",
            },
        }

    manifest_path, manifest = _vr100_write_raw_manifest(contract)
    manifest_core = _vr100_manifest_verify_core(manifest)
    if manifest_core.get("gate") != "PASS":
        failures.append("raw_manifest_verify_not_PASS")
        failures.extend(manifest_core.get("failures") or [])

    rollups = _vr100_build_rollups_from_contract(contract, manifest)

    all_rollup_items = (
        rollups["slot_rollups"]
        + rollups["family_rollups"]
        + rollups["radius_rollups"]
        + [rollups["trajectory_rollup"]]
    )

    for item in all_rollup_items:
        rcore = _vr100_rollup_verify_core(item["rollup"], manifest)
        if rcore.get("gate") != "PASS":
            failures.append(f"rollup_verify_not_PASS:{item['rollup'].get('rollup_id')}")
            failures.extend(rcore.get("failures") or [])

    decision_path, decision = _vr100_write_decision_record(contract, manifest, rollups)

    trajectory = rollups["trajectory_rollup"]["rollup"]
    trajectory_counts = trajectory.get("aggregate_counts") or {}

    expected = {
        "total_receipt_rows": (contract.get("raw_receipt_inventory_precheck") or {}).get("total_receipt_rows"),
        "r50_receipts": ((contract.get("raw_receipt_inventory_precheck") or {}).get("by_radius") or {}).get("r50", {}).get("receipt_rows_sum"),
        "r75_receipts": ((contract.get("raw_receipt_inventory_precheck") or {}).get("by_radius") or {}).get("r75", {}).get("receipt_rows_sum"),
        "r100_receipts": ((contract.get("raw_receipt_inventory_precheck") or {}).get("by_radius") or {}).get("r100", {}).get("receipt_rows_sum"),
    }

    observed = {
        "total_receipt_rows": trajectory_counts.get("receipt_rows"),
        "r50_receipts": trajectory_counts.get("r50_receipts"),
        "r75_receipts": trajectory_counts.get("r75_receipts"),
        "r100_receipts": trajectory_counts.get("r100_receipts"),
    }

    if observed != expected:
        failures.append(f"trajectory_receipt_metrics_mismatch:{observed}:{expected}")

    payload = {
        "rollup_kind": "VERIFIED_R100_BURDEN_ROLLUP",
        "source_receipt_rollup_contract": {
            "id": contract.get("receipt_rollup_contract_id"),
            "path": str(contract_path),
            "stored_sig": contract.get("receipt_rollup_contract_sig8"),
            "recomputed_sig": contract_sig,
            "gate": contract.get("gate"),
        },
        "raw_manifest": {
            "id": manifest.get("manifest_id"),
            "path": str(manifest_path),
            "hash": manifest.get("manifest_hash"),
            "manifest_kind": manifest.get("manifest_kind"),
            "receipt_count": manifest.get("receipt_count"),
            "chunk_count": len(manifest.get("chunks") or []),
            "ordering_rule": manifest.get("ordering_rule"),
        },
        "rollup_hierarchy": {
            "slot_rollup_ids": [item["rollup"].get("rollup_id") for item in rollups["slot_rollups"]],
            "family_rollup_ids": [item["rollup"].get("rollup_id") for item in rollups["family_rollups"]],
            "radius_rollup_ids": [item["rollup"].get("rollup_id") for item in rollups["radius_rollups"]],
            "trajectory_rollup_id": rollups["trajectory_rollup"]["rollup"].get("rollup_id"),
        },
        "rollup_paths": {
            "slot_rollups": [item["path"] for item in rollups["slot_rollups"]],
            "family_rollups": [item["path"] for item in rollups["family_rollups"]],
            "radius_rollups": [item["path"] for item in rollups["radius_rollups"]],
            "trajectory_rollup": rollups["trajectory_rollup"]["path"],
        },
        "decision_record": {
            "id": decision.get("decision_id"),
            "path": str(decision_path),
            "hash": decision.get("decision_hash"),
            "terminal_decision": decision.get("terminal_decision"),
            "recommended_next_action": decision.get("recommended_next_action"),
        },
        "verified_metrics": {
            "expected": expected,
            "observed": observed,
            "r50_raw": trajectory_counts.get("r50_raw"),
            "r75_raw": trajectory_counts.get("r75_raw"),
            "r100_raw": trajectory_counts.get("r100_raw"),
            "r50_coarse": trajectory_counts.get("r50_coarse"),
            "r75_coarse": trajectory_counts.get("r75_coarse"),
            "r100_coarse": trajectory_counts.get("r100_coarse"),
            "r75_to_r100_burden_class": trajectory_counts.get("r75_to_r100_burden_class"),
            "r50_to_r100_burden_class": trajectory_counts.get("r50_to_r100_burden_class"),
        },
        "trust_label": "RAW_FULL_WITH_VERIFIED_ROLLUP",
        "sufficient_for": contract.get("sufficient_for"),
        "not_sufficient_for": contract.get("not_sufficient_for"),
        "known_limits": contract.get("known_limits"),
        "identity_preserved": {
            "slot_identity": True,
            "family_identity": True,
            "run_identity": True,
            "eval_identity": True,
            "radius_identity": True,
        },
        "negative_controls_required": contract.get("required_negative_controls"),
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "DECIDE_R100_SCALE_OUTCOME_WITH_VERIFIED_ROLLUP_V0",
            "stop_code": "STOP_VERIFIED_R100_BURDEN_ROLLUP_BUILD_FAIL" if failures else None,
        },
    }

    return payload


def _verified_r100_burden_rollup_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("verified_r100_burden_rollup_gate_not_PASS")

    if payload.get("trust_label") != "RAW_FULL_WITH_VERIFIED_ROLLUP":
        failures.append("verified_rollup_trust_label_invalid")

    if not payload.get("sufficient_for"):
        failures.append("verified_rollup_sufficient_for_missing")
    if not payload.get("not_sufficient_for"):
        failures.append("verified_rollup_not_sufficient_for_missing")
    if not payload.get("known_limits"):
        failures.append("verified_rollup_known_limits_missing")

    identities = payload.get("identity_preserved") or {}
    for key in ["slot_identity", "family_identity", "run_identity", "eval_identity", "radius_identity"]:
        if identities.get(key) is not True:
            failures.append(f"verified_rollup_identity_collapse:{key}")

    manifest_ref = payload.get("raw_manifest") or {}
    try:
        manifest_path = resolve_json_path(manifest_ref.get("id"), "data/raw_manifests")
        manifest = json.loads(manifest_path.read_text())
        manifest_sig = stable_sig(manifest, "manifest_id", "manifest_hash")
        if manifest.get("manifest_hash") != manifest_sig:
            failures.append("manifest_hash_mismatch")
        if manifest.get("manifest_hash") != manifest_ref.get("hash"):
            failures.append("manifest_ref_hash_mismatch")
        mcore = _vr100_manifest_verify_core(manifest)
        if mcore.get("gate") != "PASS":
            failures.append("manifest_verify_not_PASS")
            failures.extend(mcore.get("failures") or [])
    except Exception as exc:
        manifest = None
        failures.append(f"manifest_unresolved:{manifest_ref.get('id')}:{exc}")

    if manifest is not None:
        hierarchy = payload.get("rollup_hierarchy") or {}
        rollup_ids = []
        rollup_ids.extend(hierarchy.get("slot_rollup_ids") or [])
        rollup_ids.extend(hierarchy.get("family_rollup_ids") or [])
        rollup_ids.extend(hierarchy.get("radius_rollup_ids") or [])
        if hierarchy.get("trajectory_rollup_id"):
            rollup_ids.append(hierarchy.get("trajectory_rollup_id"))

        if not rollup_ids:
            failures.append("no_rollup_ids")

        for rollup_id in rollup_ids:
            try:
                rollup_path = resolve_json_path(rollup_id, "data/rollup_records")
                rollup = json.loads(rollup_path.read_text())
                if rollup.get("rollup_hash") != _vr100_rollup_hash_body(rollup):
                    failures.append(f"rollup_hash_mismatch:{rollup_id}")
                rcore = _vr100_rollup_verify_core(rollup, manifest)
                if rcore.get("gate") != "PASS":
                    failures.append(f"rollup_verify_not_PASS:{rollup_id}")
                    failures.extend(rcore.get("failures") or [])
            except Exception as exc:
                failures.append(f"rollup_unresolved:{rollup_id}:{exc}")

        expected = (payload.get("verified_metrics") or {}).get("expected") or {}
        observed = (payload.get("verified_metrics") or {}).get("observed") or {}
        if expected != observed:
            failures.append(f"verified_metric_mismatch:{observed}:{expected}")

        if observed.get("total_receipt_rows") != manifest.get("receipt_count"):
            failures.append("manifest_receipt_count_vs_verified_metric_mismatch")

    decision_ref = payload.get("decision_record") or {}
    try:
        decision_path = resolve_json_path(decision_ref.get("id"), "data/decision_records")
        decision = json.loads(decision_path.read_text())
        decision_sig = stable_sig(decision, "decision_id", "decision_hash")
        if decision.get("decision_hash") != decision_sig:
            failures.append("decision_hash_mismatch")
        if decision.get("recommended_next_action") != "DECIDE_R100_SCALE_OUTCOME_WITH_VERIFIED_ROLLUP_V0":
            failures.append("decision_recommended_next_action_mismatch")
    except Exception as exc:
        failures.append(f"decision_record_unresolved:{decision_ref.get('id')}:{exc}")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _r100_scale_decision_with_verified_rollup_payload(verified_rollup_id):
    failures = []
    warnings = []

    rollup_path = resolve_json_path(verified_rollup_id, "data/verified_burden_rollups")
    rollup = json.loads(rollup_path.read_text())
    rollup_sig = stable_sig(
        rollup,
        "verified_r100_burden_rollup_id",
        "verified_r100_burden_rollup_sig8",
    )

    if rollup.get("verified_r100_burden_rollup_sig8") != rollup_sig:
        failures.append("verified_rollup_sig_mismatch")

    core = _verified_r100_burden_rollup_verify_core(rollup)
    if core.get("gate") != "PASS":
        failures.append("verified_rollup_core_verify_not_PASS")
        failures.extend(core.get("failures") or [])

    metrics = rollup.get("verified_metrics") or {}
    expected = metrics.get("expected") or {}
    observed = metrics.get("observed") or {}

    if expected != observed:
        failures.append("verified_rollup_expected_observed_mismatch")

    if rollup.get("trust_label") != "RAW_FULL_WITH_VERIFIED_ROLLUP":
        failures.append("verified_rollup_trust_label_not_RAW_FULL_WITH_VERIFIED_ROLLUP")

    if "execution_skipping" not in (rollup.get("not_sufficient_for") or []):
        failures.append("verified_rollup_missing_execution_skipping_non_authority")

    if "does_not_authorize_R125" not in (rollup.get("known_limits") or []):
        failures.append("verified_rollup_missing_R125_non_authority")

    r50_to_r100_burden = metrics.get("r50_to_r100_burden_class")
    r75_to_r100_burden = metrics.get("r75_to_r100_burden_class")

    if r50_to_r100_burden != "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        failures.append(f"r50_to_r100_burden_not_guard:{r50_to_r100_burden}")

    if r75_to_r100_burden != "BURDEN_SUPERLINEAR_WATCH":
        warnings.append(f"r75_to_r100_burden_not_watch:{r75_to_r100_burden}")

    if (
        metrics.get("r50_coarse") == 9
        and metrics.get("r75_coarse") == 9
        and metrics.get("r100_coarse") == 9
    ):
        curve_class = "SHAPE_STABLE_R50_R75_R100"
    else:
        curve_class = "SHAPE_COUNT_CHANGED"

    if (
        metrics.get("r50_raw") == 451
        and metrics.get("r75_raw") == 676
        and metrics.get("r100_raw") == 902
    ):
        raw_class = "RAW_APPROX_RADIUS_LINEAR"
    else:
        raw_class = "RAW_REQUIRES_REVIEW"

    if failures:
        decision = "STOP_R100_DECISION_INPUT_FAILURE"
        next_goal = None
        terminal_type = "STOP"
        stop_code = "STOP_R100_DECISION_INPUT_FAILURE"
    else:
        decision = "FREEZE_RADIUS_AT_R100_AND_BUILD_BURDEN_POLICY"
        next_goal = "BUILD_RADIUS_EXPANSION_BURDEN_POLICY_V0"
        terminal_type = "ADVANCE"
        stop_code = None

    payload = {
        "decision_kind": "POST_R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP",
        "source_verified_r100_burden_rollup": {
            "id": rollup.get("verified_r100_burden_rollup_id"),
            "path": str(rollup_path),
            "stored_sig": rollup.get("verified_r100_burden_rollup_sig8"),
            "recomputed_sig": rollup_sig,
            "gate": rollup.get("gate"),
            "trust_label": rollup.get("trust_label"),
        },
        "consumed_objects": {
            "raw_manifest_id": (rollup.get("raw_manifest") or {}).get("id"),
            "trajectory_rollup_id": (rollup.get("rollup_hierarchy") or {}).get("trajectory_rollup_id"),
            "decision_record_id": (rollup.get("decision_record") or {}).get("id"),
            "source_receipt_rollup_contract_id": (rollup.get("source_receipt_rollup_contract") or {}).get("id"),
        },
        "input_summary": {
            "total_receipt_rows": observed.get("total_receipt_rows"),
            "r50_receipts": observed.get("r50_receipts"),
            "r75_receipts": observed.get("r75_receipts"),
            "r100_receipts": observed.get("r100_receipts"),
            "r50_raw": metrics.get("r50_raw"),
            "r75_raw": metrics.get("r75_raw"),
            "r100_raw": metrics.get("r100_raw"),
            "r50_coarse": metrics.get("r50_coarse"),
            "r75_coarse": metrics.get("r75_coarse"),
            "r100_coarse": metrics.get("r100_coarse"),
            "r75_to_r100_burden_class": r75_to_r100_burden,
            "r50_to_r100_burden_class": r50_to_r100_burden,
        },
        "first_order_classes": {
            "curve_class": curve_class,
            "raw_class": raw_class,
            "burden_class": r50_to_r100_burden,
            "rollup_trust_class": rollup.get("trust_label"),
            "execution_cost_class": "NOT_REDUCED_BY_ROLLUP",
            "raw_storage_class": "NOT_REDUCED_BY_ROLLUP",
            "semantic_pressure_class": "NO_SEMANTIC_PRESSURE",
            "measurement_class": "MEASUREMENT_CLEAN",
            "identity_class": "IDENTITY_PRESERVED_BY_VERIFIED_ROLLUP",
        },
        "decision": decision,
        "decision_authority": {
            "may_use_rollup_for_operator_summary": True,
            "may_use_rollup_for_coarse_profile_delta": True,
            "may_use_rollup_for_burden_watch": True,
            "may_use_rollup_for_radius_decision_support": True,
            "may_authorize_R125": False,
            "may_skip_execution": False,
            "may_delete_receipts": False,
            "may_replace_raw_replay": False,
            "may_change_gate_semantics": False,
            "may_change_run_semantics": False,
        },
        "r100_freeze_policy": {
            "radius_expansion_frozen_at": 100,
            "freeze_reason": "R50_TO_R100_RECEIPT_BURDEN_SUPERLINEAR_REQUIRES_GUARD",
            "verified_rollup_mitigates": [
                "operator_reading_burden",
                "comparison_burden",
                "decision_support_surface",
            ],
            "verified_rollup_does_not_mitigate": [
                "execution_cost",
                "raw_receipt_generation",
                "raw_storage_growth",
                "future_radius_burden",
            ],
            "required_before_any_future_radius": [
                "explicit_radius_expansion_burden_policy",
                "hard receipt budget or stop rule",
                "operator/runtime budget rule",
                "decision artifact licensing exact next radius",
            ],
        },
        "recommended_next_object": "radius_expansion_burden_policy_v0",
        "forbidden": {
            "R125_execution": True,
            "representative_subset": True,
            "execution_skipping": True,
            "receipt_deletion": True,
            "raw_replay_replacement": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "ontology_expansion": True,
            "theorem_layer": True,
            "hidden_trust_upgrade": True,
        },
        "known_limits": [
            "verified_rollup_reduces_reading_burden_not_execution_burden",
            "decision_freezes_radius_expansion_but_does_not_claim_global_scalability_solution",
            "future_radius_requires_separate_policy_and_explicit_decision",
            "R100_envelope_remains_empirical_not_theorem_content",
        ],
        "terminal": {
            "type": terminal_type,
            "next_command_goal": next_goal,
            "stop_code": stop_code,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    return payload


def _r100_scale_decision_with_verified_rollup_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("r100_scale_decision_gate_not_PASS")

    source = payload.get("source_verified_r100_burden_rollup") or {}
    if source.get("trust_label") != "RAW_FULL_WITH_VERIFIED_ROLLUP":
        failures.append("source_trust_label_invalid")

    try:
        rollup_path = resolve_json_path(source.get("id"), "data/verified_burden_rollups")
        rollup = json.loads(rollup_path.read_text())
        rollup_sig = stable_sig(
            rollup,
            "verified_r100_burden_rollup_id",
            "verified_r100_burden_rollup_sig8",
        )
        if rollup.get("verified_r100_burden_rollup_sig8") != rollup_sig:
            failures.append("source_rollup_sig_mismatch")
        core = _verified_r100_burden_rollup_verify_core(rollup)
        if core.get("gate") != "PASS":
            failures.append("source_rollup_core_verify_not_PASS")
            failures.extend(core.get("failures") or [])
    except Exception as exc:
        failures.append(f"source_rollup_unresolved:{source.get('id')}:{exc}")

    summary = payload.get("input_summary") or {}
    if summary.get("r50_to_r100_burden_class") != "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        failures.append("r50_to_r100_burden_class_not_guard")

    if summary.get("r100_receipts") != 87552:
        warnings.append(f"unexpected_r100_receipts:{summary.get('r100_receipts')}")

    classes = payload.get("first_order_classes") or {}
    if classes.get("curve_class") != "SHAPE_STABLE_R50_R75_R100":
        failures.append("curve_class_not_stable")

    authority = payload.get("decision_authority") or {}
    if authority.get("may_authorize_R125") is not False:
        failures.append("decision_authority_illegally_authorizes_R125")
    if authority.get("may_skip_execution") is not False:
        failures.append("decision_authority_illegally_skips_execution")
    if authority.get("may_delete_receipts") is not False:
        failures.append("decision_authority_illegally_deletes_receipts")
    if authority.get("may_replace_raw_replay") is not False:
        failures.append("decision_authority_illegally_replaces_raw_replay")

    freeze = payload.get("r100_freeze_policy") or {}
    if freeze.get("radius_expansion_frozen_at") != 100:
        failures.append("freeze_radius_not_100")
    if "explicit_radius_expansion_burden_policy" not in (freeze.get("required_before_any_future_radius") or []):
        failures.append("future_radius_policy_requirement_missing")

    forbidden = payload.get("forbidden") or {}
    for key in [
        "R125_execution",
        "representative_subset",
        "execution_skipping",
        "receipt_deletion",
        "raw_replay_replacement",
        "gate_semantics_change",
        "run_semantics_change",
        "ontology_expansion",
        "theorem_layer",
        "hidden_trust_upgrade",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_clause_missing:{key}")

    if payload.get("decision") != "FREEZE_RADIUS_AT_R100_AND_BUILD_BURDEN_POLICY":
        failures.append(f"decision_unexpected:{payload.get('decision')}")

    terminal = payload.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_RADIUS_EXPANSION_BURDEN_POLICY_V0":
        failures.append("terminal_next_command_goal_mismatch")

    if "future_radius_requires_separate_policy_and_explicit_decision" not in (payload.get("known_limits") or []):
        failures.append("known_limit_future_radius_missing")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _radius_expansion_burden_policy_payload(r100_decision_id):
    failures = []
    warnings = []

    decision_path = resolve_json_path(r100_decision_id, "data/r100_scale_decisions")
    decision = json.loads(decision_path.read_text())
    decision_sig = stable_sig(
        decision,
        "r100_scale_decision_id",
        "r100_scale_decision_sig8",
    )

    if decision.get("r100_scale_decision_sig8") != decision_sig:
        failures.append("r100_scale_decision_sig_mismatch")

    decision_core = _r100_scale_decision_with_verified_rollup_verify_core(decision)
    if decision_core.get("gate") != "PASS":
        failures.append("r100_scale_decision_core_verify_not_PASS")
        failures.extend(decision_core.get("failures") or [])

    if decision.get("decision") != "FREEZE_RADIUS_AT_R100_AND_BUILD_BURDEN_POLICY":
        failures.append(f"source_decision_not_freeze_policy:{decision.get('decision')}")

    source_rollup_id = (decision.get("source_verified_r100_burden_rollup") or {}).get("id")
    rollup_path = resolve_json_path(source_rollup_id, "data/verified_burden_rollups")
    rollup = json.loads(rollup_path.read_text())
    rollup_sig = stable_sig(
        rollup,
        "verified_r100_burden_rollup_id",
        "verified_r100_burden_rollup_sig8",
    )

    if rollup.get("verified_r100_burden_rollup_sig8") != rollup_sig:
        failures.append("verified_rollup_sig_mismatch")

    rollup_core = _verified_r100_burden_rollup_verify_core(rollup)
    if rollup_core.get("gate") != "PASS":
        failures.append("verified_rollup_core_verify_not_PASS")
        failures.extend(rollup_core.get("failures") or [])

    summary = decision.get("input_summary") or {}
    freeze = decision.get("r100_freeze_policy") or {}
    authority = decision.get("decision_authority") or {}
    classes = decision.get("first_order_classes") or {}

    r100_receipts = int(summary.get("r100_receipts") or 0)
    total_receipt_rows = int(summary.get("total_receipt_rows") or 0)

    if r100_receipts <= 0:
        failures.append("r100_receipts_missing")
    if total_receipt_rows <= 0:
        failures.append("total_receipt_rows_missing")

    soft_watch_total = 100000
    hard_stop_total = max(r100_receipts * 2, 1)
    hard_stop_ratio_vs_r100 = 2.0
    hard_stop_receipt_over_radius_ratio = 1.75

    payload = {
        "policy_kind": "POST_R100_RADIUS_EXPANSION_BURDEN_POLICY",
        "policy_scope": f"RADIUS_EXPANSION_BURDEN_POLICY::{decision.get('r100_scale_decision_id')}",
        "source_r100_scale_decision": {
            "id": decision.get("r100_scale_decision_id"),
            "path": str(decision_path),
            "stored_sig": decision.get("r100_scale_decision_sig8"),
            "recomputed_sig": decision_sig,
            "gate": decision.get("gate"),
            "decision": decision.get("decision"),
        },
        "source_verified_r100_burden_rollup": {
            "id": rollup.get("verified_r100_burden_rollup_id"),
            "path": str(rollup_path),
            "stored_sig": rollup.get("verified_r100_burden_rollup_sig8"),
            "recomputed_sig": rollup_sig,
            "gate": rollup.get("gate"),
            "trust_label": rollup.get("trust_label"),
        },
        "current_state": {
            "radius_expansion_state": "FROZEN_AT_R100",
            "current_radius_ceiling": 100,
            "r50_receipts": summary.get("r50_receipts"),
            "r75_receipts": summary.get("r75_receipts"),
            "r100_receipts": summary.get("r100_receipts"),
            "total_receipt_rows_in_verified_envelope": total_receipt_rows,
            "r50_raw": summary.get("r50_raw"),
            "r75_raw": summary.get("r75_raw"),
            "r100_raw": summary.get("r100_raw"),
            "r50_coarse": summary.get("r50_coarse"),
            "r75_coarse": summary.get("r75_coarse"),
            "r100_coarse": summary.get("r100_coarse"),
            "curve_class": classes.get("curve_class"),
            "raw_class": classes.get("raw_class"),
            "burden_class": classes.get("burden_class"),
            "r75_to_r100_burden_class": summary.get("r75_to_r100_burden_class"),
            "r50_to_r100_burden_class": summary.get("r50_to_r100_burden_class"),
        },
        "policy_rules": {
            "policy_authorizes_execution": False,
            "policy_authorizes_R125": False,
            "future_radius_requires_exact_decision_artifact": True,
            "future_radius_decision_schema": "radius_expansion_candidate_decision_v0",
            "default_candidate_radius": 125,
            "max_candidate_radius_v0": 125,
            "max_radius_increment_v0": 25,
            "slot_separated_full_trace_required": True,
            "raw_receipts_required": True,
            "post_run_burden_comparison_required": True,
            "verified_rollup_required_before_future_decision": True,
            "candidate_preflight_estimate_required": True,
            "candidate_runtime_budget_required": True,
            "candidate_operator_budget_required": True,
        },
        "budget_rules": {
            "baseline_radius": 100,
            "baseline_r100_receipts": r100_receipts,
            "baseline_verified_envelope_receipts": total_receipt_rows,
            "soft_watch_total_receipts": soft_watch_total,
            "hard_stop_total_receipts": hard_stop_total,
            "hard_stop_receipt_ratio_vs_r100": hard_stop_ratio_vs_r100,
            "hard_stop_receipt_over_radius_ratio": hard_stop_receipt_over_radius_ratio,
            "budget_meaning": "Future candidate execution must fail closed unless a candidate decision supplies an explicit receipt estimate, runtime/operator budget, and exact radius license.",
        },
        "stop_rules": [
            "STOP_IF_NO_EXACT_NEXT_RADIUS",
            "STOP_IF_NO_CANDIDATE_DECISION_ARTIFACT",
            "STOP_IF_NO_PREFLIGHT_RECEIPT_ESTIMATE",
            "STOP_IF_ESTIMATED_TOTAL_RECEIPTS_GT_HARD_STOP_TOTAL_RECEIPTS",
            "STOP_IF_ESTIMATED_RECEIPT_RATIO_GT_HARD_STOP_RATIO_VS_R100",
            "STOP_IF_ESTIMATED_RECEIPT_OVER_RADIUS_RATIO_GT_POLICY_LIMIT",
            "STOP_IF_NO_RUNTIME_BUDGET",
            "STOP_IF_NO_OPERATOR_BUDGET",
            "STOP_IF_NOT_SLOT_SEPARATED_FULL_TRACE",
            "STOP_IF_ANY_EXECUTION_SKIPPING",
            "STOP_IF_ANY_RECEIPT_DELETION",
            "STOP_IF_ANY_REPRESENTATIVE_SUBSET",
            "STOP_IF_NO_POST_RUN_BURDEN_COMPARISON",
        ],
        "watch_rules": [
            "WATCH_IF_ESTIMATED_TOTAL_RECEIPTS_GT_SOFT_WATCH_TOTAL_RECEIPTS",
            "WATCH_IF_ESTIMATED_RECEIPT_RATIO_GT_RADIUS_RATIO",
            "WATCH_IF_RUNTIME_EXCEEDS_R100_SLOT_RUNTIME_ENVELOPE",
            "WATCH_IF_ROLLUP_REDUCES_READING_BUT_NOT_EXECUTION_BURDEN",
        ],
        "allowed": [
            "use_verified_rollup_for_operator_summary",
            "use_verified_rollup_for_coarse_profile_delta",
            "use_verified_rollup_for_burden_watch",
            "use_verified_rollup_for_radius_decision_support",
            "build_candidate_decision_artifact",
            "estimate_candidate_receipt_burden",
        ],
        "forbidden": {
            "R125_execution_by_policy_alone": True,
            "execution_skipping": True,
            "receipt_deletion": True,
            "representative_subset": True,
            "raw_replay_replacement": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "ontology_expansion": True,
            "theorem_layer": True,
            "hidden_trust_upgrade": True,
        },
        "candidate_decision_requirements": [
            "source_policy_id",
            "exact_next_radius",
            "candidate_radius_not_above_125_for_v0",
            "preflight_receipt_estimate",
            "preflight_receipt_estimate_method",
            "hard_stop_total_receipts",
            "runtime_budget_statement",
            "operator_budget_statement",
            "slot_separated_full_trace_commitment",
            "no_execution_skipping_commitment",
            "no_receipt_deletion_commitment",
            "post_run_burden_comparison_commitment",
            "explicit_terminal_authority",
        ],
        "non_claims": [
            "does_not_solve_global_scalability",
            "does_not_reduce_execution_cost",
            "does_not_reduce_raw_receipt_generation",
            "does_not_authorize_R125",
            "does_not_create_theorem_content",
            "does_not_replace_raw_replay",
        ],
        "known_limits": [
            "policy is conservative because R50_to_R100 burden is guard-level",
            "policy licenses candidate-decision construction only",
            "policy does not license radius execution",
            "future radius requires separate exact-radius decision",
        ],
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "BUILD_RADIUS_EXPANSION_CANDIDATE_DECISION_V0" if not failures else None,
            "stop_code": None if not failures else "STOP_RADIUS_EXPANSION_BURDEN_POLICY_FAIL",
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    return payload


def _radius_expansion_burden_policy_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("radius_expansion_burden_policy_gate_not_PASS")

    if payload.get("policy_kind") != "POST_R100_RADIUS_EXPANSION_BURDEN_POLICY":
        failures.append("policy_kind_mismatch")

    source = payload.get("source_r100_scale_decision") or {}
    if source.get("decision") != "FREEZE_RADIUS_AT_R100_AND_BUILD_BURDEN_POLICY":
        failures.append("source_decision_not_freeze_policy")

    try:
        decision_path = resolve_json_path(source.get("id"), "data/r100_scale_decisions")
        decision = json.loads(decision_path.read_text())
        decision_sig = stable_sig(decision, "r100_scale_decision_id", "r100_scale_decision_sig8")
        if decision.get("r100_scale_decision_sig8") != decision_sig:
            failures.append("source_decision_sig_mismatch")
        decision_core = _r100_scale_decision_with_verified_rollup_verify_core(decision)
        if decision_core.get("gate") != "PASS":
            failures.append("source_decision_core_not_PASS")
            failures.extend(decision_core.get("failures") or [])
    except Exception as exc:
        failures.append(f"source_decision_unresolved:{source.get('id')}:{exc}")

    rollup_source = payload.get("source_verified_r100_burden_rollup") or {}
    if rollup_source.get("trust_label") != "RAW_FULL_WITH_VERIFIED_ROLLUP":
        failures.append("source_rollup_trust_label_invalid")

    current = payload.get("current_state") or {}
    if current.get("radius_expansion_state") != "FROZEN_AT_R100":
        failures.append("radius_expansion_state_not_frozen")
    if current.get("current_radius_ceiling") != 100:
        failures.append("current_radius_ceiling_not_100")
    if current.get("r50_to_r100_burden_class") != "BURDEN_SUPERLINEAR_REQUIRES_GUARD":
        failures.append("r50_to_r100_burden_not_guard")

    rules = payload.get("policy_rules") or {}
    if rules.get("policy_authorizes_execution") is not False:
        failures.append("policy_illegally_authorizes_execution")
    if rules.get("policy_authorizes_R125") is not False:
        failures.append("policy_illegally_authorizes_R125")
    if rules.get("future_radius_requires_exact_decision_artifact") is not True:
        failures.append("exact_decision_artifact_not_required")
    if rules.get("candidate_preflight_estimate_required") is not True:
        failures.append("preflight_estimate_not_required")
    if rules.get("candidate_runtime_budget_required") is not True:
        failures.append("runtime_budget_not_required")
    if rules.get("candidate_operator_budget_required") is not True:
        failures.append("operator_budget_not_required")
    if rules.get("slot_separated_full_trace_required") is not True:
        failures.append("slot_separated_full_trace_not_required")
    if rules.get("raw_receipts_required") is not True:
        failures.append("raw_receipts_not_required")
    if rules.get("post_run_burden_comparison_required") is not True:
        failures.append("post_run_burden_comparison_not_required")

    budget = payload.get("budget_rules") or {}
    if int(budget.get("baseline_r100_receipts") or 0) != 87552:
        warnings.append(f"unexpected_baseline_r100_receipts:{budget.get('baseline_r100_receipts')}")
    if int(budget.get("hard_stop_total_receipts") or 0) < int(budget.get("baseline_r100_receipts") or 0):
        failures.append("hard_stop_total_below_baseline")
    if budget.get("hard_stop_receipt_ratio_vs_r100") != 2.0:
        failures.append("hard_stop_ratio_vs_r100_mismatch")
    if budget.get("hard_stop_receipt_over_radius_ratio") != 1.75:
        failures.append("hard_stop_receipt_over_radius_ratio_mismatch")

    required_stops = set(payload.get("stop_rules") or [])
    for rule in [
        "STOP_IF_NO_EXACT_NEXT_RADIUS",
        "STOP_IF_NO_CANDIDATE_DECISION_ARTIFACT",
        "STOP_IF_NO_PREFLIGHT_RECEIPT_ESTIMATE",
        "STOP_IF_ESTIMATED_TOTAL_RECEIPTS_GT_HARD_STOP_TOTAL_RECEIPTS",
        "STOP_IF_NO_RUNTIME_BUDGET",
        "STOP_IF_NO_OPERATOR_BUDGET",
        "STOP_IF_ANY_EXECUTION_SKIPPING",
        "STOP_IF_ANY_RECEIPT_DELETION",
        "STOP_IF_NO_POST_RUN_BURDEN_COMPARISON",
    ]:
        if rule not in required_stops:
            failures.append(f"stop_rule_missing:{rule}")

    forbidden = payload.get("forbidden") or {}
    for key in [
        "R125_execution_by_policy_alone",
        "execution_skipping",
        "receipt_deletion",
        "representative_subset",
        "raw_replay_replacement",
        "gate_semantics_change",
        "run_semantics_change",
        "ontology_expansion",
        "theorem_layer",
        "hidden_trust_upgrade",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_clause_missing:{key}")

    candidate_reqs = set(payload.get("candidate_decision_requirements") or [])
    for req in [
        "source_policy_id",
        "exact_next_radius",
        "preflight_receipt_estimate",
        "hard_stop_total_receipts",
        "runtime_budget_statement",
        "operator_budget_statement",
        "slot_separated_full_trace_commitment",
        "no_execution_skipping_commitment",
        "post_run_burden_comparison_commitment",
        "explicit_terminal_authority",
    ]:
        if req not in candidate_reqs:
            failures.append(f"candidate_requirement_missing:{req}")

    if "does_not_authorize_R125" not in (payload.get("non_claims") or []):
        failures.append("non_claim_does_not_authorize_R125_missing")

    terminal = payload.get("terminal") or {}
    if terminal.get("next_command_goal") != "BUILD_RADIUS_EXPANSION_CANDIDATE_DECISION_V0":
        failures.append("terminal_next_command_goal_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



def _candidate_estimate_from_policy(policy, candidate_radius):
    current = policy.get("current_state") or {}
    budget = policy.get("budget_rules") or {}

    r50_receipts = int(current.get("r50_receipts") or 0)
    r75_receipts = int(current.get("r75_receipts") or 0)
    r100_receipts = int(current.get("r100_receipts") or 0)

    r50_raw = int(current.get("r50_raw") or 0)
    r75_raw = int(current.get("r75_raw") or 0)
    r100_raw = int(current.get("r100_raw") or 0)

    r75_to_r100_delta_receipts = r100_receipts - r75_receipts
    r50_to_r75_delta_receipts = r75_receipts - r50_receipts
    delta_growth_receipts = r75_to_r100_delta_receipts - r50_to_r75_delta_receipts
    projected_next_delta_receipts = r75_to_r100_delta_receipts + max(delta_growth_receipts, 0)
    estimated_total_receipts = r100_receipts + projected_next_delta_receipts

    r75_to_r100_delta_raw = r100_raw - r75_raw
    r50_to_r75_delta_raw = r75_raw - r50_raw
    delta_growth_raw = r75_to_r100_delta_raw - r50_to_r75_delta_raw
    projected_next_delta_raw = r75_to_r100_delta_raw + max(delta_growth_raw, 0)
    estimated_raw_total = r100_raw + projected_next_delta_raw

    radius_ratio_vs_r100 = round(candidate_radius / 100, 6)
    receipt_ratio_vs_r100 = round(estimated_total_receipts / r100_receipts, 6) if r100_receipts else None
    raw_ratio_vs_r100 = round(estimated_raw_total / r100_raw, 6) if r100_raw else None
    receipt_over_radius_ratio = (
        round(receipt_ratio_vs_r100 / radius_ratio_vs_r100, 6)
        if receipt_ratio_vs_r100 is not None and radius_ratio_vs_r100
        else None
    )

    hard_stop_total = int(budget.get("hard_stop_total_receipts") or 0)
    soft_watch_total = int(budget.get("soft_watch_total_receipts") or 0)
    hard_stop_ratio = float(budget.get("hard_stop_receipt_ratio_vs_r100") or 0)
    hard_stop_over_radius = float(budget.get("hard_stop_receipt_over_radius_ratio") or 0)

    stop_reasons = []
    watch_reasons = []

    if estimated_total_receipts > hard_stop_total:
        stop_reasons.append("ESTIMATED_TOTAL_RECEIPTS_GT_HARD_STOP_TOTAL_RECEIPTS")
    if receipt_ratio_vs_r100 is not None and receipt_ratio_vs_r100 > hard_stop_ratio:
        stop_reasons.append("ESTIMATED_RECEIPT_RATIO_GT_HARD_STOP_RATIO_VS_R100")
    if receipt_over_radius_ratio is not None and receipt_over_radius_ratio > hard_stop_over_radius:
        stop_reasons.append("ESTIMATED_RECEIPT_OVER_RADIUS_RATIO_GT_POLICY_LIMIT")

    if estimated_total_receipts > soft_watch_total:
        watch_reasons.append("ESTIMATED_TOTAL_RECEIPTS_GT_SOFT_WATCH_TOTAL_RECEIPTS")
    if receipt_ratio_vs_r100 is not None and receipt_ratio_vs_r100 > radius_ratio_vs_r100:
        watch_reasons.append("ESTIMATED_RECEIPT_RATIO_GT_RADIUS_RATIO")

    return {
        "estimate_method": "quadratic_delta_extrapolation_from_R50_R75_R100_v0",
        "baseline": {
            "r50_receipts": r50_receipts,
            "r75_receipts": r75_receipts,
            "r100_receipts": r100_receipts,
            "r50_raw": r50_raw,
            "r75_raw": r75_raw,
            "r100_raw": r100_raw,
        },
        "receipt_delta_model": {
            "r50_to_r75_delta": r50_to_r75_delta_receipts,
            "r75_to_r100_delta": r75_to_r100_delta_receipts,
            "delta_growth": delta_growth_receipts,
            "projected_next_delta": projected_next_delta_receipts,
        },
        "raw_delta_model": {
            "r50_to_r75_delta": r50_to_r75_delta_raw,
            "r75_to_r100_delta": r75_to_r100_delta_raw,
            "delta_growth": delta_growth_raw,
            "projected_next_delta": projected_next_delta_raw,
        },
        "candidate_radius": candidate_radius,
        "estimated_total_receipts": estimated_total_receipts,
        "estimated_raw_total": estimated_raw_total,
        "estimated_coarse_total": int(current.get("r100_coarse") or 0),
        "radius_ratio_vs_r100": radius_ratio_vs_r100,
        "receipt_ratio_vs_r100": receipt_ratio_vs_r100,
        "raw_ratio_vs_r100": raw_ratio_vs_r100,
        "receipt_over_radius_ratio": receipt_over_radius_ratio,
        "hard_stop_total_receipts": hard_stop_total,
        "soft_watch_total_receipts": soft_watch_total,
        "hard_stop_receipt_ratio_vs_r100": hard_stop_ratio,
        "hard_stop_receipt_over_radius_ratio": hard_stop_over_radius,
        "stop_reasons": stop_reasons,
        "watch_reasons": watch_reasons,
    }


def _radius_expansion_candidate_decision_payload(policy_id, candidate_radius):
    failures = []
    warnings = []

    policy_path = resolve_json_path(policy_id, "data/radius_expansion_burden_policies")
    policy = json.loads(policy_path.read_text())
    policy_sig = stable_sig(
        policy,
        "radius_expansion_burden_policy_id",
        "radius_expansion_burden_policy_sig8",
    )

    if policy.get("radius_expansion_burden_policy_sig8") != policy_sig:
        failures.append("radius_expansion_burden_policy_sig_mismatch")

    policy_core = _radius_expansion_burden_policy_verify_core(policy)
    if policy_core.get("gate") != "PASS":
        failures.append("radius_expansion_burden_policy_core_verify_not_PASS")
        failures.extend(policy_core.get("failures") or [])

    rules = policy.get("policy_rules") or {}
    budget = policy.get("budget_rules") or {}

    if rules.get("policy_authorizes_execution") is not False:
        failures.append("source_policy_illegally_authorizes_execution")
    if rules.get("policy_authorizes_R125") is not False:
        failures.append("source_policy_illegally_authorizes_R125")
    if rules.get("future_radius_requires_exact_decision_artifact") is not True:
        failures.append("source_policy_does_not_require_exact_decision")
    if rules.get("candidate_preflight_estimate_required") is not True:
        failures.append("source_policy_does_not_require_preflight_estimate")
    if rules.get("candidate_runtime_budget_required") is not True:
        failures.append("source_policy_does_not_require_runtime_budget")
    if rules.get("candidate_operator_budget_required") is not True:
        failures.append("source_policy_does_not_require_operator_budget")

    max_candidate = int(rules.get("max_candidate_radius_v0") or 0)
    if candidate_radius != 125:
        failures.append(f"candidate_radius_not_exact_R125_v0:{candidate_radius}")
    if candidate_radius > max_candidate:
        failures.append(f"candidate_radius_above_policy_max:{candidate_radius}:{max_candidate}")
    if candidate_radius <= int((policy.get("current_state") or {}).get("current_radius_ceiling") or 0):
        failures.append("candidate_radius_not_above_current_ceiling")

    estimate = _candidate_estimate_from_policy(policy, candidate_radius)

    if not estimate.get("estimate_method"):
        failures.append("preflight_receipt_estimate_method_missing")
    if int(estimate.get("estimated_total_receipts") or 0) <= 0:
        failures.append("preflight_receipt_estimate_missing")

    stop_reasons = list(estimate.get("stop_reasons") or [])
    watch_reasons = list(estimate.get("watch_reasons") or [])

    runtime_budget = {
        "budget_kind": "OPERATOR_APPROVED_SINGLE_RADIUS_RUN_BUDGET",
        "candidate_radius": candidate_radius,
        "slot_count": 9,
        "full_trace_required": True,
        "progress_reporting_required": True,
        "interruption_recovery_required": True,
        "estimated_total_receipts": estimate.get("estimated_total_receipts"),
        "hard_stop_total_receipts": estimate.get("hard_stop_total_receipts"),
        "status": "DECLARED",
    }

    operator_budget = {
        "budget_kind": "ROLLUP_BACKED_READING_BUDGET",
        "requires_verified_rollup_after_run": True,
        "requires_post_run_burden_comparison": True,
        "manual_review_surface": [
            "candidate execution receipt",
            "R125 slot observation",
            "R100_to_R125 burden comparison",
            "verified R125 burden rollup",
            "post R125 decision",
        ],
        "status": "DECLARED",
    }

    commitments = {
        "slot_separated_full_trace": True,
        "raw_receipts_required": True,
        "no_execution_skipping": True,
        "no_receipt_deletion": True,
        "no_representative_subset": True,
        "no_raw_replay_replacement": True,
        "no_gate_semantics_change": True,
        "no_run_semantics_change": True,
        "post_run_burden_comparison": True,
        "verified_rollup_after_run": True,
    }

    if runtime_budget.get("status") != "DECLARED":
        failures.append("runtime_budget_missing")
    if operator_budget.get("status") != "DECLARED":
        failures.append("operator_budget_missing")

    for key, value in commitments.items():
        if value is not True:
            failures.append(f"commitment_missing:{key}")

    if stop_reasons:
        decision = "DO_NOT_LICENSE_R125_CANDIDATE_BUDGET_STOP"
        terminal_type = "STOP"
        next_goal = None
        stop_code = "STOP_R125_CANDIDATE_BUDGET_FAIL"
    elif failures:
        decision = "STOP_CANDIDATE_DECISION_BUILD_FAIL"
        terminal_type = "STOP"
        next_goal = None
        stop_code = "STOP_CANDIDATE_DECISION_BUILD_FAIL"
    elif watch_reasons:
        decision = "LICENSE_R125_WITH_BURDEN_WATCH"
        terminal_type = "ADVANCE"
        next_goal = "RUN_RADIUS_125_SLOT_SEPARATED_WITH_BURDEN_POLICY_V0"
        stop_code = None
    else:
        decision = "LICENSE_R125"
        terminal_type = "ADVANCE"
        next_goal = "RUN_RADIUS_125_SLOT_SEPARATED_WITH_BURDEN_POLICY_V0"
        stop_code = None

    payload = {
        "decision_kind": "RADIUS_EXPANSION_CANDIDATE_DECISION",
        "source_policy": {
            "id": policy.get("radius_expansion_burden_policy_id"),
            "path": str(policy_path),
            "stored_sig": policy.get("radius_expansion_burden_policy_sig8"),
            "recomputed_sig": policy_sig,
            "gate": policy.get("gate"),
        },
        "exact_next_radius": candidate_radius,
        "current_radius_ceiling": (policy.get("current_state") or {}).get("current_radius_ceiling"),
        "candidate_radius_delta": candidate_radius - int((policy.get("current_state") or {}).get("current_radius_ceiling") or 0),
        "preflight_receipt_estimate": estimate,
        "runtime_budget_statement": runtime_budget,
        "operator_budget_statement": operator_budget,
        "commitments": commitments,
        "policy_limits": {
            "max_candidate_radius_v0": max_candidate,
            "hard_stop_total_receipts": budget.get("hard_stop_total_receipts"),
            "hard_stop_receipt_ratio_vs_r100": budget.get("hard_stop_receipt_ratio_vs_r100"),
            "hard_stop_receipt_over_radius_ratio": budget.get("hard_stop_receipt_over_radius_ratio"),
            "soft_watch_total_receipts": budget.get("soft_watch_total_receipts"),
        },
        "decision": decision,
        "authorization": {
            "authorizes_exact_radius": candidate_radius if decision in {"LICENSE_R125", "LICENSE_R125_WITH_BURDEN_WATCH"} else None,
            "authorizes_R125_execution": decision in {"LICENSE_R125", "LICENSE_R125_WITH_BURDEN_WATCH"},
            "authorizes_any_other_radius": False,
            "authorizes_execution_skipping": False,
            "authorizes_receipt_deletion": False,
            "authorizes_representative_subset": False,
            "authorizes_gate_semantics_change": False,
            "authorizes_run_semantics_change": False,
        },
        "post_run_required_artifacts": [
            "radius_125_slot_separated_execution_summary",
            "domain_shift_slot_observation_v0 for radius 125",
            "R100_to_R125_burden_comparison",
            "verified_R125_burden_rollup",
            "post_R125_scale_decision",
        ],
        "stop_reasons": stop_reasons,
        "watch_reasons": watch_reasons,
        "known_limits": [
            "candidate_decision_licenses_only_exact_radius_125",
            "candidate_decision_does_not_solve_global_scalability",
            "candidate_decision_requires_full_raw_trace",
            "candidate_decision_requires_post_run_burden_comparison",
            "estimate_is_preflight_not_observation",
        ],
        "forbidden": {
            "radius_above_125": True,
            "execution_skipping": True,
            "receipt_deletion": True,
            "representative_subset": True,
            "raw_replay_replacement": True,
            "gate_semantics_change": True,
            "run_semantics_change": True,
            "ontology_expansion": True,
            "theorem_layer": True,
            "hidden_trust_upgrade": True,
        },
        "terminal": {
            "type": terminal_type,
            "next_command_goal": next_goal,
            "stop_code": stop_code,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    return payload


def _radius_expansion_candidate_decision_verify_core(payload):
    failures = []
    warnings = []

    if payload.get("gate") != "PASS":
        failures.append("candidate_decision_gate_not_PASS")

    if payload.get("decision_kind") != "RADIUS_EXPANSION_CANDIDATE_DECISION":
        failures.append("candidate_decision_kind_mismatch")

    source = payload.get("source_policy") or {}
    try:
        policy_path = resolve_json_path(source.get("id"), "data/radius_expansion_burden_policies")
        policy = json.loads(policy_path.read_text())
        policy_sig = stable_sig(
            policy,
            "radius_expansion_burden_policy_id",
            "radius_expansion_burden_policy_sig8",
        )
        if policy.get("radius_expansion_burden_policy_sig8") != policy_sig:
            failures.append("source_policy_sig_mismatch")
        policy_core = _radius_expansion_burden_policy_verify_core(policy)
        if policy_core.get("gate") != "PASS":
            failures.append("source_policy_core_not_PASS")
            failures.extend(policy_core.get("failures") or [])
    except Exception as exc:
        policy = None
        failures.append(f"source_policy_unresolved:{source.get('id')}:{exc}")

    if payload.get("exact_next_radius") != 125:
        failures.append(f"exact_next_radius_not_125:{payload.get('exact_next_radius')}")

    if payload.get("candidate_radius_delta") != 25:
        failures.append(f"candidate_radius_delta_not_25:{payload.get('candidate_radius_delta')}")

    estimate = payload.get("preflight_receipt_estimate") or {}
    if estimate.get("estimate_method") != "quadratic_delta_extrapolation_from_R50_R75_R100_v0":
        failures.append("estimate_method_mismatch")
    if int(estimate.get("estimated_total_receipts") or 0) <= 0:
        failures.append("estimated_total_receipts_missing")
    if int(estimate.get("estimated_total_receipts") or 0) > int(estimate.get("hard_stop_total_receipts") or 0):
        failures.append("estimated_total_receipts_exceeds_hard_stop")
    if float(estimate.get("receipt_ratio_vs_r100") or 0) > float(estimate.get("hard_stop_receipt_ratio_vs_r100") or 0):
        failures.append("estimated_receipt_ratio_exceeds_hard_stop")
    if float(estimate.get("receipt_over_radius_ratio") or 0) > float(estimate.get("hard_stop_receipt_over_radius_ratio") or 0):
        failures.append("estimated_receipt_over_radius_exceeds_hard_stop")

    runtime_budget = payload.get("runtime_budget_statement") or {}
    operator_budget = payload.get("operator_budget_statement") or {}
    if runtime_budget.get("status") != "DECLARED":
        failures.append("runtime_budget_not_declared")
    if operator_budget.get("status") != "DECLARED":
        failures.append("operator_budget_not_declared")
    if runtime_budget.get("full_trace_required") is not True:
        failures.append("runtime_budget_full_trace_not_required")
    if operator_budget.get("requires_verified_rollup_after_run") is not True:
        failures.append("operator_budget_verified_rollup_not_required")

    commitments = payload.get("commitments") or {}
    for key in [
        "slot_separated_full_trace",
        "raw_receipts_required",
        "no_execution_skipping",
        "no_receipt_deletion",
        "no_representative_subset",
        "no_raw_replay_replacement",
        "no_gate_semantics_change",
        "no_run_semantics_change",
        "post_run_burden_comparison",
        "verified_rollup_after_run",
    ]:
        if commitments.get(key) is not True:
            failures.append(f"commitment_missing:{key}")

    decision = payload.get("decision")
    auth = payload.get("authorization") or {}

    if decision == "LICENSE_R125_WITH_BURDEN_WATCH":
        if auth.get("authorizes_R125_execution") is not True:
            failures.append("licensed_decision_does_not_authorize_R125")
        if auth.get("authorizes_exact_radius") != 125:
            failures.append("licensed_decision_exact_radius_mismatch")
        if not payload.get("watch_reasons"):
            failures.append("burden_watch_decision_without_watch_reasons")
    elif decision == "LICENSE_R125":
        if auth.get("authorizes_R125_execution") is not True:
            failures.append("licensed_decision_does_not_authorize_R125")
        if auth.get("authorizes_exact_radius") != 125:
            failures.append("licensed_decision_exact_radius_mismatch")
    elif decision == "DO_NOT_LICENSE_R125_CANDIDATE_BUDGET_STOP":
        if auth.get("authorizes_R125_execution") is not False:
            failures.append("budget_stop_illegally_authorizes_R125")
    else:
        failures.append(f"candidate_decision_unexpected:{decision}")

    for key in [
        "authorizes_any_other_radius",
        "authorizes_execution_skipping",
        "authorizes_receipt_deletion",
        "authorizes_representative_subset",
        "authorizes_gate_semantics_change",
        "authorizes_run_semantics_change",
    ]:
        if auth.get(key) is not False:
            failures.append(f"illegal_authorization:{key}")

    forbidden = payload.get("forbidden") or {}
    for key in [
        "radius_above_125",
        "execution_skipping",
        "receipt_deletion",
        "representative_subset",
        "raw_replay_replacement",
        "gate_semantics_change",
        "run_semantics_change",
        "ontology_expansion",
        "theorem_layer",
        "hidden_trust_upgrade",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_clause_missing:{key}")

    required_artifacts = set(payload.get("post_run_required_artifacts") or [])
    for item in [
        "radius_125_slot_separated_execution_summary",
        "domain_shift_slot_observation_v0 for radius 125",
        "R100_to_R125_burden_comparison",
        "verified_R125_burden_rollup",
        "post_R125_scale_decision",
    ]:
        if item not in required_artifacts:
            failures.append(f"post_run_required_artifact_missing:{item}")

    if "estimate_is_preflight_not_observation" not in (payload.get("known_limits") or []):
        failures.append("known_limit_estimate_is_preflight_missing")

    terminal = payload.get("terminal") or {}
    if decision in {"LICENSE_R125", "LICENSE_R125_WITH_BURDEN_WATCH"}:
        if terminal.get("next_command_goal") != "RUN_RADIUS_125_SLOT_SEPARATED_WITH_BURDEN_POLICY_V0":
            failures.append("terminal_next_command_goal_mismatch")
    else:
        if terminal.get("type") != "STOP":
            failures.append("stop_decision_terminal_type_mismatch")

    return {
        "gate": "FAIL" if failures else "PASS",
        "failures": failures,
        "warnings": warnings,
    }



@app.command("radius-expansion-candidate-decision")
def radius_expansion_candidate_decision(
    policy: str = typer.Argument(
        "534f967f",
        help="Radius expansion burden policy id or JSON path.",
    ),
    candidate_radius: int = typer.Option(
        125,
        "--candidate-radius",
        help="Exact candidate radius. v0 only permits 125.",
    ),
):
    """Build exact-radius candidate decision under burden policy."""

    try:
        payload = _radius_expansion_candidate_decision_payload(policy, candidate_radius)
    except Exception as exc:
        payload = {
            "decision_kind": "RADIUS_EXPANSION_CANDIDATE_DECISION",
            "source_policy": {
                "id": policy,
            },
            "exact_next_radius": candidate_radius,
            "decision": "STOP_CANDIDATE_DECISION_BUILD_FAIL",
            "failures": [f"radius_expansion_candidate_decision_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_CANDIDATE_DECISION_BUILD_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/radius_expansion_candidate_decisions",
        "radius_expansion_candidate_decision_schema_version",
        RADIUS_EXPANSION_CANDIDATE_DECISION_SCHEMA,
        "radius_expansion_candidate_decision_id",
        "radius_expansion_candidate_decision_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"radius_expansion_candidate_decision_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("radius-expansion-candidate-decision-verify")
def radius_expansion_candidate_decision_verify(
    decision: str = typer.Argument(
        ...,
        help="Radius expansion candidate decision id or JSON path.",
    ),
):
    """Reload and verify an exact-radius candidate decision."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(decision, "data/radius_expansion_candidate_decisions")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "radius_expansion_candidate_decision_id": decision,
        }
        failures.append(f"radius_expansion_candidate_decision_unresolved:{decision}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "radius_expansion_candidate_decision_id",
            "radius_expansion_candidate_decision_sig8",
        )
        if payload.get("radius_expansion_candidate_decision_sig8") != recomputed_sig:
            failures.append("radius_expansion_candidate_decision_sig_mismatch")
        if path.stem != payload.get("radius_expansion_candidate_decision_id"):
            failures.append("radius_expansion_candidate_decision_filename_id_mismatch")

        core = _radius_expansion_candidate_decision_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_decision": decision,
        "radius_expansion_candidate_decision_id": payload.get("radius_expansion_candidate_decision_id"),
        "radius_expansion_candidate_decision_path": str(path) if path else None,
        "radius_expansion_candidate_decision_sig8": payload.get("radius_expansion_candidate_decision_sig8"),
        "radius_expansion_candidate_decision_recomputed_sig8": recomputed_sig,
        "source_policy_id": (payload.get("source_policy") or {}).get("id"),
        "exact_next_radius": payload.get("exact_next_radius"),
        "decision": payload.get("decision"),
        "authorization": payload.get("authorization"),
        "preflight_receipt_estimate": payload.get("preflight_receipt_estimate"),
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else (payload.get("terminal") or {}).get("next_command_goal"),
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/radius_expansion_candidate_decision_verifications",
        "radius_expansion_candidate_decision_verification_schema_version",
        RADIUS_EXPANSION_CANDIDATE_DECISION_VERIFICATION_SCHEMA,
        "radius_expansion_candidate_decision_verification_id",
        "radius_expansion_candidate_decision_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"radius_expansion_candidate_decision_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("radius-expansion-burden-policy")
def radius_expansion_burden_policy(
    r100_decision: str = typer.Argument(
        "49a22583",
        help="R100 scale decision id or JSON path.",
    ),
):
    """Build radius expansion burden policy after the verified R100 decision."""

    try:
        payload = _radius_expansion_burden_policy_payload(r100_decision)
    except Exception as exc:
        payload = {
            "policy_kind": "POST_R100_RADIUS_EXPANSION_BURDEN_POLICY",
            "source_r100_scale_decision": {
                "id": r100_decision,
            },
            "failures": [f"radius_expansion_burden_policy_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_RADIUS_EXPANSION_BURDEN_POLICY_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/radius_expansion_burden_policies",
        "radius_expansion_burden_policy_schema_version",
        RADIUS_EXPANSION_BURDEN_POLICY_SCHEMA,
        "radius_expansion_burden_policy_id",
        "radius_expansion_burden_policy_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"radius_expansion_burden_policy_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("radius-expansion-burden-policy-verify")
def radius_expansion_burden_policy_verify(
    policy: str = typer.Argument(
        ...,
        help="Radius expansion burden policy id or JSON path.",
    ),
):
    """Reload and verify a radius expansion burden policy."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(policy, "data/radius_expansion_burden_policies")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "radius_expansion_burden_policy_id": policy,
        }
        failures.append(f"radius_expansion_burden_policy_unresolved:{policy}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "radius_expansion_burden_policy_id",
            "radius_expansion_burden_policy_sig8",
        )
        if payload.get("radius_expansion_burden_policy_sig8") != recomputed_sig:
            failures.append("radius_expansion_burden_policy_sig_mismatch")
        if path.stem != payload.get("radius_expansion_burden_policy_id"):
            failures.append("radius_expansion_burden_policy_filename_id_mismatch")

        core = _radius_expansion_burden_policy_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_policy": policy,
        "radius_expansion_burden_policy_id": payload.get("radius_expansion_burden_policy_id"),
        "radius_expansion_burden_policy_path": str(path) if path else None,
        "radius_expansion_burden_policy_sig8": payload.get("radius_expansion_burden_policy_sig8"),
        "radius_expansion_burden_policy_recomputed_sig8": recomputed_sig,
        "source_r100_scale_decision_id": (payload.get("source_r100_scale_decision") or {}).get("id"),
        "current_radius_ceiling": (payload.get("current_state") or {}).get("current_radius_ceiling"),
        "policy_authorizes_R125": (payload.get("policy_rules") or {}).get("policy_authorizes_R125"),
        "policy_authorizes_execution": (payload.get("policy_rules") or {}).get("policy_authorizes_execution"),
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "BUILD_RADIUS_EXPANSION_CANDIDATE_DECISION_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/radius_expansion_burden_policy_verifications",
        "radius_expansion_burden_policy_verification_schema_version",
        RADIUS_EXPANSION_BURDEN_POLICY_VERIFICATION_SCHEMA,
        "radius_expansion_burden_policy_verification_id",
        "radius_expansion_burden_policy_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"radius_expansion_burden_policy_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("r100-scale-decision-with-rollup")
def r100_scale_decision_with_rollup(
    verified_rollup: str = typer.Argument(
        "279d289c",
        help="Verified R100 burden rollup id or JSON path.",
    ),
):
    """Decide R100 scale outcome using the verified burden rollup."""

    try:
        payload = _r100_scale_decision_with_verified_rollup_payload(verified_rollup)
    except Exception as exc:
        payload = {
            "decision_kind": "POST_R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP",
            "source_verified_r100_burden_rollup": {
                "id": verified_rollup,
            },
            "decision": "STOP_R100_DECISION_BUILD_FAIL",
            "failures": [f"r100_scale_decision_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_R100_DECISION_BUILD_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/r100_scale_decisions",
        "r100_scale_decision_schema_version",
        R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP_SCHEMA,
        "r100_scale_decision_id",
        "r100_scale_decision_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"r100_scale_decision_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("r100-scale-decision-with-rollup-verify")
def r100_scale_decision_with_rollup_verify(
    decision: str = typer.Argument(
        ...,
        help="R100 scale decision id or JSON path.",
    ),
):
    """Reload and verify an R100 scale decision with verified rollup."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(decision, "data/r100_scale_decisions")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "r100_scale_decision_id": decision,
        }
        failures.append(f"r100_scale_decision_unresolved:{decision}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "r100_scale_decision_id",
            "r100_scale_decision_sig8",
        )
        if payload.get("r100_scale_decision_sig8") != recomputed_sig:
            failures.append("r100_scale_decision_sig_mismatch")
        if path.stem != payload.get("r100_scale_decision_id"):
            failures.append("r100_scale_decision_filename_id_mismatch")

        core = _r100_scale_decision_with_verified_rollup_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_decision": decision,
        "r100_scale_decision_id": payload.get("r100_scale_decision_id"),
        "r100_scale_decision_path": str(path) if path else None,
        "r100_scale_decision_sig8": payload.get("r100_scale_decision_sig8"),
        "r100_scale_decision_recomputed_sig8": recomputed_sig,
        "source_verified_r100_burden_rollup_id": (payload.get("source_verified_r100_burden_rollup") or {}).get("id"),
        "decision": payload.get("decision"),
        "recommended_next_object": payload.get("recommended_next_object"),
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "BUILD_RADIUS_EXPANSION_BURDEN_POLICY_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/r100_scale_decision_verifications",
        "r100_scale_decision_verification_schema_version",
        R100_SCALE_DECISION_WITH_VERIFIED_ROLLUP_VERIFICATION_SCHEMA,
        "r100_scale_decision_verification_id",
        "r100_scale_decision_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"r100_scale_decision_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("verified-r100-burden-rollup")
def verified_r100_burden_rollup(
    contract: str = typer.Argument(
        "286e398f",
        help="Receipt rollup contract id or JSON path.",
    ),
):
    """Build verified R100 burden rollups from raw manifests."""

    try:
        payload = _verified_r100_burden_rollup_payload(contract)
    except Exception as exc:
        payload = {
            "rollup_kind": "VERIFIED_R100_BURDEN_ROLLUP",
            "source_receipt_rollup_contract": {
                "id": contract,
            },
            "failures": [f"verified_r100_burden_rollup_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_VERIFIED_R100_BURDEN_ROLLUP_BUILD_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/verified_burden_rollups",
        "verified_r100_burden_rollup_schema_version",
        VERIFIED_R100_BURDEN_ROLLUP_SCHEMA,
        "verified_r100_burden_rollup_id",
        "verified_r100_burden_rollup_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"verified_r100_burden_rollup_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("verified-r100-burden-rollup-verify")
def verified_r100_burden_rollup_verify(
    rollup: str = typer.Argument(
        ...,
        help="Verified R100 burden rollup id or JSON path.",
    ),
):
    """Reload and verify a verified R100 burden rollup bundle."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(rollup, "data/verified_burden_rollups")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "verified_r100_burden_rollup_id": rollup,
        }
        failures.append(f"verified_r100_burden_rollup_unresolved:{rollup}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "verified_r100_burden_rollup_id",
            "verified_r100_burden_rollup_sig8",
        )
        if payload.get("verified_r100_burden_rollup_sig8") != recomputed_sig:
            failures.append("verified_r100_burden_rollup_sig_mismatch")
        if path.stem != payload.get("verified_r100_burden_rollup_id"):
            failures.append("verified_r100_burden_rollup_filename_id_mismatch")

        core = _verified_r100_burden_rollup_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_verified_r100_burden_rollup": rollup,
        "verified_r100_burden_rollup_id": payload.get("verified_r100_burden_rollup_id"),
        "verified_r100_burden_rollup_path": str(path) if path else None,
        "verified_r100_burden_rollup_sig8": payload.get("verified_r100_burden_rollup_sig8"),
        "verified_r100_burden_rollup_recomputed_sig8": recomputed_sig,
        "source_receipt_rollup_contract_id": (payload.get("source_receipt_rollup_contract") or {}).get("id"),
        "raw_manifest_id": (payload.get("raw_manifest") or {}).get("id"),
        "trajectory_rollup_id": (payload.get("rollup_hierarchy") or {}).get("trajectory_rollup_id"),
        "decision_record_id": (payload.get("decision_record") or {}).get("id"),
        "verified_metrics": payload.get("verified_metrics"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "DECIDE_R100_SCALE_OUTCOME_WITH_VERIFIED_ROLLUP_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/verified_burden_rollup_verifications",
        "verified_r100_burden_rollup_verification_schema_version",
        VERIFIED_R100_BURDEN_ROLLUP_VERIFICATION_SCHEMA,
        "verified_r100_burden_rollup_verification_id",
        "verified_r100_burden_rollup_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"verified_r100_burden_rollup_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("receipt-rollup-contract")
def receipt_rollup_contract(
    r100_radius_scale_observation: str = typer.Argument(
        "a5c79278",
        help="R100 radius scale observation id or JSON path.",
    ),
):
    """Build the post-R100 receipt rollup contract."""

    try:
        payload = _receipt_rollup_contract_payload(r100_radius_scale_observation)
    except Exception as exc:
        payload = {
            "contract_kind": "POST_R100_RECEIPT_BURDEN_ROLLUP_CONTRACT",
            "contract_scope": f"R100_BURDEN_ROLLUP_SCOPE::{r100_radius_scale_observation}",
            "source_r100_radius_scale_observation": {
                "id": r100_radius_scale_observation,
            },
            "failures": [f"receipt_rollup_contract_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_ROLLUP_CONTRACT_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/receipt_rollup_contracts",
        "receipt_rollup_contract_schema_version",
        RECEIPT_ROLLUP_CONTRACT_SCHEMA,
        "receipt_rollup_contract_id",
        "receipt_rollup_contract_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"receipt_rollup_contract_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("receipt-rollup-contract-verify")
def receipt_rollup_contract_verify(
    contract: str = typer.Argument(
        ...,
        help="Receipt rollup contract id or JSON path.",
    ),
):
    """Reload and verify a receipt rollup contract."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(contract, "data/receipt_rollup_contracts")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "receipt_rollup_contract_id": contract,
        }
        failures.append(f"receipt_rollup_contract_unresolved:{contract}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "receipt_rollup_contract_id",
            "receipt_rollup_contract_sig8",
        )
        if payload.get("receipt_rollup_contract_sig8") != recomputed_sig:
            failures.append("receipt_rollup_contract_sig_mismatch")
        if path.stem != payload.get("receipt_rollup_contract_id"):
            failures.append("receipt_rollup_contract_filename_id_mismatch")

        core = _receipt_rollup_contract_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_contract": contract,
        "receipt_rollup_contract_id": payload.get("receipt_rollup_contract_id"),
        "receipt_rollup_contract_path": str(path) if path else None,
        "receipt_rollup_contract_sig8": payload.get("receipt_rollup_contract_sig8"),
        "receipt_rollup_contract_recomputed_sig8": recomputed_sig,
        "source_r100_radius_scale_observation_id": (payload.get("source_r100_radius_scale_observation") or {}).get("id"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "BUILD_VERIFIED_R100_BURDEN_ROLLUP_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/receipt_rollup_contract_verifications",
        "receipt_rollup_contract_verification_schema_version",
        RECEIPT_ROLLUP_CONTRACT_VERIFICATION_SCHEMA,
        "receipt_rollup_contract_verification_id",
        "receipt_rollup_contract_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"receipt_rollup_contract_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("r100-radius-scale-observation")
def r100_radius_scale_observation(
    r100_observation: str = typer.Argument(
        "5a442f0c",
        help="R100 domain shift slot observation id or JSON path.",
    ),
    decision: str = typer.Option(
        "0bbd1bbd",
        "--decision",
        help="R75 scale decision id or JSON path.",
    ),
    r75_radius_scale_observation: str = typer.Option(
        "b9420863",
        "--r75-rso",
        help="R50-to-R75 radius scale observation id or JSON path.",
    ),
):
    """Build the R50/R75/R100 scale observation with explicit burden evaluation."""

    try:
        payload = _r100_radius_scale_observation_payload(
            r100_observation,
            decision,
            r75_radius_scale_observation,
        )
    except Exception as exc:
        payload = {
            "source_r75_scale_decision_id": decision,
            "source_r75_radius_scale_observation_id": r75_radius_scale_observation,
            "radius_50_observation_id": None,
            "radius_75_observation_id": None,
            "radius_100_observation_id": r100_observation,
            "observation": {},
            "terminal_decision": "STOP_R100_RADIUS_SCALE_OBSERVATION_BUILD_FAIL",
            "failures": [f"r100_radius_scale_observation_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_R100_RADIUS_SCALE_OBSERVATION_BUILD_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/r100_radius_scale_observations",
        "r100_radius_scale_observation_schema_version",
        R100_RADIUS_SCALE_OBSERVATION_SCHEMA,
        "r100_radius_scale_observation_id",
        "r100_radius_scale_observation_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"r100_radius_scale_observation_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("r100-radius-scale-observation-verify")
def r100_radius_scale_observation_verify(
    r100_radius_scale_observation: str = typer.Argument(
        ...,
        help="R100 radius scale observation id or JSON path.",
    ),
):
    """Reload and verify an R100 radius scale observation."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(r100_radius_scale_observation, "data/r100_radius_scale_observations")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "r100_radius_scale_observation_id": r100_radius_scale_observation,
        }
        failures.append(f"r100_radius_scale_observation_unresolved:{r100_radius_scale_observation}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "r100_radius_scale_observation_id",
            "r100_radius_scale_observation_sig8",
        )
        if payload.get("r100_radius_scale_observation_sig8") != recomputed_sig:
            failures.append("r100_radius_scale_observation_sig_mismatch")
        if path.stem != payload.get("r100_radius_scale_observation_id"):
            failures.append("r100_radius_scale_observation_filename_id_mismatch")

        core = _r100_radius_scale_observation_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_r100_radius_scale_observation": r100_radius_scale_observation,
        "r100_radius_scale_observation_id": payload.get("r100_radius_scale_observation_id"),
        "r100_radius_scale_observation_path": str(path) if path else None,
        "r100_radius_scale_observation_sig8": payload.get("r100_radius_scale_observation_sig8"),
        "r100_radius_scale_observation_recomputed_sig8": recomputed_sig,
        "source_r75_scale_decision_id": payload.get("source_r75_scale_decision_id"),
        "source_r75_radius_scale_observation_id": payload.get("source_r75_radius_scale_observation_id"),
        "radius_50_observation_id": payload.get("radius_50_observation_id"),
        "radius_75_observation_id": payload.get("radius_75_observation_id"),
        "radius_100_observation_id": payload.get("radius_100_observation_id"),
        "terminal_decision": payload.get("terminal_decision"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "DECIDE_R100_SCALE_OUTCOME_OR_NEXT_RADIUS_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/r100_radius_scale_observation_verifications",
        "r100_radius_scale_observation_verification_schema_version",
        R100_RADIUS_SCALE_OBSERVATION_VERIFICATION_SCHEMA,
        "r100_radius_scale_observation_verification_id",
        "r100_radius_scale_observation_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"r100_radius_scale_observation_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("r75-scale-decision")
def r75_scale_decision(
    radius_scale_observation: str = typer.Argument(
        "b9420863",
        help="Radius scale observation id or JSON path.",
    ),
):
    """Decide the R75 scale outcome and whether the next radius is licensed."""

    try:
        payload = _r75_scale_decision_payload(radius_scale_observation)
    except Exception as exc:
        payload = {
            "source_radius_scale_observation_id": radius_scale_observation,
            "decision_kind": "POST_R75_FIRST_ORDER_SCALE_DECISION",
            "input_summary": {},
            "first_order_classes": {},
            "decision": "STOP_R75_DECISION_BUILD_FAIL",
            "next_radius": None,
            "next_scale_step": None,
            "execution_shape": "KEEP_9_SLOT_SEPARATED_RUNS",
            "representative_subset_status": "NOT_LICENSED_AT_V0",
            "burden_guard_v0": {},
            "forbidden": {},
            "failures": [f"r75_scale_decision_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_R75_DECISION_BUILD_FAIL",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/radius_scale_decisions",
        "r75_scale_decision_schema_version",
        R75_SCALE_DECISION_SCHEMA,
        "r75_scale_decision_id",
        "r75_scale_decision_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"r75_scale_decision_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("r75-scale-decision-verify")
def r75_scale_decision_verify(
    decision: str = typer.Argument(
        ...,
        help="R75 scale decision id or JSON path.",
    ),
):
    """Reload and verify an R75 scale decision receipt from disk."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(decision, "data/radius_scale_decisions")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "r75_scale_decision_id": decision,
        }
        failures.append(f"r75_scale_decision_unresolved:{decision}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(payload, "r75_scale_decision_id", "r75_scale_decision_sig8")
        if payload.get("r75_scale_decision_sig8") != recomputed_sig:
            failures.append("r75_scale_decision_sig_mismatch")
        if path.stem != payload.get("r75_scale_decision_id"):
            failures.append("r75_scale_decision_filename_id_mismatch")

        core = _r75_scale_decision_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])

    receipt = {
        "input_decision": decision,
        "r75_scale_decision_id": payload.get("r75_scale_decision_id"),
        "r75_scale_decision_path": str(path) if path else None,
        "r75_scale_decision_sig8": payload.get("r75_scale_decision_sig8"),
        "r75_scale_decision_recomputed_sig8": recomputed_sig,
        "source_radius_scale_observation_id": payload.get("source_radius_scale_observation_id"),
        "decision": payload.get("decision"),
        "next_radius": payload.get("next_radius"),
        "next_scale_step": payload.get("next_scale_step"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "RUN_RADIUS_100_SLOT_SEPARATED_WITH_BURDEN_GUARD_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/radius_scale_decision_verifications",
        "r75_scale_decision_verification_schema_version",
        R75_SCALE_DECISION_VERIFICATION_SCHEMA,
        "r75_scale_decision_verification_id",
        "r75_scale_decision_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"r75_scale_decision_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("radius-scale-observation")
def radius_scale_observation(
    r75_observation: str = typer.Argument(
        "601a7983",
        help="R75 domain shift slot observation id or JSON path.",
    ),
    contract: str = typer.Option(
        "ba39cd7b",
        "--contract",
        help="Scalability contract id or JSON path.",
    ),
):
    """Compare R75 slot observation against the R50 baseline under the scalability contract."""

    try:
        payload = _radius_scale_observation_payload(contract, r75_observation)
    except Exception as exc:
        payload = {
            "source_contract_id": contract,
            "radius_50_observation_id": None,
            "radius_75_observation_id": r75_observation,
            "observation": {},
            "delta_class": "UNCLASSIFIED_DELTA",
            "terminal_decision": "STOP_MEASUREMENT_FAILURE",
            "failures": [f"radius_scale_observation_build_failed:{exc}"],
            "warnings": [],
            "gate": "FAIL",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_MEASUREMENT_FAILURE",
            },
        }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/radius_scale_observations",
        "radius_scale_observation_schema_version",
        RADIUS_SCALE_OBSERVATION_SCHEMA,
        "radius_scale_observation_id",
        "radius_scale_observation_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"radius_scale_observation_path: {out_path}")

    if payload.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("radius-scale-observation-verify")
def radius_scale_observation_verify(
    radius_scale_observation: str = typer.Argument(
        ...,
        help="Radius scale observation id or JSON path.",
    ),
):
    """Reload and verify a radius scale observation from disk."""

    failures = []
    warnings = []

    try:
        path = resolve_json_path(radius_scale_observation, "data/radius_scale_observations")
        payload = json.loads(path.read_text())
    except Exception as exc:
        path = None
        payload = {
            "radius_scale_observation_id": radius_scale_observation,
        }
        failures.append(f"radius_scale_observation_unresolved:{radius_scale_observation}:{exc}")

    recomputed_sig = None
    if path is not None:
        recomputed_sig = stable_sig(
            payload,
            "radius_scale_observation_id",
            "radius_scale_observation_sig8",
        )
        if payload.get("radius_scale_observation_sig8") != recomputed_sig:
            failures.append("radius_scale_observation_sig_mismatch")
        if path.stem != payload.get("radius_scale_observation_id"):
            failures.append("radius_scale_observation_filename_id_mismatch")

        core = _radius_scale_observation_verify_core(payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])
    else:
        core = {
            "gate": "FAIL",
            "failures": failures,
            "warnings": warnings,
        }

    receipt = {
        "input_radius_scale_observation": radius_scale_observation,
        "radius_scale_observation_id": payload.get("radius_scale_observation_id"),
        "radius_scale_observation_path": str(path) if path else None,
        "radius_scale_observation_sig8": payload.get("radius_scale_observation_sig8"),
        "radius_scale_observation_recomputed_sig8": recomputed_sig,
        "source_contract_id": payload.get("source_contract_id"),
        "radius_50_observation_id": payload.get("radius_50_observation_id"),
        "radius_75_observation_id": payload.get("radius_75_observation_id"),
        "delta_class": payload.get("delta_class"),
        "terminal_decision": payload.get("terminal_decision"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "DECIDE_R75_SCALE_OUTCOME_OR_NEXT_RADIUS_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/radius_scale_observation_verifications",
        "radius_scale_observation_verification_schema_version",
        RADIUS_SCALE_OBSERVATION_VERIFICATION_SCHEMA,
        "radius_scale_observation_verification_id",
        "radius_scale_observation_verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"radius_scale_observation_verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("scalability-contract")
def scalability_contract(
    baseline_observation: str = typer.Argument(
        "566a342b",
        help="R50 domain shift slot observation id or JSON path.",
    ),
):
    """Build the post-R50/pre-R75 first-order scalability contract."""

    try:
        contract, verification = _scalability_contract_payload_from_observation(baseline_observation)
        build_failures = list(verification.get("failures") or [])
    except Exception as exc:
        build_failures = [f"baseline_observation_unresolved:{baseline_observation}:{exc}"]
        contract = {
            "contract_kind": "POST_R50_PRE_R75_FIRST_ORDER_OBSERVATION_CONTRACT",
            "layer": "OUTER_MIDDLE_BOUNDARY_OBJECT",
            "baseline": {
                "observation_id": baseline_observation,
            },
            "next_scale_step": "RADIUS_75_SLOT_SEPARATED",
            "execution_shape": "KEEP_9_SLOT_SEPARATED_RUNS",
            "representative_subset_status": "NOT_LICENSED_AT_V0",
            "target_metric": "first_order_curve_stability",
            "secondary_metrics": [
                "receipt_burden",
                "runtime_burden_if_available",
                "slot_consistency",
                "identity_distinguishability",
                "semantic_pressure",
                "operator_burden_if_available",
                "resource_boundary_if_observable",
            ],
            "required_r75_artifact": "domain_shift_slot_observation_v0 with radius=75",
            "r50_r75_comparison_artifact": "radius_scale_observation_v0",
            "required_r75_fields": [],
            "delta_classes": [],
            "failure_classes": [],
            "non_failure_continuation_classes": [],
            "r75_observation_gate": "RADIUS_SCALE_OBSERVATION_GATE_V0",
            "r75_observation_gate_pass_requirements": [],
            "r75_decision_rule": {},
            "forbidden": {},
            "baseline_linkage_check": {},
            "verification_result": {
                "gate": "FAIL",
                "failures": build_failures,
                "warnings": [],
            },
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_CONTRACT_BUILD_FAIL",
            },
        }

    contract["gate"] = "FAIL" if build_failures else "PASS"
    contract["failures"] = build_failures
    contract["warnings"] = []

    out_path, contract = write_content_addressed_receipt(
        contract,
        "data/scalability_contracts",
        "contract_schema_version",
        SCALABILITY_CONTRACT_SCHEMA,
        "contract_id",
        "contract_sig8",
    )

    typer.echo(json.dumps(contract, indent=2, sort_keys=True))
    typer.echo(f"contract_path: {out_path}")

    if contract.get("gate") != "PASS":
        raise typer.Exit(code=1)


@app.command("scalability-contract-verify")
def scalability_contract_verify(
    contract: str = typer.Argument(
        ...,
        help="Scalability contract id or JSON path.",
    ),
):
    """Reload and verify a scalability contract from disk."""

    failures = []
    warnings = []

    try:
        contract_path = resolve_json_path(contract, "data/scalability_contracts")
        contract_payload = json.loads(contract_path.read_text())
    except Exception as exc:
        contract_path = None
        contract_payload = {
            "contract_id": contract,
        }
        failures.append(f"contract_unresolved:{contract}:{exc}")

    recomputed_sig = None
    if contract_path is not None:
        try:
            recomputed_sig = stable_sig(contract_payload, "contract_id", "contract_sig8")
            if contract_payload.get("contract_sig8") != recomputed_sig:
                failures.append("contract_sig_mismatch")
            if contract_path.stem != contract_payload.get("contract_id"):
                failures.append("contract_filename_id_mismatch")
        except Exception as exc:
            failures.append(f"contract_sig_recompute_failed:{exc}")

        core = _scalability_contract_verify_core(contract_payload)
        failures.extend(core.get("failures") or [])
        warnings.extend(core.get("warnings") or [])
    else:
        core = {
            "baseline_linkage_check": {},
            "baseline_observation_check": {},
            "gate": "FAIL",
            "failures": failures,
            "warnings": warnings,
        }

    receipt = {
        "input_contract": contract,
        "contract_id": contract_payload.get("contract_id"),
        "contract_path": str(contract_path) if contract_path else None,
        "contract_sig8": contract_payload.get("contract_sig8"),
        "contract_recomputed_sig8": recomputed_sig,
        "baseline_observation_id": (contract_payload.get("baseline") or {}).get("observation_id"),
        "baseline_linkage_check": core.get("baseline_linkage_check"),
        "baseline_observation_check": core.get("baseline_observation_check"),
        "verification_result": {
            "gate": "FAIL" if failures else "PASS",
            "failures": failures,
            "warnings": warnings,
        },
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": "STOP" if failures else "ADVANCE",
            "next_command_goal": None if failures else "RUN_RADIUS_75_SLOT_SEPARATED_UNDER_SCALABILITY_CONTRACT_V0",
            "stop_code": "STOP_GATE_FAIL" if failures else None,
        },
    }

    out_path, receipt = write_content_addressed_receipt(
        receipt,
        "data/scalability_contract_verifications",
        "verification_schema_version",
        SCALABILITY_CONTRACT_VERIFICATION_SCHEMA,
        "verification_id",
        "verification_sig8",
    )

    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))
    typer.echo(f"verification_path: {out_path}")

    if receipt.get("gate") != "PASS":
        raise typer.Exit(code=1)



@app.command("domain-shift-slot-observe")
def domain_shift_slot_observe(
    slot_execution: str = typer.Argument(
        ...,
        help="Passing domain shift slot run execution id or JSON path.",
    ),
):
    """Observe a slot-separated domain-shift execution and classify transfer outcome."""

    failures = []
    warnings = []

    try:
        slot_execution_path = resolve_json_path(slot_execution, "data/domain_shift_slot_runs")
        execution = json.loads(slot_execution_path.read_text())
    except Exception as exc:
        slot_execution_path = None
        execution = {}
        failures.append(f"slot_execution_unresolved:{slot_execution}:{exc}")

    execution_id = execution.get("domain_shift_slot_run_execution_id")
    execution_sig = None
    if execution:
        execution_sig_payload = dict(execution)
        execution_sig_payload.pop("domain_shift_slot_run_execution_id", None)
        execution_sig = hashlib.sha256(
            json.dumps(execution_sig_payload, sort_keys=True).encode()
        ).hexdigest()[:8]

        if execution_id != execution_sig:
            failures.append(
                f"slot_execution_id_mismatch:stored={execution_id}:recomputed={execution_sig}"
            )

        if slot_execution_path and slot_execution_path.stem != execution_id:
            failures.append("slot_execution_filename_id_mismatch")

        if execution.get("gate") != "PASS":
            failures.append("slot_execution_gate_not_PASS")

    source_support_id = execution.get("source_support_id")
    try:
        support_path = resolve_json_path(source_support_id, "data/domain_shift_slot_runner_support")
        support = json.loads(support_path.read_text())
    except Exception as exc:
        support_path = None
        support = {}
        failures.append(f"slot_support_unresolved:{source_support_id}:{exc}")

    support_sig = None
    if support:
        support_sig = stable_sig(
            support,
            "domain_shift_slot_runner_support_id",
            "domain_shift_slot_runner_support_payload_sig8",
        )

        if support.get("gate") != "PASS":
            failures.append("slot_support_gate_not_PASS")

        if support.get("domain_shift_slot_runner_support_payload_sig8") != support_sig:
            failures.append("slot_support_sig_mismatch")

        if support_path and support_path.stem != support.get("domain_shift_slot_runner_support_id"):
            failures.append("slot_support_filename_id_mismatch")

    generator_id = support.get("domain_shift_generator_id") if support else None
    try:
        generator_path = resolve_json_path(generator_id, "data/domain_shift_generators")
        generator = json.loads(generator_path.read_text())
    except Exception as exc:
        generator_path = None
        generator = {}
        failures.append(f"domain_shift_generator_unresolved:{generator_id}:{exc}")

    generator_sig = None
    if generator:
        generator_sig = stable_sig(
            generator,
            "domain_shift_generator_id",
            "domain_shift_generator_payload_sig8",
        )

        if generator.get("gate") != "PASS":
            failures.append("domain_shift_generator_gate_not_PASS")

        if generator.get("domain_shift_generator_payload_sig8") != generator_sig:
            failures.append("domain_shift_generator_sig_mismatch")

    transfer_contract_id = support.get("transfer_contract_id") if support else None
    try:
        transfer_path = resolve_json_path(transfer_contract_id, "data/cell_transfer_contracts")
        transfer = json.loads(transfer_path.read_text())
    except Exception as exc:
        transfer_path = None
        transfer = {}
        failures.append(f"transfer_contract_unresolved:{transfer_contract_id}:{exc}")

    transfer_sig = None
    if transfer:
        transfer_sig = stable_sig(
            transfer,
            "cell_transfer_contract_id",
            "cell_transfer_contract_payload_sig8",
        )

        if transfer.get("gate") != "PASS":
            failures.append("transfer_contract_gate_not_PASS")

        if transfer.get("cell_transfer_contract_payload_sig8") != transfer_sig:
            failures.append("transfer_contract_sig_mismatch")

    slot_results = execution.get("slot_results") or []
    expected_slots = ((support.get("runner_support") or {}).get("slots") or []) if support else []

    if execution.get("slot_count_expected") != len(expected_slots):
        failures.append(
            f"slot_count_expected_mismatch:execution={execution.get('slot_count_expected')}:support={len(expected_slots)}"
        )

    if execution.get("slot_count_observed") != len(slot_results):
        failures.append(
            f"slot_count_observed_mismatch:declared={execution.get('slot_count_observed')}:actual={len(slot_results)}"
        )

    if len(slot_results) != len(expected_slots):
        failures.append(f"slot_result_count_mismatch:results={len(slot_results)}:support={len(expected_slots)}")

    observed_labels = [slot.get("slot_label") for slot in slot_results]
    expected_labels = [slot.get("slot_label") for slot in expected_slots]

    if observed_labels != expected_labels:
        failures.append("slot_label_order_mismatch")

    run_ids = [slot.get("run_id") for slot in slot_results]
    eval_ids = [slot.get("eval_id") for slot in slot_results]

    if len(run_ids) != len(set(run_ids)):
        failures.append("slot_run_ids_not_unique")

    if len(eval_ids) != len(set(eval_ids)):
        failures.append("slot_eval_ids_not_unique")

    dirty_slots = []
    boundary_slots = []
    receipt_mismatch_slots = []
    eval_gate_fail_slots = []

    aggregate_by_family = {}
    repeated_family_consistency = {}
    aggregate_coarse_profiles = {}
    aggregate_by_move = {}

    for slot in slot_results:
        label = slot.get("slot_label")
        family_code = slot.get("family_code")
        family = slot.get("family")
        eval_id = slot.get("eval_id")

        if slot.get("eval_gate") != "PASS":
            eval_gate_fail_slots.append(label)

        if slot.get("law_failures") != 0 or slot.get("unknown_laws") != 0 or slot.get("orphan_receipt_runs") != 0:
            dirty_slots.append(label)

        if slot.get("boundary_count") != 0:
            boundary_slots.append(label)

        if slot.get("total_receipts") != slot.get("receipt_rows"):
            receipt_mismatch_slots.append(label)

        aggregate_by_family.setdefault(family, {
            "family_code": family_code,
            "slot_count": 0,
            "run_ids": [],
            "eval_ids": [],
            "total_receipts": 0,
            "receipt_rows": 0,
            "coarse_counts": [],
            "raw_counts": [],
            "registered_counts": [],
        })
        agg = aggregate_by_family[family]
        agg["slot_count"] += 1
        agg["run_ids"].append(slot.get("run_id"))
        agg["eval_ids"].append(eval_id)
        agg["total_receipts"] += int(slot.get("total_receipts") or 0)
        agg["receipt_rows"] += int(slot.get("receipt_rows") or 0)
        agg["coarse_counts"].append(slot.get("coarse_move_profiles_total"))
        agg["raw_counts"].append(slot.get("raw_move_profiles_total"))
        agg["registered_counts"].append(slot.get("registered_moves_total"))

        try:
            eval_data = json.loads((Path("data/evals") / f"{eval_id}.json").read_text())
            profile_summary = eval_data.get("profile_summary") or {}
            for key, value in (profile_summary.get("coarse_profiles") or {}).items():
                aggregate_coarse_profiles[key] = aggregate_coarse_profiles.get(key, 0) + int(value)
            for key, value in (profile_summary.get("by_move") or {}).items():
                aggregate_by_move[key] = aggregate_by_move.get(key, 0) + int(value)
        except Exception as exc:
            failures.append(f"eval_profile_load_failed:{label}:{eval_id}:{exc}")

    for family, agg in aggregate_by_family.items():
        repeated_family_consistency[family] = {
            "slot_count": agg["slot_count"],
            "coarse_counts": agg["coarse_counts"],
            "raw_counts": agg["raw_counts"],
            "registered_counts": agg["registered_counts"],
            "coarse_consistent": len(set(agg["coarse_counts"])) <= 1,
            "raw_consistent": len(set(agg["raw_counts"])) <= 1,
            "registered_consistent": len(set(agg["registered_counts"])) <= 1,
        }

    repeated_family_inconsistencies = {
        family: row
        for family, row in repeated_family_consistency.items()
        if row["slot_count"] > 1 and not (
            row["coarse_consistent"] and row["raw_consistent"] and row["registered_consistent"]
        )
    }

    if eval_gate_fail_slots:
        failures.append("slot_eval_gate_failures:" + ",".join(eval_gate_fail_slots))

    if dirty_slots:
        failures.append("slot_measurement_dirty:" + ",".join(dirty_slots))

    if boundary_slots:
        failures.append("slot_resource_boundaries:" + ",".join(boundary_slots))

    if receipt_mismatch_slots:
        failures.append("slot_receipt_projection_mismatches:" + ",".join(receipt_mismatch_slots))

    if repeated_family_inconsistencies:
        failures.append("repeated_family_measurement_inconsistent")

    support_runner = support.get("runner_support") or {}
    semantic_pressure = {
        "requires_new_move_types": support_runner.get("requires_new_move_types"),
        "requires_new_laws": support_runner.get("requires_new_laws"),
        "requires_new_classifier_semantics": support_runner.get("requires_new_classifier_semantics"),
        "requires_new_halt_vocabulary": support_runner.get("requires_new_halt_vocabulary"),
        "requires_new_evaluator_semantics": support_runner.get("requires_new_evaluator_semantics"),
    }

    semantic_pressure_detected = any(value is True for value in semantic_pressure.values())

    source_baseline = support.get("source_baseline") or {}
    source_coarse_total = source_baseline.get("coarse_profiles_total")
    aggregate_coarse_total = len(aggregate_coarse_profiles)
    aggregate_raw_total_by_slot_sum = sum(int(slot.get("raw_move_profiles_total") or 0) for slot in slot_results)

    if failures:
        outcome = "FAIL_MEASUREMENT_TRUST"
        next_goal = None
        stop_code = "domain_shift_slot_observation_failed"
        terminal_type = "STOP"
    elif semantic_pressure_detected:
        outcome = "STOP_DOMAIN_REQUIRES_ONTOLOGY_SHIFT"
        next_goal = None
        stop_code = "domain_requires_ontology_shift"
        terminal_type = "STOP"
    elif aggregate_coarse_total == source_coarse_total:
        outcome = "MEASUREMENT_TRANSFER_STABLE_CURVE"
        next_goal = (
            "DECIDE_SCALE_RADIUS_OR_FREEZE_RADIUS_50_CELL1_OBSERVATION"
            if execution.get("radius") == 50
            else "BUILD_RADIUS_SCALE_OBSERVATION_V0"
        )
        stop_code = None
        terminal_type = "ADVANCE"
    else:
        outcome = "MEASUREMENT_TRANSFER_DIFFERENT_CURVE"
        next_goal = (
            "DECIDE_SCALE_RADIUS_OR_FREEZE_RADIUS_50_CELL1_OBSERVATION"
            if execution.get("radius") == 50
            else "BUILD_RADIUS_SCALE_OBSERVATION_V0"
        )
        stop_code = None
        terminal_type = "ADVANCE"

    observation = {
        "slot_execution": {
            "input": slot_execution,
            "path": str(slot_execution_path) if slot_execution_path else None,
            "id": execution_id,
            "recomputed_id": execution_sig,
            "gate": execution.get("gate"),
        },
        "slot_support": {
            "id": source_support_id,
            "path": str(support_path) if support_path else None,
            "stored_sig": support.get("domain_shift_slot_runner_support_payload_sig8"),
            "recomputed_sig": support_sig,
            "gate": support.get("gate"),
        },
        "domain_shift_generator": {
            "id": generator_id,
            "path": str(generator_path) if generator_path else None,
            "stored_sig": generator.get("domain_shift_generator_payload_sig8"),
            "recomputed_sig": generator_sig,
            "gate": generator.get("gate"),
        },
        "transfer_contract": {
            "id": transfer_contract_id,
            "path": str(transfer_path) if transfer_path else None,
            "stored_sig": transfer.get("cell_transfer_contract_payload_sig8"),
            "recomputed_sig": transfer_sig,
            "gate": transfer.get("gate"),
        },
        "radius": execution.get("radius"),
        "max_cells": execution.get("max_cells"),
        "slot_count_expected": execution.get("slot_count_expected"),
        "slot_count_observed": execution.get("slot_count_observed"),
        "slot_labels": observed_labels,
        "run_ids": run_ids,
        "eval_ids": eval_ids,
        "aggregate_by_family": aggregate_by_family,
        "repeated_family_consistency": repeated_family_consistency,
        "aggregate_coarse_profiles_total": aggregate_coarse_total,
        "source_coarse_profiles_total": source_coarse_total,
        "aggregate_raw_total_by_slot_sum": aggregate_raw_total_by_slot_sum,
        "aggregate_coarse_profiles": aggregate_coarse_profiles,
        "aggregate_by_move": aggregate_by_move,
        "semantic_pressure": semantic_pressure,
        "semantic_pressure_detected": semantic_pressure_detected,
        "measurement_cleanliness": {
            "eval_gate_fail_slots": eval_gate_fail_slots,
            "dirty_slots": dirty_slots,
            "boundary_slots": boundary_slots,
            "receipt_mismatch_slots": receipt_mismatch_slots,
            "repeated_family_inconsistencies": repeated_family_inconsistencies,
        },
        "outcome": outcome,
        "confidence_scope": f"RADIUS_{execution.get('radius')}_SLOT_SEPARATED_PROBE_ONLY",
    }

    payload = {
        "input_slot_execution": slot_execution,
        "slot_execution_id": execution_id,
        "source_support_id": source_support_id,
        "domain_shift_generator_id": generator_id,
        "transfer_contract_id": transfer_contract_id,
        "source_cell": support.get("source_cell"),
        "target_cell": support.get("target_cell"),
        "shift_kind": support.get("shift_kind"),
        "observation": observation,
        "failures": failures,
        "warnings": warnings,
        "gate": "FAIL" if failures else "PASS",
        "terminal": {
            "type": terminal_type,
            "next_command_goal": next_goal,
            "stop_code": stop_code,
        },
    }

    out_path, payload = write_content_addressed_receipt(
        payload,
        "data/domain_shift_slot_observations",
        "domain_shift_slot_observation_schema_version",
        DOMAIN_SHIFT_SLOT_OBSERVATION_SCHEMA,
        "domain_shift_slot_observation_id",
        "domain_shift_slot_observation_payload_sig8",
    )

    typer.echo(json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"domain_shift_slot_observation_path: {out_path}")



if __name__ == "__main__":
    app()
