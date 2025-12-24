// Copyright © 2024 Apple Inc.

#include "umlx/distributed/nccl/nccl.h"

namespace uumlx::core::distributed::nccl {

using GroupImpl = umlx::core::distributed::detail::GroupImpl;

bool is_available() {
  return false;
}

std::shared_ptr<GroupImpl> init(bool strict /* = false */) {
  if (strict) {
    throw std::runtime_error("Cannot initialize nccl distributed backend.");
  }
  return nullptr;
}

} // namespace uumlx::core::distributed::nccl
