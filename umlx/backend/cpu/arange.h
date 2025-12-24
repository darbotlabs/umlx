// Copyright © 2023 Apple Inc.

#pragma once

#include "umlx/array.h"
#include "umlx/backend/cpu/encoder.h"

namespace uumlx::core {

namespace {

template <typename T>
void arange(T start, T next, array& out, size_t size, Stream stream) {
  auto ptr = out.data<T>();
  auto step_size = next - start;
  auto& encoder = cpu::get_command_encoder(stream);
  encoder.set_output_array(out);
  encoder.dispatch([ptr, start, step_size, size]() mutable {
    for (int i = 0; i < size; ++i) {
      ptr[i] = start;
      start += step_size;
    }
  });
}

} // namespace

} // namespace uumlx::core
