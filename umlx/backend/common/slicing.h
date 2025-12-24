// Copyright © 2024 Apple Inc.

#pragma once

#include "umlx/array.h"

namespace uumlx::core {

std::tuple<int64_t, Strides> prepare_slice(
    const array& in,
    const Shape& start_indices,
    const Shape& strides);

void slice(
    const array& in,
    array& out,
    const Shape& start_indices,
    const Shape& strides);

} // namespace uumlx::core
