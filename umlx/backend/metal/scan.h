#pragma once

#include "umlx/array.h"
#include "umlx/primitives.h"

namespace uumlx::core {

void scan_gpu_inplace(
    array in,
    array& out,
    Scan::ReduceType reduce_type,
    int axis,
    bool reverse,
    bool inclusive,
    const Stream& s);

} // namespace uumlx::core
