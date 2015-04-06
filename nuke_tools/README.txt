IBLstuff toolset installation


Copy entire IBLstuff folder where you want and add path to environment variable
for Nuke plugins.

We recommend as said The Foundry documentation copy to .nuke user folder
(WINDOWS "C:\Users\[user]\.nuke\" OSX and LINUX "/Users/[user]/.nuke/") doing
independent of Nuke versions. Then add entry line plugin path to init.py file.

Example for .nuke/init.py:

    nuke.pluginAddPath("./IBLstuff")
    nuke.pluginAddPath("./IBLstuff/gizmos")
    nuke.pluginAddPath("./IBLstuff/icons")
