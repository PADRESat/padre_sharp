"""
This module provides errors/exceptions and warnings of general use.

Exceptions that are specific to a given package should **not** be here,
but rather in the particular package.

This code is based on that provided by SunPy see
    licenses/SUNPY.rst
"""
import warnings

__all__ = [
    "SHARPWarning",
    "SHARPUserWarning",
    "SHARPDeprecationWarning",
    "SHARPPendingDeprecationWarning",
    "warn_user",
    "warn_deprecated",
]


class SHARPWarning(Warning):
    """
    The base warning class from which all PADRE SHARP warnings should inherit.

    Any warning inheriting from this class is handled by the PADRE SHARP
    logger. This warning should not be issued in normal code. Use
    "SHARPUserWarning" instead or a specific sub-class.
    """


class SHARPUserWarning(UserWarning, SHARPWarning):
    """
    The primary warning class for PADRE SHARP.

    Use this if you do not need a specific type of warning.
    """


class SHARPDeprecationWarning(FutureWarning, SHARPWarning):
    """
    A warning class to indicate a deprecated feature.
    """


class SHARPPendingDeprecationWarning(PendingDeprecationWarning, SHARPWarning):
    """
    A warning class to indicate a soon-to-be deprecated feature.
    """


def warn_user(msg, stacklevel=1):
    """
    Raise a `SHARPUserWarning`.

    Parameters
    ----------
    msg : str
        Warning message.
    stacklevel : int
        This is interpreted relative to the call to this function,
        e.g. ``stacklevel=1`` (the default) sets the stack level in the
        code that calls this function.
    """
    warnings.warn(msg, SHARPUserWarning, stacklevel + 1)


def warn_deprecated(msg, stacklevel=1):
    """
    Raise a `SHARPDeprecationWarning`.

    Parameters
    ----------
    msg : str
        Warning message.
    stacklevel : int
        This is interpreted relative to the call to this function,
        e.g. ``stacklevel=1`` (the default) sets the stack level in the
        code that calls this function.
    """
    warnings.warn(msg, SHARPDeprecationWarning, stacklevel + 1)
