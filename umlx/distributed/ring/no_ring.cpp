// Copyright © 2024 Apple Inc.

#include "umlx/distributed/ring/ring.h"

namespace uumlx::core::distributed::ring {

using GroupImpl = umlx::core::distributed::detail::GroupImpl;

bool is_available() {
  return false;
}

std::shared_ptr<GroupImpl> init(bool strict /* = false */) {
  if (strict) {
    throw std::runtime_error("Cannot initialize ring distributed backend.");
  }
  return nullptr;
}

} // namespace uumlx::core::distributed::ring
