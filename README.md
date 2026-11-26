# UMLX - Universal MLX

[**Quickstart**](#quickstart) | [**Installation**](#installation) |
[**Documentation**](https://github.com/darbotlabs/umlx) |
[**Examples**](#examples) | [**API**](#api)

UMLX (Universal MLX) is a research fork of Apple MLX targeting heterogeneous hardware. The current source contains CPU, Metal, and CUDA backends. ROCm and NPU acceleration are roadmap items; backend source does not by itself establish tested wheels for every OS and architecture.

Originally based on Apple's MLX framework, UMLX extends support to a universal set of hardware platforms while maintaining API compatibility.

Some key features of UMLX include:

- **Backend implementation**: CPU, Apple Metal, and Nvidia CUDA code is present. AMD ROCm and NPU backends are not implemented in this tree.

- **Familiar APIs**: UMLX follows the MLX/NumPy array API design with Python and C++ interfaces. The upstream [C](https://github.com/ml-explore/mlx-c) and [Swift](https://github.com/ml-explore/mlx-swift/) projects are references, not verified bindings to the renamed UMLX runtime. Higher-level packages like `umlx.nn` and
   `umlx.optimizers` follow PyTorch patterns for building complex models.

- **REST API Integration**: FastAPI exposes array creation and binary operations, device selection, and optional single-turn LLM providers. It binds to loopback on port 1023 by default.

- **Hardware Targets** (validate each build and device combination):
  - DGX Spark containers with Nvidia Workbench optimizations
  - AMD unified-memory GPU/NPU configurations (future backend work)
  - Nvidia GPUs with CUDA Toolkit (Compute Capability 7.5+)
  - ARM Processors (expanded from x86_64-only support)
  - AMD Threadripper CPU/RAM configurations

- **Composable function transformations**: MLX supports composable function
  transformations for automatic differentiation, automatic vectorization,
  and computation graph optimization.

- **Lazy computation**: Computations in MLX are lazy. Arrays are only
  materialized when needed.

- **Dynamic graph construction**: Computation graphs in MLX are constructed
  dynamically. Changing the shapes of function arguments does not trigger
  slow compilations, and debugging is simple and intuitive.

- **Multi-device**: CPU and GPU operations depend on the compiled backend (Metal or CUDA).

- **Unified memory**: UMLX inherits MLX memory behavior for its implemented backends. Physical CPU/GPU memory sharing and transfer costs depend on the backend and hardware; AMD shared RAM does not implement ROCm or NPU execution.

UMLX is designed to provide a universal machine learning framework across diverse hardware platforms. The framework maintains ease of use while being efficient for training and deploying models across x64, ARM, Apple Silicon, Nvidia, and AMD hardware.

The design of UMLX builds upon frameworks like MLX,
[NumPy](https://numpy.org/doc/stable/index.html),
[PyTorch](https://pytorch.org/), [Jax](https://github.com/google/jax), and
[ArrayFire](https://arrayfire.org/).

## Examples

The [UMLX examples](https://github.com/darbotlabs/umlx/tree/main/examples) include:

- [Transformer language model](https://github.com/darbotlabs/umlx/tree/main/examples) training
- Linear and logistic regression examples
- Python extensions and bindings
- Model export examples

For more comprehensive examples, see the original [MLX examples repo](https://github.com/ml-explore/mlx-examples).

## Quickstart

### Basic Array Operations

```python
import umlx.core as mx

# Create arrays
a = mx.array([1, 2, 3, 4])
b = mx.array([5, 6, 7, 8])

# Perform operations
c = a + b
print(c)
```

See the [quick start guide](https://github.com/darbotlabs/umlx/tree/main/docs) for more information.

## API

UMLX includes a FastAPI-based REST API for accessing functionality remotely:

```bash
# Start the API server (default port 1023)
python -m umlx.api.server
```

API endpoints provide access to:
- Array operations
- Optional single-turn text generation through Apple Foundation Models or a local MLX-LM server
- Device management

See the [API documentation](https://github.com/darbotlabs/umlx/tree/main/docs) for detailed endpoint information.

## Apple Foundation Models and MLX-LM

See [the integration research and runbook](docs/APPLE_FM_MLX_INTEGRATION.md) for
source evidence, setup, limitations, and the hardware validation matrix.

```bash
# Run from a source checkout without compiling the array extension:
PYTHONPATH=python python -m umlx.llm available
PYTHONPATH=python python -m umlx.llm probe-fm
```

The optional provider layer uses `apple-fm-sdk` for Apple's on-device model and
loopback HTTP for MLX-LM. It does not port Apple model weights, enable PCC,
or replace `mlx.*` imports with `umlx.*` inside third-party packages.

## Installation

### Apple Silicon (macOS)

UMLX is available on [PyPI](https://pypi.org/project/umlx/). To install on macOS with Metal support:

```bash
pip install umlx
```

### Linux with CUDA (Nvidia)

For Nvidia GPU support with CUDA Toolkit:

```bash
pip install umlx[cuda]
```

Supports CUDA Toolkit 12 and 13 with Compute Capability 7.5+ (Turing, Ampere, Ada Lovelace, Hopper, Blackwell).

### Linux with ROCM (AMD)

ROCm is planned. This tree has no ROCm backend or `rocm` installation extra; do not treat `pip install umlx[rocm]` as an implemented GPU path.

### CPU-Only (x64/ARM)

For CPU-only installations on x64 or ARM processors:

```bash
pip install umlx[cpu]
```

### Building from Source

See the [build documentation](https://github.com/darbotlabs/umlx/tree/main/docs) for platform-specific build instructions including:
- DGX Spark containers with Nvidia Workbench
- AMD unified memory configurations
- ARM processor builds
- Custom optimizations

## Contributing

Check out the [contribution guidelines](https://github.com/darbotlabs/umlx/tree/main/CONTRIBUTING.md) for more information on contributing to UMLX. See the [docs](https://github.com/darbotlabs/umlx/tree/main/docs) for more information on building from source and running tests.

We are grateful for all [contributors](https://github.com/darbotlabs/umlx/tree/main/ACKNOWLEDGMENTS.md). If you contribute to UMLX and wish to be acknowledged, please add your name to the list in your pull request.

## Citing UMLX

UMLX builds upon the MLX framework originally developed by Apple machine learning research. If you use UMLX in your research, please cite both UMLX and the original MLX work:

```text
@software{umlx2025,
  author = {Darbot Labs Contributors},
  title = {{UMLX}: Universal MLX - Cross-platform machine learning framework},
  url = {https://github.com/darbotlabs/umlx},
  version = {0.30},
  year = {2025},
}

@software{mlx2023,
  author = {Awni Hannun and Jagrit Digani and Angelos Katharopoulos and Ronan Collobert},
  title = {{MLX}: Efficient and flexible machine learning on Apple silicon},
  url = {https://github.com/ml-explore},
  version = {0.0},
  year = {2023},
}
```

## License

UMLX is released under the MIT License. See [LICENSE](LICENSE) for details.
