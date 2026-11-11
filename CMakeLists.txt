cmake_minimum_required(VERSION 3.8)
project(omron_moma_capabilities)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY interfaces semantic_interfaces
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY plans
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY providers
  DESTINATION share/${PROJECT_NAME}
)

ament_package()