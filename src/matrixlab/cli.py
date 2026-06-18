from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import typer
from rich import print


app = typer.Typer(help="MatrixLab receipt runner v0")


FAMILY_MAP = {
    "A": "one_sided_suspension",
    "B": "two_sided_suspension",
    "C": "suspension_plus_repair",
    "D": "projection_quotient",
    "E": "relabel_symmetry_stress",
}


def sig8(obj) -> str:
    """Small deterministic fingerprint for receipts."""
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:8]


def matrix_sig8(a: np.ndarray) -> str:
    body = {
        "shape": list(a.shape),
        "data": a.astype(int).tolist(),
    }
    return sig8(body)


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
    Simple cycle incidence-style binary matrix.
    Rows = vertices.
    Columns = edges.
    Each edge touches two vertices.
    """
    a = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        a[i, i] = 1
        a[(i + 1) % n, i] = 1
    return a


def apply_move(a: np.ndarray, family: str, cycle_n: int) -> tuple[np.ndarray, str]:
    """Apply one deterministic lawful-ish mutation family."""
    rows, cols = a.shape

    if family == "one_sided_suspension":
        # Duplicate an existing column. No new column type.
        j = cycle_n % cols
        new_col = a[:, [j]]
        return np.concatenate([a, new_col], axis=1), "duplicate_existing_column"

    if family == "two_sided_suspension":
        # Add one row and one column touching old bottom + new row.
        out = np.zeros((rows + 1, cols + 1), dtype=np.uint8)
        out[:rows, :cols] = a
        out[rows - 1, cols] = 1
        out[rows, cols] = 1
        return out, "add_row_and_link_column"

    if family == "suspension_plus_repair":
        # Add a repair column equal to xor of two existing columns.
        j1 = cycle_n % cols
        j2 = (cycle_n + 1) % cols
        repair = (a[:, [j1]] ^ a[:, [j2]])
        return np.concatenate([a, repair], axis=1), "xor_repair_column"

    if family == "projection_quotient":
        # Occasionally merge/drop a row; otherwise add harmless zero column.
        if rows > 2 and cycle_n % 2 == 0:
            out = a.copy()
            out[0] ^= out[-1]
            out = out[:-1, :]
            return out, "quotient_merge_last_row"
        zero = np.zeros((rows, 1), dtype=np.uint8)
        return np.concatenate([a, zero], axis=1), "append_zero_column"

    if family == "relabel_symmetry_stress":
        # Deterministic row/column relabeling.
        row_shift = cycle_n % rows
        col_shift = cycle_n % cols
        out = np.roll(a, shift=row_shift, axis=0)
        out = np.roll(out, shift=col_shift, axis=1)
        return out, "relabel_rows_and_columns"

    raise ValueError(f"Unknown family: {family}")


@app.command()
def run(
    depth_min: int = typer.Option(3, help="Smallest cycle length/depth."),
    depth_max: int = typer.Option(8, help="Largest cycle length/depth."),
    families: str = typer.Option("A,B,C,D,E", help="Comma-separated family letters."),
    run_id: Optional[str] = typer.Option(None, help="Optional run id."),
):
    """
    Run small matrix mutation sweeps and write receipts.
    """
    if run_id is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{stamp}"

    selected = [x.strip().upper() for x in families.split(",") if x.strip()]
    family_names = [FAMILY_MAP[x] for x in selected]

    run_dir = Path("data/runs") / run_id
    receipt_dir = Path("data/receipts") / run_id
    trace_dir = Path("data/traces") / run_id

    run_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    all_receipts = []

    print(f"[bold green]MatrixLab run started[/bold green]: {run_id}")

    for n in range(depth_min, depth_max + 1):
        for family in family_names:
            case_id = f"n{n}_{family}"
            case_receipts = []
            registered_moves = set()
            trajectory = []

            a = base_cycle_matrix(n)

            for cycle_n in range(1, n + 1):
                before_sig = matrix_sig8(a)
                before_rank = gf2_rank(a)

                a, move_id = apply_move(a, family, cycle_n)

                after_sig = matrix_sig8(a)
                after_rank = gf2_rank(a)

                new_move_required = move_id not in registered_moves
                registered_moves.add(move_id)
                trajectory.append(after_sig)

                receipt = {
                    "run_id": run_id,
                    "case_id": case_id,
                    "family": family,
                    "depth": n,
                    "cycle_n": cycle_n,
                    "move_id": move_id,
                    "registered_moves_total": len(registered_moves),
                    "moves_reused": cycle_n - len(registered_moves),
                    "new_move_required": new_move_required,
                    "matrix_shape": list(a.shape),
                    "rank_before": before_rank,
                    "rank_after": after_rank,
                    "state_sig8_before": before_sig,
                    "state_sig8_after": after_sig,
                    "compression_ratio": round(cycle_n / len(registered_moves), 4),
                    "trajectory_signature": sig8(trajectory),
                    "halt_reason": None,
                }

                case_receipts.append(receipt)
                all_receipts.append(receipt)

                case_path = receipt_dir / case_id
                case_path.mkdir(parents=True, exist_ok=True)

                with open(case_path / f"cycle_{cycle_n:04d}.json", "w") as f:
                    json.dump(receipt, f, indent=2, sort_keys=True)

            final_receipt = case_receipts[-1]
            final_receipt["halt_reason"] = "DEPTH_COMPLETE"

            with open(trace_dir / f"{case_id}.json", "w") as f:
                json.dump(
                    {
                        "run_id": run_id,
                        "case_id": case_id,
                        "trajectory": trajectory,
                        "trajectory_signature": sig8(trajectory),
                        "final_shape": list(a.shape),
                        "final_rank": gf2_rank(a),
                    },
                    f,
                    indent=2,
                    sort_keys=True,
                )

    summary = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "families": family_names,
        "depth_min": depth_min,
        "depth_max": depth_max,
        "total_receipts": len(all_receipts),
        "total_cases": (depth_max - depth_min + 1) * len(family_names),
        "max_registered_moves": max(r["registered_moves_total"] for r in all_receipts),
        "max_compression_ratio": max(r["compression_ratio"] for r in all_receipts),
    }

    with open(run_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    print("[bold green]Done.[/bold green]")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    app()
