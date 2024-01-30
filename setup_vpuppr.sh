#!/usr/bin/env bash

git clone "https://github.com/VTuxers/VPupPr-im.git"

pushd VPupPr-im

git submodule update --init --recursive

chmod u+x setup.sh
./setup.sh

popd
