#!/usr/bin/env python

import os
import sys
import shutil

VERSION = 0.1

INFO = """IBL stuff toolset for Nuke.

Common commands:

  setup.py install      will copy and register the tools into ~/.nuke/
  setup.py uninstall    will uninstall the tools

Information display options:

  --help                list all available commands
  --version             print tool version"""

REGISTER = """# Entries plugin path for ibl_stuff toolset
nuke.pluginAddPath("./ibl_stuff")
nuke.pluginAddPath("./ibl_stuff/gizmos")
nuke.pluginAddPath("./ibl_stuff/icons")"""

NUKE_DIR = os.path.join(os.path.expanduser("~"), ".nuke")
INSTALL_DIR = os.path.join(NUKE_DIR, "ibl_stuff")


def install():
    print("Copying files...")
    if not os.path.exists(NUKE_DIR):
        os.mkdir(NUKE_DIR)
    if not os.path.exists(INSTALL_DIR):
        os.mkdir(INSTALL_DIR)
    current_dir = os.path.dirname(__file__)

    shutil.copyfile(os.path.join(current_dir, "menu.py"),
                    os.path.join(INSTALL_DIR, "menu.py"))
    for d in ("gizmos", "icons"):
        shutil.copytree(os.path.join(current_dir, d),
                        os.path.join(INSTALL_DIR, d))

    print("Registering menu...")
    init = ""
    filepath = os.path.join(NUKE_DIR, "init.py")
    if os.path.exists(filepath):
        with open(filepath) as f:
            init = f.read()
    if REGISTER not in init:
        init += "\n" + REGISTER
    with open(filepath, "w") as f:
        f.write(init)

    print("IBL Stuff has been successfully installed on your system.")


def uninstall():
    filepath = os.path.join(NUKE_DIR, "init.py")
    print("Unregistering...")
    reglines = REGISTER.splitlines()
    if os.path.exists(filepath):
        init = list()
        with open(filepath) as f:
            for l in f.readlines():
                if any([r in l for r in reglines]):
                    continue
                init.append(l)
        with open(filepath, "w") as f:
            f.write("".join(init))

    print("Removing files...")
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR)

    print("IBL Stuff has been successfully uninstalled.")


def show_help():
    print(INFO)


def show_version():
    print("IBL Stuff toolset for Nuke version {}".format(VERSION))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("install")
    {
        "install": install,
        "uninstall": uninstall,
        "help": show_help,
        "--help": show_help,
        "-h": show_help,
        "version": show_version,
        "--version": show_version,
        "-v": show_version,
    }.get(sys.argv[1], show_help)()
