# Omron Mobile Manipulator Capabilities

Omron MoMa specific capability plans and launch wrappers.

## Purpose

This package currently contains generative and non-generative execution plans for the Omron MOMA setup. It does not inherit from `mobile_manipulator` and assumes the robot is capable of using nav2 and moveit independently. 

The current plans utilize and builds on top of following capability packages:

- [nav2_capabilities](https://github.com/CollaborativeRoboticsLab/nav2_capabilities) plans for base-only navigation
- [grasping_capabilities](https://github.com/CollaborativeRoboticsLab/grasping_capabilities) plans for arm-only MoveIt and grasping actions
- [gripper_capabilities](https://github.com/CollaborativeRoboticsLab/gripper_capabilities) plans for isolated gripper command testing

## Ownership Boundary

- [grasping](https://github.com/CollaborativeRoboticsLab/grasping) owns active scene management, MoveIt planning-scene updates, arm-only feasibility, and arm execution.
- [gripper](https://github.com/CollaborativeRoboticsLab/grippers) owns isolated gripper command execution.
- [omron_moma](https://github.com/CollaborativeRoboticsLab/omron_moma) owns Omron MoMa specific Nav2 and MoveIt2 configuration and launch files.

## Plan Groups

| Group | Plans | Purpose |
| --- | --- | --- |
| Grasping | `moma_grasp_1.xml` to `moma_grasp_4.xml` | Cartesian, joint-space, and named-pose arm motion through `grasping_capabilities`. Uses non-generative execution plans. |
| Nav2 | `moma_nav2_1.xml`, `moma_nav2_2.xml` | Base-only waypoint navigation through `nav2_capabilities`. Uses non-generative execution plans. |
| Gripper | `moma_gripper_1.xml`, `moma_gripper_2.xml` | Standalone gripper open/close tests through `gripper_capabilities`. Uses non-generative execution plans. |
| Generative | `moma_generative_1.xml` to `moma_generative_2.xml` | Example generative execution plan for the Omron MoMa setup around both navigation and manipulation. Uses generative execution plans. |

## Build

```bash
cd ~/colcon_ws
colcon build --packages-up-to omron_moma_capabilities --symlink-install
```

## Runtime

Start the capabilities2 stack

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