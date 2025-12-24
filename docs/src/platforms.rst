.. _platform_support:

Platform Support
================

UMLX provides cross-platform support for a wide range of hardware configurations,
extending beyond Apple Silicon to include x64, ARM, Nvidia CUDA, and AMD ROCM platforms.

Supported Platforms
-------------------

Apple Silicon (Metal)
^^^^^^^^^^^^^^^^^^^^^

**Devices**: M1, M2, M3, M4 series chips

**Features**:
- Native unified memory architecture
- Metal GPU acceleration
- Efficient CPU/GPU operation switching
- Neural Engine support where available

**Requirements**:
- macOS >= 14.0
- Native Python >= 3.10

**Installation**:

.. code-block:: shell

    pip install umlx

**Best For**: Development, inference, and training on Mac workstations

Nvidia CUDA
^^^^^^^^^^^

**Devices**: Nvidia GPUs with Compute Capability >= 7.5

Supported architectures:
- Turing (SM 7.5) - RTX 20 series, T4
- Ampere (SM 8.0) - RTX 30 series, A100, A40
- Ada Lovelace (SM 8.9) - RTX 40 series, L4, L40
- Hopper (SM 9.0a) - H100, H200
- Blackwell (SM 10.0a) - B100, B200

**Features**:
- CUDA Toolkit integration (12.x, 13.x)
- cuDNN acceleration
- NCCL for multi-GPU training
- Tensor Core utilization

**Requirements**:
- Nvidia driver >= 550.54.14 (CUDA 12) or >= 580 (CUDA 13)
- Linux with glibc >= 2.35
- Python >= 3.10

**Installation**:

.. code-block:: shell

    # CUDA 12
    pip install umlx[cuda12]
    
    # CUDA 13
    pip install umlx[cuda13]

**DGX Spark Containers**:

UMLX provides optimized containers for DGX Spark deployments with Nvidia Workbench:

- Pre-configured CUDA environment
- Optimized kernel parameters
- Multi-GPU support via NCCL
- Integrated monitoring and profiling

See the DGX configuration guide for container setup and best practices.

**Best For**: Large-scale training, multi-GPU workflows, data center deployments

AMD ROCM
^^^^^^^^

**Devices**: AMD Radeon and Instinct GPUs (Coming Soon)

**Features**:
- ROCM runtime support
- HIP API compatibility
- AMD unified memory architecture support
- Configurations with x64 + 128GB unified memory + NPU

**Example Configurations**:
- AMD MI300 series with unified memory
- Radeon Pro workstations
- x64 systems with integrated AMD NPU

**Requirements**:
- ROCM >= 6.0
- Linux with glibc >= 2.35
- Python >= 3.10

**Installation** (Coming Soon):

.. code-block:: shell

    pip install umlx[rocm]

**Best For**: AMD GPU workflows, unified memory architectures, NPU acceleration

x64 CPUs
^^^^^^^^

**Processors**: Intel and AMD x64 processors

**Features**:
- Optimized CPU operations using OpenBLAS/MKL
- AVX2/AVX-512 SIMD acceleration where available
- Multi-threading support
- Large memory capacity support

**AMD Threadripper Configurations**:
- High core count optimization (16-96 cores)
- Large RAM support (128GB - 2TB)
- NUMA-aware memory allocation
- Ideal for CPU-intensive workloads

**Requirements**:
- Linux with glibc >= 2.35
- Python >= 3.10

**Installation**:

.. code-block:: shell

    pip install umlx[cpu]

**Best For**: CPU-only deployments, development, high-RAM requirements

ARM Processors
^^^^^^^^^^^^^^

**Processors**: ARM64/AArch64 CPUs

**Features**:
- Native ARM64 support (expanded from x86_64-only)
- NEON SIMD acceleration
- Support for ARM server and embedded platforms
- Energy-efficient computation

**Example Platforms**:
- ARM Neoverse servers
- Ampere Altra processors
- AWS Graviton instances
- Raspberry Pi 4/5 (experimental)

**Requirements**:
- Linux with glibc >= 2.35
- Python >= 3.10
- ARM64 processor

**Installation**:

.. code-block:: shell

    pip install umlx[cpu]

**Best For**: ARM servers, edge deployment, energy-efficient computing

Configuration Examples
----------------------

Single GPU Workstation
^^^^^^^^^^^^^^^^^^^^^^

Nvidia RTX 4090 development machine:

.. code-block:: shell

    # Install CUDA support
    pip install umlx[cuda12]
    
    # Verify GPU detection
    python -c "import umlx.core as mx; print(mx.metal.is_available())"

Multi-GPU Training Server
^^^^^^^^^^^^^^^^^^^^^^^^^^

DGX A100 with 8x GPUs:

.. code-block:: python

    import umlx.core as mx
    from mlx.distributed import init
    
    # Initialize multi-GPU
    init()
    
    # Distributed training code
    # ...

AMD Unified Memory System
^^^^^^^^^^^^^^^^^^^^^^^^^^

AMD configuration with unified memory and NPU (Coming Soon):

.. code-block:: shell

    # Install ROCM support
    pip install umlx[rocm]
    
    # Configure unified memory
    export HSA_XNACK=1

CPU-Only Server
^^^^^^^^^^^^^^^

AMD Threadripper with 128GB RAM:

.. code-block:: shell

    # Install CPU-only version
    pip install umlx[cpu]
    
    # Configure thread count
    export OMP_NUM_THREADS=32

Building from Source
--------------------

Platform-Specific Build Instructions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the main installation guide for detailed build instructions for each platform.

**macOS/Metal**:

.. code-block:: shell

    cmake -DMLX_BUILD_METAL=ON ..
    make

**Linux/CUDA**:

.. code-block:: shell

    cmake -DMLX_BUILD_CUDA=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda ..
    make

**Linux/CPU**:

.. code-block:: shell

    cmake -DMLX_BUILD_CPU=ON ..
    make

**Linux/ROCM** (Coming Soon):

.. code-block:: shell

    cmake -DMLX_BUILD_ROCM=ON -DROCM_PATH=/opt/rocm ..
    make

Performance Optimization
------------------------

Platform-Specific Tips
^^^^^^^^^^^^^^^^^^^^^^

**Apple Silicon**:
- Use unified memory for efficient CPU/GPU data sharing
- Leverage Neural Engine for compatible operations
- Set appropriate batch sizes for Metal shader limits

**Nvidia CUDA**:
- Enable Tensor Cores with appropriate dtypes (float16, bfloat16)
- Use NCCL for multi-GPU synchronization
- Optimize kernel launch parameters

**AMD ROCM**:
- Leverage unified memory architecture where available
- Use HIP profiling tools for optimization
- Consider NPU offload for supported operations

**CPU (x64/ARM)**:
- Set optimal thread count via OMP_NUM_THREADS
- Use SIMD-aligned data layouts
- Consider memory bandwidth limitations

Troubleshooting
---------------

Device Detection Issues
^^^^^^^^^^^^^^^^^^^^^^^

If UMLX doesn't detect your GPU:

1. Verify driver installation
2. Check CUDA/ROCM toolkit installation
3. Ensure compatible hardware (check compute capability)
4. Review system logs for errors

Performance Issues
^^^^^^^^^^^^^^^^^^

For unexpected performance problems:

1. Verify device selection (CPU vs GPU)
2. Check batch size and memory usage
3. Profile operations to identify bottlenecks
4. Review platform-specific optimization guides

Platform-Specific Issues
^^^^^^^^^^^^^^^^^^^^^^^^

See platform-specific troubleshooting sections in the installation guide.
