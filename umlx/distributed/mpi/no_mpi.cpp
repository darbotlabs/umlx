// Copyright © 2024 Apple Inc.

#include "umlx/distributed/mpi/mpi.h"

namespace uumlx::core::distributed::mpi {

using GroupImpl = umlx::core::distributed::detail::GroupImpl;

bool is_available() {
  return false;
}

std::shared_ptr<GroupImpl> init(bool strict /* = false */) {
  if (strict) {
    throw std::runtime_error("Cannot initialize MPI");
  }
  return nullptr;
}

} // namespace uumlx::core::distributed::mpi
