# phase_vs2_controlled_step_binding_manifest_v0

- Artifact identity: `phase_vs2_controlled_step_binding_manifest_v0`
- Artifact kind: `STATIC_SUCCESSOR_BINDING_MANIFEST`
- Version: `v0`
- Status: `CONTROLLED_STEP_AND_CONVERGENCE_FROZEN_RUNTIME_PACKAGE_PENDING`
- Canonicalization: `MATRIXLAB_CANONICAL_JSON_V0`
- Canonical SHA-256: `ffb10d40f6dbf641879a3385ba312f80b9a1f9d667b230e49452ad48abce1e43`

## Upstream Bindings

- `predecessor_move_space_manifest_reference`: `BOUND` `phase_vs2_move_space_binding_manifest_v0`
- `controlled_step_package_reference`: `BOUND` `phase_vs2_controlled_step_and_convergence_contract_package_v0`
- `receipt_and_atomic_publication_contract_reference`: `BOUND` `phase_vs2_receipt_and_atomic_publication_contract_v0`
- `convergence_criterion_contract_reference`: `BOUND` `phase_vs2_convergence_criterion_contract_v0`
- `fixture_set_reference`: `PENDING` `None`
- `exact_source_snapshot_reference`: `PENDING` `None`
- `exact_step_and_move_budget_reference`: `PENDING` `None`
- `pressure_readout_contract_reference`: `PENDING` `None`
- `evidence_yield_report_contract_reference`: `PENDING` `None`
- `construction_readiness_gate_reference`: `PENDING` `None`
- `active_execution_authority_reference`: `ABSENT_BY_POLICY` `None`
- `active_sweep_authority_reference`: `ABSENT_BY_POLICY` `None`

## Construction-Frame Posture

- Bounded construction consumption count after VS2.5: `1`
- Construction frame open after VS2.5: `False`

## Component Summary

- No embedded component registry in this standalone contract.

## Authority Posture

- Active execution authority present: `False`
- Active sweep authority present: `False`

## Runtime Posture

- Runtime instance created: `False`
- Candidate instance created: `False`
- Move selected: `False`
- Move applied: `False`

## Pending Bindings

- `fixture_set_reference`: `PENDING`
- `exact_source_snapshot_reference`: `PENDING`
- `exact_step_and_move_budget_reference`: `PENDING`
- `pressure_readout_contract_reference`: `PENDING`
- `evidence_yield_report_contract_reference`: `PENDING`
- `construction_readiness_gate_reference`: `PENDING`
- `active_execution_authority_reference`: `ABSENT_BY_POLICY`
- `active_sweep_authority_reference`: `ABSENT_BY_POLICY`

## Nonclaims

- `does_not_create_fixture_set`
- `does_not_bind_exact_source_snapshot`
- `does_not_bind_exact_runtime_budgets`
- `does_not_create_active_authority`

## Projection Notes

- M2 resolves the ten VS2.5 M1 bindings.
- VS2.6 bindings remain pending and active authorities remain absent by policy.
- This Markdown file is a deterministic projection of the JSON artifact.
