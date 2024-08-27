# The SWIG functions/macros used in this module, swig_add_module and swig_add_library
# are not available in CMake versions earlier than 3.8
cmake_minimum_required(VERSION 3.8)

project(iec61850_project)

# 设置 C++ 标准为 C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 显式指定 Python 3 解释器路径
set(Python3_EXECUTABLE /usr/local/bin/python3.8)  # 请根据实际路径调整


# 查找 Python 3 和库
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

find_package(PythonInterp 3.8 REQUIRED)
find_package(PythonLibs 3.8 REQUIRED)

include_directories(/usr/local/include/python3.8)


# 设置包含路径
include_directories(/usr/local/include/libiec61850/)

# 链接库路径
link_directories(/usr/local/lib)

# 设置SWIG库生成
find_package(Python3 REQUIRED)

set(SWIG_INCLUDE_DIRS /usr/local/include/libiec61850/)

# 找到并配置 SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

find_package(PythonInterp ${BUILD_PYTHON_VERSION} REQUIRED)
find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)

include_directories(${PYTHON_INCLUDE_PATH})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

set(CMAKE_SWIG_FLAGS "")
set_property(SOURCE iec61850.i PROPERTY CPLUSPLUS ON)

if(WIN32)
    set(LIBS iec61850 ws2_32)
else()
    set(LIBS iec61850)
endif()

# 创建 SWIG 库/模块
if(${CMAKE_VERSION} VERSION_LESS 3.8)
    swig_add_module(iec61850 python iec61850.i)
else()
    swig_add_library(iec61850
        LANGUAGE python
        SOURCES iec61850.i
    )
endif()

# 链接所需的库
swig_link_libraries(iec61850 ${PYTHON_LIBRARIES} ${LIBS})

# Finding python modules install path
execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -c
    "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib())"
    OUTPUT_VARIABLE PYTHON_SITE_DIR
)

# 安装生成的 Python 模块
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/iec61850.py DESTINATION ${PYTHON_SITE_DIR})
install(TARGETS _iec61850 LIBRARY DESTINATION ${PYTHON_SITE_DIR})

# 添加测试
add_test(test_pyiec61850 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/test_pyiec61850.py)
