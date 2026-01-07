# BARF Dependency Analysis

## Executive Summary

This document analyzes the dependencies of the NARF histutils component to determine the feasibility of extracting it into a standalone BARF (Boost And ROOT Framework) library.

**Conclusion**: ✅ **Feasible** - BARF can be built as a standalone library that doesn't require recompiling ROOT from source.

## Dependency Categories

### 1. Header-Only Dependencies (Non-ROOT)

These dependencies are completely header-only and don't require any compiled libraries:

#### Boost.Histogram
- **Header files**: `<boost/histogram.hpp>`, `<boost/histogram/detail/priority.hpp>`
- **Status**: ✅ Completely header-only
- **Installation**: Available via conda-forge (`boost-histogram`)
- **Impact**: No linking required, just include paths

#### Eigen3
- **Header files**: `<eigen3/Eigen/Dense>`, `<eigen3/unsupported/Eigen/CXX11/Tensor>`
- **Status**: ✅ Completely header-only
- **Installation**: Available via conda-forge (`eigen`)
- **Impact**: No linking required, just include paths

#### Standard Library Headers
- **Header files**: `<atomic>`, `<type_traits>`, `<iostream>`, `<array>`, etc.
- **Status**: ✅ Always available
- **Installation**: Part of C++ toolchain
- **Impact**: No additional dependencies

### 2. Compiled Library Dependencies

These dependencies require compiled libraries to be available:

#### ROOT
- **Header files used**:
  - `<ROOT/RResultPtr.hxx>`
  - `<ROOT/TThreadExecutor.hxx>`
  - `<ROOT/RDF/Utils.hxx>`
  - `<ROOT/RDF/ActionHelpers.hxx>`
  - `<TROOT.h>`
  - `<ROOT/RDFHelpers.hxx>`
- **Status**: ⚠️ Required compiled library
- **Key insight**: Can link against **pre-installed ROOT**, no recompilation needed
- **Installation**: Available via conda-forge (`root`)
- **Impact**: Must link against ROOT libraries (Core, RIO, Tree, Hist, ROOTDataFrame)

#### Intel TBB (Threading Building Blocks)
- **Header files used**: `<oneapi/tbb.h>`, `<tbb/task_arena.h>`
- **Status**: ⚠️ Required compiled library
- **Installation**: Available via conda-forge (`tbb`, `tbb-devel`)
- **Impact**: Must link against TBB library
- **Note**: Small, widely available library; commonly used in scientific computing

### 3. Optional Dependencies

These dependencies are used by other NARF components but not strictly required for histutils:

#### ONNX Runtime
- **Used in**: `onnxutils.hpp`
- **Status**: Optional for histutils
- **Can be excluded**: Yes

#### TensorFlow Lite
- **Used in**: `tfliteutils.hpp`
- **Status**: Optional for histutils
- **Can be excluded**: Yes

## Component Breakdown

### Core histutils Components

#### histutils.hpp
**Dependencies**:
- ✅ `<boost/histogram.hpp>` - header-only
- ✅ `traits.hpp` - local header
- ✅ `atomic_adaptor.hpp` - local header
- ✅ `tensorutils.hpp` - local header
- ⚠️ `<ROOT/RResultPtr.hxx>` - requires ROOT
- ⚠️ `<ROOT/TThreadExecutor.hxx>` - requires ROOT
- ✅ `<eigen3/Eigen/Dense>` - header-only
- ✅ `<eigen3/unsupported/Eigen/CXX11/Tensor>` - header-only
- ⚠️ `<oneapi/tbb.h>` - requires TBB

**Verdict**: Requires ROOT and TBB, but both can be pre-installed

#### atomic_adaptor.hpp
**Dependencies**:
- ✅ `<atomic>` - standard library
- ✅ `<boost/histogram/detail/priority.hpp>` - header-only
- ✅ `<type_traits>` - standard library
- ✅ `traits.hpp` - local header
- ✅ `tensorutils.hpp` - local header

**Verdict**: ✅ Fully header-only (except transitive ROOT dependency from traits.hpp)

#### tensorutils.hpp
**Dependencies**:
- ✅ `traits.hpp` - local header
- ✅ `<boost/histogram.hpp>` - header-only
- ✅ `<eigen3/Eigen/Dense>` - header-only
- ✅ `<eigen3/unsupported/Eigen/CXX11/Tensor>` - header-only

**Verdict**: ✅ Fully header-only (except transitive ROOT dependency from traits.hpp)

#### traits.hpp
**Dependencies**:
- ✅ `<boost/histogram.hpp>` - header-only
- ✅ `<eigen3/Eigen/Dense>` - header-only
- ✅ `<eigen3/unsupported/Eigen/CXX11/Tensor>` - header-only
- ⚠️ Uses `ROOT::Internal::RDF::IsDataContainer<T>` - requires ROOT headers

**Verdict**: Requires ROOT headers but only for type traits

#### FillBoostHelperAtomic.hpp
**Dependencies**:
- ✅ `<boost/histogram.hpp>` - header-only
- ⚠️ `<TROOT.h>` - requires ROOT
- ⚠️ `<ROOT/RDF/Utils.hxx>` - requires ROOT
- ⚠️ `<ROOT/RDF/ActionHelpers.hxx>` - requires ROOT
- ✅ `histutils.hpp` - local header

**Verdict**: Requires ROOT for RDataFrame integration

## Feasibility Analysis

### Original Problem Statement Claim
> "For histutils, I think this should be feasible as the non-root dependencies are all header-only libraries -- verify this!"

### Verification Result
**Partially Correct**: The non-ROOT dependencies are indeed mostly header-only, with one exception:

1. ✅ **Boost.Histogram** - Confirmed header-only
2. ✅ **Eigen3** - Confirmed header-only
3. ⚠️ **TBB** - **NOT header-only**, requires compiled library

However, this doesn't prevent the feasibility of the project because:

### Why BARF is Still Feasible

1. **TBB is widely available**:
   - Available in conda-forge
   - Available in all major Linux distributions
   - Small library, easy to install
   - Commonly used in HEP and scientific computing

2. **ROOT doesn't need recompilation**:
   - BARF can link against pre-installed ROOT from conda
   - No need to modify ROOT source
   - No need to rebuild ROOT with BARF integrated
   - ROOT is already available via conda-forge

3. **Header-only where it matters**:
   - The core BARF code is header-only C++ templates
   - Only needs to link against stable, widely-available libraries
   - No proprietary or hard-to-obtain dependencies

## Design Strategy

### BARF as a Standalone Library

BARF is implemented as:

1. **C++ Header-Only Library**:
   - All `.hpp` files in `narf/include/`
   - Templates and inline functions only
   - No `.cpp` implementation files to compile

2. **CMake Interface Library**:
   - Declared as `INTERFACE` library in CMake
   - Propagates include directories and link requirements
   - No actual compilation of BARF code itself

3. **Python Bindings via PyROOT**:
   - Uses ROOT's Cling interpreter for C++/Python interop
   - No separate binding code needed
   - Dynamic loading of C++ code at runtime

### Installation Strategy

```
User's System:
├── ROOT (from conda-forge) ──────┐
├── TBB (from conda-forge) ───────┤
├── Eigen (from conda-forge) ─────┤──> BARF links to these
├── Boost (from conda-forge) ─────┘
└── BARF (this package)
    ├── C++ headers (copied to include/)
    └── Python module (copied to site-packages/)
```

## Conclusion

### Summary
- **Primary Goal**: ✅ Achieved - BARF is a standalone package
- **No ROOT Recompilation**: ✅ Achieved - Links to pre-installed ROOT
- **Header-Only Non-ROOT Deps**: ⚠️ Mostly - TBB is the only exception
- **Conda/Pixi Installable**: ✅ Achieved - All deps available via conda

### Key Success Factors

1. **Minimal Dependencies**: Only ROOT, TBB, Eigen, and Boost.Histogram
2. **All Available via Conda**: No custom builds or manual compilation
3. **Header-Only Design**: No BARF code needs compilation
4. **Standard Build System**: Uses CMake and setuptools
5. **Python Integration**: Leverages existing PyROOT infrastructure

### Recommendations for Users

**Installation Priority**:
1. Use conda/pixi (recommended): All dependencies handled automatically
2. Use pre-built ROOT + BARF from conda-forge
3. Only build from source if necessary for development

**Dependency Installation**:
```bash
# Recommended: Install via conda
conda install -c conda-forge root tbb eigen boost-histogram

# Then install BARF
pip install barf
# or
conda install -c conda-forge barf
```

## Appendix: Complete Dependency Tree

```
BARF (histutils)
├── ROOT >=6.24 [compiled library]
│   └── Required components: Core, RIO, Tree, Hist, ROOTDataFrame
├── TBB [compiled library]
│   └── Intel Threading Building Blocks
├── Eigen3 [header-only]
│   └── Linear algebra library
├── Boost.Histogram [header-only]
│   └── Modern C++ histogram library
└── Standard Library [always available]
    ├── <atomic>
    ├── <type_traits>
    ├── <iostream>
    └── <array>

Python Dependencies
├── numpy >=1.20
├── boost-histogram >=1.0
└── hist >=2.0
```

## References

- ROOT Project: https://root.cern/
- Boost.Histogram: https://www.boost.org/doc/libs/release/libs/histogram/
- Eigen: https://eigen.tuxfamily.org/
- Intel TBB: https://github.com/oneapi-src/oneTBB
- Conda-forge: https://conda-forge.org/
