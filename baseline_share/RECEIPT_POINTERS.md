# Receipt Pointers

This packet does not copy the full receipt stack. Receipts remain evidence and should be expanded only when a claim becomes load-bearing.

## Full receipt locations

- External WSL receipt archive: `/home/asd/matrixlab_receipts/` - present; file count: `872`.
- Repo architecture extraction receipt copy: `docs/matrixlabs/receipts/` - present; file count: `714`.
- Repo Phase VS2 receipt JSONs: `docs/matrixlabs/phase_vs2/*receipt*.json` - file count: `7`.
- Repo Post-VS2 receipt JSONs: `docs/matrixlabs/post_vs2/*receipt*.json` - file count: `8`.
- Repo Post-VS2 surface-preparation receipt JSONs: file count: `1`.
- Repo Post-VS2 receipt-machinery preparation receipt JSONs: file count: `1`.
- Repo Post-VS2 decision-receipt implementation-repair receipt JSONs: file count: `1`.
- Repo authoritative Post-VS2 human decision receipt JSONs: file count: `0`.

## Current load-bearing recent receipt pointers

- C8 post-patch surface decision acceptance receipt: `data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_22e01dcc.json` - present.

## Post-VS2 receipt pointers

- `docs/matrixlabs/post_vs2/post_vs2_d01_populated_receipt_confirmation_input_contract_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_d01_populated_receipt_confirmation_surface_preparation_receipt_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_d01_populated_receipt_confirmation_surface_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_contract_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_d01_draft_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_implementation_repair_receipt_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_receipt_machinery_receipt_v0.json`
- `docs/matrixlabs/post_vs2/post_vs2_first_execution_decision_surface_receipt_v0.json`

## Architecture extraction terminal receipt pointer

- `/home/asd/matrixlab_receipts/quarantine_vs0_3_diagnostic_20260709_133716/docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json`
- `/home/asd/matrixlab_receipts/quarantine_vs0_3_diagnostic_20260709_133716/scripts/verify_phase_vs0_happy_path_v0.py`
- `/home/asd/matrixlab_receipts/receipt_20260625_002318.txt`
- `/home/asd/matrixlab_receipts/receipt_20260625_002942.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_144848.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_145207.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_150542.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_200018.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_221233.txt`
- `/home/asd/matrixlab_receipts/receipt_20260630_222449.txt`

## Upload rule

Upload `baseline_share/` first. Expand individual receipts only when a claim becomes load-bearing. Do not upload or duplicate the full receipt archive unless a later bounded task specifically asks for that evidence.
