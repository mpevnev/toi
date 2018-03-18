"""

Read module.

Provides a function to read data from YAML files that searches for such a file
in several locations.

"""

from pathlib import Path
import yaml


def read(*filename):
    """ Read a YAML file. """
    f = Path(*filename)
    try:
        return _try_read(f)
    except FileNotFoundError:
        pass
    try:
        return _try_read(".." / f)
    except FileNotFoundError:
        pass
    return _try_read(Path("/", "usr", "share", "toi", f))


def _try_read(path):
    """ Try reading a YAML file. """
    with open(path) as f:
        res = yaml.safe_load(f)
        if res is None:
            return {}
        return res
