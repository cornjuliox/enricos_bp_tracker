import pathlib

from bp_tracker.front.commands import cli_args, parser
from bp_tracker.front.input import add, remove
from bp_tracker.front.output import latest, month, date_range, report
from bp_tracker.back.data_store import BPDataStore


if __name__ == "__main__":
    filepath: str = cli_args.filepath
    path: pathlib.Path = pathlib.Path(filepath)
    store: BPDataStore = BPDataStore(path)
    command: str = cli_args.command

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
