// Copyright © 2023-2024 Apple Inc.

#pragma once

#include <future>
#include <memory>

#include "umlx/array.h"
#include "umlx/stream.h"

namespace uumlx::core::gpu {

void new_stream(Stream stream);
void eval(array& arr);
void finalize(Stream s);
void synchronize(Stream s);

} // namespace uumlx::core::gpu
