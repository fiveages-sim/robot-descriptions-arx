# Robot Descriptions - ARX

ARX robot description packages for ROS 2 (URDF/xacro, meshes, ros2_control / OCS2 configs).

Upstream umbrella: [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) (submodule path `manipulator/ARX`).

## Packages

| Brand | Model | Repaint | Images |
|-------|-------|---------|--------|
| ARX | [LIFT](arx_lift_description/) | Yes | <img src=".images/arx_lift.png" width="200" style="object-fit: cover; object-position: center;"> <img src=".images/arx_lift2.png" width="200" style="object-fit: cover; object-position: center;"> |
| ARX | [X7S](arx_x7s_description/) | Yes | <img src=".images/arx_x7s.png" width="200"> |
| ARX | [X5/R5](arx5_description/) | Yes | <img src=".images/arx_x5.png" width="200"> <img src=".images/arx_r5.png" width="200"> |
| ARX | [AC One](arx_acone_description/) | Yes | Dual-arm torso (split-body planning for Lift2S) |
| ARX | [LIFT2S](arx_lift2s_description/) | Yes | <img src=".images/arx_lift2s_x5.png" width="200" style="object-fit: cover; object-position: center;"> <img src=".images/arx_lift2s_r5.png" width="200" style="object-fit: cover; object-position: center;"> |

## Usage

Add this repository as a workspace submodule (recommended path under [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions): `manipulator/ARX`). Colcon discovers the packages under that tree.

```bash
# Via robot_descriptions
git submodule update --init manipulator/ARX

# Or standalone
git submodule add -b main git@github.com:fiveages-sim/robot-descriptions-arx.git src/robot-descriptions-arx
```

Example commands in package READMEs use `~/ros2_ws` (standard ROS 2 workspace). Source before launch:

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx5_description --symlink-install
source ~/ros2_ws/install/setup.bash
```

See each package README for visualize / OCS2 demo details.

## Related

- Umbrella: [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions)
- Shared components: [robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common)
- Controllers / HI: [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control), [arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control)
