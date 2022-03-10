"""Utility functions for the workshop."""

from __future__ import print_function
from packaging.version import LegacyVersion as Version
import importlib
import sys

OK = '\x1b[42m[ OK ]\x1b[0m'
FAIL = '\x1b[41m[FAIL]\x1b[0m'
MIN_PYTHON_VERSION, MAX_PYTHON_VERSION = Version('3.8.0'), Version('3.10.2')


def run_env_check():
    """Check that the packages we need are installed and the Python version is high enough."""
    # check the python version
    print('Using Python in %s:' % sys.prefix)
    python_version = Version(sys.version)
    if python_version >= MIN_PYTHON_VERSION and python_version <= MAX_PYTHON_VERSION:
        print(OK, 'Python is version %s\n' % sys.version)
    else:
        print(FAIL, f'Python version >= {MIN_PYTHON_VERSION} and <= {MAX_PYTHON_VERSION} is required, but %s is installed.\n' % sys.version)

    # read in the requirements
    with open('../requirements.txt', 'r') as file:
        requirements = {}
        for line in file.read().splitlines():
            if line.startswith('./'):
                line = line.replace('./', '')
            try:
                pkg, version = line.split('==')
            except ValueError:
                pkg, version = line, None

            requirements[pkg.replace('-', '_')] = version

    # check the requirements
    for pkg, req_version in requirements.items():
        try:
            mod = importlib.import_module(pkg)
            if req_version:
                version = mod.__version__
                if Version(version) != Version(req_version):
                    print(FAIL, '%s version %s is required, but %s installed.' % (pkg, req_version, version))
                    continue
            print(OK, '%s' % pkg)
        except ImportError:
            print(FAIL, '%s not installed.' % pkg)
