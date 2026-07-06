<!-- Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz) -->
## Building from Source

    apt install swig
    git submodule init
    git submodule update --remote
    cd PyNEC
    ./build.sh
    uv pip install dist/*.whl

## Testing

    uv pip install pytest
    python -m pytest tests/ -v

## Uploading the package to pypi

    uv build
    uv publish
