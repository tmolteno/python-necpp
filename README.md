<!-- Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz) -->
# python-necpp: Antenna simulation in python

This repository contains two wrappers for the [http://github.com/tmolteno/necpp nec2++] antenna simulation package:

* necpp/ contains a wrapper using SWIG of the C interface (Python module name: necpp).
* PyNEC/ contains a wrapper of the C++ interfaces (Python module name: PyNEC).  The example/ directory furthermore contains some nicer, more readable Python wrappers that make toying around with NEC a less painful experience.

Both are based on Tim Molteno (tim@physics.otago.ac.nz)'s code with major cleanup by Bart Coppens.

## Quick Install

```bash
pip install PyNEC necpp
```

Wheels are built with the Python stable ABI (**abi3**): a single wheel per
platform covers CPython **3.11 – 3.14** and newer.

| Platform | Wheel tag |
|---|---|
| Linux (x86_64, manylinux) | `cp311-abi3-manylinux_*` |
| macOS (Apple Silicon) | `cp311-abi3-macosx_arm64` |
| macOS (Intel) | `cp311-abi3-macosx_x86_64` |
| Windows (x64) | `cp311-abi3-win_amd64` |

Free-threaded CPython (`cp314t`) is not covered by the stable ABI — install
from the sdist there (a full-API build is produced automatically).

### Which NEC2++ engine is bundled?

Every release pins the `necpp_src` git submodule to a specific
[necpp](https://github.com/tmolteno/necpp) commit. Two places identify it:

* the GitHub release notes and [PyNEC/CHANGES.md](PyNEC/CHANGES.md) name the
  `necpp_src` commit for each release;
* the compiled extension embeds it as `necpp_engine_sha=<commit>` — verify any
  installed wheel with:

  ```bash
  strings "$(python -c 'import _PyNEC, pathlib; print(pathlib.Path(_PyNEC.__file__))')" | grep necpp_engine_sha
  ```

## Build from Source

Uses [uv](https://github.com/astral-sh/uv) for modern PEP 517 builds.
Generating the wrappers requires **SWIG >= 4.4.1** (4.5.1 recommended — older
SWIG cannot emit stable-ABI-compatible code); installing from a release
sdist needs no SWIG at all.

```bash
git clone --recursive https://github.com/tmolteno/python-necpp.git
cd python-necpp

# Build PyNEC
cd PyNEC && ./build.sh && uv build

# Build necpp
cd ../necpp && ./build.sh && uv build
```

## TODOs

The cleaner API should really be **ported to C++**, so the clean wrappers get automatically generated, and C++ can use the same cleaner interface. But for now, I'm happy with the Python wrapper :)
