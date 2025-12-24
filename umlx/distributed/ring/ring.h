// Copyright © 2024 Apple Inc.

#include "umlx/distributed/distributed.h"

namespace uumlx::core::distributed::ring {

using GroupImpl = umlx::core::distributed::detail::GroupImpl;

bool is_available();
std::shared_ptr<GroupImpl> init(bool strict = false);

} // namespace uumlx::core::distributed::ring
