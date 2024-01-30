#!/usr/bin/env python3

import os
from pathlib import Path
import shutil


def find_available_file(files, base_path=Path("/usr")):
    for f in files:
        if list(base_path.glob(f)):
            f = str(f).replace("*", "\\*")
            return f

    return None


if __name__ == "__main__":
    ############
    # Build godot
    os.system("./setup_godot.sh")
    godot_dir = Path("godot")
    godot_exec = godot_dir / "bin/godot.linuxbsd.editor.x86_64"

    ############
    # Build GDMP
    os.system(
        "git clone --depth=1 --recurse-submodules https://github.com/j20001970/GDMP.git"
    )

    # Find opencv files installed on the system
    gdmp_dir = Path("GDMP")
    gdmp_opencv_file = gdmp_dir / "mediapipe/third_party/opencv_linux.BUILD"

    base_path = Path("/usr")
    opencv_headers_files = [
        "include/aarch64-linux-gnu/opencv4/opencv2/cvconfig.h",
        "include/arm-linux-gnueabihf/opencv4/opencv2/cvconfig.h",
        "include/x86_64-linux-gnu/opencv4/opencv2/cvconfig.h",
        "include/opencv4/opencv2/**/*.h*",
    ]

    opencv_include_dirs = [
        "include/aarch64-linux-gnu/opencv4/",
        "include/arm-linux-gnueabihf/opencv4/",
        "include/x86_64-linux-gnu/opencv4/",
        "include/opencv4/",
    ]

    available_header = find_available_file(opencv_headers_files, base_path)
    if not available_header:
        print("Failed to find opencv header. Make sure opencv installed.")
        exit(-1)

    available_include_dir = find_available_file(opencv_include_dirs, base_path)
    if not available_include_dir:
        print("Failed to find opencv include dir. Make sure opencv is installed.")
        exit(-2)

    replace_cmd = (
        f'sed -i \'s:#"{available_header}":"{available_header}":\' {gdmp_opencv_file}'
    )
    print(replace_cmd)
    os.system(replace_cmd)

    replace_cmd = f'sed -i \'s:#"{available_include_dir}":"{available_include_dir}":\' {gdmp_opencv_file}'
    print(replace_cmd)
    os.system(replace_cmd)

    os.system(f"./setup_gdmp.sh {godot_exec}")

    ############
    # Build VPuppr
    os.system("./setup_vpuppr.sh")
    vpuppr_dir = Path("VPupPr-im")

    # Add GDMP to VPuppr
    shutil.copytree(
        f"{gdmp_dir}/addons/GDMP/libs",
        f"{vpuppr_dir}/addons/GDMP/libs/",
        dirs_exist_ok=True,
    )
    shutil.copy2(
        f"{gdmp_dir}/addons/GDMP/GDMP.gdextension", f"{vpuppr_dir}/addons/GDMP/"
    )
