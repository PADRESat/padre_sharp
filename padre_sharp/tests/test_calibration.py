import pytest
import padre_sharp.calibration as calib


def test_calibrate_file():
    with pytest.raises(ValueError) as excinfo:
        calib.calibrate_file("datafile_with_no_calib.cdf")
    assert (
        str(excinfo.value)
        == "File datafile_with_no_calib.cdf not recognized. Not a valid mission name."
    )


def test_get_calibration_file():
    assert calib.get_calibration_file("") is None


def test_read_calibration_file():
    assert calib.read_calibration_file("calib_file") is None
