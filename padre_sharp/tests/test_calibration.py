import pytest
from pathlib import Path
import tempfile

import padre_sharp.calibration as calib


def test_process_file():
    temp_dir = Path(tempfile.gettempdir())

    # Test with a valid file to l0
    result = calib.process_file(
        Path("padre_sharp/tests/data/PADRESP13_250503042550.DAT")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == temp_dir / Path("padre_sharp_l0_20250503T042550_v0.0.0.fits")

    # Test processing the l0 file to l1
    result = calib.process_file(
        temp_dir / Path("padre_sharp_l0_20250503T042550_v0.0.0.fits")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == temp_dir / Path("padre_sharp_l1_20250503T042550_v0.0.0.fits")

    # Test processing the l1 file to ql
    result = calib.process_file(
        temp_dir / Path("padre_sharp_l1_20250503T042550_v0.0.0.fits")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == temp_dir / Path("padre_sharp_ql_20250503T042550_v0.0.0.fits")
    # Test processing the ql and it raising a ValueError
    with pytest.raises(ValueError) as excinfo:
        calib.process_file(
            temp_dir / Path("padre_sharp_ql_20250503T042550_v0.0.0.fits")
        )


def test_process_file_invalid():
    # Test with an invalid file
    with pytest.raises(ValueError) as excinfo:
        calib.process_file("padre_sharp/tests/data/invalid_file.bin")
    assert str(excinfo.value) == "No valid instrument name found in invalid_file.bin"


def test_calibrate_file():
    with pytest.raises(ValueError) as excinfo:
        calib.calibrate_file("datafile_with_no_calib.cdf")
    assert (
        str(excinfo.value)
        == "No valid instrument name found in datafile_with_no_calib.cdf"
    )


def test_get_calibration_file():
    assert calib.get_calibration_file("") is None


def test_read_calibration_file():
    assert calib.read_calibration_file("calib_file") is None
