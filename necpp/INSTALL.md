<!-- Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz) -->
# necpp: Building from Source

This is the C-style SWIG wrapper for the nec2++ antenna simulation library.
The C++ code is compiled as part of the Python extension — no separate library
installation is required.

### Author

Tim Molteno. tim@physics.otago.ac.nz

## Build from Source

    git clone --recursive https://github.com/tmolteno/python-necpp.git
    cd python-necpp/necpp
    ./build.sh
    uv pip install dist/*.whl

## Testing

    uv pip install pytest
    python -m pytest tests/ -v
