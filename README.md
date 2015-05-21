IBL Stuff
=========

#### Project overview

`IBL Stuff` is an Image Based Lighting Tool for Maya and Arnold renderer, it's a
simple tool with a well organised user interface that allows look-development
artists to easily load different IBL setups in a Maya scene.

Once the IBL is loaded, the tool provide the possibility to switch
between IBL's and settings at any time. Deleting (or switching off) previous
loaded IBL's.


#### Features

* Switch between IBL's on the fly
* Thumbnails and useful information
* Hide/Unhide lighting checkers and Macbeth chart
* Hide/Unhide shadow catcher
* Hide/Unhide backplate
* Environment offset controls
* Animation turntables setup
* Have the possibility to animate both rotations, asset and environment
* Setup standard AOV's


#### Installation

There are several ways to get `ibl_stuff` installed on your system.

* You can install it as a standard python library through its `setup.py`
  script.
* You can clone the repo and add the inner `ibl_stuff` directory to your
  `PYTHONPATH` environment variable.
* You can copy/symlink the inner `ibl_stuff` directory to your `~/maya/scripts`
  directory.

##### ... so many options, what should I choose?

My humble recommendation:
* Users: copy the inner ibl_stuff directory to `~/maya/scripts`
* Developers: run `setup.py` or add the dir to your `PYTHONPATH` (you probably
  already know what suit your needs better).


> Requires Autodesk Maya >= 2014

#### Usage

```python
import ibl_stuff
ibl_stuff.show()
```

Or run it as standalone by typing te following in a terminal

```bash
python -m ibl_stuff
```

### Nuke Tools

In order to produce high quality assets for `ibl stuff`, Alberto has
contributed a nice set of Nuke tools to streamline the IBL creation proccess, you can
install those tools by cloning the repo and typing the following on a terminal:

```bash
python nuke_tools/setup.py
```

> Check other options available by typing `python nuke_tools/setup.py help`.

#### Contributing

* [Check for open issues](https://github.com/csaez/ibl_stuff/issues) or
  open a fresh issue to start a discussion around a feature idea or a bug.
* Fork the [ibl_stuff repository on Github](https://github.com/csaez/ibl_stuff)
  to start making your changes (make sure to isolate your changes in a local
  branch when possible).
* Write a test which shows that the bug was fixed or that the feature works as
  expected.
* Send a pull request and bug the maintainer until it gets merged and
  published. :)

Make sure to add yourself to `CONTRIBUTORS.md`!
