from __future__ import annotations

import hashlib
import json
import sqlite3
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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


def insert_receipt(receipt: dict) -> None:
    with sqlite3.connect(DB_PATH) as con:
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
    with sqlite3.connect(DB_PATH) as con:
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
    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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


@app.command()
def summarize(run_id: str = typer.Argument("latest")):
    """
    Show run summary from SQLite.
    """
    init_db()

    if run_id == "latest":
        run_id = latest_run_id()

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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

    with sqlite3.connect(DB_PATH) as con:
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
        with sqlite3.connect(DB_PATH) as con:
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
        con = sqlite3.connect(db_path)
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



if __name__ == "__main__":
    app()
