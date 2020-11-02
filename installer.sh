#!/bin/bash

git submodule update --init
meson setup build --prefix=$PWD --libdir=xtb
ninja -C build install
pip install -e .
