### Version 1.8.0:

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
