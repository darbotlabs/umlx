// Copyright © 2025 Apple Inc.
#include "umlx/backend/cpu/eval.h"
#include "umlx/backend/cpu/encoder.h"
#include "umlx/primitives.h"
#include "umlx/scheduler.h"
#include "umlx/utils.h"

namespace uumlx::core::cpu {

void eval(array& arr) {
  auto s = arr.primitive().stream();

  auto outputs = arr.outputs();
  {
    // If the array is a tracer hold a reference
    // to its inputs so they don't get donated
    std::vector<array> inputs;
    if (arr.is_tracer()) {
      inputs = arr.inputs();
    }
    arr.primitive().eval_cpu(arr.inputs(), outputs);
  }

  std::unordered_set<std::shared_ptr<array::Data>> buffers;
  for (auto& in : arr.inputs()) {
    buffers.insert(in.data_shared_ptr());
  }
  for (auto& s : arr.siblings()) {
    buffers.insert(s.data_shared_ptr());
  }
  // Remove the output if it was donated to by an input
  if (auto it = buffers.find(arr.data_shared_ptr()); it != buffers.end()) {
    buffers.erase(it);
  }
  auto& encoder = cpu::get_command_encoder(s);
  encoder.dispatch([buffers = std::move(buffers),
                    temps = std::move(encoder.temporaries())]() {});
}

} // namespace uumlx::core::cpu
