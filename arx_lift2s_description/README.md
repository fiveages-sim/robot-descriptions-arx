# ARX Lift 2S Description

Whole-body description for ARX Lift 2S: lift chassis + [ARX AC One](../arx_acone_description/)
dual-arm torso.

Control layout follows the FiveAges W2 / M6 CCS pattern:

| Mode | Launch | Hardware URDF | Arm planning | Lift |
|------|--------|---------------|--------------|------|
| 全身 | `full_body.launch.py` | `arx_lift2s` | `arx_lift2s` (`fixed_base.info`，含底盘/升降碰撞) | Inside OCS2 |
| 分体 | `split_body.launch.py` | `arx_lift2s` | `arx_acone` (`task.info`，仅双臂↔`body_link`) | `body_joint_controller` |
| 仅双臂 | `demo.launch.py robot:=arx_acone` | `arx_acone` | `arx_acone` | N/A |

### Self-collision（对齐 fa_w2）

| Mode | Planning robot | Collision geometry | `collisionLinkPairs` |
|------|----------------|--------------------|----------------------|
| 分体 | `arx_acone`（≈ m6_ccs） | acone `body_link` simple boxes | arms ↔ `body_link` |
| 全身 | `arx_lift2s`（≈ fiveages_w2） | chassis + lift + `body_link` simple boxes | arms ↔ `body_link` / `lift_link` / `base_link` |

## 1. Build

```bash
cd ~/arx_lift2s_ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. Visualize

### 2.1 Full Lift 2S

* Lift + X5
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
  ```

* Lift + R5
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s type:=r5
  ```

AC One (no chassis) visualization lives in `arx_acone_description`.

### 2.2 Components

* Chassis
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_lift2s
  ```

* AC One torso / arms — see [`arx_acone_description`](../arx_acone_description/README.md)

## 3. OCS2 Control

### 3.1 Full Body（全身：升降 + 双臂同一 OCS2）

```bash
source ~/arx_lift2s_ws/install/setup.bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
```

### 3.2 Split Body（分体：双臂 OCS2 + 升降 BasicJoint）

```bash
source ~/arx_lift2s_ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
```

* Isaac
  ```bash
  ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=isaac
  ```

* Real（官方 SDK：can1/can3 臂 + can5 升降；**无 MIX**，臂为 position）
  ```bash
  ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=real
  ```

单/双臂 Stanford + `full_control`（OCS2 MIX）见 `arx5_description` / `arx_acone_description`。
### 3.3 Official OCS2 Mobile Manipulator Demo

```bash
source ~/arx_lift2s_ws/install/setup.bash
ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx_lift2s
```
