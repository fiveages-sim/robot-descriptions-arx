# ARX Lift 2S Description

This package contains the description files for ARX Lift 2S
(lift chassis + [ARX AC One](../arx_acone_description/) dual-arm torso).

| Mode | Launch | OCS2 model | Lift |
|------|--------|------------|------|
| Full body | `full_body.launch.py` | `fixed_base.info` | Inside OCS2 (`ocs2_wbc_controller`) |
| Split body | `split_body.launch.py` | acone `task.info` | `body_joint_controller` |
| Arms only | `demo.launch.py robot:=arx_acone` | acone `task.info` | N/A |

Split body uses the acone Pinocchio model (`robot_name: arx_acone`) because EE poses are
relative to URDF root (`arm_base`); the Lift2S root is `base_link` under the lift.

![arx lift2s x5](../.images/arx_lift2s_x5.png)

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
# Real also needs:
#   colcon build --packages-up-to arx_ros2_control ocs2_arm_controller --symlink-install
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
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s hardware:=real
```

### 3.2 Split body

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=real
```

### 3.3 Arms only

See [`arx_acone_description/README.md`](../arx_acone_description/README.md).

## 4. Real hardware

Requires [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)：臂 can1/can3，升降 can5。

| 对象 | 模式 / 参数 | 说明 |
|------|-------------|------|
| 臂 | 仅 `full_control`（MIT MIX） | URDF：`position/velocity/effort/kp/kd` |
| 臂 MIT 增益 | HI `joint_k_gains` / `joint_d_gains` | 默认 `[20,20,20,20,10,10]` / `[0.8,0.8,0.8,0.8,0.5,0.5]`；可热调 |
| 升降 | `hybrid`（默认）或 `soft_p`/`position` | hybrid：pos+vel + HI τ_ff；soft_p：仅 position |
| 升降增益 | `arx_lift.hybrid_kp/kd` 或 `soft_p_kp` | 与臂无关 |
| `lift_joint` 行程 | URDF `upper=0.30` m | 规划限位跟 URDF |

`common.yaml` 的 `pd_gains` / `default_gains` 仅供控制器状态机；真机 MIT 不读这两项。
