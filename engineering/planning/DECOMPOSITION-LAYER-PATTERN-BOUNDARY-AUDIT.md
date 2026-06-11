# Pattern-Boundary Audit — Decomposition Layer vs. the Spin2 Pattern Library

**Sprint:** Decomposition Reasoning Layer (KB v1.7.0) · **Plan §14 (task #19)**
**Date:** 2026-06-11
**Scope:** Reconcile the new `architecture/decomposition/` guidance layer against the
existing `language/spin2/patterns/` library (43 patterns), in BOTH directions. This is
distinct from the 8 `architecture/patterns-analysis/` files (handled in §15 supersession).

**Output of this audit:** every pattern classified (cross-link / new-candidate / leave /
supersede-retag); cross-link actions feed §16 (task #21); new-pattern candidates are a
**scope decision for Stephen** (this sprint does NOT author new patterns silently).

---

## Classification key

- **cross-link** — the force/lens points INTO this pattern as concrete vocabulary; wire a
  `see_also` from the new entry, and (where the pattern is a primary landing spot) a
  reverse `see_also` from the pattern back to the layer.
- **new-candidate** — a force implies a pattern the library lacks cleanly; flag for
  Stephen, do not author this sprint.
- **leave** — a domain/application template or low-level implementation detail with no
  direct decomposition-force relationship; no action.
- **supersede / retag** — handled in §15 supersession (task #20); listed here for
  completeness.

---

## A. Implementation patterns (15)

| Pattern | Force / lens | Classification | Note |
|---------|--------------|----------------|------|
| `spin2_mailbox_communication` | Force 2 (control plane) | **supersede** (§15) | Blocking `repeat while` toy; add `superseded_by` → data-flow-contracts; keep resolving. |
| `spin2_buffer_management` | Force 3a + data plane | **cross-link** | The ring buffer the rate-domain decoupler uses when every sample matters. |
| `spin2_shared_memory` | Force 2 (control plane) | **cross-link** | Shared structures + atomicity discipline; the value-connascence case. |
| `spin2_event_dispatcher` | Force 2 (event plane) | **cross-link** | Event-plane signalling/dispatch. |
| `spin2_cog_management` | Force 1 + C5 | **cross-link** | Cog lifecycle / launch order — resource ownership + lifecycle. |
| `spin2_layered_architecture` | Force 4 (altitude) | **cross-link (primary)** | The existing pattern the altitude-layering force factors into; reverse-link it. |
| `spin2_timing_control` | Force 3 | **cross-link** | Precise timing / cadence control. |
| `spin2_protocol_implementation` | spatial-computing (edge) | **cross-link** | Bit-bang-vs-absorb decision; the "bit-banging an absorbable protocol" smell. |
| `spin2_pin_control` | spatial-computing (edge) | **cross-link** | Push computation to the smart-pin edge. |
| `spin2_resource_pool` | resource-budget | **cross-link (light)** | Pooling finite resources; budget discipline. |
| `spin2_state_machine` | Force 2 (control plane) | **leave** | Implementation idiom; tangential to the cut. (Optional light link only.) |
| `spin2_error_handling` | C1 (safety) | **leave** | Light relation to fault containment; not a decomposition driver. |
| `spin2_diagnostic_output` | C4 (testability) | **leave** | Light relation to bring-up; not a decomposition driver. |
| `spin2_memory_allocation` | — | **leave** | Hub memory mechanics; no force relationship. |
| `spin2_plugin_system` | — | **leave** | Extensibility idiom; out of scope. |

## B. Structural patterns (6)

| Pattern | Force / lens | Classification | Note |
|---------|--------------|----------------|------|
| `few_objects` | (count taxonomy) | **supersede / retag** (§15) | Count predicts nothing; retag toward depth + ownership; redirect. |
| `several_objects` | (count taxonomy) | **supersede / retag** (§15) | Same; this is the literal "flat device list" failure mode if taken at face value. |
| `framework_pattern` | Force 4 + C5 | **cross-link** | Layered orchestrator-as-sequencer. |
| `single_object` | Force 1 (sole device) | **leave (light)** | Composition depth; reframed by altitude-layering but fine as-is. |
| `no_objects` | — | **leave** | Utility-library shape; no force relationship. |
| `no_objects_minimal` | — | **leave** | Same. |

## C. Application patterns (22) — domain templates

Most application templates are single-domain shapes that benefit only INDIRECTLY from the
layer; default is **leave**. The exceptions are the multi-cog / multi-device coordination
domains, where the decomposition method is directly load-bearing — **cross-link** these so
an agent building one discovers the method:

| Pattern | Classification | Note |
|---------|----------------|------|
| `robotics` | **cross-link** | The worked-derivation domain; agents here need the forces most. |
| `multi_motor_system` | **cross-link** | Multi-actuator coordination = Force 1 + Force 3. |
| `multi_instance_coordination` | **cross-link** | Singleton-vs-instance + data-flow contracts. |
| `sensor_fusion` | **cross-link** | Multi-rate sensor crossing = Force 3 + planes. |
| `array_architecture` | **cross-link** | Scalable multi-cog arrays = spatial-computing. |
| `dual_communication` | **cross-link (light)** | Two protocol owners = Force 1. |
| `animation_engine`, `audio_processor`, `communication_handler`, `configuration_manager`, `data_logger`, `debug_enabled`, `display_driver`, `hardware_specific_app`, `iot_device`, `monitoring_device`, `motor_controller`, `multi_display_system`, `multimedia_device`, `sensor_reader`, `single_communication`, `test_harness`, `utility_library` | **leave** | Single-domain templates; no direct force cross-link this pass. |

**All 43 patterns classified — audit complete (no pattern left unclassified).**

---

## D. New-pattern candidates (SCOPE DECISION FOR STEPHEN — not authored this sprint)

Each names the force that implies it. The library has no clean home for these:

1. **Latest-wins command mailbox with seq/ack handshake** — *implied by Force 2 (control
   plane).* The library has a blocking mailbox (superseded) and a generic ring buffer, but
   not the non-blocking, args-first / seq-bumped-last contract a real-time loop requires.
2. **Rate-domain decoupler / latest-value sampler** — *implied by Force 3a.* Distinct from
   `spin2_buffer_management` (which keeps every sample); this keeps only the freshest.
3. **Slew / easing engine (discrete → continuous trajectory)** — *implied by Force 3b.*
   Nothing in the library turns a step command into a rate-limited trajectory.
4. **In-cog cooperative tasks (one bus, many cadences)** — *implied by the Force 1 × Force
   3 tension.* The library has no pattern for multiple coroutines sharing one cog and one
   bus at different cadences.

**Recommendation:** these four are genuinely missing and genuinely useful. Propose
authoring them as a follow-on `language/spin2/patterns/implementation/` effort AFTER the
guidance layer ships — the layer's force entries already teach the reasoning; these would
give the concrete code skeletons. Flagging, not authoring, per plan §14.

---

## E. Cross-link wiring worklist (feeds §16 / task #21)

**Outbound** (already present in the authored entries' `see_also` as architecture facts;
add pattern `related:` where the file exists):
- `data-flow-contracts` → `spin2_buffer_management`, `spin2_shared_memory`, `spin2_event_dispatcher`
- `rate-adaptation` → `spin2_buffer_management`, `spin2_timing_control`
- `altitude-layering` → `spin2_layered_architecture`, `framework_pattern`
- `resource-ownership` → `spin2_cog_management`
- `spatial-computing` → `spin2_protocol_implementation`, `spin2_pin_control`
- `resource-budget` → `spin2_resource_pool`

**Inbound** (add a `see_also` to the layer FROM the existing tree — the two altitudes with
the gap between them, plus the primary pattern landing spots):
- `concepts/object_archetypes.yaml` → `p2kbArchDecompositionMethod` (the grammar that derives the archetypes)
- `architecture/p2-architecture-mental-model.yaml` → `p2kbArchDecompositionMethod`
- `implementation/spin2_layered_architecture.yaml` → `p2kbArchAltitudeLayering`
- `implementation/spin2_mailbox_communication.yaml` → `p2kbArchDataFlowContracts` (via the §15 supersede link)
- `structural/framework_pattern.yaml` → `p2kbArchDecompositionMethod`
- `applications/robotics.yaml` → `p2kbArchWorkedDerivationRobotDog`
