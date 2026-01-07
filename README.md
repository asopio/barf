# BARF

**BARF**: **B**oost **A**nd **R**OOT **F**ramework

BARF (formerly NARF - "narf is not an rdf framework") is a standalone package that extends the functionality of ROOT RDataFrames with utilities for efficient parallel data analysis.

## Features

- **Header-only C++ utilities** for working with boost-histogram and ROOT together
- **PyROOT bindings** for seamless Python integration
- **Atomic histogram filling** for thread-safe parallel processing
- **Tensor support** via Eigen integration
- **Conda/Pixi installable** - no need to recompile ROOT from source!

## Installation

### Using Conda

```bash
conda install -c conda-forge barf
```

### Using Pixi

```bash
pixi add barf
```

Or clone and install from source:

```bash
git clone https://github.com/asopio/barf.git
cd barf
pixi install
pixi run build
pixi run install
```

### From Source with CMake

Requirements:
- CMake >= 3.16
- ROOT >= 6.24 with PyROOT
- TBB (Intel Threading Building Blocks)
- Eigen3
- Boost.Histogram (header-only)

```bash
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install -DBARF_BUILD_PYTHON=ON ..
cmake --build . --target install
```

### Legacy Setup (for development with singularity)

If you're using the CERN singularity image:
```bash
singularity run /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/bendavid/cmswmassdocker/wmassdevrolling\:latest
```

Setup the environment (just adds narf to PYTHONPATH)
```bash
source setup.sh
```

Run the example
```bash
python test.py
```

## Dependencies

### C++ Dependencies
- **ROOT** (>=6.24): Provides RDataFrame and core functionality
- **TBB**: Intel Threading Building Blocks for parallelization
- **Eigen3**: Linear algebra library (header-only)
- **Boost.Histogram**: Modern C++ histogram library (header-only)

### Python Dependencies
- **numpy** (>=1.20)
- **boost-histogram** (>=1.0)
- **hist** (>=2.0)

## Architecture

BARF is designed as a standalone header-only C++ library that:
1. **Does not require recompiling ROOT** - links against pre-installed ROOT
2. **Uses header-only libraries** where possible (Boost.Histogram, Eigen)
3. **Provides PyROOT bindings** via ROOT's Cling interpreter
4. **Can be installed via conda/pixi** alongside ROOT

### Key Components

- `histutils.hpp`: Utilities for boost-histogram integration with ROOT
- `atomic_adaptor.hpp`: Thread-safe atomic wrappers for histogram accumulators
- `tensorutils.hpp`: Tensor support using Eigen
- `FillBoostHelperAtomic.hpp`: RDataFrame action helper for atomic histogram filling

## Usage

```python
import ROOT
import narf
from narf import histutils
import hist

# Create a boost-histogram
h = hist.Hist(
    hist.axis.Regular(50, -5, 5, name="x"),
    hist.axis.Regular(50, -5, 5, name="y"),
)

# Use with RDataFrame
df = ROOT.RDataFrame("tree", "data.root")
# ... your analysis code ...
```

## Validation

BARF can be validated against the original narf package using pixi:

```bash
# Install with validation environment
pixi install --environment narf-validation

# Run validation tests
pixi run validate

# Or compare side-by-side
pixi run compare
```

This clones the original narf repository and runs the same tests with both packages to ensure compatibility.

## License

LGPL-2.1-or-later (same as ROOT)
