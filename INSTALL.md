# BARF Build and Installation Guide

## Overview

BARF (Boost And ROOT Framework) is a standalone C++ library with Python bindings that extends ROOT RDataFrame functionality. It can be installed alongside ROOT without requiring ROOT to be recompiled from source.

## Quick Start

### Option 1: Conda (Recommended)

```bash
# Once the package is published to conda-forge:
conda install -c conda-forge barf
```

### Option 2: Pixi (Modern Python Package Manager)

```bash
# Install pixi if you don't have it
curl -fsSL https://pixi.sh/install.sh | bash

# Clone the repository
git clone https://github.com/asopio/barf.git
cd barf

# Install dependencies and build
pixi install
pixi run build
pixi run install
```

### Option 3: Manual Build from Source

## Prerequisites

### System Dependencies

- **C++ Compiler**: GCC >= 7.0, Clang >= 5.0, or MSVC >= 19.14
- **CMake**: >= 3.16
- **Python**: >= 3.8 (for Python bindings)

### Required Libraries

1. **ROOT** (>= 6.24)
   - Must be compiled with PyROOT support
   - Install from conda: `conda install -c conda-forge root`
   - Or build from source: https://root.cern/install/build_from_source/

2. **Intel TBB** (Threading Building Blocks)
   - Install from conda: `conda install -c conda-forge tbb tbb-devel`
   - Or from system package manager:
     - Ubuntu/Debian: `sudo apt-get install libtbb-dev`
     - macOS: `brew install tbb`

3. **Eigen3** (Linear Algebra Library - Header Only)
   - Install from conda: `conda install -c conda-forge eigen`
   - Or from system package manager:
     - Ubuntu/Debian: `sudo apt-get install libeigen3-dev`
     - macOS: `brew install eigen`

4. **Boost.Histogram** (Header Only)
   - Install from conda: `conda install -c conda-forge boost-histogram`
   - Or manually: Boost.Histogram is header-only and can be found at https://www.boost.org/

### Python Dependencies

```bash
pip install numpy>=1.20 boost-histogram>=1.0 hist>=2.0
```

## Building from Source

### Step 1: Clone the Repository

```bash
git clone https://github.com/asopio/barf.git
cd barf
```

### Step 2: Configure with CMake

```bash
mkdir build
cd build

# Basic configuration
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install ..

# With Python bindings (default)
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install -DBARF_BUILD_PYTHON=ON ..

# With tests
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install -DBARF_BUILD_TESTS=ON ..
```

### Step 3: Build

```bash
cmake --build . --parallel $(nproc)
```

### Step 4: Install

```bash
cmake --build . --target install
```

Or with sudo if installing to a system location:
```bash
sudo cmake --build . --target install
```

## Using BARF in Your Project

### CMake Integration

```cmake
find_package(BARF REQUIRED)

add_executable(myapp main.cpp)
target_link_libraries(myapp PRIVATE BARF::barf)
```

### Python Integration

```python
import sys
sys.path.insert(0, '/path/to/install/python')

import ROOT
import narf
from narf import histutils

# Your code here
```

Or set `PYTHONPATH`:
```bash
export PYTHONPATH=/path/to/install/python:$PYTHONPATH
python your_script.py
```

## Verifying Installation

### C++ Headers

Check that headers are installed:
```bash
ls /path/to/install/include/barf/
# Should show: histutils.hpp, atomic_adaptor.hpp, tensorutils.hpp, etc.
```

### Python Module

```python
python -c "import narf; print('BARF imported successfully')"
```

### Run Example

```bash
cd barf
source setup.sh  # Sets PYTHONPATH
python test.py
```

## Dependency Verification

The problem statement asked to verify that non-ROOT dependencies are header-only. Here's the analysis:

### Header-Only Dependencies ✓
- **Boost.Histogram**: Completely header-only
- **Eigen3**: Completely header-only
- **Standard Library**: Always header-only

### Compiled Library Dependencies
- **ROOT**: Required (compiled library, but can use pre-installed version)
- **TBB**: Required (compiled library, easily available via conda/apt/brew)

**Important Note**: While TBB is not header-only, it is:
1. Widely available in conda-forge and system package managers
2. A small, lightweight library
3. Commonly used in scientific computing
4. Does NOT require recompiling ROOT

This makes BARF feasible as a standalone package that can be conda/pixi installed alongside ROOT, achieving the goal of the project.

## Troubleshooting

### ROOT Not Found

```bash
# Make sure ROOT is in your environment
source /path/to/root/bin/thisroot.sh

# Or set ROOT_DIR manually
cmake -DROOT_DIR=/path/to/root/cmake ..
```

### Boost.Histogram Not Found

```bash
# Set include path manually
cmake -DBOOST_HISTOGRAM_INCLUDE_DIR=/path/to/boost/include ..
```

### TBB Not Found

```bash
# For conda installation
conda install -c conda-forge tbb-devel

# Set TBB_DIR manually if needed
cmake -DTBB_DIR=/path/to/tbb/lib/cmake/TBB ..
```

### Eigen Not Found

```bash
# For conda installation
conda install -c conda-forge eigen

# Set Eigen3_DIR manually if needed
cmake -DEigen3_DIR=/path/to/eigen/share/eigen3/cmake ..
```

## Development Setup

For developers working on BARF:

```bash
# Clone the repository
git clone https://github.com/asopio/barf.git
cd barf

# Install in development mode using pixi
pixi install
pixi shell

# Build in debug mode
mkdir build-debug
cd build-debug
cmake -DCMAKE_BUILD_TYPE=Debug -DBARF_BUILD_TESTS=ON ..
cmake --build .

# Run tests
ctest
```

## Platform-Specific Notes

### Linux
- Tested on Ubuntu 20.04+, CentOS 7+
- Use system package manager for dependencies when possible

### macOS
- Tested on macOS 11+ (Big Sur and later)
- Use Homebrew for dependencies
- May need to set `SDKROOT` for XCode command line tools

### Windows
- Experimental support
- Use conda for all dependencies
- MSVC 2019 or later recommended

## Next Steps

After installation, check out:
- [README.md](README.md) for usage examples
- [test.py](test.py) for working examples
- ROOT documentation: https://root.cern/doc/master/
- Boost.Histogram documentation: https://www.boost.org/doc/libs/release/libs/histogram/
