# ARX Lift2S 描述

ARX Lift2S 描述（升降底盘 + [ARX AC One](../arx_acone_description/) 双臂躯干）。

| 模式 | Launch | OCS2 模型 | 升降 |
|------|--------|-----------|------|
| 全身 | `full_body.launch.py` | 本包 `task.info`（`ocs2_wheel_humanoid`，含 SE(2) 底盘） | 在 WBC 内（`ocs2_wbc_controller`，`waist_lifting_type: single_joint`） |
| 分体 | `split_body.launch.py` | acone `task.info` | `body_joint_controller` |
| 仅双臂 | `demo.launch.py robot:=arx_acone` | acone `task.info` | 无 |

无头、无腰转；升降只有 `lift_joint`。规划行程 0.30 m，可视化 / 真机 0.48 m（详见 §4）。

![arx lift2s x5](../.images/arx_lift2s_x5.png)

## 1. 编译

```bash
cd ~/lift2s-ws   # or ~/ros2_ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. 可视化

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
```

## 3. OCS2 演示

RMW=zenoh 时先另开终端：`ros2 run rmw_zenoh_cpp rmw_zenohd`。

### 3.1 全身

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
# Isaac：position-only（URDF + config/ros2_control/isaac.yaml）
# overlay 机制见 robot_common_launch README「ros2_control 配置合并」
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s hardware:=isaac
```

### 3.2 分体

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=isaac
```

### 3.3 仅双臂

见 [`arx_acone_description/README.md`](../arx_acone_description/README.md)。

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

## 4. 真机

需要 [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)：臂 can1/can3，升降 can5。

| 对象 | 模式 / 参数 | 说明 |
|------|-------------|------|
| 臂 | 仅 `full_control`（MIT MIX） | URDF：`position/velocity/effort` |
| 臂 MIT 增益 | HI `joint_k_gains` / `joint_d_gains` | 默认 `[20,20,20,20,10,10]` / `[0.8,0.8,0.8,0.8,0.5,0.5]`；可热调 |
| 升降 | `hybrid`（默认）或 `soft_p` | hybrid：pos+vel+重力/摩擦；soft_p：直跟 position + 常值重力（无摩擦） |
| 升降增益 | `arx_lift.hybrid_kp/kd` 或 `soft_p_kp` | 与臂无关；无 controller kp/kd IF |
| 底盘 | HI `enable_chassis_cmd_vel`（默认 `true`） | `chassis_mode=1` 时 `/cmd_vel` → `setChassisCmd` |
| 底盘 mode | `chassis_mode`（默认 **1**） | `1`：车体速度（遥控/WBC demo）；`3`：单轮保持（手转轮测反馈）`xacro_chassis_mode:=3` |
| 底盘 odom/TF | `enable_chassis_odom` / `_tf`（默认 **true**） | IMU yaw + `0x702` 轮速逆解 → `/arx_lift/odom` + `world→base_link` |
| 全身底盘模型 | `task.info` `manipulatorModelType` **4** | 全向 vx,vy,omega（`add_omni_wbc`）；差速是 1 |

全身 **WBC 与手柄/VR 共用 `/cmd_vel`**。`VRInputHandler`（`add_omni_wbc`）已把所有权互斥：

1. **人工底盘**（左右摇杆同时按下，case 20）：自动 `BASE_LOCK`，摇杆独占 `/cmd_vel`。用于开到工位。退出 case 20 时把当前车体设为 TF 原点。
2. **HOLD→OCS2**（右 A 或 RViz 面板）：只进全身跟踪，**不再**自动 reset TF / `BASE_LOCK`（避免模型跳变）。
3. **WBC 底盘**（右握把 + 右摇杆**向下拨**，case 26）：须先退出 case 20；解锁前再次 reset odom。只适合小范围。
4. **急停 HOLD**（左 X，原有 OCS2→HOLD）：立刻锁底盘、停 `/cmd_vel`、双臂保持；再按左 X 进 HOME。

不要在人工底盘（case 20）时用 case 26。WBC 开车时手放在左 X 上。

### mode=3 手转轮（分体，不发速度）

```bash
source ~/lift2s-ws/install/setup.bash
# 分体真机，覆盖默认：xacro_chassis_mode:=3
# 日志应有 chassis_mode=3

ros2 topic echo /body_information
# 重点：temp_float_data[1]=轮1车尾 [2]=轮2右前 [3]=轮3左前
```

手转单轮，看对应位是否变化。不要发 `/cmd_vel`。demo 遥控用默认 `chassis_mode=1`。

### 底盘 TF 快速验证（真机）

```bash
source ~/lift2s-ws/install/setup.bash
# 重新 quick_start（加载新 fullbody.rviz：含 lift_link/轮；HI TF≤50Hz）

# Fixed Frame=world；若车漂出视野：RViz Views → Zero，或盯着机器人 Zoom
ros2 run tf2_ros tf2_echo world base_link
ros2 topic echo /arx_lift/odom
```

日志期望：`External TF world->base_link available`。

### TF 刻度（显示正常后再调）

雅可比按**官方轮组编号**：`getWheelVel[0..2]` = 轮1车尾 / 轮2右前 / 轮3左前（URDF 名 `wheel_1` 是左前，编号不同）。

1. 静止时 `tf2_echo` 应接近原点（允许小漂）。  
2. 遥控量地面前进 ~1 m，看 Δx：偏大/偏小 → `chassis_wheel_vel_scale` 或 `chassis_wheel_radius_m`。  
3. 若某轴仍反了 → `chassis_wheel_vel_sign`，并对比 `/arx_lift/wheel_vel_expected` 与 `/body_information` 的 `temp_float_data[1..3]`。  
参数在 `xacro/ros2_control/robot.xacro` 的 Lift HI `<param>`。


真机 MIT 增益只走 HI 参数（臂 `joint_k/d_gains`，升降 `arx_lift.*`）。
