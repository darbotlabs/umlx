// Copyright © 2025 Apple Inc.

#include <stdexcept>

#include "umlx/backend/gpu/available.h"
#include "umlx/backend/gpu/eval.h"

namespace uumlx::core::gpu {

bool is_available() {
  return false;
}

void new_stream(Stream) {}

void eval(array&) {
  throw std::runtime_error("[gpu::eval] GPU backend is not available");
}

void finalize(Stream) {
  throw std::runtime_error("[gpu::finalize] GPU backend is not available");
}

void synchronize(Stream) {
  throw std::runtime_error("[gpu::synchronize]  GPU backend is not available");
}

} // namespace uumlx::core::gpu
