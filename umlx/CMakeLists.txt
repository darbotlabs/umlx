target_sources(
  umlx
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/array.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/compile.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/device.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/dtype.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/dtype_utils.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/export.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/einsum.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/fast.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/fft.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/ops.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/graph_utils.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/primitives.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/random.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/scheduler.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/transforms.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/utils.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/linalg.cpp
          ${CMAKE_CURRENT_SOURCE_DIR}/backend/metal/metal.h)

# Define UMLX_VERSION only in the version.cpp file.
add_library(mlx_version OBJECT ${CMAKE_CURRENT_SOURCE_DIR}/version.cpp)
target_compile_definitions(mlx_version PRIVATE UMLX_VERSION="${UMLX_VERSION}")
target_link_libraries(umlx PRIVATE $<BUILD_INTERFACE:mlx_version>)

if(MSVC)
  # Disable some MSVC warnings to speed up compilation.
  target_compile_options(umlx PUBLIC /wd4068 /wd4244 /wd4267 /wd4804)
endif()

if(WIN32)
  # Export symbols by default to behave like macOS/linux.
  set_target_properties(umlx PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/common)

if(UMLX_BUILD_CPU)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/cpu)
else()
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/no_cpu)
endif()

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/distributed)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/io)

if(UMLX_BUILD_METAL)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/metal)
else()
  target_sources(umlx
                 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/backend/metal/no_metal.cpp)
endif()

if(UMLX_BUILD_CUDA)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/cuda)
else()
  target_sources(umlx
                 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/backend/cuda/no_cuda.cpp)
endif()

if(UMLX_BUILD_METAL OR UMLX_BUILD_CUDA)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/gpu)
else()
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/backend/no_gpu)
endif()
