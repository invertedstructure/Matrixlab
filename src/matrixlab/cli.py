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
    selected = [x.strip().upper() for x in families.split(",") if x.strip()]
    unknown = [x for x in selected if x not in FAMILY_MAP]

    if unknown:
        raise typer.BadParameter(f"Unknown family letters: {unknown}")

    return [FAMILY_MAP[x] for x in selected]


def execute_run(
    depth_min: int,
    depth_max: int,
    families: str,
    cycles_per_case: int,
    max_cells: int,
    run_id: Optional[str],
) -> dict:
    if run_id is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{stamp}"

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
        max_cells=max_cells,
    )

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

                new_move_required = profile_id not in registered_moves
                registered_moves.add(profile_id)
                trajectory.append(after_sig)

                rows, cols = a.shape
                cells = rows * cols

                current_halt = None

                if cells > max_cells:
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
    run_id: Optional[str] = typer.Option(None, help="Optional run id."),
):
    execute_run(
        depth_min=depth_min,
        depth_max=depth_max,
        families=families,
        cycles_per_case=cycles_per_case,
        max_cells=max_cells,
        run_id=run_id,
    )


@app.command()
def stress(
    depth_max: int = typer.Option(100, help="Push depth upward."),
    cycles_per_case: int = typer.Option(100, help="Push cycles upward."),
    max_cells: int = typer.Option(250_000, help="Hard matrix cell limit."),
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


if __name__ == "__main__":
    app()
