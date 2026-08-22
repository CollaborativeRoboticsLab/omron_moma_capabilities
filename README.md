# omron_moma_capabilities

Omron-specific launch and configuration package for mobile-manipulator feasibility.

This package configures the generic `mobile_manipulator/CheckTaskFeasibility` service node with Omron-specific parameters such as:

- candidate stand-off distances and angle offsets
- navigation frame assumptions
- costmap topic and occupancy threshold
- arm base frame and re-check mode
