# ARX X7S Arms Description

Split-body OCS2 planning only: dual 7-DOF arms + grippers, URDF root = `body`.

Hardware / visualization / full-body WBC stay on `arx_x7s_description`.

Used via `ocs2_arm_controller.robot_name: arx_x7s_arms` (same pattern as Lift2S→`arx_acone`, fa_w2→`m6_ccs`).

```bash
colcon build --packages-select arx_x7s_arms_description --symlink-install
```
