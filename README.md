# omron_moma_capabilities

Omron-specific capabilities-side package for the mobile-manipulator stack.

## Purpose

This package provides the Omron capabilities around the generic mobile-manipulator stack.

## Ownership Boundary

- `grasping` owns active scene management, MoveIt planning-scene updates, arm-only feasibility, and arm execution
- `mobile_manipulator` owns the generic multi-step arm-plus-base runtime, scene registry, and default plugins
- `mobile_manipulator_capabilities` owns generic capability adapters over those ROS APIs
- `omron_moma_capabilities` owns Omron-facing composition, configuration, and capability wiring

This package should prefer parameter-driven customization of the generic mobile-manipulator stack. If a new reusable plugin is needed, it should live under `mobile_manipulator` rather than here.