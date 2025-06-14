# see license/LICENSE.rst
import os
from pathlib import Path

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

from padre_sharp.util.config import load_config, print_config
from padre_sharp.util.logger import _init_log

# Get SWXSOC_MISSIONS environment variable if it exists or use default for mission
SWXSOC_MISSION = os.getenv("SWXSOC_MISSION", "padre")
os.environ["SWXSOC_MISSION"] = SWXSOC_MISSION

# Load user configuration
config = load_config()

log = _init_log(config=config)

# Then you can be explicit to control what ends up in the namespace,
__all__ = ["config", "print_config"]

log.debug(f"padre_sharp version: {__version__}")

MISSION_NAME = "PADRE"
INSTRUMENT_NAME = "SHARP"

_package_directory = Path(__file__).parent
_data_directory = _package_directory / "data"
_test_files_directory = _package_directory / "data" / "test"
