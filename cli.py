import argparse
import datetime
import json
import pathlib
from copy import deepcopy

from datetime import timezone

import arrow
from rich import print
from rich.console import Console
from rich.table import Table

# NOTE: This is needed to convert timestamps to the correct local timezone.
# NOTE: It's also really ugly looking lol
SYSTZ: timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

parser = argparse.ArgumentParser()
parser.add_argument(
    "filepath",
    type=str,
    help="Full/relative path to the database file. If it doesn't exist it will be created."
)
subparser = parser.add_subparsers(help="sub-commands", dest="command")

add_command = subparser.add_parser("add", help="adds an entry to the log")
add_command.add_argument("sys", type=int, help="Systolic pressure, read from the machine, needs to be a number.")
add_command.add_argument("dia", type=int, help="Diastolic pressure, read from the machine, needs to be a number.")
add_command.add_argument("pulse", type=int, help="Pulse value, read from the machine, needs to be a number.")
add_command.add_argument("notes", type=str, help="Any important notes you'd like to add. Has to be a string wrapped in double quotes.")

remove_command = subparser.add_parser("remove", help="removes an entry from the log.")
remove_command.add_argument("timestamp", type=int, help="refers to the exact")

latest_command = subparser.add_parser("latest", help="shows the latest N items, use --limit to specify how many.")
latest_command.add_argument("--limit", type=int, help="how many items would you like to see?")

cli_args = parser.parse_args()

# NOTE: There is apparently no way to do this within argparse.
# NOTE: This workaround will serve until I find a better one.
if cli_args.command is None:
    parser.error("Need to specify a subcommand, run with -h flag to see the list of subcommands.")

class BPDataStore():
    def __init__(self, path: pathlib.Path):
        self.path = path
        if self.path.exists():
            with self.path.open("r") as F:
                self._bpdata: list[dict] = json.loads(F.read())
        else:
            self._bpdata: list[dict] = {}

    def _commit(self):
        with self.path.open("w") as F:
            F.write(json.dumps(self._bpdata))
    
    def latest(self, limit: int = 10, ascending: bool = False):
        if limit <= 0:
            limit: int = 1
        if limit > len(self._bpdata):
            limit: int = len(self._bpdata) - 1

        if ascending:
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])
        else:
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])[::-1]

        return prepped

    def all(self):
        return self._bpdata

    def specific_month(self, start: int):
        # NOTE: 'end' is derived from start
        # NOTE: Need to figure out how to do datepicker stuff via CLI
        #       maybe just restrict it to a specific syntax? Or I could
        #       just pass unsanitized input straight to Arrow and let it
        #       raise an exception when it's wrong.
        pass

    def add(self, sys: int, dia: int, pulse: int, notes: int, timestamp: int):
        data: dict = {
            "sys": sys,
            "dia": dia,
            "pulse": pulse,
            "notes": notes,
            "timestamp": timestamp
        }

        self._bpdata.append(data)
        self._commit()

    # NOTE: There should never be a need to 'edit' an entry, I hope.
    def remove(self, timestamp: int):
        new_list: list[dict] = [x for x in self._bpdata if x.get("timestamp") != timestamp]
        self._bpdata = new_list
        self._commit()

def _add(cli_args: argparse.Namespace, store: BPDataStore):
    store.add(
        sys=cli_args.sys,
        dia=cli_args.dia,
        pulse=cli_args.pulse,
        notes=cli_args.notes,
        timestamp=int(arrow.now().timestamp())
    )

def _remove(cli_args: argparse.Namespace, store: BPDataStore):
    timestamp: int = int(cli_args.timestamp)
    store.remove(timestamp)

def _make_readable_timestamps(rows: list[dict]) -> list[dict]:
    rows_copy: list[dict] = deepcopy(rows)
    for row in rows_copy:
        int_timestamp: int = row["timestamp"]
        arrow_timestamp: arrow.Arrow = arrow.get(int_timestamp)
        local_arrow_timestamp: arrow.Arrow = arrow_timestamp.to(SYSTZ)
        row["timestamp"] = local_arrow_timestamp.format()

    return rows_copy

def _latest(cli_args: argparse.Namespace, store: BPDataStore):
    console: Console = Console()  # TODO: Move this up later because it can be module level
    table: Table = Table(title="Latest BP measurements, in descending order by time.")

    table.add_column("Sys")
    table.add_column("Dia")
    table.add_column("Pulse")
    table.add_column("Notes")
    table.add_column("Timestamp")

    if cli_args.limit is not None:
        limit: int = cli_args.limit
    else:
        limit: int = 10
    
    raw_rows: list[dict] = store.latest(limit)
    rows: list[dict] = _make_readable_timestamps(raw_rows)

    for x in rows:
        table.add_row(str(x["sys"]), str(x["dia"]), str(x["pulse"]), str(x["notes"]), str(x["timestamp"]))

    console.print(table)

if __name__ == "__main__":
    filepath: str = cli_args.filepath
    path: pathlib.Path = pathlib.Path(filepath)
    print(cli_args)

    store: BPDataStore = BPDataStore(path)
    command: str = cli_args.command
    dispatch: dict = {
        "add": _add,
        "remove": _remove,
        "latest": _latest,
    }

    try:
        dispatch[command](cli_args, store)
    except KeyError:
        parser.error(f"Command {cli_args.command} not found! Check -h and try again.")
