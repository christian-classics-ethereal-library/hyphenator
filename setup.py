import os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


def moduleslist(directory):
    """Return a list with names for all modules under the given directory."""
    folder, basename = os.path.split(directory)
    theList = []
    for file in os.listdir(directory):
        if(file[-3:] == '.py' and file[0] != '_'):
            theList.append(basename + '.' + file[0:-3])
    return theList


# Override cmdclass with our own install script.
# https://stackoverflow.com/a/29628540/
class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download('cmudict')

setup(
    name="Hyphenator",
    version="0.1.0",
    description="Split words into syllables based on meter, etc.",
    maintainer="zdecook",
    maintainer_email="zdecook@ccel.org",
    url="https://gitlab.ccel.org/zdecook/hyphenator",
    package_list=['hyphenator'],
    py_modules=moduleslist('./hyphenator'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'nltk',
        'Pyphen',
        'PyYAML',
    ],
    cmdclass={'install': Install},
    setup_requires=['nltk'],
)
