cmake_minimum_required(VERSION 3.16)
project(BARF VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Options
option(BARF_BUILD_PYTHON "Build Python bindings" ON)
option(BARF_BUILD_TESTS "Build tests" OFF)

# Find dependencies
find_package(ROOT REQUIRED COMPONENTS Core RIO Tree Hist TreePlayer ROOTDataFrame)
find_package(TBB REQUIRED)
find_package(Eigen3 REQUIRED)

# Boost.Histogram is header-only but we need to find the include path
find_path(BOOST_HISTOGRAM_INCLUDE_DIR
    NAMES boost/histogram.hpp
    PATHS 
        /usr/include
        /usr/local/include
        $ENV{CONDA_PREFIX}/include
        $ENV{PREFIX}/include
    DOC "Path to Boost.Histogram headers"
)

if(NOT BOOST_HISTOGRAM_INCLUDE_DIR)
    message(FATAL_ERROR "Boost.Histogram headers not found. Please install boost-histogram.")
endif()

# Create BARF library as INTERFACE (header-only)
add_library(barf INTERFACE)
add_library(BARF::barf ALIAS barf)

# Include directories
target_include_directories(barf INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/narf/include>
    $<INSTALL_INTERFACE:include/barf>
    ${BOOST_HISTOGRAM_INCLUDE_DIR}
    ${EIGEN3_INCLUDE_DIR}
)

# Link dependencies
target_link_libraries(barf INTERFACE
    ROOT::Core
    ROOT::RIO
    ROOT::Tree
    ROOT::Hist
    ROOT::TreePlayer
    ROOT::ROOTDataFrame
    TBB::tbb
    Eigen3::Eigen
)

# Compile definitions
target_compile_definitions(barf INTERFACE
    $<$<CONFIG:Release>:NDEBUG>
)

# Compile options
target_compile_options(barf INTERFACE
    -O3
    -Wall
    -Wextra
)

# Installation
include(GNUInstallDirs)

install(TARGETS barf
    EXPORT BARFTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Install headers
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/narf/include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/barf
    FILES_MATCHING PATTERN "*.hpp" PATTERN "*.h"
)

# Install Python module
if(BARF_BUILD_PYTHON)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/narf/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/python/narf
        FILES_MATCHING PATTERN "*.py"
    )
endif()

# Export targets
install(EXPORT BARFTargets
    FILE BARFTargets.cmake
    NAMESPACE BARF::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/BARF
)

# Create and install package config file
include(CMakePackageConfigHelpers)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/BARFConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/BARFConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/BARFConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/BARF
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/BARFConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/BARFConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/BARF
)

# Tests
if(BARF_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
