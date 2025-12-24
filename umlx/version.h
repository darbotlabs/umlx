// Copyright © 2025 UMLX Contributors
// Based on MLX © 2023-2025 Apple Inc.

#pragma once

#define UMLX_VERSION_MAJOR 0
#define UMLX_VERSION_MINOR 30
#define UMLX_VERSION_PATCH 3
#define UMLX_VERSION_NUMERIC \
  (100000 * UMLX_VERSION_MAJOR + 1000 * UMLX_VERSION_MINOR + UMLX_VERSION_PATCH)

namespace uumlx::core {

/* A string representation of the UMLX version in the format
 * "major.minor.patch".
 *
 * For dev builds, the version will include the suffix ".devYYYYMMDD+hash"
 */
const char* version();

} // namespace uumlx::core
