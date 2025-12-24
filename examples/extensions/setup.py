# Copyright © 2023-2024 Apple Inc.

from setuptools import setup

from umlx import extension

if __name__ == "__main__":
    setup(
        name="umlx_sample_extensions",
        version="0.0.0",
        description="Sample C++ and Metal extensions for MLX primitives.",
        ext_modules=[extension.CMakeExtension("umlx_sample_extensions._ext")],
        cmdclass={"build_ext": extension.CMakeBuild},
        packages=["umlx_sample_extensions"],
        package_data={"umlx_sample_extensions": ["*.so", "*.dylib", "*.metallib"]},
        zip_safe=False,
        python_requires=">=3.8",
    )
