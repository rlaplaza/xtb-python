#!/bin/bash

git submodule update --init
LDFLAGS="-L${MKLROOT}/lib/intel64" meson setup build --prefix=$PWD --default-library=static
ninja -C build install
pip install -e '.[ase,qcschema]' 
