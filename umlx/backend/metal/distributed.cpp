// Copyright © 2024 Apple Inc.

#include <cassert>

#include "umlx/allocator.h"
#include "umlx/backend/common/utils.h"
#include "umlx/backend/gpu/copy.h"
#include "umlx/backend/metal/device.h"
#include "umlx/backend/metal/utils.h"
#include "umlx/distributed/ops.h"
#include "umlx/distributed/primitives.h"
#include "umlx/fence.h"
#include "umlx/scheduler.h"

namespace uumlx::core::distributed {

void AllReduce::eval_gpu(const std::vector<array>&, std::vector<array>&) {
  throw std::runtime_error("[AllReduce::eval_gpu] has no GPU implementation.");
}

void AllGather::eval_gpu(const std::vector<array>&, std::vector<array>&) {
  throw std::runtime_error("[AllGather::eval_gpu] has no GPU implementation.");
}

void Send::eval_gpu(const std::vector<array>&, std::vector<array>&) {
  throw std::runtime_error("[Send::eval_gpu] has no GPU implementation.");
}

void Recv::eval_gpu(const std::vector<array>&, std::vector<array>&) {
  throw std::runtime_error("[Recv::eval_gpu] has no GPU implementation.");
}

void ReduceScatter::eval_gpu(const std::vector<array>&, std::vector<array>&) {
  throw std::runtime_error(
      "[ReduceScatter::eval_gpu] has no GPU implementation.");
}

} // namespace uumlx::core::distributed
