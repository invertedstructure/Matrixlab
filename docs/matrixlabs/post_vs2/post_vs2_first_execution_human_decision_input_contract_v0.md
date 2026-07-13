# Post-VS2 First Execution Human Decision Input Contract v0

## Identity

- Artifact ID: `post_vs2_first_execution_human_decision_input_contract_v0`
- Contract ID: `POST_VS2_FIRST_EXECUTION_HUMAN_DECISION_INPUT_CONTRACT_V0`
- Contract status: `DEFINED_NOT_CONSUMED`
- Required input object: `post_vs2_first_execution_human_decision_input_v0`

## Required Fields

- `schema_version`
- `input_id`
- `input_version`
- `decision_timestamp`
- `decision_actor_class`
- `decision_actor_reference`
- `decision_actor_authentication_reference`
- `decision_interface_contract_reference`
- `decision_surface_id`
- `decision_surface_version`
- `decision_surface_canonical_hash`
- `selected_surface_option_code`
- `decision_payload`
- `decision_rationale`

## Option Vocabulary

- `AUTHORIZE_EXACT_SEALED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE` -> `D01`
- `REQUEST_REDUCED_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION` -> `D02`
- `RETURN_SEALED_FIRST_SWEEP_KERNEL_PACKAGE_FOR_REVISION` -> `D03`
- `DEFER_FIRST_SWEEP_KERNEL_EXECUTION_DECISION` -> `D04`
- `REJECT_CURRENT_FIRST_SWEEP_KERNEL_EXECUTION_REQUEST` -> `D05`
- `ABANDON_FIRST_SWEEP_KERNEL_EXECUTION_PACKAGE_VERSION` -> `D06`

## Generic Proceed Boundary

- generic_proceed_language_maps_to_surface_option: `false`
- no_default_option_exists: `true`

## Timestamp And Secret Boundary

- Timestamp syntax: `YYYY-MM-DDTHH:MM:SSZ`
- The receipt builder does not call the current clock to create or modify a decision timestamp.
- Authentication reference is evidence, not a password, token, private key, cookie, or credential.
- Secrets must not be embedded in the decision input or receipt.
