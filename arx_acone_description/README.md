# ARX AC One Description

Standalone dual-arm torso (AC One + X5/R5) description.

Used by `arx_lift2s_description` for **split-body** planning (same role as
`m6_ccs_description` for `fiveages_w2_description`).

**Real hardware (Phase 1 MIT):** Stanford [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)
with OCS2 MIX — same contract as
[panthera-ht](https://github.com/fiveages-sim/open-deploy-ws/tree/panthera-ht)
(`position/velocity/effort/kp/kd`, `control_mode:=full_control`).
Deploy flow mirrors
[arx-acone](https://github.com/fiveages-sim/open-deploy-ws/tree/arx-acone)
(`hardware:=real`, can1 / can3).

## 1. Build

```bash
cd ~/arx_lift2s_ws
colcon build --packages-up-to arx_acone_description --symlink-install
# Real MIT also needs:
#   colcon build --packages-up-to arx_ros2_control ocs2_arm_controller --symlink-install
```

Or workspace `./quick_start.sh` → Build → 单/双臂真机包（Stanford）。

## 2. Visualize

* AC One + X5 (default)
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone
  ```

* AC One + R5
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone type:=r5
  ```

* Torso only
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_acone type:=ac_one
  ```

## 3. OCS2 Arm Controller Demo

### 3.1 Simulation

* Mock
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
  ```

* Isaac Sim
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=isaac
  ```

### 3.2 Real — 控制模式（参考 panthera-ht）

Prereqs: `can1` / `can3` up；无其它节点占用总线；Stanford SDK + `arx_ros2_control` 已编译。

设计与 [panthera-ht](https://github.com/fiveages-sim/open-deploy-ws/tree/panthera-ht) 相同：URDF **始终**声明 `position/velocity/effort/kp/kd`；`control_mode` 只改变 HI `write()`。

| Launch / xacro | 默认 | 说明 | 对应 HT |
|----------------|------|------|---------|
| `xacro_control_mode:=full_control` | 是（推荐真机） | OCS2 MIX：pos/vel/effort/kp/kd → `set_gain` + `set_joint_cmd`；effort=静力学前馈 | `full_control` |
| `xacro_control_mode:=position` | 否 | **保留真机位置环**：仅 position；kp/kd = HI `joint_k/d_gains` | ≈ `pd_control` |
| `xacro_control_mode:=pd_control` | 否 | `position` 的 HT 别名 | `pd_control` |

```bash
# 推荐：full_control / OCS2 MIX
source ~/arx_lift2s_ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=real

# 真机位置环（旧路径）
ros2 launch ocs2_arm_controller demo.launch.py \
  robot:=arx_acone hardware:=real xacro_control_mode:=position
```

**两套增益（勿混用）**

| 层级 | 参数 | 何时生效 |
|------|------|----------|
| 控制器 | `default_gains` / `pd_gains: [30, 3]`（`common.yaml`） | **仅 `full_control` 运行中** |
| HI | `joint_k_gains` / `joint_d_gains`（xacro `[80…]` / `[2…]`） | **`position` 全程**；`full_control` 仅 fallback — **保留真机调好的值** |

**Bring-up checks**

1. HI log: `control_mode=full_control` on `/arx_acone_left_system`、`/arx_acone_right_system`
2. OCS2 log: `Setting OCS2 gains: kp=30.00, kd=3.00` / Mixed control mode

Runtime param tuning（mainly `position` / fallback）：见
[`arx_ros2_control` DYNAMIC_PARAMS_USAGE.md](https://github.com/fiveages-sim/arx-ros2-control/blob/main/DYNAMIC_PARAMS_USAGE.md)。

For Lift2S chassis + AC One (split / full body; **official** SDK path), see
[`arx_lift2s_description/README.md`](../arx_lift2s_description/README.md).
