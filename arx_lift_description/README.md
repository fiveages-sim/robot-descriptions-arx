# ARX Lift Description

升降底盘 + 双臂（X5/R5）+ 头部。控制模式对齐 Lift2S：**分体 / 全身**（无 `topology`；分体用 `robot_name` 指向规划包）。

| 模式 | Launch | 规划 | 升降 / 头 |
|------|--------|------|------|
| Full body | `full_body.launch.py` | 本包 `task.info`（`ocs2_wheel_humanoid`） | `ocs2_wbc_controller`（lift + 双臂 + 头） |
| Split body | `split_body.launch.py` | **`arx_acone`** `task.info`（根 `arm_base`） | `body_joint_controller` + `head_joint_controller` |

硬件 / `robot_state_publisher` / 全身规划：始终本包 **full** `xacro/robot.xacro`。

分体复用 acone（同 Lift2S），但经典 Lift 臂座 ≠ acone 默认，须传：

```text
xacro_left_xyz:="0.208 0.25000 0.092"
xacro_right_xyz:="0.208 -0.25000 0.092"
```

（`quick_start` 分体已自动加。）规划臂型为 acone 的 `X5_ac1`；与硬件 `X5.xacro` 在法兰细节上可能略有差别，一般够用 MPC。

RViz：本包 `config/rviz/` 默认关闭规划模型的 Collision 显示（不改 acone / Lift2S 的 URDF 碰撞体）。

全身 WBC 状态：`[base x,y,yaw | lift_joint | left×6 | right×6 | head×2]`。

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_lift_description --symlink-install
```

## 2. Visualize

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift type:=r5
```

## 3. OCS2

RMW=zenoh 时先：`ros2 run rmw_zenoh_cpp rmw_zenohd`。

### 3.1 Full body

```bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift hardware:=isaac
```

### 3.2 Split body

```bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift \
  xacro_left_xyz:="0.208 0.25000 0.092" \
  xacro_right_xyz:="0.208 -0.25000 0.092"
```

配置见 `config/ocs2/task.info`、`config/ros2_control/common.yaml`（`ocs2_arm_controller.robot_name: arx_acone`）。
