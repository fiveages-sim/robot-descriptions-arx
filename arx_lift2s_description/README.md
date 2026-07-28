# ARX Lift 2S Description

Whole-body description for ARX Lift 2S: lift chassis + [ARX AC One](../arx_acone_description/)
dual-arm torso.

Control layout follows [fa-w2-description/config/ocs2](https://github.com/fiveages-sim/fa-w2-description/tree/main/config/ocs2):

| Mode | Launch | Hardware URDF | OCS2 `.info` | Lift |
|------|--------|---------------|--------------|------|
| 全身 | `full_body.launch.py` | `arx_lift2s` | `fixed_base.info`（升降+双臂） | Inside OCS2 MIX |
| 分体 | `split_body.launch.py` | `arx_lift2s` | `task_arm.info`（双臂） | `body_joint_controller` |
| 仅双臂 | `demo.launch.py robot:=arx_acone` | `arx_acone` | acone `task.info` | N/A |

真机 HI：**臂 full_control MIX**；**升降 Hybrid MIT only**（`sendLiftHybrid`，可调 `arx_lift.hybrid_kp/kd`；Soft-P / `setHeight` 已退役）。

### OCS2 配置目录

```text
arx_lift2s_description/config/ocs2/
  task_arm.info        # 分体：双臂
  fixed_base.info      # 全身：固定底盘 + 升降 + 双臂
  target_manager.yaml
```

`common.yaml`：`ocs2_arm_controller` → `robot_name: arx_lift2s` + `info_file_name: task_arm`；
`ocs2_wbc_controller` → `info_file_name: fixed_base`。

### Self-collision

| Mode | `.info` | Collision |
|------|---------|-----------|
| 分体 | `task_arm` | arms ↔ `body_link` |
| 全身 | `fixed_base` | arms ↔ `body_link` / `lift_link` / `base_link` |

## 1. Build

```bash
cd ~/lift2s-ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. Visualize

### 2.1 Full Lift 2S

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
```

## 3. OCS2 Control

### 3.1 Full Body（`fixed_base.info`）

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
# 真机
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s hardware:=real
```

### 3.2 Split Body（`task_arm.info`）

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=real
```

或使用仓库根目录 `./quick_start.sh` → Launch → 3/4（真机自动 `full_control`）。

### X5 MIT gains（真机默认）

`joint_k_gains: [20, 20, 20, 20, 10, 10]`，`joint_d_gains: [3.5, 3.5, 3.5, 3.5, 1.0, 1.0]`，`gripper_kp: 5.0`。
