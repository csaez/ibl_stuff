IBL Stuff
=========

#### Project overview

Image Based Lighting Tool for Maya and Arnold render is a simple tool with a
well organised user interface that allows look-development artists to easily
load different IBL setups in a Maya scene.

Once the IBL is loaded, the tool should give you the possibility to switch
between IBL's and settings at any time. Deleting (or switching off) previous
loaded IBL's.


#### Desired Features

- Switch between IBL's on the fly
- Thumbnails and useful information
- Hide/Unhide lighting checkers and Macbeth chart
- Hide/Unhide shadow catcher
- Hide/Unhide backplate
- Environment offset controls
- Animation turntables setup
- Have the possibility to animate both rotations, asset and environment
- Setup standard AOV's


#### Installation

> Requires Autodesk Maya >= 2014

Append inner `ibl_stuff` directory to PYTHONPATH (or simply copy it to your
maya/scripts directory).

- **Windows**

```bat
$ cd ibl_stuff
$ set PYTHONPATH=%PYTHONPATH%;%CD%\ibl_stuff
```

- **Unix**

```bash
$ cd ibl_stuff
$ export PYTHONPATH=${PYTHONPATH}:${PWD}/ibl_stuff
```


#### Usage

```python
import ibl_stuff
ibl_stuff.show()
```


#### Contributing

- [Check for open issues](https://github.com/csaez/quicklauncher/issues) or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork the [quicklauncher repository on Github](https://github.com/csaez/quicklauncher) to start making your changes (make sure to isolate your changes in a local branch when possible).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Send a pull request and bug the maintainer until it gets merged and
published. :)

Make sure to add yourself to `CONTRIBUTORS.md`.
