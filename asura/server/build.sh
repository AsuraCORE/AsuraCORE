#!/bin/bash
# AsuraCORE build: ./build.sh  (logs -> /opt/asuracore/build.log)
set -e
cd /opt/asuracore
export CC=gcc-13 CXX=g++-13
cmake -GNinja -S src -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=/opt/asuracore/server \
  -DTOOLS=1 -DSCRIPTS=static -DWITH_WARNINGS=0 -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build -j 14
cmake --install build
echo BUILD_OK
