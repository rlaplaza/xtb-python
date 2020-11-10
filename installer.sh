#!/bin/bash

git submodule update --init
LDFLAGS="-L${MKLROOT}/lib/intel64" meson setup build --prefix=$PWD --libdir=xtb
ninja -C build install
pip install -e . --user 
