"""
A module for all things calibration.
"""

from pathlib import Path

from padre_sharp import log
from padre_sharp.util import validation

__all__ = [
    "process_file",
]


def process_file(data_filename: Path) -> list:
    """
    This is the entry point for the pipeline processing.
    It runs all of the various processing steps required.

    Parameters
    ----------
    data_filename: Path
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

    # NOTE: This is stubbed out for now, but should return a real Path object
    calibrated_file = None
    output_files.append(calibrated_file)

    return output_files
