#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SURFACE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_receipts"
SURFACE_MANIFEST_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_manifests"
SURFACE_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_rows"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_no_candidate_rows_diagnostics"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_no_candidate_rows_diagnostic_receipts"

DIAGNOSTIC_NAME = "DIAGNOSE_APPROVED_RECIPE_NO_CANDIDATE_COMPATIBLE_ROWS_V0"
SOURCE_SURFACE_ID = "14bbc077"
SOURCE_RECEIPT_ID = "9c2b75ec"
SOURCE_POLICY_ID = "3b22a690"
SOURCE_POLICY_RECEIPT_ID = "36177050"
EXPLICIT_RUN_ID = "run_20260621_183812_136149"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

REQUIRED_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FIELD_ALIASES = {
    "cv": ["cv"],
    "state_hash_before": [
        "state_hash_before",
        "state_sig8_before",
        "state_before_hash",
        "before_state_hash",
        "pre_state_hash",
    ],
    "move_id": [
        "move_id",
        "move",
        "move_kind",
        "transition_move_id",
        "selected_move",
    ],
    "state_hash_after": [
        "state_hash_after",
        "state_sig8_after",
        "state_after_hash",
        "after_state_hash",
        "post_state_hash",
    ],
    "raw_compression_ratio_sig6": [
        "compression_ratio",
        "raw_compression_ratio",
        "raw_compression_ratio_sig6",
    ],
}

SUSPICIOUS_DERIVATION_SOURCES = [
    "raw_total_before",
    "raw_total_after",
    "delta_raw_total",
    "active_cells_before",
    "active_cells_after",
    "delta_active_cells",
    "full_receipt_bytes",
    "projected_plus_signature_payload_bytes",
    "signature_payload_bytes",
    "projected_scale_row_bytes",
]

FORBIDDEN_AUTHORITY_TRUE = [
    "candidate_accepted",
    "scale_mode_authorized",
    "registry_inserted",
    "registry_written",
    "registry_sqlite_read",
    "full_registry_scan_used",
    "runtime_semantic_changed",
    "runtime_code_changed",
    "runtime_receipt_emission_changed",
    "latest_or_mtime_selection_used",
    "ambient_workspace_inference_used",
    "case_id_or_cycle_n_identity_patch_used",
    "rowid_or_receipt_hash_truth_surface_used",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "microhash_as_proof_used",
    "synthetic_fake_validation_rows_used",
    "transition_compression_probe_run",
]

NEXT_IF_ALIAS_FIX = "PATCH_APPROVED_RECIPE_CANDIDATE_FIELD_ALIAS_EXTRACTOR_V0"
NEXT_IF_DERIVED_METRIC = "PROPOSE_APPROVED_RECIPE_DERIVED_RAW_COMPRESSION_RATIO_RULE_V0"
NEXT_IF_NO_LAWFUL_SOURCE = "HOLD_APPROVED_RECIPE_NO_LAWFUL_CANDIDATE_FIELD_SOURCE"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def iter_json_from_file(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        if path.suffix == ".json":
            obj = json.loads(path.read_text(errors="ignore"))
            return [obj] if isinstance(obj, dict) else []
        if path.suffix == ".jsonl":
            out = []
            for line in path.read_text(errors="ignore").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if isinstance(obj, dict):
                    out.append(obj)
            return out
    except Exception:
        return []
    return []


def flatten_keys(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.append((key, v))
            out.extend(flatten_keys(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f"{prefix}[{i}]"
            out.extend(flatten_keys(v, key))
    return out


def find_aliases(obj: dict[str, Any], aliases: list[str]) -> dict[str, list[Any]]:
    hits: dict[str, list[Any]] = {a: [] for a in aliases}
    for key_path, value in flatten_keys(obj):
        leaf = key_path.split(".")[-1]
        leaf = re.sub(r"\[\d+\]$", "", leaf)
        if leaf in hits:
            hits[leaf].append(value)
    return {k: v for k, v in hits.items() if v}


def numeric_like(value: Any) -> bool:
    try:
        x = float(value)
    except Exception:
        return False
    return x == x and x not in (float("inf"), float("-inf"))


def classify_field_availability(obj: dict[str, Any]) -> dict[str, Any]:
    fields = {}
    for field, aliases in FIELD_ALIASES.items():
        hits = find_aliases(obj, aliases)
        present = bool(hits)
        numeric_valid = None
        if field == "raw_compression_ratio_sig6":
            numeric_valid = any(numeric_like(v) for values in hits.values() for v in values)
        fields[field] = {
            "present": present,
            "aliases_present": sorted(hits.keys()),
            "hit_count": sum(len(v) for v in hits.values()),
            "numeric_valid": numeric_valid,
            "sample_values": [
                str(v)[:160]
                for values in hits.values()
                for v in values[:2]
            ][:6],
        }
    missing = [f for f, info in fields.items() if not info["present"]]
    if fields["raw_compression_ratio_sig6"]["present"] and not fields["raw_compression_ratio_sig6"]["numeric_valid"]:
        missing.append("raw_compression_ratio_sig6_numeric_valid")
    return {
        "fields": fields,
        "missing": missing,
        "candidate_compatible": len(missing) == 0,
    }


def derive_source_hints(obj: dict[str, Any]) -> dict[str, Any]:
    hints = {}
    for key in SUSPICIOUS_DERIVATION_SOURCES:
        hits = find_aliases(obj, [key])
        if hits:
            hints[key] = {
                "hit_count": sum(len(v) for v in hits.values()),
                "sample_values": [str(v)[:160] for values in hits.values() for v in values[:3]][:6],
            }
    return hints


def receipt_case_cycle(path: str) -> dict[str, Any]:
    depth = None
    cycle = None
    m = re.search(r"/n(?P<n>\d+)_", "/" + path)
    if m:
        depth = int(m.group("n"))
    m = re.search(r"/cycle_(?P<c>\d+)\.json$", "/" + path)
    if m:
        cycle = int(m.group("c"))
    return {"depth": depth, "cycle": cycle}


def validate_source_surface(receipt: dict[str, Any], manifest: dict[str, Any], rows_path: Path) -> list[str]:
    failures = []
    if receipt.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"surface_id_wrong:{receipt.get('surface_id')}")
    if receipt.get("receipt_id") != SOURCE_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("policy_id") != SOURCE_POLICY_ID:
        failures.append(f"policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("policy_receipt_id") != SOURCE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('policy_receipt_id')}")
    if receipt.get("explicit_run_id") != EXPLICIT_RUN_ID:
        failures.append(f"explicit_run_id_wrong:{receipt.get('explicit_run_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"source_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("hold_code") != "HOLD_APPROVED_RECIPE_NO_CANDIDATE_COMPATIBLE_ROWS":
        failures.append(f"source_hold_code_wrong:{receipt.get('hold_code')}")
    if receipt.get("rows_created") != 0:
        failures.append(f"source_rows_created_not_zero:{receipt.get('rows_created')}")
    if manifest.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"manifest_surface_id_wrong:{manifest.get('surface_id')}")
    if not rows_path.exists():
        failures.append(f"source_rows_path_missing:{rows_path}")
    elif rows_path.read_text().strip():
        failures.append("source_rows_file_not_empty")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")

    selection = receipt.get("input_selection_summary") or {}
    if selection.get("selector_id") != "BOUNDED_CASE_CYCLE_RECEIPT_SELECTOR_V0":
        failures.append(f"selector_wrong:{selection.get('selector_id')}")
    if selection.get("selected_cycle_receipt_files_total") != 500:
        failures.append(f"selected_cycle_receipt_files_total_wrong:{selection.get('selected_cycle_receipt_files_total')}")
    if selection.get("selected_depths_total") != 10:
        failures.append(f"selected_depths_total_wrong:{selection.get('selected_depths_total')}")
    if selection.get("failure") is not None:
        failures.append(f"selection_failure_not_none:{selection.get('failure')}")

    return failures


def build_diagnostic(surface_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    surface_receipt_path = SURFACE_RECEIPT_DIR / f"{surface_id}.json"
    surface_manifest_path = SURFACE_MANIFEST_DIR / f"{surface_id}.json"
    surface_rows_path = SURFACE_ROWS_DIR / f"{surface_id}.jsonl"

    source_receipt = load_json(surface_receipt_path)
    source_manifest = load_json(surface_manifest_path)
    failures = validate_source_surface(source_receipt, source_manifest, surface_rows_path)

    selection = source_receipt.get("input_selection_summary") or {}
    selected_files = selection.get("selected_files") or []

    file_summaries = []
    aggregate_field_presence = {
        field: {
            "objects_present": 0,
            "objects_missing": 0,
            "aliases": Counter(),
            "sample_values": [],
        }
        for field in REQUIRED_PAYLOAD_FIELDS
    }
    missing_pattern_counts: Counter[str] = Counter()
    candidate_compatible_objects = 0
    objects_seen = 0
    files_read = 0
    files_missing = 0
    derivation_hint_counts: Counter[str] = Counter()
    depth_counts: Counter[int] = Counter()
    cycle_counts: Counter[int] = Counter()

    for rel_path in selected_files:
        path = ROOT / rel_path
        cc = receipt_case_cycle(rel_path)
        if cc["depth"] is not None:
            depth_counts[cc["depth"]] += 1
        if cc["cycle"] is not None:
            cycle_counts[cc["cycle"]] += 1

        if not path.exists():
            files_missing += 1
            file_summaries.append({
                "path": rel_path,
                "exists": False,
                "objects_seen": 0,
                "candidate_compatible": 0,
                "missing_pattern_counts": {},
                "field_presence": {},
                "derivation_hints": {},
            })
            continue

        files_read += 1
        objs = iter_json_from_file(path)
        file_missing_patterns: Counter[str] = Counter()
        file_compatible = 0
        file_field_presence: dict[str, Counter[str]] = {f: Counter() for f in REQUIRED_PAYLOAD_FIELDS}
        file_derivation_hints: Counter[str] = Counter()

        for obj in objs:
            objects_seen += 1
            classified = classify_field_availability(obj)
            missing = classified["missing"]
            if classified["candidate_compatible"]:
                candidate_compatible_objects += 1
                file_compatible += 1

            pattern = "|".join(sorted(missing)) if missing else "COMPATIBLE"
            missing_pattern_counts[pattern] += 1
            file_missing_patterns[pattern] += 1

            for field, info in classified["fields"].items():
                if info["present"]:
                    aggregate_field_presence[field]["objects_present"] += 1
                    file_field_presence[field]["present"] += 1
                    for alias in info["aliases_present"]:
                        aggregate_field_presence[field]["aliases"][alias] += 1
                    for sample in info["sample_values"]:
                        if len(aggregate_field_presence[field]["sample_values"]) < 12:
                            aggregate_field_presence[field]["sample_values"].append(sample)
                else:
                    aggregate_field_presence[field]["objects_missing"] += 1
                    file_field_presence[field]["missing"] += 1

            hints = derive_source_hints(obj)
            for key in hints:
                derivation_hint_counts[key] += 1
                file_derivation_hints[key] += 1

        file_summaries.append({
            "path": rel_path,
            "exists": True,
            "objects_seen": len(objs),
            "candidate_compatible": file_compatible,
            "missing_pattern_counts": dict(file_missing_patterns),
            "field_presence": {k: dict(v) for k, v in file_field_presence.items()},
            "derivation_hints": dict(file_derivation_hints),
        })

    field_presence_clean = {}
    for field, info in aggregate_field_presence.items():
        field_presence_clean[field] = {
            "objects_present": info["objects_present"],
            "objects_missing": info["objects_missing"],
            "aliases": dict(info["aliases"]),
            "sample_values": info["sample_values"],
        }

    missing_all_objects = [
        field for field, info in field_presence_clean.items()
        if info["objects_present"] == 0 and objects_seen > 0
    ]
    present_some_objects = [
        field for field, info in field_presence_clean.items()
        if info["objects_present"] > 0
    ]

    if failures:
        primary_class = "SOURCE_SURFACE_INVALID_FOR_DIAGNOSTIC"
        next_goal = None
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_NO_CANDIDATE_ROWS_DIAGNOSTIC_INVALID_SOURCE",
            "next_command_goal": None,
        }
    elif candidate_compatible_objects > 0:
        primary_class = "EXTRACTOR_LOGIC_FALSE_NEGATIVE"
        next_goal = NEXT_IF_ALIAS_FIX
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_IF_ALIAS_FIX,
        }
    elif "raw_compression_ratio_sig6" in missing_all_objects and any(
        key in derivation_hint_counts
        for key in ["raw_total_before", "raw_total_after", "delta_raw_total", "full_receipt_bytes"]
    ):
        primary_class = "DERIVED_RAW_COMPRESSION_RATIO_RULE_REQUIRED"
        next_goal = NEXT_IF_DERIVED_METRIC
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_IF_DERIVED_METRIC,
        }
    elif "raw_compression_ratio_sig6" in missing_all_objects:
        primary_class = "RAW_COMPRESSION_RATIO_SOURCE_MISSING"
        next_goal = NEXT_IF_DERIVED_METRIC
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_IF_DERIVED_METRIC,
        }
    elif missing_all_objects:
        primary_class = "REQUIRED_NATIVE_FIELDS_MISSING_FROM_RECEIPTS"
        next_goal = NEXT_IF_ALIAS_FIX
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_IF_ALIAS_FIX,
        }
    else:
        primary_class = "UNKNOWN_NO_COMPATIBLE_ROWS_PATTERN"
        next_goal = NEXT_IF_NO_LAWFUL_SOURCE
        terminal = {
            "type": "HOLD",
            "stop_code": NEXT_IF_NO_LAWFUL_SOURCE,
            "next_command_goal": None,
        }

    diagnostic = {
        "schema_version": "raw_delta_signature_candidate_approved_no_candidate_rows_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnostic_status": "OBSERVER_ONLY_DIAGNOSTIC_NOT_PATCH",
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_RECEIPT_ID,
        "source_policy_id": SOURCE_POLICY_ID,
        "source_policy_receipt_id": SOURCE_POLICY_RECEIPT_ID,
        "explicit_run_id": EXPLICIT_RUN_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "required_payload_fields": REQUIRED_PAYLOAD_FIELDS,
        "selected_files_total": len(selected_files),
        "files_read": files_read,
        "files_missing": files_missing,
        "objects_seen": objects_seen,
        "candidate_compatible_objects": candidate_compatible_objects,
        "depth_counts": dict(sorted(depth_counts.items())),
        "cycle_count_min": min(cycle_counts.values()) if cycle_counts else 0,
        "cycle_count_max": max(cycle_counts.values()) if cycle_counts else 0,
        "missing_pattern_counts": dict(missing_pattern_counts),
        "field_presence": field_presence_clean,
        "missing_all_objects": missing_all_objects,
        "present_some_objects": present_some_objects,
        "derivation_hint_counts": dict(derivation_hint_counts),
        "file_summaries_sample": file_summaries[:20],
        "file_summaries_total": len(file_summaries),
        "primary_class": primary_class,
        "interpretation": {
            "candidate_signature_payload_not_changed": True,
            "runtime_not_changed": True,
            "registry_not_read": True,
            "full_registry_not_scanned": True,
            "candidate_not_accepted": True,
            "diagnostic_only": True,
            "if_primary_class_is_derived_raw_compression_ratio_rule_required": (
                "Do not alias this blindly. The next layer must propose or authorize an observer-only derived metric rule "
                "for raw_compression_ratio_sig6 from lawful receipt fields."
            ),
        },
        "authority_guards": {
            "runner_executed": False,
            "candidate_rows_created": False,
            "candidate_accepted": False,
            "scale_mode_authorized": False,
            "registry_inserted": False,
            "registry_written": False,
            "registry_sqlite_read": False,
            "full_registry_scan_used": False,
            "runtime_semantic_changed": False,
            "runtime_code_changed": False,
            "runtime_receipt_emission_changed": False,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_inference_used": False,
            "case_id_or_cycle_n_identity_patch_used": False,
            "rowid_or_receipt_hash_truth_surface_used": False,
            "full_occurrence_key_in_signature_payload": False,
            "audit_or_debug_payload_in_signature_payload": False,
            "microhash_as_proof_used": False,
            "synthetic_fake_validation_rows_used": False,
            "transition_compression_probe_run": False,
        },
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    diagnostic_id = sha8({
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_receipt_id": SOURCE_RECEIPT_ID,
        "explicit_run_id": EXPLICIT_RUN_ID,
        "objects_seen": objects_seen,
        "candidate_compatible_objects": candidate_compatible_objects,
        "missing_pattern_counts": dict(missing_pattern_counts),
        "field_presence": field_presence_clean,
        "primary_class": primary_class,
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_no_candidate_rows_diagnostic_receipt_v0",
        "receipt_type": "NO_CANDIDATE_COMPATIBLE_ROWS_DIAGNOSTIC_RECEIPT",
        "diagnostic_id": diagnostic_id,
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnostic_status": diagnostic["diagnostic_status"],
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_RECEIPT_ID,
        "source_policy_id": SOURCE_POLICY_ID,
        "source_policy_receipt_id": SOURCE_POLICY_RECEIPT_ID,
        "explicit_run_id": EXPLICIT_RUN_ID,
        "selected_files_total": len(selected_files),
        "files_read": files_read,
        "files_missing": files_missing,
        "objects_seen": objects_seen,
        "candidate_compatible_objects": candidate_compatible_objects,
        "missing_pattern_counts": dict(missing_pattern_counts),
        "field_presence": field_presence_clean,
        "missing_all_objects": missing_all_objects,
        "present_some_objects": present_some_objects,
        "derivation_hint_counts": dict(derivation_hint_counts),
        "primary_class": primary_class,
        "terminal": terminal,
        "authority_guards": diagnostic["authority_guards"],
        "gate": diagnostic["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    if write_outputs:
        (OUT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True))
        (OUT_RECEIPT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return diagnostic, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface-id", default=SOURCE_SURFACE_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.surface_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_path=data/raw_delta_signature_candidate_approved_no_candidate_rows_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/raw_delta_signature_candidate_approved_no_candidate_rows_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
