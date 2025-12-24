// Copyright © 2023-2024 Apple Inc.
#pragma once

#include "umlx/io.h"
#include "umlx/primitives.h"
#include "umlx/transforms.h"
#include "umlx/utils.h"

extern "C" {
#include <gguflib.h>
}

namespace uumlx::core {

Shape get_shape(const gguf_tensor& tensor);
void gguf_load_quantized(
    std::unordered_map<std::string, array>& a,
    const gguf_tensor& tensor);

} // namespace uumlx::core
