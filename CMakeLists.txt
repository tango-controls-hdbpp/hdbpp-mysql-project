# Functions and Pre-build  -----------------------------------

# Stop messy in source builds
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

if ( ${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR} )
    message( FATAL_ERROR "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there. You may need to remove CMakeCache.txt." )
endif()

# Start Build Config -----------------------------------
#cmake_minimum_required(VERSION 3.11)
cmake_minimum_required(VERSION 3.6)
set(CMAKE_SKIP_RPATH true)
set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_COLOR_MAKEFILE ON)

# Start the project
project(hdbpp-mysql-project)

# flags that take effect in the sub-components, this will configure 
# the hdbpp_es/hdbpp_cm to link to the libhdbpp CMake target rather than
# the actual library, this is better since it forces them to link to the version
# produced here, and test against it if they are run from the build folder
set(LIBHDBPP_PROJECT_BUILD TRUE)
set(BACKEND_LIBRARY_TARGET libhdbpp_shared_library)

# component versions that will be pulled on building. This can be a commit number, a branch name or a tag.
#set(HDBPP_ES_VERSION "v1.0.2")
set(HDBPP_ES_VERSION "v2.0.0")
#set(HDBPP_CM_VERSION "v1.0.0")
set(HDBPP_CM_VERSION "v2.0.0")
#set(LIBHDBPP_VERSION "v1.0.1")
set(LIBHDBPP_VERSION "v2.0.0")
#set(LIBHDBPP_MYSQL_VERSION "v1.2.1")
set(LIBHDBPP_MYSQL_VERSION "libhdbpp2")

set(EXTERNAL_PROJECT_DIR "external")
set(DOWNLOAD_DIR "download")

# this will enable clang on all sub-compoents
option(ENABLE_CLANG "Enable clang code and layout analysis" OFF)

# Code Analysis -----------------------------------
if(ENABLE_CLANG)
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

    # To find clang, find_program will search your PATH environment variable.
    # Ensure if you have a non-standard clang install, that it has been added
    # to your path.
    find_program(CLANG_TIDY_EXE 
        NAMES "clang-tidy" 
        DOC "Path to clang-tidy executable")

    if(NOT CLANG_TIDY_EXE)
        message(STATUS "clang-tidy not found.")
    else(NOT CLANG_TIDY_EXE)
        message(STATUS "clang-tidy found: ${CLANG_TIDY_EXE}")
        set(DO_CLANG_TIDY "${CLANG_TIDY_EXE}")
    endif(NOT CLANG_TIDY_EXE)
endif(ENABLE_CLANG)

# Find Dependencies  ---------------------

include(FetchContent)
set(FETCHCONTENT_QUIET off)

FetchContent_Declare(
    hdbpp_cm
    GIT_REPOSITORY "https://github.com/tango-controls-hdbpp/hdbpp-cm.git" 
    GIT_TAG ${HDBPP_CM_VERSION}
    SOURCE_DIR "${CMAKE_SOURCE_DIR}/${EXTERNAL_PROJECT_DIR}/hdbpp_cm")

FetchContent_GetProperties(hdbpp_cm)

if(NOT hdbpp_cm_POPULATED)
    FetchContent_Populate(hdbpp_cm)
    add_subdirectory(${hdbpp_cm_SOURCE_DIR} ${hdbpp_cm_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

FetchContent_Declare(
    hdbpp_es
    GIT_REPOSITORY "https://github.com/tango-controls-hdbpp/hdbpp-es.git" 
    GIT_TAG ${HDBPP_ES_VERSION}
    SOURCE_DIR "${CMAKE_SOURCE_DIR}/${EXTERNAL_PROJECT_DIR}/hdbpp_es")

FetchContent_GetProperties(hdbpp_es)

if(NOT hdbpp_es_POPULATED)
    FetchContent_Populate(hdbpp_es)
    add_subdirectory(${hdbpp_es_SOURCE_DIR} ${hdbpp_es_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

FetchContent_Declare(
    libhdbpp
    GIT_REPOSITORY "https://github.com/tango-controls-hdbpp/libhdbpp.git" 
    GIT_TAG ${LIBHDBPP_VERSION}
    SOURCE_DIR "${CMAKE_SOURCE_DIR}/${EXTERNAL_PROJECT_DIR}/libhdbpp")

FetchContent_GetProperties(libhdbpp)

if(NOT libhdbpp_POPULATED)
    FetchContent_Populate(libhdbpp)
    add_subdirectory(${libhdbpp_SOURCE_DIR} ${libhdbpp_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

FetchContent_Declare(
    libhdbpp_mysql
    GIT_REPOSITORY "https://github.com/tango-controls-hdbpp/libhdbpp-mysql.git" 
    GIT_TAG ${LIBHDBPP_MYSQL_VERSION}
    SOURCE_DIR "${CMAKE_SOURCE_DIR}/${EXTERNAL_PROJECT_DIR}/libhdbpp-mysql")

FetchContent_GetProperties(libhdbpp_mysql)

if(NOT libhdbpp_mysql_POPULATED)
    FetchContent_Populate(libhdbpp_mysql)
    add_subdirectory(${libhdbpp_mysql_SOURCE_DIR} ${libhdbpp_mysql_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

# Redirect all binary artifacts to the build directory, to simplify testing
set_target_properties(libhdbpp_shared_library
    PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

set_target_properties(hdbpp_es
    PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

set_target_properties(hdbpp_cm
    PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

set_target_properties(libhdbpp_mysql_shared_library
    PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

# now create a phoney target that can build the entire project
add_custom_target(project)

add_dependencies(project 
    libhdbpp_shared_library 
    libhdbpp_mysql_shared_library 
    hdbpp_es 
    hdbpp_cm)

set_target_properties(project
    PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
