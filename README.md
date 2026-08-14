# 方舟机器人描述（ARX）

方舟（ARX）**全系**机器人描述包（URDF/xacro、meshes、ros2_control / OCS2 配置）。各机型产品清单以本仓为准。

上游聚合仓：[robot_descriptions](https://github.com/fiveages-sim/robot_descriptions)（子模块路径 `manipulator/ARX`）。

现场部署示例工作空间：**[lift2s-ws](https://github.com/fiveages-sim/open-deploy-ws)**（**ARX Lift2S Deploy Workspace**，克隆 `open-deploy-ws` 到 `~/lift2s-ws`）会拉取本仓作为 `src/robot-descriptions-arx`；该工作空间产品定位是 Lift2S，但可启动本仓内其他 ARX 机型做联调。

## 包一览

| 品牌 | 机型 | 分体 / 全身规划 | 图片 |
|------|------|----------------|------|
| ARX | [X5/R5](arx5_description/) | 仅臂（`demo.launch.py`） | <img src=".images/arx_x5.png" width="200"> <img src=".images/arx_r5.png" width="200"> |
| ARX | [AC One](arx_acone_description/) | 双臂躯干；Lift / Lift2S **分体规划**复用本包 | Dual-arm torso |
| ARX | [LIFT](arx_lift_description/) | 分体 → acone + 臂座 xyz；全身 → 本包 | <img src=".images/arx_lift.png" width="200"> |
| ARX | [LIFT2S](arx_lift2s_description/) | 分体 → acone；全身 → 本包 | <img src=".images/arx_lift2s_x5.png" width="200"> |
| ARX | [X7S](arx_x7s_description/) | 同包：`topology:=dual` / `full` | <img src=".images/arx_x7s.png" width="200"> |

在 **Lift2S Deploy Workspace**（`lift2s-ws`）中优先用 `./quick_start.sh`。各包 README 也给出 `ros2 launch` 示例（路径多为 `~/lift2s-ws`，或通用 `~/ros2_ws`）。

## 用法

将本仓库作为工作区子模块加入（推荐路径见 [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) 的 `manipulator/ARX`）。colcon 会扫描该树下的包。

```bash
# 经 robot_descriptions
git submodule update --init manipulator/ARX

# 或单独加入
git submodule add -b main git@github.com:fiveages-sim/robot-descriptions-arx.git src/robot-descriptions-arx
```

启动前先 source：

```bash
cd ~/lift2s-ws
colcon build --packages-up-to arx5_description --symlink-install
source ~/lift2s-ws/install/setup.bash
```

可视化 / OCS2 demo 详见各包 README。

## 相关仓库

- 聚合仓：[robot_descriptions](https://github.com/fiveages-sim/robot_descriptions)
- 通用组件：[robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common)
- 控制器 / HI：[arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)、[arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control)
- Lift2S 部署工作空间：[open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)（本地目录名常用 `lift2s-ws`）
