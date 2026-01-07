# BARF Architecture

## Overview

BARF (Boost And ROOT Framework) is a standalone C++ header-only library with Python bindings that extends ROOT RDataFrame functionality for high-energy physics analysis.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Application                            │
│                    (Python or C++ Analysis Code)                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
┌─────────────────┐            ┌──────────────────────┐
│  Python Module  │            │   C++ Application    │
│    (narf)       │            │                      │
│  - histutils.py │            │  #include "barf/"    │
│  - clingutils.py│            │  - histutils.hpp     │
└────────┬────────┘            └──────────┬───────────┘
         │                                │
         │    PyROOT/Cling                │
         │    (C++/Python Bridge)         │
         │                                │
         └────────────┬───────────────────┘
                      │
         ┌────────────▼──────────────────────────────┐
         │         BARF C++ Headers                  │
         │  (Header-only INTERFACE Library)          │
         │                                            │
         │  ┌──────────────────────────────────────┐ │
         │  │ histutils.hpp                        │ │
         │  │  - make_histogram()                  │ │
         │  │  - make_atomic_histogram()           │ │
         │  │  - boost-histogram utilities         │ │
         │  └──────────────────────────────────────┘ │
         │                                            │
         │  ┌──────────────────────────────────────┐ │
         │  │ atomic_adaptor.hpp                   │ │
         │  │  - Thread-safe wrappers              │ │
         │  │  - Atomic operations for histograms  │ │
         │  └──────────────────────────────────────┘ │
         │                                            │
         │  ┌──────────────────────────────────────┐ │
         │  │ tensorutils.hpp                      │ │
         │  │  - Tensor accumulator support        │ │
         │  │  - Eigen tensor integration          │ │
         │  └──────────────────────────────────────┘ │
         │                                            │
         │  ┌──────────────────────────────────────┐ │
         │  │ FillBoostHelperAtomic.hpp            │ │
         │  │  - RDataFrame action helper          │ │
         │  │  - Parallel histogram filling        │ │
         │  └──────────────────────────────────────┘ │
         │                                            │
         │  ┌──────────────────────────────────────┐ │
         │  │ traits.hpp                           │ │
         │  │  - Type traits and metaprogramming   │ │
         │  └──────────────────────────────────────┘ │
         └────────────┬───────────────────────────────┘
                      │
         ┌────────────▼──────────────────────────────┐
         │         External Dependencies             │
         │                                            │
         │  ┌─────────────────────────────────────┐  │
         │  │ ROOT (>= 6.24)                      │  │
         │  │  - RDataFrame, RResultPtr           │  │
         │  │  - TThreadExecutor                  │  │
         │  │  - PyROOT/Cling                     │  │
         │  └─────────────────────────────────────┘  │
         │                                            │
         │  ┌─────────────────────────────────────┐  │
         │  │ Intel TBB                           │  │
         │  │  - Parallel algorithms              │  │
         │  │  - Task arena                       │  │
         │  └─────────────────────────────────────┘  │
         │                                            │
         │  ┌─────────────────────────────────────┐  │
         │  │ Boost.Histogram (header-only)       │  │
         │  │  - Histogram data structures        │  │
         │  │  - Axis types                       │  │
         │  └─────────────────────────────────────┘  │
         │                                            │
         │  ┌─────────────────────────────────────┐  │
         │  │ Eigen3 (header-only)                │  │
         │  │  - Linear algebra                   │  │
         │  │  - Tensor operations                │  │
         │  └─────────────────────────────────────┘  │
         └────────────────────────────────────────────┘
```

## Build System Flow

```
┌──────────────────┐
│  CMakeLists.txt  │  Main build configuration
└────────┬─────────┘
         │
         ├─> find_package(ROOT) ───────┐
         ├─> find_package(TBB) ────────┤
         ├─> find_package(Eigen3) ─────┤──> Find dependencies
         └─> find_path(Boost) ─────────┘
         │
         ▼
┌──────────────────────────────┐
│  add_library(barf INTERFACE) │  Header-only library
└────────┬─────────────────────┘
         │
         ├─> target_include_directories()  ──> Add include paths
         ├─> target_link_libraries() ───────> Link dependencies
         └─> target_compile_definitions() ─> Add compile flags
         │
         ▼
┌─────────────────────┐
│  install(TARGETS)   │  Install headers and CMake config
└─────────────────────┘
```

## Python Integration Flow

```
┌────────────────────┐
│  import ROOT       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  import narf       │
└─────────┬──────────┘
          │
          ├─> narf/__init__.py
          │   └─> ROOT.gInterpreter.AddIncludePath("narf/include/")
          │
          ├─> from narf import histutils
          │   └─> narf/histutils.py
          │       ├─> clingutils.Declare('#include "histutils.hpp"')
          │       ├─> clingutils.Declare('#include "FillBoostHelperAtomic.hpp"')
          │       └─> Python wrapper functions
          │
          ▼
┌────────────────────────────────┐
│  C++ code loaded via Cling     │
│  (ROOT's JIT compiler)         │
└────────────────────────────────┘
```

## Package Distribution Flow

```
┌─────────────────────────────────────────────────┐
│           Source Repository                     │
│         github.com/asopio/barf                  │
└──────────────┬──────────────────────────────────┘
               │
     ┌─────────┴─────────┬─────────────┐
     │                   │             │
     ▼                   ▼             ▼
┌──────────┐    ┌────────────────┐  ┌───────────┐
│  PyPI    │    │  conda-forge   │  │   Pixi    │
│          │    │                │  │           │
│ setup.py │    │ conda/         │  │ pixi.toml │
│ pyproject│    │ meta.yaml      │  │           │
│ .toml    │    │                │  │           │
└────┬─────┘    └────────┬───────┘  └─────┬─────┘
     │                   │                 │
     └───────────────────┴────────┬────────┘
                                  │
                  ┌───────────────▼────────────────┐
                  │     User Installation          │
                  │                                │
                  │  pip install barf              │
                  │  conda install barf            │
                  │  pixi add barf                 │
                  └────────────────────────────────┘
```

## Data Flow

```
User Analysis
     │
     ▼
┌─────────────────────┐
│  ROOT.RDataFrame    │
│  ("tree", "data")   │
└──────────┬──────────┘
           │
           ├─> .Define()
           ├─> .Filter()
           └─> .Book()
               │
               ▼
┌──────────────────────────────────┐
│  FillBoostHelperAtomic           │
│  (BARF RDataFrame action)        │
└──────────────┬───────────────────┘
               │
               ├─> Parallel execution (TBB)
               │   ├─> Thread 1 ──┐
               │   ├─> Thread 2 ──┼─> Atomic fills
               │   └─> Thread N ──┘
               │
               ▼
┌──────────────────────────────────┐
│  Boost.Histogram                 │
│  with atomic storage             │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  Results (Python/C++)            │
│  - hist_to_root()                │
│  - root_to_hist()                │
└──────────────────────────────────┘
```

## Component Relationships

```
┌──────────────────────────────────────────────────────────────────┐
│                         BARF Components                          │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   traits.hpp │◄────────│tensorutils   │                     │
│  │              │         │    .hpp      │                     │
│  └──────┬───────┘         └───────┬──────┘                     │
│         │                         │                             │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────────────────────────┐                      │
│  │      atomic_adaptor.hpp              │                      │
│  │   (uses traits, tensorutils)         │                      │
│  └──────────────────┬───────────────────┘                      │
│                     │                                           │
│                     ▼                                           │
│  ┌──────────────────────────────────────┐                      │
│  │        histutils.hpp                 │                      │
│  │   (uses all above components)        │                      │
│  └──────────────────┬───────────────────┘                      │
│                     │                                           │
│                     ▼                                           │
│  ┌──────────────────────────────────────┐                      │
│  │   FillBoostHelperAtomic.hpp          │                      │
│  │   (RDataFrame integration)           │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Threading Model

```
Main Thread
    │
    ├─> Creates RDataFrame
    │
    ├─> ROOT.EnableImplicitMT(N)
    │   │
    │   └─> TBB task arena with N threads
    │
    ├─> df.Book(FillBoostHelperAtomic, ...)
    │
    └─> Trigger computation
        │
        ├─> Thread 1
        │   └─> atomic_adaptor::operator+=()
        │       └─> std::atomic<T>::fetch_add()
        │
        ├─> Thread 2
        │   └─> atomic_adaptor::operator+=()
        │       └─> std::atomic<T>::fetch_add()
        │
        └─> Thread N
            └─> atomic_adaptor::operator+=()
                └─> std::atomic<T>::fetch_add()
        │
        └─> All threads synchronized
            └─> Final histogram result
```

## Design Principles

1. **Header-Only**: No compilation of BARF code needed
2. **Minimal Dependencies**: Only well-supported, widely-available libraries
3. **No ROOT Recompilation**: Links against pre-built ROOT
4. **Thread-Safe**: Atomic operations for parallel histogram filling
5. **Template-Based**: Type-safe, compile-time optimizations
6. **Standard Compliance**: C++17, works with modern compilers

## Installation Architecture

```
Pre-installed (conda-forge):
├── ROOT
├── TBB
├── Eigen3
└── Boost.Histogram

BARF Installation:
├── C++ Headers
│   └── /include/barf/*.hpp
├── Python Module
│   └── /python/narf/*.py
└── CMake Config
    └── /lib/cmake/BARF/*.cmake
```

## Future Extensions

- Additional histogram utilities
- More RDataFrame helpers
- Integration with other analysis frameworks
- Performance optimizations
- Extended documentation and tutorials

---

For more details, see:
- [README.md](README.md) - Main documentation
- [INSTALL.md](INSTALL.md) - Installation guide
- [DEPENDENCIES.md](DEPENDENCIES.md) - Dependency analysis
