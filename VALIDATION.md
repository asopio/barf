# BARF Validation Guide

This guide explains how to validate BARF against the original narf package to ensure compatibility and correctness.

## Overview

BARF provides pixi-based tasks that automatically:
1. Clone the original narf repository
2. Set up the environment for both packages
3. Run tests with both narf and BARF
4. Compare results

## Quick Start

### Prerequisites

- pixi installed ([installation guide](https://pixi.sh/))
- Available disk space (~500 MB for ROOT + dependencies + narf)

### Setup

```bash
# Clone BARF repository
git clone https://github.com/asopio/barf.git
cd barf

# Install with validation environment
pixi install --environment narf-validation
```

## Validation Tasks

### 1. Setup Original NARF

```bash
pixi run setup-narf
```

This task:
- Clones the original narf repository to `narf-original/`
- Only clones if the directory doesn't already exist

### 2. Test with Original NARF

```bash
pixi run test-narf
```

This task:
- Sets up the narf environment (PYTHONPATH, etc.)
- Runs test.py using the original narf package
- Depends on `setup-narf` task

### 3. Test with BARF

```bash
pixi run test-barf
```

This task:
- Builds and installs BARF
- Runs test.py using BARF
- Depends on `build` and `install` tasks

### 4. Compare Both

```bash
pixi run compare
```

This task:
- Runs tests with original narf first
- Then runs tests with BARF
- Reports success if both complete

### 5. Full Validation

```bash
pixi run validate
```

This task:
- Runs both `test-narf` and `test-barf`
- Validates that both work correctly

## Environment Details

### narf-validation Environment

The `narf-validation` environment includes additional dependencies:

```toml
[feature.narf-validation.dependencies]
lz4 = "*"      # Required for narf's pickle compression
numba = "*"    # Required for JIT compilation in narf
```

Activate it with:
```bash
pixi shell --environment narf-validation
```

## Manual Validation

If you prefer manual validation:

### Setup Original NARF

```bash
# Clone original narf
git clone https://github.com/bendavid/narf.git narf-original
cd narf-original

# Setup environment
export NARF_BASE=$(pwd)
export PYTHONPATH="${NARF_BASE}:$PYTHONPATH"
export EXTRA_CLING_ARGS="-O3"

# Run tests
python ../test.py
```

### Setup BARF

```bash
# In the barf directory
export PYTHONPATH="${PWD}:$PYTHONPATH"

# Build and install
cmake -B build -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DBARF_BUILD_PYTHON=ON
cmake --build build
cmake --build build --target install

# Run tests
python test.py
```

## What to Validate

### 1. Python Imports

Both should import successfully:

```python
import ROOT
import narf
from narf import histutils, clingutils
```

### 2. Histogram Creation

Test that histogram utilities work:

```python
import hist
import narf

# Create axes
axis_pt = hist.axis.Regular(29, 26., 55., name="pt")
axis_eta = hist.axis.Regular(48, -2.4, 2.4, name="eta")

# Both narf and BARF should handle this
```

### 3. RDataFrame Integration

Test RDataFrame functionality:

```python
import ROOT
import narf

ROOT.ROOT.EnableImplicitMT()
df = ROOT.RDataFrame("tree", "data.root")
# ... analysis code ...
```

### 4. Atomic Operations

Test thread-safe histogram filling:

```python
# Both should support atomic histogram filling
# for parallel RDataFrame operations
```

## Expected Results

### Success Indicators

- ✅ Both packages import without errors
- ✅ Same test.py runs successfully with both
- ✅ Histograms are created correctly
- ✅ RDataFrame integration works
- ✅ No compilation errors

### Known Differences

BARF is designed to be compatible with narf's Python API, but:

1. **Build System**: BARF uses CMake, narf is header-only with setup.sh
2. **Installation**: BARF can be conda/pixi installed, narf requires manual setup
3. **Internal Implementation**: May differ but API should be the same

## Troubleshooting

### Issue: "narf-original already exists"

```bash
# Remove and re-clone
rm -rf narf-original
pixi run setup-narf
```

### Issue: "Module narf not found"

Check PYTHONPATH:
```bash
echo $PYTHONPATH
# Should include either ./narf-original or current directory
```

### Issue: "ROOT not found"

Ensure ROOT is installed:
```bash
pixi run python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

### Issue: Test failures

1. Check if data files exist (test.py may require specific data)
2. Verify dependencies are installed
3. Check for version compatibility issues

## Continuous Integration

The validation can be integrated into CI/CD:

```yaml
# .github/workflows/validate.yml
name: Validate BARF

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup pixi
        uses: prefix-dev/setup-pixi@v1
        with:
          environments: narf-validation
      
      - name: Run validation
        run: pixi run validate
```

## Contributing

When making changes to BARF:

1. Run validation tests before submitting PR
2. Ensure both `pixi run test-narf` and `pixi run test-barf` pass
3. Document any API changes that affect compatibility
4. Update validation tests if needed

## References

- Original NARF: https://github.com/bendavid/narf
- Pixi Documentation: https://pixi.sh/
- Pixi Advanced Tasks: https://pixi.prefix.dev/latest/workspace/advanced_tasks/
- BARF Documentation: [README.md](README.md)

## Summary

The pixi-based validation workflow makes it easy to:
- ✅ Ensure BARF maintains compatibility with narf
- ✅ Test changes against the original implementation
- ✅ Automate validation in CI/CD
- ✅ Build confidence in BARF as a drop-in replacement
