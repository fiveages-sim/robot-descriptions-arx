# ARX AC One 描述

独立双臂躯干（AC One + X5/R5）描述。

**Lift** / **Lift2S** 的**分体** OCS2 规划会复用本包。经典 Lift 须覆盖臂座 `xacro_left_xyz` / `xacro_right_xyz`；Lift2S 用本包默认安装。

**真机：** [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)，臂仅 OCS2 MIX — `position/velocity/effort`，固定 `full_control`；MIT 增益在 HI `joint_k/d_gains`。启动：`hardware:=real`，can1 / can3。

## 1. 编译

```bash
cd ~/lift2s-ws   # or ~/ros2_ws
colcon build --packages-up-to arx_acone_description --symlink-install
# 真机 MIT 还需：
#   colcon build --packages-up-to arx_ros2_control ocs2_arm_controller --symlink-install
```

## 2. 可视化

* AC One + X5（默认 `variant:=acone`，带躯干）
  ```bash
  source ~/lift2s-ws/install/setup.bash
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

* 仅躯干
  ```bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_acone type:=ac_one
  ```

### 2.1 `variant` / 臂安装

| 参数 | 说明 |
|------|------|
| `variant` | `acone`（默认）= 带 AC One 躯干；`desktop` = 展台底座（无 AC One） |
| `left_xyz` / `right_xyz` | 臂相对 `arm_base` 的安装位姿；空则用 variant 默认 |
| `left_rpy` / `right_rpy` | 可选，默认 `0 0 0` |
| `arm_base_xyz` | 仅 `desktop`：`arm_base` 相对 `base_link`，默认 `0 0 0.35` |

默认 AC One 安装：`±0.25 m` 半间距（`left_xyz:='-0.01602 0.25 -0.035'`）。  
宏：`xacro/arm_mount.xacro` → `DualArmMount` / `DesktopArmBase`（可被 Lift2S 等直接调用）。

## 3. OCS2 臂控制器演示

### 3.1 仿真

* Mock
  ```bash
  source ~/lift2s-ws/install/setup.bash
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

### 3.2 真机（仅 full_control）

前置：`can1` / `can3` 已起来；无其它节点占用总线；`arx_ros2_control` 已编译。

真机臂**仅** `full_control`（MIT MIX）：URDF 声明 `position/velocity/effort`；HI `write()` 始终下发 pos+vel+effort。

```bash
# RMW=zenoh 时先另开终端: ros2 run rmw_zenoh_cpp rmw_zenohd
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=real
```

**真机 MIT 增益**

| 层级 | 参数 | 说明 |
|------|------|------|
| HI | `joint_k_gains` / `joint_d_gains`（xacro，可用 rqt 动态改） | 驱动电机 MIT kp/kd（唯一来源） |

**上电检查**

1. HI 日志：`/arx_acone_left_system`、`/arx_acone_right_system` 上为 `full_control / MIT MIX`
2. rqt / `ros2 param`：改 `/arx_acone_*_system` 的 `joint_k_gains` / `joint_d_gains` 即生效

Lift 整机（分体 / 全身）见 [`arx_lift_description`](../arx_lift_description/README.md)。  
Lift2S 见 [`arx_lift2s_description`](../arx_lift2s_description/README.md)。
