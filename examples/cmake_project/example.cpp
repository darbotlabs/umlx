// Copyright © 2024 Apple Inc.

#include <iostream>

#include "umlx/umlx.h"

namespace mx = umlx::core;

int main() {
  auto x = mx::array({1, 2, 3});
  auto y = mx::array({1, 2, 3});
  std::cout << x + y << std::endl;
  return 0;
}
