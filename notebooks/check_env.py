"""Check the setup for the workshop."""

from functools import partial
from packaging.version import Version
import importlib
import json
import os
import sys

try:
    import yaml
except ImportError:
    from ruamel import yaml


def _print_version_ok(item):
    """
    Print an OK message for version check.

    Parameters
    ----------
    item : str
        The item being inspected (package, tool, etc.).
    """
    print('\x1b[42m[ OK ]\x1b[0m', '%s' % item)

def _print_version_failure(item, req_version, version, failures):
    """
    Print a failure message for version check.

    Parameters
    ----------
    item : str
        The item being inspected (package, tool, etc.).
    req_version : str
        The required version.
    version : str
        The version currently installed.
    failures : list
        The list of items currently failing the environment check.
    """
    failures.append(item)
    if version:
        msg = '%s version %s is required, but %s installed.'
        values = (item, req_version, version)
    else:
        msg = '%s is not installed.'
        values = item
    print('\x1b[41m[FAIL]\x1b[0m', msg % values)

def run_env_check(raise_exc=False):
    """
    Check that the packages we need are installed and, if necessary,
    whether the Python version is correct.

    Parameters
    ----------
    raise_exc : bool, default ``False``
        Whether to raise an `Exception` if any of the packages doesn't
        match the requirements (used for GitHub Action).
    """
    
    failures = []
    _print_failure = partial(_print_version_failure, failures=failures)

    # read in the environment file and process versions
    with open('../environment.yml', 'r') as file:
        env = yaml.safe_load(file)

    requirements = {}
    for line in env['dependencies']:
        try:
            if '>=' in line:
                pkg, versions = line.split('>=')
                if ',<=' in versions:
                    version = versions.split(',<=')
                else:
                    version = [versions, None]
            else:
                pkg, version = line.split('=')
        except ValueError:
            pkg, version = line, None
        if '-' in pkg:
            continue
        requirements[pkg.split('::')[-1]] = version

    # check the python version, if provided
    try:
        required_version = requirements.pop('python')
        python_version = sys.version_info
        base_python_version = Version(
            f'{python_version.major}.{python_version.minor}.{python_version.micro}'
        )
        if isinstance(required_version, list):
            min_version, max_version = (
                Version(version_str) for version_str in required_version
            )
            if (
                min_version > base_python_version
                or (
                    max_version and base_python_version > max_version
                )
            ):
                print(f'Using Python at {sys.prefix}:\n-> {sys.version}')
                _print_failure(
                    'Python',
                    f'>= {min_version}{f" and <= {max_version}" if max_version else ""}',
                    base_python_version
                )
            else:
                _print_version_ok('Python')
        else:
            for component, value in zip(
                ['major', 'minor', 'micro'], required_version.split('.')
            ):
                if getattr(python_version, component) != int(value):
                    print(f'Using Python at {sys.prefix}:\n-> {sys.version}')
                    _print_failure(
                        'Python',
                        required_version,
                        f'{python_version.major}.{python_version.minor}'
                    )
                    break
            else:
                _print_version_ok('Python')
    except KeyError:
        pass

    for pkg, req_version in requirements.items():
        try:
            mod = importlib.import_module(pkg)
            if req_version:
                version = mod.__version__
                installed_version = Version(version).base_version
                if isinstance(req_version, list):
                    min_version, max_version = req_version
                    if (
                        installed_version < Version(min_version).base_version
                        or (
                            max_version and
                            installed_version > Version(max_version).base_version
                        )
                    ):
                        _print_failure(
                            pkg,
                            f'>= {min_version}{f" and <= {max_version}" if max_version else ""}',
                            version
                        )
                        continue
                elif Version(version).base_version != Version(req_version).base_version:
                    _print_failure(pkg, req_version, version)
                    continue
            _print_version_ok(pkg)
        except ImportError:
            _print_failure(pkg, req_version, None)

    if failures and raise_exc:
        raise Exception(
            'Environment failed inspection due to incorrect versions '
            f'of {len(failures)} item(s): {", ".join(failures)}.'
        )

if __name__ == '__main__':
    print(f'Using Python at {sys.prefix}:\n-> {sys.version}')
    run_env_check(raise_exc=True)
