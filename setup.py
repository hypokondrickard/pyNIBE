import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyNIBE",
    version = "0.1",
    author = "Rickard Ostman",
    author_email = "rickard@ostman.net",
    description = ("library for interaction with the NIBE UPLINK service"),
    keywords = "nibe heating geothermal home-automation monitoring",
    url = "https://github.com/hypokondrickard/pyNIBE",
    packages=['pyNIBE', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
