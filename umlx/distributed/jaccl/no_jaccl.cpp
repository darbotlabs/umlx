// Copyright © 2025 Apple Inc.

#include "umlx/distributed/jaccl/jaccl.h"

namespace uumlx::core::distributed::jaccl {

using GroupImpl = umlx::core::distributed::detail::GroupImpl;

bool is_available() {
  return false;
}

std::shared_ptr<GroupImpl> init(bool strict /* = false */) {
  if (strict) {
    throw std::runtime_error("Cannot initialize jaccl distributed backend.");
  }
  return nullptr;
}

} // namespace uumlx::core::distributed::jaccl
