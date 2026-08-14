# ARX X7S Description

X7S 整机描述（升降 + 腰 + 双 7DOF 臂 + 头）。控制模式对齐 Lift2S / fa_w2：**分体 / 全身**（无 `topology`；分体用 `robot_name` 指向规划包）。

无法复用 `arx_acone`（6DOF、根 `arm_base`、安装/EE 均不同），分体规划包为 **`arx_x7s_arms_description`**（根 `body`，仅双臂）。

| 模式 | Launch | 规划 | 躯干/头 |
|------|--------|------|---------|
| Full body | `full_body.launch.py` | 本包 `task.info`（WheelHumanoid，含头） | `ocs2_wbc_controller`（lift+腰+头+双臂） |
| Split body | `split_body.launch.py` | **`arx_x7s_arms`** `task.info`（根 `body`） | `body_joint_controller` + `head_joint_controller` |

全身 Pinocchio 序：`[lift | waist | head×2 | L7 | R7]`（头在 Body xacro 内、臂之前）。  
MOVEJ 下 RViz **Head** 走 `/ocs2_wbc_controller/target_joint_position/head`。  
**Body** 页仍受 `waist_joint` 命名限制（arms/fa-py 只认 `lift_joint` / `body*`）；腰可用专用升降/pitch 接口。

硬件 / RSP / 全身规划：始终本包 **full** `xacro/robot.xacro`。

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_x7s_description arx_x7s_arms_description --symlink-install
```

## 2. Visualize

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_x7s
```

## 3. OCS2

### 3.1 Full Body

```bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_x7s
```

### 3.2 Split Body

```bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_x7s
```

配置见 `config/ros2_control/ros2_controllers.yaml`（`ocs2_arm_controller.robot_name: arx_x7s_arms`）。
