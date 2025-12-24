// Copyright © 2025 Apple Inc.

#pragma once

#if defined(__METAL_VERSION__) && (__METAL_VERSION__ >= 320)
#include <metal_logging>

namespace umlx {
using os_log = metal::os_log;
} // namespace umlx

#else

namespace umlx {
struct os_log {
  constexpr os_log(constant char*, constant char*) constant {}

  template <typename... Args>
  void log_debug(constant char*, Args...) const {}

  template <typename... Args>
  void log_debug(constant char*, Args...) const constant {}
};
} // namespace umlx

#endif