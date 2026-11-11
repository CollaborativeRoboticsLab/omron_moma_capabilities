# Capability package alignment: proposed changes

Status: remaining work and future planning. Align capabilities in the workspace
with the format already used by `omron_amr_capabilities`, the reference.
This covers every capability interface, provider and semantic interface, not
just Omron-specific packages. Check runtime contracts against the deployed
robots and current Fabric and Capabilities2 APIs; the reference format is not
evidence of hardware validation or multi-robot compatibility. MoMa currently
redefines generic interfaces directly. The latest focused MoMa build was blocked
by missing installed mobile-manipulator and grasping dependencies. Paths below
are relative to `src/` unless otherwise stated.

## Next: Cascading Semantic Interfaces

Plan a Capabilities2 change that allows a semantic interface to redefine
another semantic interface. The intended chains are generic Nav2 -> Omron AMR
-> Omron MoMa, generic gripper -> Omron gripper -> Omron MoMa, and generic
grasping -> TMR grasping -> Omron MoMa. Omron MoMa also specializes the generic
mobile-manipulator interfaces. Dependencies must point from child to parent;
parent packages must not depend on or reference MoMa.

Today the semantic `redefines` database foreign key points only to ordinary
interfaces, and remapping and provider lookup resolve at most one semantic
level. The current MoMa semantics therefore redefine generic interfaces
directly; the package dependency graph is not recursive semantic inheritance.

* Design schema and existing-database migration for generic or semantic parents,
  deferred loading, missing parents, and cycle rejection.
* Resolve the full inheritance chain and define remapping and namespace ordering.
* Define and test direct versus inherited provider precedence, runnable
  discovery, generic-plan compatibility, and managed/external launch ownership
  without starting duplicate stacks or selecting the wrong robot.
* Add regression tests for multi-level inheritance, load order, migration,
  missing parents, cycles, remappings, provider selection, simultaneous robot
  registrations, and existing single-level behavior.
* After the loader and compatibility tests pass, update MoMa semantic
  `redefines` targets to the corresponding AMR, Omron gripper, and TMR semantic
  interfaces; retain generic mobile-manipulator parents. Verify discovery,
  exports, plans, and non-motion integration before any approved robot use.

## AMR Reference And Alignment Scope

* `omron_amr_capabilities/semantic_interfaces/AMRWaypointRunner.yaml` and
  `AMRRobotposeRunner.yaml` redefine the generic Nav2 waypoint and robot-pose
  interfaces. Their matching providers implement those semantic interfaces and
  share the generic `nav2_capabilities/Nav2LaunchRunner` dependency using
  `omron_amr_capabilities/AMRNav2LaunchRunner`.
* The AMR launch provider implements the generic Nav2 launch interface and
  starts `amr_ros/ld250.launch.py`, with RViz disabled and an empty namespace.
  It waits for `planner_server`, `bt_navigator` and the `navigate_to_pose`
  action, each with a 60-second timeout. The launch owns the LD250 hardware
  interface and Nav2 with online SLAM by default. The package exports two
  semantic interfaces and three providers, not a separate AMR launch interface
  or perception provider.
* Discover all workspace packages exporting capability specifications, including
  definitions in packages not named `*_capabilities` such as
  `capabilities2/capabilities2_runner`. Inventory every interface, provider and
  semantic interface, and map each plan reference and dependency to its actual
  exported specification. Migrate each definition that does not already follow
  the AMR reference format, including applicable spec version, registration,
  installation, provider implementation, parameter metadata and dependency
  declarations. Record already-conforming definitions and any blockers; the
  package list below is a starting point, not an exhaustive scope limit.
  Keep MoMa semantics on generic bases for now; verify navigation provider
  selection and launch ownership without starting a duplicate driver.
  Align all other pairs with the same supported registration, naming,
  dependency and readiness conventions where applicable, while preserving each
  generic contract and verifying its own runtime, endpoints and safety limits.
  Do not rename unrelated generic capabilities or fabricate robot-specific
  semantics simply to match AMR names.
* The reference examples are `omron_amr_capabilities/plans/amr_1.xml` through
  `amr_7.xml`; plans 5-7 use the current `FabricGeneratePlanRunner`, which
  automatically queues its result. These are illustrative coordinates, not
  approved robot paths, and no review pause is implied.

## P0: Launch ownership and disabled launch runners

1. **Make launch-backed dependencies operational, without duplicate robot
   stacks.** `nav2_capabilities/providers/Nav2LaunchRunner.yaml` and
   `fp_perception_capabilities/providers/FpPerceptionLaunchRunner.yaml` already
   declare launch providers. The Nav2 `WaypointRunner` and `RobotPoseRunner`
   providers and all four perception runner providers already declare
   `depends_on`; none of those six dependencies is commented out. The
   `capabilities2_runner::LaunchRunner` plugin is registered and the current
   proxy lifecycle is documented in `capabilities2/docs/launch_system.md`.
   Therefore, do not claim these are disabled or simply uncomment them.
   Identify any actually disabled launch-backed providers/dependencies across
   all capability packages, and enable the applicable ones through the existing
   launch proxy. If a necessary provider is missing, design it against the
   owning runtime rather than inventing a launch path.
2. **Resolve external-versus-managed ownership before enabling automatic
  launches.** The AMR navigation provider starts the hardware and Nav2 stack
  together; it is not an external-stack mode. Generic Nav2 and perception
  providers also declare managed launches, with their own configuration. A
  second stack can conflict with existing nodes and use
   wrong sensors/maps. Design explicit, tested managed and external modes, with
   robot-specific configuration and clear start/stop ownership; do not silently
   start generic Nav2 or perception on live hardware. Determine whether semantic
   providers or another supported Capabilities2 mechanism are appropriate.
3. Configure and test readiness for the selected runtime, including timeout,
   startup failure, shared dependency lifetime, and cancellation. The supported
   `launch_readiness` schema has examples in
   `capabilities2/capabilities2_server/test/test_capabilities_server.cpp`.
   Verify actual endpoint names/types and ROS distribution before choosing
   checks. Update affected provider/interface specs, launch files, package
   dependencies, and docs together in the implementation phase.

## P0: Robot-specific semantic interfaces

MoMa currently has its own navigation semantics and providers that redefine
generic Nav2 interfaces; verify their behavior and interoperability with AMR.
Inventory and align the remaining interface, provider and semantic-interface
specifications across the affected packages as part of future implementation,
not in this planning-only change. Consider Omron-specific perception, arm,
gripper and mobile-manipulator runners used by example plans. Only add an
interface when it expresses a verified
robot-specific contract or remapping; avoid duplicating generic contracts
without meaningful semantics. Confirm deployed frames, endpoints, names,
limits and namespaces rather than guessing.

Use the supported `spec_type: semantic_interface` / `redefines` format in
`capabilities2/docs/semantic_interfaces.md`; install and register the files
using the mechanism actually supported by the current loader (compare
`capabilities2/capabilities2_server/docs/register.md` with the loader).
Pair each semantic interface with a compatible provider; where launch ownership
differs, provide an explicitly compatible robot-specific provider and dependency
instead of assuming remappings alone control process startup. Update example
plans, package dependencies and documentation to use the chosen pairings.

**Compatibility gate:** `capabilities2/capabilities2_server/readme.md` says
registering a semantic interface suppresses generic runnable descriptors for
its base interface and direct semantic providers take precedence;
`capabilities2/TODO.md` flags context-aware selection and dependency conflicts
as unfinished. Test discovery and validation of all affected generic and
robot-specific plans in the same workspace, with both robots' interfaces
installed. Decide the migration/selection strategy before registering
interfaces globally; do not silently make existing examples unavailable or
launch the wrong robot's stack. Test generated-plan selection, explicit
providers, lifecycle and rollback, and document any unresolved limitations.

## P1: Shared launch wrappers and documentation

* Audit remaining launch wrappers and documentation against the current Fabric
  arguments and default plans. MoMa and Nav2 wrappers already forward the config,
  prompt-tools and launch-proxy options; the generic grasping and gripper
  packages no longer own system wrappers. Fabric Experience is configured by
  `experience.enabled`; do not advertise an unsupported launch switch. Avoid
  restarting servers already started by Fabric's launch.
* `mobile_manipulator_capabilities` has example plans but no launch wrapper.
  Decide whether to add one consistent with its generic ownership boundary or
  document an existing supported way to execute the installed plans. Do not
  create a new robot runtime in this adapter package.
* Audit every capability-exporting package's `package.xml`/`CMakeLists.txt` for dependencies and
  installation of actual launch, plan and provider assets. Add only needed
  dependencies; avoid dependency cycles.

## P1: Plan and interface consistency

* Add a regression check for all shipped plan XML and capability references.
* Use AMR plans 5-7 and the currently supported Fabric generation contract as
  the reference when reconciling obsolete generative examples in other packages.
  Preserve each task, context UUID and `flush` behavior; validate capability
  discovery and generation end-to-end. `FabricGeneratePlanRunner` automatically
  queues its result, so do not imply that it provides an approval pause.
* Audit Fabric interface documentation against the current API;
  `prompt_capabilities/docs/interface.md` still documents `PromptCapabilityRunner`
  and `PromptPlanRunner`. Check documented runner commands against providers.
* `nav2_capabilities/README.md` describes waypoint following, but
  `include/nav2_capabilities/waypoint_runner.hpp` uses
  `/navigate_to_pose` (`NavigateToPose`), hard-coded `map`. Correct the
  documentation and validate frame assumptions for each robot.

## P1: Omron integration

* Verify the Omron README's runtime prerequisites and repair its remaining
  `docs/standalone_testing.md` link. Do not separately start a capabilities
  server already started by Fabric's launch.
* `plans/moma_grasp_2.xml` now uses `joint_1` through `joint_6`; confirm the
  deployed Omron URDF, prefix, planning group and safe joint values before use.
  Likewise validate named poses, Cartesian frame, gripper limits and navigation
  coordinates against the actual robot; do not infer safe motion values.
* `moma_generative_2.xml` through `moma_generative_5.xml` currently repeat the
  same task. Decide and document distinct useful examples or explicitly retain
  duplicates; do not invent hardware behavior. Validate the existing
  mobile-manipulator feasibility/search/execute examples against their interfaces
  and the approved-base-pose policy before use.

## Per-package review summary

| Package | Result and planned focus |
| --- | --- |
| `omron_amr_capabilities` | Ground-truth AMR navigation definitions and plans; validate launch ownership, readiness and shared discovery before reuse. |
| `capabilities2_runner` and any other capability-exporting workspace packages | Inventory and migrate all exported specifications to the reference format, preserving their actual runtime contracts. |
| `turtlebot_capabilities` | If present, reconcile its contracts and examples with current APIs without substituting AMR hardware assumptions. |
| `nav2_capabilities` | Launch ownership/readiness, wrapper, dependency and accurate action/frame docs. |
| `fp_perception_capabilities` | Launch ownership/config/readiness, wrapper and duplicate-server docs. |
| `fabric_capabilities` | Audit current generation interface docs, examples and wrapper arguments. |
| `prompt_capabilities` | Stale removed-runner docs and wrapper arguments; preserve current prompt contracts. |
| `grasping_capabilities` | Generic interfaces/providers and arm/scene ownership; verify plan references in specialized packages. |
| `gripper_capabilities` | Generic interfaces/providers; validate robot-specific command limits separately. |
| `mobile_manipulator_capabilities` | Plan execution entry point and generic adapter validation; no Omron policy inside adapters. |
| `omron_moma_capabilities` | Correct launch/docs, robot-specific plans, dependencies and coordinated examples. |

## Validation and decisions

For every discovered capability, record its old and new format, exported files,
provider pairing, dependent plans and validation outcome; report any skipped
definitions and blockers. Before implementation choose the managed/external stack selection and verify
deployed robot configuration and semantic-interface compatibility strategy;
request user input if these cannot be inferred safely. Run XML parsing and
runner-reference checks for all plan files, targeted
unit/launch tests, affected `colcon build` and `colcon test` packages, and
simulation integration for lifecycle and readiness. Verify generation with
mocked or configured services and UUID context. Hardware motion is a separate,
explicitly approved step after non-motion checks; record unavailable tests and
do not report them as passed. See `implementation_guideline.md` and `ToDo`.