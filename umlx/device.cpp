// Copyright © 2023 Apple Inc.

#include <stdexcept>

#include "umlx/backend/cpu/available.h"
#include "umlx/backend/gpu/available.h"
#include "umlx/device.h"

namespace uumlx::core {

Device& mutable_default_device() {
  static Device default_device{gpu::is_available() ? Device::gpu : Device::cpu};
  return default_device;
}

const Device& default_device() {
  return mutable_default_device();
}

void set_default_device(const Device& d) {
  if (!gpu::is_available() && d == Device::gpu) {
    throw std::invalid_argument(
        "[set_default_device] Cannot set gpu device without gpu backend.");
  }
  mutable_default_device() = d;
}

bool operator==(const Device& lhs, const Device& rhs) {
  return lhs.type == rhs.type && lhs.index == rhs.index;
}

bool operator!=(const Device& lhs, const Device& rhs) {
  return !(lhs == rhs);
}

bool is_available(const Device& d) {
  switch (d.type) {
    case Device::cpu:
      return cpu::is_available();
    case Device::gpu:
      return gpu::is_available();
  }
  // appease compiler
  return false;
}

} // namespace uumlx::core
