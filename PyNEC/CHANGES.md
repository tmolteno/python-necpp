### Version 1.7.2:

* Convert setup.py to pyproject.toml as primary metadata source (PEP 621)
  - All package metadata now lives in pyproject.toml `[project]` table
  - setup.py reduced to C++ extension compilation only
  - Supports uv build (`uv build`) as well as pip/build
* Fix #24: VSWR formula guard — add explicit `np.abs()` in vswr() to prevent negative values
* Fix #8: Add missing `handle_nec` method to `necpp/tests/test_multiple_sc_cards.py`
* Fix #31: Guard numpy import in `PyNEC/setup.py` with try/except for PEP 517 metadata phases
* Fix CI branch filter (main → master)

### Version 1.7.3.6:

* Update with a requested fix by user slawkory in context_clean.py
* Also fix an intger division bug introduced with the shift to python3 in logperiodic_opt.py

### Version 1.7.4:

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
