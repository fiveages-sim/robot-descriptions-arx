# ARX AC One Description

Standalone dual-arm torso (AC One + X5/R5) description.

Used by `arx_lift2s_description` for **split-body** planning (same role as
`m6_ccs_description` for `fiveages_w2_description`).

## 1. Build

```bash
cd ~/arx_lift2s_ws
colcon build --packages-up-to arx_acone_description --symlink-install
```

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

* Real (official LIFT2S arm HW, can1/can3)
  ```bash
  source ~/arx_lift2s_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=real
  ```

For Lift2S chassis + AC One (split / full body), see
[`arx_lift2s_description/README.md`](../arx_lift2s_description/README.md).
