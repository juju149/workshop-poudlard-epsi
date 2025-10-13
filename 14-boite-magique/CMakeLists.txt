cmake_minimum_required(VERSION 3.15)

project(MagicBox VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Platform-specific settings
if(WIN32)
    # Windows specific settings
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    message(STATUS "Configuring for Windows platform")
elseif(UNIX AND NOT APPLE)
    # Linux specific settings
    message(STATUS "Configuring for Linux platform")
elseif(APPLE)
    # macOS specific settings
    message(STATUS "Configuring for macOS platform")
endif()

# Compiler warnings
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# Source files
set(SOURCES
    src/main.cpp
    src/MagicBox.cpp
)

set(HEADERS
    include/MagicBox.h
)

# Create executable
add_executable(magic-box ${SOURCES} ${HEADERS})

# Link libraries
if(WIN32)
    # Windows may need additional libraries
    target_link_libraries(magic-box)
else()
    # Unix-like systems need stdc++fs for some older compilers
    target_link_libraries(magic-box stdc++fs)
endif()

# Installation rules
install(TARGETS magic-box
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install documentation
install(FILES
    ${CMAKE_SOURCE_DIR}/README.md
    DESTINATION share/doc/magic-box
)

# Print configuration summary
message(STATUS "")
message(STATUS "========================================")
message(STATUS "  Magic Box Configuration Summary")
message(STATUS "========================================")
message(STATUS "  Project: ${PROJECT_NAME}")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Install Prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "========================================")
message(STATUS "")
