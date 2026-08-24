import tempfile
from pathlib import Path

import padre_sharp.calibration as calib


def test_process_file():
    temp_dir = Path(tempfile.gettempdir())

    # Test with a valid file to l0
    result = calib.process_file(
        Path("padre_sharp/tests/data/PADRESP13_250503042550.DAT")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is None

    # Test processing the l0 file to l1
    result = calib.process_file(
        temp_dir / Path("padre_sharp_l0_20250503T042550_v0.0.0.fits")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is None

    # Test processing the l1 file to ql
    result = calib.process_file(
        temp_dir / Path("padre_sharp_l1_20250503T042550_v0.0.0.fits")
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is None
