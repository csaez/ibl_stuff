IBLstuff toolset installation
-----------------------------

## Installer script
We provide a python installer script to manage the installation and
uninstallation of ibl_stuff nuke tools, for more information please type the
following on a terminal:

    python setup.py help


### Manually (deprecated)

Copy entire IBLstuff folder where you want and add path to environment variable
for Nuke plugins.

We recommend as said The Foundry documentation copy to .nuke user folder
(WINDOWS "C:\Users\[user]\.nuke\" OSX and LINUX "/Users/[user]/.nuke/") doing
independent of Nuke versions. Then add entry line plugin path to init.py file.

Example for .nuke/init.py:

    nuke.pluginAddPath("./IBLstuff")
    nuke.pluginAddPath("./IBLstuff/gizmos")
    nuke.pluginAddPath("./IBLstuff/icons")
