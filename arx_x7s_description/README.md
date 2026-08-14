# ARX X7S Description

X7S 整机描述（升降 + 腰俯仰 `body_joint` + 双 7DOF 臂 + 头）。分体/全身用**同包 topology**（无独立 arms 包、不改 arms_ros2_control）。

| 模式 | Launch | 规划 | 躯干/头 |
|------|--------|------|---------|
| Full body | `full_body.launch.py`（`xacro_topology:=full`） | 本包 `task.info`（含头） | `ocs2_wbc_controller` |
| Split body | `split_body.launch.py` + **`xacro_topology:=dual`** | 本包 `task_arm.info`（根 `body`） | `body_joint_controller` + `head_joint_controller` |

全身 Pinocchio 序：`[lift | body_joint | head×2 | L7 | R7]`。  
MOVEJ：**Head** / **Body**（`lift_joint` + `body_joint`）均可走 `/ocs2_wbc_controller/target_joint_position/{head,body}`。

硬件 / RSP 始终 `ros2_control/robot.xacro` → **full**（忽略 dual）。

## 1. Build

```bash
colcon build --packages-up-to arx_x7s_description --symlink-install
```

## 2. Visualize

```bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_x7s
```

## 3. OCS2

### Full Body

```bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_x7s xacro_topology:=full
```

### Split Body（必须 dual）

```bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_x7s xacro_topology:=dual
```

`quick_start` 已自动加 topology。配置见 `config/ros2_control/ros2_controllers.yaml`。
