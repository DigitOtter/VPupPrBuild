#!/usr/bin/env bash

git clone --depth=1 --branch 4.2 https://github.com/godotengine/godot.git

pushd godot

git submodule update --init --recursive --depth=1
scons compiledb=true target=editor production=yes -j$(nproc)

popd
