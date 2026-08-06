# ARX AC One Description

Standalone dual-arm torso (AC One + X5/R5) description.

Used by `arx_lift2s_description` for **split-body** planning (same role as
`m6_ccs_description` for `fiveages_w2_description`).

**Real hardware:** Stanford [`arx_ros2_control`](https://github.com/fiveages-sim/arx-ros2-control)
with OCS2 MIX only — `position/velocity/effort/kp/kd`，固定 `full_control`。
Deploy: `hardware:=real`，can1 / can3。

## 1. Build

```bash
cd ~/arx_lift2s_ws
colcon build --packages-up-to arx_acone_description --symlink-install
# Real MIT also needs:
#   colcon build --packages-up-to arx_ros2_control ocs2_arm_controller --symlink-install
```

Or workspace `./quick_start.sh` → Build → 单/双臂真机包（Stanford）。

## 2. Visualize

* AC One + X5 (default)
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone
  ```

* AC One + R5
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone type:=r5
  ```

* Torso only
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_acone type:=ac_one
  ```

## 3. OCS2 Arm Controller Demo

### 3.1 Simulation

* Mock
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
  ```

* Isaac Sim
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=isaac
  ```

### 3.2 Real — full_control only

Prereqs: `can1` / `can3` up；无其它节点占用总线；Stanford SDK + `arx_ros2_control` 已编译。

真机臂**仅** `full_control`（MIT MIX）：URDF 声明 `position/velocity/effort/kp/kd`；HI `write()` 始终下发 pos+vel+effort。

```bash
# 推荐 ./quick_start.sh；手动且 RMW=zenoh 时先: ros2 run rmw_zenoh_cpp rmw_zenohd
source ~/lift2s-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=real
```

**真机 MIT 增益**

| 层级 | 参数 | 说明 |
|------|------|------|
| HI | `joint_k_gains` / `joint_d_gains`（xacro，可用 rqt 动态改） | 驱动电机 MIT kp/kd |
| 控制器 | `default_gains` / `pd_gains`（`common.yaml`） | **不再驱动真机 MIT 增益** |

**Bring-up checks**

1. HI log: `full_control / MIT MIX` on `/arx_acone_left_system`、`/arx_acone_right_system`
2. rqt / `ros2 param`：改 `/arx_acone_*_system` 的 `joint_k_gains` / `joint_d_gains` 即生效

For Lift2S chassis + AC One (split / full body), see
[`arx_lift2s_description/README.md`](../arx_lift2s_description/README.md).
