# ARX Lift 2S Description

This package contains the description files for ARX Lift 2S
(lift chassis + [ARX AC One](../arx_acone_description/) dual-arm torso).

| Mode | Launch | OCS2 model | Lift |
|------|--------|------------|------|
| Full body | `full_body.launch.py` | `task.info`（`ocs2_wheel_humanoid`，含 SE(2) 底盘） | Inside WBC（`ocs2_wbc_controller`，`waist_lifting_type: single_joint`） |
| Split body | `split_body.launch.py` | acone `task.info` | `body_joint_controller` |
| Arms only | `demo.launch.py robot:=arx_acone` | acone `task.info` | N/A |

Split body uses the acone Pinocchio model (`robot_name: arx_acone`) because EE poses are
relative to URDF root (`arm_base`); the Lift2S root is `base_link` under the lift.

Full-body WBC 状态：`[base x,y,yaw | lift_joint | left 1–6 | right 1–6]`（3+13）。
Body **仅** `lift_joint`（棱柱）：无 `body_joint*`、无头；
`waist_lifting_type: single_joint`，不要发 `waist_turning*`。
行程：`eef_fixed_joints` 规划 URDF → **0.30 m**；viz / ros2_control → **0.48 m**（同 HI `height_span_m`）。
底盘：模型已开 `manipulatorModelType=1`；无 `world→base_link` TF 时 WBC 自动锁底盘（真机无定位即失效）。

配置见 `config/ocs2/task.info` 与 `config/ros2_control/common.yaml`。
Isaac 的 position-only overlay（`isaac.yaml`）及与 `variant` 的合并顺序，见
[`robot_common_launch` README · ros2_control 配置合并](../../../common/robot_common_launch/README.md#ros2_control-配置合并load_robot_config)。

![arx lift2s x5](../.images/arx_lift2s_x5.png)

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. Visualize the robot

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
```

## 3. OCS2 Demo

RMW=zenoh 时先另开终端：`ros2 run rmw_zenoh_cpp rmw_zenohd`。

### 3.1 Full body

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
# Isaac：position-only（URDF + config/ros2_control/isaac.yaml）
# overlay 机制见 robot_common_launch README「ros2_control 配置合并」
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s hardware:=isaac
```

### 3.2 Split body

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=isaac
```

### 3.3 Arms only

See [`arx_acone_description/README.md`](../arx_acone_description/README.md).

### 3.4 分体 / 全身常用话题（body = 仅 lift）

**split_body**（臂 + `body_joint_controller`）：

```bash
# 升降绝对高度 [m]（1 维）
ros2 topic pub --once /body_joint_controller/target_joint_position \
  std_msgs/msg/Float64MultiArray "{data: [0.2]}"
# 连续升降（MOVEJ）：+升 / −降，比例 ∈ [-1, 1]
ros2 topic pub --once /body_joint_controller/waist_lifting_command \
  std_msgs/msg/Float64 "data: 0.5"
# 双臂（12 维）
ros2 topic pub --once /ocs2_arm_controller/target_joint_position \
  std_msgs/msg/Float64MultiArray "{data: [0,0.594,0.306,0.331,0,0, 0,0.594,0.306,0.331,0,0]}"
```

**full_body**（`ocs2_wbc_controller`，13 维含 lift）：

```bash
# HOME / MOVEJ 后升降（单关节）
ros2 topic pub --once /ocs2_wbc_controller/waist_lifting_command \
  std_msgs/msg/Float64 "data: 0.5"
ros2 topic pub --once /ocs2_wbc_controller/waist_lifting_pose_relative \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.05, 0.0]}"   # [dx, dz, dphi]；仅 dz 有效
# OCS2 躯干模式（仅 FREE / LOCK / TRACKING；默认 HM_DUAL_BODY_FREE = 躯干自由）
ros2 topic pub --once /ocs2_wbc_controller/mode_command std_msgs/msg/String "data: 'BODY_FREE'"
ros2 topic pub --once /ocs2_wbc_controller/mode_command std_msgs/msg/String "data: 'BODY_LOCK'"
ros2 topic pub --once /ocs2_wbc_controller/mode_command std_msgs/msg/String "data: 'BODY_TRACKING'"
# 离开腰锁定请用 BODY_FREE（BODY_UNLOCK 会切到已关闭的 RELATIVE）
# 有 world→base_link TF 时可 BASE_UNLOCK；无 TF 时 WBC 会拒绝解锁底盘
ros2 topic pub --once /ocs2_wbc_controller/fsm_command std_msgs/msg/Int32 "data: 3"
```

无转向关节，**不要**使用 `waist_turning_command`。无头 / 无竖直 RELATIVE / 无 CUSTOM_LOCK。

## 4. Real hardware

Requires [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)：臂 can1/can3，升降 can5。

| 对象 | 模式 / 参数 | 说明 |
|------|-------------|------|
| 臂 | 仅 `full_control`（MIT MIX） | URDF：`position/velocity/effort` |
| 臂 MIT 增益 | HI `joint_k_gains` / `joint_d_gains` | 默认 `[20,20,20,20,10,10]` / `[0.8,0.8,0.8,0.8,0.5,0.5]`；可热调 |
| 升降 | `hybrid`（默认，**OCS2 全身请用这个**）或 `soft_p` | hybrid：pos+vel+τ_ff 持高；soft_p 仅 position，全身易掉柱 |
| 升降增益 | `arx_lift.hybrid_kp/kd` 或 `soft_p_kp` | 与臂无关；无 controller kp/kd IF |
| 底盘 | HI `enable_chassis_cmd_vel`（默认 `true`） | hybrid：`/cmd_vel` → `setChassisCmd` + `sendChassisOnly`（不绑 Soft-P）；勿与 WBC 同时开 |
| `lift_joint` 行程 | 规划 URDF `0.30` m；ros2_control / 真机 `0.48` m | 同 m6_ccs `joint4` + `eef_fixed_joints` |

真机 MIT 增益只走 HI 参数（臂 `joint_k/d_gains`，升降 `arx_lift.*`）。
