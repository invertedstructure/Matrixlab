# C8 n22 human decision surface v0

## Surface

This is a human decision surface.

It presents options only.

It does not record a decision.

It does not consume HUMAN_ACCEPTANCE.

It does not change authority state.

The formal boundary record remains source of truth.

The Readabout remains downstream projection only.

## Source authority and projection boundary

- Formal source role: FORMAL_SOURCE_OBJECT_REMAINS_AUTHORITY.
- READABOUT role: downstream human-audit projection only.
- This decision surface presents typed options only; it does not consume HUMAN_ACCEPTANCE and does not change authority state.

Accept-as-basis authorizes only preparation of the next bounded unit definition surface.

Its typed effects grant basis-for-next-unit-definition authority and preparation authority only; final next-unit-definition authority remains NOT_GRANTED.

Execution remains NOT_GRANTED.

Reuse remains NOT_GRANTED.

Taxonomy promotion remains NOT_GRANTED.

Updater generalization remains NOT_GRANTED.

Runner authority remains NOT_GRANTED.

## Identity

- decision_surface_id = c8.n22.human_decision_surface.v0
- schema_version = matrixlabs_human_decision_surface_v0
- surface_role = HUMAN_DECISION_SURFACE
- source_boundary_record_id = c8.n22.boundary_transition.v0
- source_readabout_id = c8.n22.authority_boundary.readabout.v0
- required_authority_event = HUMAN_ACCEPTANCE
- authority_event_status_before = AUTH_EVENT_UNCONSUMED
- current_authority_state = AUTH_STATE_OBSERVED_NOT_AUTHORIZED
- requested_transition = ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- surface_status = PRESENTS_TYPED_OPTIONS_ONLY
- decision_consumed = false
- authority_changed = false

## Options

### DECISION_ACCEPT_AS_BASIS_FOR_NEXT_UNIT_DEFINITION

- option_kind = AUTHORITY_EVENT_CONSUMING_OPTION
- consumes_decision_event = HUMAN_DECISION
- consumes_authority_event = HUMAN_ACCEPTANCE
- resulting_authority_state = AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- next_allowed_surface_if_selected = PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE

Authority effects:
- basis_for_next_unit_definition_authority = GRANTED
- next_unit_definition_surface_preparation_authority = GRANTED
- next_unit_definition_authority = NOT_GRANTED
- execution_authority = NOT_GRANTED
- reuse_authority = NOT_GRANTED
- taxonomy_promotion_authority = NOT_GRANTED
- updater_generalization_authority = NOT_GRANTED
- runner_authority = NOT_GRANTED

Must not impersonate:
- NEXT_UNIT_DEFINITION_FINALIZATION
- EXECUTION_AUTHORITY
- REUSE_AUTHORITY
- TAXONOMY_PROMOTION
- UPDATER_GENERALIZATION
- RUNNER_AUTHORITY

### DECISION_ACCEPT_AS_DISCUSSION_SURFACE_ONLY

- option_kind = DECISION_CLASSIFYING_OPTION
- consumes_decision_event = HUMAN_DECISION
- consumes_authority_event = NONE
- resulting_authority_state = AUTH_STATE_DISCUSSION_SURFACE_ONLY
- next_allowed_surface_if_selected = CONTINUE_DISCUSSION_OR_RETYPE_SURFACE

Authority effects:
- basis_for_next_unit_definition_authority = NOT_GRANTED
- next_unit_definition_surface_preparation_authority = NOT_GRANTED
- next_unit_definition_authority = NOT_GRANTED
- execution_authority = NOT_GRANTED
- reuse_authority = NOT_GRANTED
- taxonomy_promotion_authority = NOT_GRANTED
- updater_generalization_authority = NOT_GRANTED
- runner_authority = NOT_GRANTED

Must not impersonate:
- ACCEPTED_AS_BASIS
- AUTHORITY_ADVANCE
- NEXT_UNIT_PREPARATION_AUTHORITY
- EXECUTION_AUTHORITY

### DECISION_REQUEST_RETYPE_OR_REVISE

- option_kind = NON_AUTHORITY_ADVANCING_OPTION
- consumes_decision_event = HUMAN_DECISION
- consumes_authority_event = NONE
- resulting_authority_state = AUTH_STATE_OBSERVED_NOT_AUTHORIZED
- next_allowed_surface_if_selected = PREPARE_RETYPE_OR_REVISE_SURFACE

Authority effects:
- basis_for_next_unit_definition_authority = NOT_GRANTED
- next_unit_definition_surface_preparation_authority = NOT_GRANTED
- next_unit_definition_authority = NOT_GRANTED
- execution_authority = NOT_GRANTED
- reuse_authority = NOT_GRANTED
- taxonomy_promotion_authority = NOT_GRANTED
- updater_generalization_authority = NOT_GRANTED
- runner_authority = NOT_GRANTED

Must not impersonate:
- AUTHORITY_ADVANCE
- ACCEPTANCE
- REJECTION
- EXECUTION_AUTHORITY

### DECISION_DEFER

- option_kind = NON_AUTHORITY_CHANGING_OPTION
- consumes_decision_event = HUMAN_DECISION
- consumes_authority_event = NONE
- resulting_authority_state = AUTH_STATE_OBSERVED_NOT_AUTHORIZED
- next_allowed_surface_if_selected = NONE_DECISION_DEFERRED

Authority effects:
- basis_for_next_unit_definition_authority = NOT_GRANTED
- next_unit_definition_surface_preparation_authority = NOT_GRANTED
- next_unit_definition_authority = NOT_GRANTED
- execution_authority = NOT_GRANTED
- reuse_authority = NOT_GRANTED
- taxonomy_promotion_authority = NOT_GRANTED
- updater_generalization_authority = NOT_GRANTED
- runner_authority = NOT_GRANTED

Must not impersonate:
- ACCEPTANCE
- REJECTION
- AUTHORITY_ADVANCE
- EXECUTION_AUTHORITY

### DECISION_REJECT_AS_BASIS

- option_kind = NON_AUTHORITY_ADVANCING_OPTION
- consumes_decision_event = HUMAN_DECISION
- consumes_authority_event = NONE
- resulting_authority_state = AUTH_STATE_REJECTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION
- next_allowed_surface_if_selected = NONE_REJECTED_AS_BASIS

Authority effects:
- basis_for_next_unit_definition_authority = NOT_GRANTED
- next_unit_definition_surface_preparation_authority = NOT_GRANTED
- next_unit_definition_authority = NOT_GRANTED
- execution_authority = NOT_GRANTED
- reuse_authority = NOT_GRANTED
- taxonomy_promotion_authority = NOT_GRANTED
- updater_generalization_authority = NOT_GRANTED
- runner_authority = NOT_GRANTED

Must not impersonate:
- ACCEPTANCE
- AUTHORITY_ADVANCE
- RETYPE_REQUEST
- EXECUTION_AUTHORITY

## Surface gate

decision_surface_gate = DECISION_SURFACE_PASS_OPTIONS_PRESENTED_ONLY
decision_option_count = 5
decision_consumed = false
authority_changed = false
selected_decision_present = false
recommendation_inserted = false
execution_authority_granted_count = 0
next_unit_definition_authority_granted_count = 0
reuse_authority_granted_count = 0
taxonomy_promotion_authority_granted_count = 0
updater_generalization_authority_granted_count = 0
runner_authority_granted_count = 0
markdown_json_parity_status = PASS
meaning_parity_status = PASS

## Non-claims

- This decision surface does not record a decision.
- This decision surface does not consume HUMAN_ACCEPTANCE.
- This decision surface does not change authority state.
- The formal boundary record remains source of truth.
- The Readabout remains downstream projection only.
- Accept-as-basis authorizes only preparation of the next bounded unit definition surface.
- This decision surface does not define the next bounded unit.
- This decision surface does not finalize the next bounded unit.
- Execution remains NOT_GRANTED.
- Reuse remains NOT_GRANTED.
- Taxonomy promotion remains NOT_GRANTED.
- Updater generalization remains NOT_GRANTED.
- Runner authority remains NOT_GRANTED.

## Unsafe to infer

- Unsafe to infer: a decision has been selected.
- Unsafe to infer: HUMAN_ACCEPTANCE has been consumed.
- Unsafe to infer: authority state has changed.
- Unsafe to infer: the next bounded unit is defined.
- Unsafe to infer: the next bounded unit is authorized.
- Unsafe to infer: execution is authorized.
- Unsafe to infer: reuse is authorized.
- Unsafe to infer: taxonomy has been promoted.
- Unsafe to infer: updater generalization is authorized.
- Unsafe to infer: runner authority exists.
