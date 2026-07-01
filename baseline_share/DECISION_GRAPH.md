# Decision Graph

Source: `docs/matrixlabs/architecture/decision_graph_readout_v0.md`.

This file summarizes observed decision graph structure. Compression candidates remain proposals only.

## Observed Recurring Pattern

Across C8 runtime adoption, C8 unit-feedback hardening, bounded schema archive surfaces, and Cell1 chains, the following pattern recurs:

1. Create packet.
2. Review packet.
3. Commit packet.
4. Accept packet or record decision.
5. Review acceptance.
6. Commit acceptance.
7. Execute one bounded unit when explicitly authorized.
8. Review execution.
9. Commit execution.
10. Create closure/readiness packet.
11. Decide post-closure or post-patch surface.

Evidence surfaces include `data/c8_runtime_adoption_*`, `data/c8_unit_feedback_hardening_*`, `data/bounded_structured_t6_trigger_surface_capability_schema_archive_*`, `data/cell1_*`, and related `scripts/create_*`, `scripts/accept_*`, `scripts/execute_*`, `scripts/close_*`, and `scripts/decide_*` files.

## Authority Boundary Notes

| Step | Allowed | Not allowed |
| --- | --- | --- |
| Create packet | Materialize one bounded packet, question, readout, target, or prep artifact for review. | Execute the packet, infer human acceptance, mutate source/receipts, promote schema, authorize hidden next work. |
| Review packet | Inspect source binding, boundary counters, negative controls, packet shape, and next-surface options. | Treat review as acceptance, execute runtime/probe/build/rerun, broaden authority. |
| Commit packet | Record the packet artifact in version control when approved by the operator workflow. | Treat commit as semantic acceptance or reusable authorization. |
| Accept packet/decision | Record bounded human decision or acceptance for the exact framed next step. | Convert one-time acceptance into reusable/preapproved schema authority; mutate schema archive unless that is the specifically authorized later unit. |
| Review acceptance | Verify acceptance scope, source chain, no hidden side effects, and next target. | Execute the next target without its own authorization. |
| Commit acceptance | Preserve the acceptance artifact/receipt. | Treat commit as future execution authority. |
| Execute bounded unit | Run exactly the authorized bounded execution unit and emit receipt/artifacts. | Execute adjacent units, rerun, discover/probe/build beyond scope, mutate unrelated source, or rewrite receipts. |
| Review execution | Classify result, audit boundaries, inspect receipts, identify useful/insufficient feedback. | Repair or rerun unless separately authorized. |
| Commit execution | Preserve execution artifacts and receipts. | Treat commit as closure or next-surface selection unless a closure/readiness packet says so. |
| Closure/readiness packet | Declare reviewed closure/readiness and identify candidate next decision surface. | Execute future units, authorize C8 rerun, grant reusable schema promotion, or open hidden work. |
| Post-closure/post-patch surface decision | Choose or request the next bounded surface for future packetization. | Treat surface decision as the future execution itself. |

## Compression Candidates

Candidate compression areas, labeled as proposals only:

- A generic readout of packet lineage: source packet, review packet, acceptance packet, execution packet, closure packet.
- Receipt inventory checks: expected receipt exists, source receipt IDs are bound, prior receipts were not mutated.
- Boundary-audit shape checks: allowed actions, forbidden actions, negative controls, and no hidden next command.
- Closure/readiness readout format: what closed, what remains open, what future decision surface is only proposed.

## Authority-sensitive Pieces Not Yet Compressible

- Human decisions and one-time acceptances.
- Schema archive promotion, mutation target prep, write authorization, and write execution.
- Runtime adoption, C8 rerun, probe execution, build execution, and source mutation.
- Validator/admissibility decisions where source status, trigger object family, or authority boundary is unresolved.
- Any use of archived graphs/schemas as reusable/preapproved authority.

Any future decision graph runner must carry explicit trigger object families, authority boundaries, source surfaces, receipt requirements, human-governed promotion rules, and fail-closed behavior before it can be more than an observation/archive layer.

## Decision Path Index v0

M1 observability/addressability surface for `docs/matrixlabs/architecture/c8_observed_decision_path_v0.json`. It is not authority, not receipt validation, and not compression.

- `docs/matrixlabs/observability/decision_path_index_v0.json` - present
- `docs/matrixlabs/observability/decision_path_index_v0.md` - present
