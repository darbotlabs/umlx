// Copyright © 2025 Apple Inc.

#pragma once

#include "umlx/backend/cuda/device.h"

namespace uumlx::core::cu {

bool can_use_gemv(int M, int N, int K, bool a_transposed, bool b_transposed);

void gemv(
    const array& a,
    const array& b,
    array& out,
    int M,
    int N,
    int K,
    uint32_t batch_count,
    const umlx::core::Shape& batch_shape,
    const umlx::core::Strides& a_batch_strides,
    const umlx::core::Strides& b_batch_strides,
    CommandEncoder& encoder);

} // namespace uumlx::core::cu
