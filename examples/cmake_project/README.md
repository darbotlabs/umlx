## Build and Run 

Install UMLX with Python:

```bash
pip install umlx>=0.22
```

Build the C++ example:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

Run the C++ example:

```
./build/example
```

which should output:

```
array([2, 4, 6], dtype=int32)
```
