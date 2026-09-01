import ROOT
import pathlib

_pkg_dir = pathlib.Path(__file__).parent
ROOT.gInterpreter.AddIncludePath(str(_pkg_dir / "include"))

_boost_candidates = [
    _pkg_dir / "boost" / "libs",
    _pkg_dir.parent / "boost" / "libs",
]
for _boost_libs_dir in _boost_candidates:
    if not _boost_libs_dir.is_dir():
        continue

    _include_roots = sorted(
        inc for inc in _boost_libs_dir.glob("*/include")
        if (inc / "boost").is_dir()
    )
    if any((inc / "boost" / "histogram.hpp").exists() for inc in _include_roots):
        for _inc in _include_roots:
            ROOT.gInterpreter.AddIncludePath(str(_inc))
        break
    else:
        raise RuntimeError(f"Vendored Boost headers found under {_boost_libs_dir}, but boost/histogram.hpp is missing")

from .graph_builder import build_and_run
from .dataset import Dataset
from .histutils import hist_to_root, root_to_hist, hist_to_pyroot_boost

import narf.clingutils
