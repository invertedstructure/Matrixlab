# Fill these explicitly, then rerun PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0.
# Do not use latest-file guessing, mtime selection, or preference collapse.

export SELECTED_TARGET_REF='exact/local/path.json'
export SELECTED_TARGET_KIND='runtime_patch_target'
export WHY_THIS_TARGET_IS_LOAD_BEARING='explain why this exact target is load-bearing'
export WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON='["explain why each non-selected bounded hint is not the target, or cite inventory rows"]'
export SOURCE_EVIDENCE_REFS_JSON='["exact/source/artifact.json"]'
export VERIFICATION_GATE_REF='exact/local/verification_gate.json'
export ROLLBACK_OR_STOP_BOUNDARY_REF='exact/local/rollback_or_stop_boundary.json'
