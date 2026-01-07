# Building ROOT with BARF Integration (Verification Guide)

This document explains how to build ROOT from source with BARF for verification purposes. **Note**: This is NOT required for normal use of BARF - the standalone installation method is recommended for users.

## Purpose

This guide is primarily for:
1. **Verification**: Confirming that BARF components work correctly with ROOT
2. **Development**: Testing changes to BARF with a custom ROOT build
3. **Understanding**: Learning how BARF integrates with ROOT's build system

## Prerequisites

### System Requirements
- **Disk Space**: ~20 GB for ROOT source and build
- **RAM**: >= 8 GB recommended
- **Time**: 1-3 hours depending on system

### Required Tools
```bash
# Ubuntu/Debian
sudo apt-get install git cmake g++ gcc binutils \
  libx11-dev libxpm-dev libxft-dev libxext-dev \
  python3-dev python3-pip

# macOS
brew install cmake git python
# Xcode Command Line Tools required
```

### Required Libraries
```bash
# Install dependencies via conda (recommended)
conda install -c conda-forge \
  tbb tbb-devel \
  eigen \
  boost-histogram

# Or via system package manager:
# Ubuntu/Debian
sudo apt-get install libtbb-dev libeigen3-dev

# macOS
brew install tbb eigen
```

## Step 1: Clone ROOT Source

```bash
# Create a workspace
mkdir -p ~/root-workspace
cd ~/root-workspace

# Clone ROOT (latest master)
git clone --depth 1 https://github.com/root-project/root.git

# Or clone a specific version
git clone --branch v6-30-00 --depth 1 https://github.com/root-project/root.git

cd root
```

## Step 2: Clone BARF Source

```bash
cd ~/root-workspace

# Clone BARF repository
git clone https://github.com/asopio/barf.git
```

## Step 3: Configure ROOT Build with BARF

ROOT doesn't need BARF to be "integrated" into its build - BARF is standalone. However, we can verify compatibility:

```bash
cd ~/root-workspace
mkdir root-build
cd root-build

# Configure ROOT with minimal options for faster build
cmake ../root \
  -DCMAKE_INSTALL_PREFIX=~/root-install \
  -DCMAKE_BUILD_TYPE=Release \
  -Dbuiltin_tbb=OFF \
  -Droofit=ON \
  -Ddataframe=ON \
  -Dpyroot=ON \
  -DPYTHON_EXECUTABLE=$(which python3)

# For a more complete build (slower):
cmake ../root \
  -DCMAKE_INSTALL_PREFIX=~/root-install \
  -DCMAKE_BUILD_TYPE=Release \
  -Dbuiltin_tbb=OFF \
  -Droofit=ON \
  -Ddataframe=ON \
  -Dpyroot=ON \
  -Dminuit2=ON \
  -Dmathmore=ON
```

## Step 4: Build ROOT

```bash
cd ~/root-workspace/root-build

# Build with all available cores
cmake --build . --parallel $(nproc)

# Or specify number of jobs manually
cmake --build . --parallel 4
```

**Expected time**: 30 minutes to 3 hours depending on system and options.

## Step 5: Install ROOT

```bash
cd ~/root-workspace/root-build
cmake --build . --target install
```

## Step 6: Setup ROOT Environment

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'source ~/root-install/bin/thisroot.sh' >> ~/.bashrc
source ~/.bashrc

# Verify ROOT installation
root --version
python3 -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

## Step 7: Build and Install BARF

Now build BARF against your custom ROOT installation:

```bash
cd ~/root-workspace/barf
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX=~/root-install -DBARF_BUILD_PYTHON=ON ..
cmake --build . --parallel $(nproc)
cmake --build . --target install
```

## Step 8: Verify Integration

```bash
cd ~/root-workspace/barf

# Set up BARF environment
source setup.sh

# Test imports
python3 -c "import ROOT; import narf; print('SUCCESS: BARF and ROOT integration verified')"

# Run example (if data files are available)
python3 test.py
```

## Alternative: Using Conda ROOT

For faster verification without building ROOT from source:

```bash
# Create a conda environment
conda create -n barf-test python=3.10
conda activate barf-test

# Install ROOT from conda-forge
conda install -c conda-forge root tbb eigen boost-histogram hist numpy

# Build and install BARF
cd ~/root-workspace/barf
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DBARF_BUILD_PYTHON=ON ..
cmake --build . --parallel $(nproc)
cmake --build . --target install

# Test
python -c "import ROOT; import narf; print('SUCCESS')"
```

## Verification Tests

### Test 1: Header Inclusion
```bash
cat > test_headers.cpp << 'EOF'
#include <ROOT/RDataFrame.hxx>
#include "histutils.hpp"
#include "atomic_adaptor.hpp"
#include "tensorutils.hpp"

int main() {
    return 0;
}
EOF

g++ -std=c++17 test_headers.cpp -I~/root-install/include/barf \
    $(root-config --cflags) -c -o /dev/null
```

### Test 2: Python Import
```python
import ROOT
import narf
from narf import histutils, clingutils

print(f"ROOT version: {ROOT.gROOT.GetVersion()}")
print("BARF modules loaded successfully")
```

### Test 3: Basic Histogram Creation
```python
import ROOT
import narf
import hist

# Create a histogram using boost-histogram
h = hist.Hist(hist.axis.Regular(50, -5, 5, name="x"))

# Verify histutils functions are available
print(dir(narf.histutils))
```

## Troubleshooting

### ROOT Build Fails
- Check disk space: `df -h`
- Reduce parallelism: Use `-j2` instead of `-j$(nproc)`
- Check logs in `root-build/CMakeFiles/CMakeError.log`

### BARF Build Fails
- Verify ROOT is in PATH: `which root-config`
- Check ROOT environment: `root-config --version`
- Set ROOT_DIR manually: `cmake -DROOT_DIR=~/root-install/cmake ..`

### TBB Not Found
```bash
# Install TBB development files
conda install -c conda-forge tbb-devel

# Or set manually
cmake -DTBB_DIR=/path/to/tbb/lib/cmake/TBB ..
```

### Eigen Not Found
```bash
# Install Eigen
conda install -c conda-forge eigen

# Or set manually
cmake -DEigen3_DIR=/path/to/eigen/share/eigen3/cmake ..
```

## Why This Verification is Useful

This verification demonstrates that:

1. ✅ BARF headers are compatible with ROOT's build system
2. ✅ BARF doesn't require modifications to ROOT source code
3. ✅ BARF can be built against different ROOT versions
4. ✅ All dependencies are properly declared and linkable

## Recommended Approach for Users

**Don't build ROOT from source** unless you have a specific reason. Instead:

```bash
# Use the standalone installation method
conda install -c conda-forge root barf

# Or
pixi add root barf
```

This is:
- ✅ Much faster (minutes vs hours)
- ✅ Less error-prone
- ✅ Easier to maintain and update
- ✅ Officially supported

## References

- ROOT Build Documentation: https://root.cern/install/build_from_source/
- ROOT CMake Options: https://root.cern/install/build_from_source/#all-build-options
- BARF Installation Guide: [INSTALL.md](INSTALL.md)
- BARF Dependency Analysis: [DEPENDENCIES.md](DEPENDENCIES.md)
