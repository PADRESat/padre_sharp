"""Tests for util.py"""

import pytest
import re

from astropy.time import Time
from padre_sharp.util import util

time = "2024-04-06T12:06:21"
time_formatted = "20240406T120621"

good_time = "2025-06-02T12:04:01"
good_instrument = "sharp"
good_level = "l1"
good_version = "1.3.4"


# -------------------------------
# Parametrized: Valid Output Tests
# -------------------------------
@pytest.mark.parametrize(
    "instrument,time,level,descriptor,version,result",
    [
        (
            "sharp",
            time,
            "l1",
            "eventlist",
            "1.2.3",
            f"padre_sharp_l1_eventlist_{time_formatted}_v1.2.3.fits",
        ),
        (
            "sharp",
            time,
            "l2",
            "spec",
            "2.4.5",
            f"padre_sharp_l2_spec_{time_formatted}_v2.4.5.fits",
        ),
        (
            "sharp",
            time,
            "l2",
            "spec-eventlist",
            "1.3.5",
            f"padre_sharp_l2_spec-eventlist_{time_formatted}_v1.3.5.fits",
        ),
        (
            "sharp",
            time,
            "l3",
            "xraydirect",
            "2.4.5",
            f"padre_sharp_l3_xraydirect_{time_formatted}_v2.4.5.fits",
        ),
    ],
)
def test_valid_science_filename_creation(
    instrument, time, level, descriptor, version, result
):
    assert (
        util.create_science_filename(
            instrument, time=time, level=level, descriptor=descriptor, version=version
        )
        == result
    )


# -------------------------------
# Parametrized: Complex Output Tests
# -------------------------------
@pytest.mark.parametrize(
    "instrument,time,level,descriptor,version,mode,test,expected",
    [
        (
            "sharp",
            time,
            "l3",
            "spec",
            "2.4.5",
            "2s",
            False,
            f"padre_sharp_2s_l3_spec_{time_formatted}_v2.4.5.fits",
        ),
        (
            "sharp",
            time,
            "l1",
            "eventlist",
            "2.4.5",
            None,
            True,
            f"padre_sharp_l1test_eventlist_{time_formatted}_v2.4.5.fits",
        ),
        (
            "sharp",
            time,
            "l3",
            "spec",
            "2.4.5",
            "2s",
            True,
            f"padre_sharp_2s_l3test_spec_{time_formatted}_v2.4.5.fits",
        ),
        (
            "sharp",
            Time(time),
            "l3",
            "spec",
            "2.4.5",
            "2s",
            True,
            f"padre_sharp_2s_l3test_spec_{time_formatted}_v2.4.5.fits",
        ),
        (
            "sharp",
            Time(2460407.004409722, format="jd"),
            "l3",
            "eventlist",
            "2.4.5",
            "2s",
            True,
            f"padre_sharp_2s_l3test_eventlist_{time_formatted}_v2.4.5.fits",
        ),
    ],
)
def test_valid_science_filename_creation_complex(
    instrument, time, level, descriptor, version, mode, test, expected
):
    assert (
        util.create_science_filename(
            instrument,
            time,
            level=level,
            descriptor=descriptor,
            version=version,
            mode=mode,
            test=test,
        )
        == expected
    )


# -------------------------------
# Parametrized: Error Creation Tests
# -------------------------------
@pytest.mark.parametrize(
    "instrument,time,level,version,descriptor,mode",
    [
        # Bad version specifications
        (good_instrument, good_time, good_level, "1.3", "eventlist", None),
        (good_instrument, good_time, good_level, "1", "eventlist", None),
        (good_instrument, good_time, good_level, "1.5.6.7", "eventlist", None),
        (good_instrument, good_time, good_level, "1..", "eventlist", None),
        (good_instrument, good_time, good_level, "a.5.6", "eventlist", None),
        # Wrong level specifications
        (good_instrument, good_time, "la", good_version, "eventlist", None),
        (good_instrument, good_time, "squirrel", good_version, "eventlist", None),
        # Wrong instrument names
        ("potato", good_time, good_level, good_version, "eventlist", None),
        ("eeb", good_time, good_level, good_version, "eventlist", None),
        ("fpi", good_time, good_level, good_version, "eventlist", None),
        # Invalid time formats
        (
            good_instrument,
            "2023-13-04T12:06:21",
            good_level,
            good_version,
            "eventlist",
            None,
        ),
        (
            good_instrument,
            "2023/13/04 12:06:21",
            good_level,
            good_version,
            "eventlist",
            None,
        ),
        (good_instrument, "12345345", good_level, good_version, "eventlist", None),
        # Invalid characters in mode and descriptor
        ("eeb", "12345345", good_level, good_version, "eventlist", "o_o"),
        ("eeb", "12345345", good_level, good_version, "blue_green", None),
    ],
)
def test_invalid_science_filename_creation(
    instrument, time, level, version, descriptor, mode
):
    with pytest.raises(ValueError):
        util.create_science_filename(
            instrument,
            time,
            descriptor=descriptor,
            level=level,
            version=version,
            mode=mode,
        )


# fmt: off

# REQUIRED SECTION FOR SWXSOC SCIENCE FILENAMES ###########################################
# Theses tests are required and need to pass to ensure that the SWXSOC science filenames
# are generated correctly and adhere to the required format for standardization.
# If you are have any questions about these tests, please reach out to the SWXSOC team.
#############################################################################################
@pytest.mark.parametrize(
    "expected_mission, expected_instrument, expected_time, expected_formatted_time, expected_level, expected_descriptor, expected_version, expected_file_extension, expected_filename",
    [
        ("padre", "sharp", time, time_formatted, "l1", "eventlist", "1.2.3", "fits", f"padre_sharp_l1_eventlist_{time_formatted}_v1.2.3.fits"),
        ("padre", "sharp", time, time_formatted, "l2", "spec", "2.4.5", "fits", f"padre_sharp_l2_spec_{time_formatted}_v2.4.5.fits"),
        ("padre", "sharp", time, time_formatted, "l2", "spec-eventlist", "1.3.5", "fits", f"padre_sharp_l2_spec-eventlist_{time_formatted}_v1.3.5.fits"),
        ("padre", "sharp", time, time_formatted, "l3", "xraydirect", "2.4.5", "fits", f"padre_sharp_l3_xraydirect_{time_formatted}_v2.4.5.fits"),
        ("padre", "sharp", time, time_formatted, "l1", "", "1.0.0", "fits", f"padre_sharp_l1_{time_formatted}_v1.0.0.fits"),  # Blank descriptor test
        ("padre", "sharp", time, time_formatted, "l2", "eventlist", "1.2.3", "fits", f"padre_sharp_l2test_eventlist_{time_formatted}_v1.2.3.fits"),  # Test file
    ],
)
def test_validate_swxsoc_science_filename(
    expected_mission, expected_instrument, expected_time, expected_formatted_time,
    expected_level, expected_descriptor, expected_version, expected_file_extension, expected_filename
):
    """
    Validate that filenames generated by `create_science_filename` conform to the SWXSOC naming convention.

    This test ensures:
    - Instrument teams can define their own `create_science_filename` implementations.
    - Filenames adhere to SWXSOC's required format.
    - Handling of blank descriptors is correct.
    - Test files are properly labeled with "test" in their filename.
    """
    # Generate filename using the function under test
    created_filename = util.create_science_filename(
        expected_instrument,
        Time(expected_time),
        expected_level,
        expected_version,
        expected_descriptor,
        test="test" in expected_filename,
    )

    # Ensure generated filename matches expectation
    assert created_filename == expected_filename, f"Generated filename {created_filename} does not match expected {expected_filename}"

    # Define expected filename pattern
    pattern = r"^(\w+)_(\w+)(?:_(\w+))?_(l[0-4]|ql)(test)?(?:_(\w+(?:-\w+)*))?_(\d{8}T\d{6})_v(\d+\.\d+\.\d+)?\.(\w+)$"
    match = re.match(pattern, expected_filename)

    # Validate filename format
    assert match, f"Filename {expected_filename} does not match expected format"

    # Extract matched groups
    mission, instrument, mode, level, test_flag, descriptor, time_str, version, extension = match.groups()

    # Ensure parsed values align with expected values
    assert mission == expected_mission, f"Mission mismatch: expected {expected_mission}, got {mission}"
    assert instrument == expected_instrument, f"Instrument mismatch: expected {expected_instrument}, got {instrument}"
    assert level == expected_level, f"Level mismatch: expected {expected_level}, got {level}"
    assert (descriptor or "") == expected_descriptor, f"Descriptor mismatch: expected {expected_descriptor}, got {descriptor}"
    assert version == expected_version, f"Version mismatch: expected {expected_version}, got {version}"
    assert extension == expected_file_extension, f"File extension mismatch: expected {expected_file_extension}, got {extension}"
    assert time_str == expected_formatted_time, f"Time format mismatch: expected {expected_formatted_time}, got {time_str}"
    assert (test_flag == "test") == ("test" in expected_filename), f"Test flag mismatch in filename {expected_filename}"
# fmt: on
