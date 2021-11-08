from .commands import *

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # < Python 3.8: Use backport module
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
    del version
except PackageNotFoundError:
    pass
