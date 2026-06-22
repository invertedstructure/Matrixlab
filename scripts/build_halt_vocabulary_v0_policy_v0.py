#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_HALT_VOCABULARY_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_HALT_VOCABULARY_V0_WITH_DEMO_RECORDS_V0"

TARGET_UNIT_ID = "halt_vocabulary.v0"

PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
PROCEED_ADAPTER_POLICY_ID = "e6b3dcfc"
PROCEED_ADAPTER_POLICY_RECEIPT_ID = "f953a9f0"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_ADAPTER_POLICY_PATH = ROOT / "data" / "proceed_adapter_v0_policies" / f"{PROCEED_ADAPTER_POLICY_ID}.json"
PROCEED_ADAPTER_POLICY_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_policy_receipts" / f"{PROCEED_ADAPTER_POLICY_ID}.json"
PROCEED_ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

OUT_DIR = ROOT / "data" / "halt_vocabulary_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "halt_vocabulary_v0_policy_receipts"

REQUIRED_HALT_ENTRY_FIELDS = [
    "halt_code",
    "halt_family",
    "smallest_honest_meaning",
    "must_not_impersonate",
    "allowed_next_handling",
]

HALT_RECORD_SCHEMA = {
    "schema_version": "halt_record_schema_v0",
    "required_fields": [
        "halt_record_id",
        "run_id",
        "unit_id",
        "step_index",
        "halt_code",
        "canonical_halt_code",
        "halt_family",
        "smallest_honest_meaning",
        "must_not_impersonate",
        "observed_pressure",
        "allowed_next_handling",
        "source_readout_ref",
        "source_trace_ref",
        "source_receipt_ref",
        "source_ledger_ref",
        "terminal_result",
    ],
    "terminal_law": {
        "halt_terminal_must_be_STOP": True,
        "stop_code_must_equal_canonical_halt_code": True,
        "advance_is_not_a_halt": True,
    },
}

HALT_FAMILIES = {
    "BASE_RUNNER": "Mechanical runner stop or shape failure.",
    "PROCEED_MODE": "Proceed adapter unit-control stop.",
    "AUTHORITY": "Stop caused by forbidden authority or undeclared input dependency.",
    "LAYERING": "Stop caused by collapsing object, layer, consumer, or authority roles.",
    "TAXONOMY_PRESSURE": "Stop caused by inadequate or missing typed vocabulary/move surface; record-only in v0.",
    "EXTRACTION_PRESSURE": "Stop caused by missing bounded extraction/dependency material.",
    "FRONTIER": "Stop caused by frontier material not encoded/promoted.",
    "RECEIPT_TRACE": "Stop caused by trace/receipt/readout disagreement.",
    "PROJECTION": "Stop caused by read-only projection/readout misreporting coherent underlying trace/receipt.",
    "GATE": "Stop caused by declared acceptance gate failure.",
}

HALT_VOCABULARY = {
    "INVALID_STATE": {
        "halt_code": "INVALID_STATE",
        "canonical_halt_code": "INVALID_STATE",
        "legacy_aliases": [],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["base_runner"],
        "smallest_honest_meaning": "The state does not satisfy required local shape or validity checks.",
        "must_not_impersonate": [
            "mathematical contradiction",
            "theorem failure",
            "invalidity of the whole runner",
        ],
        "allowed_next_handling": [
            "inspect state validation error",
            "repair fixture or state shape only if local",
            "otherwise stop for state-schema correction",
        ],
    },
    "INVALID_REGIME": {
        "halt_code": "INVALID_REGIME",
        "canonical_halt_code": "INVALID_REGIME",
        "legacy_aliases": [],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["base_runner", "local_regime"],
        "smallest_honest_meaning": "The declared regime is absent, malformed, or incompatible with the current unit.",
        "must_not_impersonate": [
            "proof failure",
            "runner impossibility",
            "permission to silently repair the regime",
        ],
        "allowed_next_handling": [
            "inspect regime schema mismatch",
            "restore declared regime artifact",
            "stop for regime correction if not local",
        ],
    },
    "FIXTURE_LOAD_ERROR": {
        "halt_code": "FIXTURE_LOAD_ERROR",
        "canonical_halt_code": "FIXTURE_LOAD_ERROR",
        "legacy_aliases": [],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["fixture"],
        "smallest_honest_meaning": "A declared fixture could not be loaded or parsed.",
        "must_not_impersonate": [
            "bad theorem",
            "invalid runner",
            "authority to infer a replacement fixture",
        ],
        "allowed_next_handling": [
            "repair fixture path or syntax",
            "redeclare fixture input",
            "halt until fixture is path-addressed",
        ],
    },
    "REGIME_MISMATCH": {
        "halt_code": "REGIME_MISMATCH",
        "canonical_halt_code": "REGIME_MISMATCH",
        "legacy_aliases": [],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["local_regime", "runner"],
        "smallest_honest_meaning": "The current unit and declared local regime do not agree on required version/hash/scope.",
        "must_not_impersonate": [
            "global regime invalidity",
            "permission to replace the regime",
            "proof failure",
        ],
        "allowed_next_handling": [
            "verify declared regime hash",
            "redeclare source surface",
            "halt for regime compatibility decision",
        ],
    },
    "STEP_LIMIT_EXCEEDED": {
        "halt_code": "STEP_LIMIT_EXCEEDED",
        "canonical_halt_code": "STEP_LIMIT_EXCEEDED",
        "legacy_aliases": [],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["base_runner"],
        "smallest_honest_meaning": "The runner hit the declared step limit before a clean terminal condition.",
        "must_not_impersonate": [
            "infinite loop proof",
            "theorem obstruction",
            "permission to continue without bound",
        ],
        "allowed_next_handling": [
            "inspect trace prefix",
            "lower or raise limit only by declared policy",
            "halt for bounded-run design if limit is structural",
        ],
    },
    "STOP_NO_APPLICABLE_MOVE": {
        "halt_code": "STOP_NO_APPLICABLE_MOVE",
        "canonical_halt_code": "STOP_NO_APPLICABLE_MOVE",
        "legacy_aliases": ["NO_APPLICABLE_MOVE"],
        "halt_family": "BASE_RUNNER",
        "source_layers_seen": ["jurisdiction_runner.v0.2", "proceed_adapter.v0"],
        "smallest_honest_meaning": "The state is valid enough to inspect, but no registered applicable move is available under the declared surface.",
        "must_not_impersonate": [
            "proof closure",
            "engine completion",
            "success",
            "permission to invent a move",
        ],
        "allowed_next_handling": [
            "check whether this is a unit boundary",
            "check whether the object is under-typed",
            "record missing-move pressure only if forced",
            "propose smallest missing move only in a later reviewed unit",
        ],
    },
    "STOP_DONE": {
        "halt_code": "STOP_DONE",
        "canonical_halt_code": "STOP_DONE",
        "legacy_aliases": [],
        "halt_family": "PROCEED_MODE",
        "source_layers_seen": ["proceed_adapter.v0", "jurisdiction_runner.v0.2.trace_ledger_hardened"],
        "smallest_honest_meaning": "The current bounded unit completed cleanly.",
        "must_not_impersonate": [
            "global completion",
            "proof closure",
            "permission to continue implicitly",
        ],
        "allowed_next_handling": [
            "freeze current artifact if useful",
            "declare next unit explicitly",
            "stop if no next objective is declared",
        ],
    },
    "STOP_NEXT_MOVE_BOUNDARY": {
        "halt_code": "STOP_NEXT_MOVE_BOUNDARY",
        "canonical_halt_code": "STOP_NEXT_MOVE_BOUNDARY",
        "legacy_aliases": [],
        "halt_family": "PROCEED_MODE",
        "source_layers_seen": ["proceed_adapter.v0"],
        "smallest_honest_meaning": "The current unit is complete, but the next action is a separate move or unit.",
        "must_not_impersonate": [
            "failure",
            "uncertainty",
            "blocked state",
            "proof closure",
        ],
        "allowed_next_handling": [
            "name the next unit explicitly",
            "freeze current readout if useful",
            "run proceed again only after the next unit is declared",
        ],
    },
    "STOP_VISIBLE_GOTCHA": {
        "halt_code": "STOP_VISIBLE_GOTCHA",
        "canonical_halt_code": "STOP_VISIBLE_GOTCHA",
        "legacy_aliases": [],
        "halt_family": "PROCEED_MODE",
        "source_layers_seen": ["proceed_adapter.v0"],
        "smallest_honest_meaning": "A visible local artifact/readout gotcha blocks honest continuation.",
        "must_not_impersonate": [
            "semantic failure",
            "authority to widen architecture",
            "proof obstruction",
        ],
        "allowed_next_handling": [
            "repair only if local and non-semantic",
            "record visible_gotchas_fixed",
            "halt if repair would touch source trace/receipt/ledger/runner/regime",
        ],
    },
    "STOP_PROJECTION_BUG": {
        "halt_code": "STOP_PROJECTION_BUG",
        "canonical_halt_code": "STOP_PROJECTION_BUG",
        "legacy_aliases": [],
        "halt_family": "PROJECTION",
        "source_layers_seen": ["proceed_adapter.v0", "readout_projection"],
        "smallest_honest_meaning": "The underlying state, trace, or receipt appears coherent, but the read-only projection misreports it.",
        "must_not_impersonate": [
            "bad runner logic",
            "theorem failure",
            "invalid state",
        ],
        "allowed_next_handling": [
            "fix projection calculation",
            "verify readout against trace",
            "rerun projection check",
        ],
    },
    "STOP_RECEIPT_MISMATCH": {
        "halt_code": "STOP_RECEIPT_MISMATCH",
        "canonical_halt_code": "STOP_RECEIPT_MISMATCH",
        "legacy_aliases": [],
        "halt_family": "RECEIPT_TRACE",
        "source_layers_seen": ["trace_ledger", "proceed_adapter.v0"],
        "smallest_honest_meaning": "The emitted receipt disagrees with the trace, final state, move list, proposal/ledger refs, or declared halt.",
        "must_not_impersonate": [
            "theorem failure",
            "frontier obstruction",
            "invalidity of the whole run",
        ],
        "allowed_next_handling": [
            "repair receipt construction",
            "inspect trace delta",
            "halt for verifier design if mismatch is not local",
        ],
    },
    "STOP_UNTYPED_UNIT": {
        "halt_code": "STOP_UNTYPED_UNIT",
        "canonical_halt_code": "STOP_UNTYPED_UNIT",
        "legacy_aliases": [],
        "halt_family": "PROCEED_MODE",
        "source_layers_seen": ["proceed_adapter.v0"],
        "smallest_honest_meaning": "The selected unit lacks required proceed-unit typing.",
        "must_not_impersonate": [
            "bad runner",
            "missing theorem",
            "permission to infer unit semantics",
        ],
        "allowed_next_handling": [
            "type the unit before movement",
            "declare unit scope and inputs",
            "halt until unit schema is satisfied",
        ],
    },
    "STOP_UNDERTYPED_OBJECT": {
        "halt_code": "STOP_UNDERTYPED_OBJECT",
        "canonical_halt_code": "STOP_UNDERTYPED_OBJECT",
        "legacy_aliases": [],
        "halt_family": "TAXONOMY_PRESSURE",
        "source_layers_seen": ["proceed_adapter.v0", "typed_labeling"],
        "smallest_honest_meaning": "A blocking object lacks enough type information to move honestly.",
        "must_not_impersonate": [
            "permission to guess object kind",
            "proof of new taxonomy",
            "authority to promote labels",
        ],
        "allowed_next_handling": [
            "label, withhold, split, or factor object",
            "record taxonomy pressure if current vocabulary cannot classify it",
            "do not promote new label without review",
        ],
    },
    "STOP_TAXONOMY_GAP": {
        "halt_code": "STOP_TAXONOMY_GAP",
        "canonical_halt_code": "STOP_TAXONOMY_GAP",
        "legacy_aliases": [],
        "halt_family": "TAXONOMY_PRESSURE",
        "source_layers_seen": ["proceed_adapter.v0"],
        "smallest_honest_meaning": "The system encountered a real stop shape that existing labels or halt terms cannot honestly classify.",
        "must_not_impersonate": [
            "permission to invent broad taxonomy",
            "proof of a new object",
            "automatic vocabulary expansion",
        ],
        "allowed_next_handling": [
            "invoke taxonomy upgrade rule later",
            "test existing vocabulary first",
            "propose smallest honest delta only if needed",
        ],
    },
    "STOP_NEEDS_NEW_MOVE": {
        "halt_code": "STOP_NEEDS_NEW_MOVE",
        "canonical_halt_code": "STOP_NEEDS_NEW_MOVE",
        "legacy_aliases": [],
        "halt_family": "TAXONOMY_PRESSURE",
        "source_layers_seen": ["proceed_adapter.v0", "move_registry"],
        "smallest_honest_meaning": "Continuation requires a lawful move not currently present in the move registry.",
        "must_not_impersonate": [
            "permission to add a large subsystem",
            "permission to self-authorize",
            "proof that the missing move is valid",
        ],
        "allowed_next_handling": [
            "draft smallest missing move",
            "include applies_when, action, emitted readout, and halt behavior",
            "submit for review before registry acceptance",
        ],
    },
    "STOP_NEEDS_EXTRACTION": {
        "halt_code": "STOP_NEEDS_EXTRACTION",
        "canonical_halt_code": "STOP_NEEDS_EXTRACTION",
        "legacy_aliases": [],
        "halt_family": "EXTRACTION_PRESSURE",
        "source_layers_seen": ["extraction", "proceed_adapter.v0"],
        "smallest_honest_meaning": "The next lawful step requires bounded extraction material not currently available as declared input.",
        "must_not_impersonate": [
            "authority violation by itself",
            "frontier impossibility",
            "permission to infer missing material",
        ],
        "allowed_next_handling": [
            "run bounded extraction pass",
            "declare extraction input/output surface",
            "stop if extraction would require undeclared authority",
        ],
    },
    "STOP_DEPENDENCY_MISSING": {
        "halt_code": "STOP_DEPENDENCY_MISSING",
        "canonical_halt_code": "STOP_DEPENDENCY_MISSING",
        "legacy_aliases": [],
        "halt_family": "EXTRACTION_PRESSURE",
        "source_layers_seen": ["mlblock", "proceed_adapter.v0", "jurisdiction_runner"],
        "smallest_honest_meaning": "A declared required artifact or input was unavailable at its path-addressed location.",
        "must_not_impersonate": [
            "authority violation",
            "proof failure",
            "missing theory",
        ],
        "allowed_next_handling": [
            "restore declared artifact",
            "redeclare allowed input",
            "stop until dependency is path-addressed",
        ],
    },
    "STOP_AUTHORITY_VIOLATION": {
        "halt_code": "STOP_AUTHORITY_VIOLATION",
        "canonical_halt_code": "STOP_AUTHORITY_VIOLATION",
        "legacy_aliases": [],
        "halt_family": "AUTHORITY",
        "source_layers_seen": ["proceed_adapter.v0", "jurisdiction_runner"],
        "smallest_honest_meaning": "The next step would depend on memory, intent, latest files, ambient workspace state, UI state, or unregistered source material.",
        "must_not_impersonate": [
            "ordinary uncertainty",
            "local gotcha",
            "missing implementation",
        ],
        "allowed_next_handling": [
            "return to declared source surface",
            "use pointer or fixture discipline",
            "redeclare allowed inputs",
        ],
    },
    "STOP_LAYER_COLLAPSE": {
        "halt_code": "STOP_LAYER_COLLAPSE",
        "canonical_halt_code": "STOP_LAYER_COLLAPSE",
        "legacy_aliases": [],
        "halt_family": "LAYERING",
        "source_layers_seen": ["typed_labeling", "proceed_adapter.v0"],
        "smallest_honest_meaning": "The step is mixing theorem, interface, outer engine, shell, receipt, authority, or frontier roles.",
        "must_not_impersonate": [
            "useful compression",
            "valid bridge",
            "theorem-side result",
        ],
        "allowed_next_handling": [
            "split object by layer",
            "factor unit by layer",
            "retry only after layer boundary is explicit",
        ],
    },
    "STOP_GATE_FAIL": {
        "halt_code": "STOP_GATE_FAIL",
        "canonical_halt_code": "STOP_GATE_FAIL",
        "legacy_aliases": [],
        "halt_family": "GATE",
        "source_layers_seen": ["proceed_adapter.v0", "mlblock"],
        "smallest_honest_meaning": "A declared acceptance gate failed.",
        "must_not_impersonate": [
            "global falsification",
            "proof failure",
            "permission to continue anyway",
        ],
        "allowed_next_handling": [
            "report exact gate and evidence",
            "repair smallest local cause if allowed",
            "fork or halt if gate failure is semantic",
        ],
    },
    "STOP_FRONTIER": {
        "halt_code": "STOP_FRONTIER",
        "canonical_halt_code": "STOP_FRONTIER",
        "legacy_aliases": [],
        "halt_family": "FRONTIER",
        "source_layers_seen": ["frontier"],
        "smallest_honest_meaning": "The next step would require frontier material not yet promoted or encoded.",
        "must_not_impersonate": [
            "implementation blockage",
            "failure of the runner",
            "proof that the frontier claim is false",
        ],
        "allowed_next_handling": [
            "stop build movement",
            "return to exploration, compression, or certification of frontier burden",
            "do not encode as settled move",
        ],
    },
}

HALT_CLASSIFIER_PRIORITY = {
    "schema_version": "halt_classifier_priority_v0",
    "classifier_id": "halt_classifier.priority.v0",
    "mode": "deterministic_priority_table_not_smart_classifier",
    "priority_order": [
        "INVALID_STATE",
        "INVALID_REGIME",
        "STOP_AUTHORITY_VIOLATION",
        "STOP_LAYER_COLLAPSE",
        "STOP_RECEIPT_MISMATCH",
        "STOP_PROJECTION_BUG",
        "STOP_GATE_FAIL",
        "STOP_UNTYPED_UNIT",
        "STOP_UNDERTYPED_OBJECT",
        "STOP_NEEDS_EXTRACTION",
        "STOP_DEPENDENCY_MISSING",
        "STOP_NEEDS_NEW_MOVE",
        "STOP_TAXONOMY_GAP",
        "STOP_FRONTIER",
        "STOP_NO_APPLICABLE_MOVE",
        "STOP_NEXT_MOVE_BOUNDARY",
        "STOP_DONE",
    ],
    "law": {
        "authority_and_layering_stop_before_local_repair": True,
        "receipt_trace_mismatch_checked_before_projection_repair": True,
        "no_applicable_move_must_not_impersonate_closure": True,
        "advance_next_unit_id_is_not_a_halt": True,
    },
}

HALT_TO_NEXT_HANDLING_TABLE = {
    "schema_version": "halt_to_next_handling_table_v0",
    "routes": {code: entry["allowed_next_handling"] for code, entry in HALT_VOCABULARY.items()},
}

RUNNER_RECEIPT_HALT_PATCH = {
    "schema_version": "runner_receipt_halt_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_receipts",
    "add_field": {
        "halt": {
            "halt_code": "<canonical_halt_code>",
            "halt_record_ref": "<path-addressed halt record ref>",
            "halt_family": "<halt_family>",
        }
    },
}

PROCEED_READOUT_HALT_PATCH = {
    "schema_version": "proceed_readout_halt_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_readouts",
    "terminal_result_extension": {
        "type": "STOP",
        "stop_code": "<canonical_halt_code>",
        "halt_record_ref": "<path-addressed halt record ref>",
    },
}

TRACE_ENTRY_HALT_PATCH = {
    "schema_version": "trace_entry_halt_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_traces",
    "add_fields": {
        "halt_code": "<canonical_halt_code>",
        "halt_record_ref": "<path-addressed halt record ref>",
    },
}

DAY3_DEMO_HALT_RECORD_PLAN = {
    "schema_version": "day3_demo_halt_record_plan_v0",
    "demo_cases": {
        "DEMO_CLEAN_NEXT_BOUNDARY": {
            "halt_code": "STOP_NEXT_MOVE_BOUNDARY",
            "meaning_check": "not failure; current unit complete; declare next unit",
        },
        "DEMO_PROJECTION_BUG": {
            "halt_code": "STOP_PROJECTION_BUG",
            "meaning_check": "state/trace may be coherent; projection misreported it",
        },
        "DEMO_NO_APPLICABLE_MOVE": {
            "halt_code": "STOP_NO_APPLICABLE_MOVE",
            "legacy_aliases_tested": ["NO_APPLICABLE_MOVE"],
            "meaning_check": "valid state has no registered applicable move; not proof closure",
        },
        "DEMO_TAXONOMY_GAP": {
            "halt_code": "STOP_TAXONOMY_GAP",
            "taxonomy_pressure_status": "RECORDED_ONLY",
            "meaning_check": "dictionary failed honestly; no runtime vocabulary promotion",
        },
    },
}

ACCEPTANCE_GATES = {
    "HVP0_source_surface_verified": {
        "required": True,
        "description": "Proceed adapter implementation and hardened trace-ledger runner surface are tracked and path-addressed.",
    },
    "HVP1_vocabulary_entries_have_four_field_rule": {
        "required": True,
        "description": "Every halt entry has halt_code, smallest_honest_meaning, must_not_impersonate, and allowed_next_handling.",
    },
    "HVP2_halt_record_schema_declared": {
        "required": True,
        "description": "halt_record_schema_v0 declares receipt-compatible halt record fields and source refs.",
    },
    "HVP3_classifier_priority_declared": {
        "required": True,
        "description": "halt_classifier_priority_v0 is deterministic and not a smart classifier.",
    },
    "HVP4_next_handling_table_declared": {
        "required": True,
        "description": "Every halt routes to lawful next handling.",
    },
    "HVP5_alias_and_no_applicable_move_discipline": {
        "required": True,
        "description": "STOP_NO_APPLICABLE_MOVE is canonical; NO_APPLICABLE_MOVE is legacy alias only; it must not impersonate proof closure.",
    },
    "HVP6_patch_artifacts_only_no_source_mutation": {
        "required": True,
        "description": "Runner/readout/trace halt patches are future-schema patches only; existing artifacts are not mutated.",
    },
    "HVP7_taxonomy_record_only": {
        "required": True,
        "description": "STOP_TAXONOMY_GAP records pressure only and cannot accept/promote taxonomy delta.",
    },
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "halt_vocabulary": "data/halt_vocabulary_v0/halt_vocabulary_v0.json",
    "halt_record_schema": "data/halt_record_schemas/halt_record_schema_v0.json",
    "halt_family_table": "data/halt_family_tables/halt_family_table_v0.json",
    "halt_classifier_priority": "data/halt_classifier_priorities/halt_classifier_priority_v0.json",
    "halt_to_next_handling_table": "data/halt_to_next_handling_tables/halt_to_next_handling_table_v0.json",
    "runner_receipt_halt_patch": "data/halt_schema_patches/runner_receipt_halt_patch_v0.json",
    "proceed_readout_halt_patch": "data/halt_schema_patches/proceed_readout_halt_patch_v0.json",
    "trace_entry_halt_patch": "data/halt_schema_patches/trace_entry_halt_patch_v0.json",
    "day3_demo_halt_record_plan": "data/halt_vocabulary_v0_demo/day3_demo_halt_record_plan_v0.json",
    "day3_demo_halt_records": "data/halt_vocabulary_v0_demo/day3_demo_halt_records.jsonl",
    "day3_demo_halt_receipts": "data/halt_vocabulary_v0_demo/day3_demo_halt_receipts.json",
    "implementation_receipt": "data/halt_vocabulary_v0_implementation_receipts/<receipt_id>.json",
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def validate_vocabulary(vocab: Dict[str, Dict[str, Any]]) -> List[str]:
    failures: List[str] = []

    if "TYPED_STATE_READY" in vocab:
        failures.append("TYPED_STATE_READY_must_not_be_halt")

    if "STOP_NO_APPLICABLE_MOVE" not in vocab:
        failures.append("STOP_NO_APPLICABLE_MOVE_missing")
    else:
        entry = vocab["STOP_NO_APPLICABLE_MOVE"]
        if "NO_APPLICABLE_MOVE" not in entry.get("legacy_aliases", []):
            failures.append("NO_APPLICABLE_MOVE_alias_missing")
        if not any("proof closure" in x for x in entry.get("must_not_impersonate", [])):
            failures.append("STOP_NO_APPLICABLE_MOVE_missing_proof_closure_anti_impersonation")

    if "NO_APPLICABLE_MOVE" in vocab:
        failures.append("NO_APPLICABLE_MOVE_must_not_be_canonical_entry")

    if "STOP_DEPENDENCY_MISSING" not in vocab:
        failures.append("STOP_DEPENDENCY_MISSING_missing")

    for code, entry in vocab.items():
        for field in REQUIRED_HALT_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"{code}:required_field_missing:{field}")
        if entry.get("halt_code") != code:
            failures.append(f"{code}:halt_code_mismatch:{entry.get('halt_code')}")
        if not entry.get("smallest_honest_meaning"):
            failures.append(f"{code}:empty_smallest_honest_meaning")
        if not isinstance(entry.get("must_not_impersonate"), list) or not entry.get("must_not_impersonate"):
            failures.append(f"{code}:must_not_impersonate_missing_or_empty")
        if not isinstance(entry.get("allowed_next_handling"), list) or not entry.get("allowed_next_handling"):
            failures.append(f"{code}:allowed_next_handling_missing_or_empty")
        if entry.get("halt_family") not in HALT_FAMILIES:
            failures.append(f"{code}:unknown_halt_family:{entry.get('halt_family')}")
        if entry.get("canonical_halt_code") != code:
            failures.append(f"{code}:canonical_halt_code_mismatch:{entry.get('canonical_halt_code')}")
        if "proof" not in " ".join(entry.get("must_not_impersonate", [])).lower() and code in ["STOP_DONE", "STOP_NEXT_MOVE_BOUNDARY", "STOP_NO_APPLICABLE_MOVE", "STOP_GATE_FAIL", "STOP_FRONTIER"]:
            failures.append(f"{code}:key_halt_missing_proof_anti_impersonation")

    return failures

def validate_inputs(
    proceed_receipt: Dict[str, Any],
    proceed_policy: Dict[str, Any],
    proceed_policy_receipt: Dict[str, Any],
    trace_ledger_receipt: Dict[str, Any],
    trace_schema: Dict[str, Any],
    ledger_schema: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if proceed_receipt.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"proceed_receipt_id_wrong:{proceed_receipt.get('receipt_id')}")
    if proceed_receipt.get("gate") != "PASS":
        failures.append(f"proceed_gate_not_PASS:{proceed_receipt.get('gate')}")
    if proceed_receipt.get("target_adapter_unit_id") != "proceed_adapter.v0":
        failures.append(f"proceed_target_adapter_wrong:{proceed_receipt.get('target_adapter_unit_id')}")
    if proceed_receipt.get("source_runner_unit_id") != "jurisdiction_runner.v0.2.trace_ledger_hardened":
        failures.append(f"proceed_source_runner_wrong:{proceed_receipt.get('source_runner_unit_id')}")
    if proceed_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"proceed_terminal_not_STOP:{proceed_receipt.get('terminal')}")
    if proceed_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"proceed_terminal_stop_not_DONE:{proceed_receipt.get('terminal')}")
    if proceed_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"proceed_terminal_next_not_null:{proceed_receipt.get('terminal')}")

    p_gates = proceed_receipt.get("acceptance_gate_results") or {}
    for gate in [
        "P0_source_surface_verified",
        "P1_proceed_contract_declared",
        "P2_unit_schema_and_registry_declared",
        "P3_selector_declared",
        "P4_readout_and_authority_schemas_declared",
        "P5_demo_implementation_required",
        "P6_no_source_runner_or_regime_mutation",
    ]:
        if p_gates.get(gate) is not True:
            failures.append(f"proceed_gate_not_true:{gate}:{p_gates.get(gate)}")

    metrics = proceed_receipt.get("aggregate_metrics") or {}
    if metrics.get("demo_case_count") != 6:
        failures.append(f"proceed_demo_case_count_wrong:{metrics.get('demo_case_count')}")
    if metrics.get("demo_case_pass_count") != 6:
        failures.append(f"proceed_demo_case_pass_count_wrong:{metrics.get('demo_case_pass_count')}")
    for key in [
        "hidden_continuation_count",
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "proposal_executed_count",
        "proposal_promoted_count",
        "registry_write_count",
        "registry_sqlite_write_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"proceed_metric_not_zero:{key}:{metrics.get(key)}")

    if proceed_policy.get("policy_id") != PROCEED_ADAPTER_POLICY_ID:
        failures.append(f"proceed_policy_id_wrong:{proceed_policy.get('policy_id')}")
    if proceed_policy_receipt.get("receipt_id") != PROCEED_ADAPTER_POLICY_RECEIPT_ID:
        failures.append(f"proceed_policy_receipt_id_wrong:{proceed_policy_receipt.get('receipt_id')}")

    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"trace_ledger_receipt_id_wrong:{trace_ledger_receipt.get('receipt_id')}")
    if trace_ledger_receipt.get("gate") != "PASS":
        failures.append(f"trace_ledger_gate_not_PASS:{trace_ledger_receipt.get('gate')}")
    if trace_ledger_receipt.get("trace_schema_id") != TRACE_SCHEMA_ID:
        failures.append(f"trace_ledger_trace_schema_wrong:{trace_ledger_receipt.get('trace_schema_id')}")
    if trace_ledger_receipt.get("proposal_ledger_schema_id") != PROPOSAL_LEDGER_SCHEMA_ID:
        failures.append(f"trace_ledger_ledger_schema_wrong:{trace_ledger_receipt.get('proposal_ledger_schema_id')}")

    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append(f"trace_schema_version_wrong:{trace_schema.get('schema_version')}")
    if ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"ledger_schema_version_wrong:{ledger_schema.get('schema_version')}")

    if local_regime_v1.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")
    if local_regime_v1.get("local_regime_version") != "local_regime.v1":
        failures.append(f"local_regime_v1_version_wrong:{local_regime_v1.get('local_regime_version')}")

    for path, label in [
        (PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_PATH, "proceed_adapter_implementation_receipt"),
        (PROCEED_ADAPTER_POLICY_PATH, "proceed_adapter_policy"),
        (PROCEED_ADAPTER_POLICY_RECEIPT_PATH, "proceed_adapter_policy_receipt"),
        (PROCEED_ADAPTER_MODULE_PATH, "proceed_adapter_module"),
        (TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH, "trace_ledger_implementation_receipt"),
        (TRACE_SCHEMA_PATH, "trace_schema"),
        (PROPOSAL_LEDGER_SCHEMA_PATH, "proposal_ledger_schema"),
        (TRACE_LEDGER_RUNNER_PATH, "trace_ledger_runner"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    proceed_receipt = read_json(PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_PATH)
    proceed_policy = read_json(PROCEED_ADAPTER_POLICY_PATH)
    proceed_policy_receipt = read_json(PROCEED_ADAPTER_POLICY_RECEIPT_PATH)
    trace_ledger_receipt = read_json(TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)

    failures = []
    failures.extend(validate_inputs(
        proceed_receipt,
        proceed_policy,
        proceed_policy_receipt,
        trace_ledger_receipt,
        trace_schema,
        ledger_schema,
        local_regime_v1,
    ))
    failures.extend(validate_vocabulary(HALT_VOCABULARY))

    family_table = {
        "schema_version": "halt_family_table_v0",
        "families": HALT_FAMILIES,
        "mapping": {code: entry["halt_family"] for code, entry in HALT_VOCABULARY.items()},
    }

    policy_seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proceed_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "vocab_hash": sha8(HALT_VOCABULARY),
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "halt_vocabulary_policy_built": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_records_emitted_by_policy": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_jurisdiction_runner_v0_2_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "new_move_added": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "halt_as_truth_claimed": False,
        "halt_as_proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "halt_vocabulary_v0_policy_v0",
        "policy_type": "HALT_VOCABULARY_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_policy_id": PROCEED_ADAPTER_POLICY_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Make every terminal stop typed, auditable, anti-impersonating, and next-handling-aware.",
            "core_law": "A halt is not failure by default, not proof by default, and not truth by default; it is typed control information.",
            "four_field_rule": REQUIRED_HALT_ENTRY_FIELDS,
            "non_goal": "no taxonomy evolution, no automatic move addition, no proof claim, no mutation of source artifacts",
        },
        "halt_vocabulary": {
            "schema_version": "halt_vocabulary_v0",
            "vocabulary_id": sha8(HALT_VOCABULARY),
            "canonical_entry_count": len(HALT_VOCABULARY),
            "entries": HALT_VOCABULARY,
            "alias_policy": {
                "canonical_stop_no_applicable_move": "STOP_NO_APPLICABLE_MOVE",
                "legacy_aliases": {"NO_APPLICABLE_MOVE": "STOP_NO_APPLICABLE_MOVE"},
                "typed_state_ready_is_status_not_halt": True,
            },
        },
        "halt_record_schema": HALT_RECORD_SCHEMA,
        "halt_family_table": family_table,
        "halt_classifier_priority": HALT_CLASSIFIER_PRIORITY,
        "halt_to_next_handling_table": HALT_TO_NEXT_HANDLING_TABLE,
        "runner_receipt_halt_patch": RUNNER_RECEIPT_HALT_PATCH,
        "proceed_readout_halt_patch": PROCEED_READOUT_HALT_PATCH,
        "trace_entry_halt_patch": TRACE_ENTRY_HALT_PATCH,
        "day3_demo_halt_record_plan": DAY3_DEMO_HALT_RECORD_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_halt_vocabulary_policy": True,
            "read_halt_vocabulary_policy_receipt": True,
            "write_halt_vocabulary_artifact": True,
            "write_halt_record_schema_artifact": True,
            "write_halt_family_table_artifact": True,
            "write_halt_classifier_priority_artifact": True,
            "write_halt_to_next_handling_table_artifact": True,
            "write_runner_receipt_halt_patch_artifact": True,
            "write_proceed_readout_halt_patch_artifact": True,
            "write_trace_entry_halt_patch_artifact": True,
            "write_day3_demo_halt_record_plan_artifact": True,
            "emit_day3_demo_halt_records": True,
            "emit_day3_demo_halt_receipts": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "mutate_existing_runner_receipts": True,
            "mutate_existing_proceed_readouts": True,
            "mutate_existing_trace_files": True,
            "mutate_existing_ledger_files": True,
            "modify_proceed_adapter_module": True,
            "modify_trace_ledger_runner_module": True,
            "modify_local_regime_v1": True,
            "accept_taxonomy_delta": True,
            "promote_taxonomy_delta": True,
            "add_new_move_automatically": True,
            "execute_or_apply_proposal": True,
            "promote_proposal_without_human_review": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "global_taxonomy_design": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "halt_as_truth_claim": True,
            "halt_as_proof_claim": True,
            "hidden_continuation_after_terminal": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_records": True,
            "does_not_mutate_existing_artifacts": True,
            "does_not_modify_source_modules": True,
            "does_not_modify_source_regime": True,
            "does_not_accept_or_promote_taxonomy_delta": True,
            "does_not_add_new_moves": True,
            "does_not_apply_or_promote_proposal": True,
            "does_not_write_registry": True,
            "does_not_claim_global_correctness": True,
            "does_not_claim_final_taxonomy": True,
            "does_not_claim_theorem_closure": True,
            "next_unit_required_for_implementation": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proceed_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "halt_vocabulary_v0_policy_receipt_v0",
        "receipt_type": "HALT_VOCABULARY_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_policy_id": PROCEED_ADAPTER_POLICY_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "halt_vocabulary": policy["halt_vocabulary"],
        "halt_record_schema": policy["halt_record_schema"],
        "halt_family_table": policy["halt_family_table"],
        "halt_classifier_priority": policy["halt_classifier_priority"],
        "halt_to_next_handling_table": policy["halt_to_next_handling_table"],
        "runner_receipt_halt_patch": policy["runner_receipt_halt_patch"],
        "proceed_readout_halt_patch": policy["proceed_readout_halt_patch"],
        "trace_entry_halt_patch": policy["trace_entry_halt_patch"],
        "day3_demo_halt_record_plan": policy["day3_demo_halt_record_plan"],
        "required_implementation_artifacts": policy["required_implementation_artifacts"],
        "acceptance_gates": policy["acceptance_gates"],
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{policy_id}.json", policy)
        write_json(OUT_RECEIPT_DIR / f"{policy_id}.json", receipt)

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"halt_vocabulary_policy_id={policy['policy_id']}")
    print(f"halt_vocabulary_policy_receipt_id={receipt['receipt_id']}")
    print(f"halt_vocabulary_policy_path=data/halt_vocabulary_v0_policies/{policy['policy_id']}.json")
    print(f"halt_vocabulary_policy_receipt_path=data/halt_vocabulary_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
