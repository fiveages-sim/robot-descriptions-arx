# ARX Lift Description

升降底盘 + 双臂（X5/R5）+ 头部。控制模式对齐 Lift2S：**分体 / 全身**（同包双 task，不另建 arms 包）。

| 模式 | Launch | OCS2 | 升降 / 头 |
|------|--------|------|------|
| Full body | `full_body.launch.py` | `task.info`（`ocs2_wheel_humanoid`） | `ocs2_wbc_controller`（lift + 双臂 + 头） |
| Split body | `split_body.launch.py` | `task_arm.info` + `topology:=dual`（根 `arm_base`，同 m6_ccs） | `body_joint_controller` + `head_joint_controller` |
| 旧 demo | `demo.launch.py` | 见 `fixed_base.info`（遗留） | 不推荐，请用分体/全身 |

分体规划与 m6_ccs 相同思路：`robot.xacro` 在 `topology:=dual` 时只生成双臂树；`task_arm.info` 留在本包 `config/ocs2/`。

全身 WBC 状态：`[base x,y,yaw | lift_joint | left×6 | right×6 | head×2]`（头进 MPC，同 W2 布局）。

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
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift hardware:=isaac
```

配置见 `config/ocs2/task.info`、`task_arm.info` 与 `config/ros2_control/common.yaml`。
