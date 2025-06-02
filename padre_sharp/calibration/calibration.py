"""
A module for all things calibration.
"""

from pathlib import Path
import random
import tempfile


from astropy.time import Time

from swxsoc.util import util
from padre_sharp import log
from padre_sharp.util import validation

__all__ = [
    "process_file",
    "calibrate_file",
    "get_calibration_file",
    "read_calibration_file",
]


def process_file(data_filename: Path) -> list:
    """
    This is the entry point for the pipeline processing.
    It runs all of the various processing steps required.

    Parameters
    ----------
    data_filename: str
        Fully specificied filename of an input file

    Returns
    -------
    output_filenames: list
        Fully specificied filenames for the output files.
    """
    log.info(f"Processing file {data_filename}.")
    output_files = []
    data_filename = Path(data_filename)

    if data_filename.suffix in [".bin", ".dat"]:
        # Before we process, validate the file with CCSDS
        custom_validators = [validation.validate_packet_checksums]
        validation_findings = validation.validate(
            data_filename, custom_validators=custom_validators
        )
        for finding in validation_findings:
            log.warning(f"Validation Finding for File : {data_filename} : {finding}")

    calibrated_file = calibrate_file(data_filename)
    output_files.append(calibrated_file)
    #  data_plot_files = plot_file(data_filename)
    #  calib_plot_files = plot_file(calibrated_file)

    # add other tasks below
    return output_files


def calibrate_file(data_filename: Path, output_level=2) -> Path:
    """
    Given an input file, calibrate it and return a new file.

    Parameters
    ----------
    data_filename: str
        Fully specificied filename of the non-calibrated file (data level < 2)
    output_level: int
        The requested data level of the output file.

    Returns
    -------
    output_filename: str
        Fully specificied filename of the non-calibrated file (data level < 2)

    Examples
    --------
    """

    log.info(
        "Despiking removing {num_spikes} spikes".format(
            num_spikes=random.randint(0, 10)
        )
    )
    log.warning(
        "Despiking could not remove {num_spikes}".format(
            num_spikes=random.randint(1, 5)
        )
    )

    file_metadata = util.parse_science_filename(data_filename)

    # Temporary directory
    tmp_dir = Path(tempfile.gettempdir())

    if file_metadata is None:
        log.error(f"Could not parse filename {data_filename}.")
        return None

    print(f"File metadata: {file_metadata}")

    if file_metadata["level"] == "raw":
        if not file_metadata["version"]:
            # If the version is not specified, set it to 0.0.0
            file_metadata["version"] = "0"
        new_filename = tmp_dir / util.create_science_filename(
            instrument=file_metadata["instrument"],
            time=file_metadata["time"],
            version="0.0.0",
            level="l0",
        )
        with open(new_filename, "w"):
            pass

    elif file_metadata["level"] == "l0":
        if not file_metadata["version"]:
            # If the version is not specified, set it to 0.0.0
            file_metadata["version"] = "0"
        new_filename = tmp_dir / util.create_science_filename(
            instrument=file_metadata["instrument"],
            time=file_metadata["time"],
            version=file_metadata["version"],
            level="l1",
        )
        with open(new_filename, "w"):
            pass

    elif file_metadata["level"] == "l1":
        new_filename = tmp_dir / util.create_science_filename(
            instrument=file_metadata["instrument"],
            time=file_metadata["time"],
            version=file_metadata["version"],
            level="ql",
        )

        with open(new_filename, "w"):
            pass
    else:
        log.error(f"Could not calibrate file {data_filename}.")
        raise ValueError(f"Cannot find calibration for file {data_filename}.")

    return new_filename


def get_calibration_file(time: Time) -> Path:
    """
    Given a time, return the appropriate calibration file.

    Parameters
    ----------
    data_filename: str
        Fully specificied filename of the non-calibrated file (data level < 2)
    time: ~astropy.time.Time

    Returns
    -------
    calib_filename: str
        Fully specificied filename for the appropriate calibration file.

    Examples
    --------
    """
    return None


def read_calibration_file(calib_filename: Path):
    """
    Given a calibration, return the calibration structure.

    Parameters
    ----------
    calib_filename: str
        Fully specificied filename of the non-calibrated file (data level < 2)

    Returns
    -------
    output_filename: str
        Fully specificied filename of the appropriate calibration file.

    Examples
    --------
    """

    # if can't read the file

    return None
