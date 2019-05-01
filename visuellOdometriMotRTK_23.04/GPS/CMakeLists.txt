cmake_minimum_required(VERSION 2.8.9)
project(libsbp_tcp_example)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

add_executable(libsbp_tcp_example tcp_example.cpp)

find_package(PkgConfig)

link_directories("/usr/local/lib/")
include_directories("/usr/local/include/")

target_link_libraries(libsbp_tcp_example sbp)
