#!/usr/bin/env bash

# Get GDMP repo
git clone https://github.com/j20001970/GDMP

YELLOW='\033[1;32m'
NOCOLOR='\033[0m'

echo -e "${YELLOW}Run this command with a parameter pointing to the godot editor binary, as './setup.py PATH/TO/GODOT_BIN'${NOCOLOR}"
echo -e "${YELLOW}If you're not using Ubuntu, edit GDMP/mediapipe/third_party/opencv_linux.BUILD so that hrdrs and includes point to the opencv headers${NOCOLOR}"
echo -e "${YELLOW}For example, on Arch Linux, uncomment 'include/opencv4/opencv2/**/*.h*' and 'include/opencv4/'${NOCOLOR}"
sleep 5

case "$1" in
  /*) GODOT_BIN="$1" ;;
  *) GODOT_BIN="$PWD/$1" ;;
esac

echo "Godot binary: $GODOT_BIN"

# Compilation setup
pushd GDMP

git submodule update --init --recursive --depth=1

# Comment out mentions of hedron_compile_commands
git apply ../comment_hedron.patch

# Setup build environment
./setup.py
source ./venv/bin/activate


./setup.py --godot-binary "$GODOT_BIN"

# Build GDMP library
./build.py desktop

# Copy library to addons folder
chmod u+rw mediapipe/bazel-bin/GDMP/desktop/libGDMP.so
mkdir -p addons/GDMP/libs/x86_64/
cp mediapipe/bazel-bin/GDMP/desktop/libGDMP.so addons/GDMP/libs/x86_64/libGDMP.linux.debug.so
cp mediapipe/bazel-bin/GDMP/desktop/libGDMP.so addons/GDMP/libs/x86_64/libGDMP.linux.release.so

deactivate

popd

echo -e "${YELLOW}Build done. Copy the GDMP/addons directory to your Godot project directory.${NOCOLOR}"
