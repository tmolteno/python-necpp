<!-- Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz) -->
### Version 2.3.4:

* Update necpp_src submodule to v2.3.4
  ([upstream changelog](https://github.com/tmolteno/necpp/compare/v2.3.2...v2.3.4))
  - **Breaking:** `get_impedance_real/imag` now accept `feed_index` parameter
    (`imp.back()` → `imp[0]`, correct for multi-feed setups)
  - New: `nec_impedance_real_indexed/imag_indexed` C API for specific feeds
  - Doxygen documentation for multi-feed access patterns
  - v2.3.3: Fix GX solve and three-plane symmetry reflection

### Version 2.3.2:

* Update necpp_src submodule to v2.3.2
  ([upstream changelog](https://github.com/tmolteno/necpp/compare/v2.2.1...v2.3.2))
  - v2.3.2: NE/NH near-field blank count defaults to 1 (NEC-2 Part 3 compliance)
  - v2.3.2: Memory safety fixes — prevent duplicate close and invalid pattern reads
  - v2.3.2: Fix uninitialized read for average-only radiation-pattern rows
  - v2.3.1: Upgrade segment/patch counts to int64_t for large simulations
  - v2.3.0: Fix flat-spiral helix (GH HL=0) degenerating to straight wire

### Version 2.2.6:

* Add Python 3.14 wheel builds, drop Python 3.10
  - Update CIBW_BUILD to cp311-* through cp314-*
  - Bump requires-python to >=3.11
  - Add Python 3.14 classifier

### Version 2.2.5:

* Fix: Include Eigen headers and all source files in MANIFEST.in for sdist
  - Add `graft necpp_src/src/eigen` to include bundled Eigen headers
  - Use `recursive-include` to ensure all .h/.cpp/.h.in files are in sdist
  - Fixes `fatal error: Eigen/Dense: No such file or directory` on pip install

### Version 2.2.4:

* Fix #XX: Auto-generate config.h in setup.py so pip install from sdist works
  - setup.py now writes necpp_src/build/config.h with version from pyproject.toml
  - No longer requires CMake to be run before pip install from source
  - Applied to both PyNEC/setup.py and necpp/setup.py

### Version 2.2.3:

* Update necpp_src submodule to v2.1.1 — major engine upgrade
  - Eigen 3.4.0 replaces LAPACK (bundled in src/eigen3/, no external dependency)
  - SIMD-accelerated LU decomposition via Eigen::PartialPivLU
  - nec_3vector now backed by Eigen::Matrix (internal, no API change)
  - Fix uninitialized structure_power_loss producing NaN efficiency
  - Fix structure loss reported as zero with current printing disabled
  - Fix exception memory leak: throw-by-pointer → throw-by-value (55+ sites)
  - Table-driven NEC card parser replaces C-string parser
  - 4 monolithic functions refactored into 13 focused methods
  - No public API changes — SWIG interface and Python wrapper fully compatible

### Version 1.7.5:

* Convert setup.py to pyproject.toml as primary metadata source (PEP 621)
  - All package metadata now lives in pyproject.toml `[project]` table
  - setup.py reduced to C++ extension compilation only
  - Supports uv build (`uv build`) as well as pip/build
  - Remove superseded necpp/setup.cfg
* Fix #24: VSWR formula guard — add explicit `np.abs()` in vswr() to prevent negative values
* Fix #8: Add missing `handle_nec` method to `necpp/tests/test_multiple_sc_cards.py`
* Fix #31: Guard numpy import in `PyNEC/setup.py` with try/except for PEP 517 metadata phases
* Fix #20/#27: Correct helix argument order in SWIG interface (tag_id/segment_count were at wrong position)
* Update necpp_src submodule to v2.1.1 (Eigen replaces LAPACK, bundled in src/eigen3/)
  - No external Eigen/LAPACK dependency needed for CI builds
* Fix #28: Add sc_card to PyNEC SWIG interface (continuation card for multiple-patch surfaces)
* Fix #22/#28: Add PyNEC/example/basic_usage.py — demonstrates wire(), feedpoint impedance,
  structure currents, and SC card usage
* Fix multiple bugs found during code analysis:
  - Move test_multiple_sc_cards.py from PyNEC/tests/ to necpp/tests/ (it imported the wrong module)
  - Fix setup.cfg referencing nonexistent README.txt → README.md
  - Fix broken nosetests command in build_wheels.sh
  - Fix double-space in CI CIBW_BUILD string
  - Fix license metadata consistency (GPLv2 → GPLv3) in both setup.py files
  - Fix hard-coded swig3.0 → swig in necpp/build.sh
  - Fix symlink creation failure on re-run in both build.sh scripts
  - Fix typo (stop_ → stop) and unassigned delta bug in context_clean.py Range class
  - Add clarifying docstring for ex_card overload in nec_context.i
  - Add scipy, matplotlib to dev-requirements.txt
  - Remove stale Python 2 classifiers from necpp/setup.py
  - Fix Makefile manylinux2014 → manylinux_2_28
  - Fix CI branch filter (main → master)

### Version 1.7.3.6:

* Update with a requested fix by user slawkory in context_clean.py
* Also fix an intger division bug introduced with the shift to python3 in logperiodic_opt.py
