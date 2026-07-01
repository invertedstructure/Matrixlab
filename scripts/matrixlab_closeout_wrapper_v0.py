#!/usr/bin/env python3
"""MatrixLab closeout wrapper v0.

Dry-run is the safe default path, but it still must be explicitly declared.
Execution mode exists behind --execute and is not used by this implementation
pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "matrixlabs_closeout_wrapper_v0"
ALLOWED_CLOSEOUT_COMMIT_MODES = {
    "ONE_COMMIT_LOCAL_READOUT",
    "TWO_COMMIT_CLOSEOUT",
}
TOP_LEVEL_STATUSES = [
    "CLOSEOUT_DRY_RUN_PASS",
    "CLOSEOUT_PASS_PUSHED_LOCAL_READOUT",
    "CLOSEOUT_PASS_TWO_COMMIT_PUSHED",
    "CLOSEOUT_PASS_LOCAL_COMMIT_ONLY",
    "CLOSEOUT_PASS_NOOP_ALREADY_CURRENT",
    "CLOSEOUT_LOCAL_COMMIT_ONLY_PUSH_FAIL",
    "CLOSEOUT_FAIL_PREFLIGHT",
    "CLOSEOUT_FAIL_SCOPE",
    "CLOSEOUT_FAIL_BASELINE_GENERATION",
    "CLOSEOUT_FAIL_BASELINE_PROJECTION",
    "CLOSEOUT_FAIL_FORBIDDEN_DRIFT",
    "CLOSEOUT_FAIL_COMMIT",
    "CLOSEOUT_FAIL_PUSH",
    "CLOSEOUT_FAIL_MODE",
]
STAGE_STATUSES = [
    "MANIFEST_PASS",
    "MODE_PASS",
    "PREFLIGHT_PASS",
    "SCOPE_PASS",
    "BASELINE_GENERATOR_PRESENT",
    "BASELINE_PROJECTION_PASS",
    "DIFF_SCOPE_PASS",
    "FORBIDDEN_DRIFT_PASS",
    "DRY_RUN_READOUT_EMIT_PASS",
    "BASELINE_GENERATION_PASS",
    "COMMIT_PASS",
    "PUSH_PASS",
    "READOUT_EMIT_PASS",
    "READOUT_COMMIT_PASS",
]
STOP_CODES = [
    "CLOSEOUT_STOP_MODE_NOT_DECLARED",
    "CLOSEOUT_STOP_MANIFEST_MISSING",
    "CLOSEOUT_STOP_MANIFEST_PARSE_FAIL",
    "CLOSEOUT_STOP_UNIT_ID_MISSING",
    "CLOSEOUT_STOP_ALLOWED_SCOPE_MISSING",
    "CLOSEOUT_STOP_FORBIDDEN_SCOPE_MISSING",
    "CLOSEOUT_STOP_COMMIT_MESSAGE_MISSING",
    "CLOSEOUT_STOP_UNKNOWN_COMMIT_MODE",
    "CLOSEOUT_STOP_NOT_GIT_REPO",
    "CLOSEOUT_STOP_BRANCH_UNKNOWN",
    "CLOSEOUT_STOP_REMOTE_UNKNOWN",
    "CLOSEOUT_STOP_STAGED_FILES_PRESENT",
    "CLOSEOUT_STOP_DIRTY_OUTSIDE_SCOPE",
    "CLOSEOUT_STOP_EXPECTED_ARTIFACT_MISSING",
    "CLOSEOUT_STOP_UNDECLARED_DIFF",
    "CLOSEOUT_STOP_FORBIDDEN_DRIFT",
    "CLOSEOUT_STOP_BASELINE_GENERATOR_MISSING",
    "CLOSEOUT_STOP_BASELINE_GENERATOR_FAIL",
    "CLOSEOUT_STOP_BASELINE_PROJECTION_MISSING_REQUIRED_FILE",
    "CLOSEOUT_STOP_COMMIT_FAIL",
    "CLOSEOUT_STOP_PUSH_FAIL",
]
REQUIRED_MANIFEST_FIELDS = [
    "schema_version",
    "unit_id",
    "closeout_commit_mode",
    "baseline_generator",
    "allowed_paths",
    "forbidden_paths",
    "ignored_untracked_paths",
    "expected_artifacts",
    "expected_baseline_projection_files",
    "primary_commit_message",
    "closeout_readout_commit_message",
    "nonclaims",
]


class CloseoutStop(RuntimeError):
    def __init__(self, stop_code: str, message: str = "") -> None:
        super().__init__(message or stop_code)
        self.stop_code = stop_code


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_git(root: Path, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_NOT_GIT_REPO", proc.stderr.strip() or proc.stdout.strip())
    return proc


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_NOT_GIT_REPO", proc.stderr.strip())
    return Path(proc.stdout.strip()).resolve()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def normalize_manifest_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def path_matches(path: str, scope: str) -> bool:
    path = normalize_manifest_path(path)
    scope = normalize_manifest_path(scope)
    if scope.endswith("/"):
        return path == scope[:-1] or path.startswith(scope)
    return path == scope or path.startswith(scope + "/")


def path_matches_any(path: str, scopes: list[str]) -> bool:
    return any(path_matches(path, scope) for scope in scopes)


def compact_scope_label(path: str, scopes: list[str]) -> str | None:
    for scope in scopes:
        if path_matches(path, scope):
            return scope
    return None


def sanitize_unit_id(unit_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", unit_id).strip("_")


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CloseoutStop("CLOSEOUT_STOP_MANIFEST_MISSING", str(path))
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CloseoutStop("CLOSEOUT_STOP_MANIFEST_PARSE_FAIL", str(exc)) from exc
    if not isinstance(manifest, dict):
        raise CloseoutStop("CLOSEOUT_STOP_MANIFEST_PARSE_FAIL", "manifest top-level is not an object")
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_MANIFEST_FIELDS if field not in manifest]
    if missing:
        stop = {
            "unit_id": "CLOSEOUT_STOP_UNIT_ID_MISSING",
            "allowed_paths": "CLOSEOUT_STOP_ALLOWED_SCOPE_MISSING",
            "forbidden_paths": "CLOSEOUT_STOP_FORBIDDEN_SCOPE_MISSING",
            "primary_commit_message": "CLOSEOUT_STOP_COMMIT_MESSAGE_MISSING",
            "closeout_readout_commit_message": "CLOSEOUT_STOP_COMMIT_MESSAGE_MISSING",
        }.get(missing[0], "CLOSEOUT_STOP_MANIFEST_PARSE_FAIL")
        raise CloseoutStop(stop, f"missing manifest field: {missing[0]}")
    if not manifest.get("unit_id"):
        raise CloseoutStop("CLOSEOUT_STOP_UNIT_ID_MISSING")
    if not manifest.get("allowed_paths"):
        raise CloseoutStop("CLOSEOUT_STOP_ALLOWED_SCOPE_MISSING")
    if not manifest.get("forbidden_paths"):
        raise CloseoutStop("CLOSEOUT_STOP_FORBIDDEN_SCOPE_MISSING")
    if manifest.get("closeout_commit_mode") not in ALLOWED_CLOSEOUT_COMMIT_MODES:
        raise CloseoutStop("CLOSEOUT_STOP_UNKNOWN_COMMIT_MODE", str(manifest.get("closeout_commit_mode")))
    for message_key in ["primary_commit_message", "closeout_readout_commit_message"]:
        message = manifest.get(message_key)
        if not isinstance(message, dict) or not message.get("subject"):
            raise CloseoutStop("CLOSEOUT_STOP_COMMIT_MESSAGE_MISSING", message_key)


def parse_status_line(line: str) -> dict[str, Any]:
    if len(line) < 4:
        raise CloseoutStop("CLOSEOUT_STOP_UNDECLARED_DIFF", f"ambiguous git status line: {line}")
    xy = line[:2]
    rest = line[3:]
    if " -> " in rest:
        before, after = rest.split(" -> ", 1)
        paths = [normalize_manifest_path(before), normalize_manifest_path(after)]
    else:
        paths = [normalize_manifest_path(rest)]
    staged = xy[0] not in (" ", "?")
    untracked = xy == "??"
    return {
        "raw": line,
        "xy": xy,
        "paths": paths,
        "primary_path": paths[-1],
        "staged": staged,
        "untracked": untracked,
    }


def git_status_entries(root: Path) -> list[dict[str, Any]]:
    proc = run_git(root, ["status", "--porcelain=v1", "-uall"], check=True)
    entries = []
    for line in proc.stdout.splitlines():
        if line.strip():
            entries.append(parse_status_line(line))
    return entries


def message_args(message: dict[str, Any]) -> list[str]:
    args = ["-m", str(message["subject"])]
    body = message.get("body") or []
    if isinstance(body, list):
        for paragraph in body:
            args.extend(["-m", str(paragraph)])
    return args


def readout_paths(unit_id: str, dry_run: bool, artifact_commit_sha: str | None = None) -> tuple[Path, Path]:
    safe = sanitize_unit_id(unit_id)
    base = Path("docs/matrixlabs/observability/closeouts")
    if dry_run:
        stem = f"closeout_{safe}_dry_run_v0"
    else:
        if not artifact_commit_sha:
            raise CloseoutStop("CLOSEOUT_STOP_COMMIT_FAIL", "execution readout requires artifact commit")
        stem = f"closeout_{safe}_{artifact_commit_sha[:8]}"
    return base / f"{stem}.json", base / f"{stem}.md"


def inspect_scope(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    entries = git_status_entries(root)
    allowed = [normalize_manifest_path(path) for path in manifest["allowed_paths"]]
    forbidden = [normalize_manifest_path(path) for path in manifest["forbidden_paths"]]
    ignored_scopes = [normalize_manifest_path(path) for path in manifest.get("ignored_untracked_paths", [])]
    ignored_seen: set[str] = set()
    changed: list[str] = []
    planned: list[str] = []
    unexpected: list[str] = []
    forbidden_hits: list[str] = []
    staged: list[str] = []

    for entry in entries:
        if entry["staged"]:
            staged.extend(entry["paths"])
        ignored_scope = None
        if entry["untracked"]:
            ignored_scope = compact_scope_label(entry["primary_path"], ignored_scopes)
        if ignored_scope:
            ignored_seen.add(ignored_scope)
            continue
        for path in entry["paths"]:
            changed.append(path)
            if path_matches_any(path, forbidden):
                forbidden_hits.append(path)
            if not path_matches_any(path, allowed):
                unexpected.append(path)
            else:
                planned.append(path)

    return {
        "entries": entries,
        "changed_files_detected": sorted(set(changed)),
        "changed_files_planned_for_commit": sorted(set(planned)),
        "ignored_untracked_paths": sorted(ignored_seen),
        "unexpected_dirty_files": sorted(set(unexpected)),
        "forbidden_drift_paths": sorted(set(forbidden_hits)),
        "staged_files": sorted(set(staged)),
    }


def verify_expected_paths(root: Path, paths: list[str], stop_code: str) -> None:
    missing = [path for path in paths if not (root / path).exists()]
    if missing:
        raise CloseoutStop(stop_code, ", ".join(missing))


def branch_and_remote(root: Path) -> tuple[str, str]:
    branch = run_git(root, ["branch", "--show-current"], check=True).stdout.strip()
    if not branch:
        raise CloseoutStop("CLOSEOUT_STOP_BRANCH_UNKNOWN")
    remote_proc = run_git(root, ["remote"], check=True)
    remotes = [line.strip() for line in remote_proc.stdout.splitlines() if line.strip()]
    if not remotes:
        raise CloseoutStop("CLOSEOUT_STOP_REMOTE_UNKNOWN")
    remote = "origin" if "origin" in remotes else remotes[0]
    return branch, remote


def build_readout(
    root: Path,
    manifest: dict[str, Any],
    dry_run: bool,
    scope: dict[str, Any],
    stage_statuses: list[str],
    closeout_status: str,
    stop_code: str | None = None,
    baseline_exit_code: int | None = None,
    artifact_commit_sha: str | None = None,
    closeout_readout_commit_sha: str | None = None,
) -> dict[str, Any]:
    branch, remote = branch_and_remote(root)
    head = run_git(root, ["rev-parse", "HEAD"], check=True).stdout.strip()
    generator_path = manifest["baseline_generator"]
    generator_abs = root / generator_path
    required_baseline = manifest.get("expected_baseline_projection_files", [])
    return {
        "schema_version": SCHEMA_VERSION,
        "unit_id": manifest["unit_id"],
        "closeout_commit_mode": manifest["closeout_commit_mode"],
        "closeout_status": closeout_status,
        "dry_run": dry_run,
        "generated_at_utc": utc_now(),
        "head_before": head,
        "artifact_commit_sha": artifact_commit_sha,
        "closeout_readout_commit_sha": closeout_readout_commit_sha,
        "branch": branch,
        "remote": remote,
        "baseline_share": {
            "generator_path": generator_path,
            "generator_sha256": sha256_file(generator_abs) if generator_abs.exists() else None,
            "exit_code": baseline_exit_code,
            "projection_checked": True,
            "required_files_present": all((root / path).exists() for path in required_baseline),
            "baseline_share_changed": None if dry_run else any(
                path_matches(path, "baseline_share/") for path in scope["changed_files_detected"]
            ),
            "baseline_share_change_reason": "not_run_in_dry_run" if dry_run else "baseline_generator_run_in_execute_mode",
        },
        "git": {
            "changed_files_detected": scope["changed_files_detected"],
            "changed_files_planned_for_commit": scope["changed_files_planned_for_commit"],
            "ignored_untracked_paths": scope["ignored_untracked_paths"],
            "unexpected_dirty_files": scope["unexpected_dirty_files"],
            "forbidden_drift_paths": scope["forbidden_drift_paths"],
            "primary_commit_created": artifact_commit_sha is not None,
            "artifact_commit_sha": artifact_commit_sha,
            "closeout_readout_commit_created": closeout_readout_commit_sha is not None,
            "push_attempted": False,
            "push_succeeded": False,
        },
        "scope": {
            "allowed_paths": manifest["allowed_paths"],
            "forbidden_paths": manifest["forbidden_paths"],
            "expected_artifacts": manifest["expected_artifacts"],
            "expected_baseline_projection_files": required_baseline,
        },
        "stage_statuses": stage_statuses,
        "stop_code": stop_code,
        "nonclaims": manifest.get("nonclaims", []),
        "terminal_result": {
            "type": "STOP_DRY_RUN_DONE" if dry_run else "STOP_EXECUTION_DONE",
            "next_boundary": "execution_requires_explicit_execute_flag" if dry_run else "closeout_complete",
        },
    }


def render_readout_md(readout: dict[str, Any]) -> str:
    git = readout["git"]
    parts = [
        "# MatrixLab Closeout Readout v0",
        "",
        f"- Unit: `{readout['unit_id']}`",
        f"- Status: `{readout['closeout_status']}`",
        f"- Dry run: `{str(readout['dry_run']).lower()}`",
        f"- Head before: `{readout['head_before']}`",
        f"- Branch: `{readout['branch']}`",
        f"- Remote: `{readout['remote']}`",
        "",
        "## Scope",
        "",
        f"- Changed files detected: `{len(git['changed_files_detected'])}`",
        f"- Planned files: `{len(git['changed_files_planned_for_commit'])}`",
        f"- Ignored untracked paths: `{', '.join(git['ignored_untracked_paths']) or 'none'}`",
        f"- Unexpected dirty files: `{', '.join(git['unexpected_dirty_files']) or 'none'}`",
        f"- Forbidden drift paths: `{', '.join(git['forbidden_drift_paths']) or 'none'}`",
        "",
        "## Stage Statuses",
        "",
        *[f"- `{status}`" for status in readout["stage_statuses"]],
        "",
        "## Nonclaims",
        "",
        *[f"- {claim}" for claim in readout.get("nonclaims", [])],
    ]
    return "\n".join(parts)


def write_readout(root: Path, rel_json: Path, rel_md: Path, readout: dict[str, Any]) -> None:
    json_path = root / rel_json
    md_path = root / rel_md
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(readout, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_readout_md(readout).rstrip() + "\n", encoding="utf-8")


def preflight(root: Path, manifest: dict[str, Any], dry_run: bool) -> tuple[dict[str, Any], list[str]]:
    validate_manifest(manifest)
    stage_statuses = ["MANIFEST_PASS", "MODE_PASS"]
    branch_and_remote(root)
    scope = inspect_scope(root, manifest)
    if scope["staged_files"]:
        raise CloseoutStop("CLOSEOUT_STOP_STAGED_FILES_PRESENT", ", ".join(scope["staged_files"]))
    verify_expected_paths(root, manifest["expected_artifacts"], "CLOSEOUT_STOP_EXPECTED_ARTIFACT_MISSING")
    stage_statuses.append("PREFLIGHT_PASS")
    if scope["unexpected_dirty_files"]:
        raise CloseoutStop("CLOSEOUT_STOP_DIRTY_OUTSIDE_SCOPE", ", ".join(scope["unexpected_dirty_files"]))
    if scope["forbidden_drift_paths"]:
        raise CloseoutStop("CLOSEOUT_STOP_FORBIDDEN_DRIFT", ", ".join(scope["forbidden_drift_paths"]))
    stage_statuses.extend(["SCOPE_PASS", "DIFF_SCOPE_PASS", "FORBIDDEN_DRIFT_PASS"])
    if not (root / manifest["baseline_generator"]).exists():
        raise CloseoutStop("CLOSEOUT_STOP_BASELINE_GENERATOR_MISSING", manifest["baseline_generator"])
    stage_statuses.append("BASELINE_GENERATOR_PRESENT")
    verify_expected_paths(
        root,
        manifest["expected_baseline_projection_files"],
        "CLOSEOUT_STOP_BASELINE_PROJECTION_MISSING_REQUIRED_FILE",
    )
    stage_statuses.append("BASELINE_PROJECTION_PASS")
    return scope, stage_statuses


def dry_run(root: Path, manifest: dict[str, Any]) -> int:
    scope, stage_statuses = preflight(root, manifest, dry_run=True)
    readout = build_readout(
        root=root,
        manifest=manifest,
        dry_run=True,
        scope=scope,
        stage_statuses=[*stage_statuses, "DRY_RUN_READOUT_EMIT_PASS"],
        closeout_status="CLOSEOUT_DRY_RUN_PASS",
    )
    rel_json, rel_md = readout_paths(manifest["unit_id"], dry_run=True)
    write_readout(root, rel_json, rel_md, readout)
    print(
        "closeout dry-run: "
        f"status={readout['closeout_status']} "
        f"changed={len(scope['changed_files_detected'])} "
        f"ignored={','.join(scope['ignored_untracked_paths']) or 'none'} "
        f"readout={rel_json.as_posix()}"
    )
    return 0


def run_baseline_generator(root: Path, manifest: dict[str, Any]) -> int:
    proc = subprocess.run(
        ["python3", manifest["baseline_generator"]],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_BASELINE_GENERATOR_FAIL", proc.stderr.strip() or proc.stdout.strip())
    return proc.returncode


def execute(root: Path, manifest: dict[str, Any]) -> int:
    scope, stage_statuses = preflight(root, manifest, dry_run=False)
    baseline_exit = run_baseline_generator(root, manifest)
    stage_statuses.append("BASELINE_GENERATION_PASS")
    scope = inspect_scope(root, manifest)
    if scope["staged_files"]:
        raise CloseoutStop("CLOSEOUT_STOP_STAGED_FILES_PRESENT", ", ".join(scope["staged_files"]))
    if scope["unexpected_dirty_files"]:
        raise CloseoutStop("CLOSEOUT_STOP_DIRTY_OUTSIDE_SCOPE", ", ".join(scope["unexpected_dirty_files"]))
    if scope["forbidden_drift_paths"]:
        raise CloseoutStop("CLOSEOUT_STOP_FORBIDDEN_DRIFT", ", ".join(scope["forbidden_drift_paths"]))
    planned = scope["changed_files_planned_for_commit"]
    if not planned:
        print("closeout execute: status=CLOSEOUT_PASS_NOOP_ALREADY_CURRENT")
        return 0
    add_proc = run_git(root, ["add", "--", *planned])
    if add_proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_COMMIT_FAIL", add_proc.stderr.strip())
    commit_proc = run_git(root, ["commit", *message_args(manifest["primary_commit_message"])])
    if commit_proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_COMMIT_FAIL", commit_proc.stderr.strip() or commit_proc.stdout.strip())
    artifact_commit = run_git(root, ["rev-parse", "HEAD"], check=True).stdout.strip()
    stage_statuses.append("COMMIT_PASS")
    remote = branch_and_remote(root)[1]
    push_proc = run_git(root, ["push", remote, "HEAD"])
    if push_proc.returncode != 0:
        raise CloseoutStop("CLOSEOUT_STOP_PUSH_FAIL", push_proc.stderr.strip() or push_proc.stdout.strip())
    stage_statuses.append("PUSH_PASS")
    rel_json, rel_md = readout_paths(manifest["unit_id"], dry_run=False, artifact_commit_sha=artifact_commit)
    readout = build_readout(
        root=root,
        manifest=manifest,
        dry_run=False,
        scope=scope,
        stage_statuses=[*stage_statuses, "READOUT_EMIT_PASS"],
        closeout_status="CLOSEOUT_PASS_PUSHED_LOCAL_READOUT",
        baseline_exit_code=baseline_exit,
        artifact_commit_sha=artifact_commit,
    )
    write_readout(root, rel_json, rel_md, readout)
    if manifest["closeout_commit_mode"] == "TWO_COMMIT_CLOSEOUT":
        add_readout = run_git(root, ["add", "--", rel_json.as_posix(), rel_md.as_posix()])
        if add_readout.returncode != 0:
            raise CloseoutStop("CLOSEOUT_STOP_COMMIT_FAIL", add_readout.stderr.strip())
        readout_commit = run_git(root, ["commit", *message_args(manifest["closeout_readout_commit_message"])])
        if readout_commit.returncode != 0:
            raise CloseoutStop("CLOSEOUT_STOP_COMMIT_FAIL", readout_commit.stderr.strip() or readout_commit.stdout.strip())
        closeout_commit = run_git(root, ["rev-parse", "HEAD"], check=True).stdout.strip()
        push_second = run_git(root, ["push", remote, "HEAD"])
        if push_second.returncode != 0:
            raise CloseoutStop("CLOSEOUT_STOP_PUSH_FAIL", push_second.stderr.strip() or push_second.stdout.strip())
        stage_statuses.append("READOUT_COMMIT_PASS")
        terminal_receipt = build_readout(
            root=root,
            manifest=manifest,
            dry_run=False,
            scope=inspect_scope(root, manifest),
            stage_statuses=stage_statuses,
            closeout_status="CLOSEOUT_PASS_TWO_COMMIT_PUSHED",
            baseline_exit_code=baseline_exit,
            artifact_commit_sha=artifact_commit,
            closeout_readout_commit_sha=closeout_commit,
        )
        print(
            "closeout execute: "
            f"status={terminal_receipt['closeout_status']} "
            f"artifact_commit={artifact_commit} "
            f"closeout_commit={closeout_commit}"
        )
    else:
        print(
            "closeout execute: "
            f"status={readout['closeout_status']} "
            f"artifact_commit={artifact_commit} "
            f"readout={rel_json.as_posix()}"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MatrixLab closeout wrapper v0")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)

    if args.dry_run and args.execute:
        print("CLOSEOUT_FAIL_MODE: choose exactly one of --dry-run or --execute", file=sys.stderr)
        return 2
    if not args.dry_run and not args.execute:
        print("CLOSEOUT_STOP_MODE_NOT_DECLARED", file=sys.stderr)
        return 2

    try:
        root = detect_repo_root(Path.cwd())
        manifest_path = root / args.manifest
        manifest = load_manifest(manifest_path)
        if args.dry_run:
            return dry_run(root, manifest)
        return execute(root, manifest)
    except CloseoutStop as exc:
        print(f"{exc.stop_code}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
