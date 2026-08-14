cmake_minimum_required(VERSION 3.14)
project(arx_x7s_arms_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config xacro
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
