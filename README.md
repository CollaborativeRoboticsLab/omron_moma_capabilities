# omron_moma_capabilities

Omron-specific capability plans and launch wrappers for standalone stack testing.

## Purpose

This package currently packages example plans for the Omron MOMA setup without inheriting from `mobile_manipulator` or `mobile_manipulator_capabilities`.

The current goal is to validate the lower-level stacks separately:

- `nav2_capabilities` plans for base-only navigation
- `grasping_capabilities` plans for arm-only MoveIt and grasping actions
- `gripper_capabilities` plans for isolated gripper command testing

## Ownership Boundary

- `grasping` owns active scene management, MoveIt planning-scene updates, arm-only feasibility, and arm execution
- `nav2` owns base-only waypoint execution
- `gripper` owns isolated gripper command execution
- `omron_moma_capabilities` owns Omron-facing example plans plus simple launch wrappers for separate stack testing

For now this package intentionally does not compose the generic mobile-manipulator stack. It is a thin plan-and-launch package for validating the individual capability packages in isolation.

## Plan Groups

| Group | Plans | Purpose |
| --- | --- | --- |
| Grasping | `moma_grasp_1.xml` to `moma_grasp_4.xml` | Cartesian, joint-space, and named-pose arm motion through `grasping_capabilities`. |
| Nav2 | `moma_nav2_1.xml`, `moma_nav2_2.xml` | Base-only waypoint navigation through `nav2_capabilities`. |
| Gripper | `moma_gripper_1.xml`, `moma_gripper_2.xml` | Standalone gripper open/close tests through `gripper_capabilities`. |

Default standalone plans are recorded in [config/standalone_test_config.json](./config/standalone_test_config.json).

## Launch Files

- `system.launch.py`: generic wrapper that runs any plan in this package through `fabric_server`
- `grasping.launch.py`: defaults to `moma_grasp_1.xml`
- `nav2.launch.py`: defaults to `moma_nav2_1.xml`
- `gripper.launch.py`: defaults to `moma_gripper_1.xml`

## Build

```bash
cd ~/colcon_ws
colcon build --packages-up-to omron_moma_capabilities --symlink-install
```

## Runtime

Start the capabilities server and whichever underlying runtime stack you want to test, then launch the matching plan wrapper.

Grasping example:

```bash
source install/setup.bash
ros2 launch capabilities2_server capabilities2_server.launch.py
```

```bash
source install/setup.bash
ros2 launch omron_moma_capabilities grasping.launch.py
```

Nav2 example:

```bash
source install/setup.bash
ros2 launch omron_moma_capabilities nav2.launch.py
```

Gripper example:

```bash
source install/setup.bash
ros2 launch omron_moma_capabilities gripper.launch.py
```

Override the plan file with `filename:=...` when you want to run a different example from the same group.

For more detail, see [docs/standalone_testing.md](./docs/standalone_testing.md).