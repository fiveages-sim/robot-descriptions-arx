# ARX Lift 2S Description

Whole-body description for ARX Lift 2S: lift chassis + [ARX AC One](../arx_acone_description/)
dual-arm torso.

Control layout follows [fa-w2-description/config](https://github.com/fiveages-sim/fa-w2-description/tree/main/config)
(`ocs2/` + `ros2_control/common.yaml` + thin overlay + `rviz/`).

| Mode | Launch | Hardware URDF | OCS2 model | Lift |
|------|--------|---------------|------------|------|
| 全身 | `full_body.launch.py` | `arx_lift2s` | `fixed_base.info` | Inside OCS2 (`ocs2_wbc_controller`) |
| 分体 | `split_body.launch.py` | `arx_lift2s` | **acone** `task.info` | `body_joint_controller` |
| 仅双臂 | `demo.launch.py robot:=arx_acone` | `arx_acone` | acone `task.info` | N/A |

真机 HI（`arxlift2s_ros2_control`）：

- 臂：`full_control` \| `position`（xacro `control_mode`；热调 `control_mode` / `joint_k_gains` / `joint_d_gains`）
- 升降：`soft_p`/`position` \| `hybrid`（`lift_motor_mode`；热调 `arx_lift.*`）
  - **hybrid**：MIT 直跟上层 position+velocity + HI τ_ff（`gravity` − `coulomb·sign(v_cmd)`；**忽略** effort；死区 `friction_vel_eps_mps`；均可 `arx_lift.*` 热调）
  - **position/soft_p**：只用上层 position（仍有 HI 斜坡）
  - 分体/全身 quick_start 均可选；xacro 默认 `hybrid`

## Config 布局

```text
arx_lift2s_description/config/
  ocs2/
    fixed_base.info       # 全身 MPC（lift + dual arms）
    task_arm.info         # 文档/离线参考；运行时分体不用此文件
    target_manager.yaml
  ros2_control/
    common.yaml           # 控制器全集（合并基底）
    ros2_controllers.yaml # 默认 overlay（当前为空，占位）
  rviz/
    fullbody.rviz
    splitbody.rviz
```

加载顺序（`robot_common_launch.load_robot_config`，同 fa-w2 / m6 / CR5）：

`common.yaml` ← deep-merge ← `{type}.yaml` 或 `ros2_controllers.yaml` ← 可选 variant overlay

参考对比：

| 仓库 | `common.yaml` | overlay 拆分时机 |
|------|---------------|------------------|
| [fa-w2](https://github.com/fiveages-sim/fa-w2-description/tree/main/config) | 全身+双臂+body/gripper 全集 | `ros2_controllers.yaml` 只补 home_* |
| [m6_ccs](https://github.com/fiveages-sim/robot-descriptions-tianji/tree/main/m6_ccs_description/config) | 双臂公共 | `left.yaml` / `right.yaml` / `desktop.yaml`（臂数/场景不同） |
| [CR5](https://github.com/fiveages-sim/robot-descriptions-dobot/tree/main/cr5_description/config) | （或空基） | EEF 类型：`AG2F90-C-Soft.yaml` 等 |
| **lift2s（当前）** | 分体臂 + 全身 WBC + body lift + grippers | 无 type/EEF 变体 → overlay 为空即可 |

**不必**按 `full_control` / `position` 拆 `common.yaml`：模式相关 MIT 增益在 HI xacro，不在控制器 yaml。

### `pd_gains` / `default_gains`（common.yaml:72–74）

| | lift2s `ocs2_arm_controller` | acone `ocs2_arm_controller` |
|--|--|--|
| 数值 | `[30.0, 2.0]` | `[30.0, 2.0]`（相同） |
| 用途 | 控制器状态机写 command IF 的 kp/kd | 同左 |
| 真机 MIT | **不驱动**；臂用 HI `joint_k/d_gains` | 同左 |

lift2s 额外有 `ocs2_wbc_controller` 的同值 `[30, 2]`（全身）；升降力矩增益在 lift HI（`hybrid_kp/kd` / `soft_p_kp`），不在这两行。

### 分体为何指向 acone

`ocs2_arm_controller`：`robot_name: arx_acone`，`info_file_name: task`。

Pinocchio EE 位姿在 URDF root；Lift2S root=`base_link`（下面有 lift），acone root≡`arm_base`，故分体规划用 acone 模型。`task_arm.info` 仅作文档/离线参考。

### Self-collision

| Mode | `.info` | Collision |
|------|---------|-----------|
| 分体 | acone `task` | arms ↔ torso（acone 模型） |
| 全身 | `fixed_base` | arms ↔ `body_link` / `lift_link` / `base_link` |

### 真机臂 MIT 默认（xacro，按 `control_mode`）

| Mode | `joint_k_gains` | `joint_d_gains` |
|------|-----------------|-----------------|
| `full_control` | `[20, 20, 20, 20, 10, 10]` | `[3.5, 3.5, 3.5, 3.5, 1.0, 1.0]` |
| `position` / `pd_control` | `[80, 70, 70, 30, 30, 20]` | `[2, 2, 2, 1, 1, 0.7]` |

## 1. Build

```bash
cd ~/lift2s-ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. Visualize

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
```

## 3. OCS2 Control

### 3.1 Full Body（`fixed_base.info`）

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s hardware:=real
```

### 3.2 Split Body（acone `task.info`）

```bash
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s hardware:=real
```

或仓库根目录 `./quick_start.sh` → Launch（真机可选臂 `control_mode`）。
