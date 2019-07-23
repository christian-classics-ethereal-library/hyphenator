import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def moduleslist(directory):
    """Return a list with names for all modules under the given directory."""
    folder, basename = os.path.split(directory)
    theList = []
    for file in os.listdir(directory):
        if(file[-3:] == '.py' and file[0] != '_'):
            theList.append(basename + '.' + file[0:-3])
    return theList


setup(
    name="Hyphenator",
    version="0.1.0",
    description="Split words into syllables based on meter, etc.",
    maintainer="zdecook",
    maintainer_email="zdecook@ccel.org",
    url="https://gitlab.ccel.org/zdecook/hymn2yaml",
    package_list=['hyphenator'],
    py_modules=moduleslist('./hyphenator'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'nltk',
        'Pyphen',
        'PyYAML',
    ],
)
