#!/usr/bin/env python3
"""
LIFT2S official-line OCS2 launch (arxlift2s_ros2_control).

Includes upstream split_body.launch.py (ocs2_arm + body_lift via enable_body).
No chassis: ArxLiftHardware does not export chassis GPIO.

Usage:
  ros2 launch arx_lift2s_description ocs2_real.launch.py
  ros2 launch arx_lift2s_description ocs2_real.launch.py hardware:=real
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    split_body = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ocs2_arm_controller"),
                "launch",
                "split_body.launch.py",
            )
        ),
        launch_arguments={
            "robot": LaunchConfiguration("robot"),
            "type": LaunchConfiguration("type"),
            "hardware": LaunchConfiguration("hardware"),
            "enable_body": LaunchConfiguration("enable_body"),
            "enable_gripper": LaunchConfiguration("enable_gripper"),
            "enable_arms_target_manager": LaunchConfiguration(
                "enable_arms_target_manager"
            ),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("robot", default_value="arx_lift2s"),
            DeclareLaunchArgument("type", default_value=""),
            DeclareLaunchArgument(
                "hardware",
                default_value="real",
                description="real → arxlift2s_ros2_control (left/right/lift systems)",
            ),
            DeclareLaunchArgument("enable_body", default_value="true"),
            DeclareLaunchArgument("enable_gripper", default_value="true"),
            DeclareLaunchArgument("enable_arms_target_manager", default_value="true"),
            DeclareLaunchArgument("use_sim_time", default_value="false"),
            split_body,
        ]
    )
