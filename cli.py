import pathlib
import logging

from bp_tracker.front.commands import cli_args, parser
from bp_tracker.front.input import add, remove
from bp_tracker.front.output import latest, month, date_range, report
from bp_tracker.back.data_store import BPDataStore
from bp_tracker.front.utils import clamp


logger: logging.Logger = logging.getLogger(__name__)

level: int = cli_args.verbose * 10
if level != 0:
    level = clamp(10, level, 50)
else:
    level = 50

logging_config: dict = {
    "level": level,
    "format": "%(created)i - %(levelname)s - %(name)s - %(message)s",
}

logging.basicConfig(**logging_config)
logging.info("Info logging enabled!")
logging.debug("Debug logging enabled!")

if __name__ == "__main__":
    filepath: str = cli_args.filepath

    path: pathlib.Path = pathlib.Path(filepath)
    logger.debug(f"path: {path}")

    store: BPDataStore = BPDataStore(path)

    command: str = cli_args.command
    logger.debug(f"command: {command}")

    # NOTE: I guess these would be the equivalent of "views"
    dispatch: dict = {
        "add": add,
        "remove": remove,
        "latest": latest,
        "month": month,
        "range": date_range,
        "report": report
    }
    try:
        dispatch[command](cli_args, store)
    except KeyError:
        parser.error(f"Command {cli_args.command} not found! Check -h and try again.")
