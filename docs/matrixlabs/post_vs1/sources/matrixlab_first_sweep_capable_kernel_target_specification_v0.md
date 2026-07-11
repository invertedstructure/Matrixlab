# MatrixLab First Sweep-Capable Kernel Target Specification v0

## 1. Status

**Specification status:** DIRECTIONAL TARGET DEFINITION  
**Implementation status:** NOT IMPLEMENTED  
**Execution authority:** NOT GRANTED  
**Runner authority:** NOT CREATED  
**Target selection status:** PROVISIONALLY SELECTED FOR FURTHER TIGHTENING

This specification defines the preferred first operational target for the MatrixLab sweep-capable kernel.

It does not define the final implementation, authorize execution, create a runner, select concrete schemas, or claim readiness for sweeps.

---

## 2. Strategic Objective

MatrixLab should transition as early as lawfully possible from architecture-led construction to evidence-led iteration.

The desired operational cycle is:

```text
declare bounded target
→ execute bounded run or sweep
→ emit receipts
→ produce run report
→ identify smallest load-bearing deficiency
→ refine that deficiency
→ rerun
````

Infrastructure should be built only where it is required to make the next informative run lawful, bounded, inspectable, and diagnostically useful.

The system should not attempt to complete every abstract architecture surface before beginning bounded execution.

---

## 3. Immediate Milestone

The next practical milestone is:

# First Sweep-Capable Kernel v0

Its purpose is to establish the smallest closed execution circuit capable of:

1. receiving a declared target;
2. operating on a typed state;
3. selecting from an explicit lawful move-space;
4. applying one bounded move at a time;
5. validating the resulting state;
6. halting under explicit conditions;
7. emitting move-level and run-level receipts;
8. sweeping across a small declared variation set;
9. reporting what held, progressed, stopped, failed, or became unavailable;
10. exposing the smallest next refinement required.

The milestone is achieved when this circuit can run against one narrow target and produce useful Confirmation Yield or Diagnostic Yield.

---

## 4. Selected First Target Family

The recommended first target family is:

# Bounded Contract Convergence

The kernel receives one bounded candidate contract and attempts to reach a declared locally valid and lawfully admissible terminal contract within a fixed move budget.

If the target cannot lawfully be reached, the kernel must halt with a typed explanation identifying the exact blocking condition.

The target is not unrestricted contract generation.

The target is:

```text
bounded candidate contract
→ lawful bounded transformation
→ validation and admissibility check
→ terminal contract or typed stop
```

---

## 5. First Concrete Target

The first concrete target should be:

# Typed State Contract Convergence v0

### Target statement

Given:

* one bounded typed-state contract candidate;
* one frozen local target schema;
* one explicit admissibility policy;
* one finite move-space;
* one fixed move budget;
* one declared source set;

attempt to transform the candidate into a locally valid and lawfully admissible typed-state contract.

The run must terminate in exactly one of the following outcome classes:

```text
TARGET_REACHED
TYPED_STOP_REPAIR_NOT_LAWFUL
TYPED_STOP_MISSING_SOURCE
TYPED_STOP_MISSING_SCHEMA
TYPED_STOP_MISSING_AUTHORITY
TYPED_STOP_MISSING_CAPABILITY
TYPED_STOP_RADIUS_EXHAUSTED
TYPED_STOP_NO_ADMISSIBLE_MOVE
TYPED_STOP_VALIDATION_FAILED
TYPED_STOP_UNCLASSIFIED_RESULT
```

The final outcome vocabulary may be refined during implementation design, but every unsuccessful terminal state must remain typed and diagnostically useful.

---

## 6. Why This Target Comes First

The typed-state contract is selected because it provides a narrow, mechanically inspectable target with limited domain ambiguity.

It forces the kernel to establish the minimum required distinctions:

```text
current state
target state
valid state
admissible state
available move
lawful move
applied move
rejected move
repairable defect
authority boundary
capability boundary
terminal condition
```

It also supports controlled perturbations with clear expected outcomes.

The first target should make failures in the kernel distinguishable from failures in an external problem domain.

---

## 7. Required Initial State Shape

The minimum run state should conceptually contain:

```text
run identity
target identity
current candidate object
target contract reference
source bindings
validation status
admissibility status
remaining move budget
applied move history
typed stop state
receipt references
```

This is a conceptual requirement only.

The exact schema, field names, serialization format, and versioning rules remain to be defined in the implementation layer.

---

## 8. Required Initial Move-Space

The first move-space must be finite, explicit, and locally authorized.

Candidate move classes include:

```text
ADD_AUTHORIZED_REQUIRED_FIELD
NORMALIZE_TYPED_VALUE
BIND_SOURCE_IDENTITY
BIND_SOURCE_FRESHNESS
REMOVE_FORBIDDEN_EFFECT
TIGHTEN_AMBIGUOUS_BOUNDARY
SPLIT_CONFLATED_FIELD
REJECT_UNSUPPORTED_CLAIM
MARK_MISSING_SOURCE
MARK_MISSING_SCHEMA
MARK_MISSING_AUTHORITY
MARK_MISSING_CAPABILITY
HALT_NO_ADMISSIBLE_MOVE
```

The exact move set is not fixed by this specification.

Implementation tightening must determine:

* which moves are genuinely required;
* which moves are transformations;
* which moves are classifications;
* which moves are terminal stops;
* which moves require separate authority;
* which moves must never be automatically selected.

No move may silently invent source material, authority, schemas, capabilities, or semantic content.

---

## 9. Minimal Controlled Step

Each loop step should have the following abstract form:

```text
inspect current state
→ identify currently exposed condition
→ enumerate admissible moves
→ select one move
→ verify authority and bounds
→ apply move or typed-stop
→ validate resulting state
→ emit receipt
→ test terminal condition
→ repeat or halt
```

A selector must not directly mutate state.

An applicator must not choose its own move.

Validation must not silently repair the object.

A typed stop must not be converted into automatic continuation.

---

## 10. First Positive-Path Target

The first positive-path specimen should contain one incomplete but lawfully repairable typed-state contract.

The initial candidate should require a small number of explicit moves, preferably between one and five.

A successful run should demonstrate:

```text
candidate accepted as input
required defects identified
lawful moves selected
moves applied within budget
receipts emitted for each decision edge
terminal contract validated
admissibility confirmed
TARGET_REACHED emitted
```

Success applies only to the bounded specimen and declared target contract.

It does not establish general convergence, portability, reusable schema authority, or runner readiness.

---

## 11. First Controlled Sweep

After the positive path works, the same target should be tested across a small perturbation set.

Candidate perturbation classes include:

```text
missing required field
invalid typed value
missing source identity
stale source binding
unsupported semantic claim
authority overreach
forbidden effect
conflated fields
missing halt obligation
missing receipt obligation
missing target schema
unrepairable capability gap
ambiguous move effect
```

Each case must declare:

* what was changed;
* which outcome class is expected;
* whether repair is lawful;
* whether authority is required;
* whether a capability boundary should be exposed;
* which evidence must appear in the receipts.

The first sweep should remain small.

A provisional initial range is:

```text
cases: 8–20
maximum moves per case: 3–5
target family count: 1
hidden continuation: forbidden
automatic schema invention: forbidden
automatic authority expansion: forbidden
```

The exact bounds remain implementation decisions.

---

## 12. Sweep Objective

The first sweep is not an optimization exercise.

Its purpose is to determine whether the kernel can distinguish among:

```text
valid and complete
invalid but lawfully repairable
invalid and not lawfully repairable
missing source
missing schema
missing authority
missing capability
radius exhausted
no admissible move
unexpected or unclassified result
```

The system should be evaluated primarily on distinguishability and Evidence Yield, not raw success count.

A correct typed stop may be more valuable than an unjustified successful transformation.

---

## 13. Receipt Obligations

Every attempted move must emit enough evidence to reconstruct the relevant decision edge.

At minimum, each move receipt should be capable of establishing:

```text
which run and case produced it
which state version was inspected
which condition was exposed
which moves were considered
which move was selected
why the move was admissible
which authority permitted it
which bounds remained
whether application occurred
what state delta resulted
which validation was performed
whether the target was reached
why the loop repeated or halted
```

Receipts should record load-bearing information only.

They should not indiscriminately expose every internal operation.

---

## 14. Run-Level Report

Each run or sweep must produce a report derived from the emitted receipts.

The report should answer:

```text
What target was attempted?
What cases were run?
What reached the target?
What stopped?
Why did each stopped case stop?
Which cases were repaired?
Which defects were not repairable?
Which authority boundaries were reached?
Which source or schema gaps were exposed?
Which outcomes were unclassified?
Which receipt fields proved useful?
Which receipt fields were insufficient?
What smallest refinement would enable the next informative run?
```

The report must distinguish:

```text
observed fact
derived classification
bounded interpretation
proposed next refinement
```

The report must not silently authorize the proposed refinement.

---

## 15. Evidence Yield

The first kernel should support two primary evidence branches.

### Confirmation Yield

Evidence obtained when the kernel correctly reaches or preserves a declared target condition.

Examples:

```text
lawfully repairable candidate reached terminal contract
already-valid candidate was preserved without unnecessary mutation
forbidden move was correctly excluded
move budget and stop rules were respected
```

### Diagnostic Yield

Evidence obtained when the kernel cannot reach the target but identifies the blocking condition precisely enough to guide the next refinement.

Examples:

```text
missing source identity exposed
authority boundary correctly reached
required schema absent
move vocabulary insufficient
receipt obligation inadequate
halt condition ambiguous
selector unable to distinguish two candidates
```

Evidence counts are descriptive.

Evidence value depends on whether the result changes or sharpens the next lawful decision.

---

## 16. First Portability Check

After the typed-state contract target is operational, the same kernel should be applied to a second bounded contract family:

# Move-Space Contract Convergence v0

The kernel should remain structurally unchanged where possible.

Only target-specific schemas, admissibility rules, and move parameters should vary.

The purpose is not to claim generalization.

The purpose is to establish a bounded portability statement such as:

```text
kernel held under typed-state contract target
kernel held with declared adaptations under move-space contract target
kernel failed under condition X
kernel required refinement Y
all other target families remain untested
```

---

## 17. Infrastructure Priority Rule

The kernel should not build machinery merely because the full MCCL architecture names it.

A new component or refinement should be introduced when at least one of the following is true:

```text
required for the next lawful run
required to preserve a load-bearing distinction
required to produce useful receipts
required to classify an observed stop
required to prevent an observed forbidden effect
required to make the target evaluable
required to make a prior result replayable or auditable
```

The following is insufficient justification by itself:

```text
architecturally elegant
possibly useful later
conventionally expected
desirable for completeness
helpful for presentation
```

---

## 18. Boundary Conditions

The first sweep-capable kernel must not imply or create:

```text
autonomous runner authority
unbounded iteration
automatic self-repair
automatic schema invention
automatic capability creation
automatic source acquisition
automatic authority escalation
reusable schema promotion
cross-domain generalization
performance optimization
global convergence claims
hidden continuation after typed stop
```

Local revision remains proposal-only unless a separate authority path explicitly permits application.

A successful bounded sweep does not authorize a larger sweep.

A valid contract in one target family does not become reusable authority for another family.

---

## 19. Completion Condition for This Milestone

The First Sweep-Capable Kernel v0 milestone is complete when:

1. one typed-state contract target is declared;
2. one finite move-space is declared;
3. one controlled move step is executable;
4. explicit validation and admissibility checks exist;
5. radius, budget, halt, and forbidden-effect rules exist;
6. move-level receipts are emitted;
7. one positive-path case reaches the target or correctly typed-stops;
8. one bounded perturbation sweep is executed;
9. one run-level report is produced;
10. the report identifies at least one evidence-backed next refinement or confirms that no refinement is yet required;
11. no execution exceeds the declared target, scope, authority, or bounds.

Completion does not require the full MCCL to be ready.

---

## 20. Immediate Tightening Sequence

This directional specification should next be tightened into the following implementation-facing objects:

```text
T1 — First target object definition
T2 — Typed-state candidate and terminal contract schemas
T3 — Run-state contract
T4 — Initial finite move-space
T5 — Selector contract
T6 — Applicator contract
T7 — Validation and admissibility boundary
T8 — Radius, budget, and halt policy
T9 — Move receipt contract
T10 — Run-level report contract
T11 — Positive-path specimen
T12 — Perturbation sweep fixture set
T13 — First-run readiness gate
```

These objects should be defined only to the depth required for the first bounded run.

---

## 21. Directional Decision

The provisional post-VS1 direction is:

```text
Build the smallest sweep-capable vertical kernel whose first target is
bounded typed-state contract convergence.

Use the resulting receipts and run report to determine the next refinement.

Then test the same kernel against a bounded move-space contract target.

Do not pre-commit to completing all later MCCL layers before running.
```

---

## 22. Directional Spine

```text
bounded target
→ typed state
→ explicit move-space
→ controlled move
→ validation/admissibility
→ receipt
→ repeat or typed halt
→ bounded sweep
→ run report
→ smallest evidence-backed refinement
→ rerun
```

This is the operational target toward which subsequent specifications should converge.
