# Closeout Wrapper v0

## Purpose

M4 is the bounded preservation wrapper for MatrixLab units.

## Timing law

A closeout readout that records a commit SHA cannot honestly be committed in the same commit it describes. `ONE_COMMIT_LOCAL_READOUT` leaves the readout as a terminal/local receipt after the artifact commit is pushed. `TWO_COMMIT_CLOSEOUT` commits the declared artifact scope first, emits a readout that references that artifact commit, then commits the closeout readout in a second commit. The committed readout may leave its own containing commit SHA null; a terminal receipt may record the final closeout readout commit.

## Manifest-driven closeout

The wrapper is driven by a declared JSON manifest with unit id, closeout commit mode, baseline generator, allowed paths, forbidden paths, ignored untracked paths, expected artifacts, expected baseline projection files, commit messages, and nonclaims.

## Dry-run mode

Dry-run is the safe validation path. It must be explicitly selected with `--dry-run`; it never stages, commits, pushes, rewrites receipts, or runs runtime/probe/build/rerun commands. It inspects repo state, validates declared scope, checks expected artifacts and baseline projection files, and emits a dry-run closeout readout.

## Execution mode

Execution requires `--execute`. Execution may later regenerate baseline_share, stage only declared allowed scope, create the primary commit, push it, emit a closeout readout, and in `TWO_COMMIT_CLOSEOUT` commit and push that readout separately. This implementation pass does not run execution mode.

## Status vocabulary

- `CLOSEOUT_DRY_RUN_PASS`
- `CLOSEOUT_PASS_PUSHED_LOCAL_READOUT`
- `CLOSEOUT_PASS_TWO_COMMIT_PUSHED`
- `CLOSEOUT_PASS_LOCAL_COMMIT_ONLY`
- `CLOSEOUT_PASS_NOOP_ALREADY_CURRENT`
- `CLOSEOUT_LOCAL_COMMIT_ONLY_PUSH_FAIL`
- `CLOSEOUT_FAIL_PREFLIGHT`
- `CLOSEOUT_FAIL_SCOPE`
- `CLOSEOUT_FAIL_BASELINE_GENERATION`
- `CLOSEOUT_FAIL_BASELINE_PROJECTION`
- `CLOSEOUT_FAIL_FORBIDDEN_DRIFT`
- `CLOSEOUT_FAIL_COMMIT`
- `CLOSEOUT_FAIL_PUSH`
- `CLOSEOUT_FAIL_MODE`

## Stage statuses

- `MANIFEST_PASS`
- `MODE_PASS`
- `PREFLIGHT_PASS`
- `SCOPE_PASS`
- `BASELINE_GENERATOR_PRESENT`
- `BASELINE_PROJECTION_PASS`
- `DIFF_SCOPE_PASS`
- `FORBIDDEN_DRIFT_PASS`
- `DRY_RUN_READOUT_EMIT_PASS`
- `BASELINE_GENERATION_PASS`
- `COMMIT_PASS`
- `PUSH_PASS`
- `READOUT_EMIT_PASS`
- `READOUT_COMMIT_PASS`

## Stop codes

- `CLOSEOUT_STOP_MODE_NOT_DECLARED`
- `CLOSEOUT_STOP_MANIFEST_MISSING`
- `CLOSEOUT_STOP_MANIFEST_PARSE_FAIL`
- `CLOSEOUT_STOP_UNIT_ID_MISSING`
- `CLOSEOUT_STOP_ALLOWED_SCOPE_MISSING`
- `CLOSEOUT_STOP_FORBIDDEN_SCOPE_MISSING`
- `CLOSEOUT_STOP_COMMIT_MESSAGE_MISSING`
- `CLOSEOUT_STOP_UNKNOWN_COMMIT_MODE`
- `CLOSEOUT_STOP_NOT_GIT_REPO`
- `CLOSEOUT_STOP_BRANCH_UNKNOWN`
- `CLOSEOUT_STOP_REMOTE_UNKNOWN`
- `CLOSEOUT_STOP_STAGED_FILES_PRESENT`
- `CLOSEOUT_STOP_DIRTY_OUTSIDE_SCOPE`
- `CLOSEOUT_STOP_EXPECTED_ARTIFACT_MISSING`
- `CLOSEOUT_STOP_UNDECLARED_DIFF`
- `CLOSEOUT_STOP_FORBIDDEN_DRIFT`
- `CLOSEOUT_STOP_BASELINE_GENERATOR_MISSING`
- `CLOSEOUT_STOP_BASELINE_GENERATOR_FAIL`
- `CLOSEOUT_STOP_BASELINE_PROJECTION_MISSING_REQUIRED_FILE`
- `CLOSEOUT_STOP_COMMIT_FAIL`
- `CLOSEOUT_STOP_PUSH_FAIL`

## Non-claims

- closeout_wrapper_v0 does not decide the next milestone.
- closeout_wrapper_v0 does not validate theorem truth.
- closeout_wrapper_v0 does not validate runtime truth.
- closeout_wrapper_v0 does not validate receipt semantics.
- closeout_wrapper_v0 does not authorize future units.
- closeout_wrapper_v0 does not promote observed patterns.
- closeout_wrapper_v0 does not create runner authority.
- closeout_wrapper_v0 does not repair undeclared drift.
- closeout_wrapper_v0 only preserves the declared closeout surface into git, baseline_share, and closeout readouts.

## Relationship to M1-M3

M1 provides addressability. M2 provides evidence anchoring. M3 provides safe compression/decompression law. M4 preserves the completed bounded unit into git history, baseline_share, artifact paths, and closeout readouts.

## Relationship to M5-M7

M4 makes future observation loops cheap but does not choose or authorize them.
