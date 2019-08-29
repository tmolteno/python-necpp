## Building from Source

    aptitude install swig3.0
    git submodule init
    git submodule update --remote
    cd PyNEC
    ./build.sh
    sudo python setup.py install
    
    
## Uploading the package to pypi

Source & Binary Distribution
    python3 setup.py sdist
    python3 setup.py bdist_wheel
    
    python3 setup.py upload
