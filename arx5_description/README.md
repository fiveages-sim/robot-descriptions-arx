# ARX X5/R5 描述

单臂 X5 / R5 描述。部署工作空间 [`lift2s-ws`](https://github.com/fiveages-sim/open-deploy-ws) 用 `./quick_start.sh` 启动（X5 真机再选 can1/can3）。

ACone / Lift / Lift2S 的硬件树也会 include 本包臂 xacro。

原始 mesh：[ARX_Models](https://github.com/ARXroboticsX/ARX_Model)。

## 1. 编译

```bash
cd ~/lift2s-ws   # or ~/ros2_ws
colcon build --packages-up-to arx5_description --symlink-install
```

## 2. 可视化

在 RViz 中可视化并检查配置，直接 launch：

* ARX X5 2023
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx5
  ```

  ![arx x5](../.images/arx_x5.png)

* ARX X5 2025 (AC1)
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx5 type:=ac1
  ```

  ![arx x5](../.images/arx_x5.png)

* ARX R5
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx5 type:="r5"
  ```

  ![arx r5](../.images/arx_r5.png)

* ARX R5 Agilex Style
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx5 type:="agilex"
  ```

  ![arx r5](../.images/arx_r5.png)

* 仅 ARX 夹爪组件
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch gripper.launch.py gripper:=arx5
  ```
  - 2023 夹爪：`xacro_arg:=type:=2023`
  - 2025(AC1) 夹爪：`xacro_arg:=type:=2025`

* 相机支架组件（`component.xacro`）
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx5 xacro_arg:=type:=d405
  ```
  - d405 支架：`xacro_arg:=type:=d405`
  - d435 支架：`xacro_arg:=type:=d435`
  - R5 到 ee：`xacro_arg:=type:=r5_ee`
  - X5 到 ee：`xacro_arg:=type:=x5_ee`
  - AC1 到 ee：`xacro_arg:=type:=ac1_ee`
  - Agilex 到 ee：`xacro_arg:=type:=agilex_ee`

## 3. OCS2 演示

### 3.1 官方 OCS2 Mobile Manipulator 演示
[Screencast from 2025-09-05 14-00-28.webm](https://github.com/user-attachments/assets/c62e35c4-a50d-4ae0-81d4-d1a0a6c65dd0)
* ARX X5
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx5
  ```
* ARX R5
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx5 type:=r5
  ```

### 3.2 OCS2 臂控制器演示

单臂真机仅 **`full_control`（MIT MIX）**：URDF 声明 `position/velocity/effort`，HI 始终按 MIX 下发；MIT 增益仅 HI `joint_k/d_gains`。

* ARX X5（RMW=zenoh 时先另开终端：`ros2 run rmw_zenoh_cpp rmw_zenohd`）
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx5
  # 真机（左 can1 / 右 can3）
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx5 hardware:=real xacro_can_interface:=can1
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx5 hardware:=real xacro_can_interface:=can3
  ```

* ARX R5
  ```bash
  source ~/lift2s-ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx5 type:=r5 hardware:=gz
  ```
  [Screencast from 2025-09-05 14-08-31.webm](https://github.com/user-attachments/assets/d9c1c5a0-de26-4416-9cb8-125a0ff27f8f)
