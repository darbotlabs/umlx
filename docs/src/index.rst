UMLX
====

UMLX (Universal MLX) is a NumPy-like array framework designed for efficient and 
flexible machine learning across multiple platforms. Based on Apple's MLX framework,
UMLX extends support to x64, ARM, Nvidia CUDA, and AMD ROCM for GPU and NPU acceleration.

The Python API closely follows NumPy with a few exceptions. UMLX also has a
fully featured C++ API which closely follows the Python API.

The main features of UMLX include:

 - **Cross-Platform Support**: UMLX runs on Apple Silicon (Metal), Nvidia GPUs 
   (CUDA), AMD GPUs (ROCM), x64 CPUs, and ARM processors including NPUs.
 - **Composable function transformations**: UMLX has composable function
   transformations for automatic differentiation, automatic vectorization,
   and computation graph optimization.
 - **Lazy computation**: Computations in UMLX are lazy. Arrays are only
   materialized when needed.
 - **Multi-device**: Operations can run on any of the supported devices (CPU,
   GPU, NPU)
 - **REST API**: Complete FastAPI integration exposes functionality via REST API
   on port 1023.

The design of UMLX builds upon MLX and is inspired by frameworks like `PyTorch
<https://pytorch.org/>`_, `Jax <https://github.com/google/jax>`_, and
`ArrayFire <https://arrayfire.org/>`_. UMLX extends the *unified memory model*
where possible. Arrays in UMLX live in shared memory on supported platforms.
Operations on UMLX arrays can be performed on any of the supported device types
without performing data copies where hardware supports it. Currently supported 
device types include CPU, GPU (Metal/CUDA/ROCM), and NPU.

.. toctree::
   :caption: Install
   :maxdepth: 1

   install
   platforms

.. toctree::
   :caption: Usage 
   :maxdepth: 1

   usage/quick_start
   usage/lazy_evaluation
   usage/unified_memory
   usage/indexing
   usage/saving_and_loading
   usage/function_transforms
   usage/compile
   usage/numpy
   usage/distributed
   usage/using_streams
   usage/export
   api

.. toctree::
   :caption: Examples
   :maxdepth: 1

   examples/linear_regression
   examples/mlp
   examples/llama-inference

.. toctree::
   :caption: Python API Reference
   :maxdepth: 1

   python/array
   python/data_types
   python/devices_and_streams
   python/export
   python/ops
   python/random
   python/transforms
   python/fast
   python/fft
   python/linalg
   python/metal
   python/cuda
   python/memory_management
   python/nn
   python/optimizers
   python/distributed
   python/tree_utils

.. toctree::
   :caption: C++ API Reference
   :maxdepth: 1

   cpp/ops

.. toctree::
   :caption: Further Reading
   :maxdepth: 1

   dev/extensions
   dev/metal_debugger
   dev/metal_logging
   dev/custom_metal_kernels
   dev/mlx_in_cpp
