from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def _boost_package_data():
    boost_root = this_directory / "narf" / "boost"
    patterns = []
    if not boost_root.exists():
        return patterns

    for path in boost_root.rglob("*.hpp"):
        patterns.append(str(path.relative_to(this_directory / "narf")))
    for path in boost_root.rglob("*.h"):
        patterns.append(str(path.relative_to(this_directory / "narf")))

    return sorted(set(patterns))


setup(
    name="barf",
    version="0.1.0",
    description="BARF: Boost And ROOT Framework - A standalone package extending ROOT RDataFrames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ben David",
    url="https://github.com/asopio/barf",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20",
        "boost-histogram>=1.0",
        "hist>=2.0",
        "h5py",
        "hdf5plugin",
    ],
    extras_require={
        "dev": ["pytest", "black", "isort"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: C++",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    package_data={
        "narf": ["include/*.hpp", "include/*.h", *_boost_package_data()],
    },
    include_package_data=True,
)
