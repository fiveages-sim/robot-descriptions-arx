# ARX AC One Description

Standalone dual-arm torso (AC One + X5/R5) description.

Used by `arx_lift2s_description` for **split-body** planning (same role as
`m6_ccs_description` for `fiveages_w2_description`).

**Real hardware:** Stanford [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)
with OCS2 MIX only — `position/velocity/effort`，固定 `full_control`；MIT 增益在 HI `joint_k/d_gains`。
Deploy: `hardware:=real`，can1 / can3。

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_acone_description --symlink-install
# Real MIT also needs:
#   colcon build --packages-up-to arx_ros2_control ocs2_arm_controller --symlink-install
```

## 2. Visualize

* AC One + X5（默认 `variant:=acone`，带躯干）
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone
  # 等价显式写法：
  # ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone variant:=acone
  ```

* AC One + R5
  ```bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone type:=r5
  ```

* 展台底座（无 AC One mesh，同 m6 `variant:=desktop`）
  ```bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone variant:=desktop
  ```

* 自定义双臂间距（覆盖默认安装位姿，单位 m）
  ```bash
  # 例：与经典 Lift 臂座一致（左右 y=±0.25，前伸 0.208）
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone \
    variant:=desktop \
    xacro_left_xyz:="0.208 0.25 0.092" \
    xacro_right_xyz:="0.208 -0.25 0.092"
  ```

* Torso only
  ```bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_acone type:=ac_one
  ```

### 2.1 `variant` / 臂安装（对齐 m6_ccs）

| 参数 | 说明 |
|------|------|
| `variant` | `acone`（默认）= 带 AC One 躯干；`desktop` = 展台底座（无 AC One） |
| `left_xyz` / `right_xyz` | 臂相对 `arm_base` 的安装位姿；空则用 variant 默认 |
| `left_rpy` / `right_rpy` | 可选，默认 `0 0 0` |
| `arm_base_xyz` | 仅 `desktop`：`arm_base` 相对 `base_link`，默认 `0 0 0.35` |

默认 AC One 安装：`±0.25 m` 半间距（`left_xyz:='-0.01602 0.25 -0.035'`）。  
宏：`xacro/arm_mount.xacro` → `DualArmMount` / `DesktopArmBase`（可被 Lift2S 等直接调用）。

## 3. OCS2 Arm Controller Demo

### 3.1 Simulation

* Mock
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
  ```

* Isaac Sim
  ```bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=isaac
  ```

* Desktop + 自定义间距
  ```bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone \
    variant:=desktop \
    xacro_left_xyz:="0.208 0.25 0.092" \
    xacro_right_xyz:="0.208 -0.25 0.092"
  ```

### 3.2 Real — full_control only

Prereqs: `can1` / `can3` up；无其它节点占用总线；Stanford SDK + `arx_ros2_control` 已编译。

真机臂**仅** `full_control`（MIT MIX）：URDF 声明 `position/velocity/effort`；HI `write()` 始终下发 pos+vel+effort。

```bash
# RMW=zenoh 时先另开终端: ros2 run rmw_zenoh_cpp rmw_zenohd
source ~/ros2_ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=real
```

**真机 MIT 增益**

| 层级 | 参数 | 说明 |
|------|------|------|
| HI | `joint_k_gains` / `joint_d_gains`（xacro，可用 rqt 动态改） | 驱动电机 MIT kp/kd（唯一来源） |

**Bring-up checks**

1. HI log: `full_control / MIT MIX` on `/arx_acone_left_system`、`/arx_acone_right_system`
2. rqt / `ros2 param`：改 `/arx_acone_*_system` 的 `joint_k_gains` / `joint_d_gains` 即生效

For Lift2S chassis + AC One (split / full body), see
[`arx_lift2s_description/README.md`](../arx_lift2s_description/README.md).
