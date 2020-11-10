#!/bin/bash

git submodule update --init
DFLAGS="-L${MKLROOT}/lib/intel64" meson setup build --prefix=$PWD --libdir=xtb
ninja -C build install
pip install -e . --user 
