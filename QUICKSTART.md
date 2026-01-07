# BARF Quick Start Guide

## For Users: Installation

### Option 1: Conda (Recommended)
```bash
# Once published to conda-forge:
conda install -c conda-forge barf

# Use it:
python
>>> import ROOT
>>> import narf
>>> # Your analysis code
```

### Option 2: Pixi (Modern Alternative)
```bash
# Install pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Add BARF to your project
pixi add barf

# Use it:
pixi run python
>>> import ROOT
>>> import narf
```

### Option 3: From Source
```bash
# Install dependencies first
conda install -c conda-forge root tbb eigen boost-histogram hist numpy cmake

# Clone and build
git clone https://github.com/asopio/barf.git
cd barf
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DBARF_BUILD_PYTHON=ON ..
cmake --build . --parallel
cmake --build . --target install

# Test
python -c "import ROOT; import narf; print('Success!')"
```

## For Developers: Contributing

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/asopio/barf.git
cd barf

# Option A: Using pixi (recommended)
pixi install
pixi shell

# Option B: Using conda
conda env create -f environment.yml  # (create this file if needed)
conda activate barf-dev
```

### Build BARF

```bash
# Create build directory
mkdir build && cd build

# Configure (Debug mode for development)
cmake -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX \
      -DBARF_BUILD_PYTHON=ON \
      -DBARF_BUILD_TESTS=ON \
      ..

# Build
cmake --build . --parallel

# Install
cmake --build . --target install
```

### Test Your Changes

```bash
# Set environment
source setup.sh

# Run example
python test.py

# Import in Python
python -c "import ROOT; import narf; from narf import histutils"
```

### Code Style

BARF follows standard C++ and Python conventions:
- C++17 for C++ code
- PEP 8 for Python code
- Use `black` for Python formatting: `black narf/`
- Use `isort` for import sorting: `isort narf/`

## Quick Examples

### Example 1: Basic Histogram Creation

```python
import ROOT
import narf
import hist

# Create a boost-histogram
h = hist.Hist(
    hist.axis.Regular(50, -5, 5, name="x"),
    hist.axis.Regular(50, -5, 5, name="y"),
)

print(f"Created histogram with {h.size} bins")
```

### Example 2: Using with RDataFrame

```python
import ROOT
import narf
from narf import histutils

# Enable multithreading
ROOT.ROOT.EnableImplicitMT()

# Create RDataFrame
df = ROOT.RDataFrame("tree", "data.root")

# Your analysis using BARF utilities
# (See test.py for complete examples)
```

### Example 3: Atomic Histogram Filling

```python
import ROOT
import narf

# Use BARF's atomic histogram helpers for thread-safe filling
# (See histutils documentation for details)
```

## Project Structure

```
barf/
├── narf/                  # Python package
│   ├── __init__.py
│   ├── histutils.py       # Main histogram utilities
│   ├── clingutils.py      # ROOT Cling interface
│   └── include/           # C++ headers
│       ├── histutils.hpp
│       ├── atomic_adaptor.hpp
│       └── ...
├── CMakeLists.txt         # Main build config
├── setup.py               # Python package setup
├── pyproject.toml         # Modern Python metadata
└── conda/meta.yaml        # Conda recipe
```

## Key Files

- `narf/include/histutils.hpp` - Main C++ header for histogram utilities
- `narf/histutils.py` - Python interface to C++ utilities
- `CMakeLists.txt` - Build system configuration
- `README.md` - Main documentation
- `INSTALL.md` - Detailed installation guide
- `DEPENDENCIES.md` - Dependency analysis

## Common Tasks

### Add a New Header File
1. Create `narf/include/newfeature.hpp`
2. Add includes to `narf/include/histutils.hpp` if needed
3. Update CMakeLists.txt if installing separately
4. Document in README.md

### Add Python Bindings
1. Add to `narf/__init__.py` for exports
2. Use `clingutils.Declare()` to load C++ code
3. Document usage in docstrings

### Update Dependencies
1. Update `CMakeLists.txt` (C++ deps)
2. Update `pyproject.toml` (Python deps)
3. Update `conda/meta.yaml` (conda deps)
4. Update `DEPENDENCIES.md` (documentation)

### Run Tests
```bash
# Python import test
python -c "import narf"

# Run example
source setup.sh
python test.py

# CMake tests (if BARF_BUILD_TESTS=ON)
cd build
ctest
```

## Getting Help

- **Documentation**: See [README.md](README.md), [INSTALL.md](INSTALL.md)
- **Issues**: https://github.com/asopio/barf/issues
- **ROOT Documentation**: https://root.cern/
- **Boost.Histogram**: https://www.boost.org/doc/libs/release/libs/histogram/

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create Pull Request

## License

BARF is licensed under LGPL-2.1-or-later, same as ROOT.
See [LICENSE](LICENSE) for details.
