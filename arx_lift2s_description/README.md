# ARX Lift 2S Description

This package contains the description files for ARX Lift 2S. 

## 1. Build

```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_lift2s_description --symlink-install
```

## 2. Visualize the robot

### 2.1 Full Lift 2S

* Lift with X5 Arm
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
  ```

* Lift with R5 Arm
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s type:="r5"
  ```

### 2.1 AC One Config

* AC One with X5 Arm
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s type:="acone_x5"
  ```

* AC One with R5 Arm
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s type:="acone_r5"
  ```


## 2.2 Components

* chassis
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_lift2s
  ```
* AC One Base
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_lift2s type:=ac_one
  ```
* Wheel
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_lift2s type:=wheel
  ```

## 3. OCS2 Demo

### 3.1 Official OCS2 Mobile Manipulator Demo

* Lift with X5 Arm
    ```bash
    source ~/ros2_ws/install/setup.bash
    ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx_lift2s
    ```
* Lift with R5 Arm
   ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx_lift2s type:=r5
    ```

### 3.2 OCS2 Arm Controller Demo

* Mock Components
  ```bash
  # Lift with X5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s
  ```
  ```bash
  # Lift with R5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s type:=r5
  ```
  ```bash
  # AC-one and X5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s type:=acone_x5
  ```

* Gazebo
  ```bash
  # Lift2S with R5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s type:=r5 hardware:=gz world:=dart
  ```

* Isaac Sim Launch
  ```bash
  # Lift2S with X5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s hardware:=isaac
  ```
  ```bash
  # AC-one and X5 Arm
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_lift2s type:=acone_x5 hardware:=isaac
  ```
  