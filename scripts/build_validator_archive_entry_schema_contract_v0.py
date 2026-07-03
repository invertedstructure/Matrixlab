#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

OUT_JSON = Path("docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.json")
OUT_MD = Path("docs/matrixlabs/validator_archive/validator_archive_entry_schema_contract_v0.md")

REQUIRED_GROUPS = [
    "identity",
    "archive_status",
    "source_basis",
    "authority_scope",
    "requested_action_scope",
    "input_object_shape",
    "output_object_shape",
    "machine_action_scope",
    "radius_discipline",
    "validator_requirements",
    "receipt_obligations",
    "halt_conditions",
    "escalation_conditions",
    "freshness_rules",
    "forbidden_authority_changes",
    "promotion_and_reuse_status",
    "revocation_and_expiry",
    "readabout_projection_hooks",
]

def group(
    group_id: str,
    group_role: str,
    required_fields: list[str],
    missing_field_halt: str,
    non_impersonation: list[str],
    **extra: object,
) -> dict:
    rec = {
        "group_id": group_id,
        "group_role": group_role,
        "required_fields": required_fields,
        "required_value_policy": "MUST_BE_EXPLICIT_NO_DEFAULT_INFERENCE",
        "missing_field_halt": missing_field_halt,
        "non_impersonation": non_impersonation,
    }
    rec.update(extra)
    return rec

FIELD_GROUP_CONTRACTS = [
    group(
        "identity",
        "MAKE_ARCHIVE_ENTRIES_ADDRESSABLE_AND_VERSIONED",
        [
            "archive_entry_id",
            "archive_entry_version",
            "archive_entry_kind",
            "archive_entry_status",
            "created_from_source_kind",
            "created_from_source_id",
            "created_at_or_commit_context",
        ],
        "ARCHIVE_SCHEMA_FAIL_IDENTITY_GROUP_MISSING",
        [
            "identity_does_not_imply_validity",
            "identity_does_not_imply_reuse_authority",
        ],
    ),
    group(
        "archive_status",
        "SEPARATE_CANDIDATE_REVIEW_PREAPPROVED_ACTIVE_REVOKED_AND_EXPIRED_STATES",
        [
            "archive_entry_status",
            "promotion_status",
            "reuse_authority_status",
            "activation_status",
            "expiration_status",
            "revocation_status",
        ],
        "ARCHIVE_SCHEMA_FAIL_STATUS_GROUP_MISSING",
        [
            "archive_entry_status_does_not_imply_reuse_authority",
            "promotion_status_does_not_imply_activation_status",
            "preapproved_inactive_does_not_mean_active",
        ],
    ),
    group(
        "source_basis",
        "DECLARE_WHAT_SPECIMEN_DECISION_OR_PROMOTION_OBJECT_PRODUCED_THE_ENTRY",
        [
            "source_specimen_kind",
            "source_specimen_id",
            "source_route_classification_id",
            "source_decision_receipt_id",
            "source_promotion_receipt_id",
            "source_commit_sha",
            "source_artifact_paths",
        ],
        "ARCHIVE_SCHEMA_FAIL_SOURCE_BASIS_GROUP_MISSING",
        [
            "candidate_source_specimen_is_not_sufficient_for_active_reuse",
            "active_entries_require_promotion_decision_receipt_id",
        ],
    ),
    group(
        "authority_scope",
        "DEFINE_WHEN_ENTRY_MAY_APPLY",
        [
            "allowed_current_authority_state",
            "allowed_prior_authority_event_status",
            "allowed_basis_scope",
            "allowed_source_object_type",
            "allowed_source_object_status",
            "forbidden_current_authority_states",
        ],
        "ARCHIVE_SCHEMA_FAIL_AUTHORITY_SCOPE_GROUP_MISSING",
        [
            "does_not_grant_authority",
            "does_not_extend_scope_by_similarity",
            "must_not_apply_to_merely_observed_objects_unless_explicitly_scoped",
        ],
    ),
    group(
        "requested_action_scope",
        "DEFINE_EXACT_REQUESTED_ACTION_THE_ENTRY_MAY_ROUTE_OR_PERMIT",
        [
            "allowed_requested_action",
            "allowed_requested_action_scope",
            "allowed_output_kind",
            "forbidden_requested_actions",
        ],
        "ARCHIVE_SCHEMA_FAIL_REQUESTED_ACTION_SCOPE_GROUP_MISSING",
        [
            "does_not_authorize_forbidden_requested_actions",
            "does_not_generalize_by_action_similarity",
        ],
        forbidden_action_examples=[
            "EXECUTE_UNIT",
            "PROMOTE_SCHEMA",
            "AUTHORIZE_REUSE",
            "ACTIVATE_RUNNER",
            "REWRITE_RECEIPTS",
        ],
    ),
    group(
        "input_object_shape",
        "ENSURE_ENTRY_APPLIES_ONLY_TO_EXPECTED_FORMAL_INPUT_OBJECTS",
        [
            "required_input_object_type",
            "required_input_schema_version",
            "required_input_authority_fields",
            "required_input_source_fields",
            "required_input_non_effect_fields",
            "required_input_commit_or_freshness_fields",
        ],
        "ARCHIVE_SCHEMA_FAIL_INPUT_SHAPE_GROUP_MISSING",
        [
            "must_not_operate_on_loose_prose",
            "must_not_operate_on_markdown_as_source_authority",
            "must_not_operate_on_chat_text_as_source_authority",
            "must_not_operate_on_readabout_projection_as_source_authority",
        ],
    ),
    group(
        "output_object_shape",
        "DEFINE_OUTPUT_OBJECT_SHAPE_IF_ENTRY_IS_LATER_ACTIVE",
        [
            "allowed_output_object_type",
            "allowed_output_schema_version",
            "required_output_fields",
            "required_output_nonclaims",
            "required_output_receipts",
        ],
        "ARCHIVE_SCHEMA_FAIL_OUTPUT_SHAPE_GROUP_MISSING",
        [
            "contract_defines_field_but_does_not_fill_instance_value",
            "output_shape_does_not_authorize_output_creation",
        ],
    ),
    group(
        "machine_action_scope",
        "STATE_WHAT_MACHINE_MAY_DO_UNDER_AN_ACTIVE_ENTRY",
        [
            "machine_action_scope",
            "auto_disposition_allowed",
            "human_review_required",
            "human_acceptance_required",
            "action_performs_authority_change",
        ],
        "ARCHIVE_SCHEMA_FAIL_MACHINE_SCOPE_GROUP_MISSING",
        [
            "contract_defines_scopes_but_authorizes_none",
            "auto_disposition_requires_explicit_active_entry",
        ],
        scope_vocabulary_defined_by_contract=[
            "CLASSIFY_ONLY",
            "PREPARE_SURFACE_ONLY",
            "APPLY_AUTHORITY_TRANSITION",
            "EXECUTE_LOCAL_UNIT",
            "BATCH_EXECUTE_WITH_RADIUS",
        ],
    ),
    group(
        "radius_discipline",
        "PREVENT_SINGLE_USE_BEHAVIOR_FROM_BECOMING_BROAD_AUTOMATION",
        [
            "radius_mode",
            "radius_limit",
            "radius_unit",
            "radius_consumed_per_action",
            "radius_reset_rule",
            "radius_escalation_rule",
            "radius_expansion_requires_decision",
        ],
        "ARCHIVE_SCHEMA_FAIL_RADIUS_GROUP_MISSING",
        [
            "candidate_entries_must_use_radius_0_candidate_only",
            "active_entries_may_expand_radius_only_if_promotion_and_activation_explicitly_grant_it",
            "no_implicit_radius_expansion",
        ],
        radius_vocabulary_defined_by_contract=[
            "RADIUS_0_CANDIDATE_ONLY",
            "RADIUS_1_SINGLE_OBJECT",
            "RADIUS_N_DECLARED_BATCH",
        ],
    ),
    group(
        "validator_requirements",
        "DECLARE_CHECKS_THAT_MUST_PASS_BEFORE_ENTRY_CAN_BE_USED",
        [
            "required_validators",
            "validator_versions",
            "validator_input_fields",
            "validator_pass_statuses",
            "validator_fail_statuses",
        ],
        "ARCHIVE_SCHEMA_FAIL_VALIDATOR_REQUIREMENTS_GROUP_MISSING",
        [
            "missing_validator_halts_use",
            "validator_pass_does_not_bypass_receipt_obligations",
        ],
        example_validators=[
            "authority_state_match_validator",
            "requested_action_scope_validator",
            "basis_scope_validator",
            "forbidden_effects_validator",
            "output_shape_validator",
            "freshness_validator",
            "radius_validator",
        ],
    ),
    group(
        "receipt_obligations",
        "DECLARE_RECEIPTS_REQUIRED_WHEN_AN_ACTIVE_ENTRY_IS_USED",
        [
            "required_receipts_before_action",
            "required_receipts_during_action",
            "required_receipts_after_action",
            "required_closeout_receipt",
            "required_baseline_projection",
        ],
        "ARCHIVE_SCHEMA_FAIL_RECEIPT_OBLIGATIONS_GROUP_MISSING",
        [
            "no_receipt_obligations_no_preapproval",
            "receipts_are_required_for_active_entry_use",
        ],
    ),
    group(
        "halt_conditions",
        "DEFINE_WHEN_MACHINE_MUST_STOP",
        [
            "mandatory_halt_conditions",
            "halt_codes",
            "halt_receipt_required",
            "halt_readabout_required_if_human_facing",
        ],
        "ARCHIVE_SCHEMA_FAIL_HALT_CONDITIONS_GROUP_MISSING",
        [
            "every_archive_entry_must_declare_halt_conditions",
            "halt_does_not_equal_escalation",
        ],
        initial_halt_codes=[
            "HALT_AUTHORITY_STATE_MISMATCH",
            "HALT_REQUESTED_ACTION_SCOPE_MISMATCH",
            "HALT_BASIS_SCOPE_MISMATCH",
            "HALT_OUTPUT_KIND_MISMATCH",
            "HALT_FORBIDDEN_EFFECT_DETECTED",
            "HALT_VALIDATOR_MISSING",
            "HALT_RADIUS_EXCEEDED",
            "HALT_SOURCE_FRESHNESS_UNKNOWN",
        ],
    ),
    group(
        "escalation_conditions",
        "DEFINE_WHEN_MACHINE_MUST_ROUTE_TO_REVIEW_INSTEAD_OF_ACTING",
        [
            "mandatory_escalation_conditions",
            "escalation_codes",
            "escalation_target",
            "escalation_surface_required",
        ],
        "ARCHIVE_SCHEMA_FAIL_ESCALATION_CONDITIONS_GROUP_MISSING",
        [
            "escalation_routes_to_review_but_does_not_authorize_action",
            "escalation_does_not_equal_halt",
        ],
        initial_escalation_codes=[
            "ESCALATE_BOUNDARY_UNCLEAR",
            "ESCALATE_SCHEMA_SCOPE_AMBIGUOUS",
            "ESCALATE_FRESHNESS_UNKNOWN",
            "ESCALATE_OUTPUT_SHAPE_UNEXPECTED",
            "ESCALATE_AUTHORITY_CHANGE_REQUESTED",
            "ESCALATE_HUMAN_PROMOTION_REQUIRED",
        ],
    ),
    group(
        "freshness_rules",
        "PREVENT_STALE_SOURCE_FROM_BEING_TREATED_AS_CURRENT_AUTHORITY",
        [
            "freshness_required",
            "freshness_basis",
            "allowed_freshness_statuses",
            "stale_source_halt_code",
            "unknown_freshness_halt_code",
        ],
        "ARCHIVE_SCHEMA_FAIL_FRESHNESS_GROUP_MISSING",
        [
            "readabout_may_project_freshness_but_is_not_source_authority",
            "unknown_freshness_halts",
        ],
        allowed_freshness_statuses_defined_by_contract=[
            "SOURCE_COMMIT_VERIFIED",
        ],
    ),
    group(
        "forbidden_authority_changes",
        "PREVENT_ARCHIVE_USE_FROM_SMUGGLING_STRONGER_AUTHORITY",
        [
            "forbidden_authority_changes",
            "forbidden_side_effects",
            "required_non_effect_checks",
        ],
        "ARCHIVE_SCHEMA_FAIL_FORBIDDEN_AUTHORITY_GROUP_MISSING",
        [
            "no_implicit_default",
            "forbidden_authority_changes_must_be_checked",
        ],
        forbidden_authority_classes=[
            "EXECUTION_AUTHORITY",
            "REUSE_AUTHORITY",
            "TAXONOMY_PROMOTION_AUTHORITY",
            "UPDATER_GENERALIZATION_AUTHORITY",
            "RUNNER_AUTHORITY",
            "RECEIPT_REWRITE_AUTHORITY",
            "OBSERVED_PATH_UPDATE_AUTHORITY",
        ],
        required_authority_status_vocabulary=[
            "NOT_GRANTED",
            "GRANTED_FOR_DECLARED_SCOPE",
            "FORBIDDEN",
        ],
    ),
    group(
        "promotion_and_reuse_status",
        "MAKE_PROMOTION_REUSE_AND_ACTIVATION_EXPLICIT_AUTHORITY_STATES",
        [
            "promotion_status",
            "promotion_decision_receipt_id",
            "promotion_scope",
            "reuse_authority_status",
            "reuse_scope",
            "reuse_activation_status",
        ],
        "ARCHIVE_SCHEMA_FAIL_PROMOTION_REUSE_GROUP_MISSING",
        [
            "promotion_does_not_imply_activation",
            "reuse_authority_requires_declared_scope",
            "active_use_requires_activation_receipt",
        ],
        candidate_entry_required_values={
            "promotion_status": "PROMOTION_NOT_REQUESTED",
            "reuse_authority_status": "REUSE_AUTHORITY_NOT_GRANTED",
            "activation_status": "ACTIVATION_NOT_APPLICABLE",
        },
        preapproved_inactive_required_values={
            "promotion_decision_receipt_id": "REQUIRED",
            "reuse_scope": "REQUIRED",
            "activation_status": "ACTIVATION_INACTIVE",
        },
        active_entry_required_values={
            "promotion_decision_receipt_id": "REQUIRED",
            "reuse_scope": "REQUIRED",
            "activation_status": "ACTIVATION_ACTIVE",
            "activation_receipt_id": "REQUIRED",
        },
    ),
    group(
        "revocation_and_expiry",
        "MAKE_PREAPPROVAL_REVERSIBLE_AND_BOUNDED",
        [
            "expiry_rule",
            "review_required_after",
            "revocation_status",
            "revocation_reason",
            "revocation_receipt_id",
        ],
        "ARCHIVE_SCHEMA_FAIL_REVOCATION_EXPIRY_GROUP_MISSING",
        [
            "no_forever_by_omission",
            "revocation_status_must_be_explicit",
        ],
        v0_minimum_expiry_rule="NONE_DECLARED_FOR_V0",
    ),
    group(
        "readabout_projection_hooks",
        "MAKE_ARCHIVE_ENTRIES_PROJECTABLE_INTO_HUMAN_AUDIT_LANGUAGE_WITHOUT_REWRITING_MEANING",
        [
            "readabout_required_for_human_promotion",
            "readabout_projection_allowed",
            "source_of_truth_role",
            "projection_claim_requirements",
        ],
        "ARCHIVE_SCHEMA_FAIL_READABOUT_HOOKS_GROUP_MISSING",
        [
            "human_facing_projection_is_downstream_and_field_backed",
            "archive_entries_remain_formal_source_objects",
            "readabout_projection_does_not_create_authority",
        ],
    ),
]

def build_artifact() -> dict:
    gate = {
        "archive_schema_gate": "ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED",
        "required_field_group_count": 18,
        "required_field_groups_present": True,
        "authority_creation_detected": False,
        "archive_entry_created": False,
        "candidate_entry_created": False,
        "reuse_authority_granted": False,
        "promotion_granted": False,
        "active_archive_entry_created": False,
        "auto_disposition_allowed": False,
        "runner_authority_created": False,
        "failures": [],
    }
    for gid in REQUIRED_GROUPS:
        gate[f"{gid}_group_present"] = True

    return {
        "schema_version": "matrixlabs_validator_archive_entry_schema_contract_v0",
        "archive_schema_contract_id": "validator_archive_entry_schema_contract.v0",
        "contract_role": "ARCHIVE_ENTRY_CONTRACT_ONLY",
        "contract_status": "ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED",
        "generated_by": "scripts/build_validator_archive_entry_schema_contract_v0.py",
        "contract_authority_state": {
            "archive_entry_creation_status": "NO_ARCHIVE_ENTRY_CREATED_BY_CONTRACT",
            "candidate_entry_creation_status": "NO_CANDIDATE_ENTRY_CREATED_BY_CONTRACT",
            "promotion_status": "PROMOTION_NOT_GRANTED_BY_CONTRACT",
            "reuse_authority_status": "REUSE_AUTHORITY_NOT_GRANTED_BY_CONTRACT",
            "activation_status": "ACTIVATION_NOT_APPLICABLE_TO_CONTRACT",
            "auto_disposition_status": "AUTO_DISPOSITION_NOT_ALLOWED_BY_CONTRACT",
            "runner_authority_status": "RUNNER_AUTHORITY_NOT_CREATED_BY_CONTRACT",
        },
        "required_field_groups": REQUIRED_GROUPS,
        "field_group_contracts": FIELD_GROUP_CONTRACTS,
        "entry_status_vocabulary": {
            "archive_entry_status": [
                "ARCHIVE_STATUS_NONE",
                "ARCHIVE_STATUS_CANDIDATE",
                "ARCHIVE_STATUS_REVIEW_REQUIRED",
                "ARCHIVE_STATUS_PREAPPROVED_INACTIVE",
                "ARCHIVE_STATUS_PREAPPROVED_ACTIVE",
                "ARCHIVE_STATUS_REVOKED",
                "ARCHIVE_STATUS_EXPIRED",
            ],
            "promotion_status": [
                "PROMOTION_NOT_REQUESTED",
                "PROMOTION_PENDING_HUMAN_DECISION",
                "PROMOTION_GRANTED_FOR_DECLARED_SCOPE",
                "PROMOTION_REJECTED",
                "PROMOTION_REVOKED",
            ],
            "reuse_authority_status": [
                "REUSE_AUTHORITY_NOT_GRANTED",
                "REUSE_AUTHORITY_GRANTED_FOR_DECLARED_SCOPE",
            ],
            "activation_status": [
                "ACTIVATION_NOT_APPLICABLE",
                "ACTIVATION_INACTIVE",
                "ACTIVATION_ACTIVE",
                "ACTIVATION_REVOKED",
                "ACTIVATION_EXPIRED",
            ],
        },
        "contract_laws": {
            "schema_contract_does_not_create_entry": True,
            "schema_contract_does_not_create_candidate": True,
            "archive_entry_status_does_not_imply_reuse_authority": True,
            "promotion_status_does_not_imply_activation_status": True,
            "candidate_source_specimen_is_not_sufficient_for_active_reuse": True,
            "preapproved_inactive_entry_is_not_active": True,
            "no_receipt_obligations_no_preapproval": True,
            "no_implicit_radius_expansion": True,
            "no_forever_by_omission": True,
            "readabout_projection_is_downstream_only": True,
        },
        "derived_non_effect_checks": {
            "creates_archive_entry": False,
            "creates_candidate_entry": False,
            "grants_promotion": False,
            "grants_reuse_authority": False,
            "creates_active_entry": False,
            "allows_auto_disposition": False,
            "creates_runner_authority": False,
        },
        "contract_gate": gate,
        "failure_vocabulary": [
            "ARCHIVE_SCHEMA_FAIL_IDENTITY_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_STATUS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_SOURCE_BASIS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_AUTHORITY_SCOPE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_REQUESTED_ACTION_SCOPE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_INPUT_SHAPE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_OUTPUT_SHAPE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_MACHINE_SCOPE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_RADIUS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_VALIDATOR_REQUIREMENTS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_RECEIPT_OBLIGATIONS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_HALT_CONDITIONS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_ESCALATION_CONDITIONS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_FRESHNESS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_FORBIDDEN_AUTHORITY_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_PROMOTION_REUSE_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_REVOCATION_EXPIRY_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_READABOUT_HOOKS_GROUP_MISSING",
            "ARCHIVE_SCHEMA_FAIL_ARCHIVE_ENTRY_CREATED",
            "ARCHIVE_SCHEMA_FAIL_CANDIDATE_ENTRY_CREATED",
            "ARCHIVE_SCHEMA_FAIL_PROMOTION_GRANTED",
            "ARCHIVE_SCHEMA_FAIL_REUSE_GRANTED",
            "ARCHIVE_SCHEMA_FAIL_ACTIVE_ENTRY_CREATED",
            "ARCHIVE_SCHEMA_FAIL_AUTO_DISPOSITION_ALLOWED",
            "ARCHIVE_SCHEMA_FAIL_RUNNER_AUTHORITY_CREATED",
            "ARCHIVE_SCHEMA_FAIL_INSTANCE_VALUE_INSERTED",
            "ARCHIVE_SCHEMA_FAIL_MARKDOWN_JSON_PARITY",
            "ARCHIVE_SCHEMA_FAIL_RECOMMENDATION_INSERTED",
        ],
        "non_claims": [
            "C.1 does not create an archive entry.",
            "C.1 does not create a candidate archive entry.",
            "C.1 does not represent the prior router specimen as a candidate.",
            "C.1 does not grant promotion.",
            "C.1 does not authorize reuse.",
            "C.1 does not activate an archive entry.",
            "C.1 does not allow auto-disposition.",
            "C.1 does not create runner authority.",
            "C.1 does not execute or prepare any move.",
            "C.1 only defines the required contract shape for future validator archive entries.",
        ],
        "unsafe_to_infer": [
            "schema_contract_implies_schema_authorization",
            "candidate_entry_implies_reuse_authority",
            "promotion_implies_activation",
            "preapproved_inactive_implies_active",
            "local_specimen_implies_reusable_authority",
        ],
        "terminal_transition": "ADVANCE(C2_VALIDATOR_ARCHIVE_CANDIDATE_ENTRY_PENDING)",
    }

def build_md(artifact: dict) -> str:
    display_names = {
        "identity": "identity",
        "archive_status": "archive status",
        "source_basis": "source basis",
        "authority_scope": "authority scope",
        "requested_action_scope": "requested action scope",
        "input_object_shape": "input object shape",
        "output_object_shape": "output object shape",
        "machine_action_scope": "machine action scope",
        "radius_discipline": "radius discipline",
        "validator_requirements": "validator requirements",
        "receipt_obligations": "receipt obligations",
        "halt_conditions": "halt conditions",
        "escalation_conditions": "escalation conditions",
        "freshness_rules": "freshness rules",
        "forbidden_authority_changes": "forbidden authority changes",
        "promotion_and_reuse_status": "promotion and reuse status",
        "revocation_and_expiry": "revocation and expiry",
        "readabout_projection_hooks": "Readabout projection hooks",
    }
    groups_md = "\n".join(f"- {display_names[g]}" for g in artifact["required_field_groups"])

    return f"""# Validator archive entry schema contract v0

## Status

{artifact["contract_status"]}

## Role

ARCHIVE_ENTRY_CONTRACT_ONLY

This artifact defines the required contract for future validator archive entries.

## It does not

- create an archive entry
- create a candidate entry
- grant promotion
- authorize reuse
- activate an archive entry
- allow auto-disposition
- create runner authority
- create an active validator archive entry

## Required field groups

{groups_md}

## Core laws

A local specimen is not reusable authority.

A candidate entry is not reusable authority.

A schema contract is not schema authorization.

Reuse requires explicit promotion and declared scope.

Activation requires explicit activation.

Preapproved inactive does not mean active.
"""

def validate(artifact: dict, md: str) -> None:
    failures: list[str] = []

    if artifact.get("required_field_groups") != REQUIRED_GROUPS:
        failures.append("ARCHIVE_SCHEMA_FAIL_REQUIRED_FIELD_GROUP_LIST_SHAPE")
    if len(artifact.get("field_group_contracts", [])) != 18:
        failures.append("ARCHIVE_SCHEMA_FAIL_FIELD_GROUP_CONTRACT_COUNT")
    ids = [g.get("group_id") for g in artifact.get("field_group_contracts", [])]
    if ids != REQUIRED_GROUPS:
        failures.append("ARCHIVE_SCHEMA_FAIL_FIELD_GROUP_CONTRACT_ORDER_OR_IDS")
    for rec in artifact.get("field_group_contracts", []):
        for key in [
            "group_id",
            "group_role",
            "required_fields",
            "required_value_policy",
            "missing_field_halt",
            "non_impersonation",
        ]:
            if key not in rec:
                failures.append(f"ARCHIVE_SCHEMA_FAIL_GROUP_KEY_MISSING:{rec.get('group_id')}:{key}")
        if rec.get("required_value_policy") != "MUST_BE_EXPLICIT_NO_DEFAULT_INFERENCE":
            failures.append(f"ARCHIVE_SCHEMA_FAIL_GROUP_POLICY:{rec.get('group_id')}")

    forbidden_terms = [
        "c8.n22",
        "C8_N22",
        "AUTH_STATE_ACCEPTED_AS_BASIS_FOR_NEXT_UNIT_DEFINITION",
        "PREPARE_NEXT_BOUNDED_UNIT_DEFINITION_SURFACE",
        "ROUTE_MACHINE_MAY_PREPARE_ONLY",
    ]
    blob = json.dumps(artifact, sort_keys=True) + "\n" + md
    for term in forbidden_terms:
        if term in blob:
            failures.append(f"ARCHIVE_SCHEMA_FAIL_INSTANCE_VALUE_INSERTED:{term}")

    if "A schema contract is not schema authorization." not in md:
        failures.append("ARCHIVE_SCHEMA_FAIL_MARKDOWN_JSON_PARITY")
    if "Preapproved inactive does not mean active." not in md:
        failures.append("ARCHIVE_SCHEMA_FAIL_MARKDOWN_JSON_PARITY")

    if failures:
        print(json.dumps({"archive_schema_gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        raise SystemExit(1)

def main() -> None:
    artifact = build_artifact()
    md = build_md(artifact)
    validate(artifact, md)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text(md)

    gate = artifact["contract_gate"]
    print("BUILD_VALIDATOR_ARCHIVE_ENTRY_SCHEMA_CONTRACT_V0_COMPLETE")
    print("archive_schema_contract_id=validator_archive_entry_schema_contract.v0")
    print("schema_version=matrixlabs_validator_archive_entry_schema_contract_v0")
    print("contract_role=ARCHIVE_ENTRY_CONTRACT_ONLY")
    print("contract_status=ARCHIVE_SCHEMA_PASS_CONTRACT_DEFINED")
    print("archive_entry_creation_status=NO_ARCHIVE_ENTRY_CREATED_BY_CONTRACT")
    print("candidate_entry_creation_status=NO_CANDIDATE_ENTRY_CREATED_BY_CONTRACT")
    print("promotion_status=PROMOTION_NOT_GRANTED_BY_CONTRACT")
    print("reuse_authority_status=REUSE_AUTHORITY_NOT_GRANTED_BY_CONTRACT")
    print("activation_status=ACTIVATION_NOT_APPLICABLE_TO_CONTRACT")
    print("auto_disposition_status=AUTO_DISPOSITION_NOT_ALLOWED_BY_CONTRACT")
    print("runner_authority_status=RUNNER_AUTHORITY_NOT_CREATED_BY_CONTRACT")
    print("required_field_group_count=18")
    print("required_field_groups_present=true")
    for gid in REQUIRED_GROUPS:
        print(f"{gid}_group_present=true")
    print("schema_contract_does_not_create_entry=true")
    print("schema_contract_does_not_create_candidate=true")
    print("archive_entry_status_does_not_imply_reuse_authority=true")
    print("promotion_status_does_not_imply_activation_status=true")
    print("candidate_source_specimen_is_not_sufficient_for_active_reuse=true")
    print("preapproved_inactive_entry_is_not_active=true")
    print("no_receipt_obligations_no_preapproval=true")
    print("no_implicit_radius_expansion=true")
    print("no_forever_by_omission=true")
    print("readabout_projection_is_downstream_only=true")
    print("creates_archive_entry=false")
    print("creates_candidate_entry=false")
    print("grants_promotion=false")
    print("grants_reuse_authority=false")
    print("creates_active_entry=false")
    print("allows_auto_disposition=false")
    print("creates_runner_authority=false")
    print(f"archive_schema_gate={gate['archive_schema_gate']}")
    print("archive_entry_created=false")
    print("candidate_entry_created=false")
    print("reuse_authority_granted=false")
    print("promotion_granted=false")
    print("active_archive_entry_created=false")
    print("auto_disposition_allowed=false")
    print("runner_authority_created=false")
    print("c2_created=false")
    print("c3_created=false")
    print("promotion_receipt_created=false")
    print("activation_object_created=false")
    print("next_unit_defined=false")
    print("next_unit_authorized=false")
    print("next_unit_definition_surface_prepared=false")
    print("observed_path_updated=false")
    print("observed_path_update_proposed=false")
    print("commit_created=false")
    print("push_executed=false")
    print("terminal_transition=ADVANCE(C2_VALIDATOR_ARCHIVE_CANDIDATE_ENTRY_PENDING)")

if __name__ == "__main__":
    main()
