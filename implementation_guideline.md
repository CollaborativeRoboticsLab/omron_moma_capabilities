# Implementation handoff for GPT Luna

This is a future implementation task, not authorization to change code now.
Start with `proposed_changes.md` and `ToDo` in this directory; inspect current
worktree state and the actual source before editing. Use
`omron_amr_capabilities` as the ground truth for the new capability format.
Update all workspace capability interfaces, providers and semantic interfaces
to that format, including exported definitions outside `*_capabilities`
packages. Verify runtime contracts against the deployed robot and current
Fabric and Capabilities2 APIs before applying them elsewhere.

## Order of work

1. Discover every workspace package exporting capability specifications and
   inventory package versions, all interfaces, providers, semantic interfaces,
   existing launch providers, disabled dependencies, and user
   changes. Map each plan and dependency to an installed specification. Use
   AMR plans 5-7 and the supported Fabric generation contract to reconcile
   obsolete examples, preserving task, UUID and `flush` behavior; document
   that generated plans are automatically queued without a review pause.
2. Design managed and external runtime ownership for Nav2 and perception.
   Existing Nav2/perception dependencies are already present in provider YAML;
   verify actual behavior before changing them. Enable any genuinely disabled
   applicable launch runners through the existing Capabilities2 launch proxy.
   Verify launch parameters, endpoint readiness, startup failure, reference
   sharing, cancellation and ownership of externally managed stacks.
3. Agree on robot-specific map, sensor configuration and safe lifecycle behavior
   before launching hardware. Ask the user when the configuration or required
   selection cannot be established. Never start a second navigation/perception
   stack merely to satisfy a dependency; never treat process startup as service
   readiness without testing the actual contract.
4. Keep MoMa semantic interfaces on their generic base interfaces until the
   planned cascading semantic inheritance is implemented and validated. Audit
   remaining interfaces, providers and semantics against the reference format,
   as specified in `proposed_changes.md`. Record conforming definitions and blockers. Add a new
   specialization only for a verified robot-specific contract, without
   duplicating the AMR launch or assuming its hardware configuration applies to
   other robots. Verify the current loader's registration/install rules and the
   base interface for each specialization. Verify descriptions and remappings
   against real robot configuration. Account for generic runnable descriptors
   being suppressed
   when semantic interfaces exist, direct-provider precedence, and the known
   unfinished context-aware provider selection. Preserve generic and
   multi-robot examples through an explicit tested migration strategy; stop and
   request a decision if compatibility cannot be ensured.
5. Audit remaining launch wrappers, defaults and dependency manifests against
   the supported Fabric launch arguments. Check all shipped plan XML and
   reconcile plan/API documentation. Add or document a generic
   mobile-manipulator plan entry point without moving robot policy into generic
   capability adapters.
6. Correct Omron documentation and examples only against verified robot
   configuration. Preserve scene management, arm-only and mobile-manipulator
   ownership boundaries. Do not invent poses, limits, frames or motion approval.
7. Update documentation and `ToDo` based on actual completion, not intentions;
   leave policy decisions and hardware validation unchecked until demonstrated.

## Required verification

* Verify discovery, registration and format coverage for every exported
   capability, including packages outside `*_capabilities`; report each
   migrated, already-conforming or blocked definition.
* Parse every shipped example XML and check runner interface/provider
   availability against the real capability discovery mechanism. Add regression
   coverage for shipped plans and any changed default plan.
* Add targeted tests for managed/external mode selection, readiness and timeouts,
  dependency sharing and teardown, process failure, and duplicate-start
  avoidance. Exercise actual launch-proxy behavior where possible.
* Test semantic interface discovery and installation, remappings, explicit and
  generated provider selection, generic plan compatibility, simultaneous robot
  registrations, and conflicts/rollback across shared launch dependencies.
* Check launch argument forwarding and file installation; test defaults and
  overrides. Validate generative task/context/UUID and `flush` semantics with
  mocks or configured services; assert generated plans are queued once.
* Run targeted tests and `colcon build`/`colcon test` for affected packages and
  their necessary dependencies. Run non-motion simulation integration before any
  approved hardware test. Report exact commands, outcomes, missing dependencies,
  and every skipped/unavailable test.
* Do not commit credentials or depend on real API keys in tests. Do not send
  robot motion goals without separate user approval and verified safe setup.

## Review handoff

Provide a concise list of changed files and behavior, design decisions and their
evidence, tests and results, remaining risks, and a clear statement about
whether any robot or real services were used. Preserve unrelated work and do not
mark unverified items complete. Stop after implementation and testing so the
requesting assistant can review; do not self-approve the change.
