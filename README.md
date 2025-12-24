# UMLX - Universal MLX

[**Quickstart**](#quickstart) | [**Installation**](#installation) |
[**Documentation**](https://github.com/darbotlabs/umlx) |
[**Examples**](#examples) | [**API**](#api)

UMLX (Universal MLX) is an enhanced array framework for machine learning with cross-platform support including Apple Silicon, x64, ARM, Nvidia CUDA, and AMD ROCM for GPU and NPU acceleration.

Originally based on Apple's MLX framework, UMLX extends support to a universal set of hardware platforms while maintaining API compatibility.

Some key features of UMLX include:

- **Cross-Platform Support**: UMLX runs on Apple Silicon (Metal), Nvidia GPUs (CUDA), AMD GPUs (ROCM), x64 CPUs, and ARM processors including NPUs.

- **Familiar APIs**: UMLX maintains API compatibility with MLX, closely following NumPy conventions. It includes fully featured Python, C++, [C](https://github.com/ml-explore/mlx-c), and
   [Swift](https://github.com/ml-explore/mlx-swift/) APIs. Higher-level packages like `mlx.nn` and
   `mlx.optimizers` follow PyTorch patterns for building complex models.

- **REST API Integration**: Complete FastAPI integration exposes all functionality via REST API on port 1023.

- **Hardware Configurations**: 
  - DGX Spark containers with Nvidia Workbench optimizations
  - AMD ROCM with unified memory architecture (x64 + 128GB unified memory + NPU)
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

- **Multi-device**: Operations can run on any supported device: CPU, GPU (Metal/CUDA/ROCM), and NPU.

- **Unified memory**: UMLX extends MLX's unified memory model across platforms. Arrays live in shared memory where supported (Apple Silicon, AMD unified architecture), enabling efficient operations without data transfer.

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
import mlx.core as mx

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
python -m mlx.api.server
```

API endpoints provide access to:
- Array operations
- Model inference
- Training utilities
- Device management

See the [API documentation](https://github.com/darbotlabs/umlx/tree/main/docs) for detailed endpoint information.

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

For AMD GPU support (coming soon):

```bash
pip install umlx[rocm]
```

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
