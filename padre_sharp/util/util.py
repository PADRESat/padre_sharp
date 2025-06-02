"""
This module provides general utility functions.
"""

import os

from astropy.time import Time
from swxsoc import config


__all__ = ["create_science_filename"]

TIME_FORMAT_L0 = "%Y%j-%H%M%S"
TIME_FORMAT = "%Y%m%dT%H%M%S"
VALID_DESCRIPTORS = ["eventlist", "spec-eventlist", "spec", "xraydirect"]
FILENAME_EXTENSION = ".fits"


def create_science_filename(
    instrument: str,
    time: str,
    level: str,
    version: str,
    descriptor: str = "",
    mode: str = "",
    test: bool = False,
):
    """Return a compliant filename. The format is defined as
    {mission}_{instrument}_{mode}_{level}{test}_{descriptor}_{time}_v{version}.{file_extension}
    This format is only appropriate for data level >= 1.
    Parameters
    ----------
    instrument : `str`
        The instrument name.
    time : `str` (in isot format) or ~astropy.time
        The time
    level : `str`
        The data level. Must be one of the following "raw", "l0", "l1", "l2", "l3", "l4", "ql"
    version : `str`
        The file version which must be given as X.Y.Z
    descriptor : `str`
        An optional file descriptor.
    mode : `str`
        An optional instrument mode.
    test : bool
        Selects whether the file is a test file.
    Returns
    -------
    filename : `str`
        A file name including the given parameters that matches the PADRE file naming conventions
    Raises
    ------
    ValueError: If the instrument is not recognized as one of the PADRE instruments
    ValueError: If the data level is not recognized as one of the PADRE valid data levels
    ValueError: If the data version does not match the PADRE data version formatting conventions
    ValueError: If the data product descriptor or instrument mode do not match the PADRE formatting conventions
    """
    test_str = ""

    # Ensure mode and descriptor are always strings (never None)
    mode = mode or ""
    descriptor = descriptor or ""

    if instrument not in ["sharp"]:
        raise ValueError(f"Instrument, {instrument}, is not recognized.")

    if isinstance(time, str):
        time_str = Time(time, format="isot").strftime(TIME_FORMAT)
    else:
        time_str = time.strftime(TIME_FORMAT)

    if level not in config["mission"]["valid_data_levels"]:
        raise ValueError(
            f"Level, {level}, is not recognized. Must be one of {config["mission"]["valid_data_levels"]}."
        )
    # check that version is in the right format with three parts
    if len(version.split(".")) != 3:
        raise ValueError(
            f"Version, {version}, is not formatted correctly. Should be X.Y.Z"
        )
    # check that version has integers in each part
    for item in version.split("."):
        try:
            int_value = int(item)
        except ValueError:
            raise ValueError(f"Version, {version}, is not all integers.")

    if test is True:
        test_str = "test"

    if descriptor:
        # check that the descriptor is valid
        if descriptor not in VALID_DESCRIPTORS:
            raise ValueError(f"Descriptor, {descriptor}, is not recognized.")
        # the parse_science_filename function depends on _ not being present elsewhere
        if ("_" in mode) or ("_" in descriptor):
            raise ValueError(
                "The underscore symbol _ is not allowed in mode or descriptor."
            )

    filename = (
        f"padre_sharp_{mode}_{level}{test_str}_{descriptor}_{time_str}_v{version}"
    )
    filename = filename.replace("__", "_")  # reformat if mode or descriptor not given

    return filename + FILENAME_EXTENSION
