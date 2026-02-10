# ARX X7S Description
This package contains the description files for ARX Lift. The origin models could be found at [ARX_Models](https://github.com/ARXroboticsX/ARX_Model)

## 1. Build
```bash
cd ~/ros2_ws
colcon build --packages-up-to arx_x7s_description --symlink-install
```

## 2. Visualize the robot

### 2.1 Full Robot

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_x7s
```

![arx x7s](../../.images/arx_x7s.png)

## 2.2 Components

* Base
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch robot_common_launch component.launch.py robot:=arx_x7s
  ```
  
## 3. OCS2 Demo
### 3.1 Official OCS2 Mobile Manipulator Demo
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch robot_common_launch manipulator_ocs2.launch.py robot_name:=arx_x7s 
```

### 3.2 OCS2 Arm Controller Demo

* Mock Components
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_x7s
  ```
* Isaac Sim
  ```bash
  source ~/ros2_ws/install/setup.bash
  ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_x7s hardware:=isaac
  ```