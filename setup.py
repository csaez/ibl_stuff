from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

config = {
    "name": "ibl_stuff",
    "description": "",
    "version": "0.1.0",
    "license": "The MIT License",
    "author": "Cesar Saez",
    "author_email": "cesarte@gmail.com",
    "url": "https://www.github.com/csaez/ibl_stuff",
    "packages": find_packages(exclude=["ez_setup", "tests"]),
    "tests_require": ["nose", "coverage", "mock"],
    }

setup(**config)
