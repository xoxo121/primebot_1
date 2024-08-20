cmake_minimum_required(VERSION 3.5)
project(primebot_1)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Install Python package
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(
  PROGRAMS
  primebot_1/line_follower_node.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY config description launch worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
