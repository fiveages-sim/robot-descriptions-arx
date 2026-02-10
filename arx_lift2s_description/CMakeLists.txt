cmake_minimum_required(VERSION 3.8)

project(arx_lift2s_description)

find_package(ament_cmake REQUIRED)

install(
		DIRECTORY config meshes urdf xacro
		DESTINATION share/${PROJECT_NAME}/
)

ament_package()

