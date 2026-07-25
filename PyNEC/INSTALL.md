<!-- Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz) -->
# PyNEC: Building from Source

    git clone --recursive https://github.com/tmolteno/python-necpp.git
    cd python-necpp/PyNEC
    ./build.sh
    uv pip install dist/*.whl

## Test

    uv pip install pytest
    python -m pytest tests/ -v

## Upload

    uv build
    uv publish
