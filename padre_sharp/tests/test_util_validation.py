from pathlib import Path

import pytest

import padre_sharp
from padre_sharp.util import validation


def test_validate_packet_checksums():
    # TODO Insert you own test file here - Remove the FileNotFoundError when you have a test file
    with pytest.raises(FileNotFoundError):
        test_file = padre_sharp._test_files_directory / "apid160_4packets.bin"
        warnings = validation.validate_packet_checksums(test_file)
        # assert len(warnings) == 0


def test_validate():
    # TODO Insert you own test file here - Remove the FileNotFoundError when you have a test file
    test_file = padre_sharp._test_files_directory / "apid160_4packets.bin"
    warnings = validation.validate(test_file)
    assert len(warnings) == 1
    assert "No such file or directory:" in warnings[0]
